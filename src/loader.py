import json
import sqlite3
import os
from src import config

def veritabaniHazirla():
    """
    SQLite veritabanini ve raporlar tablosunu olusturur.
    Eger tablo zaten varsa islem yapmaz.
    """
    baglanti = sqlite3.connect(config.VERITABANI_YOLU)
    imlec = baglanti.cursor()
    
    # JSON yapisindaki tum alanlari kapsayan tablo semasi
    imlec.execute('''
        CREATE TABLE IF NOT EXISTS raporlar (
            id TEXT PRIMARY KEY,
            kaynak TEXT,
            baslik TEXT,
            zaman TEXT,
            metin TEXT,
            guvenilirlik TEXT
        )
    ''')
    
    baglanti.commit()
    baglanti.close()

def jsonVerisiniAktar():
    """
    Mevcut JSON dosyasindaki verileri okur ve veritabanina aktarir.
    Daha once eklenen kayitlari (ID cakismazsa) tekrar eklemez.
    """
    if not os.path.exists(config.HAM_VERI_YOLU):
        print(f"Uyari: {config.HAM_VERI_YOLU} bulunamadi, aktarim atlandi.")
        return

    try:
        with open(config.HAM_VERI_YOLU, "r", encoding="utf-8") as dosya:
            veriler = json.load(dosya)
            
        baglanti = sqlite3.connect(config.VERITABANI_YOLU)
        imlec = baglanti.cursor()
        
        eklenenSayisi = 0
        for rapor in veriler:
            # JSON keys: id, kaynak, baslik, zaman, metin, guvenilirlik
            # Eksik anahtar ihtimaline karsi .get() kullanilir
            imlec.execute('''
                INSERT OR IGNORE INTO raporlar (id, kaynak, baslik, zaman, metin, guvenilirlik)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                rapor.get('id'),
                rapor.get('kaynak'),
                rapor.get('baslik'),
                rapor.get('zaman'),
                rapor.get('metin'),
                rapor.get('guvenilirlik')
            ))
            if imlec.rowcount > 0:
                eklenenSayisi += 1
                
        baglanti.commit()
        baglanti.close()
        
        if eklenenSayisi > 0:
            print(f"{eklenenSayisi} adet rapor veritabanina basariyla aktarildi.")
            
    except Exception as hata:
        print(f"Veri aktarimi sirasinda hata: {str(hata)}")

def verileriYukle():
    """
    Veritabanindaki tum raporlari okur ve liste formatinda dondurur.
    Cikti formati eski JSON yapisiyla aynidir, boylece diger fonksiyonlar bozulmaz.
    """
    if not os.path.exists(config.VERITABANI_YOLU):
        return []

    baglanti = sqlite3.connect(config.VERITABANI_YOLU)
    imlec = baglanti.cursor()
    
    imlec.execute('SELECT id, kaynak, baslik, zaman, metin, guvenilirlik FROM raporlar')
    satirlar = imlec.fetchall()
    baglanti.close()
    
    raporListesi = []
    for satir in satirlar:
        raporListesi.append({
            "id": satir[0],
            "kaynak": satir[1],
            "baslik": satir[2],
            "zaman": satir[3],
            "metin": satir[4],
            "guvenilirlik": satir[5]
        })
        
    return raporListesi

def metniParcala(metin):
    """
    Metni, config dosyasindaki boyut ve cakisma miktarina gore boler.
    Bu islem, LLM'in baglami (context) kaybetmeden veriyi islemesini saglar.
    """
    parcalar = []
    adim = config.PARCA_BOYUTU - config.PARCA_CAKISMA_MIKTARI
    
    # Eger metin cok kisaysa tek parca olarak dondur
    if len(metin) <= config.PARCA_BOYUTU:
        return [metin]
    
    for i in range(0, len(metin), adim):
        parca = metin[i : i + config.PARCA_BOYUTU]
        parcalar.append(parca)
        
    return parcalar

def raporlariHazirla(raporListesi):
    """
    Veritabanindan gelen raporlari RAG yapisina uygun, parcalanmis listeye donusturur.
    Kaynak ve baslik bilgilerini metne ekleyerek arama (retrieval) kalitesini artirir.
    """
    islenmisVeriler = []
    
    for rapor in raporListesi:
        # LLM'e gidecek zenginlestirilmis metin blogu
        zenginMetin = (
            f"KAYNAK: {rapor['kaynak']} | "
            f"BASLIK: {rapor['baslik']} | "
            f"ZAMAN: {rapor['zaman']} | "
            f"ICERIK: {rapor['metin']}"
        )
        
        parcalar = metniParcala(zenginMetin)
        
        for p in parcalar:
            islenmisVeriler.append({
                "raporId": rapor["id"],
                "metinParcasi": p,
                "guvenilirlik": rapor["guvenilirlik"]
            })
            
    return islenmisVeriler