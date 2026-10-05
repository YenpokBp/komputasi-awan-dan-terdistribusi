# Jurnal Proses — Tugas 3

## Percobaan tanpa Lock
- Hasil `processed_count` yang didapat adalah 91 dari target 100 pesanan. Counter tidak sesuai dengan jumlah pesanan yang seharusnya diproses.
    
- Kenapa bisa meleset (jelaskan mekanisme race condition dengan kata sendiri): 
  1. Program menggunakan beberapa thread untuk memproses pesanan secara bersamaan.
  2. Semua thread mengakses variabel bersama `processed_count`
  3. Saat tidak menggunakan `Lock`, beberapa thread dapat membaca nilai `processed_count` yang sama pada waktu yang hampir bersamaan
  4. Setelah membaca nilai tersebut, masing-masing thread menambahkan 1 dan menuliskan kembali hasilnya.
  5. Karena pembaruan dilakukan bersamaan, maka hasil dari salah satu thread dapat menimpa pembaruan thread lainnya.
  6. Akibatnya, terdapat increment yang hilang dan nilai akhir menjadi lebih kecil dari 100
  7. Pada eksperimen ini, penggunaan `barrier` membantu memunculkan kondisi race tersebut secara konsisten sehingga hasil yang diperoleh adalah 91

## Percobaan dengan Lock
- Hasil `processed_count` setelah perbaikan: 100 dari target 100 pesanan. Counter sesuai dengan target
- Kenapa bisa sesuai?
  1. Program menggunakan `threading.Lock()` untuk melindungi proses perubahan `processed_count`
  2. Bagian increment counter ditempatkan di dalam `with lock:`
  3. Sehingga Lock dapat memastikan hanya satu thread yang dapat melakukan perubahan terhadap counter pada satu waktu.
  4. Dan thread yang lainnya harus menunggu sampai thread sebelumnya selesai melakukan increment.
  5. Dengan demikian, pembaruan counter tidak saling menimpa.
  6. Akhirnya hasil menjadi 100 sesuai dengan jumlah pesanan yang diproses.

## Kendala Docker
- Error yang ditemui saat `docker build`/`docker run` adalah pada awal pengujian, hasil yang muncul dari docker tetap 100 meskipun bagian penggunaan Lock pada kode python sudah dikomentari. Setelah diperiksa, penyebabnya adalah docker menggunakan kode yang sudah tersimpan di dalam image saat proses `docker build`. Jadi, perubahan yang dilakukan pada file python di komputer belum otomatis mengubah kode yang ada di dalam image dan cara memperbaikinya adalah melakukan `docker build` ulang setelah kode diubah, sehingga image docker menggunakan versi kode terbaru. 
- Saat mencoba menjalankan docker run ... --lock muncul error exec: "--lock": executable file not found in $PATH. Hal ini terjadi karena docker memperlakukan teks setelah nama image sebagai pengganti seluruh `CMD` yang ada di Dockerfile. Akibat, docker mencoba menjalankan `--lock` sebagai sebuah executable, bukan argumen untuk program python. Untuk mengatasinya, perintah dijalankan dengan menyebutkan program python dan file script secara lengkap, misalnya: docker run --rm foodgo-order-sim python src/order_simulator.py --lock dan untuk pengujian tanpa lock kita menggunakan docker run --rm foodgo-order-sim-pyhton src/order_simulator.py --no-lock. jadi intinya perubahan kode lokaal perlu diikuti dengan `docker build` ulang agar masuk ke image, sedangkan argumen `--lock` dan `--no-lock` perlu diberikan dengan cara yang sesuai dengan konfigurasi `CMD` pada dockerfile

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |
