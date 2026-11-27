# Jurnal Proses — Tugas 10

## Setup Nginx & multi-instance
- Kendala saat konfigurasi upstream: File app.py yang digunakan oleh Docker belum diperbarui sesuai dengan perubahan kode terbaru. Hal ini terjadi karena belum dilakukan pengecekan ulang terhadap file yang digunakan oleh container. Setelah menyadari kendala tersebut, dilakukan pembaruan dan penyesuaian kembali pada Docker agar container menggunakan versi app.py terbaru. Selanjutnya, dilakukan pengecekan ulang untuk memastikan aplikasi dapat berjalan sesuai konfigurasi.

## Hasil Load Test Horizontal (3 instance)
- Distribusi request per instance:
  - Total request: 300
  - Request berhasil: 300
  - Request gagal: 0
  - app1: 100 request
  - app2: 100 request
  - app3: 100 request
  - Rata-rata latensi: 0,0608 detik
  - Throughput: 417,42 request/detik

**Analisis hasil:**

Dari hasil pengujian, ketiga instance mendapatkan jumlah request yang sama, yaitu masing-masing 100 request. Hal ini menunjukkan bahwa Nginx berhasil membagikan beban secara merata.

## Hasil Setelah Scale-up (4 instance)
- Distribusi request per instance:
  Setelah pengujian tiga instance selesai, kami menambahkan satu instance lagi, yaitu app4. Tujuannya untuk melihat perubahan distribusi beban ketika jumlah instance ditambah menjadi empat.
  Pengujian tetap menggunakan 300 request dan concurrency 30 agar hasilnya bisa dibandingkan dengan pengujian sebelumnya.

**Hasil pengujian:**

- Total request: 300
- Request berhasil: 300
- Request gagal: 0
- app1: 75 request
- app2: 75 request
- app3: 75 request
- app4: 75 request
- Rata-rata latensi: 0,0891 detik
- Throughput: 311,25 request/detik

**Analisis hasil:**

Setelah app4 ditambahkan, setiap instance menangani 75 request. Pembagian request tetap merata, tetapi throughput justru lebih rendah dibandingkan pengujian dengan tiga instance. Hal ini bisa dipengaruhi oleh kondisi komputer atau proses lain yang berjalan saat pengujian.

Dari percobaan ini, kami memahami bahwa penambahan instance membantu membagi beban, tetapi tidak selalu meningkatkan kecepatan aplikasi.

## Hasil Vertical Scaling (1 instance besar)
- Latensi/kegagalan dibanding horizontal:
- Pada tahap ini, kami mencoba meningkatkan kapasitas resource pada satu instance aplikasi tanpa menambah jumlah instance. Pengujian dilakukan dalam dua kondisi, yaitu sebelum dan sesudah peningkatan CPU.

#### A. Sebelum peningkatan resource

Konfigurasi yang digunakan:
- Jumlah instance: 1
- CPU limit: 0,5 CPU
- RAM limit: 512 MB
- Total request: 300
- Concurrency: 30

Hasil pengujian:
- Request berhasil: 300
- Request gagal: 0
- Rata-rata latensi: 2,3815 detik
- Throughput: 11,50 request/detik
- Durasi pengujian: 26,08 detik

#### B. Sesudah peningkatan resource

Konfigurasi yang digunakan:
- Jumlah instance: 1
- CPU limit: 2 CPU
- RAM limit: 512 MB
- Total request: 300
- Concurrency: 30

Hasil pengujian:
- Request berhasil: 300
- Request gagal: 0
- Rata-rata latensi: 0,0671 detik
- Throughput: 379,06 request/detik
- Durasi pengujian: 0,79 detik

**Analisis hasil:**

Setelah CPU ditingkatkan dari 0,5 menjadi 2 CPU, performa aplikasi meningkat dengan latensi yang lebih rendah dan throughput yang lebih tinggi. Jumlah instance dan RAM tetap sama. Dari pengujian ini, saya memahami bahwa Vertical Scaling dilakukan dengan meningkatkan kapasitas resource pada satu instance tanpa menambah jumlah instance.

### 5. Hasil Eksperimen Failover

Pada tahap ini, kami mencoba melihat bagaimana sistem bekerja ketika salah satu instance aplikasi dihentikan. Tujuannya adalah mengetahui apakah Nginx masih bisa mengarahkan request ke instance lain yang masih berjalan.

**Hasil pengujian:**

- Total request: 300
- Request berhasil: 240
- Request gagal (timeout): 60
- app1: 80 request
- app2: 80 request
- app3: 80 request

**Analisis hasil:**

Ketika salah satu instance dihentikan, sistem masih bisa melayani sebagian besar request melalui instance yang tersisa. Namun, terdapat 60 request yang mengalami timeout.

Hal ini menunjukkan bahwa mekanisme failover belum berjalan sempurna. Kemungkinan penyebabnya adalah Nginx masih mencoba mengirimkan request ke instance yang sudah berhenti.Dari pengujian ini, kami memahami pentingnya failover serta konfigurasi health check agar layanan tetap berjalan saat terjadi gangguan.

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 27/11/2026 | ChatGPT  | Brainstorming alur komunikasi Docker Compose, Nginx, dan instance aplikasi | Memahami hubungan antarservice | Mempelajari kembali alur komunikasi dan menerapkannya pada konfigurasi Docker Compose dan Nginx.|
| 27/11/2026 | ChatGPT  | Memeriksa kode load_test.py dan menambahkan pengukuran latensi.| Mendapat saran mengenai pengukuran waktu request, distribusi beban, dan validasi jumlah request.| Memahami saran yang diberikan, menyesuaikan kode dengan app.py, kemudian menjalankan pengujian untuk melihat hasilnya.|
| 27/11/2026 | ChatGPT  |  Membantu menganalisis hasil pengujian 3 dan 4 instance.| Mendapat penjelasan mengenai distribusi request, throughput, dan latensi.| Membandingkan hasil pengujian berdasarkan output terminal dan mencatat hasilnya ke dalam jurnal.|
| 27/11/2026 | ChatGPT  | Membantu memahami perbedaan Horizontal Scaling dan Vertical Scaling.|Mendapat gambaran mengenai penambahan jumlah instance dan peningkatan kapasitas resource.| Melakukan pengujian dengan jumlah instance dan kapasitas CPU yang berbeda, kemudian membandingkan hasilnya.|
