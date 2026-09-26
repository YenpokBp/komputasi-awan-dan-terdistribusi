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

## **Alur Skenario End-to-End:**

### **1. Pelanggan membuat pesanan**

    Pelanggan membuat pesanan melalui Service Pesanan. Komunikasi dilakukan
    secara sinkron karena pelanggan mengirimkan request dan menerima response
    dari Service Pesanan.

### **2. Melakukan pembayaran**

    Setelah pesanan dibuat, Service Pesanan mengirimkan RequestPayment kepada
    Service Pembayaran. Komunikasi dilakukan secara sinkron dengan pola
    request-response.

### **3. Pembayaran berhasil**

    Jika pembayaran berhasil, Service Pembayaran mengirimkan event
    PaymentCompleted ke Message Broker. Komunikasi pada tahap ini dilakukan
    secara asinkron.

### **4. Resto menerima informasi**

    Message Broker meneruskan event PaymentCompleted kepada Service Katalog
    Resto. Resto menerima informasi bahwa pembayaran telah berhasil dan dapat
    memproses pesanan.

### **5. Kurir menerima informasi**

    Message Broker juga meneruskan event PaymentCompleted kepada Service Kurir.
    Setelah menerima informasi tersebut, Kurir dapat melanjutkan proses
    penugasan untuk pesanan.
### Jenis Komunikasi

| Komponen | Komunikasi | Jenis |
|---|---|---|
| Pelanggan dan Service Pesanan | Request dan response | Sinkron |
| Service Pesanan dan Service Pembayaran | RequestPayment | Sinkron / Request-Response |
| Service Pembayaran dan Message Broker | PaymentCompleted | Asinkron / Event |
| Message Broker dan Service Katalog Resto | PaymentCompleted | Asinkron / Event |
| Message Broker dan Service Kurir | PaymentCompleted | Asinkron / Event |

## Trade-Off Publish-Subscribe

Penggunaan arsitektur Publish-Subscribe dapat mengurangi coupling antar-service,
tetapi terdapat beberapa konsekuensi yang perlu diperhatikan.

### 1. Kompleksitas Sistem

Penambahan Message Broker membuat arsitektur menjadi lebih kompleks dibandingkan
komunikasi langsung antar-service. Selain service yang sudah ada, sistem juga
harus mengelola Message Broker sebagai perantara komunikasi.

### 2. Debugging Lebih Sulit

Komunikasi menggunakan event bersifat asynchronous sehingga alurnya tidak selalu
berjalan secara linear. Ketika terjadi kesalahan, proses debugging dapat menjadi
lebih sulit karena perlu ditelusuri dari service pengirim, Message Broker, sampai
service penerima.

### 3. Penanganan Event

Sistem perlu menangani kemungkinan event gagal dikirim, terlambat diproses,
atau diterima lebih dari satu kali. Oleh karena itu, setiap service perlu
memiliki mekanisme yang sesuai untuk menangani kondisi tersebut.

### 4. Ketergantungan terhadap Message Broker

Walaupun service menjadi lebih loosely coupled satu sama lain, service-service
tersebut tetap bergantung pada Message Broker untuk pertukaran event. Jika
Message Broker mengalami masalah, komunikasi asynchronous antar-service dapat
terganggu.

### 5. Skalabilitas dan Fleksibilitas

Di sisi lain, Publish-Subscribe memungkinkan satu event diterima oleh beberapa
subscriber. Service baru juga dapat ditambahkan sebagai subscriber tanpa harus
mengubah secara langsung service yang menghasilkan event. Hal ini memberikan
fleksibilitas ketika sistem FoodGo dikembangkan.

### Kesimpulan Trade-Off

Publish-Subscribe mengurangi komunikasi langsung antar-service sehingga coupling
dapat dikurangi. Namun, keuntungan tersebut disertai konsekuensi berupa
bertambahnya kompleksitas sistem, terutama dalam pengelolaan Message Broker,
debugging asynchronous, dan penanganan event.