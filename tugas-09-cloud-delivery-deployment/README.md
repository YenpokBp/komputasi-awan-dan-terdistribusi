# Tugas 9 (Pekan 9) — Cloud Delivery & Deployment Model

**Materi terkait:** Karakteristik esensial cloud computing (NIST SP 800-145), Deployment Model (Public/Private/Hybrid/Community), Service Model (IaaS/PaaS/SaaS).

> Bagian 2 mata kuliah ini murni **analisis & desain di atas kertas** — tidak ada biaya cloud sama sekali, karena tugas berhenti di tahap rekomendasi, bukan implementasi nyata (implementasi baru mulai Tugas 11).

## Studi Kasus

Pemerintah ingin membangun **Sistem Data Kependudukan** (nama, NIK, alamat, data biometrik) yang:
- Sangat **rahasia** (data pribadi warga negara, diatur UU Perlindungan Data Pribadi).
- Diakses oleh **ribuan instansi** (dukcapil daerah, kepolisian, bank untuk verifikasi KYC) dengan pola akses yang **tidak rata** (lonjakan saat musim pemilu/pendaftaran sekolah).
- Butuh **skalabilitas** agar tidak downtime saat lonjakan akses, tapi **tidak boleh** datanya berada di infrastruktur yang tidak terkendali penuh oleh negara.

## Tugas Kelompok

1. **Rekomendasikan Deployment Model** (Public / Private / Hybrid / Community Cloud) yang paling tepat untuk sistem ini. Jelaskan alasannya berdasarkan **karakteristik NIST** (on-demand self-service, broad network access, resource pooling, rapid elasticity, measured service) dikaitkan dengan kebutuhan kerahasiaan vs skalabilitas.

Rekomendasi Deployment Model: Hybrid Cloud [Zaki]
Berdasarkan analisis ketegangan arsitektural antara tuntutan kedaulatan data mutlak dan elastisitas akses massal, model penyebaran yang paling tepat Hybrid Cloud. Arsitektur ini memisahkan beban kerja secara tegas ke dalam dua segmen terintegrasi:
- Segmen Private Cloud (Pusat Data Nasional): Dikelola dan dikendalikan sepenuhnya oleh pemerintah untuk menyimpan basis data inti kependudukan (NIK, biodata, dan template biometrik), menjalankan mesin pencocokan identitas, serta menangani API Gateway internal dan proses verifikasi identitas. Seluruh pemrosesan data pribadi tetap berada dalam lingkungan Private Cloud.
- Segmen Public cloud (Lapisan Antarmuka & Komputasi Publik): Berfungsi sebagai lapisan pendukung yang menyediakan antarmuka informasi umum, portal layanan non-sensitif, serta komponen penerima permintaan awal yang tidak menyimpan atau memproses data pribadi sensitif. Apabila terdapat permintaan verifikasi yang membutuhkan data kependudukan, proses tersebut diteruskan melalui koneksi aman menuju layanan inti di Private Cloud

    1. On-Demand Self-Service: Pengguna dapat menggunakan layanan cloud secara mandiri tanpa bantuan penyedia, misalnya membuat server virtual sendiri.
    2. Broad Network Access: Layanan dapat diakses melalui internet menggunakan berbagai perangkat, seperti laptop, smartphone, dan tablet.
    3. Resource Pooling: Sumber daya komputasi digunakan bersama oleh banyak pengguna secara efisien.
    4. Rapid Elasticity: Kapasitas layanan dapat ditambah atau dikurangi sesuai kebutuhan secara cepat.
    5. Measured Service: Penggunaan layanan dipantau dan dihitung sehingga pengguna membayar sesuai sumber daya yang digunakan.

2. **Rekomendasikan Service Model** (IaaS / PaaS / SaaS)  yang tepat untuk komponen-komponen berbeda dari sistem ini (boleh berbeda service model untuk komponen berbeda, mis. database inti vs portal publik untuk pengecekan status).

Pada sistem ini kami memutuskan untuk menggunakan kombinasi service model IaaS, PaaS, dan SaaS karena ketiga model itu memiliki kebutuhan yang berbeda setiap komponennya. 
- Komponen yang menggunakan IaaS: Server database utama kependudukan, Infrastruktur penyimpanan data NIK dan biometrik, Virtual Machine untuk menjalankan aplikasi inti, Infrastruktur jaringan dan keamanan server. Alasannya IaaS memberikan pemerintah kendali lebih besar terhadap pengelolaan infrastruktur, seperti server, penyimpanan, jaringan, dan sistem operasi. Hal ini penting karena sistem mengelola data pribadi warga yang bersifat rahasia. Jadi fokus utamanya ada pada infrastruktur sehingga dapat mengendalikan server dan penyimpanan data sensitif
- Komponen yang menggunakan PaaS: Platform pengelolaan aplikasi kependudukan, Middleware untuk komunikasi antarlayanan, Platform pengolahan dan pencocokan identitas, Layanan API untuk menghubungkan aplikasi dengan database. Alasannya PaaS membantu tim pengembang mengelola dan menjalankan aplikasi tanpa harus mengatur seluruh infrastruktur server secara manual. Penggunaannya di Private Cloud memungkinkan pemrosesan data sensitif tetap berada dalam lingkungan yang dikendalikan pemerintah. Jadi fokus utamanya ada pada platform aplikasi di mana untuk mempermudah pengembangan dan pengelolaan layanan kependudukan
- Komponen yang menggunakan SaaS: Dashboard monitoring layanan pendukung yang tidak menampilkan data pribadi sensitif, Aplikasi administrasi non-sensitif yang menggunakan perangkat lunak siap pakai dari penyedia layanan, dan Aplikasi dokumentasi dan kolaborasi umum yang sudah tersedia dari penyedia layanan. .Alasannya SaaS memungkinkan pemerintah menggunakan perangkat lunak yang sudah disediakan oleh penyedia layanan tanpa harus membangun dan memelihara aplikasi dari awal. Model ini dapat membantu kegiatan monitoring, administrasi, dan dokumentasi. Namun, layanan SaaS harus dipastikan memiliki keamanan dan kebijakan perlindungan data yang sesuai serta tidak digunakan untuk menyimpan atau memproses data pribadi kependudukan yang sensitif.

Dari penjelasan ini dapat disimpulkan bahwa pembagian ini dapat membantu menjaga kendali data sekaligus mempermudah pengelolaan aplikasi. sehingga kita tidak menggunakan 1 service model saja karena setiap komponennya memiliki kebutuhan pengelolaan yang berbeda

### Perbedaan Portal Informasi dan SaaS

Supaya pembagian service model tidak rancu, berikut perbedaan antara portal informasi yang dikembangkan sendiri oleh pemerintah dan aplikasi SaaS yang sudah tersedia dari penyedia layanan.

| Komponen | Service Model | Penjelasan |
|---|---|---|
| Portal informasi umum yang dibangun dan dikembangkan sendiri oleh pemerintah | PaaS | Pemerintah mengembangkan aplikasinya sendiri dengan memanfaatkan platform cloud. |
| Aplikasi dokumentasi siap pakai dari penyedia layanan | SaaS | Pemerintah langsung menggunakan perangkat lunak yang sudah tersedia. |
| Dashboard monitoring siap pakai dari penyedia layanan | SaaS | Pemerintah menggunakan aplikasi yang sudah disediakan untuk memantau layanan pendukung. |

3. Jelaskan **minimal 2 risiko spesifik** dari pilihan kalian dan mitigasinya (mis. jika Hybrid Cloud dipilih: risiko sinkronisasi data antara private & public segment).

Analisis Risiko Spesifik & Strategi Mitigasi [Zaki]
Penerapan Hybrid Cloud pada sistem identitas nasional menghadirkan tantangan spesifik terkait perlindungan data kependudukan dan akurasi status warga negara:
Risiko 1: Kebocoran Template Biometrik & Rekonstruksi Identitas pada Jalur Verifikasi KYC
- Skenario Risiko: Saat perbankan atau kepolisian melakukan verifikasi wajah maupun sidik jari secara massal melalui segmen Public Cloud, pengiriman data biometrik mentah melintasi batas jaringan
( public-to-private) berisiko mengekspos data biometrik warga. Berbeda dengan kata sandi, data biometrik bersifat permanen seumur hidup dan tidak dapat diganti apabila bocor
- Strategi Mitigasi: Menerapkan Cancelable Biometrics & Feature Extraction di Sisi Klien sebelum permintaan dikirim ke Public Cloud, melalui jalur privat terenkripsi (Dedicated Leased Line dengan Mutual TLS). Proses pencocokan (biometric matching) dilakukan sepenuhnya di dalam Private Cloud negara, sedangkan Public Cloud hanya meneruskan vektor terenkripsi dan mengembalikan skor kecocokan (match score) tanpa pernah menyimpan citra wajah atau NIK mentah
Risiko 2: Inkonsistensi Status Kependudukan (Data Kematian/Perubahan NIK) Saat Lonjakan Pemilu atau PPDB
Skenario Risiko: Pembaruan data penduduk (seperti pencatatan kematian, perubahan domisili, atau status hak pilih oleh Dukcapil daerah) berlangsung langsung di Private Cloud. Apabila lapisan cache pada API Gateway di Public Cloud terlambat tersinkronisasi saat beban akses memuncak, identitas penduduk yang sudah tidak berlaku berpotensi lolos proses verifikasi pemilu atau seleksi
sekolah
- Strategi Mitigasi: Menerapkan mekanisme Event-Driven Cache Invalidation berbasis Change Data Capture (CDC) dari basis data inti di Private Cloud menuju lapisan API Gateway. Setiap perubahan status krusial warga negara secara otomatis memicu penghapusan token verifikasi lama dalam hitungan milidetik (near real-time) tanpa perlu mentransfer rincian data pribadi ke segmen publik

4. Bandingkan singkat dengan **satu alternatif yang kalian tolak** — kenapa alternatif itu kurang tepat (mis. kenapa Public Cloud murni ditolak, atau kenapa Private Cloud murni dianggap kurang skalabel).

## Struktur Submission

```
tugas-09-cloud-delivery-deployment/
├── README.md      # Analisis lengkap (isi dengan poin 1-4 di atas)
├── JURNAL.md
└── bukti/          # (opsional) diagram pendukung
```

## Rubrik Penilaian (Tugas 9)

| Komponen | Bobot | Kriteria |
|---|---|---|
| Ketepatan rekomendasi deployment model | 30% | Argumen berbasis karakteristik NIST, bukan sekadar "private cloud lebih aman" tanpa detail |
| Ketepatan rekomendasi service model | 25% | Pemetaan komponen sistem ke IaaS/PaaS/SaaS masuk akal |
| Analisis risiko & mitigasi | 25% | Risiko spesifik ke konteks data kependudukan (bukan risiko generik) |
| Perbandingan dengan alternatif yang ditolak | 20% | Argumen penolakan jelas dan berdasar |

## Batasan Penggunaan AI (Level 2)

Kebijakan **Level 2 (AI Assisted Idea Generation & Structuring)** berlaku — lihat [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Boleh bertanya ke AI gambaran umum karakteristik NIST/deployment model untuk brainstorming; **tidak boleh** meminta AI menuliskan rekomendasi/analisis akhir yang tinggal ditempel ke `README.md`. Catat pemakaian AI di "Log Penggunaan AI" pada `JURNAL.md`.

- Jawaban yang terasa seperti "template" (bisa dipakai untuk sistem cloud apa saja tanpa menyebut spesifik kependudukan/data pribadi/regulasi) akan dinilai rendah pada komponen ketepatan rekomendasi.
- `README.md` wajib membahas minimal satu skenario tandingan yang kalian buat sendiri (mis. "bagaimana jika instansi daerah tidak punya infrastruktur private cloud sendiri?") beserta jawabannya.
