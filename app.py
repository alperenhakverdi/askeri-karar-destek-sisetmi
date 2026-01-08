import streamlit as st
import pandas as pd
import sqlite3
import os
from src import config, loader, vector_store, analyzer

def sayfayiYapilandir():
    # Sayfa basligi ve yerlesim ayarlarini yapar
    st.set_page_config(page_title="Karar Destek Sistemi", layout="wide")
    st.title("🛡️ Sınır Güvenliği Karar Destek Sistemi")
    
    st.sidebar.title("Sistem Bilgileri")
    # Config dosyasindaki guncel model ismini gosterir
    st.sidebar.success(f"Model: {config.MODEL_ISMI}")
    st.sidebar.info("Veri Kaynağı: SQLite Veritabanı (İstihbarat)")
    
    # Raporun için ekran görüntüsü alırken güzel dursun diye versiyon ekledik
    st.sidebar.markdown("---")
    st.sidebar.caption("Versiyon: 2.0 (Tez Çalışması)")

def verileriBaslat():
    # Uygulama acilisinda veritabani kontrolu ve yukleme islemleri
    
    # 1. Veritabani tablolarini olustur
    loader.veritabaniHazirla()
    
    # 2. Eger varsa raporlar.json icindeki verileri veritabanina aktar
    loader.jsonVerisiniAktar()
    
    # 3. Verileri artik dogrudan veritabanindan yukle
    hamRaporlar = loader.verileriYukle()
    islenmisVeriler = loader.raporlariHazirla(hamRaporlar)
    
    # 4. Mevcut vektor indeksini yukle, yoksa yeniden olustur
    indeks = vector_store.indeksiYukle()
    
    if indeks is None:
        st.toast("Vektör indeksi oluşturuluyor...")
        indeks = vector_store.vektorIndeksiOlustur(islenmisVeriler)
        vector_store.indeksiKaydet(indeks)
        
    return indeks, islenmisVeriler

def anaAkis():
    sayfayiYapilandir()
    
    # Oturum bazli veri saklama (Session State)
    if "verilerHazirMi" not in st.session_state:
        with st.spinner("Sistem veritabanına bağlanıyor ve veriler işleniyor..."):
            indeks, islenmisVeriler = verileriBaslat()
            st.session_state.indeks = indeks
            st.session_state.islenmisVeriler = islenmisVeriler
            st.session_state.verilerHazirMi = True

    # --- SEKMELİ YAPIYA GEÇİŞ (Tabs) ---
    # Raporundaki Şekil 4.1 ve Şekil 4.2 için gerekli alanlar
    tab1, tab2 = st.tabs(["📊 Analiz Ekranı", "🗄️ Veritabanı Kayıtları"])

    # ---------------------------------------------------------
    # 1. SEKME: ANALİZ EKRANI (Senin eski kodun buraya taşındı)
    # ---------------------------------------------------------
    with tab1:
        st.subheader("İstihbarat Analiz Modülü")
        st.markdown("Aşağıdaki alana sahadan gelen emareleri veya şüphelerinizi giriniz.")
        
        sorguMesaji = "Sorgunuzu Giriniz:"
        sorguGirdisi = st.text_input(sorguMesaji, placeholder="Örneğin: Vadi tabanındaki hareketlilik ile beyaz pikap arasında bağ var mı?")

        if st.button("Analizi Başlat") and sorguGirdisi:
            with st.spinner(f"Raporlar taranıyor ve {config.MODEL_ISMI} ile analiz ediliyor..."):
                
                # 1. Benzerlik aramasi ile ilgili rapor parcalarini getir
                ilgiliParcalar = vector_store.ilgiliParcalariGetir(
                    sorguGirdisi, 
                    st.session_state.indeks, 
                    st.session_state.islenmisVeriler
                )
                
                # 2. Gemini API ile nihai analiz raporunu uret
                analizSonucu = analyzer.analizRaporuUret(sorguGirdisi, ilgiliParcalar)
                
                # 3. Sonuclari ekrana yazdir
                st.markdown("### 📝 Analiz Sonucu")
                st.info(analizSonucu)
                
                # Alt kisimda referans alinan raporlari goster
                with st.expander("🔍 Analizde Kullanılan Kaynak Rapor Parçaları"):
                    if not ilgiliParcalar:
                        st.warning("Veritabanında ilgili kayıt bulunamadı.")
                    else:
                        for parca in ilgiliParcalar:
                            st.text(f"• {parca}")

    # ---------------------------------------------------------
    # 2. SEKME: VERİTABANI GÖRÜNTÜLEME (Şekil 4.2 İçin Yeni Kısım)
    # ---------------------------------------------------------
    with tab2:
        st.subheader("Sistemdeki Ham İstihbarat Raporları")
        st.markdown("SQLite veritabanına (`istihbarat.db`) kaydedilmiş tüm ham veriler aşağıdadır.")
        
        # Config dosyasından veya varsayılan yoldan veritabanı yolunu al
        db_yolu = getattr(config, 'VERITABANI_YOLU', os.path.join("data", "istihbarat.db"))
        
        if os.path.exists(db_yolu):
            try:
                # Veritabanına bağlan ve verileri çek
                conn = sqlite3.connect(db_yolu)
                df = pd.read_sql_query("SELECT * FROM raporlar", conn)
                conn.close()
                
                # Veriyi tablo olarak göster
                st.dataframe(df, use_container_width=True)
                st.caption(f"Toplam Kayıt Sayısı: {len(df)}")
            except Exception as e:
                st.error(f"Veritabanı okuma hatası: {e}")
        else:
            st.warning("Henüz veritabanı dosyası oluşturulmamış.")

if __name__ == "__main__":
    anaAkis()