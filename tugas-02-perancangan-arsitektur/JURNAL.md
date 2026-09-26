# Jurnal Proses — Tugas 2

## [Sabtu, 26 September 2026]
- Opsi arsitektur yang dipertimbangkan: ...
- Kenapa akhirnya pilih [SOA/Pub-Sub]: ...
- Revisi diagram (versi 1 → versi 2, apa yang berubah dan kenapa): ...
Alur diagram diubah dengan menempatkan proses pembayaran sebelum `Message Broker`. Pesanan terlebih dulu melakukan `RequestPayment` ke Pembayaran. Kemudian jika berhasil melakukan Pembayaran `PaymentCompleted` ke Message Broker, kemudian akan diteruskan ke Resto dan Kurir. Tujuan dilakukan revisi ini agar Resto dan Kurir hanya menerima informasi pesanan setelah pembayaran dilakukan serta menerapkan metode Publish-Subscribe

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |
