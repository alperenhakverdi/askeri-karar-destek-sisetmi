from google import genai
from src import config

def istemciyiHazirla():
    # Google GenAI istemcisini en guncel SDK yapisina gore baslatir
    return genai.Client(api_key=config.API_ANAHTARI)

def raporPromptuOlustur(sorgu, raporParcalari):
    # Vektor veritabanindan gelen parcalari analiz sablonuyla birlestirir
    baglam = "\n---\n".join(raporParcalari)
    
    sablon = (
        f"KULLANICI ANALIZ TALEBI: {sorgu}\n\n"
        f"ILGILI RAPOR KAYITLARI:\n{baglam}\n\n"
        "GOREV: Verilen kayitlari inceleyerek asagidaki basliklarla raporla:\n"
    )
    
    # Config icinde belirlenen standart rapor bolumlerini ekler
    for bolum in config.RAPOR_BOLUMLERI:
        sablon += f"## {bolum}\n"
        
    return sablon

def analizRaporuUret(sorgu, raporParcalari):
    # Belirlenen en guncel modeli kullanarak analizi tamamlar
    istemci = istemciyiHazirla()
    tamMetin = raporPromptuOlustur(sorgu, raporParcalari)
    
    try:
        # Modeli dogrudan config uzerinden cagirarak uretimi baslatir
        cevap = istemci.models.generate_content(
            model=config.MODEL_ISMI,
            contents=tamMetin
        )
        return cevap.text
    except Exception as hata:
        # API kaynakli hatalari veya kota sorunlarini dondurur
        return f"Analiz uretimi sirasinda teknik bir sorun yasandi: {str(hata)}"