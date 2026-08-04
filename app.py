
import streamlit as st
import joblib
import pandas as pd
import time

# ──────────────────────────────────────────────
# Page config
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="SpamShield AI",
    page_icon="🛡️",
    layout="centered",
    initial_sidebar_state="collapsed",
)


# ──────────────────────────────────────────────
# Custom CSS — dark premium theme
# ──────────────────────────────────────────────
st.markdown("""
<style>
    /* ── Google Font ── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    /* ── Root variables ── */
    :root {
        --bg-primary: #0f172a;
        --bg-card: rgba(30, 41, 59, 0.65);
        --bg-card-hover: rgba(30, 41, 59, 0.85);
        --border-glass: rgba(99, 102, 241, 0.2);
        --border-glow: rgba(99, 102, 241, 0.4);
        --accent-blue: #6366f1;
        --accent-cyan: #22d3ee;
        --accent-green: #34d399;
        --accent-red: #f87171;
        --accent-amber: #fbbf24;
        --text-primary: #f1f5f9;
        --text-secondary: #94a3b8;
        --text-muted: #64748b;
    }

    /* ── Global ── */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #0f172a 100%) !important;
        font-family: 'Inter', sans-serif !important;
    }

    .stApp > header { background: transparent !important; }

    .block-container {
        max-width: 760px !important;
        padding-top: 2rem !important;
        padding-bottom: 4rem !important;
    }

    /* ── Hide default Streamlit elements ── */
    #MainMenu, footer, .stDeployButton { display: none !important; }

    /* ── Hero header ── */
    .hero-header {
        text-align: center;
        padding: 2.5rem 0 1.5rem;
    }
    .hero-header .logo-icon {
        font-size: 3.2rem;
        margin-bottom: 0.5rem;
        filter: drop-shadow(0 0 24px rgba(99, 102, 241, 0.5));
    }
    .hero-header h1 {
        font-family: 'Inter', sans-serif;
        font-size: 2.4rem;
        font-weight: 800;
        background: linear-gradient(135deg, #e0e7ff 0%, #6366f1 50%, #22d3ee 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0;
        letter-spacing: -0.03em;
    }
    .hero-header p {
        color: var(--text-secondary);
        font-size: 1rem;
        font-weight: 400;
        margin-top: 0.4rem;
    }

    /* ── Glass card ── */
    .glass-card {
        background: var(--bg-card);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid var(--border-glass);
        border-radius: 16px;
        padding: 2rem;
        margin-bottom: 1.5rem;
        transition: all 0.3s ease;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    .glass-card:hover {
        border-color: var(--border-glow);
        box-shadow: 0 8px 40px rgba(99, 102, 241, 0.15);
    }

    /* ── Section title ── */
    .section-label {
        font-family: 'Inter', sans-serif;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: var(--accent-blue);
        margin-bottom: 1rem;
    }

    /* ── Text area styling ── */
    .stTextArea textarea {
        background: rgba(15, 23, 42, 0.6) !important;
        border: 1px solid rgba(99, 102, 241, 0.2) !important;
        border-radius: 12px !important;
        color: var(--text-primary) !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.95rem !important;
        padding: 1rem !important;
        transition: border-color 0.3s ease, box-shadow 0.3s ease !important;
    }
    .stTextArea textarea:focus {
        border-color: var(--accent-blue) !important;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.15) !important;
    }
    .stTextArea textarea::placeholder {
        color: var(--text-muted) !important;
    }
    .stTextArea label {
        color: var(--text-secondary) !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 500 !important;
    }

    /* ── Button styling ── */
    .stButton > button {
        width: 100% !important;
        background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.8rem 2rem !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.02em !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 16px rgba(99, 102, 241, 0.3) !important;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #818cf8 0%, #6366f1 100%) !important;
        box-shadow: 0 6px 24px rgba(99, 102, 241, 0.45) !important;
        transform: translateY(-1px) !important;
    }
    .stButton > button:active {
        transform: translateY(0px) !important;
    }

    /* ── Result cards ── */
    .result-spam {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.15) 0%, rgba(248, 113, 113, 0.08) 100%);
        border: 1px solid rgba(239, 68, 68, 0.3);
        border-radius: 16px;
        padding: 1.8rem;
        text-align: center;
    }
    .result-ham {
        background: linear-gradient(135deg, rgba(52, 211, 153, 0.15) 0%, rgba(16, 185, 129, 0.08) 100%);
        border: 1px solid rgba(52, 211, 153, 0.3);
        border-radius: 16px;
        padding: 1.8rem;
        text-align: center;
    }
    .result-icon { font-size: 2.8rem; margin-bottom: 0.5rem; }
    .result-label {
        font-family: 'Inter', sans-serif;
        font-size: 1.4rem;
        font-weight: 700;
        margin: 0.3rem 0;
    }
    .result-sublabel {
        font-family: 'Inter', sans-serif;
        font-size: 0.85rem;
        color: var(--text-secondary);
    }

    /* ── Confidence bar ── */
    .confidence-container {
        margin-top: 1.5rem;
    }
    .confidence-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.6rem;
    }
    .confidence-label {
        font-family: 'Inter', sans-serif;
        font-size: 0.85rem;
        font-weight: 500;
        color: var(--text-secondary);
    }
    .confidence-value {
        font-family: 'Inter', sans-serif;
        font-size: 1.1rem;
        font-weight: 700;
    }
    .confidence-track {
        width: 100%;
        height: 10px;
        background: rgba(15, 23, 42, 0.6);
        border-radius: 99px;
        overflow: hidden;
    }
    .confidence-fill {
        height: 100%;
        border-radius: 99px;
        transition: width 1s ease;
    }

    /* ── Metrics row ── */
    .metrics-row {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 1rem;
        margin-top: 1rem;
    }
    .metric-card {
        background: var(--bg-card);
        backdrop-filter: blur(16px);
        border: 1px solid var(--border-glass);
        border-radius: 12px;
        padding: 1.2rem;
        text-align: center;
        transition: all 0.3s ease;
    }
    .metric-card:hover {
        border-color: var(--border-glow);
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(99, 102, 241, 0.12);
    }
    .metric-icon {
        font-size: 1.4rem;
        margin-bottom: 0.4rem;
    }
    .metric-value {
        font-family: 'Inter', sans-serif;
        font-size: 1.5rem;
        font-weight: 700;
        color: var(--text-primary);
    }
    .metric-name {
        font-family: 'Inter', sans-serif;
        font-size: 0.72rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: var(--text-muted);
        margin-top: 0.2rem;
    }

    /* ── About section ── */
    .about-section {
        margin-top: 0.5rem;
    }
    .about-section h3 {
        font-family: 'Inter', sans-serif;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: var(--accent-blue);
        margin-bottom: 0.8rem;
        margin-top: 0;
    }
    .tech-pills {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
        margin-top: 0.5rem;
    }
    .pill {
        display: inline-block;
        background: rgba(99, 102, 241, 0.12);
        border: 1px solid rgba(99, 102, 241, 0.2);
        border-radius: 99px;
        padding: 0.35rem 0.85rem;
        font-family: 'Inter', sans-serif;
        font-size: 0.78rem;
        font-weight: 500;
        color: #a5b4fc;
    }

    /* ── Footer ── */
    .app-footer {
        text-align: center;
        padding: 2rem 0 1rem;
        color: var(--text-muted);
        font-family: 'Inter', sans-serif;
        font-size: 0.78rem;
    }
    .app-footer a {
        color: var(--accent-blue);
        text-decoration: none;
    }

    /* ── Divider override ── */
    hr {
        border-color: rgba(99, 102, 241, 0.12) !important;
        margin: 1.5rem 0 !important;
    }

    /* ── Streamlit alert overrides ── */
    .stAlert { display: none !important; }

    /* ── Animations ── */
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(16px); }
        to   { opacity: 1; transform: translateY(0); }
    }
    .animate-in {
        animation: fadeInUp 0.5s ease forwards;
    }
    @keyframes pulse-glow {
        0%, 100% { box-shadow: 0 0 8px rgba(99, 102, 241, 0.2); }
        50%      { box-shadow: 0 0 20px rgba(99, 102, 241, 0.4); }
    }
</style>
""", unsafe_allow_html=True)


# ──────────────────────────────────────────────
# Load model
# ──────────────────────────────────────────────
@st.cache_resource
def load_model():
    return joblib.load("spam_detector.pkl")

@st.cache_data
def load_results():
    return pd.read_csv("model_results.csv")

model = load_model()
results = load_results()


# ──────────────────────────────────────────────
# Hero header
# ──────────────────────────────────────────────
st.markdown("""
<div class="hero-header">
    <div class="logo-icon">🛡️</div>
    <h1>SpamShield AI</h1>
    <p>Intelligent spam detection powered by machine learning</p>
</div>
""", unsafe_allow_html=True)


# ──────────────────────────────────────────────
# Model performance metrics
# ──────────────────────────────────────────────
best = results.iloc[0]
st.markdown(f"""
<div class="metrics-row">
    <div class="metric-card">
        <div class="metric-icon">🎯</div>
        <div class="metric-value">{best['Accuracy']*100:.1f}%</div>
        <div class="metric-name">Accuracy</div>
    </div>
    <div class="metric-card">
        <div class="metric-icon">🔬</div>
        <div class="metric-value">{best['Spam Precision']*100:.1f}%</div>
        <div class="metric-name">Precision</div>
    </div>
    <div class="metric-card">
        <div class="metric-icon">📡</div>
        <div class="metric-value">{best['Spam F1 Score']*100:.1f}%</div>
        <div class="metric-name">F1 Score</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<div style='height: 1.2rem'></div>", unsafe_allow_html=True)


# ──────────────────────────────────────────────
# Input card
# ──────────────────────────────────────────────
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.markdown('<div class="section-label">✉️ &nbsp;Message Analysis</div>', unsafe_allow_html=True)

message = st.text_area(
    "Paste your message below",
    height=150,
    placeholder="Example: Congratulations! You've won a $1,000 gift card. Click here to claim your prize now!",
    label_visibility="collapsed",
)

analyze = st.button("🔍  Analyze Message", type="primary")
st.markdown('</div>', unsafe_allow_html=True)


# ──────────────────────────────────────────────
# Prediction result
# ──────────────────────────────────────────────
if analyze:
    if not message.strip():
        st.markdown("""
        <div class="glass-card" style="text-align:center; border-color: rgba(251, 191, 36, 0.3);">
            <span style="font-size:1.5rem;">⚠️</span>
            <p style="color: #fbbf24; font-family: 'Inter', sans-serif; font-weight: 500; margin: 0.3rem 0 0;">
                Please enter a message to analyze
            </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Show a brief loading state
        with st.spinner(""):
            time.sleep(0.6)

        prediction = model.predict([message])[0]
        is_spam = prediction == "spam"

        # Confidence score
        classifier = model.named_steps["model"]
        if hasattr(classifier, "predict_proba"):
            probabilities = model.predict_proba([message])[0]
            spam_index = list(model.classes_).index("spam")
            confidence = probabilities[spam_index] * 100
        else:
            score = model.decision_function([message])[0]
            # Normalize the SVM decision function to a 0-100 scale
            import math
            confidence = 1 / (1 + math.exp(-score)) * 100

        if is_spam:
            display_conf = confidence
            bar_color = "linear-gradient(90deg, #fbbf24 0%, #f87171 100%)"
            conf_color = "#f87171"
        else:
            display_conf = 100 - confidence
            bar_color = "linear-gradient(90deg, #6366f1 0%, #34d399 100%)"
            conf_color = "#34d399"

        # Result card
        if is_spam:
            st.markdown(f"""
            <div class="result-spam animate-in">
                <div class="result-icon">🚫</div>
                <div class="result-label" style="color: #f87171;">SPAM DETECTED</div>
                <div class="result-sublabel">This message appears to be spam</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="result-ham animate-in">
                <div class="result-icon">✅</div>
                <div class="result-label" style="color: #34d399;">LEGITIMATE</div>
                <div class="result-sublabel">This message appears safe</div>
            </div>
            """, unsafe_allow_html=True)

        # Confidence bar
        st.markdown(f"""
        <div class="confidence-container animate-in" style="animation-delay: 0.15s;">
            <div class="confidence-header">
                <span class="confidence-label">Confidence</span>
                <span class="confidence-value" style="color: {conf_color};">{display_conf:.1f}%</span>
            </div>
            <div class="confidence-track">
                <div class="confidence-fill" style="width: {display_conf}%; background: {bar_color};"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='height: 0.5rem'></div>", unsafe_allow_html=True)


# ──────────────────────────────────────────────
# About / Tech stack (collapsible)
# ──────────────────────────────────────────────
st.markdown("<hr>", unsafe_allow_html=True)

with st.expander("ℹ️  About this project", expanded=False):
    st.markdown("""
    <div class="about-section">
        <h3>Technology</h3>
        <div class="tech-pills">
            <span class="pill">Linear SVM</span>
            <span class="pill">TF-IDF</span>
            <span class="pill">Scikit-learn</span>
            <span class="pill">Streamlit</span>
            <span class="pill">Python</span>
        </div>
        <br>
        <h3>How it works</h3>
        <p style="color: #94a3b8; font-size: 0.88rem; line-height: 1.65;">
            Messages are vectorized using <strong style="color:#a5b4fc">TF-IDF</strong> with unigrams and bigrams,
            then classified by a <strong style="color:#a5b4fc">Linear SVM</strong> model selected for the highest
            spam F1-score across Naive Bayes, Logistic Regression, and SVM comparisons.
        </p>
        <h3>Limitation</h3>
        <p style="color: #94a3b8; font-size: 0.88rem; line-height: 1.65;">
            Trained on SMS-style messages. A production filter would also use sender reputation,
            URL analysis, email headers, and more recent training data.
        </p>
    </div>
    """, unsafe_allow_html=True)


# ──────────────────────────────────────────────
# Footer
# ──────────────────────────────────────────────
st.markdown("""
<div class="app-footer">
    Built with 🤍 by <a href="https://github.com/NONion15" target="_blank">NONion15</a>
    &nbsp;·&nbsp; Powered by Streamlit & Scikit-learn
</div>
""", unsafe_allow_html=True)
