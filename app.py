import os
import base64
import hashlib
import hmac
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import requests
import streamlit as st


DEFAULT_API_URL = os.getenv("ACADIQ_API_URL", "http://127.0.0.1:8000")
REQUEST_TIMEOUT = 45
FALLBACK_SECRET = "fallback-secret-key-change-in-production"


def _parse_simple_env_file(path: Path) -> dict[str, str]:
    env_vars: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
        env_vars[key.strip()] = value.strip().strip('"').strip("'")
    return env_vars


def load_jwt_settings() -> dict[str, Any]:
    secret = os.getenv("ACADIQ_JWT_SECRET", "").strip()
    algorithm = os.getenv("ACADIQ_JWT_ALGORITHM", "").strip()
    expire_raw = os.getenv("ACADIQ_JWT_EXPIRE_DAYS", "").strip()
    source = "environment variables"

    if not secret:
        env_path = Path(__file__).resolve().parent / "backend" / ".env"
        if env_path.exists():
            env_data = _parse_simple_env_file(env_path)
            secret = env_data.get("SECRET_KEY", "").strip()
            algorithm = algorithm or env_data.get("JWT_ALGORITHM", "").strip()
            expire_raw = expire_raw or env_data.get("JWT_EXPIRE_DAYS", "").strip()
            source = str(env_path)

    if not secret:
        secret = FALLBACK_SECRET
        source = "backend fallback secret"

    if not algorithm:
        algorithm = "HS256"

    try:
        expire_days = int(expire_raw) if expire_raw else 7
    except ValueError:
        expire_days = 7

    return {
        "secret": secret,
        "algorithm": algorithm,
        "expire_days": expire_days,
        "source": source,
    }


def _b64url_encode(raw: bytes) -> str:
    return base64.urlsafe_b64encode(raw).rstrip(b"=").decode("ascii")


def create_dev_token(email: str) -> tuple[str, str]:
    settings = load_jwt_settings()
    if settings["algorithm"] != "HS256":
        raise ValueError(
            "Quick session supports HS256 only. "
            "Set ACADIQ_JWT_ALGORITHM=HS256 or use manual token login."
        )

    header = {"alg": "HS256", "typ": "JWT"}
    expiry = datetime.now(timezone.utc) + timedelta(days=settings["expire_days"])
    payload = {"sub": email, "exp": int(expiry.timestamp())}

    header_segment = _b64url_encode(json.dumps(header, separators=(",", ":")).encode("utf-8"))
    payload_segment = _b64url_encode(json.dumps(payload, separators=(",", ":")).encode("utf-8"))
    signing_input = f"{header_segment}.{payload_segment}".encode("ascii")
    signature = hmac.new(settings["secret"].encode("utf-8"), signing_input, hashlib.sha256).digest()
    token = f"{header_segment}.{payload_segment}.{_b64url_encode(signature)}"
    return token, settings["source"]


def init_state() -> None:
    defaults = {
        "api_base_url": DEFAULT_API_URL,
        "token": "",
        "user_name": "",
        "user_email": "",
        "prediction": None,
        "prediction_input": None,
        "reports_cache": [],
        "chat_messages": [],
        "coach_session_id": "",
        "plan_result": None,
        "diagnosis_result": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def parse_error(response: requests.Response) -> str:
    try:
        payload = response.json()
    except ValueError:
        raw_text = (response.text or "").strip()
        return f"HTTP {response.status_code}: {raw_text or 'Unexpected server error'}"

    detail = payload.get("detail", payload)
    if isinstance(detail, list):
        parts = []
        for item in detail:
            if isinstance(item, dict):
                msg = item.get("msg") or str(item)
                loc = item.get("loc")
                if loc:
                    msg = f"{'.'.join(str(x) for x in loc)}: {msg}"
                parts.append(msg)
            else:
                parts.append(str(item))
        return "; ".join(parts)
    return str(detail)


def call_api(method: str, path: str, token: str = "", payload: dict | None = None) -> tuple[bool, Any]:
    base_url = st.session_state.api_base_url.rstrip("/")
    url = f"{base_url}{path}"
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    try:
        response = requests.request(
            method=method,
            url=url,
            headers=headers,
            json=payload,
            timeout=REQUEST_TIMEOUT,
        )
    except requests.RequestException as exc:
        return False, f"Request failed: {exc}"

    if response.ok:
        if response.content:
            try:
                return True, response.json()
            except ValueError:
                return True, response.text
        return True, {}

    return False, parse_error(response)


def default_student_input() -> dict:
    return {
        "age": 20,
        "gender": "Male",
        "academic_level": "Undergraduate",
        "study_hours": 4.0,
        "self_study_hours": 2.0,
        "online_classes_hours": 1.5,
        "social_media_hours": 2.0,
        "gaming_hours": 1.0,
        "sleep_hours": 7.0,
        "screen_time_hours": 5.0,
        "exercise_minutes": 30,
        "caffeine_intake_mg": 100,
        "part_time_job": "No",
        "upcoming_deadline": "No",
        "internet_quality": "Good",
        "mental_health_score": 7,
        "focus_index": 60.0,
        "burnout_level": 30.0,
        "productivity_score": 60.0,
        "quiz_avg": 65.0,
        "assignment_avg": 65.0,
        "midterm_score": 60.0,
        "topics_completed": 15,
    }


def build_student_profile(prediction: dict) -> dict:
    return {
        "predicted_score": prediction["predicted_score"],
        "classification": prediction["classification"],
        "pass_probability": prediction["pass_probability"],
        "learner_type": prediction["learner_type"],
        "top_weaknesses": prediction.get("top_weaknesses", []),
    }


def clear_coach_state() -> None:
    st.session_state.chat_messages = []
    st.session_state.plan_result = None
    st.session_state.diagnosis_result = None
    st.session_state.coach_session_id = ""


def render_sidebar() -> None:
    st.sidebar.title("AcadIQ Streamlit")
    st.sidebar.caption("Backend-driven UI for prediction + coaching")

    new_api_url = st.sidebar.text_input(
        "Backend URL",
        value=st.session_state.api_base_url,
        help="FastAPI base URL. Example: http://127.0.0.1:8000",
    ).strip()
    if new_api_url:
        st.session_state.api_base_url = new_api_url

    if st.sidebar.button("Check Backend Health", use_container_width=True):
        ok, data = call_api("GET", "/health")
        if ok:
            st.sidebar.success(f"Backend OK | models_loaded={data.get('models_loaded')}")
        else:
            st.sidebar.error(data)

    st.sidebar.divider()
    if st.session_state.token:
        st.sidebar.success(f"Active session: {st.session_state.user_email}")
        if st.sidebar.button("Logout", use_container_width=True):
            st.session_state.token = ""
            st.session_state.user_name = ""
            st.session_state.user_email = ""
            st.session_state.prediction = None
            st.session_state.prediction_input = None
            st.session_state.reports_cache = []
            clear_coach_state()
            st.rerun()
    else:
        st.sidebar.info("Start quick session or login to use prediction history and coaching.")


def render_auth() -> None:
    st.subheader("Start your session")
    st.caption("Login is optional. Use Quick Session to bypass login while keeping all features intact.")

    quick_tab, login_tab, register_tab, token_tab = st.tabs(
        ["Quick Session", "Login", "Register", "Use Existing Token"]
    )

    with quick_tab:
        jwt_settings = load_jwt_settings()
        st.caption(
            f"Quick token uses {jwt_settings['algorithm']} with key source: {jwt_settings['source']}"
        )

        with st.form("quick_session_form", clear_on_submit=False):
            display_name = st.text_input("Name", value="Streamlit User")
            email = st.text_input("Email", value="streamlit.user@example.com")
            submitted = st.form_submit_button("Start Quick Session", use_container_width=True)

        if submitted:
            normalized_email = email.strip().lower()
            if not normalized_email or "@" not in normalized_email:
                st.error("Enter a valid email to create quick session token.")
            else:
                try:
                    token, source = create_dev_token(normalized_email)
                except ValueError as exc:
                    st.error(str(exc))
                else:
                    st.session_state.token = token
                    st.session_state.user_name = display_name.strip() or "Streamlit User"
                    st.session_state.user_email = normalized_email
                    st.success(f"Quick session started using JWT key from {source}")
                    st.rerun()

    with login_tab:
        with st.form("login_form", clear_on_submit=False):
            email = st.text_input("Email", key="login_email")
            password = st.text_input("Password", type="password", key="login_password")
            submitted = st.form_submit_button("Login", use_container_width=True)

        if submitted:
            payload = {"email": email, "password": password}
            ok, data = call_api("POST", "/auth/login", payload=payload)
            if ok:
                st.session_state.token = data["token"]
                st.session_state.user_name = data["name"]
                st.session_state.user_email = data["email"]
                st.success("Login successful")
                st.rerun()
            else:
                st.error(data)

    with token_tab:
        with st.form("manual_token_form", clear_on_submit=False):
            display_name = st.text_input("Name", value="Manual Session User", key="manual_name")
            email = st.text_input("Email", value="manual.user@example.com", key="manual_email")
            token = st.text_area("JWT Token", key="manual_token")
            submitted = st.form_submit_button("Use Token", use_container_width=True)

        if submitted:
            normalized_email = email.strip().lower()
            clean_token = token.strip()
            if not clean_token:
                st.error("Paste a JWT token to continue.")
            elif not normalized_email or "@" not in normalized_email:
                st.error("Enter a valid email for the current session.")
            else:
                st.session_state.token = clean_token
                st.session_state.user_name = display_name.strip() or "Manual Session User"
                st.session_state.user_email = normalized_email
                st.success("Manual token session started")
                st.rerun()

    with register_tab:
        with st.form("register_form", clear_on_submit=False):
            name = st.text_input("Name", key="register_name")
            email = st.text_input("Email", key="register_email")
            password = st.text_input("Password", type="password", key="register_password")
            submitted = st.form_submit_button("Register", use_container_width=True)

        if submitted:
            payload = {"name": name, "email": email, "password": password}
            ok, data = call_api("POST", "/auth/register", payload=payload)
            if ok:
                st.session_state.token = data["token"]
                st.session_state.user_name = data["name"]
                st.session_state.user_email = data["email"]
                st.success("Registration successful")
                st.rerun()
            else:
                st.error(data)


def render_prediction_tab() -> None:
    st.markdown("### Generate Student Profile")
    st.caption("This calls /predict and creates the profile used by the coach endpoints.")

    defaults = default_student_input()
    with st.form("prediction_form"):
        c1, c2, c3 = st.columns(3)

        with c1:
            age = st.number_input("Age", min_value=16, max_value=40, value=defaults["age"])
            gender = st.selectbox("Gender", ["Male", "Female", "Other"], index=0)
            academic_level = st.selectbox(
                "Academic Level",
                ["High School", "Undergraduate", "Postgraduate"],
                index=1,
            )
            part_time_job = st.selectbox("Part-time Job", ["No", "Yes"], index=0)
            upcoming_deadline = st.selectbox("Upcoming Deadline", ["No", "Yes"], index=0)
            internet_quality = st.selectbox(
                "Internet Quality",
                ["Good", "Poor", "Average", "Excellent"],
                index=0,
            )
            sleep_hours = st.slider("Sleep Hours", 4.0, 12.0, defaults["sleep_hours"], 0.5)
            exercise_minutes = st.slider("Exercise Minutes", 0, 180, defaults["exercise_minutes"], 5)

        with c2:
            study_hours = st.slider("Study Hours", 0.0, 16.0, defaults["study_hours"], 0.5)
            self_study_hours = st.slider("Self Study Hours", 0.0, 10.0, defaults["self_study_hours"], 0.5)
            online_classes_hours = st.slider(
                "Online Classes Hours", 0.0, 10.0, defaults["online_classes_hours"], 0.5
            )
            social_media_hours = st.slider(
                "Social Media Hours", 0.0, 12.0, defaults["social_media_hours"], 0.5
            )
            gaming_hours = st.slider("Gaming Hours", 0.0, 10.0, defaults["gaming_hours"], 0.5)
            screen_time_hours = st.slider(
                "Screen Time Hours", 0.0, 16.0, defaults["screen_time_hours"], 0.5
            )
            caffeine_intake_mg = st.slider(
                "Caffeine Intake mg", 0, 600, defaults["caffeine_intake_mg"], 10
            )

        with c3:
            mental_health_score = st.slider("Mental Health Score", 1, 10, defaults["mental_health_score"], 1)
            focus_index = st.slider("Focus Index", 0.0, 100.0, defaults["focus_index"], 1.0)
            burnout_level = st.slider("Burnout Level", 0.0, 100.0, defaults["burnout_level"], 1.0)
            productivity_score = st.slider(
                "Productivity Score", 0.0, 100.0, defaults["productivity_score"], 1.0
            )
            quiz_avg = st.slider("Quiz Average", 0.0, 100.0, defaults["quiz_avg"], 1.0)
            assignment_avg = st.slider("Assignment Average", 0.0, 100.0, defaults["assignment_avg"], 1.0)
            midterm_score = st.slider("Midterm Score", 0.0, 100.0, defaults["midterm_score"], 1.0)
            topics_completed = st.slider("Topics Completed", 0, 50, defaults["topics_completed"], 1)

        submitted = st.form_submit_button("Run Prediction", use_container_width=True)

    if submitted:
        payload = {
            "age": age,
            "gender": gender,
            "academic_level": academic_level,
            "study_hours": study_hours,
            "self_study_hours": self_study_hours,
            "online_classes_hours": online_classes_hours,
            "social_media_hours": social_media_hours,
            "gaming_hours": gaming_hours,
            "sleep_hours": sleep_hours,
            "screen_time_hours": screen_time_hours,
            "exercise_minutes": exercise_minutes,
            "caffeine_intake_mg": caffeine_intake_mg,
            "part_time_job": part_time_job,
            "upcoming_deadline": upcoming_deadline,
            "internet_quality": internet_quality,
            "mental_health_score": mental_health_score,
            "focus_index": focus_index,
            "burnout_level": burnout_level,
            "productivity_score": productivity_score,
            "quiz_avg": quiz_avg,
            "assignment_avg": assignment_avg,
            "midterm_score": midterm_score,
            "topics_completed": topics_completed,
        }
        with st.spinner("Running prediction..."):
            ok, data = call_api("POST", "/predict", token=st.session_state.token, payload=payload)
        if ok:
            st.session_state.prediction = data
            st.session_state.prediction_input = payload
            clear_coach_state()
            st.success("Prediction profile ready for coaching")
        else:
            st.error(data)

    prediction = st.session_state.prediction
    if prediction:
        st.markdown("#### Active Profile")
        mc1, mc2, mc3, mc4 = st.columns(4)
        mc1.metric("Predicted Score", f"{prediction['predicted_score']:.1f}")
        mc2.metric("Classification", prediction["classification"])
        mc3.metric("Pass Probability", f"{prediction['pass_probability']:.1f}%")
        mc4.metric("Learner Type", prediction["learner_type"])


def format_report_label(report: dict) -> str:
    timestamp = report.get("timestamp", "")
    parsed = timestamp
    try:
        parsed_dt = datetime.fromisoformat(timestamp)
        parsed = parsed_dt.strftime("%Y-%m-%d %H:%M")
    except ValueError:
        pass
    prediction = report.get("prediction", {})
    score = prediction.get("predicted_score", "?")
    learner_type = prediction.get("learner_type", "Unknown")
    return f"{parsed} | score={score} | {learner_type}"


def render_history_tab() -> None:
    st.markdown("### Prediction History")
    st.caption("Load an older profile and continue coaching from it.")

    if st.button("Refresh History", use_container_width=False):
        ok, data = call_api("GET", "/predict/history", token=st.session_state.token)
        if ok:
            st.session_state.reports_cache = data.get("reports", [])
        else:
            st.error(data)

    reports = st.session_state.reports_cache
    if not reports:
        st.info("No cached reports. Click Refresh History.")
        return

    selected_index = st.selectbox(
        "Select report",
        options=list(range(len(reports))),
        format_func=lambda idx: format_report_label(reports[idx]),
    )
    selected_report = reports[selected_index]

    st.json(selected_report.get("prediction", {}), expanded=False)

    if st.button("Use Selected Report As Active Profile", use_container_width=True):
        st.session_state.prediction = selected_report.get("prediction")
        st.session_state.prediction_input = selected_report.get("input_data")
        clear_coach_state()
        st.success("Selected report is now active for coaching")


def render_coach_tab() -> None:
    st.markdown("### Study Coach")

    prediction = st.session_state.prediction
    if not prediction:
        st.warning("Create a prediction profile or load one from history before using coaching.")
        return

    profile = build_student_profile(prediction)

    st.caption("Active student profile")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Predicted Score", f"{profile['predicted_score']:.1f}")
    c2.metric("Classification", profile["classification"])
    c3.metric("Pass Probability", f"{profile['pass_probability']:.1f}%")
    c4.metric("Learner Type", profile["learner_type"])

    if st.button("Reset Coach Session Memory", use_container_width=False):
        ok, data = call_api("DELETE", "/coach/reset", token=st.session_state.token)
        if ok:
            clear_coach_state()
            st.success(data.get("message", "Coach memory reset"))
        else:
            st.error(data)

    chat_tab, plan_tab, diagnose_tab = st.tabs(["Chat", "7-Day Plan", "Diagnose Gaps"])

    with chat_tab:
        for message in st.session_state.chat_messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        prompt = st.chat_input("Ask your study coach a question")
        if prompt:
            st.session_state.chat_messages.append({"role": "user", "content": prompt})
            payload = {"message": prompt, "student_profile": profile}
            with st.spinner("Coach is thinking..."):
                ok, data = call_api("POST", "/coach/chat", token=st.session_state.token, payload=payload)

            if ok:
                reply = data.get("reply", "")
                st.session_state.coach_session_id = data.get("session_id", "")
                st.session_state.chat_messages.append({"role": "assistant", "content": reply})
                st.rerun()
            else:
                st.error(data)

    with plan_tab:
        goals = st.text_area(
            "Optional goal guidance",
            placeholder="Example: Improve focus and sleep consistency before finals.",
        )
        if st.button("Generate Personalized 7-Day Plan", use_container_width=True):
            payload = {"student_profile": profile, "goals": goals or None}
            with st.spinner("Generating plan..."):
                ok, data = call_api("POST", "/coach/plan", token=st.session_state.token, payload=payload)
            if ok:
                st.session_state.plan_result = data
            else:
                st.error(data)

        plan_result = st.session_state.plan_result
        if plan_result:
            st.markdown("#### Weekly Goal")
            st.info(plan_result.get("weekly_goal", ""))

            st.markdown("#### Study Plan")
            st.text(plan_result.get("plan", ""))

            resources = plan_result.get("resources", [])
            if resources:
                st.markdown("#### Retrieved Resources (RAG)")
                for idx, resource in enumerate(resources, start=1):
                    st.markdown(
                        f"{idx}. [{resource.get('title', 'Resource')}]({resource.get('url', '')})"
                    )
                    st.caption(resource.get("description", ""))

    with diagnose_tab:
        if st.button("Diagnose Learning Gaps", use_container_width=True):
            payload = {"student_profile": profile}
            with st.spinner("Diagnosing learning gaps..."):
                ok, data = call_api("POST", "/coach/diagnose", token=st.session_state.token, payload=payload)
            if ok:
                st.session_state.diagnosis_result = data
            else:
                st.error(data)

        diagnosis = st.session_state.diagnosis_result
        if diagnosis:
            st.markdown("#### Critical Gaps")
            for gap in diagnosis.get("gaps", []):
                st.write(f"- {gap}")

            st.markdown("#### Reasoning")
            st.write(diagnosis.get("reasoning", ""))


def main() -> None:
    st.set_page_config(
        page_title="AcadIQ Streamlit Coach",
        page_icon="A",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    init_state()
    render_sidebar()

    st.title("AcadIQ Streamlit UI")
    st.caption("React-free UI for prediction and AI coaching (login optional)")

    if not st.session_state.token:
        render_auth()
        return

    st.success(f"Welcome {st.session_state.user_name}")

    prediction_tab, coach_tab, history_tab = st.tabs(["Predict", "Coach", "History"])
    with prediction_tab:
        render_prediction_tab()
    with coach_tab:
        render_coach_tab()
    with history_tab:
        render_history_tab()


if __name__ == "__main__":
    main()