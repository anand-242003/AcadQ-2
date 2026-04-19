"""Study Plan generation page."""
import streamlit as st
import requests
import time

API_BASE = "http://localhost:8000"


def _render_topbar():
    """Fixed top app bar."""
    st.markdown('<div style="position:fixed;top:0;left:0;right:0;z-index:9999;height:64px;display:flex;align-items:center;justify-content:space-between;padding:0 5%;background:rgba(250,249,247,.92);backdrop-filter:blur(20px);border-bottom:1px solid rgba(218,192,196,.15);font-family:Manrope,sans-serif"><div style="display:flex;align-items:center;gap:32px"><a href="/?p=dash" style="text-decoration:none;display:flex;align-items:center;gap:12px;transition:opacity .2s" onmouseover="this.style.opacity=.8" onmouseout="this.style.opacity=1"><span style="font-size:22px;font-weight:900;color:#6e1a37;letter-spacing:-0.5px">AcadIQ</span><span style="width:1px;height:20px;background:rgba(218,192,196,.3);display:inline-block"></span><span style="font-size:14px;font-weight:700;color:#510122">Study Plan</span></a><div style="display:flex;gap:24px;margin-left:16px"><a href="/?p=dash" style="text-decoration:none;font-size:13px;font-weight:600;color:#544246;font-family:Inter,sans-serif;opacity:.8" onmouseover="this.style.opacity=1" onmouseout="this.style.opacity=.8">Results</a><a href="/?p=resources" style="text-decoration:none;font-size:13px;font-weight:600;color:#544246;font-family:Inter,sans-serif;opacity:.8" onmouseover="this.style.opacity=1" onmouseout="this.style.opacity=.8">Resources</a><a href="/?p=quiz" style="text-decoration:none;font-size:13px;font-weight:600;color:#544246;font-family:Inter,sans-serif;opacity:.8" onmouseover="this.style.opacity=1" onmouseout="this.style.opacity=.8">Quiz Bot</a></div></div></div><div style="height:80px"></div>', unsafe_allow_html=True)


def _render_plan(plan_text: str):
    """Render the generated study plan."""
    st.markdown('<div style="background:#fff;border-radius:24px;padding:40px;border:1px solid rgba(218,192,196,.15);box-shadow:0 12px 32px rgba(81,1,34,.03)">', unsafe_allow_html=True)
    
    lines = plan_text.split("\n")
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        if line.startswith("Day "):
            # Split Day X: ...
            if ":" in line:
                day_part, rest = line.split(":", 1)
                st.markdown(f'''
                    <div style="display: flex; align-items: flex-start; gap: 16px; margin-bottom: 24px;">
                        <div style="background: #6e1a37; color: white; padding: 6px 12px; border-radius: 10px; font-weight: 800; font-size: 13px; min-width: 60px; text-align: center; box-shadow: 0 4px 12px rgba(110, 26, 55, 0.15);">
                            {day_part.strip()}
                        </div>
                        <div style="color: #1a1c1b; font-size: 15px; font-weight: 600; line-height: 1.6; padding-top: 2px;">
                            {rest.strip()}
                        </div>
                    </div>
                ''', unsafe_allow_html=True)
            else:
                st.markdown(f'<div style="margin-bottom: 24px; color: #1a1c1b; font-weight: 700;">{line}</div>', unsafe_allow_html=True)
        elif line.startswith("- ") or line.startswith("* "):
            st.markdown(f'<div style="margin-left: 76px; margin-bottom: 12px; color: #544246; font-size: 14px; display: flex; gap: 12px;"><span style="color: #6e1a37; font-weight: 900;">•</span> <span>{line[2:]}</span></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div style="margin-left: 76px; margin-bottom: 16px; color: #544246; font-size: 14px; line-height: 1.6;">{line}</div>', unsafe_allow_html=True)
            
    st.markdown('</div>', unsafe_allow_html=True)


def show_plan():
    """Render the AI generate plan interface."""
    _render_topbar()

    st.markdown('<h1 style="font-family:Manrope,sans-serif;font-size:34px;font-weight:900;color:#1a1c1b;letter-spacing:-1px;margin:0 0 4px 0">Targeted Study Plan</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color:#544246;font-size:14px;font-weight:500;margin-bottom:32px">Generative AI study scheduling based on your predictive profile.</p>', unsafe_allow_html=True)

    results = st.session_state.get("results")
    if not results:
        results = {
            "prediction": 65,
            "grade": "C",
            "status": "Average",
            "learner_type": "Standard Learner",
            "top_weaknesses": [{"feature": "Time Management", "importance": 0.8}, {"feature": "Consistency", "importance": 0.6}],
            "risk_assessment": "Moderate",
        }

    # Check if we already have a generated plan in session
    if "current_plan" not in st.session_state:
        st.markdown('<div style="background:#1a1a24;border-radius:24px;padding:48px;text-align:center;border:1px solid rgba(255,255,255,.05);position:relative;overflow:hidden"><div style="position:absolute;top:-50%;left:-50%;width:200%;height:200%;background:radial-gradient(circle at 50% 50%, rgba(242,131,160,0.08) 0%, transparent 60%);pointer-events:none"></div><div style="font-family:Manrope,sans-serif;font-size:24px;font-weight:800;color:#ffffff;letter-spacing:-0.5px;margin-bottom:12px">Ready to execute?</div><p style="color:rgba(255,255,255,.6);font-size:14px;max-width:400px;margin:0 auto 24px auto;line-height:1.6">We will construct a 7-day optimized schedule specifically targeting your weak points to maximize your academic performance.</p></div>', unsafe_allow_html=True)
        
        _, btn_col, _ = st.columns([1, 1, 1])
        with btn_col:
            st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)
            if st.button("Generate 7-Day Plan", type="primary", use_container_width=True):
                with st.spinner("AI is analyzing your profile and constructing a schedule..."):
                    try:
                        resp = requests.post(f"{API_BASE}/coach/plan", json={"student_profile": results}, timeout=10)
                        if resp.status_code == 200:
                            data = resp.json()
                            st.session_state["current_plan"] = data.get("plan", "No plan returned.")
                            if data.get("resources"):
                                st.session_state["plan_resources"] = data["resources"]
                            st.rerun()
                        else:
                            st.error(f"Failed to generate plan: {resp.json().get('detail')}")
                    except requests.exceptions.ConnectionError:
                        import os, sys
                        backend_path = os.path.abspath("backend")
                        if backend_path not in sys.path:
                            sys.path.append(backend_path)
                        try:
                            from dotenv import load_dotenv
                            load_dotenv(os.path.join(backend_path, ".env"))
                            from services.coach_service import generate_plan
                            from services.rag_service import retrieve_resources
                            weaknesses = results.get("top_weaknesses", [])
                            query = " ".join([w.get("feature", "").replace("_", " ") for w in weaknesses]) if weaknesses else f"{results.get('learner_type', 'student')} study improvement"
                            retrieved = retrieve_resources(query, k=3)
                            
                            # Convert dicts or objects to list of dicts natively expected by the view
                            resc_dicts = []
                            for r in retrieved:
                                resc_dicts.append({
                                    "title": r.get('title', 'Resource'), 
                                    "topic": r.get('topic', 'Paper'), 
                                    "description": r.get('description', ''),
                                    "url": r.get('url', '')
                                })
                            
                            result = generate_plan(results, retrieved)
                            st.session_state["current_plan"] = result.get("plan", "Plan generation completed.")
                            st.session_state["plan_resources"] = resc_dicts
                            st.rerun()
                        except Exception as fallback_e:
                            st.error(f"AI Plan Generation failed internally: {str(fallback_e)}")
    else:
        # Display the existing plan
        _render_plan(st.session_state["current_plan"])
        
        st.markdown("<div style='height:32px'></div>", unsafe_allow_html=True)
        st.markdown('<h3 style="font-family:Manrope,sans-serif;font-size:22px;font-weight:800;color:#1a1c1b;margin-bottom:16px">Recommended Resources</h3>', unsafe_allow_html=True)
        
        resources = st.session_state.get("plan_resources", [])
        if resources:
            for r in resources:
                st.markdown(f'<div style="background:#f4f3f1;border-radius:16px;padding:20px;border:1px solid rgba(218,192,196,.15);margin-bottom:12px;transition:transform 0.2s;cursor:pointer" onmouseover="this.style.transform=\'translateY(-2px)\'" onmouseout="this.style.transform=\'none\'"><div style="display:flex;align-items:center;justify-content:space-between"><div style="font-weight:700;color:#6e1a37;font-size:15px">{r.get("title", "Resource")}</div><div style="font-size:11px;font-weight:700;color:#1b6a5b;background:rgba(167,241,222,.3);padding:4px 10px;border-radius:99px;text-transform:uppercase;letter-spacing:1px">{r.get("topic", "Material")}</div></div><p style="font-size:13px;color:#544246;margin:8px 0 0 0;line-height:1.6">{r.get("description", "")}</p></div>', unsafe_allow_html=True)
        else:
            st.info("No specific resources recommended for this plan phase.")
            
        st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)
        if st.button("Regenerate Plan", use_container_width=False):
            del st.session_state["current_plan"]
            if "plan_resources" in st.session_state:
                del st.session_state["plan_resources"]
            st.rerun()
