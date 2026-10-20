# Jurnal Proses — Tugas 5

## Implementasi Bully
- Kendala saat mengisi TODO 1-4:
  Kendala yang kita temukan adalah pengaturan `threading.Lock` pada proses election. Jika lock tetap digunakan ketika proses memanggil fungsi lain yang juga membutuhkan lock, thread dapat mengalami deadlock.

- Bug yang ditemukan:  
  Pada versi awal, kondisi tersebut dapat terjadi ketika node mengirim `ELECTION` tetapi tidak menerima `OK`. Jika `declare_leader()` dipanggil saat lock masih digunakan, sehingga proses dapat berhenti karena lock yang sama dicoba untuk diambil kembali oleh thread tersebut.

- Perbaikan yang dilakukan:  
  Jadi pada kode yang digunakan saat pengujian, lock hanya digunakan untuk melindungi perubahan data penting seperti `leader_id` dan `election_in_progress`. Proses yang membutuhkan waktu atau komunikasi dengan node lain, seperti menunggu ok, menunggu coordinator, dan mengirim pesaan coordinator, dilakukan di luar lock.

- Hasil perbaikan:  
  Dengan pengaturan tersebut, node tetap dapat menerima dan memproses pesan selama proses election berlangsung. Proses pengiriman coordinator juga dapat berjalan tanpa membuat thread terhenti, sehingga proses pemilihan leader dapat berjalan dengan lebih konsisten.

## Skenario 1: Start normal
- Leader yang terpilih: Node 5
- Log/observasi: Semua node (1-5) berhasil dijalankan
  Node dengan id lebih rendah mengirimkan pesan election ke node dengan id lebih tinggi dan menerima pesan ok. Sedangkan node 5 tidak memiliki node dengan id lebih tinggi, sehingga node 5 menjadi leader dengan mengirim pesan coordinator. Nah node 1-4 kemudian menerima pesan coordinator dengan menetapkan node 5 sebagai leadernya

## Skenario 2: Leader dimatikan
- Leader baru yang terpilih: 4
- Berapa lama waktu sampai leader baru terdeteksi: 
  Waktu deteksi leader mati: 23:11:24.381 pada node 4
  Waktu leader baru diumumkan: 23:11:24.411
  Waktu proses pemilihan dari deteksi hingga leader baru: sekitar 0,030 detik
- Log/ Observasi: Setelah node 5 tadi dimatikan, node yang masih aktif mendeteksi kalau node 5 tidak merespons dan memicu proses pemilihan ulang. Akhirnya node 4 menjadi node dengan id paling tinggi yang masih aktif. Sehingga node 4 kemudian mulai election kepada node 5, tapi tidak mendapat renspons. Karena tidak da node dengan id lebih tinggi yang aktif, jadilah node 4 menjadi leader dengan melakukan broadcast coordinator

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 20-10-2026 | ChatGPT | Bantu aku untuk memahami alur dan kebutuhan tugas 5 bully algorithm. | AI memberikan gambaran tentang tahapan implementasi bully algorithm dan hal-hal yang perlu diperhatikan dalam pengujian. | Kami gunakan sebagai acuan untuk memahami tugas, kemudian implementasi dan pengujian dilakukan sendiri oleh kelompok. |
