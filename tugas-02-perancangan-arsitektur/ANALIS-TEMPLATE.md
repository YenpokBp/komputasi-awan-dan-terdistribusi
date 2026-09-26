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

### **Skenario**

    Pelanggan membuat pesanan di FoodGo lalu melakukan pembayaran. Setelah
    pembayaran berhasil, informasi pesanan dikirim melalui Message Broker
    sehingga Resto dan Kurir dapat menerima informasi tersebut.

### **1. Pelanggan membuat pesanan**

    Pelanggan mengirimkan pesanan ke Service Pesanan. Komunikasi pada tahap
    ini dilakukan secara sinkron karena pelanggan mengirimkan request dan
    Service Pesanan memberikan response.

### **2. Pesanan melakukan pembayaran**

    Setelah pesanan diterima, Service Pesanan mengirimkan RequestPayment kepada
    Service Pembayaran. Komunikasi dilakukan secara sinkron dengan pola
    request-response. Service Pesanan menunggu hasil pembayaran sebelum
    melanjutkan ke proses berikutnya.

### **3. Pembayaran berhasil**

    Jika pembayaran berhasil, Service Pembayaran membuat event PaymentCompleted.
    Event tersebut dikirimkan ke Message Broker. Komunikasi pada tahap ini
    bersifat asinkron karena Service Pembayaran tidak berkomunikasi langsung
    dengan Resto dan Kurir.

### **4. Resto menerima informasi pesanan**

    Message Broker meneruskan event PaymentCompleted kepada Service Katalog
    Resto sebagai subscriber. Setelah menerima event tersebut, Resto mengetahui
    bahwa pembayaran telah berhasil dan dapat melanjutkan proses pesanan.

### **5. Kurir menerima informasi**

    Service Kurir juga menerima event PaymentCompleted dari Message Broker.
    Setelah mendapatkan informasi bahwa pembayaran telah berhasil, Kurir dapat
    melanjutkan proses penugasan untuk pesanan tersebut.

### Jenis Komunikasi

| Komponen | Komunikasi | Jenis |
|---|---|---|
| Pelanggan dan Service Pesanan | Request dan response | Sinkron |
| Service Pesanan dan Service Pembayaran | `RequestPayment` | Sinkron / Request-Response |
| Service Pembayaran dan Message Broker | `PaymentCompleted` | Asinkron / Event |
| Message Broker dan Service Katalog Resto | `PaymentCompleted` | Asinkron / Event |
| Message Broker dan Service Kurir | `PaymentCompleted` | Asinkron / Event |