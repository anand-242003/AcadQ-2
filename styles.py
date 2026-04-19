"""
AcadIQ Design System — Light Material Design 3 Theme
Colors: Manrope headlines, Inter body, maroon/teal palette on #faf9f7
"""


def get_global_css() -> str:
    """Return full global CSS injected once."""
    return """
<style>
/* ─── Google Fonts ───────────────────────────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800;900&family=Inter:wght@300;400;500;600;700&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap');

/* ─── Design Tokens ─────────────────────────────────────────────────────── */
:root {
    --primary: #510122;
    --primary-container: #6e1a37;
    --on-primary: #ffffff;
    --on-primary-container: #f283a0;
    --secondary: #1b6a5b;
    --secondary-container: #a7f1de;
    --on-secondary: #ffffff;
    --on-secondary-container: #247061;
    --surface: #faf9f7;
    --surface-container-low: #f4f3f1;
    --surface-container: #efeeec;
    --surface-container-high: #e9e8e6;
    --surface-container-highest: #e3e2e0;
    --surface-container-lowest: #ffffff;
    --on-surface: #1a1c1b;
    --on-surface-variant: #544246;
    --outline: #877276;
    --outline-variant: #dac0c4;
    --error: #ba1a1a;
    --error-container: #ffdad6;
    --accent-red: #ae2448;
    --font-headline: 'Manrope', sans-serif;
    --font-body: 'Inter', sans-serif;
}

/* ─── Global Reset ──────────────────────────────────────────────────────── */
*, *::before, *::after { box-sizing: border-box; }

html, body, .stApp, [class*="css"] {
    background: var(--surface) !important;
    color: var(--on-surface) !important;
    font-family: var(--font-body) !important;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
}

/* ─── Hide Streamlit Chrome ─────────────────────────────────────────────── */
#MainMenu, footer, header,
[data-testid="stDecoration"],
[data-testid="stStatusWidget"],
.stDeployButton,
[data-testid="stToolbar"] { display: none !important; }

/* ─── Layout Overrides ──────────────────────────────────────────────────── */
.block-container {
    padding: 2rem 5% 4rem !important;
    max-width: 1400px !important;
    margin: 0 auto !important;
}
.element-container { margin: 0 !important; }
.stMarkdown { margin: 0 !important; }

/* Sidebar completely hidden by default */
[data-testid="stSidebar"] { display: none !important; }
section[data-testid="stSidebar"] { display: none !important; }
button[kind="header"] { display: none !important; }

/* ─── Typography ────────────────────────────────────────────────────────── */
h1, h2, h3, .headline {
    font-family: var(--font-headline) !important;
    color: var(--primary);
}

/* ─── Buttons ───────────────────────────────────────────────────────────── */
.stButton > button {
    font-family: var(--font-headline) !important;
    font-weight: 700 !important;
    border-radius: 12px !important;
    border: none !important;
    transition: all .2s ease !important;
    cursor: pointer !important;
}
.stButton > button[kind="primary"] {
    background: var(--primary-container) !important;
    color: var(--on-primary) !important;
    padding: 14px 32px !important;
    box-shadow: 0 8px 28px rgba(110,26,55,.22) !important;
    font-size: 15px !important;
}
.stButton > button[kind="primary"]:hover {
    filter: brightness(1.1) !important;
    transform: translateY(-1px) !important;
}
.stButton > button[kind="primary"]:active {
    transform: scale(0.97) !important;
}
.stButton > button[kind="secondary"],
.stButton > button:not([kind="primary"]) {
    background: var(--surface-container-low) !important;
    color: var(--primary) !important;
    border: 1.5px solid rgba(218,192,196,.5) !important;
    padding: 14px 28px !important;
    font-size: 15px !important;
}
.stButton > button[kind="secondary"]:hover,
.stButton > button:not([kind="primary"]):hover {
    background: var(--surface-container-high) !important;
    transform: translateY(-1px) !important;
}

/* ─── Text Inputs ───────────────────────────────────────────────────────── */
.stTextInput > label {
    font-family: var(--font-body) !important;
    font-size: 11px !important;
    font-weight: 700 !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    color: var(--on-surface-variant) !important;
}
.stTextInput input {
    background: transparent !important;
    border: 0 !important;
    border-bottom: 2px solid rgba(218,192,196,.3) !important;
    border-radius: 0 !important;
    padding: 12px 16px !important;
    font-size: 16px !important;
    font-weight: 500 !important;
    color: var(--on-surface) !important;
    transition: border-color .3s !important;
}
.stTextInput input:focus {
    border-bottom-color: var(--primary) !important;
    box-shadow: none !important;
}
.stTextInput input::placeholder {
    color: rgba(218,192,196,.6) !important;
}

/* ─── Number Inputs ─────────────────────────────────────────────────────── */
.stNumberInput > label {
    font-family: var(--font-headline) !important;
    font-size: 12px !important;
    font-weight: 600 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    color: var(--on-surface-variant) !important;
}
.stNumberInput input {
    background: transparent !important;
    border: 0 !important;
    border-bottom: 2px solid rgba(218,192,196,.3) !important;
    border-radius: 0 !important;
    padding: 12px 0 !important;
    font-size: 22px !important;
    font-weight: 500 !important;
    color: var(--on-surface) !important;
}
.stNumberInput input:focus {
    border-bottom-color: var(--primary) !important;
    box-shadow: none !important;
}

/* ─── Sliders ───────────────────────────────────────────────────────────── */
.stSlider > label {
    font-size: 13px !important;
    font-weight: 500 !important;
    color: var(--on-surface-variant) !important;
}
div[data-baseweb="slider"] > div > div {
    background: var(--surface-container-highest) !important;
}
div[data-baseweb="slider"] > div > div > div {
    background: var(--primary-container) !important;
}
div[data-baseweb="slider"] [role="slider"] {
    background: var(--on-primary) !important;
    border: 2px solid var(--primary-container) !important;
    width: 16px !important;
    height: 16px !important;
    box-shadow: 0 2px 8px rgba(110,26,55,.2) !important;
}
.stSlider [data-testid="stTickBar"] { display: none !important; }

/* ─── Selectbox ─────────────────────────────────────────────────────────── */
.stSelectbox > label {
    font-size: 13px !important;
    font-weight: 500 !important;
    color: var(--on-surface-variant) !important;
}
.stSelectbox > div > div {
    background: var(--surface-container-lowest) !important;
    border: 1px solid var(--outline-variant) !important;
    border-radius: 12px !important;
    color: var(--on-surface) !important;
    font-size: 14px !important;
}
.stSelectbox > div > div:focus-within {
    border-color: var(--primary) !important;
    box-shadow: 0 0 0 3px rgba(110,26,55,.08) !important;
}
[data-baseweb="popover"], [data-baseweb="menu"] {
    background: var(--surface-container-lowest) !important;
    border: 1px solid var(--outline-variant) !important;
    border-radius: 12px !important;
}
[data-baseweb="option"] {
    background: transparent !important;
    color: var(--on-surface) !important;
    font-size: 13px !important;
}
[data-baseweb="option"]:hover,
[aria-selected="true"][data-baseweb="option"] {
    background: rgba(110,26,55,.06) !important;
    color: var(--primary) !important;
}

/* ─── Radio Buttons ─────────────────────────────────────────────────────── */
.stRadio > label {
    font-size: 13px !important;
    font-weight: 500 !important;
    color: var(--on-surface-variant) !important;
}

/* ─── Tabs ──────────────────────────────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {
    background: transparent !important;
    border-bottom: 1px solid var(--outline-variant) !important;
    gap: 0 !important;
}
.stTabs [data-baseweb="tab"] {
    font-family: var(--font-headline) !important;
    font-size: 12px !important;
    font-weight: 600 !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase !important;
    color: var(--outline) !important;
    padding: 12px 20px !important;
    background: transparent !important;
    border-bottom: 2px solid transparent !important;
}
.stTabs [aria-selected="true"] {
    color: var(--primary) !important;
    border-bottom: 2px solid var(--primary-container) !important;
    background: transparent !important;
}

/* ─── Metrics ───────────────────────────────────────────────────────────── */
[data-testid="stMetric"] {
    background: var(--surface-container-lowest) !important;
    border: 1px solid rgba(218,192,196,.15) !important;
    border-radius: 16px !important;
    padding: 20px !important;
    transition: all .2s !important;
}
[data-testid="stMetric"]:hover {
    border-color: var(--outline-variant) !important;
    transform: translateY(-2px) !important;
}
[data-testid="stMetricLabel"] p {
    font-family: var(--font-headline) !important;
    font-size: 10px !important;
    font-weight: 700 !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    color: var(--outline) !important;
}
[data-testid="stMetricValue"] {
    font-family: var(--font-headline) !important;
    font-size: 26px !important;
    font-weight: 800 !important;
    color: var(--primary) !important;
    letter-spacing: -0.02em !important;
}

/* ─── Expander ──────────────────────────────────────────────────────────── */
.streamlit-expanderHeader {
    background: var(--surface-container-low) !important;
    border: 1px solid rgba(218,192,196,.15) !important;
    border-radius: 12px !important;
    color: var(--on-surface-variant) !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    padding: 14px 18px !important;
}
.streamlit-expanderContent {
    background: var(--surface-container-lowest) !important;
    border: 1px solid rgba(218,192,196,.15) !important;
    border-top: none !important;
    border-radius: 0 0 12px 12px !important;
    padding: 20px !important;
}

/* ─── Misc ──────────────────────────────────────────────────────────────── */
hr {
    border: none !important;
    border-top: 1px solid var(--outline-variant) !important;
    margin: 32px 0 !important;
    opacity: 0.3 !important;
}
.stSpinner > div { border-top-color: var(--primary-container) !important; }
.stCaption p {
    font-size: 11px !important;
    color: var(--outline) !important;
}
.stAlert {
    background: var(--surface-container-low) !important;
    border: 1px solid rgba(218,192,196,.15) !important;
    border-radius: 12px !important;
    font-size: 13px !important;
}
[data-testid="stDataFrame"] {
    border-radius: 12px !important;
    border: 1px solid rgba(218,192,196,.15) !important;
    overflow: hidden !important;
}
.stProgress > div > div {
    background: var(--surface-container-highest) !important;
    border-radius: 99px !important;
}
.stProgress > div > div > div {
    background: var(--primary-container) !important;
    border-radius: 99px !important;
}
</style>
"""


def get_material_icons():
    """Material Symbols Outlined CSS injection."""
    return """
<style>
.material-symbols-outlined {
    font-family: 'Material Symbols Outlined';
    font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24;
    display: inline-block;
    vertical-align: middle;
}
</style>
"""
