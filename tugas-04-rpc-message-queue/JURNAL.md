# Jurnal Proses — Tugas 4

## Jalur yang dipilih
- [keduanya], alasan: saya mencoba kedua jalur untuk memahami perbedaan komunikasi sinkron dan asinkron
  - RPC: digunakan untuk memanggil fungsi pada server pembayaran, yaitu `cek_saldo()` dan `proses_pembayaran()`
  - Message Queue: digunakan untuk mengirim event pembayaran melalui RabbitMQ aagr notifikasi dapat diproses oleh consumer secara asinkron
Dengan mencoba kedua jalur, kami dapat membandingkan bagaimana client merima respons langsung pada RPC dan bagaimana psan dapat menunggu di antrean pada MQ

## Hasil Pengujian RPC
Kami melakukan pengujian dnegan menjalankan `server.py` dan server.py pada dua terminal
Hasil yang kami peroleh:
1. Server RPC berhasil berjalan di `http://localhost:8000`
2. Pemanggilan `cek_saldo('user1')` berhasil dan menghasilkan saldo Rp130.000
3. Pemanggilan `proses_pembayaran('user1',20000)` menghasilkan status `SUCCESS`
4. Sisa saldo setelah pembayaran adalah Rp110.000
5. Client menerima hasil dari server dan menampilkan waktu tunggu sekitar 2 detik pada pengujian tersebut
Analisisnya dari apa yang kami kerjakan RPC cocok untuk operasi yang membutuhkan respons langsung, seperti pengecekan saldo dan proses pembayaran. Kemeudian client menunggu hasil dari server sebelum melanjutkan proses berikutnya

## Hasil Pengujian Message Queue
Pengujian dilakukan menggunakan RabbitMQ, `publisher.py`, dan `consumer.py`
1. Publisher dan consumer berjalan normal
   Publisher berhasil mengirim 3 event dengan data berikut:
   - `user1` dengan jumlah 20.000
   - `user2` dengan jumlah 40.000
   - `user3` dengan jumlah 60.000
  Sehingga consumer menerima event dan menampilkan notifikasi pembayaran untuk ketiga pengguna tersebut. 
2. Consumer dihentikan
   Pengujian dilanjutkan denegan menghentikan consumer dan mengirim pesan melalui publisher
   Pada dashboard RabbitMQ, antrean di `pembayaran_berhasil` menunjukkan ready = 3, unacked = 0, dan totalnya = 3
   Sehingga hasil yang kami peroleh adalah menunjukkan bahwa ada 3 pesan yang menunggu untuk diproses dan belum dikirimkan kepada consumer yang aktif
3. Consumer dijalankan kembali
   Setelah consumer dijalankan kembali, dashboard RabbitMQ menunjukkan bahwa ready = 0, unacked = 0, dan total = 0
   Kondisi ini konsisten denegan pesan yang sudah diproses sehingga tidak ada pesan tersisa di antrean pada saat screenschot diambil.

   Jadi menurut analisis kami pengujian ini mendukung konsep asynchronous decoupling. Sehingga publisher dapat memasukkan pesan ke antrean tanpa harus menunggu consumer memprosesnya. Dan pesan dapat menunggu sampai consumer kembali aktif, selama konfigurasi dan kondisi penyimpanan RabbitMQ tetap mendukungnya

## Kendala teknis
- Error saat setup (mis. koneksi RabbitMQ ditolak, port bentrok): 
  Saat menginisialisasi lingkungan virtual Python untuk modul Message Queue, perintah standar berbasis Unix (python3 -m venv venv && source venv/bin/activate) gagal dieksekusi karena PowerShell tidak mengenali operator pemisah &&. Kendala ini diatasi dengan memecah perintah menjadi dua tahapan secara terpisah, yaitu pembuatan lingkungan virtual menggunakan python -m venv venv dilanjutkan dengan aktivasi skrip eksekusi khusus PowerShell melalui perintah .\venv\Scripts\Activate.ps1

## Uji "pesan tidak hilang" (khusus Jalur B)
- Langkah uji: matikan consumer → jalankan publisher → nyalakan consumer
- Hasil yang diamati: saat consumer mati, RabbitMQ menunjukkan `Ready = 3`, artinya ada tiga pesan yang menunggu. Setelah consumer dijalankan kembali, jumlan pesannya menjadi `0`. 
- Sehingga dari pengujian ini, terlihat bahwa pesan tidak langsung hilang saat consumer mati, tetapi tetap menunggu di antrean sampai consumernya aktif

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|09-10-2026|ChatGPT|Bantu aku untuk memahami perbedaan RPC dan Message Queue serta mengevaluasi hasil pengujian.|AI menjelaskan konsep sinkron dan asinkron serta cara membaca status antrean RabbitMQ.|Saya mencocokkan penjelasan dengan kode dan hasil pengujian sendiri, lalu menulis analisis berdasarkan screenshot yang diperoleh.|
| ... | ... | ... | ... | ... |
