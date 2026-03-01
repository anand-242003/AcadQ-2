"""
pages.py
────────
All Streamlit page-rendering functions (landing, input, results) and the navbar.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from models import run_predictions, generate_recommendations, strip_emoji
from utils import (
    get_score_color,
    get_score_grade,
    get_result_label,
    validate_inputs,
    CHART_BASE,
    C,
)


# ─── Navbar ─────────────────────────────────────────────────────────────────

def render_navbar(active_page: str):
    """Render the top navigation bar with step indicators."""
    pages = [("landing", "Overview"), ("input", "Input Data"), ("results", "Results")]
    steps_html = ""
    done = True

    for pg, label in pages:
        is_active = pg == active_page
        is_done   = done and pg != active_page
        cls = "active" if is_active else ("done" if is_done else "")
        idx = pages.index((pg, label)) + 1
        if is_active:
            done = False
        steps_html += f"""
        <div class="nav-step {cls}">
            <div class="nav-step-num">{'✓' if is_done else idx}</div>
            {label}
        </div>"""
        if pg != "results":
            steps_html += '<span class="nav-step-sep">›</span>'

    badge_map = {"landing": "Home", "input": "Step 1 of 2", "results": "Step 2 of 2"}

    st.markdown(f"""
    <div class="navbar">
        <div class="nav-logo">
            <div class="nav-logo-mark">A</div>
            <div>
                <div class="nav-logo-text">AcadIQ</div>
                <div class="nav-logo-sub">Performance Analytics</div>
            </div>
        </div>
        <div class="nav-steps">{steps_html}</div>
        <div class="nav-badge">{badge_map.get(active_page, '')}</div>
    </div>
    """, unsafe_allow_html=True)


# ─── Landing page ───────────────────────────────────────────────────────────

def show_landing_page():
    render_navbar("landing")

    with st.container():
        st.caption("ML-Powered Academic Analytics")
        st.title("Predict Your Academic Performance")
        st.write(
            "Enter your study habits, lifestyle data, and wellness metrics. "
            "Get an instant predicted exam score, pass/fail classification, "
            "and personalized recommendations to improve."
        )

        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("Get Started →", type="primary", use_container_width=True, key="hero_cta"):
                st.session_state['page'] = 'input'
                st.rerun()

    st.divider()

    with st.container():
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("ML Models", "3")
        m2.metric("Input Features", "20+")
        m3.metric("Output Predictions", "3")
        m4.metric("Recommendations", "10+")

    st.divider()

    # ── Core features ──
    with st.container():
        st.header("Core Features")
        f1, f2, f3 = st.columns(3)
        with f1:
            st.subheader("Score Prediction")
            st.write(
                "A regression model estimates your predicted exam score out of 100, "
                "calibrated on student performance data across 20+ behavioral features."
            )
        with f2:
            st.subheader("Pass / Fail Classification")
            st.write(
                "A binary classifier predicts whether you are on track to pass or at risk "
                "of failing, with a confidence probability breakdown for both outcomes."
            )
        with f3:
            st.subheader("Learner Profiling")
            st.write(
                "A clustering model assigns you to a learner archetype — from Struggling "
                "to High Achiever — and generates targeted improvement recommendations."
            )

    st.divider()

    # ── How it works ──
    with st.container():
        st.caption("How It Works")
        st.header("Three steps to your report")
        st.write(
            "No account needed. Fill in your data, run the models, and get your "
            "full performance analysis in seconds."
        )
        s1, s2, s3 = st.columns(3)
        with s1:
            st.subheader("01. Enter Your Data")
            st.write(
                "Provide details about your study schedule, sleep, screen time, "
                "mental health, and wellbeing across 20 input fields."
            )
        with s2:
            st.subheader("02. Run the Models")
            st.write(
                "Three ML models process your inputs — a regressor, classifier, "
                "and clustering model — to produce a complete performance profile."
            )
        with s3:
            st.subheader("03. Review & Improve")
            st.write(
                "Explore your predicted score, classification, learner type, "
                "interactive charts, and a personalized list of actionable recommendations."
            )


# ─── Input page ─────────────────────────────────────────────────────────────

def show_input_page(models: dict):
    render_navbar("input")

    with st.container():
        st.caption("AcadIQ › Input Data")
        st.header("Enter Your Information")
        st.write("Fill in all fields accurately for the best prediction. The live summary on the right updates as you type.")

    col1, col2, col3 = st.columns(3, gap="large")

    with col1:
        st.subheader("Personal Information")
        age               = st.slider("Age", 16, 25, 20)
        gender            = st.selectbox("Gender", ["Male", "Female", "Other"])
        academic_level    = st.selectbox("Academic Level", ["High School", "Undergraduate"])
        part_time_job     = st.radio("Part-time Job", ["No", "Yes"], horizontal=True)
        upcoming_deadline = st.radio("Upcoming Deadline", ["No", "Yes"], horizontal=True)
        internet_quality  = st.selectbox("Internet Quality", ["Good", "Poor"])

        st.divider()
        st.subheader("Lifestyle")
        sleep_hours        = st.slider("Sleep Hours / Night", 3.0, 12.0, 7.0, 0.5)
        exercise_minutes   = st.slider("Exercise (min / day)", 0, 180, 30, 5)
        caffeine_intake_mg = st.slider("Caffeine Intake (mg / day)", 0, 600, 150, 10)

    with col2:
        st.subheader("Study Habits")
        study_hours          = st.slider("Study Hours / Day", 0.0, 12.0, 4.0, 0.5)
        self_study_hours     = st.slider("Self-Study Hours / Day", 0.0, 8.0, 1.5, 0.5)
        online_classes_hours = st.slider("Online Class Hours / Day", 0.0, 8.0, 1.5, 0.5)

        st.divider()
        st.subheader("Screen & Distractions")
        social_media_hours = st.slider("Social Media Hours / Day", 0.0, 10.0, 2.0, 0.5)
        gaming_hours       = st.slider("Gaming Hours / Day", 0.0, 10.0, 1.0, 0.5)
        screen_time_hours  = st.slider("Total Screen Time / Day", 0.0, 16.0, 6.0, 0.5)

    with col3:
        st.subheader("Wellbeing & Scores")
        mental_health_score = st.slider("Mental Health Score (1–10)", 1, 10, 7, 1)
        focus_index         = st.slider("Focus Index (0–100)", 0.0, 100.0, 50.0, 1.0)
        burnout_level       = st.slider("Burnout Level (0–100)", 0.0, 100.0, 40.0, 1.0)
        productivity_score  = st.slider("Productivity Score (0–100)", 0.0, 100.0, 50.0, 1.0)

        st.divider()
        st.subheader("Live Summary")
        total_study = study_hours + self_study_hours + online_classes_hours
        total_dist  = social_media_hours + gaming_hours
        sleep_ok    = 7 <= sleep_hours <= 9
        mh_label    = "Good" if mental_health_score >= 7 else "Moderate" if mental_health_score >= 4 else "Low"

        sc_col1, sc_col2 = st.columns(2)
        sc_col1.metric("Total Study", f"{total_study:.1f}h")
        sc_col2.metric("Distractions", f"{total_dist:.1f}h")

        sc_col3, sc_col4 = st.columns(2)
        sc_col3.metric("Sleep", "Healthy" if sleep_ok else "Poor")
        sc_col4.metric("Mental Health", mh_label)

    # Build raw input dict
    raw_input = {
        "age": age, "gender": gender, "academic_level": academic_level,
        "study_hours": study_hours, "self_study_hours": self_study_hours,
        "online_classes_hours": online_classes_hours,
        "social_media_hours": social_media_hours, "gaming_hours": gaming_hours,
        "sleep_hours": sleep_hours, "screen_time_hours": screen_time_hours,
        "exercise_minutes": exercise_minutes, "caffeine_intake_mg": caffeine_intake_mg,
        "part_time_job": part_time_job, "upcoming_deadline": upcoming_deadline,
        "internet_quality": internet_quality, "mental_health_score": mental_health_score,
        "focus_index": focus_index, "burnout_level": burnout_level,
        "productivity_score": productivity_score,
    }

    st.markdown('<div class="input-wrap">', unsafe_allow_html=True)

    # Validation warnings
    warnings = validate_inputs(raw_input)
    if warnings:
        with st.expander(f"{len(warnings)} input warning{'s' if len(warnings) > 1 else ''} — click to review"):
            for w in warnings:
                st.warning(w)
            st.caption("You can still proceed. Correcting these will improve prediction accuracy.")

    # Run button
    _, btn_col, _ = st.columns([2, 2, 2])
    with btn_col:
        if st.button("Run Prediction →", type="primary", use_container_width=True):
            with st.spinner("Running models..."):
                try:
                    results = run_predictions(raw_input, models)
                    st.session_state['results']          = results
                    st.session_state['raw_input']        = raw_input
                    st.session_state['validation_warns'] = warnings
                    st.session_state['page']             = 'results'
                    st.rerun()
                except ValueError as ve:
                    st.error(f"Data error: {ve}")
                except Exception as e:
                    st.error(f"Prediction failed: `{e}`")

    st.markdown('</div>', unsafe_allow_html=True)


# ─── Results page ───────────────────────────────────────────────────────────

def show_results_page():
    results   = st.session_state.get('results', {})
    raw       = st.session_state.get('raw_input', {})
    warn_list = st.session_state.get('validation_warns', [])

    if not results:
        st.warning("No results found. Please complete the input step first.")
        if st.button("Go to Input"):
            st.session_state['page'] = 'input'
            st.rerun()
        return

    score    = results['pred_score']
    passed   = results['pred_class'] == 1
    grade    = get_score_grade(score)
    result_l = get_result_label(score)
    s_color  = get_score_color(score)
    ltype    = strip_emoji(results['pred_learner_type'])

    render_navbar("results")

    with st.container():
        st.caption("AcadIQ › Input Data › Results")
        st.header("Your Performance Report")
        st.write("Based on your inputs, here is the full prediction analysis from all three models.")

    if warn_list:
        with st.expander(f"{len(warn_list)} input warning{'s' if len(warn_list) > 1 else ''} — accuracy may be reduced"):
            for w in warn_list:
                st.warning(w)

    # ── Score hero row ──
    hero_l, hero_r = st.columns([1, 1], gap="large")

    with hero_l:
        st.subheader("Predicted Exam Score")
        st.metric("Score", f"{score} / 100", delta=grade)
        st.progress(score / 100)
        if passed:
            st.success(f"Pass — {result_l}")
        else:
            st.error(f"Fail — {result_l}")

    with hero_r:
        m1, m2 = st.columns(2)
        m3, m4 = st.columns(2)
        m1.metric("Pass Probability",  f"{results['pass_probability']}%")
        m2.metric("Fail Probability",  f"{results['fail_probability']}%")
        m3.metric("Learner Type",      ltype)
        m4.metric("Cluster Group",     f"Group {results['pred_cluster']}")

    st.divider()

    # ── Charts + Recommendations ──
    chart_col, rec_col = st.columns([11, 8], gap="large")

    with chart_col:
        st.markdown('<div class="chart-panel">', unsafe_allow_html=True)
        st.markdown('<div class="section-lbl">Performance Breakdown</div>', unsafe_allow_html=True)

        tab1, tab2, tab3 = st.tabs(["Radar Profile", "Habit Comparison", "Time Allocation"])

        with tab1:
            _render_radar_chart(results)

        with tab2:
            _render_bar_chart(results)

        with tab3:
            _render_pie_chart(results, raw)

        st.markdown('</div>', unsafe_allow_html=True)

    with rec_col:
        _render_recommendations(results, ltype)

    # ── Input summary + navigation ──
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    with st.expander("View full input summary"):
        summary = pd.DataFrame([{
            "Age": raw.get('age'),
            "Gender": raw.get('gender'),
            "Academic level": raw.get('academic_level'),
            "Study hours / day": raw.get('study_hours'),
            "Self-study hours / day": raw.get('self_study_hours'),
            "Online class hours / day": raw.get('online_classes_hours'),
            "Sleep hours / night": raw.get('sleep_hours'),
            "Social media hours / day": raw.get('social_media_hours'),
            "Gaming hours / day": raw.get('gaming_hours'),
            "Screen time / day": raw.get('screen_time_hours'),
            "Exercise (minutes / day)": raw.get('exercise_minutes'),
            "Caffeine (mg / day)": raw.get('caffeine_intake_mg'),
            "Mental health score": raw.get('mental_health_score'),
            "Focus index": raw.get('focus_index'),
            "Burnout level": raw.get('burnout_level'),
            "Productivity score": raw.get('productivity_score'),
            "Internet quality": raw.get('internet_quality'),
            "Part-time job": raw.get('part_time_job'),
            "Upcoming deadline": raw.get('upcoming_deadline'),
        }]).T.rename(columns={0: "Value"})
        st.dataframe(summary, use_container_width=True)

    b1, _, b3 = st.columns([2, 4, 2])
    with b1:
        if st.button("← Edit Inputs", use_container_width=True):
            st.session_state['page'] = 'input'
            st.rerun()
    with b3:
        if st.button("New Prediction →", use_container_width=True, type="primary"):
            for k in ['results', 'raw_input', 'validation_warns']:
                st.session_state.pop(k, None)
            st.session_state['page'] = 'input'
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)


# ─── Private chart helpers ──────────────────────────────────────────────────

def _render_radar_chart(results: dict):
    try:
        cats = ["Study hrs", "Sleep hrs", "Mental health",
                "Focus index", "Productivity", "Exercise"]
        vals = [
            min(results['study_hours'] / 12 * 10, 10),
            min(results['sleep_hours'] / 12 * 10, 10),
            float(results['mental_health_score']),
            results['focus_index'] / 10,
            results['productivity_score'] / 10,
            min(results['exercise_minutes'] / 180 * 10, 10),
        ]
        cl = cats + [cats[0]]
        vl = vals + [vals[0]]

        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=vl, theta=cl, fill='toself', name='Your profile',
            line=dict(color=C['c1'], width=2.5),
            fillcolor='rgba(255,255,255,0.08)',
        ))
        fig.add_trace(go.Scatterpolar(
            r=[5] * 7, theta=cl, fill=None, name='Average student',
            line=dict(color='#2A2A2A', dash='dot', width=1.5),
        ))
        fig.update_layout(
            **CHART_BASE,
            polar=dict(
                bgcolor='rgba(0,0,0,0)',
                radialaxis=dict(
                    visible=True, range=[0, 10],
                    tickfont=dict(size=9, color='#2A2A2A'),
                    gridcolor=C['grid'], linecolor=C['grid'],
                ),
                angularaxis=dict(
                    tickfont=dict(size=10, color=C['axis']),
                    gridcolor=C['grid'], linecolor=C['grid'],
                ),
            ),
            legend=dict(orientation='h', y=-0.12, font=dict(size=10, color='#6B6B6B')),
        )
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Chart error: {e}")


def _render_bar_chart(results: dict):
    try:
        labels = [
            "Study hrs", "Sleep hrs", "Social media", "Gaming",
            "Exercise ÷10", "Mental health", "Burnout ÷10", "Productivity ÷10",
        ]
        values = [
            results['study_hours'], results['sleep_hours'],
            results['social_media_hours'], results['gaming_hours'],
            results['exercise_minutes'] / 10, float(results['mental_health_score']),
            results['burnout_level'] / 10, results['productivity_score'] / 10,
        ]
        bar_colors = [
            C['c1'], C['c2'], C['c3'], C['c3'],
            C['c5'], C['c1'], C['c4'], C['c5'],
        ]
        fig = go.Figure(go.Bar(
            x=values, y=labels, orientation='h',
            marker=dict(color=bar_colors, line_width=0),
            text=[f"{v:.1f}" for v in values],
            textposition='outside',
            textfont=dict(size=10, color='#6B6B6B'),
        ))
        fig.update_layout(
            **CHART_BASE,
            xaxis=dict(showgrid=False, showticklabels=False, showline=False, zeroline=False),
            yaxis=dict(showgrid=False, tickfont=dict(size=11, color=C['axis'])),
            bargap=0.38,
        )
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Chart error: {e}")


def _render_pie_chart(results: dict, raw: dict):
    try:
        study_total  = (
            raw.get('study_hours', 0)
            + raw.get('self_study_hours', 0)
            + raw.get('online_classes_hours', 0)
        )
        exercise_hrs = raw.get('exercise_minutes', 0) / 60
        other_hrs    = max(
            0,
            24 - study_total - results['social_media_hours']
            - results['gaming_hours'] - results['sleep_hours'] - exercise_hrs,
        )

        time_labels = ["Study", "Social media", "Gaming", "Sleep", "Exercise", "Other"]
        time_values = [
            study_total, results['social_media_hours'], results['gaming_hours'],
            results['sleep_hours'], exercise_hrs, other_hrs,
        ]
        pie_colors = [C['c1'], C['c4'], C['c3'], C['c2'], C['c5'], '#262626']

        fig = go.Figure(go.Pie(
            labels=time_labels, values=time_values, hole=0.56,
            marker=dict(colors=pie_colors, line=dict(color='#000000', width=2.5)),
            textinfo='label+percent',
            textfont=dict(size=10, color='#E0E0E0'),
            pull=[0.04, 0, 0, 0, 0, 0],
        ))
        fig.add_annotation(
            text="24 hrs", x=0.5, y=0.5,
            font=dict(size=13, color='#6B6B6B', family='-apple-system, system-ui'),
            showarrow=False,
        )
        fig.update_layout(
            **CHART_BASE,
            legend=dict(font=dict(size=10, color='#A0A0A0'), orientation='v'),
        )
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Chart error: {e}")


def _render_recommendations(results: dict, ltype: str):
    st.markdown('<div class="section-lbl">Recommendations</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="learner-card">
        <div class="learner-eyebrow">Learner Classification</div>
        <div class="learner-name">{ltype}</div>
        <div class="learner-meta">
            <div class="learner-meta-item">
                Pass probability: <strong style="color:#E0E0E0">{results['pass_probability']}%</strong>
            </div>
            <div class="learner-meta-dot"></div>
            <div class="learner-meta-item">
                Cluster: <strong style="color:#E0E0E0">Group {results['pred_cluster']}</strong>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    tips = generate_recommendations(results)
    if tips:
        for category, message in tips:
            st.markdown(f"""
            <div class="tip-card">
                <div class="tip-indicator"></div>
                <div>
                    <div class="tip-cat">{category}</div>
                    <div class="tip-txt">{message}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        st.caption(f"{len(tips)} recommendations generated from your profile.")
    else:
        st.success("No major concerns. Keep up the strong work.")
