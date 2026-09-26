# Tugas 2 - Arsitektur Sistem Decouple

**Kelompok:** [yencefran]
| Nama                  | NIM            | Kontribusi                       |
| --------------------- | -------------- | -------------------------------- |
| [Grace Roswita Sallu] | [103072400093] | [Menganalisis kekurangan arsitektur lama dan menyusun skenario] |
| [Yustinus Yendy S.A]  | [103072400065] | [Perancangan arsitektur, message broker, dan diagram]                      |
| [Efran Gustine Y]     | [103072400046] | [Menjelaskan alur skenario, analisis trade-off] |

### **Bukti di Skenario:**

### **Kenapa arsitektur pertama keliru:**
    Karena arsitektur itu membuat setiap layanan memiliki ketergantungan langsung satu sama lain. Di mana jika terdapat perubahan atau terjadi masalah di salah satu service saja, komunikasi dengan service lain juga akan ikut terdampak. Selain itu, semakin banyak layanan yang ditambahkan akan semakin banyak juga hubungan langsung yang harus dikelola

### **Dampak ke FoodGo:**
    Sistem menjadi ketergantungan dengan antar servicenya, jadi sistem semakin sulit dikembangkan dan dimaintenace. Kemudian jika FoodGo ingin menambahkan atau mengubah service, koneksi dengan service lain juga perlu disesuaikan lagi. Sehingga dapat meningkatkan kompleksitas sistem dan membuat proses deplyoment menjadi kurang fleksibel

**Solusi Arsitektur Awal:**

### 1. Memisahkan modul menjadi beberapa service
    Pesanan, pembayaran, resto, dan kurir dapat dipisahkan menjadi service yang memiliki tugas masing-masing 

### 2. Menambahkan Message Broker
    Message broker digunakan sebagai perantara komunikasi antar service. Di mana pesanan dapat mengirim event seperti OrderCreated ke Message Broker, kemudian event tersebut diteruskan kepada resto. Dan pembayaran juga dapat mengirim PaymentCompleted melalui message broker untuk diteruskan ke kurir

## Alur Skenario End-to-End

### Skenario

Pelanggan membuat pesanan, melakukan pembayaran, kemudian Resto menerima informasi
pesanan dan Kurir dapat ditugaskan setelah pembayaran berhasil.

### 1. Pelanggan → Pesanan

Komunikasi dilakukan secara **sinkron**.

- Komponen pengirim: Pelanggan
- Komponen penerima: Service Pesanan
- Jenis komunikasi: Request
- Tujuan: [jelaskan tujuan komunikasi]

### 2. Pesanan → Pembayaran

Komunikasi dilakukan secara **sinkron** dengan pola **request-response**.

- Request: `RequestPayment`
- Pengirim: Service Pesanan
- Penerima: Service Pembayaran
- Alasan menggunakan komunikasi sinkron: [jelaskan alasan]

Setelah menerima request, Service Pembayaran memproses pembayaran dan
mengembalikan hasil pembayaran kepada Service Pesanan.

### 3. Pembayaran → Message Broker

Setelah pembayaran berhasil, Service Pembayaran menghasilkan event
`PaymentCompleted`.

Komunikasi dilakukan secara **asinkron** dengan pola **event**.

- Event: `PaymentCompleted`
- Pengirim: Service Pembayaran
- Penerima: Message Broker
- Alasan menggunakan event: [jelaskan alasan]

### 4. Message Broker → Service Katalog Resto

Service Katalog Resto menjadi subscriber terhadap event yang dikirim melalui
Message Broker.

Komunikasi dilakukan secara **asinkron** dengan pola **event**.

- Event: `PaymentCompleted`
- Pengirim: Message Broker
- Penerima: Service Katalog Resto
- Tindakan setelah menerima event: [jelaskan]

### 5. Message Broker → Service Kurir

Service Kurir juga menerima event yang relevan dari Message Broker.

Komunikasi dilakukan secara **asinkron** dengan pola **event**.

- Event: `PaymentCompleted`
- Pengirim: Message Broker
- Penerima: Service Kurir
- Tindakan setelah menerima event: [jelaskan]

### Ringkasan Komunikasi

| Dari | Ke | Jenis | Pola |
|---|---|---|---|
| Pelanggan | Pesanan | Sinkron | Request |
| Pesanan | Pembayaran | Sinkron | Request-Response |
| Pembayaran | Message Broker | Asinkron | Event |
| Message Broker | Katalog Resto | Asinkron | Event |
| Message Broker | Kurir | Asinkron | Event |