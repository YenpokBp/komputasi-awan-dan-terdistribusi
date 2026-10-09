"""
Tugas 4 - Jalur A: RPC Client (simulasi modul Pesanan)
Jalankan server.py di terminal lain terlebih dahulu.
"""

import xmlrpc.client
import time


def main():
    # TODO 1: buat ServerProxy ke http://localhost:8000
    proxy = xmlrpc.client.ServerProxy("http://localhost:8000")

    print("Memanggil cek_saldo('user1') ... menunggu respons sinkron")
    start = time.time()
    
    # TODO 2: panggil proxy.cek_saldo("user1") dan cetak hasilnya + waktu tempuh
    #         (buktikan client BENAR-BENAR menunggu sampai server membalas)
    saldo = proxy.cek_saldo("user1")
    elapsed = time.time() - start
    print(f"-> Saldo user1: Rp{saldo}")
    print(f"-> Waktu tunggu respons sinkron: {elapsed:.4f} detik\n")

    print("Memanggil proses_pembayaran('user1', 20000) ...")
    
    # TODO 3: panggil proxy.proses_pembayaran("user1", 20000) dan cetak hasilnya
    start_pembayaran = time.time()
    hasil_pembayaran = proxy.proses_pembayaran("user1", 20000)
    elapsed_pembayaran = time.time() - start_pembayaran
    
    print(f"-> Hasil Pembayaran: {hasil_pembayaran}")
    print(f"-> Waktu tunggu proses pembayaran: {elapsed_pembayaran:.4f} detik")


if __name__ == "__main__":
    main()