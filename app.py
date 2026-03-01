import streamlit as st

from styles import get_css
from models import load_all_models
from pages import show_input_page, show_results_page

st.set_page_config(
    page_title="AcadIQ · Student Performance Predictor",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(get_css(), unsafe_allow_html=True)

models = load_all_models()

if not models['loaded']:
    st.error(f"""
**Models not found** — `{models.get('error')}`
Place these files in the Notebook/student_ml_app/ folder:
`classification_model.pkl` · `regression_model.pkl` · `clustering_model.pkl`
`scaler.pkl` · `feature_columns.pkl` · `cluster_label_map.pkl`
    """)
    st.stop()

for key, default in [('page', 'input'), ('results', {}), ('raw_input', {}), ('validation_warns', [])]:
    if key not in st.session_state:
        st.session_state[key] = default

page = st.session_state['page']

if page == 'landing':
    show_landing_page()
elif page == 'input':
    show_input_page(models)
else:
    show_results_page()