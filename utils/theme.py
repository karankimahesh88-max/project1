"""
Kubera-inspired visual theme for the Finance Tracker.
Clean, minimal, light aesthetic: warm off-white background, bold black
headings, black pill buttons, soft-shadow cards, and a top nav bar with
an animated underline on hover/active — replacing the old dark sidebar look.
"""

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, sans-serif;
}

/* ================= Background ================= */
.stApp {
    background: #FAF7F1;
}
section.main .block-container {
    padding-top: 1.2rem;
    animation: fadeIn 0.5s ease;
}
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to   { opacity: 1; transform: translateY(0); }
}

/* Hide the default Streamlit sidebar entirely -- nav lives at the top now */
section[data-testid="stSidebar"] { display: none; }

/* ================= Headings ================= */
h1, h2, h3 {
    font-family: 'Inter', sans-serif !important;
    font-weight: 800 !important;
    color: #111111 !important;
    letter-spacing: -0.02em;
}
p, span, label, .stMarkdown, .stCaption { color: #33312E; }

/* ================= Top nav bar ================= */
.kb-logo {
    font-size: 1.35rem;
    font-weight: 800;
    color: #111111;
    padding-top: 6px;
    letter-spacing: -0.02em;
}
.kb-user {
    text-align: right;
    padding-top: 12px;
    font-size: 0.85rem;
    color: #6b6b6b;
}

/* Log out button (top-right) rendered as a slim outline pill */
div[data-testid="column"]:last-of-type .stButton > button {
    background: transparent;
    color: #111 !important;
    border: 1.5px solid #111 !important;
    border-radius: 999px;
    padding: 4px 16px;
    font-weight: 600;
    font-size: 0.85rem;
    transition: all 0.2s ease;
}
div[data-testid="column"]:last-of-type .stButton > button:hover {
    background: #111;
    color: #fff !important;
    transform: translateY(-1px);
}

/* ================= Tabs styled as a top nav bar ================= */
div[data-baseweb="tab-list"] {
    gap: 28px;
    border-bottom: 1.5px solid #E8E3DA;
    margin-top: 8px;
    margin-bottom: 22px;
}
button[data-baseweb="tab"] {
    height: 44px;
    background: transparent !important;
    color: #6b6b6b !important;
    font-weight: 600;
    font-size: 0.95rem;
    border: none !important;
    position: relative;
    transition: color 0.2s ease;
}
button[data-baseweb="tab"]::after {
    content: "";
    position: absolute;
    left: 0; bottom: -1.5px;
    width: 0%;
    height: 2.5px;
    background: #111111;
    transition: width 0.25s ease;
}
button[data-baseweb="tab"]:hover {
    color: #111111 !important;
}
button[data-baseweb="tab"]:hover::after { width: 100%; }
button[data-baseweb="tab"][aria-selected="true"] {
    color: #111111 !important;
}
button[data-baseweb="tab"][aria-selected="true"]::after {
    width: 100%;
    background: #C9622A; /* warm rust accent */
}
div[data-baseweb="tab-highlight"] { display: none; }

/* ================= Buttons -> bold black pills, Kubera style ================= */
.stButton > button, .stFormSubmitButton > button {
    background: #111111;
    color: #ffffff;
    border: none;
    border-radius: 999px;
    font-weight: 600;
    padding: 8px 22px;
    transition: all 0.2s ease;
    box-shadow: none;
}
.stButton > button:hover, .stFormSubmitButton > button:hover {
    background: #C9622A;
    transform: translateY(-2px);
    box-shadow: 0 6px 16px rgba(201, 98, 42, 0.3);
}
.stButton > button:active, .stFormSubmitButton > button:active {
    transform: translateY(0);
}

/* ================= Metrics ================= */
div[data-testid="stMetric"] {
    background: #ffffff;
    border: 1px solid #ECE6DA;
    border-radius: 14px;
    padding: 16px 18px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    transition: all 0.25s ease;
}
div[data-testid="stMetric"]:hover {
    transform: translateY(-3px);
    box-shadow: 0 10px 24px rgba(0,0,0,0.08);
    border-color: #C9622A;
}
div[data-testid="stMetricLabel"] { color: #6b6b6b !important; }
div[data-testid="stMetricValue"] { color: #111111 !important; font-weight: 700; }

/* ================= Bordered containers (cards) ================= */
div[data-testid="stVerticalBlockBorderWrapper"] {
    border-radius: 14px !important;
    background: #ffffff !important;
    border-color: #ECE6DA !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    transition: all 0.25s ease;
}
div[data-testid="stVerticalBlockBorderWrapper"]:hover {
    box-shadow: 0 10px 24px rgba(0,0,0,0.08);
    border-color: #C9622A !important;
    transform: translateY(-2px);
}

/* ================= Expanders ================= */
details {
    background: #ffffff;
    border-radius: 12px !important;
    border: 1px solid #ECE6DA !important;
    transition: all 0.2s ease;
}
details:hover { border-color: #C9622A !important; }
details summary { color: #111 !important; font-weight: 600; }

/* ================= Progress bars ================= */
div[data-testid="stProgress"] > div > div {
    background: linear-gradient(90deg, #C9622A, #E8A15C) !important;
    transition: width 0.6s ease;
}

/* ================= Inputs ================= */
.stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"], .stDateInput input {
    border-radius: 10px !important;
    border-color: #E0DACE !important;
}
.stTextInput input:focus, .stNumberInput input:focus {
    border-color: #C9622A !important;
    box-shadow: 0 0 0 1px #C9622A !important;
}

/* ================= Dataframe / tables ================= */
div[data-testid="stDataFrame"] {
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid #ECE6DA;
}

/* ================= Alerts ================= */
div[data-testid="stAlert"] {
    border-radius: 10px;
    animation: alertSlide 0.35s ease;
}
@keyframes alertSlide {
    from { opacity: 0; transform: translateX(-8px); }
    to   { opacity: 1; transform: translateX(0); }
}

/* ================= Scrollbar ================= */
::-webkit-scrollbar { width: 9px; height: 9px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb {
    background: #D8CFBE;
    border-radius: 10px;
}
</style>
"""


def apply_custom_theme():
    import streamlit as st
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
