# Tugas 1 — Analisis Pitfall FoodGo

**Kelompok:** [yencefran]

| Nama | NIM | Kontribusi |
|---|---|---|
| [Grace Roswita Sallu] | [103072400093] | [pitfall/bagian yang dikerjakan] |
| [Yustinus Yendy S.A] | [103072400065] | [Pitfall 1] |
| [Efran Gustine Y] | [103072400046] | [pitfall/bagian yang dikerjakan] |

## Pitfall 1: [The Network Is Reliable] — ditulis oleh [Yustinus Yendy]

### **Bukti di skenario:** network is always reliable, no need for retry

### **Kenapa ini keliru:** 
    FoodGo menganggap komunikasi antar service selalu berhasil, sehingga sistem tidak menyediakan mekanisme retry. Dan juga komunikasi jaringan dapat mengalami kegagalan/gangguan sehingga request tidak konsisten mendapatkan respons


### **Dampak ke FoodGo:** 
    ketika komunikasi tidak reliable dan tidak ada sistem yang memperbaiki problem itu, maka satu kegagalan komunikasi itu bisa mempengaruhi keberlanjutan alur sistem


**Solusi desain awal:** 
###    1. Tambahkan mekanisme retry
        kalau request gagal karena gangguan jaringan sementara, sistem masih dapat mencoba mengirim request.
        tapi retry tidak disarankan dilakukan terus menerus. Harus diberikan batas jumlah percobaan dan jeda antar percobaan
###    2. Gunakan backoff
        tujuannya ketika payment service bermasalah, seluruh request tidak langsung mengirim bersamaan.
###    3. Pertimbangkan idempoteny untuk operasi pembayaran
        kalau request pembayaran berhasil, tapi response hilang karena gangguan jaringan, retry bisa menyebabkan pembayaran dilakukan kembali.
        maka request pembayaran perlu ID transaksi yang dimana sistem dapat mengenali request yang sama

### **Trade-off:** 
retry mungkin merupakan solusi untuk menghadapi kegagalan jaringan sementara, tetapi retry yang terlalu sering juga bisa meningkatkan beban service yang bermasalah. Kemudian retry ada operasi pembayaran dapat menyebabkan duplikasi proses apabila sistem tidak memiliki mekanisme  utnuk mengenali request yang sama  

---

## Pitfall 2: [nama pitfall] — ditulis oleh [nama]

(ulangi struktur di atas)

---

## Pitfall 3: [nama pitfall] — ditulis oleh [nama]

(ulangi struktur di atas)

---

## Kesimpulan Kelompok

[Ringkasan: jika FoodGo memperbaiki ketiga pitfall ini, apa arsitektur yang disarankan secara garis besar? Kaitkan dengan Tugas 2.]
