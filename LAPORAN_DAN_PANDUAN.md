# LAPORAN TUGAS BESAR KOMPUTASI CLOUD
## Distributed Image Resizer API

**Nama Proyek:** Distributed Image Resizer API
**Teknologi:** Docker, Flask (Python), Redis, Pillow

---

## 1. Latar Belakang & Deskripsi Proyek
Proyek ini adalah sistem pemrosesan gambar terdistribusi yang dirancang untuk menangani beban tinggi secara skalabel. Sistem ini memungkinkan pengguna mengunggah gambar, yang kemudian akan diproses (di-resize) oleh sekumpulan "Worker" di latar belakang.

Masalah yang diselesaikan:
*   Jika pemrosesan dilakukan langsung di API server, server akan berat dan lambat merespons jika banyak user upload bersamaan.
*   Dengan arsitektur ini, API server hanya menerima file, sedangkan pemrosesan berat dilakukan oleh Worker terpisah.

## 2. Arsitektur Sistem
Sistem dibangun menggunakan **Microservices Architecture** berbasis container Docker:

1.  **API Service (Port 5000)**
    *   Dibuat dengan Python Flask.
    *   Tugas: Menerima upload gambar dari user, validasi file, simpan file asli, dan kirim tugas (job) ke antrian.
    *   Stateless: Tidak menyimpan status pemrosesan, siap menerima request kapan saja.
    
2.  **Message Queue (Redis)**
    *   Bertindak sebagai perantara (broker).
    *   Menampung daftar pekerjaan (queue) yang dikirim API.
    *   Menjamin tugas tidak hilang sebelum diambil worker.

3.  **Worker Service (3 Replicas)**
    *   Program Python yang berjalan di background.
    *   Tugas: Selalu memantau Redis. Jika ada tugas, ambil gambar, resize jadi 300x300 pixel, simpan hasilnya.
    *   **Scalable**: Kita menjalankan 3 worker sekaligus untuk mempercepat kerja secara paralel.

4.  **Shared Storage (Volume)**
    *   Folder bersama yang bisa diakses API dan semua Worker.
    *   `storage/uploads`: Tempat API taruh file asli.
    *   `storage/processed`: Tempat Worker taruh hasil resize.

---

## 3. PANDUAN DEMO (Langkah-langkah Ujian)

Ikuti langkah ini saat presentasi atau demo di depan dosen:

### Persiapan (Sebelum Demo Dimulai)
1.  Pastikan **Docker Desktop** sudah jalan.
2.  Buka aplikasi **Terminal** (CMD atau Powershell) di folder proyek ini.
3.  Pastikan tidak ada container lama yang nyangkut (opsional):
    `docker-compose down`

### Langkah 1: Menjalankan Aplikasi
Jelaskan bahwa Anda akan menyalakan sistem dengan satu perintah orkestrasi.

**Perintah:**
```bash
docker-compose up -d --build
```
*Tunggu sampai semua status "Started" atau "Running".*

### Langkah 2: Membuktikan Skalabilitas (3 Worker)
Tunjukkan bahwa sistem Anda punya 3 pekerja yang siap lembur bersamaan.

**Perintah:**
```bash
docker-compose ps
```
**Tunjukkan di layar:** Lihat ada `worker-1`, `worker-2`, `worker-3` yang statusnya "Up".

### Langkah 3: Demo Upload Lewat Web (User Experience)
Tunjukkan bahwa aplikasi mudah digunakan.

1.  Buka Browser (Chrome/Edge).
2.  Ketik: `http://localhost:5000`
3.  Pilih file gambar (siapkan 1 gambar contoh, misal `test_image.jpg`).
4.  Klik **Upload**.
5.  Perlihatkan pesan "Success Job ID ... "
6.  Buka folder `storage/processed` di Windows Explorer Anda, tunjukkan gambarnya sudah ada di situ.

### Langkah 4: Demo Load Test (Stress Test 10 Foto)
Ini bagian paling keren. Anda akan menunjukkan bagaimana 3 worker berebut mengerjakan 10 tugas sekaligus.

1.  Buka **Terminal Baru** (biarkan terminal lama tetap ada).
2.  Di terminal baru ini, kita akan melihat **LOG kerja Worker** secara live.
    **Perintah:**
    ```bash
    docker-compose logs -f worker
    ```
    *(Biarkan terminal ini terbuka, ini akan jadi layar pemantauan worker)*

3.  Kembali ke **Terminal Pertama**, jalankan script load test yang sudah disiapkan. Script ini otomatis mengirim 10 upload secepat kilat.
    **Perintah:**
    ```bash
    python load_test.py
    ```

4.  **AMATI TERMINAL KEDUA (Logs)**:
    Anda akan melihat log bergerak cepat. Tunjukkan ke dosen:
    *   "Lihat pak, `worker-1` mengerjakan job A..."
    *   "`worker-3` mengerjakan job B..."
    *   Mereka bekerja paralel.

### Langkah 5: Cek Hasil Akhir
Setelah semua selesai:
1.  Buka folder `storage/processed` di Windows Explorer.
2.  Tunjukkan bahwa sekarang sudah ada banyak file hasil resize di sana.

### Langkah 6: Mematikan Sistem
Setelah demo selesai, matikan sistem.

**Perintah:**
```bash
docker-compose down
```

---

## 4. Analisis & Kesimpulan
*   **Efisiensi**: Dengan memisahkan API dan Worker, API tetap responsif walau sedang memproses banyak gambar.
*   **Skalabilitas**: Kita bisa menambah worker jadi 5 atau 10 hanya dengan satu baris config di `docker-compose.yml`, tanpa mengubah kode program.
*   **Keandalan**: Jika satu worker mati, worker lain masih bisa handle antrian dari Redis.
