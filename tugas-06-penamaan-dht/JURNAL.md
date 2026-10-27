# Jurnal Proses — Tugas 6

## Implementasi find_successor
- Kesalahan pertama yang ditemui (mis. lupa wrap-around di ring): 
1. NameError: self/node tidak dikenali, karena Badan method join()/leave() indentasinya sejajar dengan def, bukan masuk 1 level lagi
2. find_successor() tidak bisa dipanggil method lain	
Tertulis ter-nested di dalam leave(), bukan method class yang sejajar
3. Perlu validasi logika migrasi data	Interval migrasi (predecessor, node_id] sulit diverifikasi hanya dari membaca kode
- Cara memperbaikinya: ...
1. Perbaiki indentasi: badan method harus 8 spasi (2 level dari class)
2. Pindahkan ke level indentasi yang sama dengan method lain (4 spasi langsung di bawah class)
3. Uji manual dengan skenario tambahan (4 node + beberapa kurir + 1 node baru) untuk memastikan hanya kurir di interval yang tepat yang termigrasi
## Skenario join/leave
- Hasil sebelum & sesudah node baru bergabung:
Sebelum: urutan node di ring adalah 40 → 102 → 136 → 177 → (kembali ke 40). kurir-001 (hash=50) ditanggung oleh node 102, karena 102 adalah hash node terkecil yang ≥ 50.

Sesudah node-medan-1 (id=123) bergabung: 
urutan ring menjadi 40 → 102 → 123 → 136 → 177. Node 123 kini bertanggung jawab atas interval (102, 123] — yaitu hash 103 sampai 123. Karena hash kurir-001 (=50) tidak berada dalam interval tersebut, tanggung jawabnya tetap di node 102, sehingga tidak ada migrasi dan lookup kurir-001 tetap mengembalikan 192.168.1.10.

Ini membuktikan logika migrasi bekerja dengan benar: node baru hanya mengambil alih data yang memang jatuh di rentang tanggung jawabnya, bukan mengambil semua data secara sembarangan.

- Hasil sebelum & sesudah node keluar:
Sebelum: urutan ring adalah 40 → 102 → 123 → 136 → 177. Node 177 bertanggung jawab atas interval (136, 177], namun tidak ada satupun kurir (hash 50, 28, 132) yang berada di rentang tersebut — artinya node 177 tidak memegang data kurir apa pun.

Sesudah node-jakarta-1 (id=177) keluar: successor-nya adalah node 40 (karena ring wrap-around), sehingga seharusnya data node 177 (jika ada) dipindah ke node 40. Karena memang tidak ada data yang dipegang node 177, log menunjukkan "Total data dimigrasi: 0" — ini valid, bukan bug. Lookup kurir-001 → 192.168.1.10 dan kurir-002 → 192.168.1.11 tetap berhasil ditemukan tanpa perubahan, karena keduanya ditanggung oleh node lain (102 dan 40) yang tidak terganggu oleh keluarnya node 177.

Ini menunjukkan bahwa leave() sudah benar menghitung interval tanggung jawab node yang keluar sebelum memindahkan data, dan tidak memaksa migrasi pada data yang sebenarnya tidak terpengaruh.

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 27 Oktober 2026 | ChatGPT | Bantuan menyusun jurnal Tugas 6 berdasarkan kode Chord DHT | Mendapatkan arahan mengenai struktur jurnal dan aspek yang perlu diperiksa | [Jelaskan secara jujur bagaimana bantuan digunakan dan bagaimana kelompok memverifikasi hasilnya.] |
