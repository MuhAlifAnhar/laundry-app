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

# Custom CSS for WhatsApp-like aesthetic
st.markdown("""
<style>
    /* Primary Colors: #25D366 (Light Green), #075E54 (Dark Green) */
    .main {
        background-color: #f0f2f5;
        font-family: 'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
    h1, h2, h3 {
        color: #075E54;
        font-weight: 600;
    }
    .stButton>button {
        background-color: #25D366 !important;
        color: white !important;
        font-weight: bold;
        border-radius: 8px;
        border: none;
        padding: 0.5rem 1rem;
        transition: all 0.3s ease;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #128C7E !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transform: translateY(-2px);
    }
    .status-card-hoax {
        background-color: #ffebee;
        border-left: 5px solid #f44336;
        color: #212121;
        padding: 1rem;
        border-radius: 4px;
        margin-bottom: 1rem;
    }
    .status-card-fakta {
        background-color: #e8f5e9;
        border-left: 5px solid #4caf50;
        color: #212121;
        padding: 1rem;
        border-radius: 4px;
        margin-bottom: 1rem;
    }
    .status-card-cek {
        background-color: #fff3e0;
        border-left: 5px solid #ff9800;
        color: #212121;
        padding: 1rem;
        border-radius: 4px;
        margin-bottom: 1rem;
    }
    .stTextArea textarea {
        border-radius: 8px;
        border: 1px solid #ccc;
        padding: 10px;
    }
    .stTextArea textarea:focus {
        border-color: #25D366;
        box-shadow: 0 0 0 1px #25D366;
    }
    .response-box {
        background-color: #ffffff;
        color: #212121;
        border-radius: 8px;
        padding: 15px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        border-left: 4px solid #25D366;
    }
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("<h1 style='text-align: center;'>🛡️ Adem-Adem Grup</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #666; font-size: 1.1em;'>Luruskan info, tetap jaga silaturahmi.</p>", unsafe_allow_html=True)
st.markdown("---")

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

Buatkan 3 pilihan balasan chat:
1. 'Sopan': Gunakan kata ganti yang hormat (Bapak/Ibu/Om/Tante), awali dengan maaf, sampaikan fakta dengan lembut. Sangat cocok untuk membalas orang tua/sesepuh tanpa menggurui.
2. 'Santai': Gunakan bahasa gaul/asik, tanpa kesan menggurui. Cocok untuk sepupu atau teman sebaya.
3. 'Formal': Gunakan bahasa baku yang netral. Cocok untuk grup RT atau lingkungan.

Format output HARUS JSON dengan struktur persis seperti ini:
{
    "status": "Hoaks" | "Fakta" | "Perlu Cek Lagi",
    "penjelasan": "Penjelasan singkat 1-2 kalimat.",
    "balasan_sopan": "Teks balasan sopan...",
    "balasan_santai": "Teks balasan santai...",
    "balasan_formal": "Teks balasan formal..."
}
Pastikan hanya mengembalikan JSON mentah yang valid, tanpa markdown tambahan seperti ```json.
"""

# Input Area
user_input = st.text_area("Paste pesan dari grup WA di sini...", height=150, placeholder="Misal: Besok pom bensin tutup semua karena ada demo besar-besaran, isi full sekarang!")

# Action Button
if st.button("Vibe-Check Sekarang!", use_container_width=True):
    if not user_input.strip():
        st.error("Pesan tidak boleh kosong!")
    else:
        with st.spinner("Menganalisis pesan dengan Vibe-Logic..."):
            try:
                # Combine system instruction and user input to avoid config schema issues in v1
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
                
                # Parse JSON
                try:
                    result = json.loads(response_text)
                except json.JSONDecodeError:
                    st.error("Gagal membaca hasil dari AI. AI mengembalikan format yang tidak valid.")
                    st.stop()
                
                # Display Results
                st.markdown("### Hasil Analisis")
                
                status = result.get("status", "Perlu Cek Lagi")
                penjelasan = result.get("penjelasan", "Tidak ada penjelasan.")
                
                # Status Card
                if "Hoaks" in status:
                    st.markdown(f'<div class="status-card-hoax"><strong>❌ HOAKS DETECTED</strong><br/>{penjelasan}</div>', unsafe_allow_html=True)
                elif "Fakta" in status:
                    st.markdown(f'<div class="status-card-fakta"><strong>✅ FAKTA</strong><br/>{penjelasan}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="status-card-cek"><strong>⚠️ PERLU CEK LAGI</strong><br/>{penjelasan}</div>', unsafe_allow_html=True)
                
                # Tabs for Responses
                st.markdown("### Pilih Gaya Balasan")
                tab1, tab2, tab3 = st.tabs(["🙏 Gaya Anak Berbakti (Sopan)", "😎 Gaya Sepupu Asik (Santai)", "👔 Gaya Warga Bijak (Formal)"])
                
                with tab1:
                    st.markdown('<div class="response-box">' + result.get("balasan_sopan", "") + '</div>', unsafe_allow_html=True)
                    st.markdown("<div style='margin-top: 10px; font-size: 0.9em; color: #555;'>💡 <b>Mau disalin?</b> Arahkan kursor ke area abu-abu di bawah, lalu klik ikon 📋 di pojok kanan atas:</div>", unsafe_allow_html=True)
                    st.code(result.get("balasan_sopan", ""), language="text")
                
                with tab2:
                    st.markdown('<div class="response-box">' + result.get("balasan_santai", "") + '</div>', unsafe_allow_html=True)
                    st.markdown("<div style='margin-top: 10px; font-size: 0.9em; color: #555;'>💡 <b>Mau disalin?</b> Arahkan kursor ke area abu-abu di bawah, lalu klik ikon 📋 di pojok kanan atas:</div>", unsafe_allow_html=True)
                    st.code(result.get("balasan_santai", ""), language="text")
                    
                with tab3:
                    st.markdown('<div class="response-box">' + result.get("balasan_formal", "") + '</div>', unsafe_allow_html=True)
                    st.markdown("<div style='margin-top: 10px; font-size: 0.9em; color: #555;'>💡 <b>Mau disalin?</b> Arahkan kursor ke area abu-abu di bawah, lalu klik ikon 📋 di pojok kanan atas:</div>", unsafe_allow_html=True)
                    st.code(result.get("balasan_formal", ""), language="text")
                    
            except Exception as e:
                st.error(f"Terjadi kesalahan saat menghubungi API: {str(e)}")
