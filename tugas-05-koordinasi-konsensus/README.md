# Tugas 5 (Pekan 5) — Koordinasi & Konsensus

**Materi terkait:** Physical/Logical Clock, Election Algorithm (Bully/Raft).

## Studi Kasus

Terjadi konflik urutan waktu pada pesanan FoodGo (dua server mencatat urutan pesanan berbeda karena jam tidak sinkron), dan sistem membutuhkan satu **"Node Leader"** untuk mengelola antrean pesanan pusat agar tidak terjadi konflik pemrosesan ganda.

## Tugas Kelompok

Implementasikan simulasi **Bully Algorithm** untuk memilih leader di antara **5 node virtual** yang berjalan sebagai 5 proses Python terpisah di laptop yang sama (tiap node = satu proses di port berbeda, komunikasi lewat TCP socket di `localhost`).

Skeleton yang disediakan (`src/node.py`) sudah menangani bagian **infrastruktur jaringan** (membuka socket, menerima & mengirim pesan antar node) — bagian **algoritma Bully sendiri sengaja dikosongkan** (`# TODO`), karena itu inti pembelajaran tugas ini.

### Aturan Bully Algorithm yang harus diimplementasikan

1. Node yang mendeteksi leader tidak merespons (atau saat start pertama kali) mengirim pesan `ELECTION` ke semua node dengan ID **lebih besar** darinya.
2. Jika ada node ber-ID lebih besar yang merespons `OK`, node yang memulai election **berhenti mencalonkan diri** dan menunggu pesan `COORDINATOR`.
3. Jika **tidak ada** node ber-ID lebih besar yang merespons dalam batas waktu tertentu, node tersebut menjadi leader dan mem-broadcast `COORDINATOR` ke semua node lain.
4. Semua node mencatat siapa leader saat ini.

### Cara Menjalankan

Buka 5 terminal terpisah (satu per node):
```bash
python3 src/node.py --id 1 --port 5001 --peers 5002,5003,5004,5005
python3 src/node.py --id 2 --port 5002 --peers 5001,5003,5004,5005
python3 src/node.py --id 3 --port 5003 --peers 5001,5002,5004,5005
python3 src/node.py --id 4 --port 5004 --peers 5001,5002,5003,5005
python3 src/node.py --id 5 --port 5005 --peers 5001,5002,5003,5004
```

### Skenario Wajib Diuji & Dicatat

1. **Start normal**: nyalakan node 1–5 hampir bersamaan, catat siapa yang terpilih jadi leader (harusnya node ber-ID tertinggi, yaitu node 5).
2. **Leader mati**: matikan (Ctrl+C) proses node leader (node 5), amati node lain mendeteksi leader hilang dan memicu election baru. Catat leader baru yang terpilih (harusnya node 4).
3. Simpan log terminal (screenshot atau `> log_nodeX.txt` redirect) dari kedua skenario ke folder `bukti/`.

## Struktur Submission

```
tugas-05-koordinasi-konsensus/
├── README.md      # Analisis: kenapa perlu leader, kenapa Bully (vs Raft), hasil 2 skenario
├── JURNAL.md
├── src/
│   └── node.py
└── bukti/          # Log/screenshot skenario start normal & leader mati
```

## Rubrik Penilaian (Tugas 5)

| Komponen | Bobot | Kriteria |
|---|---|---|
| Implementasi Bully Algorithm benar | 35% | Election, OK, COORDINATOR message bekerja sesuai aturan algoritma |
| Bukti skenario leader mati → re-election | 30% | Log jelas menunjukkan leader baru terpilih otomatis |
| Analisis (kenapa perlu leader, trade-off Bully vs Raft) | 20% | Dikaitkan ke masalah urutan pesanan di skenario FoodGo |
| Proses & kontribusi kelompok | 15% | `JURNAL.md`, commit history |

## Batasan Penggunaan AI (Level 2)

Kebijakan **Level 2 (AI Assisted Idea Generation & Structuring)** berlaku — lihat [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Boleh bertanya ke AI tentang gambaran umum algoritma election; **tidak boleh** meminta AI menuliskan isi `# TODO` di `src/node.py` (logika `on_message`, `start_election`, `declare_leader`, `monitor_leader`). Catat pemakaian AI di "Log Penggunaan AI" pada `JURNAL.md`.

- `README.md` wajib menjelaskan kenapa Bully Algorithm selalu memilih node ber-ID tertinggi yang masih hidup, dan apa kelemahannya dibanding algoritma lain (mis. jumlah pesan yang dikirim saat election, single point of failure sebelum leader baru terpilih) — bukan sekadar definisi generik.

## Hasil Pengujian

### Skenario 1 - Start Normal
Kelomaima node dijalankan secara bersamaan. Setelah itu proses election, dimana node terpilih sebagai leader karena ia memiliki ID yang tertinggi dibandingkan dengan node lainnya.
Karena node 1, 2, 3, dan menerima pesan coordinator dari node 5 dan menetapkan node 5 sebagai leader

### Skenario 2 - Leader Mati

Node 5 yang sebelumnya menjadi leader kita matikan dengan menggunakan Ctrl+C. Sehingga node lain mendeteksi kalau node 5 itu tidak lagi merespons
Jadi proses election kemudian dijalankan kembali.Kemudian yang terjadi adalah node 4 itu menjadi node dengan id tertinggi yang masih aktif, sehingga node 4 terpilih sebagai leader baru dan mengiirmkan pesan coordinator kepada node lainnya

## Analisis

### Mengapa FoodGo membutuhkan leader?

Dengan adanya leader ini dapat digunakan untuk mengatur koordinasi pemrosesan pesana agar beberapa node tidak memproses pesanan yang sama secara bersamaa. Jadi dengan adanya leader, programa akan mendapat 1 node yang menjadi pusaat koordinasi sehingga urutan pemrosesan pesanan nanti dapat lebih konsisten

### Mengapa menggunakan Bully Algorithm?

Karena Bully Algorithm ini cocok banget digunakan pada simulasi yang seperti ini di mana mekanismenya itu sederhana dan dapat menentukan leader berdasarkan id node tertinggi yang masih aktif. Sehingga waktu leader gagal, node yang lain itu bisa melakukan election juga dan memilih node dengan id tertinggi berikutnya.

### Kelemahan Bully Algirthm

Bagi kami kelemahannya yaitu bisa menghasilkan banyak pesan ketika proses election terjadi, terutama jika jumlah nodenya itu semakin banyak. Selain itu, selama proses pemilihan leader terdapat waktu ketika sistem belum memliki leader juga jadi koordinasinya itu bisa terganggu

### Bully vs Raft

Bully itu lebih sederhana untuk dipahami dan cocok untuk simulasi dengan jumlah node kecil seperti 5 node di tugas ini. Sedangkan raft itu lebih cocok digunakan pada sistem terdistribusi yang membutuhkan koordinsai lebih baik dan data yang tetap konsisten