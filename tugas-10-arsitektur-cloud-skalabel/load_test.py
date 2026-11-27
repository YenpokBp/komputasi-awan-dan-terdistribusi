"""
Tugas 10 - Load Test Sederhana

Mengirim banyak request konkuren ke Load Balancer (http://localhost:8080)
dan menghitung berapa kali masing-masing instance app menangani request,
untuk membuktikan distribusi beban.
"""

import urllib.request
import threading
import time
import statistics
from collections import Counter

TARGET_URL = "http://localhost:8080/"
TOTAL_REQUESTS = 300
CONCURRENCY = 30

hasil = Counter()
latencies = []
latencies_error = []
error_details = Counter()
lock = threading.Lock()
semaphore = threading.Semaphore(CONCURRENCY)

def kirim_request():
    waktu_mulai = None
    try:
        with semaphore:
    # TODO 1: lakukan GET request ke TARGET_URL, baca body response
    # (yang berisi INSTANCE_ID dari app/app.py), lalu update `hasil`
    # (Counter) dengan lock supaya thread-safe.
            waktu_mulai = time.perf_counter()
            with urllib.request.urlopen(TARGET_URL, timeout=5) as resp:
                body = resp.read().decode()
            waktu_selesai = time.perf_counter()
            latensi = waktu_selesai - waktu_mulai
            # TODO 2: ekstrak instance_id dari `body` sesuai format response
            # yang kalian buat di app.py, lalu:
            instance_id = body.split(":")[-1].strip()
            with lock:
                hasil[instance_id] += 1
                latencies.append(latensi)
    except Exception as e:
        if waktu_mulai is not None:
            latensi = time.perf_counter() - waktu_mulai
        else:
            latensi = 0
        with lock:
            hasil["ERROR"] += 1
            latencies_error.append(latensi)
            error_details[str(e)] += 1
def tampilkan_statistik_latensi(judul, data):
    print(f"\n{judul}")

    if not data:
        print("Tidak ada data.")
        return

    data_urut = sorted(data)
    indeks_p95 = max(0, int(0.95 * len(data_urut)) - 1)

    print(f"Jumlah sampel : {len(data)}")
    print(f"Rata-rata     : {statistics.mean(data):.4f} detik")
    print(f"Median        : {statistics.median(data):.4f} detik")
    print(f"Tercepat      : {min(data):.4f} detik")
    print(f"Terlambat     : {max(data):.4f} detik")
    print(f"P95           : {data_urut[indeks_p95]:.4f} detik")

def main():
    print(f"Mengirim {TOTAL_REQUESTS} request dengan concurrency {CONCURRENCY} ...")
    start = time.time()

    threads = []
    for _ in range(TOTAL_REQUESTS):
        t = threading.Thread(target=kirim_request)
        threads.append(t)
        t.start()
        # TODO 3: batasi jumlah thread aktif bersamaan sesuai CONCURRENCY
        # (mis. dengan semaphore, atau proses batch per CONCURRENCY thread).

    for t in threads:
        t.join()
    total_hasil = sum(hasil.values())

    jumlah_berhasil = total_hasil - hasil["ERROR"]
    jumlah_error = hasil["ERROR"]

    print("\nValidasi Request:")
    print(f"Total request dikirim : {TOTAL_REQUESTS}")
    print(f"Request berhasil      : {jumlah_berhasil}")
    print(f"Request gagal (ERROR) : {jumlah_error}")
    print(f"Total hasil tercatat  : {total_hasil}")

    if total_hasil == TOTAL_REQUESTS:
        print("Status                : BERHASIL")
    else:
        print("Status                : TIDAK SESUAI")  

    durasi = time.time() - start
    print(f"\nSelesai dalam {durasi:.2f} detik")
    
    if durasi > 0:
        throughput = jumlah_berhasil / durasi
        print(f"Throughput            : {throughput:.2f} request/detik")

    if TOTAL_REQUESTS > 0:
        print(f"Persentase berhasil   : {jumlah_berhasil / TOTAL_REQUESTS * 100:.2f}%")
        print(f"Persentase error      : {jumlah_error / TOTAL_REQUESTS * 100:.2f}%")

    print("\nDistribusi beban per instance:")
    for instance_id, jumlah in hasil.most_common():
        if instance_id == "ERROR":
            continue

        persentase = (
            jumlah / jumlah_berhasil * 100
            if jumlah_berhasil > 0 else 0
        )
        print(f"  {instance_id}: {jumlah} request ({persentase:.2f}%)")

    if jumlah_error > 0:
        print(f"  ERROR: {jumlah_error} request")

    # Menampilkan statistik latensi
    semua_latencies = latencies + latencies_error

    tampilkan_statistik_latensi(
        "Statistik Latensi - Semua Request",
        semua_latencies
    )

    tampilkan_statistik_latensi(
        "Statistik Latensi - Request Berhasil",
        latencies
    )

    tampilkan_statistik_latensi(
        "Statistik Latensi - Request Gagal",
        latencies_error
    )

    # Menampilkan rincian error
    if error_details:
        print("\nRincian Error:")
        for pesan, jumlah in error_details.most_common():
            print(f"  {jumlah} kali: {pesan}")


if __name__ == "__main__":
    main()
