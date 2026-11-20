"""
Tugas 10 - Load Test Sederhana

Mengirim banyak request konkuren ke Load Balancer (http://localhost:8080)
dan menghitung berapa kali masing-masing instance app menangani request,
untuk membuktikan distribusi beban.
"""

import urllib.request
import threading
import time
from collections import Counter

TARGET_URL = "http://localhost:8080/"
TOTAL_REQUESTS = 300
CONCURRENCY = 30

hasil = Counter()
latencies = []
lock = threading.Lock()
semaphore = threading.Semaphore(CONCURRENCY)

def kirim_request():
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
        with lock:
            hasil["ERROR"] += 1
        print(f"Request gagal: {e}")

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

    print("\nValidasi Request:")
    print(f"Total request dikirim : {TOTAL_REQUESTS}")
    print(f"Total hasil tercatat  : {total_hasil}")

    if total_hasil == TOTAL_REQUESTS:
        print("Status                : BERHASIL")
    else:
        print("Status                : TIDAK SESUAI")  

    durasi = time.time() - start
    print(f"\nSelesai dalam {durasi:.2f} detik")
    print("Distribusi beban per instance:")
    for instance_id, jumlah in hasil.most_common():
        print(f"  {instance_id}: {jumlah} request")


if __name__ == "__main__":
    main()
