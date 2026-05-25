import streamlit as st
import joblib
import pandas as pd
import json

# ── PAGE CONFIG ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CardioScan AI",
    page_icon="🫀",
    layout="centered",
)

# ── CUSTOM CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=JetBrains+Mono:wght@300;400;500&display=swap');

/* ── ROOT VARIABLES ── */
:root {
    --red:        #ff2d55;
    --red-soft:   #ff6b81;
    --red-glow:   rgba(255,45,85,0.35);
    --dark:       #0a0a0f;
    --dark-2:     #111118;
    --dark-3:     #1a1a24;
    --dark-4:     #22222f;
    --border:     rgba(255,45,85,0.20);
    --text:       #f0f0f8;
    --text-dim:   #8888aa;
    --success:    #00e5a0;
    --success-glow: rgba(0,229,160,0.30);
}

/* ── GLOBAL RESET ── */
html, body, [class*="css"] {
    font-family: 'JetBrains Mono', monospace !important;
    background-color: var(--dark) !important;
    color: var(--text) !important;
}

/* ── ANIMATED GRID BACKGROUND ── */
.stApp {
    background-color: var(--dark) !important;
    background-image:
        linear-gradient(rgba(255,45,85,0.04) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,45,85,0.04) 1px, transparent 1px);
    background-size: 40px 40px;
    animation: gridShift 20s linear infinite;
}
@keyframes gridShift {
    0%   { background-position: 0 0; }
    100% { background-position: 40px 40px; }
}

/* ── SCANLINE OVERLAY ── */
.stApp::before {
    content: '';
    position: fixed; inset: 0;
    background: repeating-linear-gradient(
        0deg,
        transparent,
        transparent 2px,
        rgba(0,0,0,0.07) 2px,
        rgba(0,0,0,0.07) 4px
    );
    pointer-events: none;
    z-index: 9999;
}

/* ── MAIN CONTAINER ── */
.block-container {
    max-width: 780px !important;
    padding: 2rem 2.5rem 4rem !important;
}

/* ── HEADER ── */
.hero-wrap {
    text-align: center;
    padding: 2.5rem 0 2rem;
    position: relative;
}
.hero-wrap::after {
    content: '';
    display: block;
    width: 60%;
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--red), transparent);
    margin: 1.5rem auto 0;
}
.hero-icon {
    font-size: 4rem;
    line-height: 1;
    animation: heartbeat 1.4s ease-in-out infinite;
    display: inline-block;
    filter: drop-shadow(0 0 20px var(--red));
}
@keyframes heartbeat {
    0%,100% { transform: scale(1);   }
    14%      { transform: scale(1.18);}
    28%      { transform: scale(1);   }
    42%      { transform: scale(1.12);}
    70%      { transform: scale(1);   }
}
.hero-title {
    font-family: 'Syne', sans-serif !important;
    font-size: 2.8rem !important;
    font-weight: 800 !important;
    letter-spacing: -1px;
    background: linear-gradient(135deg, #fff 30%, var(--red-soft));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0.4rem 0 0.2rem !important;
    line-height: 1.1 !important;
}
.hero-sub {
    font-size: 0.78rem;
    color: var(--text-dim);
    letter-spacing: 0.25em;
    text-transform: uppercase;
}

/* ── SECTION LABELS ── */
.section-label {
    font-family: 'Syne', sans-serif !important;
    font-size: 1rem !important;
    letter-spacing: 0.3em;
    text-transform: uppercase;
    color: var(--red) !important;
    border-left: 2px solid var(--red);
    padding-left: 0.6rem;
    margin: 2rem 0 1rem !important;
    display: block;
}

/* ── INPUT CARDS ── */
div[data-testid="stNumberInput"],
div[data-testid="stSelectbox"] {
    background: var(--dark-3) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    padding: 0.6rem 0.8rem !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
    margin-bottom: 0.5rem !important;
}
div[data-testid="stNumberInput"]:focus-within,
div[data-testid="stSelectbox"]:focus-within {
    border-color: var(--red) !important;
    box-shadow: 0 0 0 3px var(--red-glow) !important;
}

/* Input labels */
div[data-testid="stNumberInput"] label,
div[data-testid="stSelectbox"] label {
    font-size: 0.7rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--text-dim) !important;
}

/* Input fields */
input[type="number"], .stSelectbox select,
div[data-baseweb="select"] {
    background: transparent !important;
    color: var(--text) !important;
    border: none !important;
    font-family: 'JetBrains Mono', monospace !important;
}

/* Selectbox dropdown */
div[data-baseweb="select"] > div {
    background: var(--dark-3) !important;
    border-color: transparent !important;
    color: var(--text) !important;
}
div[data-baseweb="popover"] ul {
    background: var(--dark-4) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
}
div[data-baseweb="popover"] li {
    color: var(--text) !important;
}
div[data-baseweb="popover"] li:hover {
    background: var(--red-glow) !important;
}

/* ── TWO COLUMN GRID ── */
div[data-testid="column"] {
    gap: 0.5rem !important;
}

/* ── PREDICT BUTTON ── */
.stButton > button {
    width: 100% !important;
    padding: 1rem 0 !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 1rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    background: linear-gradient(135deg, #c0001e, var(--red)) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 8px !important;
    cursor: pointer !important;
    position: relative;
    overflow: hidden;
    transition: transform 0.15s, box-shadow 0.15s !important;
    box-shadow: 0 4px 24px var(--red-glow) !important;
    margin-top: 1.5rem !important;
}
.stButton > button::before {
    content: '';
    position: absolute;
    top: -50%; left: -60%;
    width: 40%; height: 200%;
    background: rgba(255,255,255,0.15);
    transform: skewX(-20deg);
    animation: shimmer 2.5s infinite;
}
@keyframes shimmer {
    0%   { left: -60%; }
    100% { left: 130%; }
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 32px var(--red-glow) !important;
}
.stButton > button:active {
    transform: translateY(0) !important;
}

/* ── RESULT CARDS ── */
div[data-testid="stAlert"] {
    border-radius: 12px !important;
    border-width: 1px !important;
    font-family: 'JetBrains Mono', monospace !important;
    animation: fadeSlideUp 0.5s cubic-bezier(.22,1,.36,1) both !important;
}
@keyframes fadeSlideUp {
    from { opacity: 0; transform: translateY(16px); }
    to   { opacity: 1; transform: translateY(0); }
}

/* Success */
div[data-testid="stAlert"][data-baseweb="notification"]:has(svg[data-testid="stAlertDynamicIcon-success"]) {
    background: rgba(0,229,160,0.08) !important;
    border-color: var(--success) !important;
    box-shadow: 0 0 32px var(--success-glow) !important;
}

/* Error */
div[data-testid="stAlert"][data-baseweb="notification"]:has(svg[data-testid="stAlertDynamicIcon-error"]) {
    background: rgba(255,45,85,0.08) !important;
    border-color: var(--red) !important;
    box-shadow: 0 0 32px var(--red-glow) !important;
}

/* ── RISK TIER COLORS ── */
/* Mild = blue (info) — already default */
/* Moderate = yellow override on warning */
div[data-testid="stAlert"][data-baseweb="notification"]:has(svg[data-testid="stAlertDynamicIcon-warning"]) {
    background: rgba(255,180,0,0.08) !important;
    border-color: #ffb400 !important;
    box-shadow: 0 0 24px rgba(255,180,0,0.20) !important;
    color: #ffe080 !important;
}
/* Critical/High = deeper red pulse */
@keyframes criticalPulse {
    0%,100% { box-shadow: 0 0 24px var(--red-glow); }
    50%      { box-shadow: 0 0 48px rgba(255,45,85,0.6); }
}
div[data-testid="stAlert"][data-baseweb="notification"]:has(svg[data-testid="stAlertDynamicIcon-error"]) {
    background: rgba(255,45,85,0.08) !important;
    border-color: var(--red) !important;
    animation: criticalPulse 2s ease-in-out infinite !important;
}

/* ── DIVIDERS ── */
hr {
    border-color: var(--border) !important;
    margin: 1.5rem 0 !important;
}

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: var(--dark); }
::-webkit-scrollbar-thumb { background: var(--red); border-radius: 2px; }

/* ── FOOTER ── */
.footer-txt {
    text-align: center;
    font-size: 0.65rem;
    color: var(--text-dim);
    letter-spacing: 0.15em;
    padding-top: 2rem;
    opacity: 0.6;
}
</style>
""", unsafe_allow_html=True)

# ── LOAD MODEL ─────────────────────────────────────────────────────────────────
@st.cache_resource
def load_model():
    return joblib.load("heart_model.pkl")

model = load_model()

with open("heart_features.json") as f:
    feature_order = json.load(f)

# ── HERO ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-wrap">
    <div class="hero-icon">🫀</div>
    <div class="hero-title">CardioScan AI</div>
    <div class="hero-sub">Clinical Heart Disease Risk Assessment</div>
</div>
""", unsafe_allow_html=True)

# ── SECTION: PATIENT PROFILE ───────────────────────────────────────────────────
st.markdown('<span class="section-label">01 — Patient Profile</span>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    age = st.number_input("Age", 18, 120, 50)
with col2:
    sex = st.selectbox("Sex", [0, 1], format_func=lambda x: "Female (0)" if x == 0 else "Male (1)")
with col3:
    cp = st.selectbox(
        "Chest Pain Type",
        [0, 1, 2, 3],
        format_func=lambda x: ["Typical Angina", "Atypical Angina", "Non-Anginal", "Asymptomatic"][x]
    )

# ── SECTION: VITALS ────────────────────────────────────────────────────────────
st.markdown('<span class="section-label">02 — Vitals</span>', unsafe_allow_html=True)

col4, col5, col6 = st.columns(3)
with col4:
    trestbps = st.number_input("Resting BP (mmHg)", 60, 250, 120)
with col5:
    chol = st.number_input("Cholesterol (mg/dl)", 50, 600, 200)
with col6:
    thalach = st.number_input("Max Heart Rate", 50, 250, 150)

col7, col8 = st.columns(2)
with col7:
    fbs = st.selectbox(
        "Fasting Blood Sugar > 120",
        [0, 1],
        format_func=lambda x: "No (0)" if x == 0 else "Yes (1)"
    )
with col8:
    oldpeak = st.number_input("Oldpeak (ST depression)", 0.0, 10.0, 1.0, step=0.1)

# ── SECTION: DIAGNOSTICS ───────────────────────────────────────────────────────
st.markdown('<span class="section-label">03 — Diagnostics</span>', unsafe_allow_html=True)

col9, col10, col11, col12, col13 = st.columns(5)
with col9:
    restecg = st.selectbox(
        "Rest ECG",
        [0, 1, 2],
        format_func=lambda x: ["Normal", "ST Abnorm.", "LV Hyper."][x]
    )
with col10:
    exang = st.selectbox(
        "Exercise Angina",
        [0, 1],
        format_func=lambda x: "No (0)" if x == 0 else "Yes (1)"
    )
with col11:
    slope = st.selectbox(
        "ST Slope",
        [0, 1, 2],
        format_func=lambda x: ["Upsloping", "Flat", "Downsloping"][x]
    )
with col12:
    ca = st.selectbox("Major Vessels (CA)", [0, 1, 2, 3])
with col13:
    thal = st.selectbox(
        "Thal",
        [1, 2, 3],
        format_func=lambda x: {1: "Normal", 2: "Fixed", 3: "Reversable"}[x]
    )

# ── PREDICT ────────────────────────────────────────────────────────────────────
st.markdown("")
if st.button("⚡  Run Cardiac Analysis"):
    with st.spinner("Analyzing cardiovascular markers…"):
        patient = pd.DataFrame([{
            "age": age, "sex": sex, "cp": cp,
            "trestbps": trestbps, "chol": chol, "fbs": fbs,
            "restecg": restecg, "thalach": thalach, "exang": exang,
            "oldpeak": oldpeak, "slope": slope, "ca": ca, "thal": thal
        }])

        # ── FEATURE ENGINEERING (matches training pipeline) ────────────────
        patient["high_chol"]         = (patient["chol"] > 240).astype(int)
        patient["high_bp"]           = (patient["trestbps"] > 140).astype(int)
        patient["hr_ratio"]          = patient["thalach"] / (220 - patient["age"])
        patient["sig_oldpeak"]       = (patient["oldpeak"] > 2.0).astype(int)
        patient["age_group_middle"]  = 0
        patient["age_group_senior"]  = 0
        patient["age_group_elderly"] = 0
        if 40 <= age < 55:
            patient["age_group_middle"]  = 1
        elif 55 <= age < 70:
            patient["age_group_senior"]  = 1
        elif age >= 70:
            patient["age_group_elderly"] = 1
        # ───────────────────────────────────────────────────────────────────

        # Reorder columns to match training feature order
        try:
            patient = patient[feature_order]
        except KeyError as e:
            st.error(f"Feature mismatch with heart_features.json: {e}")
            st.stop()

        pred  = model.predict(patient)[0]
        proba = model.predict_proba(patient)[0][1]

        # ── TARGET WAS INVERTED DURING TRAINING — flip pred and proba ──────
        pred_corrected  = 1 - int(pred)
        proba_corrected = 1.0 - proba
        # ────────────────────────────────────────────────────────────────────

    p = proba_corrected

    if p < 0.30:
        st.success(f"✅  **LOW RISK PROFILE** — Model confidence: **{(1-p):.1%}**")
        st.info("No significant indicators detected. Maintain healthy lifestyle habits and routine monitoring.")
    elif p < 0.50:
        st.info(f"🔵  **MILD RISK PROFILE** — Model confidence: **{p:.1%}**")
        st.write("Some mild cardiovascular indicators detected. Lifestyle improvements and periodic checkups are recommended.")
    elif p < 0.70:
        st.warning(f"⚠️  **MODERATE RISK PROFILE** — Model confidence: **{p:.1%}**")
        st.write("Several indicators associated with heart disease are present. Further medical evaluation is advised.")
    elif p < 0.85:
        st.error(f"🚨  **HIGH RISK PROFILE** — Model confidence: **{p:.1%}**")
        st.write("Strong indicators of cardiovascular disease detected. Clinical consultation is strongly recommended.")
    else:
        st.error(f"🛑  **CRITICAL RISK PROFILE** — Model confidence: **{p:.1%}**")
        st.write("Very high probability of heart disease detected. Immediate professional medical assessment is advised.")

    st.caption("This tool is for educational purposes only and does not replace professional medical diagnosis.")

# ── FOOTER ─────────────────────────────────────────────────────────────────────
st.markdown('<div class="footer-txt">CardioScan AI · For clinical research use only · Not a substitute for professional diagnosis</div>', unsafe_allow_html=True)
