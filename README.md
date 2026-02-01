
# 🧬MPI ile Paralel DNA Dizilimi Analizi


Bu proje, Python ve mpi4py kütüphanesini kullanarak büyük ölçekli bir DNA dizilimi içerisinde spesifik bir genetik kodun (ACTAGATG) aranmasını simüle eder. İşlemi hızlandırmak için Proses Tabanlı Paralelleştirme (Process-Based Parallelism) kullanılmıştır.



## 🚀 Proje Hakkında

Bu uygulama, toplamda 200.000.000 elemanlı rastgele oluşturulmuş bir DNA dizisini (A, T, G, C) analiz eder. Tek bir işlemci yerine, MPI protokolü ile iş yükünü birden fazla işlemci çekirdeğine (Core) dağıtarak arama süresini minimize etmeyi amaçlar.

#### Çalışma Mantığı (Master-Worker Modeli)

Dağıtım (Scatter): Rank 0 (Ana Proses), toplam veri uzunluğunu mevcut işlemci sayısına böler ve her bir "işçi" prosese ne kadar veri üreteceğini ve hangi seed değerini kullanacağını bildirir.

İşleme (Processing): Her bir proses (Worker), kendisine atanan parçayı (Chunk) bellekte oluşturur ve aranan dizilimi (ACTAGATG) kendi parçasında sayar.

Kesişim Kontrolü: Veri parçalara bölündüğünde, aranan kelimenin tam sınırda kalıp bölünmesini engellemek için kod, parçalar arası "kesişim alanlarını" (overlap) da hesaba katar.

Toplama (Gather/Reduce): İşçiler buldukları sonuçları Ana Prosese gönderir. Rank 0, tüm sonuçları toplar ve toplam süreyi hesaplar.

### 🛠 Kurulum ve Gereksinimler
Bu projeyi çalıştırmak için bilgisayarınızda bir MPI implementasyonu ve ilgili Python kütüphanesi yüklü olmalıdır.
1. MPI Yüklemesi

Windows için: Microsoft MPI (MS-MPI) yüklemeniz gerekir.

Linux/macOS için: OpenMPI veya MPICH kullanabilirsiniz.

2. Python Kütüphanesi

Gerekli Python kütüphanesini yükleyin:
   
    pip install mpi4py

3. ▶️ Kullanım
Kodu doğrudan python komutu ile çalıştırmak yerine, MPI ortamını başlatan mpiexec veya mpirun komutunu kullanmalısınız.

Örneğin, kodu 4 çekirdek üzerinde çalıştırmak için terminale şu komutu girin:
   
    mpiexec -n 4 python 1MPI_Ornek.py

Eğer işlemci sayısını değiştirmek isterseniz -n parametresinden sonraki sayıyı (örn: 8) değiştirebilirsiniz.

4. 📊 Örnek Çıktı
   
Program başarıyla çalıştığında aşağıdakine benzer bir çıktı verecektir:

    Hesaplama icin 4 MPI prosesi kullaniliyor...
    Toplam 200000000 elemanli dizi, 4 parcaya bolundu.
    
    Olusturulan Ornek Genetik Dizinin Uzunlugu: 200000000
   
    Aranan Dizilim: 'ACTAGATG'
   
    'ACTAGATG' dizilimi, ornek dizi icinde yaklasik 3052 kez bulundu.
   
    Yuzde 0.0020'dir.
   
    Islem 3.42 saniyede tamamlandi.
