# 🧬 MPI ile Paralel DNA Dizilimi Analizi

Python ve `mpi4py` kullanarak 200 milyon elemanlı bir DNA dizisi içinde belirli bir genetik kodun (`ACTAGATG`) aranmasını simüle eden paralel hesaplama projesi.

---

## Proje Hakkında

Uygulama, rastgele oluşturulmuş 200.000.000 elemanlı bir DNA dizisini (A, T, G, C) analiz eder. İş yükünü tek bir işlemci yerine MPI protokolü aracılığıyla birden fazla çekirdeğe dağıtarak arama süresini minimize eder.

---

## Çalışma Mantığı — Master-Worker Modeli

| Aşama | Açıklama |
|---|---|
| **Dağıtım (Scatter)** | Rank 0 (Ana Proses), veriyi işlemci sayısına böler; her worker'a chunk boyutunu ve seed değerini bildirir |
| **İşleme (Processing)** | Her proses kendi chunk'ını bellekte oluşturur ve `ACTAGATG` dizilimini kendi parçasında sayar |
| **Kesişim Kontrolü** | Dizilimin parça sınırında bölünmesini önlemek için parçalar arası örtüşme (overlap) alanları hesaba katılır |
| **Toplama (Gather/Reduce)** | Worker'lar sonuçlarını Ana Proses'e gönderir; Rank 0 tüm sonuçları toplar ve toplam süreyi hesaplar |

---

## Kurulum

### 1. MPI

İşletim sisteminize göre bir MPI implementasyonu yükleyin:

- **Windows** — [Microsoft MPI (MS-MPI)](https://learn.microsoft.com/en-us/message-passing-interface/microsoft-mpi)
- **Linux / macOS** — OpenMPI veya MPICH

### 2. Python Kütüphanesi

```bash
pip install mpi4py
```

---

## Kullanım

Kodu doğrudan `python` ile değil, MPI ortamını başlatan `mpiexec` komutuyla çalıştırın:

```bash
mpiexec -n 4 python 1MPI_Ornek.py
```

`-n` parametresini değiştirerek kullanılacak çekirdek sayısını ayarlayabilirsiniz (örn. `-n 8`).

---

## Örnek Çıktı

```
Hesaplama icin 4 MPI prosesi kullaniliyor...
Toplam 200000000 elemanli dizi, 4 parcaya bolundu.

Olusturulan Ornek Genetik Dizinin Uzunlugu: 200000000

Aranan Dizilim: 'ACTAGATG'

'ACTAGATG' dizilimi, ornek dizi icinde yaklasik 3052 kez bulundu.

Yuzde 0.0020'dir.

Islem 3.42 saniyede tamamlandi.
```
