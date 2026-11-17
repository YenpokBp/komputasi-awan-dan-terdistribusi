# Jurnal Proses — Tugas 7

## Diskusi pemilihan model konsistensi
- **Argumen yang dipertimbangkan:** 
  1. *Sequential / Strong Consistency*: 
     - *Kelebihan*: Menjamin bahwa seluruh replika di berbagai wilayah (misalnya server Jakarta dan Bandung) melihat urutan operasi penulisan (*write*) yang persis sama, sehingga tidak pernah ada celah perbedaan data.
     - *Kekurangan*: Berdasarkan teorema CAP, sistem harus mengorbankan ketersediaan (*availability*) atau mengalami latensi yang sangat tinggi karena setiap operasi harus menunggu sinkronisasi global selesai sebelum dikonfirmasi ke pengguna. Hal ini kurang ideal untuk aplikasi publik yang menuntut respons cepat.
  2. *Eventual Consistency*: 
     - *Kelebihan*: Memberikan performa tinggi, latensi rendah, dan ketersediaan maksimum karena server lokal dapat langsung merespons permintaan baca/tulis tanpa harus menunggu replikasi lintas region selesai seketika.
     - *Kekurangan*: Rentan terhadap masalah *stale data* (data usang). Jika pengguna berpindah konteks jaringan atau dilayani oleh server berbeda sebelum replikasi selesai, mereka akan melihat data yang belum diperbarui.
  3. *Client-Centric Consistency (Read-Your-Writes)*: 
     - Menjadi jalan tengah (*sweet spot*) yang mempertahankan kecepatan *eventual consistency* di tingkat *backend*, namun memberikan jaminan khusus dari sudut pandang klien bahwa pengguna yang baru saja melakukan aksi tulis (*write* seperti *top-up*) tidak akan pernah melihat versi data lama saat melakukan pembacaan berikutnya.
- **Kesimpulan akhir & alasan:** 
  - Kelompok memutuskan untuk mengadopsi kombinasi **Eventual Consistency** untuk replikasi latar belakang antar pusat data guna menjaga performa dan *availability* sistem secara keseluruhan, yang diperkuat dengan mekanisme **Client-Centric Consistency: Read-Your-Writes**. Keputusan ini diambil karena aplikasi *e-wallet* FoodGo menuntut keamanan finansial yang tinggi (pengguna harus langsung melihat saldo terbaru mereka setelah *top-up*), namun di sisi lain aplikasi harus tetap ringan dan responsif diakses dari berbagai wilayah geografis tanpa hambatan latensi jaringan global yang ketat.

## Simulasi (jika dikerjakan)
- **Hasil skenario naif vs Read-Your-Writes:** 
  - **Skenario Naif (Tanpa Proteksi Konsistensi):** 
    - Berdasarkan hasil eksekusi kode simulasi (`replica_simulation.py`), ketika pelanggan melakukan *top-up* sebesar Rp50.000 melalui server Jakarta, data langsung tersimpan secara lokal. Namun, karena proses replikasi latar belakang disimulasikan memiliki jeda waktu (`REPLICATION_DELAY = 2.0` detik), pembacaan yang dilakukan kurang dari 2 detik kemudian melalui server Bandung akan menghasilkan data usang (saldo terbaca Rp0). 
    - Dampak bisnis: Transaksi pemesanan makanan pelanggan berisiko ditolak secara keliru oleh sistem karena saldo dianggap tidak mencukupi padahal *top-up* sudah berhasil dilakukan.
  - **Skenario dengan Mekanisme Read-Your-Writes:** 
    - Dengan menerapkan pengecekan versi data (`version_of` dan `versi_minimal`), ketika pelanggan melakukan penambahan saldo berikutnya sebesar Rp20.000 (sehingga total versi tercatat meningkat), sistem mendeteksi bahwa replika server Bandung masih tertinggal versinya. 
    - Melalui fungsi pengalihan (*redirect*) pembacaan secara transparan ke server Jakarta yang memegang versi data mutakhir, sistem berhasil menampilkan saldo total yang benar sebesar Rp70.000 secara instan, meskipun proses replikasi asinkron di latar belakang belum sepenuhnya selesai.

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 17 November 2026 | Gemini | *Brainstorming* studi kasus alternatif selain *e-wallet* yang relevan dengan tantangan konsistensi data replikasi dalam sistem terdistribusi skala luas. | AI menyarankan skenario perubahan status pengiriman kurir atau status pesanan e-commerce (*delivery status*) yang bersifat asinkron dan terdistribusi antar region. | Kelompok menggunakan ide tersebut untuk merancang studi kasus tambahan terkait perubahan status pesanan pada aplikasi FoodGo (antara "Menunggu Konfirmasi" dan "Sedang Diproses") serta menyusun analisis perbandingannya secara mandiri di dalam laporan utama. |