# Simulasi "VM Linux kustom" - pakai base image OS penuh, BUKAN slim/alpine
FROM ubuntu:22.04

# Install package yang dibutuhkan untuk skenario Backup Otomatis (cron & rsync)
RUN apt-get update && apt-get install -y cron rsync && rm -rf /var/lib/apt/lists/*

WORKDIR /opt/provision

COPY provision.sh .
RUN chmod +x provision.sh

# Menjalankan provision.sh otomatis saat container start (simulasi user-data script EC2)
ENTRYPOINT ["./provision.sh"]