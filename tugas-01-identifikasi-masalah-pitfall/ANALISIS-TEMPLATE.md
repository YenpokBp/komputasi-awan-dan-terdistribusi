# Tugas 1 — Analisis Pitfall FoodGo

**Kelompok:** [yencefran]

| Nama                  | NIM            | Kontribusi                       |
| --------------------- | -------------- | -------------------------------- |
| [Grace Roswita Sallu] | [103072400093] | [pitfall/bagian yang dikerjakan] |
| [Yustinus Yendy S.A]  | [103072400065] | [Pitfall 1]                      |
| [Efran Gustine Y]     | [103072400046] | [pitfall/bagian yang dikerjakan] |

## Pitfall 1: [The Network Is Reliable] — ditulis oleh [Yustinus Yendy]

### **Bukti di skenario:** network is always reliable, no need for retry

### **Kenapa ini keliru:**

    FoodGo menganggap komunikasi antar service selalu berhasil, sehingga sistem tidak menyediakan mekanisme retry. Dan juga komunikasi jaringan dapat mengalami kegagalan/gangguan sehingga request tidak konsisten mendapatkan respons

### **Dampak ke FoodGo:**

    ketika komunikasi tidak reliable dan tidak ada sistem yang memperbaiki problem itu, maka satu kegagalan komunikasi itu bisa mempengaruhi keberlanjutan alur sistem

**Solusi desain awal:**

### 1. Tambahkan mekanisme retry

        kalau request gagal karena gangguan jaringan sementara, sistem masih dapat mencoba mengirim request.
        tapi retry tidak disarankan dilakukan terus menerus. Harus diberikan batas jumlah percobaan dan jeda antar percobaan

### 2. Gunakan backoff

        tujuannya ketika payment service bermasalah, seluruh request tidak langsung mengirim bersamaan.

### 3. Pertimbangkan idempoteny untuk operasi pembayaran

        kalau request pembayaran berhasil, tapi response hilang karena gangguan jaringan, retry bisa menyebabkan pembayaran dilakukan kembali.
        maka request pembayaran perlu ID transaksi yang dimana sistem dapat mengenali request yang sama

### **Trade-off:**

retry mungkin merupakan solusi untuk menghadapi kegagalan jaringan sementara, tetapi retry yang terlalu sering juga bisa meningkatkan beban service yang bermasalah. Kemudian retry ada operasi pembayaran dapat menyebabkan duplikasi proses apabila sistem tidak memiliki mekanisme utnuk mengenali request yang sama

---

## Pitfall 2: [Latency Is Zero] — ditulis oleh [Grace Roswita Sallu]

### **Bukti di skenario:** 
        Pada skenario FoodGo, di modul pesanan memanggil modul pembayaran dan menunggu respons tanpa batas waktu. Sehingga membuat sistem menganggap komunikasi antar modul pesanan dan modul pembayaran akan mendapatkan respons dalam beberapa waktu 

### **Kenapa ini keliru:**
      FoodGo menganggap komunikasi antar request dan response bisa terjadi hampir tanpa jeda. Padahal seharusnya setiap request perlu waktu untuk dikirim, diproses oleh service tujuan, lalu response dikirim kembali.

### **Dampak ke FoodGo:**
        Ketika payment memberikan respons dengan lambat, maka order akan terus menunggu karena tidak memiliki timeout. Lalu jika kondisi ini terjadi saat banyak pesanan bersamaan, maka semakin banyak request yang ikut nunggu respons dari payment. Sehingga code yang digunakan aplikasi bisa ikut tertahan dan waktu untuk respons pengguna jadi semakin lama 

**Solusi desain awal:**
### 1. Memberikan timout pada komunikasi antara order dan payment
       Sehingga order tidak akan menunggu respons selamanya. Jika dalam waktu tertentu respons belum diterima, sistem dapat menghentikan proses tersebut dan menangani kondisi gagal. seperti menandai transaksi sebagain pending

### 2. Circuit breaker   
        Membantu mencegah order terus mengirim request ke payment ketika service tersebut sedang bermasalah atau terlalu lambat

### **Trade-off:**
        Menggunakan timeout mungkin dapat mencegah menunggu terlalu lama, tapi menentukan nilai timeout juga tidak bisa sembarangan. Jadi jika waktunya terlalu pendek, FoodGo bisa menganggap pembayaran gagal padahal payment sebenernya masih memproses transaksi tersebut. Sehingga ini dapat menimbulkan masalah lain, seperti status pembayaran sudah berhasil tapi status pesanan belum berubah, atau sistem melakukan percobaan ulang yang sebenarnya tidak perlu. Jadi penggunaan timeout perlu dibarengi dengan penangan status transaksi yang baik agar tidak menimbulkan transaksi ganda 
---

## Pitfall 3: [nama pitfall] — ditulis oleh [nama]

## Pitfall 3: [Single Point of Failure pada Arsitektur Monolitik] — ditulis oleh [Efran Gustine Y]

### **Bukti di skenario:**

    Pada skenario FoodGo, semua modul seperti pesanan, pembayaran, dan notifikasi kurir berjalan pada satu server dan satu proses monolitik. Ketika server mengalami masalah atau crash, seluruh bagian aplikasi ikut terdampak dan server harus di-restart secara manual.

### **Kenapa ini keliru:**

    FoodGo menganggap semua modul dapat dijalankan dalam satu server tanpa menimbulkan masalah ketika jumlah pengguna meningkat. Padahal jika semua modul berada pada server dan proses yang sama, maka server tersebut menjadi satu titik kegagalan. Jika server mengalami overload atau crash, modul pesanan, pembayaran, dan notifikasi juga bisa ikut terganggu.

### **Dampak ke FoodGo:**

    Ketika terjadi peningkatan jumlah pesanan, semua modul harus menggunakan resource dari server yang sama. Jika beban semakin tinggi, resource server dapat habis dan membuat aplikasi menjadi lambat atau bahkan crash. Karena semua modul berada pada server yang sama, ketika server mengalami crash maka proses pesanan, pembayaran, dan notifikasi kurir dapat ikut berhenti. Sehingga sistem juga akan sulit menangani lonjakan traffic karena semua proses bergantung pada satu server.

**Solusi desain awal:**
### 1. Memisahkan modul menjadi beberapa service

    Modul pesanan, pembayaran, dan notifikasi dapat dipisahkan menjadi service yang berbeda sehingga tidak semuanya bergantung pada satu proses yang sama. Dengan begitu, setiap service dapat menangani tugasnya masing-masing.

### 2. Menambahkan lebih dari satu instance

    Service yang sering menerima banyak request dapat dijalankan dalam beberapa instance. Jika salah satu instance mengalami masalah, request masih dapat diarahkan ke instance lainnya sehingga tidak langsung membuat seluruh sistem berhenti.

### **Trade-off:**

    Memisahkan service dapat mengurangi ketergantungan pada satu server, tetapi membuat sistem menjadi lebih kompleks. Setiap service harus berkomunikasi melalui jaringan sehingga FoodGo juga perlu menangani masalah seperti latency, kegagalan komunikasi, dan monitoring dari beberapa service. Selain itu, menjalankan beberapa instance juga membutuhkan resource yang lebih banyak dibandingkan hanya menggunakan satu server.

---

## Kesimpulan Kelompok

[Ringkasan: jika FoodGo memperbaiki ketiga pitfall ini, apa arsitektur yang disarankan secara garis besar? Kaitkan dengan Tugas 2.]
