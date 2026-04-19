import os
import hashlib
from typing import Dict, List
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from dotenv import load_dotenv

load_dotenv()



_sessions: Dict[str, List] = {}


COACH_SYSTEM_PROMPT_TEMPLATE = """You are AcadIQ Coach — a warm, encouraging study assistant and academic mentor.

Your PRIMARY job is to help the student understand and improve on their specific weaknesses listed below.
Always bring the conversation back to their actual data when relevant.

You can discuss: studying, academics, exams, student wellness, focus, burnout, sleep, learning strategies, and the student's AcadIQ profile.
Only decline requests that are clearly harmful, illegal, or have absolutely nothing to do with student life.
For borderline topics (stress, motivation, life balance), engage helpfully — these affect academics too.

─── Student Profile ───────────────────────────────────────────
Predicted Exam Score : {student_score}/100
Classification       : {classification} (Pass Probability: {pass_probability}%)
Learner Archetype    : {learner_type}
Top Weaknesses       : {top_weaknesses}
───────────────────────────────────────────────────────────────

Guidelines:
1. When the student asks about improvement, ALWAYS reference their specific weaknesses above by name
2. Be warm and specific — never generic
3. Give concrete, actionable steps tied to their actual numbers
4. Ask follow-up questions to understand their situation
5. Keep replies to 3–5 sentences unless generating a full plan
6. Think step by step before answering"""


def _get_llm() -> ChatGroq:
    return ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0.7,
        groq_api_key=os.getenv("GROQ_API_KEY"),
    )


def _format_weaknesses(top_weaknesses: list) -> str:
    if not top_weaknesses:
        return "No significant weaknesses identified"
    parts = []
    for w in top_weaknesses:
        if isinstance(w, dict):
            feature = w.get("feature", "")
            student_val = w.get("student_value", 0)
            avg = w.get("dataset_average", 0)
            parts.append(f"{feature} ({student_val:.1f} vs avg {avg:.1f})")
        else:
            parts.append(str(w))
    return ", ".join(parts)


def _build_system_message(student_profile: dict) -> SystemMessage:
    weaknesses_list = student_profile.get("top_weaknesses", [])
    content = COACH_SYSTEM_PROMPT_TEMPLATE.format(
        student_score=student_profile.get("predicted_score", "N/A"),
        classification=student_profile.get("classification", "N/A"),
        pass_probability=student_profile.get("pass_probability", "N/A"),
        learner_type=student_profile.get("learner_type", "N/A"),
        top_weaknesses=_format_weaknesses(weaknesses_list),
    )
    return SystemMessage(content=content)


def get_or_create_session(user_email: str) -> List:
    if user_email not in _sessions:
        _sessions[user_email] = []
    return _sessions[user_email]


def chat(user_email: str, message: str, student_profile: dict) -> str:
    llm = _get_llm()
    history = get_or_create_session(user_email)

    system_msg = _build_system_message(student_profile)
    messages = [system_msg] + history + [HumanMessage(content=message)]

    response = llm.invoke(messages)
    reply = response.content


    history.append(HumanMessage(content=message))
    history.append(AIMessage(content=reply))

    return reply


def diagnose(student_profile: dict) -> dict:
    llm = _get_llm()
    weaknesses_str = _format_weaknesses(student_profile.get("top_weaknesses", []))

    prompt = f"""You are an expert academic coach. Analyze this student's profile and identify their 3 most critical learning gaps.

Student Profile:
- Predicted Score: {student_profile.get('predicted_score', 'N/A')}/100
- Classification: {student_profile.get('classification', 'N/A')}
- Pass Probability: {student_profile.get('pass_probability', 'N/A')}%
- Learner Type: {student_profile.get('learner_type', 'N/A')}
- Top Weaknesses: {weaknesses_str}

Think step by step (chain-of-thought reasoning). Then provide:
1. Three specific learning gaps (one sentence each)
2. A brief explanation of why each gap is critical

Format your response as:
GAP 1: [gap description]
GAP 2: [gap description]
GAP 3: [gap description]
REASONING: [your chain-of-thought explanation]"""

    response = llm.invoke([HumanMessage(content=prompt)])
    content = response.content

    gaps = []
    reasoning = ""
    for line in content.split("\n"):
        line = line.strip()
        if line.startswith("GAP 1:") or line.startswith("GAP 2:") or line.startswith("GAP 3:"):
            gap_text = line.split(":", 1)[1].strip() if ":" in line else line
            gaps.append(gap_text)
        elif line.startswith("REASONING:"):
            reasoning = line.split(":", 1)[1].strip() if ":" in line else ""

    if not gaps:
        gaps = [l.strip() for l in content.split("\n") if l.strip() and not l.startswith("REASONING")][:3]
    if not reasoning:
        reasoning = content

    return {"gaps": gaps[:3], "reasoning": reasoning}


def generate_plan(student_profile: dict, resources: list[dict]) -> dict:
    llm = _get_llm()
    weaknesses_str = _format_weaknesses(student_profile.get("top_weaknesses", []))

    resources_text = "\n".join([
        f"- {r.get('title', '')}: {r.get('description', '')} ({r.get('url', '')})"
        for r in resources
    ])

    prompt = f"""Generate a personalized 7-day study plan for this student.

Student Profile:
- Predicted Score: {student_profile.get('predicted_score', 'N/A')}/100
- Classification: {student_profile.get('classification', 'N/A')}
- Pass Probability: {student_profile.get('pass_probability', 'N/A')}%
- Learner Type: {student_profile.get('learner_type', 'N/A')}
- Top Weaknesses: {weaknesses_str}

Available Resources:
{resources_text}

Format the plan EXACTLY as:
Day 1: [Focus Area] — [Specific Task] — [Time]
Day 2: [Focus Area] — [Specific Task] — [Time]
Day 3: [Focus Area] — [Specific Task] — [Time]
Day 4: [Focus Area] — [Specific Task] — [Time]
Day 5: [Focus Area] — [Specific Task] — [Time]
Day 6: [Focus Area] — [Specific Task] — [Time]
Day 7: [Focus Area] — [Specific Task] — [Time]
Weekly Goal: [One measurable goal]"""

    response = llm.invoke([HumanMessage(content=prompt)])
    content = response.content

    weekly_goal = ""
    plan_lines = []
    for line in content.split("\n"):
        line = line.strip()
        if line.startswith("Weekly Goal:"):
            weekly_goal = line.split(":", 1)[1].strip() if ":" in line else ""
        elif line.startswith("Day "):
            plan_lines.append(line)

    plan = "\n".join(plan_lines) if plan_lines else content
    if not weekly_goal:
        score = student_profile.get("predicted_score", 0)
        weekly_goal = f"Improve predicted score from {score:.0f} to {min(100, score + 10):.0f} through consistent daily study."

    return {"plan": plan, "weekly_goal": weekly_goal}


def reset_memory(user_email: str) -> None:
    if user_email in _sessions:
        del _sessions[user_email]


def get_session_id(user_email: str) -> str:
    return hashlib.md5(user_email.encode()).hexdigest()[:12]