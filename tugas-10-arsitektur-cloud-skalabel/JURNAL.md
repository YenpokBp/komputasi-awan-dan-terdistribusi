# Jurnal Proses — Tugas 10

## Setup Nginx & multi-instance
- Kendala saat konfigurasi upstream: File app.py yang digunakan oleh Docker belum diperbarui sesuai dengan perubahan kode terbaru. Hal ini terjadi karena belum dilakukan pengecekan ulang terhadap file yang digunakan oleh container. Setelah menyadari kendala tersebut, dilakukan pembaruan dan penyesuaian kembali pada Docker agar container menggunakan versi app.py terbaru. Selanjutnya, dilakukan pengecekan ulang untuk memastikan aplikasi dapat berjalan sesuai konfigurasi.

## Hasil Load Test Horizontal (3 instance)
- Distribusi request per instance: ...

## Hasil Setelah Scale-up (4 instance)
- Distribusi request per instance: ...

## Hasil Vertical Scaling (1 instance besar)
- Latensi/kegagalan dibanding horizontal: ...

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |
