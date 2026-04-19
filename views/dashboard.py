"""Dashboard — Results page with bento grid, charts, and recommendations."""
import streamlit as st
import plotly.graph_objects as go

from models import generate_recommendations, strip_emoji
from utils import get_score_color, get_score_grade, get_result_label


CHART_BASE = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(family='Inter, sans-serif', color='#544246', size=11),
    margin=dict(t=20, b=16, l=8, r=16),
    height=340,
)


def _render_topbar():
    """Fixed top app bar for dashboard."""
    user = st.session_state.get("user_name", "User")
    initial = user[0].upper() if user else "U"
    st.markdown(f'<div style="position:fixed;top:0;left:0;right:0;z-index:9999;height:64px;display:flex;align-items:center;justify-content:space-between;padding:0 5%;background:rgba(250,249,247,.92);backdrop-filter:blur(20px);border-bottom:1px solid rgba(218,192,196,.15);font-family:Manrope,sans-serif"><div style="display:flex;align-items:center;gap:32px"><a href="/?p=dash" style="text-decoration:none;display:flex;align-items:center;gap:12px;transition:opacity .2s" onmouseover="this.style.opacity=.8" onmouseout="this.style.opacity=1"><span style="font-size:22px;font-weight:900;color:#6e1a37;letter-spacing:-0.5px">AcadIQ</span><span style="width:1px;height:20px;background:rgba(218,192,196,.3);display:inline-block"></span><span style="font-size:14px;font-weight:700;color:#510122">Dashboard</span></a><div style="display:flex;gap:24px;margin-left:16px"><a href="#" style="text-decoration:none;font-size:13px;font-weight:600;color:#544246;font-family:Inter,sans-serif;opacity:.8" onmouseover="this.style.opacity=1" onmouseout="this.style.opacity=.8">Chat History</a><a href="#" style="text-decoration:none;font-size:13px;font-weight:600;color:#544246;font-family:Inter,sans-serif;opacity:.8" onmouseover="this.style.opacity=1" onmouseout="this.style.opacity=.8">Accounting</a><a href="#" style="text-decoration:none;font-size:13px;font-weight:600;color:#544246;font-family:Inter,sans-serif;opacity:.8" onmouseover="this.style.opacity=1" onmouseout="this.style.opacity=.8">Resources</a></div></div><div style="display:flex;align-items:center;gap:16px"><div style="width:36px;height:36px;border-radius:50%;background:#510122;color:#fff;display:flex;align-items:center;justify-content:center;font-size:13px;font-weight:700;box-shadow:0 4px 12px rgba(81,1,34,.2)">{initial}</div></div></div><div style="height:80px"></div>', unsafe_allow_html=True)


def show_dashboard():
    """Render the results dashboard."""
    results = st.session_state.get("results", {})
    raw = st.session_state.get("raw_input", {})

    if not results:
        st.warning("No results found. Please complete the input wizard first.")
        if st.button("Go to Input Wizard →", type="primary"):
            st.session_state["page"] = "input_wizard"
            st.rerun()
        return

    score = results["pred_score"]
    passed = results["pred_class"] == 1
    grade = get_score_grade(score)
    result_l = get_result_label(score)
    ltype = strip_emoji(results["pred_learner_type"])

    _render_topbar()

    # ── Page Header ──────────────────────────────────────────────────────────
    st.markdown(f'<h1 style="font-family:Manrope,sans-serif;font-size:34px;font-weight:900;color:#1a1c1b;letter-spacing:-1px;margin:0 0 4px 0">Your Insights</h1>', unsafe_allow_html=True)
    st.markdown(f'<p style="color:#544246;font-size:14px;font-weight:500;margin-bottom:24px">Academic performance analysis for {st.session_state.get("user_name", "User")}</p>', unsafe_allow_html=True)

    # Action buttons
    btn1, btn2, spacer = st.columns([1.5, 1.8, 6])
    with btn1:
        if st.button("← New Analysis", use_container_width=True, key="dash_new"):
            for k in ["results", "raw_input", "validation_warns", "wizard_data"]:
                st.session_state.pop(k, None)
            st.session_state["page"] = "input_wizard"
            st.rerun()
    with btn2:
        if st.button("Consult AI Coach →", type="primary", use_container_width=True, key="dash_coach"):
            st.session_state["page"] = "coach"
            st.rerun()

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    # ── Row 1: Score card + Learner profile ──────────────────────────────────
    score_col, profile_col = st.columns([7, 5], gap="medium")

    with score_col:
        pass_text = f"Likely Pass ({results['pass_probability']}%)" if passed else f"At Risk ({results['fail_probability']}% Fail)"
        badge_bg = "rgba(167,241,222,.3)" if passed else "rgba(255,218,214,.3)"
        badge_color = "#1b6a5b" if passed else "#ba1a1a"
        badge_icon = "✓" if passed else "⚠"

        st.markdown(f'<div style="background:#fff;border-radius:22px;padding:32px;border:1px solid rgba(218,192,196,.12);position:relative;overflow:hidden"><div style="position:absolute;top:0;left:0;right:0;height:3px;background:linear-gradient(90deg,#510122,#6e1a37,#ae2448)"></div><div style="display:flex;justify-content:space-between;align-items:flex-start"><div><span style="font-size:10px;font-weight:800;text-transform:uppercase;letter-spacing:2px;color:rgba(81,1,34,.6);display:block;margin-bottom:8px">Performance Prediction</span><div style="font-family:Manrope,sans-serif;font-size:52px;font-weight:900;color:#1a1c1b;letter-spacing:-3px;line-height:1">{int(score)}<span style="font-size:18px;color:rgba(26,28,27,.3);vertical-align:super">/100</span></div></div><div style="background:{badge_bg};padding:8px 16px;border-radius:99px"><span style="color:{badge_color};font-weight:700;font-size:13px">{badge_icon} {pass_text}</span></div></div><div style="margin-top:24px"><div style="display:flex;justify-content:space-between;font-size:13px;font-weight:600;margin-bottom:8px"><span style="color:#544246">Confidence</span><span style="color:#510122">{max(0,int(score)-3)} – {min(100,int(score)+3)} range</span></div><div style="height:10px;background:#e9e8e6;border-radius:99px;overflow:hidden"><div style="height:100%;width:{score}%;background:#510122;border-radius:99px;box-shadow:0 0 12px rgba(81,1,34,.3)"></div></div></div></div>', unsafe_allow_html=True)

        # Grade badge
        st.markdown(f'<div style="display:flex;gap:16px;margin-top:12px"><div style="background:#fff;border-radius:16px;padding:18px 24px;border:1px solid rgba(218,192,196,.12);flex:1;text-align:center"><div style="font-family:Manrope;font-size:10px;font-weight:800;text-transform:uppercase;letter-spacing:1.5px;color:#877276;margin-bottom:4px">Grade</div><div style="font-family:Manrope;font-size:32px;font-weight:900;color:#510122">{grade}</div></div><div style="background:#fff;border-radius:16px;padding:18px 24px;border:1px solid rgba(218,192,196,.12);flex:1;text-align:center"><div style="font-family:Manrope;font-size:10px;font-weight:800;text-transform:uppercase;letter-spacing:1.5px;color:#877276;margin-bottom:4px">Status</div><div style="font-family:Manrope;font-size:20px;font-weight:800;color:{badge_color}">{result_l}</div></div><div style="background:#fff;border-radius:16px;padding:18px 24px;border:1px solid rgba(218,192,196,.12);flex:1;text-align:center"><div style="font-family:Manrope;font-size:10px;font-weight:800;text-transform:uppercase;letter-spacing:1.5px;color:#877276;margin-bottom:4px">Pass Prob</div><div style="font-family:Manrope;font-size:32px;font-weight:900;color:#1b6a5b">{results["pass_probability"]}%</div></div></div>', unsafe_allow_html=True)

    with profile_col:
        st.markdown(f'<div style="background:#f4f3f1;border-radius:22px;padding:32px;border:1px solid rgba(218,192,196,.1)"><div style="font-size:10px;font-weight:800;text-transform:uppercase;letter-spacing:2px;color:#877276;margin-bottom:4px">Learner Profile</div><div style="font-family:Manrope,sans-serif;font-size:24px;font-weight:800;color:#1a1c1b;margin-bottom:12px">{ltype}</div><p style="font-size:13px;color:rgba(84,66,70,.7);line-height:1.6;margin-bottom:20px">Your cognitive consistency and study rhythm align with your peer cohort analysis.</p><div style="padding-top:16px;border-top:1px solid rgba(218,192,196,.2);display:flex;gap:8px;flex-wrap:wrap"><span style="padding:4px 12px;background:#fff;border-radius:99px;font-size:10px;font-weight:700;text-transform:uppercase;color:#510122;border:1px solid rgba(81,1,34,.05)">Resilient</span><span style="padding:4px 12px;background:#fff;border-radius:99px;font-size:10px;font-weight:700;text-transform:uppercase;color:#510122;border:1px solid rgba(81,1,34,.05)">Data-Driven</span><span style="padding:4px 12px;background:#fff;border-radius:99px;font-size:10px;font-weight:700;text-transform:uppercase;color:#510122;border:1px solid rgba(81,1,34,.05)">Logical</span></div></div>', unsafe_allow_html=True)

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

    # ── Row 2: Radar chart + Recommendations ─────────────────────────────────
    chart_col, rec_col = st.columns([7, 5], gap="medium")

    with chart_col:
        st.markdown('<div style="background:#fff;border-radius:22px;padding:32px;border:1px solid rgba(218,192,196,.12)"><h4 style="font-family:Manrope,sans-serif;font-size:18px;font-weight:800;color:#1a1c1b;margin-bottom:4px">Behavioral Dimensions</h4><p style="font-size:13px;color:#544246;margin-bottom:0">You vs. Institutional Average</p></div>', unsafe_allow_html=True)
        _render_radar(results)

        st.markdown('<div style="display:flex;gap:24px;padding:0 8px;margin-top:8px"><div style="display:flex;align-items:center;gap:8px"><div style="width:10px;height:10px;border-radius:50%;background:#1b6a5b"></div><span style="font-size:12px;font-weight:600;color:#544246">Your Profile</span></div><div style="display:flex;align-items:center;gap:8px"><div style="width:10px;height:10px;border-radius:50%;background:#6e1a37"></div><span style="font-size:12px;font-weight:600;color:#544246">Average Student</span></div></div>', unsafe_allow_html=True)

    with rec_col:
        _render_recommendations(results, ltype)

    st.markdown('<div style="background:#1a1a24;border-radius:24px;padding:48px 56px;position:relative;overflow:hidden;border:1px solid rgba(255,255,255,.05);box-shadow:0 24px 48px rgba(0,0,0,.15);display:flex;flex-direction:column;gap:16px;margin:20px 0"><div style="position:absolute;top:0;right:0;width:50%;height:100%;background:radial-gradient(ellipse at right,rgba(235,119,150,.1) 0%,transparent 70%)"></div><div style="position:relative;z-index:1;border-left:3px solid #f283a0;padding-left:24px"><div style="font-family:Manrope,sans-serif;font-size:28px;font-weight:800;color:#ffffff;margin:0;letter-spacing:-0.5px;line-height:1.2">Strategic Intervention Required</div><p style="color:rgba(255,255,255,.7);font-size:15px;margin:12px 0 0 0;line-height:1.6;max-width:500px;font-family:Inter,sans-serif">Your predictive models indicate key performance anomalies. Initiate a session with your AI Coach to outline a mitigation strategy.</p></div></div>', unsafe_allow_html=True)

    btn_col, _ = st.columns([3, 7])
    with btn_col:
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        if st.button("Talk to AI Coach", type="primary", use_container_width=True, key="cta_coach"):
            st.session_state["page"] = "coach"
            st.rerun()

    # ── Input Summary ────────────────────────────────────────────────────────
    st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)
    with st.expander("View full input summary"):
        import pandas as pd
        summary = pd.DataFrame([{
            "Age": raw.get("age"),
            "Gender": raw.get("gender"),
            "Academic level": raw.get("academic_level"),
            "Study hours / day": raw.get("study_hours"),
            "Sleep hours / night": raw.get("sleep_hours"),
            "Social media hours": raw.get("social_media_hours"),
            "Mental health score": raw.get("mental_health_score"),
            "Focus index": raw.get("focus_index"),
            "Burnout level": raw.get("burnout_level"),
            "Productivity score": raw.get("productivity_score"),
        }]).T.rename(columns={0: "Value"}).astype(str)
        st.dataframe(summary, use_container_width=True)

    # Footer
    st.markdown('<div style="border-top:1px solid rgba(218,192,196,.15);padding:24px 0;margin-top:40px;display:flex;justify-content:space-between;align-items:center"><span style="font-family:Manrope;font-size:11px;font-weight:600;color:rgba(26,28,27,.32);text-transform:uppercase;letter-spacing:1.5px">© 2024 AcadIQ Analytics</span><div style="display:flex;gap:20px"><span style="font-size:11px;font-weight:700;color:rgba(26,28,27,.32);text-transform:uppercase;letter-spacing:1.5px">Privacy</span><span style="font-size:11px;font-weight:700;color:rgba(26,28,27,.32);text-transform:uppercase;letter-spacing:1.5px">Terms</span></div></div>', unsafe_allow_html=True)


# ─── Chart Helpers ───────────────────────────────────────────────────────────

def _render_radar(results: dict):
    """Radar chart — you vs average."""
    try:
        cats = ["Study hrs", "Sleep hrs", "Mental health", "Focus index", "Productivity", "Exercise"]
        vals = [
            min(results["study_hours"] / 12 * 10, 10),
            min(results["sleep_hours"] / 12 * 10, 10),
            float(results["mental_health_score"]),
            results["focus_index"] / 10,
            results["productivity_score"] / 10,
            min(results["exercise_minutes"] / 180 * 10, 10),
        ]
        cl = cats + [cats[0]]
        vl = vals + [vals[0]]

        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=[5]*7, theta=cl, fill=None, name="Average",
            line=dict(color="#6e1a37", dash="dot", width=1.5),
        ))
        fig.add_trace(go.Scatterpolar(
            r=vl, theta=cl, fill="toself", name="Your Profile",
            line=dict(color="#1b6a5b", width=2.5),
            fillcolor="rgba(27,106,91,0.15)",
        ))
        fig.update_layout(
            **CHART_BASE,
            polar=dict(
                bgcolor="rgba(0,0,0,0)",
                radialaxis=dict(
                    visible=True, range=[0, 10],
                    tickfont=dict(size=9, color="#877276"),
                    gridcolor="rgba(218,192,196,.15)",
                    linecolor="rgba(218,192,196,.15)",
                ),
                angularaxis=dict(
                    tickfont=dict(size=11, color="#544246"),
                    gridcolor="rgba(218,192,196,.15)",
                    linecolor="rgba(218,192,196,.15)",
                ),
            ),
            showlegend=False,
        )
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Chart error: {e}")


def _render_recommendations(results: dict, ltype: str):
    """Recommendations panel."""
    tips = generate_recommendations(results)

    st.markdown('<div style="background:#fff;border-radius:22px;padding:32px;border:1px solid rgba(218,192,196,.12)"><h4 style="font-family:Manrope,sans-serif;font-size:18px;font-weight:800;color:#1a1c1b;margin-bottom:24px">Recommendations</h4>', unsafe_allow_html=True)

    icons = {
        "Sleep": ("🌙", "rgba(255,218,214,.2)"),
        "Study time": ("📚", "rgba(255,217,224,.2)"),
        "Mental health": ("🧘", "rgba(167,241,222,.2)"),
        "Burnout": ("🔥", "rgba(255,218,214,.2)"),
        "Distractions": ("📵", "rgba(255,178,187,.2)"),
        "Exercise": ("💪", "rgba(167,241,222,.2)"),
        "Performing well": ("🏆", "rgba(167,241,222,.2)"),
        "Critical alert": ("🚨", "rgba(255,218,214,.3)"),
        "At risk": ("⚠️", "rgba(255,218,214,.3)"),
        "Room to improve": ("📈", "rgba(255,217,224,.2)"),
        "Study approach": ("📖", "rgba(255,217,224,.2)"),
        "Planning": ("📋", "rgba(167,241,222,.2)"),
        "Study strategy": ("🎯", "rgba(167,241,222,.2)"),
        "Next level": ("🚀", "rgba(167,241,222,.2)"),
        "Connectivity": ("📡", "rgba(218,192,196,.15)"),
        "Learner profile": ("🧠", "rgba(218,192,196,.15)"),
    }

    if tips:
        for cat, msg in tips[:5]:
            icon, bg = icons.get(cat, ("💡", "rgba(218,192,196,.15)"))
            st.markdown(f'<div style="display:flex;gap:14px;margin-bottom:18px"><div style="flex-shrink:0;width:40px;height:40px;border-radius:12px;background:{bg};display:flex;align-items:center;justify-content:center;font-size:18px">{icon}</div><div><p style="font-size:13px;font-weight:700;color:#1a1c1b;margin:0 0 4px">{cat}</p><p style="font-size:12px;color:#544246;margin:0;line-height:1.5">{msg}</p></div></div>', unsafe_allow_html=True)
    else:
        st.success("No major concerns. Keep up the strong work.")

    st.markdown('</div>', unsafe_allow_html=True)
