"""Quiz Bot generation page."""
import streamlit as st
import requests
import time

API_BASE = "http://localhost:8000"


def _render_topbar():
    """Fixed top app bar."""
    st.markdown('<div style="position:fixed;top:0;left:0;right:0;z-index:9999;height:64px;display:flex;align-items:center;justify-content:space-between;padding:0 5%;background:rgba(250,249,247,.92);backdrop-filter:blur(20px);border-bottom:1px solid rgba(218,192,196,.15);font-family:Manrope,sans-serif"><div style="display:flex;align-items:center;gap:32px"><a href="/?p=dash" style="text-decoration:none;display:flex;align-items:center;gap:12px;transition:opacity .2s" onmouseover="this.style.opacity=.8" onmouseout="this.style.opacity=1"><span style="font-size:22px;font-weight:900;color:#6e1a37;letter-spacing:-0.5px">AcadIQ</span><span style="width:1px;height:20px;background:rgba(218,192,196,.3);display:inline-block"></span><span style="font-size:14px;font-weight:700;color:#510122">Quiz Bot</span></a><div style="display:flex;gap:24px;margin-left:16px"><a href="/?p=dash" style="text-decoration:none;font-size:13px;font-weight:600;color:#544246;font-family:Inter,sans-serif;opacity:.8" onmouseover="this.style.opacity=1" onmouseout="this.style.opacity=.8">Results</a><a href="/?p=resources" style="text-decoration:none;font-size:13px;font-weight:600;color:#544246;font-family:Inter,sans-serif;opacity:.8" onmouseover="this.style.opacity=1" onmouseout="this.style.opacity=.8">Resources</a><a href="/?p=plan" style="text-decoration:none;font-size:13px;font-weight:600;color:#544246;font-family:Inter,sans-serif;opacity:.8" onmouseover="this.style.opacity=1" onmouseout="this.style.opacity=.8">Study Plan</a></div></div></div><div style="height:80px"></div>', unsafe_allow_html=True)


def show_quiz_bot():
    """Render the interactive Quiz Bot page."""
    _render_topbar()

    st.markdown('<h1 style="font-family:Manrope,sans-serif;font-size:34px;font-weight:900;color:#1a1c1b;letter-spacing:-1px;margin:0 0 4px 0">Interactive Quiz Bot</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color:#544246;font-size:14px;font-weight:500;margin-bottom:32px">Test your knowledge dynamically with generative AI quizzes.</p>', unsafe_allow_html=True)

    if "quiz_data" not in st.session_state:
        st.markdown('<div style="background:#fff;border-radius:24px;padding:48px;border:1px solid rgba(218,192,196,.15);box-shadow:0 12px 32px rgba(81,1,34,.03)"><h3 style="font-family:Manrope,sans-serif;font-size:22px;font-weight:800;color:#510122;margin-bottom:24px">Configure Your Session</h3>', unsafe_allow_html=True)
        
        tc, dc = st.columns([2, 1])
        with tc:
            topic = st.text_input("Study Topic", placeholder="e.g. Cellular Biology, Machine Learning, Roman History")
        with dc:
            diff = st.selectbox("Difficulty", ["easy", "medium", "hard"], index=1)
            
        c1, c2 = st.columns(2)
        with c1:
            lvl = st.selectbox("Academic Level", ["high school", "undergraduate", "graduate"], index=1)
        with c2:
            num = st.slider("Number of Questions", 1, 10, 5)
            
        st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)
        
        if st.button("Generate Quiz", type="primary", use_container_width=True):
            if not topic:
                st.error("Please enter a topic.")
            else:
                with st.spinner("AI is crafting your questions..."):
                    try:
                        req_data = {
                            "topic": topic, "count": num, "level": lvl,
                            "difficulty": diff, "distractor_count": 3, "language": "english"
                        }
                        resp = requests.post(f"{API_BASE}/quiz/generate", json=req_data, timeout=15)
                        if resp.status_code == 200:
                            st.session_state["quiz_data"] = resp.json()
                            st.session_state["quiz_answers"] = {}
                            st.session_state["quiz_submitted"] = False
                            st.rerun()
                        else:
                            st.error(f"Failed to generate quiz: {resp.json().get('detail')}")
                    except requests.exceptions.ConnectionError:
                        import os, sys
                        backend_path = os.path.abspath("backend")
                        if backend_path not in sys.path:
                            sys.path.append(backend_path)
                        try:
                            from dotenv import load_dotenv
                            load_dotenv(os.path.join(backend_path, ".env"))
                            from services.quiz_service import generate_quiz
                            quiz_result = generate_quiz(topic, num, lvl, diff, 3, "english")
                            st.session_state["quiz_data"] = quiz_result
                            st.session_state["quiz_answers"] = {}
                            st.session_state["quiz_submitted"] = False
                            st.rerun()
                        except Exception as fallback_e:
                            st.error(f"AI Quiz Generation failed internally: {str(fallback_e)}")
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        # Display the Quiz UI
        quiz = st.session_state["quiz_data"]
        submitted = st.session_state.get("quiz_submitted", False)
        
        st.markdown(f'<div style="background:#f4f3f1;padding:16px 24px;border-radius:16px;margin-bottom:24px;border:1px solid rgba(218,192,196,.15);display:flex;justify-content:space-between;align-items:center"><span style="font-family:Manrope;font-weight:800;color:#510122;font-size:18px">{quiz.get("topic", quiz.get("title", "Quiz Bot"))}</span><span style="font-size:12px;font-weight:800;color:#877276;text-transform:uppercase;letter-spacing:1px">{len(quiz["questions"])} Questions</span></div>', unsafe_allow_html=True)
        
        for idx, q_data in enumerate(quiz["questions"]):
            st.markdown(f'<h4 style="font-family:Manrope,sans-serif;font-size:16px;font-weight:700;color:#1a1c1b;margin-bottom:12px">{idx+1}. {q_data["question"]}</h4>', unsafe_allow_html=True)
            
            # Use columns to create a neat UI for radio buttons without the markdown clashing
            ans_key = f"q_{idx}"
            options = q_data.get("options", [])
            
            if not submitted:
                st.session_state["quiz_answers"][ans_key] = st.radio(
                    "Options", 
                    options=options, 
                    key=f"radio_{idx}",
                    format_func=lambda x: f"{x['label']}. {x['text']}",
                    label_visibility="collapsed"
                )
            else:
                user_ans_dict = st.session_state["quiz_answers"].get(ans_key)
                user_label = user_ans_dict.get("label") if user_ans_dict else ""
                correct_label = q_data.get("correct_option_label", "")
                
                # Find the text of the correct answer for display
                correct_ans_text = next((opt["text"] for opt in options if opt["label"] == correct_label), "Unknown")
                user_ans_text = user_ans_dict.get("text", "") if user_ans_dict else ""

                if user_label == correct_label:
                    st.success(f"**Correct!** {user_label}. {user_ans_text}")
                else:
                    st.error(f"**Incorrect.** You selected: {user_label}. {user_ans_text}")
                    st.success(f"**Correct Answer:** {correct_label}. {correct_ans_text}")
                
                with st.expander("Explanation", expanded=(user_label != correct_label)):
                    st.markdown(f'<p style="font-size:14px;color:#544246;margin:0">{q_data["explanation"]}</p>', unsafe_allow_html=True)
            st.markdown("<hr style='border:none;border-top:1px solid rgba(218,192,196,.15);margin:24px 0'>", unsafe_allow_html=True)
            
        if not submitted:
            if st.button("Submit Answers", type="primary", use_container_width=True):
                st.session_state["quiz_submitted"] = True
                st.rerun()
        else:
            if st.button("Generate New Quiz", use_container_width=False):
                del st.session_state["quiz_data"]
                st.rerun()
