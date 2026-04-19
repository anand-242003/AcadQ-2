"""
AcadIQ — Predict Your Academic Future
Main entry point: page config, CSS injection, routing.
"""
import streamlit as st


st.set_page_config(
    page_title="AcadIQ | Predict Your Academic Future",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed",
)


from styles import get_global_css, get_material_icons

st.markdown(get_global_css(), unsafe_allow_html=True)
st.markdown(get_material_icons(), unsafe_allow_html=True)


from models import load_all_models

models = load_all_models()
if not models.get("loaded"):
    st.error(f"⚠️ Models failed to load: {models.get('error', 'Unknown error')}")
    st.stop()


if "p" in st.query_params:
    val = st.query_params["p"]
    if val in ["dash", "plan", "quiz", "resources", "coach"]:
        st.session_state["page"] = "dashboard" if val == "dash" else val
    else:
        st.session_state["page"] = "landing"
    st.query_params.clear()

if "page" not in st.session_state:
    st.session_state["page"] = "landing"

page = st.session_state["page"]

if page == "landing":
    from views.landing import show_landing_page
    show_landing_page()

elif page == "login":
    from views.login import show_login_page
    show_login_page()

elif page == "signup":
    from views.signup import show_signup_page
    show_signup_page()

elif page == "input_wizard":
    from views.input_wizard import show_input_wizard
    show_input_wizard(models)

elif page == "dashboard":
    from views.dashboard import show_dashboard
    show_dashboard()

elif page == "coach":
    from views.coach import show_coach
    show_coach()

elif page == "plan":
    from views.plan import show_plan
    show_plan()

elif page == "quiz":
    from views.quiz import show_quiz_bot
    show_quiz_bot()

elif page == "resources":
    from views.resources import show_resources
    show_resources()

else:
    st.error(f"Unknown page: {page}")
    st.session_state["page"] = "landing"
    st.rerun()