def get_css() -> str:
    return """
<style>
:root {
    --bg: #000000;
    --surface: #0A0A0A;
    --elevated: #141414;
    --border: #1E1E1E;
    --divider: #262626;
    --text-primary: #E0E0E0;
    --text-secondary: #A0A0A0;
    --text-muted: #6B6B6B;
    --text-heading: #FFFFFF;
    --text-disabled: #404040;
    --brand: #FFFFFF;
    --brand-hover: #D4D4D4;
    --brand-active: #B0B0B0;
    --brand-soft: rgba(255,255,255,0.08);
    --success: #10B981;
    --warning: #F59E0B;
    --danger: #EF4444;
    --info: #3B82F6;
    --success-bg: rgba(16,185,129,0.15);
    --warning-bg: rgba(245,158,11,0.15);
    --danger-bg: rgba(239,68,68,0.15);
    --info-bg: rgba(59,130,246,0.15);
    --input-bg: #0A0A0A;
    --input-border: #1E1E1E;
    --input-focus: #FFFFFF;
    --input-text: #E0E0E0;
    --placeholder: #6B6B6B;
    --track: #2A2A2A;
    --track-active: #FFFFFF;
    --handle: #FFFFFF;
    --handle-border: #1E1E1E;
    --btn-primary-bg: #FFFFFF;
    --btn-primary-hover: #D4D4D4;
    --btn-primary-text: #000000;
    --btn-secondary-bg: #1A1A1A;
    --btn-secondary-hover: #2A2A2A;
    --btn-secondary-text: #E0E0E0;
    --btn-ghost-hover: rgba(255,255,255,0.08);
    --card-bg: #0A0A0A;
    --card-border: #1E1E1E;
    --card-hover-border: #FFFFFF;
    --card-shadow: 0 0 0 1px rgba(255,255,255,0.02), 0 10px 30px rgba(0,0,0,0.50);
    --chart-1: #FFFFFF;
    --chart-2: #10B981;
    --chart-3: #F59E0B;
    --chart-4: #EF4444;
    --chart-5: #3B82F6;
    --chart-grid: #1E1E1E;
    --chart-axis: #A0A0A0;
    --nav-bg: #000000;
    --nav-active-bg: rgba(255,255,255,0.08);
    --nav-hover-bg: rgba(255,255,255,0.04);
    --nav-text: #A0A0A0;
    --nav-active-text: #FFFFFF;
    --r-sm: 6px;
    --r-md: 8px;
    --r-lg: 12px;
    --r-xl: 16px;
    --font: -apple-system, BlinkMacSystemFont, "Segoe UI", system-ui, sans-serif;
    --mono: "SF Mono", "Fira Code", ui-monospace, monospace;
}

html, body, [class*="css"] {
    font-family: var(--font) !important;
    background-color: var(--bg) !important;
    color: var(--text-primary) !important;
    -webkit-font-smoothing: antialiased;
}
#MainMenu, footer, header { visibility: hidden; }
.block-container {
    padding: 0 48px 80px 48px !important;
    max-width: 1400px !important;
    margin: 0 auto !important;
}
* { box-sizing: border-box; }


.page-wrap { max-width: 1200px; margin: 0 auto; padding: 0 48px; }

.hero { display: flex; flex-direction: column; align-items: center; text-align: center; padding: 100px 48px 56px; position: relative; overflow: hidden; }
.hero-bg-glow { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -60%); width: 800px; height: 600px; background: radial-gradient(ellipse at center, rgba(255,255,255,0.06) 0%, rgba(255,255,255,0.02) 40%, transparent 70%); pointer-events: none; }
.hero-bg-grid { position: absolute; inset: 0; background-image: linear-gradient(var(--divider) 1px, transparent 1px), linear-gradient(90deg, var(--divider) 1px, transparent 1px); background-size: 48px 48px; opacity: 0.3; mask-image: radial-gradient(ellipse at center, black 30%, transparent 80%); -webkit-mask-image: radial-gradient(ellipse at center, black 30%, transparent 80%); }
.hero-badge { display: inline-flex; align-items: center; gap: 8px; background: var(--brand-soft); border: 1px solid rgba(255,255,255,0.2); border-radius: 20px; padding: 6px 16px; margin-bottom: 32px; font-size: 12px; font-weight: 600; color: var(--brand-hover); letter-spacing: 0.04em; }
.hero-badge-dot { width: 6px; height: 6px; border-radius: 50%; background: var(--brand); animation: pulse 2s infinite; }
@keyframes pulse { 0%, 100% { opacity: 1; transform: scale(1); } 50% { opacity: 0.6; transform: scale(0.85); } }
.hero-title { font-size: 64px; font-weight: 800; color: var(--text-heading); letter-spacing: -0.04em; line-height: 1.08; margin-bottom: 24px; max-width: 760px; }
.hero-title-accent { color: var(--brand-hover); }
.hero-desc { font-size: 18px; font-weight: 400; color: var(--text-secondary); line-height: 1.7; max-width: 540px; margin: 0 auto 48px; }
.hero-cta-group { display: flex; align-items: center; justify-content: center; gap: 16px; margin-bottom: 56px; }
.hero-stats-row { display: flex; align-items: center; gap: 48px; justify-content: center; padding: 40px 48px 64px; border-top: 1px solid var(--divider); margin-top: 40px; max-width: 1100px; margin-left: auto; margin-right: auto; width: 100%; }
.hero-stat { text-align: center; }
.hero-stat-num { font-family: var(--mono); font-size: 28px; font-weight: 700; color: var(--text-heading); letter-spacing: -0.03em; }
.hero-stat-lbl { font-size: 12px; color: var(--text-muted); margin-top: 4px; }
.hero-stat-sep { width: 1px; height: 40px; background: var(--border); }

.feature-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; max-width: 1100px; margin: 80px auto 0; padding: 0 48px; }
.feature-card { background: var(--surface); border: 1px solid var(--card-border); border-radius: var(--r-lg); padding: 28px; box-shadow: var(--card-shadow); transition: border-color 0.2s, transform 0.2s; }
.feature-card:hover { border-color: var(--card-hover-border); transform: translateY(-2px); }
.feature-icon { width: 40px; height: 40px; border-radius: var(--r-md); background: var(--brand-soft); display: flex; align-items: center; justify-content: center; margin-bottom: 16px; font-size: 18px; }
.feature-title { font-size: 15px; font-weight: 700; color: var(--text-heading); margin-bottom: 8px; }
.feature-desc { font-size: 13px; color: var(--text-secondary); line-height: 1.65; }

.how-section { max-width: 1100px; margin: 80px auto 0; padding: 0 48px; }
.section-tag { font-size: 11px; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase; color: var(--brand); margin-bottom: 12px; }
.section-title { font-size: 32px; font-weight: 800; color: var(--text-heading); letter-spacing: -0.02em; margin-bottom: 16px; }
.section-desc { font-size: 15px; color: var(--text-secondary); line-height: 1.65; max-width: 520px; margin-bottom: 48px; }
.steps-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 24px; }
.step-card { background: var(--surface); border: 1px solid var(--card-border); border-radius: var(--r-lg); padding: 28px; box-shadow: var(--card-shadow); position: relative; }
.step-num { font-family: var(--mono); font-size: 11px; font-weight: 700; color: var(--brand); background: var(--brand-soft); border-radius: 4px; padding: 3px 8px; display: inline-block; margin-bottom: 16px; letter-spacing: 0.06em; }
.step-title { font-size: 15px; font-weight: 700; color: var(--text-heading); margin-bottom: 8px; }
.step-desc { font-size: 13px; color: var(--text-secondary); line-height: 1.65; }

.page-header { padding: 40px 48px 32px; border-bottom: 1px solid var(--border); margin-bottom: 40px; }
.page-header-inner { max-width: 1200px; margin: 0 auto; }
.breadcrumb { display: flex; align-items: center; gap: 8px; font-size: 12px; color: var(--text-muted); margin-bottom: 10px; }
.bc-sep { color: var(--border); }
.bc-cur { color: var(--text-secondary); font-weight: 500; }
.page-h1 { font-size: 26px; font-weight: 800; color: var(--text-heading); letter-spacing: -0.02em; margin-bottom: 8px; }
.page-sub { font-size: 14px; color: var(--text-muted); line-height: 1.6; max-width: 560px; }

.input-wrap { max-width: 1200px; margin: 0 auto; padding: 0 48px 80px; }
.input-panel { background: var(--surface); border: 1px solid var(--card-border); border-radius: var(--r-xl); padding: 28px 24px; box-shadow: var(--card-shadow); height: 100%; }
.panel-section-title { font-size: 11px; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase; color: var(--text-muted); padding-bottom: 10px; border-bottom: 1px solid var(--divider); margin-bottom: 20px; }
.panel-section-title + .panel-section-title, .sub-section { margin-top: 24px; }

.summary-card { background: var(--elevated); border: 1px solid var(--card-border); border-radius: var(--r-md); padding: 13px 16px; margin-bottom: 8px; transition: border-color 0.15s; }
.summary-card:hover { border-color: var(--brand); }
.summary-card.success { border-left: 3px solid var(--success); }
.summary-card.warning { border-left: 3px solid var(--warning); }
.summary-card.danger { border-left: 3px solid var(--danger); }
.sc-label { font-size: 10px; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; color: var(--text-muted); margin-bottom: 4px; }
.sc-value { font-family: var(--mono); font-size: 17px; font-weight: 700; color: var(--text-primary); letter-spacing: -0.02em; }
.sc-value.brand { color: var(--brand-hover); }
.sc-value.success { color: var(--success); }
.sc-value.warning { color: var(--warning); }
.sc-value.danger { color: var(--danger); }
.sc-sub { font-size: 11px; color: var(--text-muted); margin-top: 3px; }

.results-wrap { max-width: 1200px; margin: 0 auto; padding: 0 48px 80px; }
.score-card { background: var(--surface); border: 1px solid var(--card-border); border-radius: var(--r-xl); padding: 32px; box-shadow: var(--card-shadow); position: relative; overflow: hidden; margin-bottom: 0; }
.score-card::after { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px; background: linear-gradient(90deg, var(--brand), var(--brand-hover), transparent); }
.score-eyebrow { font-size: 10px; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase; color: var(--text-muted); margin-bottom: 14px; }
.score-number { font-family: var(--mono); font-size: 80px; font-weight: 800; letter-spacing: -0.05em; line-height: 1; }
.score-denom { font-family: var(--mono); font-size: 18px; font-weight: 500; color: var(--text-muted); vertical-align: super; margin-left: 4px; }
.score-grade-badge { font-family: var(--mono); font-size: 20px; font-weight: 800; padding: 6px 18px; border-radius: var(--r-sm); display: inline-block; margin-left: 12px; vertical-align: middle; }
.prog-track { background: var(--elevated); border-radius: 99px; height: 4px; margin: 20px 0; overflow: hidden; }
.prog-fill { height: 100%; border-radius: 99px; transition: width 0.8s cubic-bezier(0.4,0,0.2,1); }
.result-chip { display: inline-flex; align-items: center; gap: 6px; font-size: 11px; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; padding: 5px 14px; border-radius: 4px; }
.result-chip.pass { background: var(--success-bg); color: var(--success); border: 1px solid rgba(16,185,129,0.3); }
.result-chip.fail { background: var(--danger-bg); color: var(--danger); border: 1px solid rgba(239,68,68,0.3); }
.result-chip::before { content: ''; width: 5px; height: 5px; border-radius: 50%; background: currentColor; }
.result-label { font-size: 14px; color: var(--text-secondary); font-weight: 500; margin-left: 8px; }

[data-testid="stMetric"] { background: var(--surface) !important; border: 1px solid var(--card-border) !important; border-radius: var(--r-lg) !important; padding: 20px !important; box-shadow: var(--card-shadow) !important; transition: border-color 0.15s !important; }
[data-testid="stMetric"]:hover { border-color: var(--brand) !important; }
[data-testid="stMetricLabel"] p { font-size: 10px !important; font-weight: 700 !important; letter-spacing: 0.1em !important; text-transform: uppercase !important; color: var(--text-muted) !important; }
[data-testid="stMetricValue"] { font-family: var(--mono) !important; font-size: 22px !important; font-weight: 700 !important; color: var(--text-heading) !important; letter-spacing: -0.02em !important; }
[data-testid="stMetricDelta"] { font-size: 11px !important; }

.learner-card { background: var(--brand-soft); border: 1px solid rgba(255,255,255,0.2); border-radius: var(--r-lg); padding: 20px; margin-bottom: 16px; }
.learner-eyebrow { font-size: 10px; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase; color: var(--brand-hover); margin-bottom: 8px; }
.learner-name { font-size: 18px; font-weight: 700; color: var(--text-heading); letter-spacing: -0.01em; margin-bottom: 8px; }
.learner-meta { font-size: 12px; color: var(--text-muted); display: flex; gap: 12px; flex-wrap: wrap; }
.learner-meta-item { display: flex; align-items: center; gap: 6px; }
.learner-meta-dot { width: 4px; height: 4px; border-radius: 50%; background: var(--text-disabled); }

.tip-card { background: var(--surface); border: 1px solid var(--card-border); border-radius: var(--r-md); padding: 14px 16px; margin-bottom: 8px; display: flex; gap: 12px; transition: border-color 0.15s; }
.tip-card:hover { border-color: var(--brand); }
.tip-indicator { width: 3px; border-radius: 99px; background: var(--brand); flex-shrink: 0; min-height: 36px; }
.tip-cat { font-size: 10px; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; color: var(--brand-hover); margin-bottom: 5px; }
.tip-txt { font-size: 13px; color: var(--text-secondary); line-height: 1.6; }

.chart-panel { background: var(--surface); border: 1px solid var(--card-border); border-radius: var(--r-xl); padding: 24px; box-shadow: var(--card-shadow); }
.section-lbl { font-size: 11px; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; color: var(--text-muted); padding-bottom: 10px; border-bottom: 1px solid var(--divider); margin-bottom: 20px; }

.stButton > button[kind="primary"] { background: var(--btn-primary-bg) !important; color: var(--btn-primary-text) !important; border: none !important; border-radius: var(--r-sm) !important; font-family: var(--font) !important; font-size: 13px !important; font-weight: 700 !important; padding: 14px 32px !important; transition: all 0.15s ease !important; box-shadow: 0 0 20px rgba(255,255,255,0.10) !important; }
.stButton > button[kind="primary"]:hover { background: var(--btn-primary-hover) !important; box-shadow: 0 0 32px rgba(255,255,255,0.18) !important; transform: translateY(-1px) !important; }
.stButton > button[kind="primary"]:active { background: var(--brand-active) !important; transform: translateY(0) !important; }
.stButton > button:not([kind="primary"]) { background: var(--btn-secondary-bg) !important; color: var(--btn-secondary-text) !important; border: 1px solid var(--border) !important; border-radius: var(--r-sm) !important; font-family: var(--font) !important; font-size: 13px !important; font-weight: 600 !important; padding: 12px 24px !important; transition: all 0.15s ease !important; box-shadow: none !important; }
.stButton > button:not([kind="primary"]):hover { background: var(--btn-secondary-hover) !important; border-color: var(--brand) !important; color: var(--text-heading) !important; transform: translateY(-1px) !important; }

.stSlider > label { font-size: 13px !important; font-weight: 500 !important; color: var(--text-secondary) !important; }
div[data-baseweb="slider"] > div > div { background: var(--track) !important; }
div[data-baseweb="slider"] > div > div > div { background: var(--brand) !important; }
div[data-baseweb="slider"] [role="slider"] { background: var(--handle) !important; border: 2px solid var(--brand) !important; width: 14px !important; height: 14px !important; box-shadow: none !important; }
.stSlider [data-testid="stTickBar"] { display: none !important; }

.stSelectbox > label { font-size: 13px !important; font-weight: 500 !important; color: var(--text-secondary) !important; }
.stSelectbox > div > div { background: var(--input-bg) !important; border: 1px solid var(--input-border) !important; border-radius: var(--r-sm) !important; color: var(--input-text) !important; font-size: 14px !important; }
.stSelectbox > div > div:focus-within { border-color: var(--input-focus) !important; box-shadow: 0 0 0 3px var(--brand-soft) !important; }
[data-baseweb="popover"], [data-baseweb="menu"] { background: var(--elevated) !important; border: 1px solid var(--border) !important; border-radius: var(--r-md) !important; }
[data-baseweb="option"] { background: transparent !important; color: var(--text-secondary) !important; font-size: 13px !important; }
[data-baseweb="option"]:hover, [aria-selected="true"][data-baseweb="option"] { background: var(--brand-soft) !important; color: var(--brand-hover) !important; }

.stRadio > label { font-size: 13px !important; font-weight: 500 !important; color: var(--text-secondary) !important; }
.stRadio [data-baseweb="radio"] { background: transparent !important; border: none !important; padding: 4px 8px !important; }
.stRadio [data-baseweb="radio"] div:first-child { border-color: var(--border) !important; }
.stRadio [data-baseweb="radio"] input:checked + div { background-color: var(--brand) !important; border-color: var(--brand) !important; }
.stRadio [data-baseweb="radio"] input:checked + div + div { color: var(--text-heading) !important; }
[data-baseweb="radio"]:focus, [data-baseweb="radio"]:active { outline: none !important; box-shadow: none !important; }

.stTabs [data-baseweb="tab-list"] { background: transparent !important; border-bottom: 1px solid var(--border) !important; gap: 0 !important; }
.stTabs [data-baseweb="tab"] { font-family: var(--font) !important; font-size: 12px !important; font-weight: 600 !important; letter-spacing: 0.06em !important; text-transform: uppercase !important; color: var(--text-muted) !important; padding: 10px 20px !important; background: transparent !important; border-bottom: 2px solid transparent !important; transition: color 0.15s !important; }
.stTabs [aria-selected="true"] { color: var(--brand-hover) !important; border-bottom: 2px solid var(--brand) !important; background: transparent !important; }
.stTabs [data-baseweb="tab"]:hover { color: var(--text-secondary) !important; }

.streamlit-expanderHeader { background: var(--surface) !important; border: 1px solid var(--border) !important; border-radius: var(--r-sm) !important; color: var(--text-secondary) !important; font-size: 12px !important; font-weight: 600 !important; letter-spacing: 0.06em !important; text-transform: uppercase !important; padding: 12px 16px !important; }
.streamlit-expanderHeader:hover { border-color: var(--brand) !important; color: var(--text-primary) !important; }
.streamlit-expanderContent { background: var(--surface) !important; border: 1px solid var(--border) !important; border-top: none !important; border-radius: 0 0 var(--r-sm) var(--r-sm) !important; padding: 20px !important; }

hr { border: none !important; border-top: 1px solid var(--border) !important; margin: 40px 0 !important; }
.stSpinner > div { border-top-color: var(--brand) !important; }
.stCaption p { font-size: 11px !important; color: var(--text-muted) !important; letter-spacing: 0.02em !important; }
.stAlert { background: var(--elevated) !important; border: 1px solid var(--border) !important; border-radius: var(--r-md) !important; font-size: 13px !important; }
[data-testid="stDataFrame"] { border-radius: var(--r-lg) !important; border: 1px solid var(--border) !important; overflow: hidden !important; }
.divider { height: 1px; background: var(--divider); margin: 32px 0; }
</style>
"""
