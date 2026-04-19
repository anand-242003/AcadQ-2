"""Input Wizard — 5-step data entry matching the AcadIQ design."""
import streamlit as st

from models import run_predictions, load_all_models
from utils import validate_inputs


STEP_TITLES = [
    "Academic Performance",
    "Study Habits",
    "Lifestyle & Health",
    "Wellbeing & Focus",
    "Personal Information",
]

STEP_DESCRIPTIONS = [
    "Your academic scores are the foundation of the AcadIQ Intelligence Engine.",
    "We correlate study patterns to predict potential final outcomes.",
    "Lifestyle factors like sleep and exercise heavily influence cognition.",
    "Mental health and focus metrics improve prediction accuracy significantly.",
    "Demographic context helps calibrate predictions to your peer group.",
]


def _render_header():
    """Top nav bar for wizard pages."""
    st.markdown('<div style="position:fixed;top:0;left:0;right:0;z-index:9999;height:64px;display:flex;align-items:center;justify-content:space-between;padding:0 5%;background:rgba(250,249,247,.92);backdrop-filter:blur(20px);border-bottom:1px solid rgba(218,192,196,.15);font-family:Manrope,sans-serif"><a href="/?p=dash" style="text-decoration:none;"><span style="font-size:22px;font-weight:900;color:#6e1a37;letter-spacing:-0.5px">AcadIQ</span></a><div style="display:flex;align-items:center;gap:8px"><span style="color:rgba(26,28,27,.5);font-size:14px;font-weight:600">Input Wizard</span></div></div><div style="height:64px"></div>', unsafe_allow_html=True)


def _render_progress(step: int):
    """Step indicator and progress bar."""
    pct = ((step + 1) / 5) * 100
    dots_html = ""
    for i in range(5):
        color = "#1b6a5b" if i <= step else "#e3e2e0"
        dots_html += f'<div style="height:6px;width:32px;border-radius:99px;background:{color}"></div>'

    st.markdown(f'<div style="max-width:900px;margin:0 auto;padding:32px 40px 0"><div style="display:flex;justify-content:space-between;align-items:flex-end;margin-bottom:20px"><div><span style="font-family:Manrope,sans-serif;font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:2.5px;color:#1b6a5b">Step {step + 1} of 5</span><h1 style="font-family:Manrope,sans-serif;font-size:36px;font-weight:900;color:#510122;letter-spacing:-1px;margin-top:4px">{STEP_TITLES[step]}</h1></div><div style="display:flex;gap:4px">{dots_html}</div></div><div style="height:2px;background:rgba(218,192,196,.15);overflow:hidden;border-radius:99px"><div style="height:100%;width:{pct}%;background:#1b6a5b;transition:width .4s ease"></div></div></div>', unsafe_allow_html=True)


def _render_sidebar_info(step: int):
    """Contextual info sidebar."""
    st.markdown(f'<div style="position:sticky;top:120px;padding:32px;border-radius:22px;background:#f4f3f1;border:1px solid rgba(218,192,196,.1)"><div style="font-size:32px;color:#1b6a5b;margin-bottom:16px">🧠</div><h3 style="font-family:Manrope,sans-serif;font-size:18px;font-weight:800;color:#510122;margin-bottom:12px">Why this data?</h3><p style="color:rgba(84,66,70,.7);line-height:1.65;font-size:14px;margin-bottom:20px">{STEP_DESCRIPTIONS[step]} We correlate these scores with your study habits via the <span style="color:#1b6a5b;font-weight:600">AcadIQ Intelligence Engine</span>.</p><div style="background:rgba(255,255,255,.5);border:1px solid rgba(255,255,255,.4);border-radius:14px;padding:14px"><div style="display:flex;align-items:center;gap:10px;margin-bottom:8px"><div style="width:7px;height:7px;border-radius:50%;background:#1b6a5b"></div><span style="font-size:12px;font-weight:500;color:#1a1c1b">Data is encrypted & private</span></div><div style="display:flex;align-items:center;gap:10px"><div style="width:7px;height:7px;border-radius:50%;background:#1b6a5b"></div><span style="font-size:12px;font-weight:500;color:#1a1c1b">Immediate feedback generation</span></div></div></div>', unsafe_allow_html=True)


def show_input_wizard(models: dict):
    """Render the 5-step input wizard."""

    _render_header()


    if "wizard_step" not in st.session_state:
        st.session_state["wizard_step"] = 0
    if "wizard_data" not in st.session_state:
        st.session_state["wizard_data"] = {}

    step = st.session_state["wizard_step"]
    data = st.session_state["wizard_data"]

    _render_progress(step)


    form_col, info_col = st.columns([7, 5], gap="large")

    with form_col:
        if step == 0:
            _step_academic(data)
        elif step == 1:
            _step_study(data)
        elif step == 2:
            _step_lifestyle(data)
        elif step == 3:
            _step_wellbeing(data)
        elif step == 4:
            _step_personal(data)

    with info_col:
        _render_sidebar_info(step)


    st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)
    nav_left, nav_spacer, nav_right = st.columns([2, 5, 2])

    with nav_left:
        if step > 0:
            if st.button("← Back", use_container_width=True, key="wizard_back"):
                st.session_state["wizard_step"] = step - 1
                st.rerun()
        else:
            if st.button("← Home", use_container_width=True, key="wizard_home"):
                st.session_state["page"] = "landing"
                st.rerun()

    with nav_right:
        if step < 4:
            if st.button("Continue →", type="primary", use_container_width=True, key="wizard_next"):
                st.session_state["wizard_step"] = step + 1
                st.rerun()
        else:
            if st.button("Run Prediction →", type="primary", use_container_width=True, key="wizard_run"):
                _run_prediction(data, models)


    st.markdown('<div style="border-top:1px solid rgba(218,192,196,.15);padding:24px 40px;margin-top:40px;display:flex;justify-content:space-between;align-items:center;font-family:Manrope,sans-serif"><span style="font-size:11px;font-weight:600;color:rgba(26,28,27,.32);text-transform:uppercase;letter-spacing:1.5px">© 2024 AcadIQ Analytics</span><div style="display:flex;gap:20px"><span style="font-size:11px;font-weight:700;color:rgba(26,28,27,.32);text-transform:uppercase;letter-spacing:1.5px">Privacy Policy</span><span style="font-size:11px;font-weight:700;color:rgba(26,28,27,.32);text-transform:uppercase;letter-spacing:1.5px">Research Docs</span></div></div>', unsafe_allow_html=True)




def _step_academic(data: dict):
    st.markdown('<p style="font-size:13px;color:#544246;margin-bottom:20px;font-style:italic">Used to track short-term knowledge retention and consistency.</p>', unsafe_allow_html=True)

    data["study_hours"] = st.slider(
        "Quiz Average (Study Hours / Day)", 0.0, 12.0,
        data.get("study_hours", 4.0), 0.5, key="wiz_study_hours",
        help="Average daily study hours"
    )
    data["self_study_hours"] = st.slider(
        "Assignment Average (Self-Study Hours / Day)", 0.0, 8.0,
        data.get("self_study_hours", 1.5), 0.5, key="wiz_self_study",
        help="Self-directed study time"
    )
    data["online_classes_hours"] = st.slider(
        "Online Class Hours / Day", 0.0, 8.0,
        data.get("online_classes_hours", 1.5), 0.5, key="wiz_online",
        help="Time spent in online sessions"
    )


def _step_study(data: dict):
    st.markdown('<p style="font-size:13px;color:#544246;margin-bottom:20px;font-style:italic">Your study patterns reveal how effectively you absorb and retain information.</p>', unsafe_allow_html=True)

    data["social_media_hours"] = st.slider(
        "Social Media Hours / Day", 0.0, 10.0,
        data.get("social_media_hours", 2.0), 0.5, key="wiz_social"
    )
    data["gaming_hours"] = st.slider(
        "Gaming Hours / Day", 0.0, 10.0,
        data.get("gaming_hours", 1.0), 0.5, key="wiz_gaming"
    )
    data["screen_time_hours"] = st.slider(
        "Total Screen Time / Day", 0.0, 16.0,
        data.get("screen_time_hours", 6.0), 0.5, key="wiz_screen"
    )


def _step_lifestyle(data: dict):
    st.markdown('<p style="font-size:13px;color:#544246;margin-bottom:20px;font-style:italic">Sleep, exercise, and caffeine directly impact cognitive performance.</p>', unsafe_allow_html=True)

    data["sleep_hours"] = st.slider(
        "Sleep Hours / Night", 3.0, 12.0,
        data.get("sleep_hours", 7.0), 0.5, key="wiz_sleep"
    )
    data["exercise_minutes"] = st.slider(
        "Exercise (min / day)", 0, 180,
        data.get("exercise_minutes", 30), 5, key="wiz_exercise"
    )
    data["caffeine_intake_mg"] = st.slider(
        "Caffeine Intake (mg / day)", 0, 600,
        data.get("caffeine_intake_mg", 150), 10, key="wiz_caffeine"
    )


def _step_wellbeing(data: dict):
    st.markdown('<p style="font-size:13px;color:#544246;margin-bottom:20px;font-style:italic">Mental health and focus are the strongest non-academic predictors of success.</p>', unsafe_allow_html=True)

    data["mental_health_score"] = st.slider(
        "Mental Health Score (1-10)", 1, 10,
        data.get("mental_health_score", 7), 1, key="wiz_mh"
    )
    data["focus_index"] = st.slider(
        "Focus Index (0-100)", 0.0, 100.0,
        data.get("focus_index", 50.0), 1.0, key="wiz_focus"
    )
    data["burnout_level"] = st.slider(
        "Burnout Level (0-100)", 0.0, 100.0,
        data.get("burnout_level", 40.0), 1.0, key="wiz_burnout"
    )
    data["productivity_score"] = st.slider(
        "Productivity Score (0-100)", 0.0, 100.0,
        data.get("productivity_score", 50.0), 1.0, key="wiz_productivity"
    )


def _step_personal(data: dict):
    st.markdown('<p style="font-size:13px;color:#544246;margin-bottom:20px;font-style:italic">Demographics help us calibrate your prediction against relevant peer cohorts.</p>', unsafe_allow_html=True)

    data["age"] = st.slider("Age", 16, 25, data.get("age", 20), key="wiz_age")
    data["gender"] = st.selectbox(
        "Gender", ["Male", "Female", "Other"],
        index=["Male", "Female", "Other"].index(data.get("gender", "Male")),
        key="wiz_gender"
    )
    data["academic_level"] = st.selectbox(
        "Academic Level", ["High School", "Undergraduate"],
        index=["High School", "Undergraduate"].index(data.get("academic_level", "Undergraduate")),
        key="wiz_level"
    )
    data["part_time_job"] = st.radio(
        "Part-time Job", ["No", "Yes"], horizontal=True,
        index=["No", "Yes"].index(data.get("part_time_job", "No")),
        key="wiz_job"
    )
    data["upcoming_deadline"] = st.radio(
        "Upcoming Deadline", ["No", "Yes"], horizontal=True,
        index=["No", "Yes"].index(data.get("upcoming_deadline", "No")),
        key="wiz_deadline"
    )
    data["internet_quality"] = st.selectbox(
        "Internet Quality", ["Good", "Poor"],
        index=["Good", "Poor"].index(data.get("internet_quality", "Good")),
        key="wiz_internet"
    )


    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
    st.markdown('<div style="font-family:Manrope,sans-serif;font-size:11px;font-weight:800;text-transform:uppercase;letter-spacing:2px;color:#877276;margin-bottom:12px">Live Summary</div>', unsafe_allow_html=True)

    total_study = data.get("study_hours", 4) + data.get("self_study_hours", 1.5) + data.get("online_classes_hours", 1.5)
    total_dist = data.get("social_media_hours", 2) + data.get("gaming_hours", 1)
    m1, m2 = st.columns(2)
    m1.metric("Total Study", f"{total_study:.1f}h")
    m2.metric("Distractions", f"{total_dist:.1f}h")




def _run_prediction(data: dict, models: dict):
    """Process wizard data through ML models."""
    raw_input = {
        "age": data.get("age", 20),
        "gender": data.get("gender", "Male"),
        "academic_level": data.get("academic_level", "Undergraduate"),
        "study_hours": data.get("study_hours", 4.0),
        "self_study_hours": data.get("self_study_hours", 1.5),
        "online_classes_hours": data.get("online_classes_hours", 1.5),
        "social_media_hours": data.get("social_media_hours", 2.0),
        "gaming_hours": data.get("gaming_hours", 1.0),
        "sleep_hours": data.get("sleep_hours", 7.0),
        "screen_time_hours": data.get("screen_time_hours", 6.0),
        "exercise_minutes": data.get("exercise_minutes", 30),
        "caffeine_intake_mg": data.get("caffeine_intake_mg", 150),
        "part_time_job": data.get("part_time_job", "No"),
        "upcoming_deadline": data.get("upcoming_deadline", "No"),
        "internet_quality": data.get("internet_quality", "Good"),
        "mental_health_score": data.get("mental_health_score", 7),
        "focus_index": data.get("focus_index", 50.0),
        "burnout_level": data.get("burnout_level", 40.0),
        "productivity_score": data.get("productivity_score", 50.0),
    }

    warnings = validate_inputs(raw_input)
    if warnings:
        for w in warnings:
            st.warning(w)

    with st.spinner("Running ML models..."):
        try:
            results = run_predictions(raw_input, models)
            st.session_state["results"] = results
            st.session_state["raw_input"] = raw_input
            st.session_state["validation_warns"] = warnings
            st.session_state["page"] = "dashboard"
            st.session_state["wizard_step"] = 0
            st.rerun()
        except Exception as e:
            st.error(f"Prediction failed: {e}")
