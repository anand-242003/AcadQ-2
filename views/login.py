"""Login page — Split layout with branding + form."""
import streamlit as st
import requests

API_BASE = "http://localhost:8000"


def show_login_page():
    """Render the login page."""

    # CSS for the page
    st.markdown("""<style>
.login-brand-panel{background:linear-gradient(135deg,#510122 0%,#6e1a37 50%,#7a002a 100%);border-radius:22px;padding:48px;color:#fff;position:relative;overflow:hidden;min-height:500px;display:flex;flex-direction:column;justify-content:space-between}
.login-brand-panel::before{content:'';position:absolute;inset:0;background:url('https://lh3.googleusercontent.com/aida-public/AB6AXuDw1Q0yuBGiuEqXgihVSyGur9EUaFQKWsUJyvkwG1FbNEQsvMf7psobWQPlJgk2RjAXNVPX49wMJ1t11wl7ZcOYKUDmnEtglh0qTjsaG1tQAC2LxTw0yzU3pn0O7OIzDDeFGHqqPNuReN11hb4Fs5pBkiQgvJAsRzsQTUBgU9A2boP1XqZqR3fWVoU3tZE4Rdwo5VmmHFrg75qxxxzFjQtotTYydoaEjVtyMTnB3eSZ7qoLvE2Sps7bE3qNHVBJgbYnl9b7_tikrliw') center/cover;opacity:.15;mix-blend-mode:overlay}
</style>""", unsafe_allow_html=True)

    # Top bar
    st.markdown('<div style="display:flex;justify-content:space-between;align-items:center;padding:8px 0 24px"><a href="/?p=dash" style="text-decoration:none;"><span style="font-family:Manrope,sans-serif;font-size:22px;font-weight:900;color:#6e1a37;letter-spacing:-0.5px">AcadIQ</span></a><span></span></div>', unsafe_allow_html=True)

    # Two-column layout
    brand_col, form_col = st.columns([1, 1], gap="large")

    with brand_col:
        st.markdown('<div class="login-brand-panel"><div style="position:relative;z-index:1"><div style="font-family:Manrope,sans-serif;font-size:26px;font-weight:900;color:#fff">AcadIQ</div><div style="font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:3px;color:rgba(242,131,160,.7);margin-top:6px">Academic Intelligence</div></div><div style="position:relative;z-index:1;max-width:400px"><div style="font-size:32px;margin-bottom:16px;color:rgba(242,131,160,.7)">❝</div><h2 style="font-family:Manrope,sans-serif;font-size:28px;font-weight:700;line-height:1.25;color:#fff !important;margin-bottom:16px">The capacity to learn is a gift; the ability to learn is a skill; the willingness to learn is a choice.</h2><div style="display:flex;align-items:center;gap:12px;font-size:14px;color:rgba(242,131,160,.8);font-weight:500"><div style="width:28px;height:1px;background:rgba(242,131,160,.4)"></div>Brian Herbert</div></div><div style="position:relative;z-index:1;font-size:10px;font-weight:600;text-transform:uppercase;letter-spacing:2px;color:rgba(242,131,160,.35)">© 2024 AcadIQ Analytics</div></div>', unsafe_allow_html=True)

    with form_col:
        st.markdown('<h3 style="font-family:Manrope,sans-serif;font-size:34px;font-weight:800;color:#510122;margin-bottom:6px">Welcome back</h3>', unsafe_allow_html=True)
        st.markdown('<p style="color:#544246;font-size:16px;margin-bottom:32px">Continue your intellectual journey.</p>', unsafe_allow_html=True)

        email = st.text_input("Email Address", placeholder="curator@acadiq.edu", key="login_email")
        password = st.text_input("Password", type="password", placeholder="••••••••", key="login_password")

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

        if st.button("Sign In →", type="primary", use_container_width=True, key="login_submit"):
            if not email or not password:
                st.error("Please enter both email and password.")
            else:
                try:
                    resp = requests.post(
                        f"{API_BASE}/auth/login",
                        json={"email": email, "password": password},
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
                        detail = resp.json().get("detail", "Invalid credentials")
                        st.error(detail)
                except requests.exceptions.ConnectionError:
                    st.warning("Backend not available. Proceeding in demo mode...")
                    st.session_state["user_name"] = email.split("@")[0].title()
                    st.session_state["user_email"] = email
                    st.session_state["page"] = "input_wizard"
                    st.rerun()
                except Exception as e:
                    st.error(f"Login failed: {e}")

        # Divider
        st.markdown('<div style="display:flex;align-items:center;gap:16px;margin:24px 0"><div style="flex:1;height:1px;background:rgba(218,192,196,.15)"></div><span style="font-size:11px;text-transform:uppercase;letter-spacing:2px;color:rgba(84,66,70,.4)">or</span><div style="flex:1;height:1px;background:rgba(218,192,196,.15)"></div></div>', unsafe_allow_html=True)

        if st.button("Continue in Demo Mode", use_container_width=True, key="login_demo"):
            st.session_state["user_name"] = "Demo User"
            st.session_state["user_email"] = "demo@acadiq.edu"
            st.session_state["page"] = "input_wizard"
            st.rerun()

        st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

        _, mid, _ = st.columns([1, 2, 1])
        with mid:
            if st.button("New to AcadIQ? Create account →", use_container_width=True, key="go_signup"):
                st.session_state["page"] = "signup"
                st.rerun()
