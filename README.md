# 🖼️ Distributed Image Resizer API

![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
![Redis](https://img.shields.io/badge/redis-%23DD0031.svg?style=for-the-badge&logo=redis&logoColor=white)

Ini adalah tugas besar Komputasi Cloud (Tugas Besar) yang berupa sistem *distributed image resizing*. Sistem ini dirancang untuk menangani proses resize banyak gambar sekaligus tanpa membuat server utama lemot. Menggunakan arsitektur *producer-consumer* dengan **Flask** (API), **Redis** (Antrian), dan **Python Workers** (Pemroses), yang semuanya dijalankan lewat **Docker Compose**.

---

## 🚀 Fitur Utama

*   **Arsitektur Terdistribusi**: Memisahkan penerimaan upload (API) dan pemrosesan gambar (Workers) pakai message queue.
*   **Worker Skalabel**: Bisa nambah jumlah worker sesuka hati cuma pakai satu perintah.
*   **Web Interface**: Ada tampilan web sederhana buat upload gambar, nggak harus pakai command line.
*   **Akses File Lokal**: Folder upload dan hasil resize langsung muncul di folder komputer kita, jadi gampang dicek.
*   **Full Docker**: Tinggal `docker-compose up`, langsung jalan semua tanpa ribet install dependencies satu-satu.

---

## 🏗️ Cara Kerja sistem

Ada 3 komponen utama di sini:

1.  **API Service**:
    *   Menerima upload gambar lewat web atau API (`POST /upload`).
    *   Cek file (validasi), terus simpan file aslinya di `storage/uploads`.
    *   Kirim pesan "Tolong resize gambar ini dong" ke antrian Redis.
2.  **Message Queue (Redis)**:
    *   Jadi perantara (broker). Dia yang megang daftar antrian tugas buat dibagi-bagi ke worker yang lagi nganggur.
3.  **Worker Service**:
    *   Program yang jalan di background, nungguin tugas dari Redis.
    *   Begitu dapet tugas, dia ambil gambarnya, resize jadi 300x300 pixel.
    *   Hasilnya disimpan di `storage/processed`.

---

## 📦 Struktur Project

```
project-root/
├── api/                # Kodingan Flask API & Tampilan Web
│   ├── app.py
│   ├── templates/
│   └── Dockerfile
├── worker/             # Kodingan Worker (Pekerja)
│   ├── worker.py
│   └── Dockerfile
├── storage/            # Folder Penyimpanan (Nyambung ke folder lokal)
│   ├── uploads/        # Gambar asli masuk sini
│   └── processed/      # Hasil resize masuk sini
├── docker-compose.yml  # Config buat jalanin semua container
├── load_test.py        # Script buat ngetes beban (simulasi banyak upload)
└── README.md
```

---

## 🛠️ Cara Menjalankan

### Persiapan

*   Pastikan udah install **Docker** & **Docker Compose** di laptop/PC.

### Langkah-langkah

1.  **Masuk ke folder project**:
    ```bash
    cd path/to/project
    ```

2.  **Jalankan aplikasi**:
    ```bash
    docker-compose up -d --build
    ```
    *Tunggu sebentar sampai proses build selesai dan semua kontainer jalan.*

3.  **Cek status**:
    ```bash
    docker-compose ps
    ```
    Pastikan semua statusnya `Up`.

---

## 💻 Cara Pakai

### 1. Lewat Web (Paling Gampang)
Buka browser, terus akses:
👉 **[http://localhost:5000](http://localhost:5000)**

Tinggal pilih file gambar (JPG/PNG) terus klik tombol "Upload & Resize".

### 2. Lewat Terminal (Curl)
Kalau mau nyoba gaya programmer backend:

```bash
curl -X POST -F "file=@/path/to/image.jpg" http://localhost:5000/upload
```

### 3. Cek Hasilnya
Gambar yang sudah selesai di-resize bakal muncul otomatis di folder:
📂 **`storage/processed/`** (Cek di file explorer laptop kamu)

---

## 🧪 Testing Beban (Load Test)

Buat membuktikan kalau sistem ini beneran terdistribusi (dikerjain bareng-bareng sama banyak worker), coba langkah ini:

1.  Buka terminal baru buat **melihat log worker**:
    ```bash
    docker-compose logs -f worker
    ```

2.  Buka terminal satu lagi buat **jalanin script test**:
    ```bash
    python load_test.py
    ```

Perhatikan terminal yang nampilin log. Kamu bakal lihat `worker-1`, `worker-2`, dan `worker-3` ganti-gantian ngerjain tugasnya. Keren kan? 😎

---

## ⚙️ Skalabilitas

Butuh lebih banyak worker biar makin ngebut? Gampang, tinggal ketik:

```bash
docker-compose up -d --scale worker=5
```
Sekarang kamu punya 5 worker yang siap lembur!

---

## 📝 Lisensi
Project ini dibuat untuk memenuhi **Tugas Besar Komputasi Cloud**.
Boleh dipakai atau dimodifikasi buat belajar.
