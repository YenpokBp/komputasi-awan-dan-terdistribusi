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

Risiko 1: Kebocoran Data Biometrik pada Proses Verifikasi Identitas
- Skenario risiko: Jelaskan bahwa instansi mitra seperti bank atau kepolisian mengirimkan permintaan verifikasi identitas. Dalam proses pengiriman permintaan dari Public Cloud menuju Private Cloud, terdapat risiko penyadapan atau kebocoran data biometrik apabila komunikasi tidak diamankan.
- Strategi mitigasi:
  - Melakukan proses pencocokan biometrik sepenuhnya di Private Cloud.
  - Menggunakan enkripsi dan Mutual TLS (mTLS) untuk komunikasi antarkomponen.
  - Tidak menyimpan data biometrik mentah di Public Cloud.
  - Membatasi akses dan menghapus data sementara setelah proses verifikasi selesai.

Risiko 2: Inkonsistensi Status Kependudukan Akibat Keterlambatan Sinkronisasi Data
- Skenario risiko: Ketika terjadi perubahan data penduduk di Private Cloud, seperti pencatatan kematian atau perubahan domisili, informasi yang tersimpan sementara pada layanan pendukung Public Cloud berpotensi belum diperbarui. Akibatnya, informasi lama dapat digunakan dalam proses verifikasi.
- Strategi mitigasi:
  - Menjadikan database Private Cloud sebagai sumber data utama (single source of truth).
  - Menggunakan mekanisme Change Data Capture (CDC) untuk mendeteksi perubahan data.
  - Menerapkan Event-Driven Cache Invalidation untuk menonaktifkan cache atau token lama.
  - Membatasi masa berlaku cache dan melakukan pengecekan ulang ke Private Cloud untuk verifikasi yang bersifat kritis.

4. Bandingkan singkat dengan **satu alternatif yang kalian tolak** — kenapa alternatif itu kurang tepat (mis. kenapa Public Cloud murni ditolak, atau kenapa Private Cloud murni dianggap kurang skalabel).
**Alternatif yang ditolak: Public Cloud murni.** Alasan utamanya adalah bahwa model ini bertentangan langsung dengan syarat studi kasus, yaitu data tidak boleh berada di infrastruktur yang tidak sepenuhnya dikendalikan negara.

Alasan Penolakan

**1. Kedaulatan dan kontrol data tidak terjamin.**
Pada Public Cloud, infrastruktur dimiliki dan dioperasikan penyedia pihak ketiga, dengan *resource pooling* yang berbagi perangkat keras dengan banyak pelanggan lain (*multi-tenant*). Untuk data NIK, alamat, dan biometrik yang sangat rahasia, pemerintah tidak punya kendali penuh atas lokasi fisik data, siapa yang punya akses administratif ke server, maupun hukum negara mana yang dapat menjangkau data tersebut. Ini sulit dipenuhi dengan kewajiban pelindungan data pribadi dalam UU PDP.
 
**2. Risiko biometrik bersifat permanen.**
Seperti pada Risiko 1, data biometrik tidak dapat diganti seperti kata sandi. Jika terjadi kebocoran akibat salah konfigurasi, celah *hypervisor*, atau serangan antar-*tenant*, dampaknya berlaku seumur hidup bagi warga. Pada Public Cloud murni, permukaan serangan ini jauh lebih besar karena seluruh data inti ikut berada di sana.
 
**3. Ketergantungan pada penyedia (*vendor lock-in*).**
Dengan data kependudukan nasional sepenuhnya di satu penyedia komersial, negara bergantung pada kebijakan, harga, dan kelangsungan bisnis penyedia tersebut. Gangguan layanan atau sengketa dapat melumpuhkan layanan identitas nasional.
 
**4. Keunggulan elastisitasnya sudah bisa didapat lewat Hybrid.**
Memang benar Public Cloud unggul dalam *rapid elasticity*, *on-demand self-service*, dan *measured service* untuk menangani lonjakan saat pemilu atau PPDB. Namun keunggulan itu tidak perlu dibayar dengan menyerahkan data inti. Pada Hybrid Cloud, elastisitas tetap dimanfaatkan di lapisan antarmuka dan penerima permintaan, sedangkan data dan proses pencocokan identitas tetap di Private Cloud.

| Aspek | Public Cloud Murni | Hybrid Cloud (pilihan kami) |
|---|---|---|
| Kontrol data inti | Dipegang penyedia pihak ketiga | Penuh di tangan pemerintah (Private) |
| Kepatuhan UU PDP | Sulit dijamin | Terpenuhi, data pribadi tidak keluar dari Private |
| Elastisitas saat lonjakan | Sangat baik | Baik, lewat segmen Public |
| Risiko kebocoran biometrik | Tinggi, permukaan serangan luas | Lebih terkendali dengan mitigasi di jalur verifikasi |
| Ketergantungan vendor | Tinggi | Rendah, data inti tetap milik negara |

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
