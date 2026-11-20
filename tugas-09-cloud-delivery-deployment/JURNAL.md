# Jurnal Proses — Tugas 9

## Diskusi deployment model
- **Opsi yang dipertimbangkan:** Public Cloud, Private Cloud, dan Hybrid Cloud.
- **Keputusan kelompok:** Memilih Hybrid Cloud karena sistem kependudukan membutuhkan perlindungan data pribadi yang ketat, tetapi juga harus mampu melayani ribuan instansi dengan jumlah permintaan yang berubah-ubah.
- **Alasan pemilihan:** Private Cloud digunakan untuk menyimpan data inti kependudukan seperti NIK, biodata, dan template biometrik serta menjalankan proses verifikasi identitas. Public Cloud digunakan untuk layanan pendukung, seperti portal informasi umum dan penerimaan permintaan awal yang tidak memproses data pribadi sensitif.
- **Pertimbangan terhadap alternatif:** Public Cloud murni tidak dipilih karena pemerintah membutuhkan kendali terhadap infrastruktur yang menyimpan data sensitif. Hybrid Cloud dipilih agar kebutuhan keamanan dan skalabilitas dapat diseimbangkan.
- **Hasil diskusi:** Kelompok menetapkan bahwa pemrosesan data pribadi dan pencocokan identitas tetap dilakukan di Private Cloud, sedangkan Public Cloud hanya menangani layanan non-sensitif.

## Diskusi service model per komponen
- - **IaaS:** Digunakan untuk server database utama kependudukan, penyimpanan NIK dan biometrik, Virtual Machine aplikasi inti, serta infrastruktur jaringan dan keamanan server. Model ini dipilih karena pemerintah membutuhkan kendali lebih besar terhadap infrastruktur.
- **PaaS:** Digunakan untuk platform aplikasi kependudukan, middleware, pengolahan dan pencocokan identitas, layanan API, serta portal informasi umum yang dikembangkan sendiri oleh pemerintah. Model ini membantu pengembangan dan pengelolaan aplikasi tanpa harus mengatur seluruh infrastruktur secara manual.
- **SaaS:** Digunakan untuk dashboard monitoring layanan pendukung, aplikasi administrasi non-sensitif, serta aplikasi dokumentasi dan kolaborasi siap pakai. Penggunaannya dibatasi agar tidak menyimpan atau memproses data kependudukan yang sensitif.
- **Hasil diskusi:** Kelompok memutuskan menggunakan kombinasi IaaS, PaaS, dan SaaS karena setiap komponen memiliki kebutuhan pengelolaan yang berbeda. Portal yang dikembangkan sendiri dibedakan dari aplikasi SaaS yang sudah disediakan oleh penyedia layanan.


## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 20/11/2026 | ChatGPT | Membantu memahami dan mengevaluasi rekomendasi Deployment Model Hybrid Cloud berdasarkan karakteristik NIST. | AI memberikan penjelasan mengenai penerapan on-demand self-service, broad network access, resource pooling, rapid elasticity, dan measured service pada sistem kependudukan. |  Kelompok menggunakan penjelasan tersebut sebagai bahan diskusi, kemudian menyesuaikan contoh penerapan dengan kebutuhan sistem kependudukan.|
| 20/11/2026 | ChatGPT | Meminta penjelasan perbedaan portal informasi yang dikembangkan sendiri dengan aplikasi SaaS siap pakai. | AI menjelaskan bahwa portal yang dikembangkan sendiri lebih sesuai dengan PaaS, sedangkan aplikasi siap pakai dari penyedia layanan termasuk SaaS. | Kelompok meninjau kembali pembagian komponen pada IaaS, PaaS, dan SaaS agar tidak terjadi kesalahan klasifikasi. |
| 20/11/2026 | ChatGPT | Meminta bantuan mengevaluasi risiko dan mitigasi pada penerapan Hybrid Cloud. | AI memberikan masukan mengenai risiko kebocoran data biometrik dan inkonsistensi status kependudukan akibat keterlambatan sinkronisasi data. | Kelompok menggunakan masukan tersebut sebagai bahan evaluasi, kemudian menyesuaikan skenario risiko dan mitigasi dengan arsitektur yang telah dipilih. |
