# Jurnal Proses — Tugas 2

## [Sabtu, 26 September 2026]
- Opsi arsitektur yang dipertimbangkan: 
  1. Monolithic - seluruh modul seperti pesanan, pembayaran, resto, dan kurir berada dalam satu sistem dan saling terhubung secara langsung
  2. Service-Oriented Architecture (SOA) - setiap fungsi utama dipisahkan menjadi beberapa service sehingga dapat dikelola secara terpisah
  3. SOA dengan Publish-Subscribe dan Message Broker - Service dipisahkan dan komunikasi antar service menggunakan message broker sebagai perantara untuk pertukaran event secara asinkron
   
- Kenapa akhirnya pilih [SOA/Pub-Sub]: 
  Arsitektur yang dipilih adalah SOA dengan Publish-Subscribe dan message broker karena menurut kita itu paling sesuai dengan kebutuhan untuk memisahkan service dan mengurangi komunikasi langsung antar komponennya
  
- Revisi diagram (versi 1 → versi 2, apa yang berubah dan kenapa): ...
Alur diagram diubah dengan menempatkan proses pembayaran sebelum `Message Broker`. Pesanan terlebih dulu melakukan `RequestPayment` ke Pembayaran. Kemudian jika berhasil melakukan Pembayaran `PaymentCompleted` ke Message Broker, kemudian akan diteruskan ke Resto dan Kurir. Tujuan dilakukan revisi ini agar Resto dan Kurir hanya menerima informasi pesanan setelah pembayaran dilakukan serta menerapkan metode Publish-Subscribe

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |
