"""
Tugas 4 - Jalur A: RPC Server (simulasi modul Pembayaran)
"""

from xmlrpc.server import SimpleXMLRPCServer

# Database simulasi
DATABASE_SALDO = {
    "user1": 150000,
    "user2": 20000
}

def cek_saldo(user_id):
    """Mengembalikan saldo user"""
    return DATABASE_SALDO.get(user_id, 0)

def proses_pembayaran(user_id, jumlah):
    """Memotong saldo jika mencukupi"""
    saldo = DATABASE_SALDO.get(user_id, 0)
    if saldo >= jumlah:
        DATABASE_SALDO[user_id] -= jumlah
        return {"status": "SUCCESS", "sisa_saldo": DATABASE_SALDO[user_id]}
    return {"status": "FAILED", "pesan": "Saldo tidak mencukupi"}

def main():
    server = SimpleXMLRPCServer(("localhost", 8000), allow_none=True)
    print("Server RPC Modul Pembayaran berjalan di http://localhost:8000 ...")
    
    # Registrasi fungsi agar bisa dipanggil client
    server.register_function(cek_saldo, "cek_saldo")
    server.register_function(proses_pembayaran, "proses_pembayaran")
    
    server.serve_forever()

if __name__ == "__main__":
    main()