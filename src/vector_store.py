import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from src import config

# Embedding modeli performans icin bir kez yuklenir
_embeddingModeli = SentenceTransformer('all-MiniLM-L6-v2')

def embeddingUret(metinListesi):
    # Metinleri sayisal vektorlere donusturur
    return _embeddingModeli.encode(metinListesi)

def vektorIndeksiOlustur(islenmisVeriler):
    # Metin parcalarindan FAISS indeksi olusturur
    metinler = [veri["metinParcasi"] for veri in islenmisVeriler]
    vektorler = embeddingUret(metinler)
    
    boyut = vektorler.shape[1]
    indeks = faiss.IndexFlatL2(boyut)
    indeks.add(vektorler.astype('float32'))
    
    return indeks

def indeksiKaydet(indeks):
    # Olusturulan indeksi belirlenen dizine kaydeder
    if not os.path.exists(config.VEKTOR_DIZINI):
        os.makedirs(config.VEKTOR_DIZINI)
    
    dosyaYolu = os.path.join(config.VEKTOR_DIZINI, "faiss.index")
    faiss.write_index(indeks, dosyaYolu)

def indeksiYukle():
    # Kayitli indeksi diskten yukler
    dosyaYolu = os.path.join(config.VEKTOR_DIZINI, "faiss.index")
    if os.path.exists(dosyaYolu):
        return faiss.read_index(dosyaYolu)
    return None

def ilgiliParcalariGetir(sorgu, indeks, islenmisVeriler):
    # Sorguya en yakin metin parcalarini dondurur
    sorguVektoru = embeddingUret([sorgu]).astype('float32')
    mesafeler, indisler = indeks.search(sorguVektoru, config.EN_IYI_SONUC_SAYISI)
    
    enAlakaliParcalar = []
    for i in indisler[0]:
        if i != -1:
            enAlakaliParcalar.append(islenmisVeriler[i]["metinParcasi"])
            
    return enAlakaliParcalar