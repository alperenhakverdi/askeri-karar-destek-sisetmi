import os
from dotenv import load_dotenv

# ==========================================
# 1. TEMEL DOSYA YOLU AYARLARI (PATH SETUP)
# ==========================================
# Bu dosya 'src' içinde olduğu için proje ana dizinini bulmak adına bir üst dizine çıkıyoruz.
src_dir = os.path.dirname(os.path.abspath(__file__))  # .../src
root_dir = os.path.dirname(src_dir)                 # .../ (Proje Ana Dizini)
env_path = os.path.join(root_dir, '.env')           # .../.env

# ==========================================
# 2. ORTAM DEĞİŞKENLERİNİ YÜKLEME (.ENV)
# ==========================================
if os.path.exists(env_path):
    load_dotenv(dotenv_path=env_path)
else:
    print(f"UYARI: .env dosyası şu konumda bulunamadı: {env_path}")

# ==========================================
# 3. API VE MODEL AYARLARI
# ==========================================
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Kritik Hata Kontrolü
if not GEMINI_API_KEY:
    raise ValueError(
        f"KRİTİK HATA: 'GEMINI_API_KEY' bulunamadı!\n"
        f"Lütfen '{env_path}' dosyasını kontrol edin ve anahtarın doğru yazıldığından emin olun."
    )

MODEL_NAME = "gemini-1.5-flash"  # Hız ve maliyet için flash, kalite için 'gemini-1.5-pro'
TEMPERATURE = 0.3                # 0: Deterministik (Sabit), 1: Yaratıcı

# ==========================================
# 4. VERİTABANI VE DOSYA YOLU SABİTLERİ
# ==========================================
# SQLite Veritabanı Yolu
DB_PATH = os.path.join(root_dir, 'data', 'istihbarat.db')

# Vektör Veritabanı (FAISS) Yolu
VECTOR_DB_FOLDER = os.path.join(root_dir, 'vector_db', 'faiss_indeksi')
VECTOR_DB_FILE = os.path.join(VECTOR_DB_FOLDER, 'faiss.index')

# Ham Veri Klasörü (PDF, JSON vb. dosyaların olduğu yer)
RAW_DATA_PATH = os.path.join(root_dir, 'data', 'raw')

# ==========================================
# 5. RAG (RETRIEVAL) PARAMETRELERİ
# ==========================================
CHUNK_SIZE = 1000        # Metin kaça karakterlik parçalara bölünecek?
CHUNK_OVERLAP = 200      # Parçalar arasında ne kadar örtüşme olacak? (Bağlam kopmaması için)
TOP_K_RETRIEVAL = 5      # LLM'e gönderilecek en alakalı kaç parça seçilsin?

# ==========================================
# 6. ANALİZ RAPORU ŞABLONU (PROMPT)
# ==========================================
REPORT_TEMPLATE = """
Sen devlet düzeyinde çalışan uzman bir istihbarat analistisin. 
Aşağıda sağlanan "Bağlam" (Context) içerisindeki bilgileri kullanarak, sorulan "Soru"ya (Question) 
net, kanıta dayalı ve profesyonel bir yanıt ver.

--- BAĞLAM BAŞLANGICI ---
{context}
--- BAĞLAM BİTİŞİ ---

Soru: {question}

Yanıtlama Kuralları:
1. Sadece yukarıdaki bağlamda verilen bilgilere dayan. Dışarıdan bilgi uydurma (Halüsinasyon görme).
2. Eğer bağlamda sorunun cevabı yoksa, dürüstçe "Verilen belgelerde bu bilgi bulunmamaktadır." de.
3. Cevabını maddeler halinde (bullet points) yapılandır.
4. Tonun resmi, objektif ve analitik olsun.

Analiz Raporu:
"""