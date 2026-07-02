"""
Custom visual theme for the Finance Tracker.
Lighter, vibrant animated gradient background with visible floating shapes,
plus a variety of distinct animations (gradient shift, floating blobs,
button shimmer, staggered card entrance, pulsing active nav, bounce icons).
"""

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&family=Inter:wght@400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* ================= Animated gradient background ================= */
.stApp {
    background: linear-gradient(120deg, #4338ca, #7c3aed, #db2777, #2563eb);
    background-size: 300% 300%;
    animation: gradientShift 16s ease infinite;
}
@keyframes gradientShift {
    0%   { background-position: 0% 50%; }
    50%  { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* Frosted overlay so text stays readable over the vivid gradient */
.stApp::after {
    content: "";
    position: fixed;
    inset: 0;
    background: rgba(15, 15, 35, 0.55);
    z-index: 0;
    pointer-events: none;
}

/* Floating glowing blobs -- clearly visible, drifting at different speeds */
.stApp::before {
    content: "";
    position: fixed;
    top: -10%;
    left: -10%;
    width: 130%;
    height: 130%;
    background:
        radial-gradient(circle at 15% 20%, rgba(255, 200, 87, 0.35), transparent 22%),
        radial-gradient(circle at 85% 15%, rgba(56, 189, 248, 0.4), transparent 24%),
        radial-gradient(circle at 25% 85%, rgba(244, 63, 94, 0.35), transparent 25%),
        radial-gradient(circle at 80% 80%, rgba(139, 92, 246, 0.4), transparent 26%);
    animation: blobFloat 14s ease-in-out infinite alternate;
    z-index: 0;
    pointer-events: none;
    filter: blur(4px);
}
@keyframes blobFloat {
    0%   { transform: translate(0, 0) rotate(0deg) scale(1); }
    50%  { transform: translate(3%, -2%) rotate(3deg) scale(1.08); }
    100% { transform: translate(-2%, 3%) rotate(-2deg) scale(1.03); }
}

section.main .block-container { position: relative; z-index: 1; }
section[data-testid="stSidebar"] { position: relative; z-index: 1; }

/* ================= Content entrance ================= */
section.main > div {
    animation: fadeInUp 0.55s ease;
}
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(16px); }
    to   { opacity: 1; transform: translateY(0); }
}

/* Stagger metric cards / containers so they cascade in */
div[data-testid="stMetric"], div[data-testid="stVerticalBlockBorderWrapper"] {
    animation: fadeInUp 0.5s ease backwards;
}
div[data-testid="column"]:nth-of-type(1) div[data-testid="stMetric"] { animation-delay: 0.05s; }
div[data-testid="column"]:nth-of-type(2) div[data-testid="stMetric"] { animation-delay: 0.1s; }
div[data-testid="column"]:nth-of-type(3) div[data-testid="stMetric"] { animation-delay: 0.15s; }
div[data-testid="column"]:nth-of-type(4) div[data-testid="stMetric"] { animation-delay: 0.2s; }
div[data-testid="column"]:nth-of-type(5) div[data-testid="stMetric"] { animation-delay: 0.25s; }

/* ================= Headers ================= */
h1, h2, h3 {
    font-family: 'Poppins', sans-serif !important;
    font-weight: 700 !important;
    color: #ffffff !important;
    text-shadow: 0 2px 12px rgba(0,0,0,0.35);
}
h2 {
    display: inline-block;
    animation: headerPop 0.5s ease;
}
@keyframes headerPop {
    0%   { opacity: 0; transform: scale(0.9); }
    70%  { transform: scale(1.02); }
    100% { opacity: 1; transform: scale(1); }
}

/* ================= Sidebar ================= */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, rgba(20, 16, 50, 0.92) 0%, rgba(35, 20, 60, 0.92) 100%);
    border-right: 1px solid rgba(255, 255, 255, 0.12);
    backdrop-filter: blur(6px);
}
section[data-testid="stSidebar"] h1 {
    color: #fff !important;
}

/* Sidebar nav -> animated pill buttons */
section[data-testid="stSidebar"] div[role="radiogroup"] {
    gap: 8px;
    display: flex;
    flex-direction: column;
}
section[data-testid="stSidebar"] div[role="radiogroup"] label {
    background: rgba(255, 255, 255, 0.06);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 12px;
    padding: 11px 14px !important;
    margin: 0 !important;
    transition: all 0.25s cubic-bezier(.4,0,.2,1);
    cursor: pointer;
    position: relative;
    overflow: hidden;
}
/* shimmer sweep on hover */
section[data-testid="stSidebar"] div[role="radiogroup"] label::before {
    content: "";
    position: absolute;
    top: 0; left: -75%;
    width: 50%; height: 100%;
    background: linear-gradient(120deg, transparent, rgba(255,255,255,0.35), transparent);
    transform: skewX(-20deg);
    transition: left 0.55s ease;
}
section[data-testid="stSidebar"] div[role="radiogroup"] label:hover::before { left: 125%; }
section[data-testid="stSidebar"] div[role="radiogroup"] label:hover {
    background: rgba(255, 255, 255, 0.14);
    border-color: rgba(255, 255, 255, 0.35);
    transform: translateX(5px);
}
section[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) {
    background: linear-gradient(90deg, #f59e0b, #ec4899 60%, #8b5cf6);
    border-color: transparent;
    box-shadow: 0 0 18px rgba(236, 72, 153, 0.55);
    animation: activePulse 2.2s ease-in-out infinite;
    transform: translateX(5px);
}
@keyframes activePulse {
    0%, 100% { box-shadow: 0 0 14px rgba(236, 72, 153, 0.45); }
    50%      { box-shadow: 0 0 24px rgba(236, 72, 153, 0.75); }
}
section[data-testid="stSidebar"] div[role="radiogroup"] label p {
    color: #fff !important;
    font-weight: 600;
}

/* ================= Buttons ================= */
.stButton > button, .stFormSubmitButton > button {
    background: linear-gradient(90deg, #f59e0b, #ec4899, #8b5cf6);
    background-size: 200% auto;
    color: white;
    border: none;
    border-radius: 10px;
    font-weight: 600;
    transition: all 0.3s ease;
    box-shadow: 0 3px 10px rgba(236, 72, 153, 0.3);
}
.stButton > button:hover, .stFormSubmitButton > button:hover {
    background-position: right center;
    transform: translateY(-3px) scale(1.03);
    box-shadow: 0 8px 22px rgba(236, 72, 153, 0.5);
}
.stButton > button:active, .stFormSubmitButton > button:active {
    transform: translateY(0) scale(0.97);
}

/* ================= Metrics ================= */
div[data-testid="stMetric"] {
    background: rgba(255, 255, 255, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.18);
    border-radius: 14px;
    padding: 14px 16px;
    backdrop-filter: blur(8px);
    transition: all 0.3s ease;
}
div[data-testid="stMetric"]:hover {
    transform: translateY(-5px) scale(1.02);
    border-color: rgba(255, 255, 255, 0.4);
    box-shadow: 0 10px 28px rgba(0, 0, 0, 0.25);
}
div[data-testid="stMetric"] label, div[data-testid="stMetricValue"] {
    color: #ffffff !important;
}

/* ================= Bordered containers (cards) ================= */
div[data-testid="stVerticalBlockBorderWrapper"] {
    border-radius: 14px !important;
    background: rgba(255, 255, 255, 0.08) !important;
    backdrop-filter: blur(8px);
    transition: all 0.3s ease;
}
div[data-testid="stVerticalBlockBorderWrapper"]:hover {
    border-color: rgba(255, 255, 255, 0.4) !important;
    box-shadow: 0 10px 26px rgba(0, 0, 0, 0.25);
    transform: translateY(-3px);
}

/* ================= Expanders ================= */
details {
    background: rgba(255, 255, 255, 0.08);
    border-radius: 12px !important;
    border: 1px solid rgba(255, 255, 255, 0.15) !important;
    transition: all 0.25s ease;
}
details:hover { border-color: rgba(255,255,255,0.35) !important; }
details summary { color: #fff !important; }

/* ================= Progress bars ================= */
div[data-testid="stProgress"] > div > div {
    background: linear-gradient(90deg, #f59e0b, #ec4899, #8b5cf6) !important;
    background-size: 200% auto;
    animation: progressShimmer 3s linear infinite;
    transition: width 0.6s ease;
}
@keyframes progressShimmer {
    0%   { background-position: 0% center; }
    100% { background-position: 200% center; }
}

/* ================= Tabs ================= */
button[data-baseweb="tab"] {
    transition: all 0.25s ease;
    color: rgba(255,255,255,0.7) !important;
}
button[data-baseweb="tab"]:hover {
    color: #fff !important;
    transform: translateY(-2px);
}
button[data-baseweb="tab"][aria-selected="true"] {
    color: #fbbf24 !important;
}

/* ================= Dataframe / tables ================= */
div[data-testid="stDataFrame"] {
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid rgba(255, 255, 255, 0.18);
}

/* ================= Text readability on frosted cards ================= */
p, span, label, .stMarkdown { color: #f1f5f9; }
section.main .stCaption, .stCaption p { color: #cbd5e1 !important; }

/* ================= Alerts (info/success/error) get a soft glow-in ================= */
div[data-testid="stAlert"] {
    animation: alertSlide 0.4s ease;
    border-radius: 10px;
}
@keyframes alertSlide {
    from { opacity: 0; transform: translateX(-10px); }
    to   { opacity: 1; transform: translateX(0); }
}

/* ================= Scrollbar ================= */
::-webkit-scrollbar { width: 10px; height: 10px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb {
    background: linear-gradient(180deg, #f59e0b, #ec4899, #8b5cf6);
    border-radius: 10px;
}
</style>
"""


def apply_custom_theme():
    import streamlit as st
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
