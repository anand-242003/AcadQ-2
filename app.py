import streamlit as st
import joblib
import numpy as np
import pandas as pd
import plotly.graph_objects as go
st.set_page_config(
    page_title="AcadIQ · Student Performance Predictor",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="collapsed"
)
st.markdown("""
<style>
:root {
    /* Backgrounds */
    --bg:        #0B0F14;
    --surface:   #111827;
    --elevated:  #1A2330;
    --border:    #1F2937;
    --divider:   #273244;
    /* Text */
    --text-primary:   #E5E7EB;
    --text-secondary: #9CA3AF;
    --text-muted:     #6B7280;
    --text-heading:   #FFFFFF;
    --text-disabled:  #4B5563;
    /* Brand */
    --brand:        #6366F1;
    --brand-hover:  #818CF8;
    --brand-active: #4F46E5;
    --brand-soft:   rgba(99,102,241,0.15);
    /* Status */
    --success:      #10B981;
    --warning:      #F59E0B;
    --danger:       #EF4444;
    --info:         #3B82F6;
    --success-bg:   rgba(16,185,129,0.15);
    --warning-bg:   rgba(245,158,11,0.15);
    --danger-bg:    rgba(239,68,68,0.15);
    --info-bg:      rgba(59,130,246,0.15);
    /* Inputs */
    --input-bg:     #0F172A;
    --input-border: #1F2937;
    --input-focus:  #6366F1;
    --input-text:   #E5E7EB;
    --placeholder:  #6B7280;
    /* Slider */
    --track:        #374151;
    --track-active: #6366F1;
    --handle:       #E5E7EB;
    --handle-border:#1F2937;
    /* Buttons */
    --btn-primary-bg:    #6366F1;
    --btn-primary-hover: #818CF8;
    --btn-primary-text:  #FFFFFF;
    --btn-secondary-bg:    #1F2937;
    --btn-secondary-hover: #374151;
    --btn-secondary-text:  #E5E7EB;
    --btn-ghost-hover:   rgba(99,102,241,0.12);
    /* Cards */
    --card-bg:     #111827;
    --card-border: #1F2937;
    --card-hover-border: #6366F1;
    --card-shadow: 0 0 0 1px rgba(255,255,255,0.02), 0 10px 30px rgba(0,0,0,0.35);
    /* Charts */
    --chart-1: #6366F1;
    --chart-2: #22C55E;
    --chart-3: #F59E0B;
    --chart-4: #EF4444;
    --chart-5: #06B6D4;
    --chart-grid: #1F2937;
    --chart-axis: #9CA3AF;
    /* Nav */
    --nav-bg:          #0B0F14;
    --nav-active-bg:   rgba(99,102,241,0.15);
    --nav-hover-bg:    rgba(255,255,255,0.04);
    --nav-text:        #9CA3AF;
    --nav-active-text: #FFFFFF;
    /* Spacing */
    --r-sm: 6px;
    --r-md: 8px;
    --r-lg: 12px;
    --r-xl: 16px;
    /* Font */
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

.navbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 48px;
    height: 60px;
    background: var(--nav-bg);
    border-bottom: 1px solid var(--border);
    position: sticky;
    top: 0;
    z-index: 100;
}
.nav-logo {
    display: flex;
    align-items: center;
    gap: 10px;
}
.nav-logo-mark {
    width: 32px; height: 32px;
    background: var(--brand);
    border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    font-size: 14px; font-weight: 800; color: #fff;
    letter-spacing: -0.02em;
}
.nav-logo-text {
    font-size: 15px; font-weight: 700;
    color: var(--text-heading); letter-spacing: -0.01em;
}
.nav-logo-sub { font-size: 11px; color: var(--text-muted); font-weight: 400; }
.nav-badge {
    font-size: 11px; font-weight: 600;
    color: var(--brand);
    background: var(--brand-soft);
    border: 1px solid rgba(99,102,241,0.3);
    border-radius: 20px;
    padding: 4px 12px;
    letter-spacing: 0.02em;
}
.nav-steps {
    display: flex; align-items: center; gap: 4px;
}
.nav-step {
    display: flex; align-items: center; gap: 8px;
    padding: 6px 14px;
    border-radius: 20px;
    font-size: 12px; font-weight: 600;
    color: var(--nav-text);
    letter-spacing: 0.02em;
}
.nav-step.active {
    background: var(--nav-active-bg);
    color: var(--nav-active-text);
}
.nav-step-num {
    width: 18px; height: 18px;
    border-radius: 50%;
    background: var(--border);
    display: flex; align-items: center; justify-content: center;
    font-size: 10px; font-weight: 700;
    color: var(--text-muted);
}
.nav-step.active .nav-step-num {
    background: var(--brand);
    color: #fff;
}
.nav-step.done .nav-step-num {
    background: var(--success);
    color: #fff;
}
.nav-step-sep { color: var(--border); font-size: 12px; }

.page-wrap {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 48px;
}

.hero {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    padding: 100px 48px 56px;
    position: relative;
    overflow: hidden;
}
.hero-bg-glow {
    position: absolute;
    top: 50%; left: 50%;
    transform: translate(-50%, -60%);
    width: 800px; height: 600px;
    background: radial-gradient(ellipse at center,
        rgba(99,102,241,0.12) 0%,
        rgba(99,102,241,0.04) 40%,
        transparent 70%);
    pointer-events: none;
}
.hero-bg-grid {
    position: absolute;
    inset: 0;
    background-image:
        linear-gradient(var(--divider) 1px, transparent 1px),
        linear-gradient(90deg, var(--divider) 1px, transparent 1px);
    background-size: 48px 48px;
    opacity: 0.3;
    mask-image: radial-gradient(ellipse at center, black 30%, transparent 80%);
    -webkit-mask-image: radial-gradient(ellipse at center, black 30%, transparent 80%);
}
.hero-badge {
    display: inline-flex; align-items: center; gap: 8px;
    background: var(--brand-soft);
    border: 1px solid rgba(99,102,241,0.3);
    border-radius: 20px;
    padding: 6px 16px;
    margin-bottom: 32px;
    font-size: 12px; font-weight: 600;
    color: var(--brand-hover);
    letter-spacing: 0.04em;
}
.hero-badge-dot {
    width: 6px; height: 6px;
    border-radius: 50%;
    background: var(--brand);
    animation: pulse 2s infinite;
}
@keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.6; transform: scale(0.85); }
}
.hero-title {
    font-size: 64px; font-weight: 800;
    color: var(--text-heading);
    letter-spacing: -0.04em; line-height: 1.08;
    margin-bottom: 24px;
    max-width: 760px;
}
.hero-title-accent { color: var(--brand-hover); }
.hero-desc {
    font-size: 18px; font-weight: 400;
    color: var(--text-secondary);
    line-height: 1.7; max-width: 540px;
    margin: 0 auto 48px;
}
.hero-cta-group {
    display: flex; align-items: center;
    justify-content: center; gap: 16px;
    margin-bottom: 56px;
}
.hero-stats-row {
    display: flex; align-items: center;
    gap: 48px; justify-content: center;
    padding: 40px 48px 64px;
    border-top: 1px solid var(--divider);
    margin-top: 40px;
    max-width: 1100px;
    margin-left: auto;
    margin-right: auto;
    width: 100%;
}
.hero-stat {
    text-align: center;
}
.hero-stat-num {
    font-family: var(--mono);
    font-size: 28px; font-weight: 700;
    color: var(--text-heading);
    letter-spacing: -0.03em;
}
.hero-stat-lbl {
    font-size: 12px; color: var(--text-muted);
    margin-top: 4px;
}
.hero-stat-sep {
    width: 1px; height: 40px;
    background: var(--border);
}
/* Feature cards */
.feature-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 16px;
    max-width: 1100px;
    margin: 80px auto 0;
    padding: 0 48px;
}
.feature-card {
    background: var(--surface);
    border: 1px solid var(--card-border);
    border-radius: var(--r-lg);
    padding: 28px;
    box-shadow: var(--card-shadow);
    transition: border-color 0.2s, transform 0.2s;
}
.feature-card:hover {
    border-color: var(--card-hover-border);
    transform: translateY(-2px);
}
.feature-icon {
    width: 40px; height: 40px;
    border-radius: var(--r-md);
    background: var(--brand-soft);
    display: flex; align-items: center; justify-content: center;
    margin-bottom: 16px;
    font-size: 18px;
}
.feature-title {
    font-size: 15px; font-weight: 700;
    color: var(--text-heading);
    margin-bottom: 8px;
}
.feature-desc {
    font-size: 13px; color: var(--text-secondary);
    line-height: 1.65;
}
/* How it works */
.how-section {
    max-width: 1100px;
    margin: 80px auto 0;
    padding: 0 48px;
}
.section-tag {
    font-size: 11px; font-weight: 700;
    letter-spacing: 0.12em; text-transform: uppercase;
    color: var(--brand);
    margin-bottom: 12px;
}
.section-title {
    font-size: 32px; font-weight: 800;
    color: var(--text-heading);
    letter-spacing: -0.02em;
    margin-bottom: 16px;
}
.section-desc {
    font-size: 15px; color: var(--text-secondary);
    line-height: 1.65; max-width: 520px;
    margin-bottom: 48px;
}
.steps-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 24px;
}
.step-card {
    background: var(--surface);
    border: 1px solid var(--card-border);
    border-radius: var(--r-lg);
    padding: 28px;
    box-shadow: var(--card-shadow);
    position: relative;
}
.step-num {
    font-family: var(--mono);
    font-size: 11px; font-weight: 700;
    color: var(--brand);
    background: var(--brand-soft);
    border-radius: 4px;
    padding: 3px 8px;
    display: inline-block;
    margin-bottom: 16px;
    letter-spacing: 0.06em;
}
.step-title {
    font-size: 15px; font-weight: 700;
    color: var(--text-heading); margin-bottom: 8px;
}
.step-desc {
    font-size: 13px; color: var(--text-secondary);
    line-height: 1.65;
}

.page-header {
    padding: 40px 48px 32px;
    border-bottom: 1px solid var(--border);
    margin-bottom: 40px;
}
.page-header-inner { max-width: 1200px; margin: 0 auto; }
.breadcrumb {
    display: flex; align-items: center; gap: 8px;
    font-size: 12px; color: var(--text-muted);
    margin-bottom: 10px;
}
.bc-sep { color: var(--border); }
.bc-cur { color: var(--text-secondary); font-weight: 500; }
.page-h1 {
    font-size: 26px; font-weight: 800;
    color: var(--text-heading); letter-spacing: -0.02em;
    margin-bottom: 8px;
}
.page-sub {
    font-size: 14px; color: var(--text-muted);
    line-height: 1.6; max-width: 560px;
}

.input-wrap {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 48px 80px;
}
.input-panel {
    background: var(--surface);
    border: 1px solid var(--card-border);
    border-radius: var(--r-xl);
    padding: 28px 24px;
    box-shadow: var(--card-shadow);
    height: 100%;
}
.panel-section-title {
    font-size: 11px; font-weight: 700;
    letter-spacing: 0.12em; text-transform: uppercase;
    color: var(--text-muted);
    padding-bottom: 10px;
    border-bottom: 1px solid var(--divider);
    margin-bottom: 20px;
}
.panel-section-title + .panel-section-title,
.sub-section {
    margin-top: 24px;
}
/* Live summary cards */
.summary-card {
    background: var(--elevated);
    border: 1px solid var(--card-border);
    border-radius: var(--r-md);
    padding: 13px 16px;
    margin-bottom: 8px;
    transition: border-color 0.15s;
}
.summary-card:hover { border-color: var(--brand); }
.summary-card.success { border-left: 3px solid var(--success); }
.summary-card.warning { border-left: 3px solid var(--warning); }
.summary-card.danger  { border-left: 3px solid var(--danger); }
.sc-label {
    font-size: 10px; font-weight: 700;
    letter-spacing: 0.1em; text-transform: uppercase;
    color: var(--text-muted); margin-bottom: 4px;
}
.sc-value {
    font-family: var(--mono);
    font-size: 17px; font-weight: 700;
    color: var(--text-primary); letter-spacing: -0.02em;
}
.sc-value.brand  { color: var(--brand-hover); }
.sc-value.success{ color: var(--success); }
.sc-value.warning{ color: var(--warning); }
.sc-value.danger { color: var(--danger); }
.sc-sub {
    font-size: 11px; color: var(--text-muted); margin-top: 3px;
}

.results-wrap {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 48px 80px;
}
/* Score hero card */
.score-card {
    background: var(--surface);
    border: 1px solid var(--card-border);
    border-radius: var(--r-xl);
    padding: 32px;
    box-shadow: var(--card-shadow);
    position: relative;
    overflow: hidden;
    margin-bottom: 0;
}
.score-card::after {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, var(--brand), var(--brand-hover), transparent);
}
.score-eyebrow {
    font-size: 10px; font-weight: 700;
    letter-spacing: 0.12em; text-transform: uppercase;
    color: var(--text-muted); margin-bottom: 14px;
}
.score-number {
    font-family: var(--mono);
    font-size: 80px; font-weight: 800;
    letter-spacing: -0.05em; line-height: 1;
}
.score-denom {
    font-family: var(--mono);
    font-size: 18px; font-weight: 500;
    color: var(--text-muted); vertical-align: super;
    margin-left: 4px;
}
.score-grade-badge {
    font-family: var(--mono);
    font-size: 20px; font-weight: 800;
    padding: 6px 18px;
    border-radius: var(--r-sm);
    display: inline-block;
    margin-left: 12px;
    vertical-align: middle;
}
.prog-track {
    background: var(--elevated);
    border-radius: 99px; height: 4px;
    margin: 20px 0; overflow: hidden;
}
.prog-fill {
    height: 100%; border-radius: 99px;
    transition: width 0.8s cubic-bezier(0.4,0,0.2,1);
}
.result-chip {
    display: inline-flex; align-items: center; gap: 6px;
    font-size: 11px; font-weight: 700;
    letter-spacing: 0.08em; text-transform: uppercase;
    padding: 5px 14px; border-radius: 4px;
}
.result-chip.pass {
    background: var(--success-bg);
    color: var(--success);
    border: 1px solid rgba(16,185,129,0.3);
}
.result-chip.fail {
    background: var(--danger-bg);
    color: var(--danger);
    border: 1px solid rgba(239,68,68,0.3);
}
.result-chip::before {
    content: '';
    width: 5px; height: 5px;
    border-radius: 50%;
    background: currentColor;
}
.result-label {
    font-size: 14px; color: var(--text-secondary);
    font-weight: 500; margin-left: 8px;
}
/* Metric cards */
[data-testid="stMetric"] {
    background: var(--surface) !important;
    border: 1px solid var(--card-border) !important;
    border-radius: var(--r-lg) !important;
    padding: 20px !important;
    box-shadow: var(--card-shadow) !important;
    transition: border-color 0.15s !important;
}
[data-testid="stMetric"]:hover {
    border-color: var(--brand) !important;
}
[data-testid="stMetricLabel"] p {
    font-size: 10px !important; font-weight: 700 !important;
    letter-spacing: 0.1em !important; text-transform: uppercase !important;
    color: var(--text-muted) !important;
}
[data-testid="stMetricValue"] {
    font-family: var(--mono) !important;
    font-size: 22px !important; font-weight: 700 !important;
    color: var(--text-heading) !important;
    letter-spacing: -0.02em !important;
}
[data-testid="stMetricDelta"] { font-size: 11px !important; }
/* Learner classification card */
.learner-card {
    background: var(--brand-soft);
    border: 1px solid rgba(99,102,241,0.3);
    border-radius: var(--r-lg);
    padding: 20px;
    margin-bottom: 16px;
}
.learner-eyebrow {
    font-size: 10px; font-weight: 700;
    letter-spacing: 0.12em; text-transform: uppercase;
    color: var(--brand-hover); margin-bottom: 8px;
}
.learner-name {
    font-size: 18px; font-weight: 700;
    color: var(--text-heading);
    letter-spacing: -0.01em; margin-bottom: 8px;
}
.learner-meta {
    font-size: 12px; color: var(--text-muted);
    display: flex; gap: 12px; flex-wrap: wrap;
}
.learner-meta-item { display: flex; align-items: center; gap: 6px; }
.learner-meta-dot {
    width: 4px; height: 4px;
    border-radius: 50%; background: var(--text-disabled);
}
/* Tip cards */
.tip-card {
    background: var(--surface);
    border: 1px solid var(--card-border);
    border-radius: var(--r-md);
    padding: 14px 16px;
    margin-bottom: 8px;
    display: flex; gap: 12px;
    transition: border-color 0.15s;
}
.tip-card:hover { border-color: var(--brand); }
.tip-indicator {
    width: 3px; border-radius: 99px;
    background: var(--brand);
    flex-shrink: 0; min-height: 36px;
}
.tip-cat {
    font-size: 10px; font-weight: 700;
    letter-spacing: 0.1em; text-transform: uppercase;
    color: var(--brand-hover); margin-bottom: 5px;
}
.tip-txt {
    font-size: 13px; color: var(--text-secondary);
    line-height: 1.6;
}
/* Chart section */
.chart-panel {
    background: var(--surface);
    border: 1px solid var(--card-border);
    border-radius: var(--r-xl);
    padding: 24px;
    box-shadow: var(--card-shadow);
}
/* Section label */
.section-lbl {
    font-size: 11px; font-weight: 700;
    letter-spacing: 0.1em; text-transform: uppercase;
    color: var(--text-muted);
    padding-bottom: 10px;
    border-bottom: 1px solid var(--divider);
    margin-bottom: 20px;
}

/* Buttons */
.stButton > button[kind="primary"] {
    background: var(--btn-primary-bg) !important;
    color: var(--btn-primary-text) !important;
    border: none !important;
    border-radius: var(--r-sm) !important;
    font-family: var(--font) !important;
    font-size: 13px !important; font-weight: 700 !important;
    padding: 14px 32px !important;
    transition: all 0.15s ease !important;
    box-shadow: 0 0 20px rgba(99,102,241,0.25) !important;
}
.stButton > button[kind="primary"]:hover {
    background: var(--btn-primary-hover) !important;
    box-shadow: 0 0 32px rgba(99,102,241,0.4) !important;
    transform: translateY(-1px) !important;
}
.stButton > button[kind="primary"]:active {
    background: var(--brand-active) !important;
    transform: translateY(0) !important;
}
.stButton > button:not([kind="primary"]) {
    background: var(--btn-secondary-bg) !important;
    color: var(--btn-secondary-text) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--r-sm) !important;
    font-family: var(--font) !important;
    font-size: 13px !important; font-weight: 600 !important;
    padding: 12px 24px !important;
    transition: all 0.15s ease !important;
    box-shadow: none !important;
}
.stButton > button:not([kind="primary"]):hover {
    background: var(--btn-secondary-hover) !important;
    border-color: var(--brand) !important;
    color: var(--text-heading) !important;
    transform: translateY(-1px) !important;
}
/* Sliders */
.stSlider > label {
    font-size: 13px !important; font-weight: 500 !important;
    color: var(--text-secondary) !important;
}
div[data-baseweb="slider"] > div > div {
    background: var(--track) !important;
}
div[data-baseweb="slider"] > div > div > div {
    background: var(--brand) !important;
}
div[data-baseweb="slider"] [role="slider"] {
    background: var(--handle) !important;
    border: 2px solid var(--brand) !important;
    width: 14px !important; height: 14px !important;
    box-shadow: none !important;
}
.stSlider [data-testid="stTickBar"] { display: none !important; }
/* Selectbox */
.stSelectbox > label {
    font-size: 13px !important; font-weight: 500 !important;
    color: var(--text-secondary) !important;
}
.stSelectbox > div > div {
    background: var(--input-bg) !important;
    border: 1px solid var(--input-border) !important;
    border-radius: var(--r-sm) !important;
    color: var(--input-text) !important;
    font-size: 14px !important;
}
.stSelectbox > div > div:focus-within {
    border-color: var(--input-focus) !important;
    box-shadow: 0 0 0 3px var(--brand-soft) !important;
}
[data-baseweb="popover"], [data-baseweb="menu"] {
    background: var(--elevated) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--r-md) !important;
}
[data-baseweb="option"] {
    background: transparent !important;
    color: var(--text-secondary) !important;
    font-size: 13px !important;
}
[data-baseweb="option"]:hover,
[aria-selected="true"][data-baseweb="option"] {
    background: var(--brand-soft) !important;
    color: var(--brand-hover) !important;
}
/* Radio */
.stRadio > label {
    font-size: 13px !important; font-weight: 500 !important;
    color: var(--text-secondary) !important;
}
.stRadio [data-baseweb="radio"] {
    background: transparent !important;
    border: none !important;
    padding: 4px 8px !important;
}
.stRadio [data-baseweb="radio"] div:first-child {
    border-color: var(--border) !important;
}
.stRadio [data-baseweb="radio"] input:checked + div {
    background-color: var(--brand) !important;
    border-color: var(--brand) !important;
}
.stRadio [data-baseweb="radio"] input:checked + div + div {
    color: var(--text-heading) !important;
}
/* Focus & Hover Overrides to prevent "red things" */
[data-baseweb="radio"]:focus, [data-baseweb="radio"]:active {
    outline: none !important;
    box-shadow: none !important;
}
/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: transparent !important;
    border-bottom: 1px solid var(--border) !important;
    gap: 0 !important;
}
.stTabs [data-baseweb="tab"] {
    font-family: var(--font) !important;
    font-size: 12px !important; font-weight: 600 !important;
    letter-spacing: 0.06em !important; text-transform: uppercase !important;
    color: var(--text-muted) !important;
    padding: 10px 20px !important;
    background: transparent !important;
    border-bottom: 2px solid transparent !important;
    transition: color 0.15s !important;
}
.stTabs [aria-selected="true"] {
    color: var(--brand-hover) !important;
    border-bottom: 2px solid var(--brand) !important;
    background: transparent !important;
}
.stTabs [data-baseweb="tab"]:hover { color: var(--text-secondary) !important; }
/* Expander */
.streamlit-expanderHeader {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--r-sm) !important;
    color: var(--text-secondary) !important;
    font-size: 12px !important; font-weight: 600 !important;
    letter-spacing: 0.06em !important; text-transform: uppercase !important;
    padding: 12px 16px !important;
}
.streamlit-expanderHeader:hover {
    border-color: var(--brand) !important;
    color: var(--text-primary) !important;
}
.streamlit-expanderContent {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-top: none !important;
    border-radius: 0 0 var(--r-sm) var(--r-sm) !important;
    padding: 20px !important;
}
/* Misc */
hr {
    border: none !important;
    border-top: 1px solid var(--border) !important;
    margin: 40px 0 !important;
}
.stSpinner > div { border-top-color: var(--brand) !important; }
.stCaption p {
    font-size: 11px !important;
    color: var(--text-muted) !important;
    letter-spacing: 0.02em !important;
}
.stAlert {
    background: var(--elevated) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--r-md) !important;
    font-size: 13px !important;
}
[data-testid="stDataFrame"] {
    border-radius: var(--r-lg) !important;
    border: 1px solid var(--border) !important;
    overflow: hidden !important;
}
/* Divider */
.divider {
    height: 1px;
    background: var(--divider);
    margin: 32px 0;
}
</style>
""", unsafe_allow_html=True)
@st.cache_resource
def load_all_models():
    m = {}
    try:
        m['classifier']        = joblib.load("Notebook/student_ml_app/classification_model.pkl")
        m['regressor']         = joblib.load("Notebook/student_ml_app/regression_model.pkl")
        m['kmeans']            = joblib.load("Notebook/student_ml_app/clustering_model.pkl")
        m['scaler']            = joblib.load("Notebook/student_ml_app/scaler.pkl")
        m['feature_columns']   = joblib.load("Notebook/student_ml_app/feature_columns.pkl")
        m['cluster_label_map'] = joblib.load("Notebook/student_ml_app/cluster_label_map.pkl")
        m['loaded']            = True
    except FileNotFoundError as e:
        m['loaded'] = False; m['error'] = str(e)
    except Exception as e:
        m['loaded'] = False; m['error'] = f"Unexpected error: {e}"
    return m
models = load_all_models()
if not models['loaded']:
    st.error(f"""
**Models not found** — `{models.get('error')}`
Place these files in the same folder as app.py:
`classification_model.pkl` · `regression_model.pkl` · `clustering_model.pkl`
`scaler.pkl` · `feature_columns.pkl` · `cluster_label_map.pkl`
    """)
    st.stop()
for key, default in [('page', 'landing'), ('results', {}), ('raw_input', {}), ('validation_warns', [])]:
    if key not in st.session_state:
        st.session_state[key] = default
def get_score_color(score: float) -> str:
    if score >= 60: return "#6366F1"
    if score >= 40: return "#F59E0B"
    return "#EF4444"
def get_score_grade(score: float) -> str:
    if score >= 75: return "A"
    if score >= 60: return "B"
    if score >= 45: return "C"
    if score >= 30: return "D"
    return "F"
def get_result_label(score: float) -> str:
    if score >= 75: return "Excellent"
    if score >= 60: return "Good"
    if score >= 45: return "Average"
    if score >= 30: return "Below Average"
    return "Critical"
def strip_emoji(text: str) -> str:
    import re
    return re.sub(r'[\U00010000-\U0010ffff\u2600-\u26FF\u2700-\u27BF\U0001F300-\U0001F9FF]+\s*', '', text).strip()
def validate_inputs(raw: dict) -> list:
    errors = []
    total_study = raw['study_hours'] + raw['self_study_hours'] + raw['online_classes_hours']
    if total_study > 20:
        errors.append(f"Total study time ({total_study:.1f} hrs/day) seems unrealistically high.")
    min_screen = raw['social_media_hours'] + raw['gaming_hours'] + raw['online_classes_hours']
    if raw['screen_time_hours'] < min_screen:
        errors.append(f"Screen time ({raw['screen_time_hours']} hrs) is less than sub-components combined ({min_screen:.1f} hrs).")
    total_day = (raw['study_hours'] + raw['self_study_hours'] + raw['online_classes_hours'] +
                 raw['social_media_hours'] + raw['gaming_hours'] +
                 raw['sleep_hours'] + raw['exercise_minutes'] / 60)
    if total_day > 24:
        errors.append(f"Combined hours ({total_day:.1f}) exceed 24 hours in a day.")
    if raw['sleep_hours'] < 4:
        errors.append("Sleep below 4 hours is extremely low.")
    if raw['burnout_level'] > 80 and raw['mental_health_score'] >= 9:
        errors.append("Very high burnout with very high mental health score are contradictory.")
    if raw['productivity_score'] > 85 and raw['study_hours'] < 1:
        errors.append("High productivity with less than 1 hour study seems inconsistent.")
    if raw['caffeine_intake_mg'] >= 580:
        errors.append("Caffeine intake at or above 580 mg/day exceeds safe daily limits.")
    return errors
def preprocess_input(raw: dict):
    df = pd.DataFrame([raw])
    df['gender']            = df['gender'].map({'Male': 1, 'Female': 0, 'Other': 2})
    df['academic_level']    = df['academic_level'].map({'High School': 0, 'Undergraduate': 1})
    df['internet_quality']  = df['internet_quality'].map({'Good': 1, 'Poor': 0})
    df['part_time_job']     = 1 if raw['part_time_job']     == 'Yes' else 0
    df['upcoming_deadline'] = 1 if raw['upcoming_deadline'] == 'Yes' else 0
    df['total_active_hours']      = df['study_hours'] + df['self_study_hours'] + df['online_classes_hours']
    df['total_distraction_hours'] = df['social_media_hours'] + df['gaming_hours']
    df['study_distraction_ratio'] = df['study_hours'] / df['total_distraction_hours'].replace(0, 0.1)
    df['healthy_sleep']           = df['sleep_hours'].apply(lambda x: 1 if 7 <= x <= 9 else 0)
    df['wellness_score']          = (df['mental_health_score'] * 0.4 + df['sleep_hours'] * 0.3 + (df['exercise_minutes'] / 60) * 0.3)
    df['stress_index']            = (df['burnout_level'] * 0.5 + df['screen_time_hours'] * 0.3 + (10 - df['sleep_hours']) * 0.2)
    cols = models['feature_columns']
    for c in cols:
        if c not in df.columns: df[c] = 0
    df = df[cols]
    scaled = models['scaler'].transform(df)
    return pd.DataFrame(scaled, columns=cols), df
def run_predictions(raw: dict) -> dict:
    scaled_df, _ = preprocess_input(raw)
    pred_class   = int(models['classifier'].predict(scaled_df)[0])
    proba        = models['classifier'].predict_proba(scaled_df)[0]
    pred_score   = round(float(np.clip(models['regressor'].predict(scaled_df)[0], 0, 100)), 2)
    pred_cluster = int(models['kmeans'].predict(scaled_df)[0])
    ltype        = models['cluster_label_map'].get(pred_cluster, "Unknown")
    return {
        "pred_score"             : pred_score,
        "pred_class"             : pred_class,
        "pass_probability"       : round(float(proba[1]) * 100, 1),
        "fail_probability"       : round(float(proba[0]) * 100, 1),
        "pred_learner_type"      : ltype,
        "pred_cluster"           : pred_cluster,
        "study_hours"            : raw['study_hours'],
        "sleep_hours"            : raw['sleep_hours'],
        "total_distraction_hours": raw['social_media_hours'] + raw['gaming_hours'],
        "mental_health_score"    : raw['mental_health_score'],
        "burnout_level"          : raw['burnout_level'],
        "exercise_minutes"       : raw['exercise_minutes'],
        "internet_quality"       : raw['internet_quality'],
        "productivity_score"     : raw['productivity_score'],
        "social_media_hours"     : raw['social_media_hours'],
        "gaming_hours"           : raw['gaming_hours'],
        "screen_time_hours"      : raw['screen_time_hours'],
        "caffeine_intake_mg"     : raw['caffeine_intake_mg'],
        "focus_index"            : raw['focus_index'],
    }
def generate_recommendations(results: dict) -> list:
    tips  = []
    score = results['pred_score']
    if score < 20:
        tips.append(("Critical alert",  "Predicted score is very low. Speak with your academic advisor as soon as possible."))
        tips.append(("Study approach",  "Review foundational concepts before attempting advanced material."))
    elif score < 40:
        tips.append(("At risk",         "You are at risk of failing. Increase daily study hours significantly."))
        tips.append(("Planning",        "Build a structured weekly timetable and commit to it every day."))
    elif score < 60:
        tips.append(("Room to improve", "You are passing but there is clear room for improvement."))
        tips.append(("Study strategy",  "Practice with past exam papers and focus on your weakest topics."))
    else:
        tips.append(("Performing well", "You are on track. Stay consistent and maintain your current habits."))
        tips.append(("Next level",      "Challenge yourself with harder material to push your score even higher."))
    if results['study_hours'] < 2:
        tips.append(("Study time",      "Less than 2 hours of study per day. Aim for at least 4 to 5 hours for meaningful progress."))
    elif results['study_hours'] < 4:
        tips.append(("Study time",      "Consider increasing to 5 to 6 study hours per day for better retention."))
    if results['sleep_hours'] < 6:
        tips.append(("Sleep",           "Under 6 hours of sleep significantly impairs memory and focus. Target 7 to 8 hours per night."))
    elif results['sleep_hours'] > 9:
        tips.append(("Sleep",           "Oversleeping can reduce motivation. 7 to 8 hours is the optimal range."))
    if results['total_distraction_hours'] > 4:
        tips.append(("Distractions",    "More than 4 hours on social media and gaming per day is reducing your study effectiveness."))
    elif results['total_distraction_hours'] > 2:
        tips.append(("Distractions",    "Aim to keep social media and gaming under 2 hours per day to free up study time."))
    if results['mental_health_score'] <= 3:
        tips.append(("Mental health",   "Mental health score is low. Consider speaking with a counselor or a trusted person."))
    elif results['mental_health_score'] <= 6:
        tips.append(("Mental health",   "Try the Pomodoro method — 25 minutes of focused study followed by a 5-minute break."))
    if results['burnout_level'] > 70:
        tips.append(("Burnout",         "Burnout level is very high. Take a full rest day and avoid cramming sessions."))
    elif results['burnout_level'] > 50:
        tips.append(("Burnout",         "Moderate burnout detected. Space out study sessions and include planned rest."))
    if results['exercise_minutes'] < 20:
        tips.append(("Exercise",        "Less than 20 minutes of activity per day. A 30-minute walk improves focus and retention."))
    if results['internet_quality'] == 'Poor':
        tips.append(("Connectivity",    "Poor internet detected. Download study materials in advance for offline access."))
    learner = strip_emoji(results['pred_learner_type'])
    if 'Struggling' in learner:
        tips.append(("Learner profile", "Join a study group or work with a tutor. Peer learning significantly accelerates understanding."))
    elif 'Average' in learner:
        tips.append(("Learner profile", "Set small measurable daily goals and review your progress at the end of each week."))
    elif 'Developing' in learner:
        tips.append(("Learner profile", "You are on the right trajectory. Consistency is your biggest asset right now."))
    elif 'High Achiever' in learner:
        tips.append(("Learner profile", "Consider mentoring peers. Teaching material is one of the most effective ways to master it."))
    return tips
CHART_BASE = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(family='-apple-system, BlinkMacSystemFont, "Segoe UI", system-ui, sans-serif',
              color='#9CA3AF', size=11),
    margin=dict(t=20, b=16, l=8, r=16),
    height=340,
)
C = {
    "c1": "#6366F1", "c2": "#22C55E", "c3": "#F59E0B",
    "c4": "#EF4444", "c5": "#06B6D4",
    "grid": "#1F2937", "axis": "#9CA3AF",
}
def render_navbar(active_page: str):
    pages = [("landing", "Overview"), ("input", "Input Data"), ("results", "Results")]
    steps_html = ""
    done = True
    for pg, label in pages:
        is_active = pg == active_page
        is_done   = done and pg != active_page
        cls = "active" if is_active else ("done" if is_done else "")
        idx = pages.index((pg, label)) + 1
        if is_active: done = False
        steps_html += f"""
        <div class="nav-step {cls}">
            <div class="nav-step-num">{'✓' if is_done else idx}</div>
            {label}
        </div>"""
        if pg != "results":
            steps_html += '<span class="nav-step-sep">›</span>'
    badge_map = {"landing": "Home", "input": "Step 1 of 2", "results": "Step 2 of 2"}
    st.markdown(f"""
    <div class="navbar">
        <div class="nav-logo">
            <div class="nav-logo-mark">A</div>
            <div>
                <div class="nav-logo-text">AcadIQ</div>
                <div class="nav-logo-sub">Performance Analytics</div>
            </div>
        </div>
        <div class="nav-steps">{steps_html}</div>
        <div class="nav-badge">{badge_map.get(active_page, '')}</div>
    </div>
    """, unsafe_allow_html=True)
def show_landing_page():
    render_navbar("landing")
    with st.container():
        st.caption("ML-Powered Academic Analytics")
        st.title("Predict Your Academic Performance")
        st.write("Enter your study habits, lifestyle data, and wellness metrics. Get an instant predicted exam score, pass/fail classification, and personalized recommendations to improve.")
        
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("Get Started →", type="primary", use_container_width=True, key="hero_cta"):
                st.session_state['page'] = 'input'
                st.rerun()
    
    st.divider()
    
    with st.container():
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("ML Models", "3")
        m2.metric("Input Features", "20+")
        m3.metric("Output Predictions", "3")
        m4.metric("Recommendations", "10+")
    
    st.divider()
    
    with st.container():
        st.header("Core Features")
        f1, f2, f3 = st.columns(3)
        with f1:
            st.subheader("Score Prediction")
            st.write("A regression model estimates your predicted exam score out of 100, calibrated on student performance data across 20+ behavioral features.")
        with f2:
            st.subheader("Pass / Fail Classification")
            st.write("A binary classifier predicts whether you are on track to pass or at risk of failing, with a confidence probability breakdown for both outcomes.")
        with f3:
            st.subheader("Learner Profiling")
            st.write("A clustering model assigns you to a learner archetype — from Struggling to High Achiever — and generates targeted improvement recommendations.")
            
    st.divider()
    
    with st.container():
        st.caption("How It Works")
        st.header("Three steps to your report")
        st.write("No account needed. Fill in your data, run the models, and get your full performance analysis in seconds.")
        
        s1, s2, s3 = st.columns(3)
        with s1:
            st.subheader("01. Enter Your Data")
            st.write("Provide details about your study schedule, sleep, screen time, mental health, and wellbeing across 20 input fields.")
        with s2:
            st.subheader("02. Run the Models")
            st.write("Three ML models process your inputs — a regressor, classifier, and clustering model — to produce a complete performance profile.")
        with s3:
            st.subheader("03. Review & Improve")
            st.write("Explore your predicted score, classification, learner type, interactive charts, and a personalized list of actionable recommendations.")
def show_input_page():
    render_navbar("input")
    with st.container():
        st.caption("AcadIQ › Input Data")
        st.header("Enter Your Information")
        st.write("Fill in all fields accurately for the best prediction. The live summary on the right updates as you type.")
        
    col1, col2, col3 = st.columns(3, gap="large")
    with col1:
        st.subheader("Personal Information")
        age               = st.slider("Age", 16, 25, 20)
        gender            = st.selectbox("Gender", ["Male", "Female", "Other"])
        academic_level    = st.selectbox("Academic Level", ["High School", "Undergraduate"])
        part_time_job     = st.radio("Part-time Job", ["No", "Yes"], horizontal=True)
        upcoming_deadline = st.radio("Upcoming Deadline", ["No", "Yes"], horizontal=True)
        internet_quality  = st.selectbox("Internet Quality", ["Good", "Poor"])
        
        st.divider()
        st.subheader("Lifestyle")
        sleep_hours        = st.slider("Sleep Hours / Night", 3.0, 12.0, 7.0, 0.5)
        exercise_minutes   = st.slider("Exercise (min / day)", 0, 180, 30, 5)
        caffeine_intake_mg = st.slider("Caffeine Intake (mg / day)", 0, 600, 150, 10)
        
    with col2:
        st.subheader("Study Habits")
        study_hours          = st.slider("Study Hours / Day", 0.0, 12.0, 4.0, 0.5)
        self_study_hours     = st.slider("Self-Study Hours / Day", 0.0, 8.0, 1.5, 0.5)
        online_classes_hours = st.slider("Online Class Hours / Day", 0.0, 8.0, 1.5, 0.5)
        
        st.divider()
        st.subheader("Screen & Distractions")
        social_media_hours = st.slider("Social Media Hours / Day", 0.0, 10.0, 2.0, 0.5)
        gaming_hours       = st.slider("Gaming Hours / Day", 0.0, 10.0, 1.0, 0.5)
        screen_time_hours  = st.slider("Total Screen Time / Day", 0.0, 16.0, 6.0, 0.5)
        
    with col3:
        st.subheader("Wellbeing & Scores")
        mental_health_score = st.slider("Mental Health Score (1–10)", 1, 10, 7, 1)
        focus_index         = st.slider("Focus Index (0–100)", 0.0, 100.0, 50.0, 1.0)
        burnout_level       = st.slider("Burnout Level (0–100)", 0.0, 100.0, 40.0, 1.0)
        productivity_score  = st.slider("Productivity Score (0–100)", 0.0, 100.0, 50.0, 1.0)
        
        st.divider()
        st.subheader("Live Summary")
        total_study = study_hours + self_study_hours + online_classes_hours
        total_dist  = social_media_hours + gaming_hours
        sleep_ok    = 7 <= sleep_hours <= 9
        mh_label    = "Good" if mental_health_score >= 7 else "Moderate" if mental_health_score >= 4 else "Low"
        
        sc_col1, sc_col2 = st.columns(2)
        sc_col1.metric("Total Study", f"{total_study:.1f}h")
        sc_col2.metric("Distractions", f"{total_dist:.1f}h")
        
        sc_col3, sc_col4 = st.columns(2)
        sc_col3.metric("Sleep", "Healthy" if sleep_ok else "Poor")
        sc_col4.metric("Mental Health", mh_label)
              
    raw_input = {
        "age": age, "gender": gender, "academic_level": academic_level,
        "study_hours": study_hours, "self_study_hours": self_study_hours,
        "online_classes_hours": online_classes_hours,
        "social_media_hours": social_media_hours, "gaming_hours": gaming_hours,
        "sleep_hours": sleep_hours, "screen_time_hours": screen_time_hours,
        "exercise_minutes": exercise_minutes, "caffeine_intake_mg": caffeine_intake_mg,
        "part_time_job": part_time_job, "upcoming_deadline": upcoming_deadline,
        "internet_quality": internet_quality, "mental_health_score": mental_health_score,
        "focus_index": focus_index, "burnout_level": burnout_level,
        "productivity_score": productivity_score,
    }
    st.markdown('<div class="input-wrap">', unsafe_allow_html=True)
    warnings = validate_inputs(raw_input)
    if warnings:
        with st.expander(f"{len(warnings)} input warning{'s' if len(warnings) > 1 else ''} — click to review"):
            for w in warnings:
                st.warning(w)
            st.caption("You can still proceed. Correcting these will improve prediction accuracy.")
    _, btn_col, _ = st.columns([2, 2, 2])
    with btn_col:
        if st.button("Run Prediction →", type="primary", use_container_width=True):
            with st.spinner("Running models..."):
                try:
                    results = run_predictions(raw_input)
                    st.session_state['results']          = results
                    st.session_state['raw_input']        = raw_input
                    st.session_state['validation_warns'] = warnings
                    st.session_state['page']             = 'results'
                    st.rerun()
                except ValueError as ve:
                    st.error(f"Data error: {ve}")
                except Exception as e:
                    st.error(f"Prediction failed: `{e}`")
    st.markdown('</div>', unsafe_allow_html=True)
def show_results_page():
    results = st.session_state.get('results', {})
    raw     = st.session_state.get('raw_input', {})
    warn_list = st.session_state.get('validation_warns', [])
    if not results:
        st.warning("No results found. Please complete the input step first.")
        if st.button("Go to Input"):
            st.session_state['page'] = 'input'; st.rerun()
        return
    score    = results['pred_score']
    passed   = results['pred_class'] == 1
    grade    = get_score_grade(score)
    result_l = get_result_label(score)
    s_color  = get_score_color(score)
    ltype    = strip_emoji(results['pred_learner_type'])
    render_navbar("results")
    with st.container():
        st.caption("AcadIQ › Input Data › Results")
        st.header("Your Performance Report")
        st.write("Based on your inputs, here is the full prediction analysis from all three models.")
    
    if warn_list:
        with st.expander(f"{len(warn_list)} input warning{'s' if len(warn_list) > 1 else ''} — accuracy may be reduced"):
            for w in warn_list: st.warning(w)
            
    hero_l, hero_r = st.columns([1, 1], gap="large")
    with hero_l:
        st.subheader("Predicted Exam Score")
        st.metric("Score", f"{score} / 100", delta=grade)
        st.progress(score / 100)
        if passed:
            st.success(f"Pass — {result_l}")
        else:
            st.error(f"Fail — {result_l}")
            
    with hero_r:
        m1, m2 = st.columns(2)
        m3, m4 = st.columns(2)
        m1.metric("Pass Probability",  f"{results['pass_probability']}%")
        m2.metric("Fail Probability",  f"{results['fail_probability']}%")
        m3.metric("Learner Type",      ltype)
        m4.metric("Cluster Group",     f"Group {results['pred_cluster']}")
        
    st.divider()
    chart_col, rec_col = st.columns([11, 8], gap="large")
    with chart_col:
        st.markdown('<div class="chart-panel">', unsafe_allow_html=True)
        st.markdown('<div class="section-lbl">Performance Breakdown</div>', unsafe_allow_html=True)
        tab1, tab2, tab3 = st.tabs(["Radar Profile", "Habit Comparison", "Time Allocation"])
        with tab1:
            try:
                cats = ["Study hrs", "Sleep hrs", "Mental health",
                        "Focus index", "Productivity", "Exercise"]
                vals = [
                    min(results['study_hours'] / 12 * 10, 10),
                    min(results['sleep_hours'] / 12 * 10, 10),
                    float(results['mental_health_score']),
                    results['focus_index'] / 10,
                    results['productivity_score'] / 10,
                    min(results['exercise_minutes'] / 180 * 10, 10),
                ]
                cl = cats + [cats[0]]; vl = vals + [vals[0]]
                fig = go.Figure()
                fig.add_trace(go.Scatterpolar(
                    r=vl, theta=cl, fill='toself', name='Your profile',
                    line=dict(color=C['c1'], width=2.5),
                    fillcolor='rgba(99,102,241,0.12)',
                ))
                fig.add_trace(go.Scatterpolar(
                    r=[5]*7, theta=cl, fill=None, name='Average student',
                    line=dict(color='#374151', dash='dot', width=1.5),
                ))
                fig.update_layout(
                    **CHART_BASE,
                    polar=dict(
                        bgcolor='rgba(0,0,0,0)',
                        radialaxis=dict(visible=True, range=[0,10],
                                        tickfont=dict(size=9, color='#374151'),
                                        gridcolor=C['grid'], linecolor=C['grid']),
                        angularaxis=dict(tickfont=dict(size=10, color=C['axis']),
                                         gridcolor=C['grid'], linecolor=C['grid']),
                    ),
                    legend=dict(orientation='h', y=-0.12, font=dict(size=10, color='#6B7280')),
                )
                st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.error(f"Chart error: {e}")
        with tab2:
            try:
                labels = ["Study hrs", "Sleep hrs", "Social media", "Gaming",
                          "Exercise ÷10", "Mental health", "Burnout ÷10", "Productivity ÷10"]
                values = [
                    results['study_hours'], results['sleep_hours'],
                    results['social_media_hours'], results['gaming_hours'],
                    results['exercise_minutes'] / 10, float(results['mental_health_score']),
                    results['burnout_level'] / 10, results['productivity_score'] / 10,
                ]
                bar_colors = [C['c1'], C['c2'], C['c3'], C['c3'], C['c5'], C['c1'], C['c4'], C['c5']]
                fig = go.Figure(go.Bar(
                    x=values, y=labels, orientation='h',
                    marker=dict(color=bar_colors, line_width=0),
                    text=[f"{v:.1f}" for v in values],
                    textposition='outside',
                    textfont=dict(size=10, color='#6B7280'),
                ))
                fig.update_layout(
                    **CHART_BASE,
                    xaxis=dict(showgrid=False, showticklabels=False, showline=False, zeroline=False),
                    yaxis=dict(showgrid=False, tickfont=dict(size=11, color=C['axis'])),
                    bargap=0.38,
                )
                st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.error(f"Chart error: {e}")
        with tab3:
            try:
                study_total  = (raw.get('study_hours', 0) + raw.get('self_study_hours', 0) + raw.get('online_classes_hours', 0))
                exercise_hrs = raw.get('exercise_minutes', 0) / 60
                other_hrs    = max(0, 24 - study_total - results['social_media_hours'] - results['gaming_hours'] - results['sleep_hours'] - exercise_hrs)
                time_labels = ["Study", "Social media", "Gaming", "Sleep", "Exercise", "Other"]
                time_values = [study_total, results['social_media_hours'], results['gaming_hours'],
                               results['sleep_hours'], exercise_hrs, other_hrs]
                pie_colors  = [C['c1'], C['c4'], C['c3'], C['c2'], C['c5'], '#273244']
                fig = go.Figure(go.Pie(
                    labels=time_labels, values=time_values, hole=0.56,
                    marker=dict(colors=pie_colors, line=dict(color='#0B0F14', width=2.5)),
                    textinfo='label+percent',
                    textfont=dict(size=10, color='#E5E7EB'),
                    pull=[0.04, 0, 0, 0, 0, 0],
                ))
                fig.add_annotation(text="24 hrs", x=0.5, y=0.5,
                    font=dict(size=13, color='#6B7280', family='-apple-system, system-ui'), showarrow=False)
                fig.update_layout(**CHART_BASE,
                    legend=dict(font=dict(size=10, color='#9CA3AF'), orientation='v'))
                st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.error(f"Chart error: {e}")
        st.markdown('</div>', unsafe_allow_html=True)               
    with rec_col:
        st.markdown('<div class="section-lbl">Recommendations</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="learner-card">
            <div class="learner-eyebrow">Learner Classification</div>
            <div class="learner-name">{ltype}</div>
            <div class="learner-meta">
                <div class="learner-meta-item">
                    Pass probability: <strong style="color:#E5E7EB">{results['pass_probability']}%</strong>
                </div>
                <div class="learner-meta-dot"></div>
                <div class="learner-meta-item">
                    Cluster: <strong style="color:#E5E7EB">Group {results['pred_cluster']}</strong>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        tips = generate_recommendations(results)
        if tips:
            for category, message in tips:
                st.markdown(f"""
                <div class="tip-card">
                    <div class="tip-indicator"></div>
                    <div>
                        <div class="tip-cat">{category}</div>
                        <div class="tip-txt">{message}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            st.caption(f"{len(tips)} recommendations generated from your profile.")
        else:
            st.success("No major concerns. Keep up the strong work.")
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    with st.expander("View full input summary"):
        summary = pd.DataFrame([{
            "Age": raw.get('age'), "Gender": raw.get('gender'),
            "Academic level": raw.get('academic_level'),
            "Study hours / day": raw.get('study_hours'),
            "Self-study hours / day": raw.get('self_study_hours'),
            "Online class hours / day": raw.get('online_classes_hours'),
            "Sleep hours / night": raw.get('sleep_hours'),
            "Social media hours / day": raw.get('social_media_hours'),
            "Gaming hours / day": raw.get('gaming_hours'),
            "Screen time / day": raw.get('screen_time_hours'),
            "Exercise (minutes / day)": raw.get('exercise_minutes'),
            "Caffeine (mg / day)": raw.get('caffeine_intake_mg'),
            "Mental health score": raw.get('mental_health_score'),
            "Focus index": raw.get('focus_index'),
            "Burnout level": raw.get('burnout_level'),
            "Productivity score": raw.get('productivity_score'),
            "Internet quality": raw.get('internet_quality'),
            "Part-time job": raw.get('part_time_job'),
            "Upcoming deadline": raw.get('upcoming_deadline'),
        }]).T.rename(columns={0: "Value"})
        st.dataframe(summary, use_container_width=True)
    b1, _, b3 = st.columns([2, 4, 2])
    with b1:
        if st.button("← Edit Inputs", use_container_width=True):
            st.session_state['page'] = 'input'; st.rerun()
    with b3:
        if st.button("New Prediction →", use_container_width=True, type="primary"):
            for k in ['results', 'raw_input', 'validation_warns']:
                st.session_state.pop(k, None)
            st.session_state['page'] = 'input'; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)                
page = st.session_state['page']
if page == 'landing':
    show_landing_page()
elif page == 'input':
    show_input_page()
else:
    show_results_page()