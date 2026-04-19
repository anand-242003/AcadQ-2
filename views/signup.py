"""Signup page — Form + editorial visual."""
import streamlit as st
import requests

API_BASE = "http://localhost:8000"


def show_signup_page():
    """Render the signup page."""


    st.markdown('<div style="display:flex;justify-content:space-between;align-items:center;padding:8px 0 24px"><a href="/?p=dash" style="text-decoration:none;"><span style="font-family:Manrope,sans-serif;font-size:22px;font-weight:900;color:#6e1a37;letter-spacing:-0.5px">AcadIQ</span></a><span></span></div>', unsafe_allow_html=True)

    form_col, visual_col = st.columns([1, 1], gap="large")

    with form_col:
        st.markdown('<h1 style="font-family:Manrope,sans-serif;font-size:38px;font-weight:900;color:#510122;margin-bottom:10px;letter-spacing:-1px;line-height:1.15">Begin your research journey.</h1>', unsafe_allow_html=True)
        st.markdown('<p style="color:rgba(26,28,27,.6);font-size:16px;font-weight:300;line-height:1.6;margin-bottom:32px">Precision analytics for the next generation of academic excellence.</p>', unsafe_allow_html=True)

        name = st.text_input("Full Name", placeholder="Dr. Julian Thorne", key="signup_name")
        email = st.text_input("Institutional Email", placeholder="j.thorne@oxford.ac.uk", key="signup_email")
        password = st.text_input("Password", type="password", placeholder="••••••••••••", key="signup_password")


        st.markdown('<div style="background:#f4f3f1;padding:20px;border-radius:14px;margin:20px 0"><div style="display:flex;align-items:center;gap:8px;color:#1b6a5b;margin-bottom:8px"><span style="font-size:16px">🛡️</span><span style="font-size:13px;font-weight:700">Responsible Intelligence</span></div><p style="font-size:12px;color:rgba(26,28,27,.6);line-height:1.6;margin:0">At AcadIQ, we utilize your institutional data strictly to tailor analysis engines. Your research remains yours. We never sell student metadata to third parties.</p></div>', unsafe_allow_html=True)

        if st.button("Create Academic Profile", type="primary", use_container_width=True, key="signup_submit"):
            if not name or not email or not password:
                st.error("Please fill in all fields.")
            elif len(password) < 6:
                st.error("Password must be at least 6 characters.")
            else:
                try:
                    resp = requests.post(
                        f"{API_BASE}/auth/register",
                        json={"name": name, "email": email, "password": password},
                        timeout=5,
                    )
                    if resp.status_code == 200:
                        data = resp.json()
                        st.session_state["auth_token"] = data["token"]
                        st.session_state["user_name"] = data["name"]
                        st.session_state["user_email"] = data["email"]
                        st.session_state["page"] = "input_wizard"
                        st.rerun()
                    else:
                        detail = resp.json().get("detail", "Registration failed")
                        st.error(detail)
                except requests.exceptions.ConnectionError:
                    st.warning("Backend not available. Proceeding in demo mode...")
                    st.session_state["user_name"] = name
                    st.session_state["user_email"] = email
                    st.session_state["page"] = "input_wizard"
                    st.rerun()
                except Exception as e:
                    st.error(f"Registration failed: {e}")

        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
        _, mid, _ = st.columns([1, 2, 1])
        with mid:
            if st.button("Already have an account? Log in →", use_container_width=True, key="go_login"):
                st.session_state["page"] = "login"
                st.rerun()

    with visual_col:
        st.markdown('<div style="background:rgba(227,226,224,.6);backdrop-filter:blur(24px);border-radius:24px;padding:44px;border:1px solid rgba(218,192,196,.15);margin-top:20px"><div style="font-size:40px;color:#6e1a37;margin-bottom:20px">📖</div><h2 style="font-family:Manrope,sans-serif;font-size:24px;font-weight:800;color:#6e1a37;margin-bottom:16px;line-height:1.3">"Intelligence is the ability to discover the hidden patterns in chaos."</h2><div style="height:4px;width:60px;background:#1b6a5b;margin-bottom:16px;border-radius:2px"></div><p style="color:rgba(110,26,55,.6);font-style:italic;line-height:1.6;font-size:14px">AcadIQ empowers over 200 institutions worldwide to bridge the gap between raw data and groundbreaking research breakthroughs.</p></div>', unsafe_allow_html=True)


        st.markdown('<div style="margin-top:20px;padding:24px;background:#fff;border-radius:18px;border:1px solid rgba(218,192,196,.12)"><div style="display:flex;align-items:center;gap:12px;margin-bottom:16px"><div style="width:40px;height:40px;border-radius:12px;background:#a7f1de;display:flex;align-items:center;justify-content:center"><span style="font-size:18px">🔒</span></div><div><div style="font-size:14px;font-weight:700;color:#1a1c1b">Data Encrypted & Private</div><div style="font-size:12px;color:#877276">End-to-end encryption for all data</div></div></div><div style="display:flex;align-items:center;gap:12px"><div style="width:40px;height:40px;border-radius:12px;background:#ffd9e0;display:flex;align-items:center;justify-content:center"><span style="font-size:18px">⚡</span></div><div><div style="font-size:14px;font-weight:700;color:#1a1c1b">Instant Results</div><div style="font-size:12px;color:#877276">Get predictions in under 0.4 seconds</div></div></div></div>', unsafe_allow_html=True)
