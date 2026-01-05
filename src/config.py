import os
from dotenv import load_dotenv

# .env dosyasindaki degiskenleri yukler
load_dotenv()

# --- API Yapilandirmasi ---
API_ANAHTARI = os.getenv("GEMINI_API_KEY")
MODEL_ISMI = "gemini-3-flash-preview"

# --- Klasor ve Dosya Yollari ---
# Proje ana dizinini belirler
ANA_DIZIN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Veri ve veritabani yollari
HAM_VERI_YOLU = os.path.join(ANA_DIZIN, "data", "raw", "raporlar.json")
# Yeni SQLite veritabani yolu eklendi
VERITABANI_YOLU = os.path.join(ANA_DIZIN, "data", "istihbarat.db")
VEKTOR_DIZINI = os.path.join(ANA_DIZIN, "vector_db", "faiss_indeksi")

# --- RAG Parametreleri ---
PARCA_BOYUTU = 500
PARCA_CAKISMA_MIKTARI = 50
EN_IYI_SONUC_SAYISI = 3

# --- Analiz Raporu Sablonu ---
RAPOR_BOLUMLERI = [
    "Durum Ozeti",
    "Mevcut Durum Analizi",
    "Stratejik Planlama Senaryolari",
    "Yanlilik ve Bilgi Bosluklari",
    "Belirsizlik ve Guven Notu"
]