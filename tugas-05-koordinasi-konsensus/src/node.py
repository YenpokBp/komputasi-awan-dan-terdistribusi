"""
Tugas 5 - Simulasi Node untuk Bully Algorithm

Infrastruktur jaringan (socket server/client) sudah disediakan.
Logika Bully Algorithm (bagian # TODO) sudah dilengkapi.
"""

import argparse
import socket
import threading
import time

ELECTION_TIMEOUT = 2.0  # detik menunggu balasan OK sebelum menyatakan diri leader


class Node:
    def __init__(self, node_id: int, port: int, peers: dict):
        self.node_id = node_id
        self.port = port
        # peers: dict {peer_id: peer_port} untuk semua node LAIN
        self.peers = peers
        self.leader_id = None
        self.lock = threading.Lock()
        self.received_ok = False  # Variabel untuk melacak respons OK

    # ---------- Infrastruktur jaringan (SUDAH LENGKAP, jangan diubah) ----------

    def start_server(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(("localhost", self.port))
        server.listen()
        print(f"[Node {self.node_id}] Listening di port {self.port}")
        while True:
            conn, _ = server.accept()
            threading.Thread(target=self.handle_connection, args=(conn,), daemon=True).start()

    def handle_connection(self, conn: socket.socket):
        with conn:
            data = conn.recv(1024).decode()
            if not data:
                return
            sender_id, msg_type = data.split(":")
            self.on_message(int(sender_id), msg_type)

    def send_message(self, target_port: int, msg_type: str) -> bool:
        """Kirim pesan ke node lain. Return False jika node target tidak merespons (dianggap mati)."""
        try:
            with socket.create_connection(("localhost", target_port), timeout=1.0) as s:
                s.sendall(f"{self.node_id}:{msg_type}".encode())
            return True
        except (ConnectionRefusedError, socket.timeout, OSError):
            return False

    # ---------- Logika Bully Algorithm (SUDAH LENGKAP) ----------

    def on_message(self, sender_id: int, msg_type: str):
        """Dipanggil setiap kali node ini menerima pesan dari node lain."""
        with self.lock:
            if msg_type == "ELECTION":
                print(f"[Node {self.node_id}] Menerima pesan 'ELECTION' dari node {sender_id}")
                if self.node_id > sender_id:
                    # Kirim OK ke node pengirim yang ID-nya lebih kecil
                    target_port = self.peers.get(sender_id)
                    if target_port:
                        self.send_message(target_port, "OK")
                    # Mulai election kita sendiri di background thread
                    threading.Thread(target=self.start_election, daemon=True).start()

            elif msg_type == "OK":
                print(f"[Node {self.node_id}] Menerima pesan 'OK' dari node {sender_id}")
                self.received_ok = True

            elif msg_type == "COORDINATOR":
                self.leader_id = sender_id
                print(f"[Node {self.node_id}] Menerima pesan 'COORDINATOR'. Leader saat ini adalah Node {sender_id}")

            elif msg_type == "PING":
                # Pesan pengecekan kesehatan dari monitor_leader
                pass

    def start_election(self):
        """Dipanggil saat node ini mendeteksi leader tidak ada / tidak merespons."""
        with self.lock:
            self.received_ok = False

        # Ambil peer dengan ID lebih besar dari node kita
        higher_peers = {pid: p for pid, p in self.peers.items() if pid > self.node_id}
        print(f"[Node {self.node_id}] Memulai election ke peer lebih tinggi: {list(higher_peers.keys())}")

        if not higher_peers:
            # Jika tidak ada node yang lebih tinggi, langsung deklarasikan diri sebagai leader
            self.declare_leader()
            return

        sent_any = False
        for pid, port in higher_peers.items():
            success = self.send_message(port, "ELECTION")
            if success:
                sent_any = True

        if not sent_any:
            # Jika tidak ada peer lebih tinggi yang merespons (misal mati), deklarasikan diri sebagai leader
            self.declare_leader()
            return

        # Tunggu balasan OK selama batas waktu ELECTION_TIMEOUT
        time.sleep(ELECTION_TIMEOUT)

        with self.lock:
            if not self.received_ok:
                # Tidak ada respons OK dari node yang lebih tinggi -> kita jadi leader
                self.declare_leader()

    def declare_leader(self):
        """Node ini menyatakan dirinya leader dan memberi tahu semua node lain."""
        with self.lock:
            self.leader_id = self.node_id
        print(f"[Node {self.node_id}] Mengumumkan diri sebagai LEADER (broadcast COORDINATOR)")
        
        # Broadcast pesan COORDINATOR ke SELURUH peer (baik lebih tinggi maupun lebih rendah)
        for pid, port in self.peers.items():
            self.send_message(port, "COORDINATOR")

    def monitor_leader(self):
        """Loop periodik: cek apakah leader masih hidup, trigger election jika mati."""
        while True:
            time.sleep(3)
            with self.lock:
                current_leader = self.leader_id
                my_id = self.node_id

            # Jika kita sendiri adalah leader atau belum ada leader, lewati
            if current_leader == my_id or current_leader is None:
                continue

            # Cek apakah leader saat ini masih hidup
            leader_port = self.peers.get(current_leader)
            if leader_port:
                is_alive = self.send_message(leader_port, "PING")
                if not is_alive:
                    print(f"[Node {self.node_id}] Leader (Node {current_leader}) mati! Memicu pemilihan ulang...")
                    with self.lock:
                        self.leader_id = None
                    threading.Thread(target=self.start_election, daemon=True).start()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--id", type=int, required=True)
    parser.add_argument("--port", type=int, required=True)
    parser.add_argument("--peers", type=str, required=True,
                        help="daftar port peer dipisah koma, mis. 5002,5003,5004,5005")
    args = parser.parse_args()

    peer_ports = [int(p) for p in args.peers.split(",")]
    peers = {port - 5000: port for port in peer_ports}

    node = Node(args.id, args.port, peers)

    threading.Thread(target=node.start_server, daemon=True).start()
    threading.Thread(target=node.monitor_leader, daemon=True).start()

    # Beri jeda proporsional agar node ber-ID lebih tinggi siap lebih stabil
    time.sleep(1.5 + (args.id * 0.1))  
    node.start_election()

    while True:
        time.sleep(60)


if __name__ == "__main__":
    main()