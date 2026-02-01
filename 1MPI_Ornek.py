# MPI ile Proses Tabanlı Paralelleştirme (Process-Based Parallelism)
import random
import time
from mpi4py import MPI

# Aranacak olan spesifik dizilim ve uzunluğu global olarak tanımlanıyor
ARANAN_DIZILIM = "ACTAGATG"
ARANAN_UZUNLUK = len(ARANAN_DIZILIM)
TOPLAM_DIZI_UZUNLUGU = 200_000_000

def sayim_ve_kesisimleri_hesapla_mpi(chunk_uzunlugu, seed):
    random.seed(seed)
    
    bazlar = ['A', 'T', 'G', 'C']
    kesisim_alani_uzunlugu = ARANAN_UZUNLUK - 1
    
    # 1. Ana chunk'ı oluştur
    ana_chunk = "".join(random.choice(bazlar) for _ in range(chunk_uzunlugu))
    
    # 2. Bir sonraki chunk'ın başlangıcını simüle eden rastgele kesişim alanını oluştur
    #    (Orijinal kodun "kesişim kontrolü" simülasyon mantığını korumak için)
    kesisim_alani = "".join(random.choice(bazlar) for _ in range(kesisim_alani_uzunlugu))
    
    # 3. Ana chunk ve kesişim alanını birleştirerek tara
    toplam_sayim = (ana_chunk + kesisim_alani).count(ARANAN_DIZILIM)
    
    return toplam_sayim


if __name__ == '__main__':
    # MPI evrenini başlat
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()  # Prosesin kimlik numarası (0'dan başlar)
    size = comm.Get_size()  # Toplam proses sayısı
    
    if rank == 0:
        # Ana Proses (Master - Rank 0)
        
        # 1. İş dağılımını hesapla
        cekirdek_sayisi = size
        parca_uzunlugu = TOPLAM_DIZI_UZUNLUGU // cekirdek_sayisi
        
        # Her bir prosesin iş yükü (uzunluk, seed)
        gorevler = [(parca_uzunlugu, i) for i in range(cekirdek_sayisi)]
        
        # Kalan kısmı son göreve ekle
        kalan_uzunluk = TOPLAM_DIZI_UZUNLUGU % cekirdek_sayisi
        if kalan_uzunluk > 0:
            # Son gorev (size - 1) ise son prosesin iş yükünü güncelle
            son_gorev_uzunlugu = gorevler[size - 1][0] + kalan_uzunluk
            gorevler[size - 1] = (son_gorev_uzunlugu, size - 1)
        
        print(f"Hesaplama icin {size} MPI prosesi kullaniliyor...")
        print(f"Toplam {TOPLAM_DIZI_UZUNLUGU} elemanli dizi, {size} parcaya bolundu.")
        print("-" * 40)
        
        baslangic_zamani = time.time()
        
        # Her bir prosesin alacağı iş yükünü ayır (Dağıtık bellek mantığı)
        # Rank 0 kendi görevini kendisi yapar
        my_chunk_params = gorevler[0]
        
        # Diğer proseslere işlerini gönder (Görev dağıtımı)
        for i in range(1, size):
            comm.send(gorevler[i], dest=i, tag=11)
            
        # Kendi görevini yap
        kendi_sonuc = sayim_ve_kesisimleri_hesapla_mpi(my_chunk_params[0], my_chunk_params[1])
        
        # Diğer proseslerden sonuçları topla (Toplama)
        sonuc_listesi = [kendi_sonuc]
        for i in range(1, size):
            # i. prosesin sonucunu bekle ve al
            sonuc = comm.recv(source=i, tag=22)
            sonuc_listesi.append(sonuc)
            
        # Tüm sonuçları topla ve yazdır
        toplam_bulunan = sum(sonuc_listesi)
        bitis_zamani = time.time()
        
        print(f"Olusturulan Ornek Genetik Dizinin Uzunlugu: {TOPLAM_DIZI_UZUNLUGU}")
        print(f"Aranan Dizilim: '{ARANAN_DIZILIM}'")
        print(f"'{ARANAN_DIZILIM}' dizilimi, ornek dizi icinde yaklasik {toplam_bulunan} kez bulundu.")
        print("-" * 40)
        print(f"Yuzde {toplam_bulunan / 1500000:.4f}'dir.")
        print(f"Islem {bitis_zamani - baslangic_zamani:.2f} saniyede tamamlandi.")

    else:
        # İşçi Prosesler (Worker - Rank > 0)
        
        # Ana Prosesten görevi al
        chunk_params = comm.recv(source=0, tag=11)
        
        # Görevi yap
        bulunan_sayisi = sayim_ve_kesisimleri_hesapla_mpi(chunk_params[0], chunk_params[1])
        
        # Sonucu Ana Proseşe gönder
        comm.send(bulunan_sayisi, dest=0, tag=22)