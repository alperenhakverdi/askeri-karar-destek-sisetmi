import streamlit as st
from src import config, loader, vector_store, analyzer

def sayfayiYapilandir():
    # Sayfa basligi ve yerlesim ayarlarini yapar
    st.set_page_config(page_title="Karar Destek Sistemi", layout="wide")
    st.title("🛡️ Sinir Guvenligi Karar Destek Sistemi")
    
    st.sidebar.title("Sistem Bilgileri")
    # Config dosyasindaki guncel model ismini gosterir
    st.sidebar.success(f"Model: {config.MODEL_ISMI}")
    st.sidebar.info("Veri Kaynagi: SQLite Veritabani (Istihbarat)")

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
    
    # Eger indeks yoksa veya veri sayisi degistiyse (basit kontrol) yeniden olusturulabilir
    # Not: Daha gelismis versiyonda indeks guncelleme mantigi eklenebilir
    if indeks is None:
        st.toast("Vektor indeksi olusturuluyor...")
        indeks = vector_store.vektorIndeksiOlustur(islenmisVeriler)
        vector_store.indeksiKaydet(indeks)
        
    return indeks, islenmisVeriler

def anaAkis():
    sayfayiYapilandir()
    
    # Oturum bazli veri saklama (Session State)
    if "verilerHazirMi" not in st.session_state:
        with st.spinner("Sistem veritabanina baglaniyor ve veriler isleniyor..."):
            indeks, islenmisVeriler = verileriBaslat()
            st.session_state.indeks = indeks
            st.session_state.islenmisVeriler = islenmisVeriler
            st.session_state.verilerHazirMi = True

    # Kullanici arayuzu bilesenleri
    sorguMesaji = "Analiz edilmesini istediginiz durumu veya soruyu giriniz:"
    sorguGirdisi = st.text_input(sorguMesaji, placeholder="Ornegin: Vadi tabanindaki hareketlilik ile beyaz pikap arasinda bag var mi?")

    if st.button("Analizi Baslat") and sorguGirdisi:
        with st.spinner(f"Raporlar veritabaninda taraniyor ve {config.MODEL_ISMI} tarafindan analiz ediliyor..."):
            
            # 1. Benzerlik aramasi ile ilgili rapor parcalarini getir
            ilgiliParcalar = vector_store.ilgiliParcalariGetir(
                sorguGirdisi, 
                st.session_state.indeks, 
                st.session_state.islenmisVeriler
            )
            
            # 2. Gemini API ile nihai analiz raporunu uret
            analizSonucu = analyzer.analizRaporuUret(sorguGirdisi, ilgiliParcalar)
            
            # 3. Sonuclari ekrana yazdir
            st.markdown("---")
            st.markdown(analizSonucu)
            
            # Alt kisimda referans alinan raporlari goster
            with st.expander("🔍 Analizde Kullanilan Kaynak Rapor Parcalari"):
                if not ilgiliParcalar:
                    st.warning("Veritabaninda ilgili kayit bulunamadi.")
                else:
                    for parca in ilgiliParcalar:
                        st.info(parca)

if __name__ == "__main__":
    anaAkis()