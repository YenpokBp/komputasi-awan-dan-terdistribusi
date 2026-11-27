# Tugas 10 (Pekan 10) — Arsitektur Cloud yang Skalabel

**Materi terkait:** Workload Distribution, Resource Pooling, Dynamic/Horizontal/Vertical Scalability, Load Balancing.

## Studi Kasus

Situs web tiket konser "TicketGo" **mogok total** karena tidak mampu menangani lonjakan **1 juta pengguna dalam 1 menit** saat penjualan tiket dibuka (fenomena *thundering herd*). Server tunggal mereka kehabisan koneksi dan CPU 100% dalam hitungan detik.

## Tugas Kelompok

Simulasikan (di laptop, memakai Docker Compose) sebuah arsitektur dengan **Load Balancer** di depan **beberapa instance aplikasi identik**, lalu buktikan dengan load test sederhana bahwa distribusi beban benar-benar terjadi.

### Yang Sudah Disediakan

- `app/app.py` — skeleton server HTTP super sederhana yang mengembalikan ID instance-nya sendiri (supaya kalian bisa melihat request mana ditangani instance mana).
- `nginx/nginx.conf` — skeleton konfigurasi Nginx sebagai Load Balancer, dengan 3 backend (`app1`, `app2`, `app3`).
- `docker-compose.yml` — skeleton yang menjalankan 3 instance `app` + 1 `nginx` sebagai LB.
- `load_test.py` — skeleton script pengirim request konkuren untuk menguji distribusi beban.

### Langkah Kerja

1. Lengkapi `# TODO` di `app/app.py` (kembalikan `INSTANCE_ID` dari environment variable di response).
2. Lengkapi `# TODO` di `nginx/nginx.conf` (buat `upstream` block berisi 3 backend, gunakan di `proxy_pass`).
3. Jalankan:
   ```bash
   docker compose up --build
   ```
4. Lengkapi `load_test.py` untuk mengirim **N request konkuren** (mis. 300 request, 30 thread) ke `http://localhost:8080/`, lalu hitung berapa kali masing-masing instance (`app1`/`app2`/`app3`) menangani request — buktikan beban **terdistribusi**, bukan selalu ke satu instance saja.
5. **Simulasikan scale-up manual**: tambah 1 instance lagi (`app4`) di `docker-compose.yml` + `nginx.conf`, restart, ulangi load test, bandingkan distribusi beban.
6. **Simulasikan Vertical Scaling** untuk perbandingan: jalankan **1 instance saja** tapi beri batas resource lebih besar (`docker run --cpus=2 --memory=1g ...` atau field `deploy.resources` di compose), lakukan load test yang sama, catat latensi/kegagalan dibanding skenario horizontal 3 instance.

## Analisis yang Wajib Ditulis di `README.md`

1. Bukti distribusi beban (angka request per instance) dari load test horizontal.
Pengujian dilakukan menggunakan 300 request dengan concurrency 30 melalui Nginx Load Balancer.

**Pengujian dengan 3 instance**

| Instance | Jumlah Request |
|---|---:|
| app1 | 100 |
| app2 | 100 |
| app3 | 100 |
| **Total** | **300** |

Hasil pengujian:
- Total request: 300
- Concurrency: 30
- Error: 0
- Rata-rata latency: 0,0608 detik
- Throughput: 417,42 request/detik

**Pengujian dengan 4 instance**

| Instance | Jumlah Request |
|---|---:|
| app1 | 75 |
| app2 | 75 |
| app3 | 75 |
| app4 | 75 |
| **Total** | **300** |

Hasil pengujian:
- Total request: 300
- Concurrency: 30
- Error: 0
- Rata-rata latency: 0,0891 detik
- Throughput: 311,25 request/detik

Dari hasil tersebut, request berhasil dibagikan ke seluruh instance. Pada pengujian 3 instance, setiap instance menangani 100 request. Setelah ditambahkan menjadi 4 instance, setiap instance menangani 75 request.
2. Perbandingan hasil **Horizontal Scaling (3-4 instance kecil)** vs **Vertical Scaling (1 instance besar)** — mana yang lebih tangguh untuk skenario *thundering herd* seperti TicketGo, dan kenapa.
Pengujian dilakukan dengan total 300 request dan concurrency 30.

**Hasil Horizontal Scaling**

| Skenario | Jumlah Instance | Request per Instance | Rata-rata Latency | Throughput | Error |
|---|---:|---|---:|---:|---:|
| Horizontal 3 instance | 3 | 100, 100, 100 | 0,0608 detik | 417,42 req/detik | 0 |
| Horizontal 4 instance | 4 | 75, 75, 75, 75 | 0,0891 detik | 311,25 req/detik | 0 |

**Hasil Vertical Scaling**

| Kondisi | Jumlah Instance | CPU | RAM | Rata-rata Latency | Throughput | Error |
|---|---:|---:|---:|---:|---:|---:|
| Sebelum peningkatan | 1 | 0,5 CPU | 512 MB | 2,3815 detik | 11,50 req/detik | 0 |
| Setelah peningkatan | 1 | 2 CPU | 512 MB | 0,0671 detik | 379,06 req/detik | 0 |

Pada Vertical Scaling, kapasitas CPU ditingkatkan dari 0,5 menjadi 2 CPU, sedangkan RAM tetap 512 MB.

**Analisis Perbandingan**
Berdasarkan hasil pengujian, horizontal scaling dengan 3 instance menghasilkan throughput sebesar 417,42 request/detik dan rata-rata latensi 0,0608 detik. Sementara itu, vertical scaling setelah peningkatan CPU menjadi 2 core menghasilkan throughput 379,06 request/detik dan rata-rata latensi 0,0671 detik.

Horizontal scaling lebih cocok untuk menghadapi lonjakan pengunjung TicketGo karena beban dapat dibagi ke beberapa instance. Selain itu, jika satu instance mengalami gangguan, instance lain masih dapat melayani permintaan. Vertical scaling juga meningkatkan kemampuan server, tetapi tetap bergantung pada satu instance sehingga berisiko menjadi titik kegagalan tunggal 
### Keterbatasan Simulasi Dibandingkan Auto Scaling Cloud

Pada simulasi ini, penambahan dan pengurangan instance masih dilakukan secara manual melalui Docker Compose dan konfigurasi Nginx. Berbeda dengan Auto Scaling pada AWS, jumlah instance dapat bertambah atau berkurang secara otomatis berdasarkan metrik seperti penggunaan CPU atau jumlah permintaan.

Agar sistem dapat menerapkan auto-scaling, diperlukan beberapa komponen, yaitu pemantauan metrik (*metric collector*), pengatur penambahan dan pengurangan instance (*auto-scaler*), serta pemeriksaan kesehatan instance (*health check*). Dengan komponen tersebut, kapasitas sistem dapat menyesuaikan kebutuhan trafik secara otomatis.

### Kesimpulan Kelompok

Berdasarkan hasil pengujian, horizontal scaling dengan 3 instance memberikan throughput tertinggi dibandingkan skenario lainnya yang diuji. Horizontal scaling juga lebih sesuai untuk menghadapi lonjakan trafik TicketGo karena beban dapat dibagi ke beberapa instance dan layanan tidak hanya bergantung pada satu server.

Namun, simulasi ini masih memiliki keterbatasan karena proses scaling dilakukan secara manual dan belum menggunakan mekanisme auto-scaling seperti pada layanan cloud. Oleh karena itu, pengembangan selanjutnya dapat menerapkan pemantauan metrik dan penambahan instance otomatis agar sistem lebih responsif terhadap perubahan jumlah pengguna.


3. Jelaskan **keterbatasan simulasi ini** dibanding *auto-scaling* cloud sungguhan (mis. AWS Auto Scaling Group): di sini kalian menambah instance **manual**, sedangkan cloud asli menambah/mengurangi instance **otomatis berdasarkan metrik** (CPU, jumlah request) tanpa campur tangan manusia. Jelaskan komponen apa yang dibutuhkan agar proses manual kalian bisa jadi otomatis (mis. metric collector + auto-scaler + health check).
Pada simulasi ini, penambahan jumlah instance dilakukan secara manual melalui konfigurasi Docker Compose dan Nginx. Artinya, pengguna harus menambahkan instance dan memperbarui konfigurasi ketika beban meningkat.

Pada layanan cloud sungguhan, seperti AWS Auto Scaling Group, jumlah instance dapat bertambah atau berkurang secara otomatis berdasarkan metrik tertentu, misalnya penggunaan CPU atau jumlah request.

**Komponen yang Dibutuhkan untuk Auto-Scaling**

1. **Metric Collector**  
   Mengumpulkan metrik penggunaan resource, seperti CPU, memori, dan jumlah request.

2. **Auto-Scaler**  
   Mengambil keputusan untuk menambah atau mengurangi instance berdasarkan aturan dan ambang batas metrik.

3. **Health Check**  
   Memeriksa apakah instance berjalan dengan baik dan dapat menerima request.

4. **Load Balancer**  
   Membagikan request ke instance yang aktif dan sehat.

Dengan komponen tersebut, proses penambahan dan pengurangan instance dapat berjalan otomatis tanpa harus dilakukan secara manual.

**Analisis Keterbatasan**

Simulasi ini masih menggunakan penambahan instance secara manual. Agar otomatis seperti AWS Auto Scaling, diperlukan Metric Collector, Auto-Scaler, Health Check, dan Load Balancer untuk memantau trafik serta menambah atau mengurangi instance sesuai kebutuhan.
  
### Kesimpulan

Berdasarkan percobaan Horizontal Scaling dan Vertical Scaling, tuliskan kesimpulan kelompok mengenai:
- Keberhasilan Nginx dalam membagikan request ke beberapa instance.
- Perbedaan hasil pengujian Horizontal Scaling dan Vertical Scaling.
- Pendekatan yang dianggap lebih sesuai untuk menghadapi lonjakan pengguna TicketGo.
- Pentingnya auto-scaling untuk menjaga ketersediaan layanan ketika traffic berubah.

## Struktur Submission

```
tugas-10-arsitektur-cloud-skalabel/
├── README.md
├── JURNAL.md
├── docker-compose.yml
├── app/
│   └── app.py
├── nginx/
│   └── nginx.conf
├── load_test.py
└── bukti/          # Output load test (horizontal vs vertical), screenshot docker compose ps
```

## Rubrik Penilaian (Tugas 10)

| Komponen | Bobot | Kriteria |
|---|---|---|
| LB & multi-instance berjalan | 30% | Nginx berhasil mendistribusikan request ke ≥3 instance berbeda |
| Load test & bukti distribusi | 25% | Angka konkret request per instance, bukan klaim tanpa data |
| Analisis Horizontal vs Vertical | 25% | Perbandingan berbasis hasil eksperimen sendiri, bukan teori generik |
| Analisis keterbatasan vs auto-scaling nyata | 10% | Paham perbedaan simulasi manual vs mekanisme otomatis di cloud asli |
| Proses & kontribusi kelompok | 10% | `JURNAL.md`, commit history |

## Batasan Penggunaan AI (Level 2)

Kebijakan **Level 2 (AI Assisted Idea Generation & Structuring)** berlaku — lihat [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Boleh bertanya konsep umum load balancing ke AI; **tidak boleh** meminta AI menuliskan isi `# TODO` di `app/app.py`, `nginx/nginx.conf`, atau `load_test.py`. Catat pemakaian AI di "Log Penggunaan AI" pada `JURNAL.md`.

- `JURNAL.md` wajib mencatat apa yang terjadi jika satu instance `app` dimatikan saat load test berjalan (jalankan skenario ini dan catat hasilnya, jangan cuma diklaim tanpa data).
