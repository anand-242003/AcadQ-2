"""Landing page — Hero, pillars, stats, CTA, footer."""
import streamlit as st


def _nav():
    """Fixed top navigation bar."""
    st.markdown("""<style>
.nav-bar{position:fixed;top:0;left:0;right:0;z-index:9999;height:64px;display:flex;align-items:center;justify-content:space-between;padding:0 40px;background:rgba(250,249,247,.92);backdrop-filter:blur(20px);-webkit-backdrop-filter:blur(20px);border-bottom:1px solid rgba(218,192,196,.15);font-family:'Manrope',sans-serif}
.nav-logo{font-size:22px;font-weight:800;color:#6e1a37;letter-spacing:-.5px}
.nav-links{display:flex;gap:4px;align-items:center}
.nav-link{font-weight:600;font-size:13.5px;padding:7px 14px;border-radius:10px;text-decoration:none !important;color:rgba(26,28,27,.5) !important;transition:all .18s}
.nav-link:hover{background:#f4f3f1 !important;color:#510122 !important}
.nav-link-active{color:#6e1a37 !important;background:rgba(110,26,55,.07) !important}
</style>
<div class="nav-bar">
<div class="nav-logo">AcadIQ</div>
<div class="nav-links">
<a href="/?p=dash" class="nav-link nav-link-active">Predictor</a>
<a href="/?p=coach" class="nav-link">Coach</a>
<a href="/?p=methodology" class="nav-link">Methodology</a>
</div>
<div></div>
</div>""", unsafe_allow_html=True)
    st.markdown("<div style='height:66px'></div>", unsafe_allow_html=True)


def show_landing_page():
    """Render the complete landing page."""
    _nav()
    st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)

    hero_left, hero_right = st.columns([5, 5], gap="large")

    with hero_left:
        st.markdown('<div style="display:inline-flex;align-items:center;gap:8px;padding:6px 16px;border-radius:99px;background:#a7f1de;color:#1b6a5b;font-family:Manrope,sans-serif;font-weight:700;font-size:13px;border:1px solid rgba(27,106,91,.18);margin-bottom:24px;">★ 97.1% Prediction Accuracy</div>', unsafe_allow_html=True)

        st.markdown('<h1 style="font-family:Manrope,sans-serif;font-size:54px;font-weight:900;line-height:1.08;letter-spacing:-2.5px;color:#510122;margin:0 0 20px 0;">Predict Your<br>Academic Future<br>with <span style="color:#6e1a37">AcadIQ</span></h1>', unsafe_allow_html=True)

        st.markdown('<p style="font-size:17px;color:#544246;line-height:1.72;margin-bottom:32px;max-width:480px;font-family:Inter,sans-serif;">Harness the power of high-fidelity ML models to forecast your GPA, graduation outcomes, and research impact before the semester even begins.</p>', unsafe_allow_html=True)

        btn1, btn2 = st.columns(2)
        with btn1:
            if st.button("Get Started →", type="primary", use_container_width=True, key="hero_cta"):
                st.session_state["page"] = "login"
                st.rerun()
        with btn2:
            if st.button("Log In", use_container_width=True, key="hero_login"):
                st.session_state["page"] = "login"
                st.rerun()

        st.markdown('<div style="display:flex;align-items:center;gap:20px;margin-top:28px;flex-wrap:wrap;"><span style="font-size:13px;font-weight:600;color:#877276">50k+ students</span><span style="width:1px;height:18px;background:rgba(218,192,196,.5);display:inline-block"></span><span style="font-size:13px;font-weight:600;color:#877276">120+ institutions</span><span style="width:1px;height:18px;background:rgba(218,192,196,.5);display:inline-block"></span><span style="font-size:13px;font-weight:600;color:#877276">0.4s inference</span></div>', unsafe_allow_html=True)

    with hero_right:
        st.markdown('<div style="background:rgba(227,226,224,.6);backdrop-filter:blur(24px);border-radius:22px;padding:40px;border:1px solid rgba(255,255,255,.25);text-align:center;box-shadow:0 24px 64px rgba(81,1,34,.08)"><div style="font-family:Manrope,sans-serif;font-size:68px;font-weight:900;color:#ae2448;line-height:1;letter-spacing:-4px;margin-bottom:8px">97.1%</div><div style="font-family:Manrope,sans-serif;font-size:11px;font-weight:800;text-transform:uppercase;letter-spacing:4px;color:#510122;margin-bottom:20px">Prediction Accuracy</div><div style="height:8px;background:#e3e2e0;border-radius:99px;overflow:hidden;margin-bottom:10px"><div style="height:100%;width:97%;background:linear-gradient(90deg,#1b6a5b,#2ea892);border-radius:99px"></div></div><div style="display:flex;justify-content:space-between;font-size:9px;font-weight:700;text-transform:uppercase;letter-spacing:1.5px;color:rgba(135,114,118,.5);margin-bottom:24px"><span>Historical Data</span><span>Real-Time ML</span></div></div>', unsafe_allow_html=True)

        mc1, mc2 = st.columns(2)
        with mc1:
            st.markdown('<div style="background:#fff;border-radius:16px;padding:18px 20px;border:1px solid rgba(218,192,196,.2);box-shadow:0 4px 16px rgba(81,1,34,.04);margin-top:12px"><div style="font-family:Manrope,sans-serif;font-size:10px;font-weight:800;text-transform:uppercase;letter-spacing:1.5px;color:#877276;margin-bottom:5px">Model Accuracy</div><div style="font-family:Manrope,sans-serif;font-size:28px;font-weight:900;color:#510122;letter-spacing:-1px">94.2%</div></div>', unsafe_allow_html=True)
        with mc2:
            st.markdown('<div style="background:#fff;border-radius:16px;padding:18px 20px;border:1px solid rgba(218,192,196,.2);box-shadow:0 4px 16px rgba(81,1,34,.04);margin-top:12px"><div style="font-family:Manrope,sans-serif;font-size:10px;font-weight:800;text-transform:uppercase;letter-spacing:1.5px;color:#877276;margin-bottom:5px">Pass Probability</div><div style="font-family:Manrope,sans-serif;font-size:28px;font-weight:900;color:#1b6a5b;letter-spacing:-1px">88%</div></div>', unsafe_allow_html=True)

    # ── Pillars Section ───────────────────────────────────────────────────────
    st.markdown('<div style="background:#f4f3f1;padding:60px 0 0;margin-top:60px"><div style="max-width:1200px;margin:0 auto;padding:0 40px"><h2 style="font-family:Manrope,sans-serif;font-size:40px;font-weight:900;color:#510122;letter-spacing:-1.5px;line-height:1.1;margin-bottom:12px">Built on Two Scientific Pillars</h2><p style="font-size:16px;color:#544246;line-height:1.7;max-width:540px;margin-bottom:8px">Our architecture combines predictive modelling with generative intelligence to support every stage of the academic lifecycle.</p></div></div>', unsafe_allow_html=True)

    st.markdown('<div style="background:#f4f3f1;padding:20px 0 60px">', unsafe_allow_html=True)
    p1, p2 = st.columns(2, gap="medium")

    with p1:
        st.markdown('<div style="background:#fff;border-radius:22px;padding:40px;border:1px solid rgba(218,192,196,.12)"><div style="width:56px;height:56px;border-radius:16px;background:#ffd9e0;display:flex;align-items:center;justify-content:center;margin-bottom:24px"><span style="font-family:Manrope,sans-serif;font-weight:900;font-size:14px;color:#510122">ML</span></div><h3 style="font-family:Manrope,sans-serif;font-size:22px;font-weight:800;color:#510122;margin-bottom:12px">ML Prediction Engine</h3><p style="font-size:14.5px;color:#544246;line-height:1.72;margin-bottom:24px">Neural networks trained on millions of academic data points identify performance patterns before they manifest. Get early warnings and strategic pivots.</p><div style="display:flex;gap:10px"><div style="flex:1;background:#f4f3f1;border-radius:12px;padding:14px 10px;text-align:center;border:1px solid rgba(218,192,196,.12)"><span style="font-family:Manrope;font-size:19px;font-weight:900;color:#510122">94.2%</span><br><span style="font-size:9px;font-weight:800;text-transform:uppercase;letter-spacing:1px;color:#877276">Accuracy</span></div><div style="flex:1;background:#f4f3f1;border-radius:12px;padding:14px 10px;text-align:center;border:1px solid rgba(218,192,196,.12)"><span style="font-family:Manrope;font-size:19px;font-weight:900;color:#510122">3</span><br><span style="font-size:9px;font-weight:800;text-transform:uppercase;letter-spacing:1px;color:#877276">Models</span></div><div style="flex:1;background:#f4f3f1;border-radius:12px;padding:14px 10px;text-align:center;border:1px solid rgba(218,192,196,.12)"><span style="font-family:Manrope;font-size:19px;font-weight:900;color:#510122">20+</span><br><span style="font-size:9px;font-weight:800;text-transform:uppercase;letter-spacing:1px;color:#877276">Features</span></div></div></div>', unsafe_allow_html=True)

    with p2:
        st.markdown('<div style="background:#fff;border-radius:22px;padding:40px;border:1px solid rgba(218,192,196,.12)"><div style="width:56px;height:56px;border-radius:16px;background:#a7f1de;display:flex;align-items:center;justify-content:center;margin-bottom:24px"><span style="font-family:Manrope,sans-serif;font-weight:900;font-size:14px;color:#1b6a5b">AI</span></div><h3 style="font-family:Manrope,sans-serif;font-size:22px;font-weight:800;color:#1b6a5b;margin-bottom:12px">Generative AI Coaching</h3><p style="font-size:14.5px;color:#544246;line-height:1.72;margin-bottom:24px">Beyond data, AcadIQ provides context. Our coach understands complex academic material, providing Socratic guidance and personalised study schedules.</p><div style="display:flex;gap:10px"><div style="flex:1;background:#f4f3f1;border-radius:12px;padding:14px 10px;text-align:center;border:1px solid rgba(218,192,196,.12)"><span style="font-family:Manrope;font-size:19px;font-weight:900;color:#1b6a5b">&lt;2s</span><br><span style="font-size:9px;font-weight:800;text-transform:uppercase;letter-spacing:1px;color:#877276">Response</span></div><div style="flex:1;background:#f4f3f1;border-radius:12px;padding:14px 10px;text-align:center;border:1px solid rgba(218,192,196,.12)"><span style="font-family:Manrope;font-size:19px;font-weight:900;color:#1b6a5b">7-Day</span><br><span style="font-size:9px;font-weight:800;text-transform:uppercase;letter-spacing:1px;color:#877276">Plans</span></div><div style="flex:1;background:#f4f3f1;border-radius:12px;padding:14px 10px;text-align:center;border:1px solid rgba(218,192,196,.12)"><span style="font-family:Manrope;font-size:19px;font-weight:900;color:#1b6a5b">24/7</span><br><span style="font-size:9px;font-weight:800;text-transform:uppercase;letter-spacing:1px;color:#877276">Available</span></div></div></div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # ── Stats Section ─────────────────────────────────────────────────────────
    st.markdown("<div style='height:40px'></div>", unsafe_allow_html=True)
    s1, s2, s3, s4 = st.columns(4)
    with s1:
        st.markdown('<div style="text-align:center;padding:28px 12px"><div style="font-family:Manrope;font-size:46px;font-weight:900;color:#510122;letter-spacing:-2px">50k+</div><div style="font-size:10px;font-weight:800;text-transform:uppercase;letter-spacing:2.5px;color:#877276;margin-top:6px">Active Students</div></div>', unsafe_allow_html=True)
    with s2:
        st.markdown('<div style="text-align:center;padding:28px 12px"><div style="font-family:Manrope;font-size:46px;font-weight:900;color:#510122;letter-spacing:-2px">120+</div><div style="font-size:10px;font-weight:800;text-transform:uppercase;letter-spacing:2.5px;color:#877276;margin-top:6px">Partner Institutions</div></div>', unsafe_allow_html=True)
    with s3:
        st.markdown('<div style="text-align:center;padding:28px 12px"><div style="font-family:Manrope;font-size:46px;font-weight:900;color:#1b6a5b;letter-spacing:-2px">0.4s</div><div style="font-size:10px;font-weight:800;text-transform:uppercase;letter-spacing:2.5px;color:#877276;margin-top:6px">Inference Time</div></div>', unsafe_allow_html=True)
    with s4:
        st.markdown('<div style="text-align:center;padding:28px 12px"><div style="font-family:Manrope;font-size:46px;font-weight:900;color:#1b6a5b;letter-spacing:-2px">A+</div><div style="font-size:10px;font-weight:800;text-transform:uppercase;letter-spacing:2.5px;color:#877276;margin-top:6px">User Avg Improvement</div></div>', unsafe_allow_html=True)

    # ── CTA Banner ────────────────────────────────────────────────────────────
    st.markdown('<div style="margin:40px auto;max-width:1200px;padding:0 20px"><div style="background:linear-gradient(130deg,#3f0019 0%,#6e1a37 55%,#8a2040 100%);border-radius:26px;padding:64px 72px;display:flex;justify-content:space-between;align-items:center;gap:40px;position:relative;overflow:hidden"><div style="position:absolute;top:-80px;right:-80px;width:350px;height:350px;border-radius:50%;background:radial-gradient(circle,rgba(255,255,255,.06),transparent 70%);pointer-events:none"></div><div style="position:relative;z-index:1"><div style="font-family:Manrope;font-size:10px;font-weight:800;text-transform:uppercase;letter-spacing:3px;color:rgba(255,255,255,.4);margin-bottom:12px">Start Today — Free</div><div style="font-family:Manrope;font-size:36px;font-weight:900;color:#fff;letter-spacing:-1.5px;line-height:1.1">Ready to Own<br>Your Academic Future?</div><p style="font-size:15px;color:rgba(255,255,255,.55);margin-top:12px;line-height:1.6">Join 50,000+ students who transformed their approach with AcadIQ.</p></div><div style="position:relative;z-index:1;flex-shrink:0;text-align:center"><div style="font-size:11px;color:rgba(255,255,255,.35);margin-top:8px;font-weight:500">No credit card · Setup in 2 min</div></div></div></div>', unsafe_allow_html=True)

    _, cta_btn, _ = st.columns([5, 2, 5])
    with cta_btn:
        if st.button("Create Free Account →", type="primary", use_container_width=True, key="footer_cta"):
            st.session_state["page"] = "signup"
            st.rerun()

    # ── Footer ────────────────────────────────────────────────────────────────
    st.markdown('<div style="background:#faf9f7;border-top:1px solid rgba(218,192,196,.15);padding:32px 40px;margin-top:40px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:20px"><div><div style="font-family:Manrope;font-size:18px;font-weight:900;color:#6e1a37;letter-spacing:-.5px">AcadIQ</div><div style="font-family:Manrope;font-size:11px;font-weight:600;color:rgba(26,28,27,.3);text-transform:uppercase;letter-spacing:1.5px;margin-top:4px">© 2024 AcadIQ Analytics. All rights reserved.</div></div><div style="display:flex;gap:24px"><span style="font-family:Manrope;font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:1.5px;color:rgba(26,28,27,.3)">Privacy Policy</span><span style="font-family:Manrope;font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:1.5px;color:rgba(26,28,27,.3)">Terms of Service</span><span style="font-family:Manrope;font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:1.5px;color:rgba(26,28,27,.3)">Research Docs</span></div></div>', unsafe_allow_html=True)
