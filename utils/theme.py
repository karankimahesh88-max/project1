"""
Custom visual theme for the Finance Tracker.
Injects CSS via st.markdown — gradient backgrounds, animated pill-style
sidebar navigation, glowing hover states on cards/buttons/metrics, and
smooth fade-in transitions.
"""

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&family=Inter:wght@400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* ---------- App background ---------- */
.stApp {
    background: linear-gradient(135deg, #0f1226 0%, #1a1f3c 45%, #241b3f 100%);
    background-attachment: fixed;
}

/* subtle animated glow drifting across the background */
.stApp::before {
    content: "";
    position: fixed;
    top: -20%;
    left: -20%;
    width: 140%;
    height: 140%;
    background: radial-gradient(circle at 20% 20%, rgba(124, 92, 255, 0.15), transparent 40%),
                radial-gradient(circle at 80% 70%, rgba(0, 212, 170, 0.12), transparent 40%);
    animation: drift 18s ease-in-out infinite alternate;
    pointer-events: none;
    z-index: 0;
}
@keyframes drift {
    0%   { transform: translate(0, 0) scale(1); }
    100% { transform: translate(3%, 2%) scale(1.05); }
}

/* ---------- Main content fade-in ---------- */
section.main > div {
    animation: fadeInUp 0.5s ease;
}
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(12px); }
    to   { opacity: 1; transform: translateY(0); }
}

/* ---------- Headers ---------- */
h1, h2, h3 {
    font-family: 'Poppins', sans-serif !important;
    font-weight: 600 !important;
    background: linear-gradient(90deg, #a78bfa, #22d3ee);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* ---------- Sidebar ---------- */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #171a34 0%, #100f24 100%);
    border-right: 1px solid rgba(167, 139, 250, 0.15);
}
section[data-testid="stSidebar"] .stTitle, section[data-testid="stSidebar"] h1 {
    background: linear-gradient(90deg, #c4b5fd, #67e8f9);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* Sidebar nav radio -> animated pill buttons */
section[data-testid="stSidebar"] div[role="radiogroup"] {
    gap: 6px;
    display: flex;
    flex-direction: column;
}
section[data-testid="stSidebar"] div[role="radiogroup"] label {
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 12px;
    padding: 10px 14px !important;
    margin: 0 !important;
    transition: all 0.25s ease;
    cursor: pointer;
    position: relative;
    overflow: hidden;
}
section[data-testid="stSidebar"] div[role="radiogroup"] label:hover {
    background: rgba(167, 139, 250, 0.12);
    border-color: rgba(167, 139, 250, 0.4);
    transform: translateX(4px);
}
section[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) {
    background: linear-gradient(90deg, rgba(124, 92, 255, 0.35), rgba(34, 211, 238, 0.2));
    border-color: rgba(167, 139, 250, 0.6);
    box-shadow: 0 0 14px rgba(124, 92, 255, 0.35);
    transform: translateX(4px);
}
section[data-testid="stSidebar"] div[role="radiogroup"] label p {
    color: #e5e7eb !important;
    font-weight: 500;
}

/* ---------- Buttons ---------- */
.stButton > button, .stFormSubmitButton > button {
    background: linear-gradient(90deg, #7c5cff, #22d3ee);
    color: white;
    border: none;
    border-radius: 10px;
    font-weight: 600;
    transition: all 0.25s ease;
    box-shadow: 0 2px 8px rgba(124, 92, 255, 0.25);
}
.stButton > button:hover, .stFormSubmitButton > button:hover {
    transform: translateY(-2px) scale(1.02);
    box-shadow: 0 6px 20px rgba(124, 92, 255, 0.45);
    filter: brightness(1.1);
}
.stButton > button:active, .stFormSubmitButton > button:active {
    transform: translateY(0) scale(0.98);
}

/* ---------- Metrics ---------- */
div[data-testid="stMetric"] {
    background: rgba(255, 255, 255, 0.035);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 14px;
    padding: 14px 16px;
    transition: all 0.25s ease;
}
div[data-testid="stMetric"]:hover {
    transform: translateY(-3px);
    border-color: rgba(124, 92, 255, 0.45);
    box-shadow: 0 8px 24px rgba(124, 92, 255, 0.2);
}

/* ---------- Bordered containers (cards) ---------- */
div[data-testid="stVerticalBlockBorderWrapper"] {
    border-radius: 14px !important;
    transition: all 0.25s ease;
    background: rgba(255, 255, 255, 0.02);
}
div[data-testid="stVerticalBlockBorderWrapper"]:hover {
    border-color: rgba(34, 211, 238, 0.4) !important;
    box-shadow: 0 6px 18px rgba(34, 211, 238, 0.12);
}

/* ---------- Expanders ---------- */
details {
    background: rgba(255, 255, 255, 0.03);
    border-radius: 12px !important;
    border: 1px solid rgba(255, 255, 255, 0.07) !important;
}

/* ---------- Progress bars ---------- */
div[data-testid="stProgress"] > div > div {
    background: linear-gradient(90deg, #7c5cff, #22d3ee) !important;
    transition: width 0.6s ease;
}

/* ---------- Tabs ---------- */
button[data-baseweb="tab"] {
    transition: all 0.2s ease;
}
button[data-baseweb="tab"]:hover {
    color: #a78bfa !important;
}

/* ---------- Dataframe / tables ---------- */
div[data-testid="stDataFrame"] {
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid rgba(255, 255, 255, 0.08);
}

/* ---------- Scrollbar ---------- */
::-webkit-scrollbar { width: 10px; height: 10px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb {
    background: linear-gradient(180deg, #7c5cff, #22d3ee);
    border-radius: 10px;
}
</style>
"""


def apply_custom_theme():
    import streamlit as st
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
