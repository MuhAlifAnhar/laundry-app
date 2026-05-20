import streamlit as st
from google import genai
from google.genai import types
import os
import json
import time
import urllib.parse
import requests
from streamlit_lottie import st_lottie
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set page config
st.set_page_config(
    page_title="Adem-Adem Grup",
    page_icon="🛡️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ─── Premium CSS: WhatsApp-inspired, bulletproof dark/light mode ─────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    /* ══ NUCLEAR OVERRIDE: force dark text on everything ══ */
    *, *::before, *::after {
        color: #1a1a1a !important;
    }

    /* ── Streamlit native component overrides ── */
    .stMarkdown, .stMarkdown p, .stMarkdown span, .stMarkdown li,
    .stText, .stTextArea label, .stTextInput label,
    .stAlert p, .stCaption, .stCaption p,
    div[data-testid="stMarkdownContainer"],
    div[data-testid="stMarkdownContainer"] p,
    div[data-testid="stMarkdownContainer"] span,
    div[data-testid="stMarkdownContainer"] li,
    div[data-testid="stText"],
    .element-container, .element-container p, .element-container span {
        color: #1a1a1a !important;
    }

    /* ── Global layout ── */
    .main, [data-testid="stAppViewContainer"] {
        background: linear-gradient(160deg, #e8f5e9 0%, #ECE5DD 30%, #f0f4f0 60%, #ECE5DD 100%) !important;
        background-attachment: fixed !important;
        font-family: 'Inter', 'Segoe UI', sans-serif !important;
    }
    [data-testid="stSidebar"], [data-testid="stHeader"] {
        background-color: transparent !important;
    }
    .block-container {
        padding-top: 2rem !important;
        max-width: 720px !important;
        background-color: transparent !important;
    }

    /* ── Animated background pattern (subtle WhatsApp doodle feel) ── */
    [data-testid="stAppViewContainer"]::before {
        content: '';
        position: fixed;
        top: 0; left: 0; right: 0; bottom: 0;
        background-image:
            radial-gradient(circle at 20% 80%, rgba(37, 211, 102, 0.06) 0%, transparent 50%),
            radial-gradient(circle at 80% 20%, rgba(7, 94, 84, 0.05) 0%, transparent 50%),
            radial-gradient(circle at 50% 50%, rgba(18, 140, 126, 0.03) 0%, transparent 60%);
        animation: bgPulse 12s ease-in-out infinite;
        pointer-events: none;
        z-index: 0;
    }
    @keyframes bgPulse {
        0%, 100% { opacity: 0.7; transform: scale(1); }
        50% { opacity: 1; transform: scale(1.05); }
    }

    /* ── EXEMPTION: Header card text stays white ── */
    .app-header, .app-header *,
    .app-header h1, .app-header p {
        color: #ffffff !important;
    }

    /* ── Headings ── */
    h1, h2, h3, .stMarkdown h3 {
        color: #075E54 !important;
        font-weight: 700 !important;
        font-family: 'Inter', sans-serif !important;
    }

    /* ── App Header Card ── */
    .app-header {
        background: linear-gradient(135deg, #075E54 0%, #128C7E 40%, #25D366 100%) !important;
        color: #ffffff !important;
        border-radius: 20px !important;
        padding: 2.5rem 1.5rem 2rem !important;
        text-align: center !important;
        margin-bottom: 1.5rem !important;
        box-shadow: 0 12px 40px rgba(7, 94, 84, 0.35) !important;
        position: relative;
        overflow: hidden;
        animation: headerSlideIn 0.8s ease-out;
    }
    @keyframes headerSlideIn {
        from { opacity: 0; transform: translateY(-30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .app-header::before {
        content: '';
        position: absolute;
        top: -50%; left: -50%;
        width: 200%; height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 60%);
        animation: shimmer 8s ease-in-out infinite;
    }
    .app-header::after {
        content: '';
        position: absolute;
        bottom: -2px; left: 0; right: 0;
        height: 4px;
        background: linear-gradient(90deg, #25D366, #ffffff80, #25D366);
        background-size: 200% 100%;
        animation: borderGlow 3s linear infinite;
    }
    @keyframes shimmer {
        0%, 100% { transform: translate(0, 0) rotate(0deg); }
        33% { transform: translate(15px, 10px) rotate(1deg); }
        66% { transform: translate(-10px, 5px) rotate(-1deg); }
    }
    @keyframes borderGlow {
        0% { background-position: 0% 0%; }
        100% { background-position: 200% 0%; }
    }
    .app-header h1 {
        color: #ffffff !important;
        font-size: 2.2rem !important;
        margin-bottom: 0.3rem !important;
        position: relative; z-index: 1;
        text-shadow: 0 2px 10px rgba(0,0,0,0.15);
    }
    .app-header p {
        color: rgba(255,255,255,0.92) !important;
        font-size: 1.08rem !important;
        font-weight: 400 !important;
        position: relative; z-index: 1;
    }
    .app-header .badge {
        display: inline-block;
        background: rgba(255,255,255,0.2) !important;
        color: #ffffff !important;
        padding: 4px 14px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.5px;
        margin-top: 10px;
        position: relative; z-index: 1;
        backdrop-filter: blur(4px);
    }

    /* ── Main Action Button ── */
    .stButton>button, .stButton>button * {
        background: linear-gradient(135deg, #25D366 0%, #128C7E 100%) !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        font-size: 1.05rem !important;
        border-radius: 12px !important;
        border: none !important;
        padding: 0.75rem 1.5rem !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        width: 100% !important;
        box-shadow: 0 4px 15px rgba(37, 211, 102, 0.35) !important;
        letter-spacing: 0.3px !important;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #128C7E 0%, #075E54 100%) !important;
        box-shadow: 0 6px 20px rgba(7, 94, 84, 0.4) !important;
        transform: translateY(-2px) !important;
    }
    .stButton>button:active {
        transform: translateY(0) !important;
        box-shadow: 0 2px 8px rgba(7, 94, 84, 0.3) !important;
    }

    /* ── Status Cards (premium bubble style) ── */
    .status-card {
        padding: 1.25rem 1.5rem !important;
        border-radius: 14px !important;
        margin-bottom: 1rem !important;
        position: relative !important;
        overflow: hidden !important;
        animation: cardSlideIn 0.6s cubic-bezier(0.16, 1, 0.3, 1) !important;
    }
    @keyframes cardSlideIn {
        from { opacity: 0; transform: translateY(20px) scale(0.97); }
        to { opacity: 1; transform: translateY(0) scale(1); }
    }
    .status-card::after {
        content: '';
        position: absolute;
        top: 0; right: 0;
        width: 80px; height: 80px;
        border-radius: 50%;
        opacity: 0.08;
        animation: statusPulse 3s ease-in-out infinite;
    }
    @keyframes statusPulse {
        0%, 100% { transform: scale(1); opacity: 0.08; }
        50% { transform: scale(1.4); opacity: 0.04; }
    }
    .status-card-hoax::after { background: #e53935; }
    .status-card-fakta::after { background: #43a047; }
    .status-card-cek::after { background: #fb8c00; }
    .status-card .status-icon {
        font-size: 1.6rem !important;
        margin-bottom: 0.3rem !important;
        display: block !important;
    }
    .status-card .status-label {
        font-weight: 800 !important;
        font-size: 1.1rem !important;
        letter-spacing: 0.5px !important;
        margin-bottom: 0.5rem !important;
        display: block !important;
    }
    .status-card .status-reason {
        font-size: 0.95rem !important;
        line-height: 1.6 !important;
        font-weight: 400 !important;
    }

    /* Hoax */
    .status-card-hoax {
        background: linear-gradient(135deg, #fff5f5 0%, #ffebee 100%) !important;
        border-left: 5px solid #e53935 !important;
        box-shadow: 0 4px 20px rgba(229, 57, 53, 0.15), 0 1px 3px rgba(0,0,0,0.06) !important;
    }
    .status-card-hoax .status-label { color: #c62828 !important; }

    /* Fakta */
    .status-card-fakta {
        background: linear-gradient(135deg, #f1f8e9 0%, #e8f5e9 100%) !important;
        border-left: 5px solid #43a047 !important;
        box-shadow: 0 4px 20px rgba(67, 160, 71, 0.15), 0 1px 3px rgba(0,0,0,0.06) !important;
    }
    .status-card-fakta .status-label { color: #2e7d32 !important; }

    /* Perlu Cek */
    .status-card-cek {
        background: linear-gradient(135deg, #fffde7 0%, #fff3e0 100%) !important;
        border-left: 5px solid #fb8c00 !important;
        box-shadow: 0 4px 20px rgba(251, 140, 0, 0.15), 0 1px 3px rgba(0,0,0,0.06) !important;
    }
    .status-card-cek .status-label { color: #e65100 !important; }

    /* ── Input Textarea ── */
    .input-section {
        background: rgba(255, 255, 255, 0.7) !important;
        color: #1a1a1a !important;
        backdrop-filter: blur(10px) !important;
        -webkit-backdrop-filter: blur(10px) !important;
        border-radius: 16px !important;
        padding: 20px !important;
        margin-bottom: 16px !important;
        box-shadow: 0 4px 20px rgba(0,0,0,0.06) !important;
        border: 1px solid rgba(37, 211, 102, 0.15) !important;
        animation: fadeInUp 0.5s ease-out;
    }
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(15px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .input-section h4 {
        color: #075E54 !important;
        margin-bottom: 4px !important;
    }
    .stTextArea textarea {
        border-radius: 12px !important;
        border: 2px solid #d1d5db !important;
        padding: 14px !important;
        font-size: 0.95rem !important;
        background-color: #ffffff !important;
        color: #1a1a1a !important;
        transition: all 0.3s ease !important;
    }
    .stTextArea textarea:focus {
        border-color: #25D366 !important;
        box-shadow: 0 0 0 3px rgba(37, 211, 102, 0.15) !important;
        transform: translateY(-1px) !important;
    }
    .stTextArea label {
        color: #374151 !important;
        font-weight: 600 !important;
    }

    /* ── Response Bubble (WhatsApp chat style) ── */
    .response-bubble {
        background-color: #DCF8C6 !important;
        color: #1a1a1a !important;
        border-radius: 0 14px 14px 14px !important;
        padding: 16px 18px !important;
        margin: 8px 0 !important;
        box-shadow: 0 3px 12px rgba(0,0,0,0.08) !important;
        font-size: 0.95rem !important;
        line-height: 1.7 !important;
        position: relative !important;
        max-width: 95% !important;
        animation: bubbleIn 0.5s cubic-bezier(0.16, 1, 0.3, 1) !important;
    }
    @keyframes bubbleIn {
        from { opacity: 0; transform: translateX(-15px) scale(0.95); }
        to { opacity: 1; transform: translateX(0) scale(1); }
    }
    .response-bubble::before {
        content: '';
        position: absolute;
        top: 0; left: -8px;
        width: 0; height: 0;
        border-top: 8px solid #DCF8C6;
        border-left: 8px solid transparent;
    }

    /* ── Copy Hint ── */
    .copy-hint {
        background: linear-gradient(90deg, #e8f5e9 0%, #f1f8e9 100%) !important;
        color: #2e7d32 !important;
        border-radius: 8px !important;
        padding: 10px 14px !important;
        margin: 10px 0 6px 0 !important;
        font-size: 0.88rem !important;
        font-weight: 600 !important;
        display: flex !important;
        align-items: center !important;
        gap: 8px !important;
        border: 1px solid rgba(46, 125, 50, 0.2) !important;
    }

    /* ── Tabs styling ── */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px !important;
        background-color: #f5f5f5 !important;
        border-radius: 10px !important;
        padding: 4px !important;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px !important;
        color: #555 !important;
        font-weight: 600 !important;
        font-size: 0.85rem !important;
        padding: 8px 12px !important;
    }
    .stTabs [aria-selected="true"] {
        background-color: #ffffff !important;
        color: #075E54 !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1) !important;
    }
    .stTabs [data-baseweb="tab-panel"] {
        padding-top: 1rem !important;
    }

    /* ── Code block (copy-ready balasan) ── */
    .stCode {
        border-radius: 10px !important;
        border: 1px solid rgba(37, 211, 102, 0.25) !important;
        overflow: hidden !important;
    }
    .stCode pre, .stCode code {
        color: #1a1a1a !important;
        background-color: #f0faf0 !important;
        font-family: 'Inter', 'Segoe UI', sans-serif !important;
        font-size: 0.92rem !important;
        line-height: 1.65 !important;
        white-space: pre-wrap !important;
        word-wrap: break-word !important;
    }
    /* Make the built-in copy button more visible */
    .stCode button[kind="icon"],
    .stCode button[data-testid="stCodeCopyButton"],
    .stCodeBlock button {
        background-color: #25D366 !important;
        color: #ffffff !important;
        border-radius: 6px !important;
        opacity: 1 !important;
        width: 32px !important;
        height: 32px !important;
    }

    /* ── Hide Streamlit Branding ── */
    #MainMenu {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    header {visibility: hidden !important;}

    /* ── Divider ── */
    hr {
        border-color: rgba(7, 94, 84, 0.15) !important;
    }

    /* ── Spinner text ── */
    .stSpinner, .stSpinner > div {
        color: #075E54 !important;
    }

    /* ── Retry Status Banner ── */
    .retry-banner {
        background: linear-gradient(135deg, #fff8e1 0%, #fff3e0 100%) !important;
        border-left: 4px solid #fb8c00 !important;
        border-radius: 10px !important;
        padding: 12px 16px !important;
        margin: 8px 0 !important;
        font-size: 0.9rem !important;
        font-weight: 500 !important;
        color: #e65100 !important;
        animation: cardSlideIn 0.4s ease-out !important;
        display: flex !important;
        align-items: center !important;
        gap: 8px !important;
    }
    .retry-success {
        background: linear-gradient(135deg, #e8f5e9 0%, #f1f8e9 100%) !important;
        border-left: 4px solid #43a047 !important;
        color: #2e7d32 !important;
    }

    /* ── Footer ── */
    .app-footer {
        text-align: center !important;
        padding: 2rem 0 1.5rem !important;
        margin-top: 2.5rem !important;
        animation: fadeInUp 0.8s ease-out !important;
    }
    .footer-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(7, 94, 84, 0.25), transparent);
        margin-bottom: 1.5rem;
    }
    .footer-content {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
        font-size: 0.92rem;
        color: #6b7280 !important;
        font-weight: 500;
        flex-wrap: wrap;
    }
    .footer-content span {
        color: #6b7280 !important;
    }
    .footer-ig {
        color: #075E54 !important;
        font-weight: 700 !important;
        text-decoration: none !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        padding: 2px 8px;
        border-radius: 6px;
        background: rgba(37, 211, 102, 0.1);
    }
    .footer-ig:hover {
        color: #ffffff !important;
        background: linear-gradient(135deg, #25D366, #128C7E) !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 3px 10px rgba(37, 211, 102, 0.3) !important;
    }
    .footer-powered {
        font-size: 0.78rem;
        color: #9ca3af !important;
        margin-top: 6px;
        letter-spacing: 0.3px;
    }
    .footer-powered span {
        color: #9ca3af !important;
    }

    /* ── Success/Warning/Error alerts ── */
    .stAlert, .stAlert p, .stAlert span,
    div[data-testid="stNotification"],
    div[data-testid="stNotification"] p,
    div[data-testid="stNotification"] span {
        color: #1a1a1a !important;
    }
    .stSuccess, .stSuccess p { color: #2e7d32 !important; }
    .stWarning, .stWarning p { color: #e65100 !important; }
    .stError, .stError p { color: #c62828 !important; }

    /* ── Text input (API key) ── */
    .stTextInput input {
        color: #1a1a1a !important;
        background-color: #ffffff !important;
    }

    /* ── Share to WA Button ── */
    .btn-wa-share {
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        gap: 8px !important;
        width: 100% !important;
        padding: 0.75rem 1.5rem !important;
        background: linear-gradient(135deg, #25D366 0%, #128C7E 100%) !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        font-size: 1.05rem !important;
        text-decoration: none !important;
        border-radius: 12px !important;
        margin-top: 12px !important;
        box-shadow: 0 4px 15px rgba(37, 211, 102, 0.35) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    .btn-wa-share:hover {
        background: linear-gradient(135deg, #128C7E 0%, #075E54 100%) !important;
        box-shadow: 0 6px 20px rgba(7, 94, 84, 0.4) !important;
        transform: translateY(-2px) !important;
    }
    .btn-wa-share svg {
        width: 22px !important;
        height: 22px !important;
        fill: currentColor !important;
    }

    /* ── Tab text inside tab buttons ── */
    .stTabs [data-baseweb="tab"] *,
    .stTabs [data-baseweb="tab"] p,
    .stTabs [data-baseweb="tab"] span {
        color: inherit !important;
    }

    /* ── Metric Cards (Dashboard) ── */
    [data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.8) !important;
        backdrop-filter: blur(8px) !important;
        -webkit-backdrop-filter: blur(8px) !important;
        padding: 15px 10px !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05) !important;
        border: 1px solid rgba(37, 211, 102, 0.2) !important;
        text-align: center !important;
        transition: transform 0.3s ease !important;
    }
    [data-testid="stMetric"]:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 6px 20px rgba(37, 211, 102, 0.15) !important;
    }
    [data-testid="stMetricLabel"] {
        justify-content: center !important;
        font-weight: 700 !important;
        color: #075E54 !important;
        font-size: 0.9rem !important;
    }
    [data-testid="stMetricValue"] {
        justify-content: center !important;
        font-size: 1.8rem !important;
        font-weight: 800 !important;
        color: #1a1a1a !important;
    }
</style>
""", unsafe_allow_html=True)

# ─── Header ──────────────────────────────────────────────────────────────────
st.markdown("""
<div class="app-header">
    <h1>🛡️ Adem-Adem Grup</h1>
    <p>Luruskan info, tetap jaga silaturahmi.</p>
    <span class="badge">✨ Powered by Gemini AI</span>
</div>
""", unsafe_allow_html=True)

# API Key handling
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    api_key = st.text_input("Masukkan Gemini API Key Anda untuk mulai:", type="password")
    if api_key:
        os.environ["GEMINI_API_KEY"] = api_key
    else:
        st.warning("⚠️ API Key diperlukan. Anda bisa mendapatkannya di Google AI Studio.")
        st.stop()

# Bersihkan API key dari spasi atau tanda kutip yang tidak sengaja terbawa
api_key = api_key.strip().strip("'").strip('"')
os.environ["GEMINI_API_KEY"] = api_key

# Configure Gemini
try:
    client = genai.Client(api_key=api_key)
except Exception as e:
    st.error(f"Gagal mengonfigurasi API: {e}")
    st.stop()

# ─── Lottie Animations Helper ────────────────────────────────────────────────
@st.cache_data
def load_lottieurl(url: str):
    try:
        r = requests.get(url, timeout=5)
        if r.status_code != 200:
            return None
        return r.json()
    except Exception:
        return None

# Load animations (using reliable public Lottiefiles URLs)
lottie_thinking = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_tno6cg2w.json")  # Robot thinking/typing
lottie_success = load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_M9p23l.json")   # Robot greeting/success


# ─── Model Fallback Chain & Retry Logic ────────────────────────────────────
FALLBACK_MODELS = [
    "gemini-2.5-flash",
    "gemini-2.0-flash",
    "gemini-1.5-flash",
]

def call_gemini_with_retry(client, prompt, max_retries=3, base_delay=2):
    """Call Gemini API with automatic retry (exponential backoff) and model fallback."""
    last_error = None
    status_placeholder = st.empty()
    
    for model_idx, model_name in enumerate(FALLBACK_MODELS):
        for attempt in range(1, max_retries + 1):
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt
                )
                # Success! Show which model was used if it wasn't the primary
                if model_idx > 0 or attempt > 1:
                    status_placeholder.markdown(
                        f'<div class="retry-banner retry-success">'
                        f'✅ <b>{model_name}</b>'
                        f'</div>',
                        unsafe_allow_html=True
                    )
                else:
                    status_placeholder.empty()
                return response
                
            except Exception as e:
                last_error = e
                error_str = str(e).lower()
                
                # Check if it's a retryable server error
                is_retryable = any(kw in error_str for kw in [
                    "503", "overloaded", "unavailable",
                    "resource_exhausted", "resource exhausted",
                    "quota", "rate limit", "rate_limit",
                    "too many requests", "429",
                    "500", "internal", "deadline", "timeout",
                    "capacity", "busy", "congested"
                ])
                
                if is_retryable:
                    if attempt < max_retries:
                        delay = base_delay * (2 ** (attempt - 1))
                        status_placeholder.markdown(
                            f'<div class="retry-banner">'
                            f'⏳ Model <b>{model_name}</b> sedang sibuk '
                            f'(percobaan {attempt}/{max_retries}). '
                            f'Retry dalam {delay} detik...'
                            f'</div>',
                            unsafe_allow_html=True
                        )
                        time.sleep(delay)
                    else:
                        if model_idx < len(FALLBACK_MODELS) - 1:
                            next_model = FALLBACK_MODELS[model_idx + 1]
                            status_placeholder.markdown(
                                f'<div class="retry-banner">'
                                f'⚠️ Model <b>{model_name}</b> gagal setelah {max_retries}x percobaan. '
                                f'Beralih ke model cadangan: <b>{next_model}</b>...'
                                f'</div>',
                                unsafe_allow_html=True
                            )
                            time.sleep(1)
                        break  # Try next model in fallback chain
                else:
                    # Non-retryable error — raise immediately
                    status_placeholder.empty()
                    raise e
    
    # All models exhausted
    status_placeholder.empty()
    raise last_error if last_error else Exception("Semua model Gemini gagal merespons.")

# System Instruction
SYSTEM_INSTRUCTION = """Kamu adalah pakar literasi digital dan ahli komunikasi budaya Indonesia. Kamu menerima teks dari grup WhatsApp.

Analisis apakah teks itu hoaks, fakta, atau opini/belum terverifikasi.

Berikan alasan singkat yang logis tapi mudah dimengerti orang awam (1-2 kalimat).

Berikan juga sumber referensi untuk mendukung analisismu. Sumber bisa berupa:
- Link artikel berita terpercaya (Kompas, Detik, CNN Indonesia, Tempo, dll.)
- Link situs fact-checker (TurnBackHoax, CekFakta, Mafindo, dll.)
- Nama lembaga resmi yang memberikan klarifikasi (misal: Kementerian Kesehatan, BMKG, Pertamina, dll.)
Berikan 1-3 sumber referensi dalam bentuk array. Jika tidak ada sumber spesifik, berikan saran pencarian Google yang relevan.

Buatkan 3 pilihan balasan chat:
1. 'Sopan': Gunakan kata ganti yang hormat (Bapak/Ibu/Om/Tante), awali dengan maaf, sampaikan fakta dengan lembut. Sangat cocok untuk membalas orang tua/sesepuh tanpa menggurui.
2. 'Santai': Gunakan bahasa gaul/asik, tanpa kesan menggurui. Cocok untuk sepupu atau teman sebaya.
3. 'Formal': Gunakan bahasa baku yang netral. Cocok untuk grup RT atau lingkungan.

Format output HARUS JSON dengan struktur persis seperti ini:
{
    "status": "Hoaks" | "Fakta" | "Perlu Cek Lagi",
    "penjelasan": "Penjelasan singkat 1-2 kalimat.",
    "sumber_referensi": [
        {"judul": "Nama/judul sumber", "url": "https://link-sumber.com" },
        {"judul": "Nama/judul sumber kedua", "url": "https://link-sumber2.com" }
    ],
    "balasan_sopan": "Teks balasan sopan...",
    "balasan_santai": "Teks balasan santai...",
    "balasan_formal": "Teks balasan formal..."
}
Pastikan hanya mengembalikan JSON mentah yang valid, tanpa markdown tambahan seperti ```json.
"""

# ─── Initialize Session State ────────────────────────────────────────────────
if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None

# Input Area (wrapped in glassmorphism card)
st.markdown('<div class="input-section">', unsafe_allow_html=True)
st.markdown("#### 💬 Masukkan Pesan")
user_input = st.text_area(
    "Paste pesan dari grup WA di sini...",
    height=150,
    placeholder="Misal: Besok pom bensin tutup semua karena ada demo besar-besaran, isi full sekarang!",
    label_visibility="collapsed"
)
st.markdown('</div>', unsafe_allow_html=True)

# Action Button
if st.button("🔍  Vibe-Check Sekarang!", use_container_width=True):
    if not user_input.strip():
        st.error("Pesan tidak boleh kosong!")
    else:
        # Placeholder for Lottie Animation during loading
        lottie_placeholder = st.empty()
        with lottie_placeholder.container():
            if lottie_thinking:
                st_lottie(lottie_thinking, height=180, key="thinking")
                
        with st.spinner("🧠 Menganalisis pesan dengan Vibe-Logic..."):
            try:
                # Combine system instruction and user input
                prompt = f"{SYSTEM_INSTRUCTION}\n\nPESAN WA UNTUK DIANALISIS:\n{user_input}"
                
                # Call Gemini with automatic retry & model fallback
                response = call_gemini_with_retry(client, prompt)
                
                # Clean markdown blocks if Gemini returns them
                response_text = response.text.strip()
                if response_text.startswith("```json"):
                    response_text = response_text[7:]
                elif response_text.startswith("```"):
                    response_text = response_text[3:]
                if response_text.endswith("```"):
                    response_text = response_text[:-3]
                response_text = response_text.strip()
                
                # Parse JSON and store in session state
                try:
                    st.session_state.analysis_result = json.loads(response_text)
                except json.JSONDecodeError:
                    st.error("❌ Gagal membaca hasil dari AI. Format respons tidak valid.")
                    st.session_state.analysis_result = None
                    
            except Exception as e:
                error_msg = str(e)
                if any(kw in error_msg.lower() for kw in ["503", "overloaded", "unavailable"]):
                    st.error(
                        "🔥 **Server Gemini sedang sangat sibuk (503 Overloaded).**\n\n"
                        "Semua model cadangan juga tidak tersedia saat ini. "
                        "Silakan tunggu 1-2 menit lalu coba lagi."
                    )
                elif any(kw in error_msg.lower() for kw in ["api_key", "api key", "invalid", "unauthorized", "401", "403"]):
                    st.error(
                        "🔑 **API Key tidak valid atau sudah expired.**\n\n"
                        "Silakan periksa kembali API Key Anda di Google AI Studio."
                    )
                elif any(kw in error_msg.lower() for kw in ["quota", "rate limit", "429"]):
                    st.error(
                        "📊 **Kuota API habis atau terlalu banyak request.**\n\n"
                        "Tunggu beberapa saat sebelum mencoba lagi."
                    )
                else:
                    st.error(f"⚠️ Terjadi kesalahan: {error_msg}")
                st.session_state.analysis_result = None
                
        # Clear the lottie loading animation when done
        lottie_placeholder.empty()

# ─── Display Results (persisted via session_state) ───────────────────────────
if st.session_state.analysis_result is not None:
    result = st.session_state.analysis_result
    
    st.markdown("---")
    
    # Layout with Lottie Success Animation
    col1, col2 = st.columns([1, 5])
    with col1:
        if lottie_success:
            st_lottie(lottie_success, height=80, key="success")
    with col2:
        st.markdown("<h3 style='margin-top: 15px;'>📊 Hasil Analisis</h3>", unsafe_allow_html=True)
    
    status = result.get("status", "Perlu Cek Lagi")
    penjelasan = result.get("penjelasan", "Tidak ada penjelasan.")
    
    # Status Card with premium styling
    if "Hoaks" in status:
        card_class = "status-card status-card-hoax"
        icon = "❌"
        label = "HOAKS DETECTED"
    elif "Fakta" in status:
        card_class = "status-card status-card-fakta"
        icon = "✅"
        label = "FAKTA TERVERIFIKASI"
    else:
        card_class = "status-card status-card-cek"
        icon = "⚠️"
        label = "PERLU CEK LAGI"

    st.markdown(f"""
    <div class="{card_class}">
        <span class="status-icon">{icon}</span>
        <span class="status-label">{label}</span>
        <span class="status-reason">{penjelasan}</span>
    </div>
    """, unsafe_allow_html=True)
    
    # ─── Source References ────────────────────────────────────────────────
    sumber_list = result.get("sumber_referensi", [])
    if sumber_list and len(sumber_list) > 0:
        refs_html = ""
        for ref in sumber_list:
            judul = ref.get("judul", "Sumber")
            url = ref.get("url", "")
            if url and url.startswith("http"):
                refs_html += f'<a href="{url}" target="_blank" style="color: #075E54 !important; text-decoration: none; display: flex; align-items: center; gap: 8px; padding: 8px 12px; background: rgba(37, 211, 102, 0.08); border-radius: 8px; margin-bottom: 6px; transition: all 0.2s ease; font-weight: 500;"><span style="font-size: 1.1rem;">🔗</span> {judul}</a>'
            else:
                refs_html += f'<div style="display: flex; align-items: center; gap: 8px; padding: 8px 12px; background: rgba(37, 211, 102, 0.08); border-radius: 8px; margin-bottom: 6px; font-weight: 500; color: #1a1a1a !important;"><span style="font-size: 1.1rem;">📰</span> {judul}</div>'
        
        st.markdown(f"""
        <div style="background: rgba(255,255,255,0.75); backdrop-filter: blur(8px); border-radius: 14px; padding: 16px 18px; margin-bottom: 1rem; box-shadow: 0 2px 12px rgba(0,0,0,0.05); border: 1px solid rgba(7, 94, 84, 0.12); animation: cardSlideIn 0.7s cubic-bezier(0.16, 1, 0.3, 1);">
            <div style="font-weight: 700; font-size: 0.95rem; color: #075E54 !important; margin-bottom: 10px; display: flex; align-items: center; gap: 8px;">
                <span style="font-size: 1.2rem;">📚</span> Sumber & Referensi Fact-Check
            </div>
            {refs_html}
        </div>
        """, unsafe_allow_html=True)
    
    # ─── Tabs for Responses ──────────────────────────────────────────────
    st.markdown("### 💬 Pilih Gaya Balasan")
    tab1, tab2, tab3 = st.tabs([
        "🙏 Anak Berbakti (Sopan)",
        "😎 Sepupu Asik (Santai)",
        "👔 Warga Bijak (Formal)"
    ])
    
    def render_response_tab(tab, response_content, style_id):
        """Render a response tab with WhatsApp bubble and st.code copy."""
        with tab:
            # WhatsApp-style chat bubble (visual preview)
            st.markdown(
                f'<div class="response-bubble">{response_content}</div>',
                unsafe_allow_html=True
            )
            
            # Copy instruction
            st.markdown(
                '<div class="copy-hint">📋 Klik tombol hijau di <b>pojok kanan atas</b> kotak di bawah untuk menyalin teks</div>',
                unsafe_allow_html=True
            )
            
            # st.code with built-in copy button (guaranteed to work)
            st.code(response_content, language=None)
            
            # Share to WA Button
            encoded_text = urllib.parse.quote(response_content)
            wa_url = f"https://wa.me/?text={encoded_text}"
            
            st.markdown(f"""
            <a href="{wa_url}" target="_blank" class="btn-wa-share">
                <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51a12.8 12.8 0 0 0-.57-.01c-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 0 1-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 0 1-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 0 1 2.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0 0 12.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 0 0 5.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 0 0-3.48-8.413Z"/>
                </svg>
                Bagikan ke WA
            </a>
            """, unsafe_allow_html=True)
    
    render_response_tab(tab1, result.get("balasan_sopan", ""), "sopan")
    render_response_tab(tab2, result.get("balasan_santai", ""), "santai")
    render_response_tab(tab3, result.get("balasan_formal", ""), "formal")

# ─── Footer ──────────────────────────────────────────────────────────────────
# st.markdown("""
# <div class="app-footer">
#     <div class="footer-divider"></div>
#     <div class="footer-content">
#         <span>Made with ❤️ by</span>
#         <a href="https://instagram.com/itsalifanhar" target="_blank" class="footer-ig">📸 @itsalifanhar</a>
#     </div>
#     <div class="footer-powered">
#         <span>🛡️ Adem-Adem Grup &bull; Powered by Gemini AI</span>
#     </div>
# </div>
# """, unsafe_allow_html=True)

# ─── Live Dashboard Counter ───────────────────────────────────────────────────
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("<h4 style='text-align: center; color: #075E54; margin-bottom: 20px; font-weight: 800;'>🌍 Dampak Sosial Adem-Adem Grup</h4>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="🛡️ Grup Diademkan", value="1,200+")

with col2:
    st.metric(label="❌ Hoaks Ditangkal", value="4,500+")

with col3:
    st.metric(label="🤝 Silaturahmi Aman", value="100%")

st.markdown("<p style='text-align: center; color: #666; font-size: 0.8rem; margin-top: 15px;'>*Data simulasi dashboard real-time</p>", unsafe_allow_html=True)

# ─── Footer ───────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align: center; margin-top: 50px; margin-bottom: 20px; font-size: 0.85rem; color: #555;">
    Developed by <a href="https://www.instagram.com/itsalifanhar?igsh=d2YxaGJ2NDJvcTRx" target="_blank" style="color: #075E54; text-decoration: none; font-weight: 800; transition: all 0.3s ease;">Muh. Alif Anhar</a>
</div>
""", unsafe_allow_html=True)
