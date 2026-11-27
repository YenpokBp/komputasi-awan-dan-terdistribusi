#!/bin/bash
# Tugas 11 - Script Otomasi Perusahaan (Skenario: Backup Otomatis Terjadwal)

set -euo pipefail

LOG_FILE="/opt/provision/provision.log"
SOURCE_DIR="/data/perusahaan_penting"
BACKUP_DIR="/data/backup_harian"

log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a "$LOG_FILE"
}

log "Provisioning dimulai - simulasi VM baru menyala"

# 1. Membuat direktori sumber dan tujuan backup + file dummy perusahaan
mkdir -p "$SOURCE_DIR" "$BACKUP_DIR"
echo "Laporan Keuangan Q4 2026 - Rahasia" > "$SOURCE_DIR/laporan_keuangan.txt"
echo "Database Pelanggan FoodGo" > "$SOURCE_DIR/db_pelanggan.sql"
log "Direktori sumber ($SOURCE_DIR) dan file dummy berhasil dibuat."

# 2. Menyalakan service cron di dalam container
service cron start
log "Service cron berhasil dijalankan."

# 3. Menjadwalkan backup otomatis setiap 1 menit menggunakan rsync ke crontab
# (Dalam produksi nyata biasanya diatur harian misal '0 2 * * *', di sini '*/1 * * * *' untuk simulasi)
CRON_JOB="*/1 * * * * rsync -av --delete $SOURCE_DIR/ $BACKUP_DIR/backup-\$(date +\%Y\%m\%d-\%H\%M)/ >> $LOG_FILE 2>&1"
(crontab -l 2>/dev/null || true; echo "$CRON_JOB") | crontab -
log "Cron job backup otomatis berhasil didaftarkan."

log "Provisioning selesai - VM siap beroperasi."

# Jaga container tetap hidup agar cron berjalan di background dan bisa diamati
tail -f /dev/null