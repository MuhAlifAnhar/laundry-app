import streamlit as st
from google import genai
from google.genai import types
import os
import json
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

    /* ── Tab text inside tab buttons ── */
    .stTabs [data-baseweb="tab"] *,
    .stTabs [data-baseweb="tab"] p,
    .stTabs [data-baseweb="tab"] span {
        color: inherit !important;
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
        with st.spinner("🧠 Menganalisis pesan dengan Vibe-Logic..."):
            try:
                # Combine system instruction and user input to avoid config schema issues
                prompt = f"{SYSTEM_INSTRUCTION}\n\nPESAN WA UNTUK DIANALISIS:\n{user_input}"
                
                # Use Gemini 2.5 Flash based on available models
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=prompt
                )
                
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
                    st.error("Gagal membaca hasil dari AI. AI mengembalikan format yang tidak valid.")
                    st.session_state.analysis_result = None
                    
            except Exception as e:
                st.error(f"Terjadi kesalahan saat menghubungi API: {str(e)}")
                st.session_state.analysis_result = None

# ─── Display Results (persisted via session_state) ───────────────────────────
if st.session_state.analysis_result is not None:
    result = st.session_state.analysis_result
    
    st.markdown("---")
    st.markdown("### 📊 Hasil Analisis")
    
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
    
    render_response_tab(tab1, result.get("balasan_sopan", ""), "sopan")
    render_response_tab(tab2, result.get("balasan_santai", ""), "santai")
    render_response_tab(tab3, result.get("balasan_formal", ""), "formal")
