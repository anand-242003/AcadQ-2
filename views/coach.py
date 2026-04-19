"""AI Study Coach — Chat interface."""
import streamlit as st
import requests
from datetime import datetime

API_BASE = "http://localhost:8000"


def show_coach():
    """Render the AI Study Coach page."""

    # Top bar
    st.markdown('<div style="position:fixed;top:0;left:0;right:0;z-index:9999;height:64px;display:flex;align-items:center;justify-content:space-between;padding:0 5%;background:rgba(250,249,247,.92);backdrop-filter:blur(20px);border-bottom:1px solid rgba(218,192,196,.15);font-family:Manrope,sans-serif"><div style="display:flex;align-items:center;gap:32px"><a href="/?p=dash" style="text-decoration:none;display:flex;align-items:center;gap:12px;transition:opacity .2s" onmouseover="this.style.opacity=.8" onmouseout="this.style.opacity=1"><span style="font-size:22px;font-weight:900;color:#6e1a37;letter-spacing:-0.5px">AcadIQ</span><span style="width:1px;height:20px;background:rgba(218,192,196,.3);display:inline-block"></span><span style="font-size:14px;font-weight:700;color:#510122">AI Coach</span></a><div style="display:flex;gap:24px;margin-left:16px"><a href="/?p=dash" style="text-decoration:none;font-size:13px;font-weight:600;color:#544246;font-family:Inter,sans-serif;opacity:.8" onmouseover="this.style.opacity=1" onmouseout="this.style.opacity=.8">Predictor</a><a href="/?p=plan" style="text-decoration:none;font-size:13px;font-weight:600;color:#544246;font-family:Inter,sans-serif;opacity:.8" onmouseover="this.style.opacity=1" onmouseout="this.style.opacity=.8">Study Plan</a><a href="/?p=resources" style="text-decoration:none;font-size:13px;font-weight:600;color:#544246;font-family:Inter,sans-serif;opacity:.8" onmouseover="this.style.opacity=1" onmouseout="this.style.opacity=.8">Resources</a><a href="/?p=quiz" style="text-decoration:none;font-size:13px;font-weight:600;color:#544246;font-family:Inter,sans-serif;opacity:.8" onmouseover="this.style.opacity=1" onmouseout="this.style.opacity=.8">Quiz Bot</a></div></div><div style="display:flex;align-items:center;gap:12px"><div style="display:flex;align-items:center;gap:6px;background:#f4f3f1;padding:6px 14px;border-radius:99px;border:1px solid rgba(218,192,196,.1)"><div style="width:7px;height:7px;border-radius:50%;background:#1b6a5b"></div><span style="font-size:11px;font-weight:700;color:#1b6a5b">Active</span></div></div></div><div style="height:80px"></div>', unsafe_allow_html=True)

    # Initialize chat history
    if "chat_history" not in st.session_state:
        results = st.session_state.get("results", {})
        score = results.get("pred_score", "N/A")
        ltype = results.get("pred_learner_type", "Student")

        st.session_state["chat_history"] = [
            {
                "role": "assistant",
                "content": f"Hello! I noticed your predicted score is **{score}**. Based on your profile, you are a **{ltype}**. I can help you improve your wellness, study habits, and academic performance. Would you like a personalized 7-day plan?",
                "time": datetime.now().strftime("%I:%M %p"),
            }
        ]

    # Session header
    st.markdown('<div style="text-align:center;margin-bottom:24px"><p style="font-size:10px;text-transform:uppercase;letter-spacing:2px;color:rgba(84,66,70,.5);font-weight:700">Today\'s Focus: Wellness & Cognition</p><div style="height:1px;width:40px;background:rgba(218,192,196,.3);margin:8px auto 0"></div></div>', unsafe_allow_html=True)

    # Render chat messages
    for msg in st.session_state["chat_history"]:
        if msg["role"] == "assistant":
            _render_ai_message(msg["content"], msg.get("time", ""))
        else:
            _render_user_message(msg["content"], msg.get("time", ""))

    # Dashboard nav button
    nav1, spacer, nav2 = st.columns([2, 6, 2])
    with nav1:
        if st.button("← Dashboard", use_container_width=True, key="coach_to_dash"):
            st.session_state["page"] = "dashboard"
            st.rerun()
    with nav2:
        if st.button("Clear Chat", use_container_width=True, key="coach_clear"):
            st.session_state.pop("chat_history", None)
            st.rerun()

    # Chat input
    user_input = st.chat_input("Type your message to AcadIQ Coach...", key="coach_input")

    if user_input:
        st.session_state["chat_history"].append({
            "role": "user",
            "content": user_input,
            "time": datetime.now().strftime("%I:%M %p"),
        })

        reply = _get_coach_reply(user_input)
        st.session_state["chat_history"].append({
            "role": "assistant",
            "content": reply,
            "time": datetime.now().strftime("%I:%M %p"),
        })
        st.rerun()

    # Footer
    st.markdown('<div style="text-align:center;padding:16px 0"><div style="display:flex;justify-content:center;gap:24px"><span style="font-size:10px;color:rgba(84,66,70,.4);font-weight:700;text-transform:uppercase;letter-spacing:1.5px">✓ AI-Generated Insights</span><span style="font-size:10px;color:rgba(84,66,70,.4);font-weight:700;text-transform:uppercase;letter-spacing:1.5px">🔒 Privacy Protected</span></div></div>', unsafe_allow_html=True)


def _render_ai_message(content: str, time: str):
    """Render an AI message bubble."""
    st.markdown(f'<div style="max-width:800px;margin:0 auto;padding:0 20px"><div style="display:flex;gap:14px;margin-bottom:20px;max-width:680px"><div style="flex-shrink:0;width:40px;height:40px;border-radius:50%;background:#6e1a37;color:#ffffff;font-size:14px;font-weight:700;display:flex;align-items:center;justify-content:center;">AI</div><div style="background:#fff;border:1px solid rgba(218,192,196,.15);padding:16px 20px;border-radius:18px 18px 18px 4px;box-shadow:0 2px 8px rgba(0,0,0,.03)"><p style="font-size:14px;line-height:1.65;color:#1a1c1b;font-weight:500;margin:0">{content}</p><span style="font-size:10px;color:rgba(84,66,70,.35);font-weight:700;text-transform:uppercase;margin-top:8px;display:block">AcadIQ Coach • {time}</span></div></div></div>', unsafe_allow_html=True)


def _render_user_message(content: str, time: str):
    """Render a user message bubble."""
    st.markdown(f'<div style="max-width:800px;margin:0 auto;padding:0 20px"><div style="display:flex;gap:14px;margin-bottom:20px;max-width:680px;margin-left:auto;flex-direction:row-reverse"><div style="flex-shrink:0;width:40px;height:40px;border-radius:50%;background:#1b6a5b;display:flex;align-items:center;justify-content:center;color:#fff;font-size:14px;font-weight:700">You</div><div style="background:#a7f1de;padding:16px 20px;border-radius:18px 18px 4px 18px;box-shadow:0 2px 8px rgba(0,0,0,.03)"><p style="font-size:14px;line-height:1.65;color:#00201a;font-weight:500;margin:0">{content}</p><span style="font-size:10px;color:rgba(0,32,26,.35);font-weight:700;text-transform:uppercase;margin-top:8px;display:block;text-align:right">You • {time}</span></div></div></div>', unsafe_allow_html=True)


def _get_coach_reply(message: str) -> str:
    """Get AI coach reply from backend or generate locally."""
    token = st.session_state.get("auth_token")
    results = st.session_state.get("results", {})

    # Try backend
    if token:
        try:
            profile = {
                "predicted_score": results.get("pred_score", 0),
                "pass_probability": results.get("pass_probability", 0),
                "learner_type": results.get("pred_learner_type", "Unknown"),
                "cluster": results.get("pred_cluster", 0),
                "study_hours": results.get("study_hours", 0),
                "sleep_hours": results.get("sleep_hours", 0),
                "mental_health_score": results.get("mental_health_score", 0),
                "burnout_level": results.get("burnout_level", 0),
                "focus_index": results.get("focus_index", 0),
                "exercise_minutes": results.get("exercise_minutes", 0),
                "top_weaknesses": [],
            }
            resp = requests.post(
                f"{API_BASE}/coach/chat",
                json={"message": message, "student_profile": profile},
                headers={"Authorization": f"Bearer {token}"},
                timeout=15,
            )
            if resp.status_code == 200:
                return resp.json().get("reply", "I'm here to help with your studies!")
        except Exception:
            pass

    # Fallback: local response
    msg_lower = message.lower()

    if any(w in msg_lower for w in ["plan", "schedule", "7-day", "week"]):
        return (
            "Here's your personalized plan: "
            "Day 1-2: Focus on sleep hygiene — strict 10 PM bedtime, no screens 30 min before. "
            "Day 3-4: Implement Pomodoro technique — 25 min study, 5 min break. "
            "Day 5-6: Add 30 min daily exercise and reduce social media to under 1 hour. "
            "Day 7: Review progress, celebrate wins, and plan next week."
        )
    elif any(w in msg_lower for w in ["sleep", "tired", "rest"]):
        score = results.get("sleep_hours", 0)
        return f"Your current sleep is at {score} hours. For optimal cognitive performance, aim for 7-8 hours. Try setting a consistent bedtime alarm and avoiding caffeine after noon."
    elif any(w in msg_lower for w in ["stress", "burnout", "overwhelm"]):
        return "I understand. High burnout can significantly impact your performance. Try the 4-7-8 breathing technique: breathe in for 4 seconds, hold for 7, exhale for 8. Also, schedule one full rest day per week."
    elif any(w in msg_lower for w in ["study", "focus", "concentrate"]):
        return "To boost focus, try the Pomodoro Technique: 25 minutes of intense study followed by a 5-minute break. After 4 cycles, take a longer 15-minute break. This prevents cognitive fatigue."
    elif any(w in msg_lower for w in ["score", "grade", "improve", "better"]):
        score = results.get("pred_score", 0)
        return f"Your predicted score is {score}/100. To improve, focus on your weakest areas first. Consistent daily study of 4-5 hours with proper breaks is more effective than cramming."
    else:
        return "That's a great question! As your AI Study Coach, I can help you with study plans, sleep optimization, stress management, and academic strategy. What specific area would you like to focus on?"
