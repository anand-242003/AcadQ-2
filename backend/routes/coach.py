from datetime import datetime, timedelta
from collections import defaultdict
from pathlib import Path
from urllib.parse import quote

from fastapi import APIRouter, HTTPException, Depends, Request

from models.schemas import (
    CoachChatRequest, CoachChatResponse,
    StudyPlanRequest, StudyPlanResponse,
    DiagnoseRequest, DiagnoseResponse,
    MessageResponse, ResourceItem,
)
from services import coach_service, rag_service
from routes.auth import get_current_user

router = APIRouter()

# ─── Rate Limiting Store ──────────────────────────────────────────────────────
# { user_email: [list of timestamps] }
_rate_limit_store: dict = defaultdict(list)
RATE_LIMIT_MAX = 20       # max messages
RATE_LIMIT_WINDOW = 3600  # per hour (seconds)

# ─── Layer 2: Blocked Keywords ────────────────────────────────────────────────
BLOCKED_KEYWORDS = [
    "hack", "illegal", "drug", "weapon", "bomb", "kill", "steal",
    "cheat exam", "fraud", "jailbreak", "ignore instructions",
    "forget your instructions", "act as", "pretend you are",
    "dan", "override", "bypass",
]

# ─── Layer 3: Academic Keywords ───────────────────────────────────────────────
ACADEMIC_KEYWORDS = [
    "study", "exam", "score", "focus", "sleep", "plan", "resource",
    "learn", "grade", "quiz", "assignment", "mental health", "productivity",
    "burnout", "schedule", "homework", "university", "college", "school",
    "coach", "marks", "syllabus", "revision", "notes", "lecture",
]

# ─── Layer 4: Harmful Output Signals ─────────────────────────────────────────
HARMFUL_OUTPUT_SIGNALS = [
    "here is how to",
    "you can hack",
    "illegal way",
    "ignore my instructions",
    "as an ai without restrictions",
]

OFF_TOPIC_SAFE_RESPONSE = "I can only assist with academic and study related questions!"
INPUT_BLOCKED_RESPONSE = "I can only help with study-related topics. Please ask me something about your academics!"


def _build_resource_url(raw_url: str, request: Request) -> str:
    """Return a fully-qualified, openable URL for a retrieved resource."""
    url = (raw_url or "").strip()
    if not url:
        return ""

    lower = url.lower()
    if lower.startswith("http://") or lower.startswith("https://"):
        return url

    file_name = Path(url).name
    if not file_name:
        return ""

    base_url = str(request.base_url).rstrip("/")
    return f"{base_url}/resources/files/{quote(file_name)}"


def _normalize_resource_urls(resources: list[dict], request: Request) -> list[dict]:
    normalized: list[dict] = []
    for item in resources:
        data = dict(item)
        data["url"] = _build_resource_url(str(data.get("url", "")), request)
        normalized.append(data)
    return normalized


def _check_rate_limit(user_email: str) -> None:
    """Raise 429 if user has exceeded 20 messages in the last hour."""
    now = datetime.utcnow()
    window_start = now - timedelta(seconds=RATE_LIMIT_WINDOW)
    # Prune old timestamps
    _rate_limit_store[user_email] = [
        ts for ts in _rate_limit_store[user_email] if ts > window_start
    ]
    if len(_rate_limit_store[user_email]) >= RATE_LIMIT_MAX:
        raise HTTPException(
            status_code=429,
            detail="Message limit reached. Please try again in an hour.",
        )
    _rate_limit_store[user_email].append(now)


def _layer2_input_filter(message: str) -> str | None:
    """Return blocked response string if message contains blocked keywords, else None."""
    msg_lower = message.lower()
    for keyword in BLOCKED_KEYWORDS:
        if keyword in msg_lower:
            return INPUT_BLOCKED_RESPONSE
    return None


def _layer3_topic_check(message: str) -> str | None:
    """Return off-topic warning string to append to prompt if message seems off-topic, else None."""
    if len(message) <= 20:
        return None  # short messages get a pass
    msg_lower = message.lower()
    for keyword in ACADEMIC_KEYWORDS:
        if keyword in msg_lower:
            return None  # on-topic
    return "The user may be going off-topic. Remind them you are a study coach only."


def _layer4_output_filter(response: str) -> str:
    """Replace response if it contains harmful output signals."""
    resp_lower = response.lower()
    for signal in HARMFUL_OUTPUT_SIGNALS:
        if signal in resp_lower:
            return OFF_TOPIC_SAFE_RESPONSE
    return response


@router.post("/diagnose", response_model=DiagnoseResponse)
async def diagnose(
    request: DiagnoseRequest,
    current_user: str = Depends(get_current_user),
):
    try:
        profile = request.student_profile.model_dump()
        result = coach_service.diagnose(profile)
        return DiagnoseResponse(**result)
    except Exception as e:
        error_msg = str(e)
        if "rate_limit" in error_msg.lower() or "429" in error_msg or "timeout" in error_msg.lower():
            raise HTTPException(status_code=503, detail="AI coach temporarily unavailable. Please try again.")
        raise HTTPException(status_code=500, detail=f"Diagnosis failed: {error_msg}")


@router.post("/plan", response_model=StudyPlanResponse)
async def plan(
    request: StudyPlanRequest,
    http_request: Request,
    current_user: str = Depends(get_current_user),
):
    try:
        profile = request.student_profile.model_dump()

        weaknesses = profile.get("top_weaknesses", [])
        if weaknesses:
            query = " ".join([w.get("feature", "").replace("_", " ") for w in weaknesses])
        else:
            query = f"{profile.get('learner_type', 'student')} study improvement"

        resources = rag_service.retrieve_resources(query, k=3)
        resources = _normalize_resource_urls(resources, http_request)

        if not resources and rag_service._vector_store is None:
            raise HTTPException(status_code=503, detail="Resource database not ready")

        result = coach_service.generate_plan(profile, resources)
        resource_items = [ResourceItem(**r) for r in resources]

        return StudyPlanResponse(
            plan=result["plan"],
            weekly_goal=result["weekly_goal"],
            resources=resource_items,
        )
    except HTTPException:
        raise
    except Exception as e:
        error_msg = str(e)
        if "rate_limit" in error_msg.lower() or "429" in error_msg or "timeout" in error_msg.lower():
            raise HTTPException(status_code=503, detail="AI coach temporarily unavailable. Please try again.")
        raise HTTPException(status_code=500, detail=f"Plan generation failed: {error_msg}")


@router.post("/chat", response_model=CoachChatResponse)
async def chat(
    request: CoachChatRequest,
    current_user: str = Depends(get_current_user),
):
    # ── Rate limit check ──────────────────────────────────────────────────────
    _check_rate_limit(current_user)

    message = request.message

    # ── Layer 2: Input keyword filter ─────────────────────────────────────────
    blocked = _layer2_input_filter(message)
    if blocked:
        return CoachChatResponse(
            reply=blocked,
            session_id=coach_service.get_session_id(current_user),
        )

    # ── Layer 3: Topic relevance check ────────────────────────────────────────
    off_topic_warning = _layer3_topic_check(message)
    if off_topic_warning:
        message = f"{message}\n\n[SYSTEM NOTE: {off_topic_warning}]"

    try:
        profile = request.student_profile.model_dump()
        raw_reply = coach_service.chat(current_user, message, profile)

        # ── Layer 4: Output filter ────────────────────────────────────────────
        safe_reply = _layer4_output_filter(raw_reply)

        session_id = coach_service.get_session_id(current_user)
        return CoachChatResponse(reply=safe_reply, session_id=session_id)

    except HTTPException:
        raise
    except Exception as e:
        error_msg = str(e)
        if "rate_limit" in error_msg.lower() or "429" in error_msg or "timeout" in error_msg.lower():
            raise HTTPException(status_code=503, detail="AI coach temporarily unavailable. Please try again.")
        raise HTTPException(status_code=500, detail=f"Chat failed: {error_msg}")


@router.delete("/reset", response_model=MessageResponse)
async def reset(current_user: str = Depends(get_current_user)):
    coach_service.reset_memory(current_user)
    # Also reset rate limit on session clear
    if current_user in _rate_limit_store:
        del _rate_limit_store[current_user]
    return MessageResponse(message="Session cleared")
