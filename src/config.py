import os
from dotenv import load_dotenv

# ==========================================
# 1. TEMEL DOSYA YOLU AYARLARI
# ==========================================
src_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(src_dir)
env_path = os.path.join(root_dir, '.env')

# ==========================================
# 2. .ENV YÜKLEME
# ==========================================
if os.path.exists(env_path):
    load_dotenv(dotenv_path=env_path)
else:
    print(f"UYARI: .env dosyası bulunamadı: {env_path}")

# ==========================================
# 3. API VE MODEL AYARLARI (TÜM VARYASYONLAR)
# ==========================================
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError(f"KRİTİK HATA: 'GEMINI_API_KEY' {env_path} içinde bulunamadı!")

# --- API ANAHTARI EŞANLAMLILARI ---
API_ANAHTARI = GEMINI_API_KEY  
API_KEY = GEMINI_API_KEY      

# --- MODEL İSMİ EŞANLAMLILARI ---
MODEL_ISMI = "gemini-2.0-flash" 
MODEL_NAME = MODEL_ISMI 
MODEL = MODEL_ISMI

TEMPERATURE = 0.3

# ==========================================
# 4. VERİTABANI VE DOSYA YOLLARI
# ==========================================
VERITABANI_YOLU = os.path.join(root_dir, 'data', 'istihbarat.db')
DB_PATH = VERITABANI_YOLU

HAM_VERI_YOLU = os.path.join(root_dir, 'data', 'raw')
RAW_DATA_PATH = HAM_VERI_YOLU

# --- VEKTÖR VERİTABANI ---
VEKTOR_DB_KLASORU = os.path.join(root_dir, 'vector_db', 'faiss_indeksi')

# Eşanlamlılar
VEKTOR_DIZINI = VEKTOR_DB_KLASORU
VECTOR_DB_FOLDER = VEKTOR_DB_KLASORU
VEKTOR_KLASORU = VEKTOR_DB_KLASORU

VEKTOR_DB_DOSYASI = os.path.join(VEKTOR_DB_KLASORU, 'faiss.index')
VEKTOR_DOSYASI = VEKTOR_DB_DOSYASI
VECTOR_DB_FILE = VEKTOR_DB_DOSYASI

# ==========================================
# 5. RAG PARAMETRELERİ
# ==========================================
PARCA_BOYUTU = 1000          
CHUNK_SIZE = PARCA_BOYUTU

PARCA_CAKISMA_MIKTARI = 200  
CHUNK_OVERLAP = PARCA_CAKISMA_MIKTARI

EN_IYI_SONUC_SAYISI = 5         
GETIRILECEK_DOKUMAN_SAYISI = EN_IYI_SONUC_SAYISI
TOP_K = EN_IYI_SONUC_SAYISI

# ==========================================
# 6. ANALİZ RAPORU ŞABLONU VE BÖLÜMLERİ
# ==========================================
RAPOR_SABLONU = """
Sen devlet düzeyinde çalışan uzman bir istihbarat analistisin. 
Aşağıda sağlanan "Bağlam" (Context) içerisindeki bilgileri kullanarak, sorulan "Soru"ya (Question) 
net, kanıta dayalı ve profesyonel bir yanıt ver.

--- BAĞLAM BAŞLANGICI ---
{context}
--- BAĞLAM BİTİŞİ ---

Soru: {question}

Yanıtlama Kuralları:
1. Sadece yukarıdaki bağlamda verilen bilgilere dayan.
2. Bilgi yoksa uydurma.
3. Yanıtı maddeler halinde yaz.

Analiz Raporu:
"""

ANALIZ_SABLONU = RAPOR_SABLONU
REPORT_TEMPLATE = RAPOR_SABLONU
PROMPT_SABLONU = RAPOR_SABLONU

# --- HATA VEREN KISIM İÇİN EKLENDİ ---
# analyzer.py içindeki döngü için gerekli liste:
RAPOR_BOLUMLERI = [
    "Yönetici Özeti",
    "Ana Bulgular",
    "Detaylı Analiz",
    "Olası Riskler",
    "Öneriler ve Sonuç"
]