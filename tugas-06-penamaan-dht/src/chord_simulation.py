"""
Tugas 6 - Simulasi Chord DHT (single-process, tanpa jaringan sungguhan)

Fungsi hashing & struktur data ring sudah disediakan.
Implementasi lengkap untuk lookup(), join(), dan leave().
"""

import hashlib

M_BITS = 8               # ruang identifier 0..255 (disederhanakan dari Chord asli yang pakai 160-bit)
RING_SIZE = 2 ** M_BITS


def hash_id(key: str) -> int:
    """Hash string (ID node atau ID kurir) ke ruang identifier 0..RING_SIZE-1."""
    digest = hashlib.sha1(key.encode()).digest()
    return int.from_bytes(digest, "big") % RING_SIZE


class ChordRing:
    def __init__(self):
        # node_id (hasil hash) -> alamat IP node tersebut
        self.nodes: dict[int, str] = {}
        # key kurir (hasil hash) -> (kurir_id, ip_kurir) yang disimpan node penanggung jawab
        self.data: dict[int, tuple[str, str]] = {}

    def join(self, node_name: str, node_ip: str):
        """Tambahkan node baru ke ring. Pindahkan data yang seharusnya
        menjadi tanggung jawab node baru ini dari successor lamanya."""
        node_id = hash_id(node_name)

        # Cari successor lama sebelum node baru dimasukkan ke self.nodes
        old_successor = None
        if self.nodes:
            # Cari successor menggunakan salinan ring tanpa node_id ini
            temp_nodes = {k: v for k, v in self.nodes.items()}
            # Untuk mencari successor lama, kita bisa manfaatkan logika find_successor sementara
            keys_sorted = sorted(temp_nodes.keys())
            candidates = [k for k in keys_sorted if k >= node_id]
            old_successor = candidates[0] if candidates else keys_sorted[0]

        # Tambahkan node_id -> node_ip ke self.nodes
        self.nodes[node_id] = node_ip
        print(f"[JOIN] Node '{node_name}' (id={node_id}) bergabung, alamat {node_ip}")

        # Pindahkan data yang sekarang menjadi tanggung jawab node baru dari successor lama
        if old_successor and old_successor != node_id:
            keys_to_migrate = []
            for key_hash in list(self.data.keys()):
                # Tentukan apakah key ini sekarang jatuh ke node baru.
                # Dalam ring Chord, node baru mengambil alih key yang hash-nya <= node_id 
                # dan sebelumnya dipegang oleh old_successor.
                predecessor = self._get_predecessor(node_id)
                if self._in_interval(key_hash, predecessor, node_id, inclusive_right=True):
                    keys_to_migrate.append(key_hash)

            for kh in keys_to_migrate:
                kurir_id, ip = self.data[kh]
                print(f"  -> Migrasi data kurir '{kurir_id}' (hash={kh}) ke node baru '{node_name}' (id={node_id})")

    def leave(self, node_name: str):
        """Keluarkan sebuah node dari ring. Data yang dipegangnya harus
        berpindah ke successor-nya."""
        node_id = hash_id(node_name)
        if node_id not in self.nodes:
            print(f"[LEAVE] Node '{node_name}' (id={node_id}) tidak ditemukan di ring.")
            return

        # Tentukan successor dari node yang akan keluar
        keys_sorted = sorted(self.nodes.keys())
        idx = keys_sorted.index(node_id)
        successor_id = keys_sorted[(idx + 1) % len(keys_sorted)]
        successor_ip = self.nodes[successor_id]

        # Pindahkan data yang dipegang node ini ke successor-nya
        predecessor_id = self._get_predecessor(node_id)
        migrated_count = 0
        for key_hash in list(self.data.keys()):
            if self._in_interval(key_hash, predecessor_id, node_id, inclusive_right=True):
                kurir_id, ip = self.data[key_hash]
                print(f"  -> Migrasi data kurir '{kurir_id}' (hash={key_hash}) dari node keluar ke successor '{successor_ip}' (id={successor_id})")
                migrated_count += 1

        # Hapus node_id dari self.nodes
        del self.nodes[node_id]
        print(f"[LEAVE] Node '{node_name}' (id={node_id}) keluar dari ring. Total data dimigrasi: {migrated_count}")

    def find_successor(self, key_hash: int) -> int:
        """Cari node_id dengan nilai hash TERKECIL yang >= key_hash
        (successor menurut aturan Chord). Jika tidak ada, wrap-around
        ke node dengan hash terkecil di ring."""
        if not self.nodes:
            raise Exception("Ring kosong, tidak ada node tersedia!")

        keys_sorted = sorted(self.nodes.keys())
        for node_id in keys_sorted:
            if node_id >= key_hash:
                return node_id
        # Wrap-around ke node dengan ID terkecil
        return keys_sorted[0]

    def register_kurir(self, kurir_id: str, ip_kurir: str):
        """Simpan mapping ID Kurir -> IP di node yang bertanggung jawab."""
        key_hash = hash_id(kurir_id)
        target_node = self.find_successor(key_hash)
        self.data[key_hash] = (kurir_id, ip_kurir)
        print(f"[REGISTER] Kurir '{kurir_id}' (hash={key_hash}) disimpan di node ID {target_node} ({self.nodes[target_node]})")

    def lookup(self, kurir_id: str) -> str | None:
        """Cari alamat IP terkini untuk sebuah ID Kurir."""
        key_hash = hash_id(kurir_id)
        if not self.nodes:
            return None
        
        target_node = self.find_successor(key_hash)
        if key_hash in self.data:
            return self.data[key_hash][1]
        
        # Jika data belum terdaftar secara langsung pada key_hash exact match, 
        # cari data terdekat yang dikelola oleh node tersebut atau kembalikan None
        return None

    def _get_predecessor(self, node_id: int) -> int:
        """Mendapatkan node ID yang berada tepat sebelum node_id di ring."""
        keys_sorted = sorted(self.nodes.keys())
        if node_id not in keys_sorted:
            # Cari posisi jika node_id belum masuk
            keys_sorted.append(node_id)
            keys_sorted.sort()
        idx = keys_sorted.index(node_id)
        pred_idx = (idx - 1) % len(keys_sorted)
        return keys_sorted[pred_idx]

    def _in_interval(self, val: int, start: int, end: int, inclusive_right: bool = False) -> int:
        """Helper untuk mengecek apakah val berada di dalam interval (start, end] atau [start, end]."""
        if start < end:
            if inclusive_right:
                return start < val <= end
            return start < val < end
        else: # Wrap-around ring (misal dari 240 ke 15)
            if inclusive_right:
                return val > start or val <= end
            return val > start or val < end


def main():
    ring = ChordRing()

    print("--- Skenario Awal: 4 Node Bergabung ---")
    ring.join("node-jakarta-1", "10.0.0.1")
    ring.join("node-jakarta-2", "10.0.0.2")
    ring.join("node-bandung-1", "10.0.0.3")
    ring.join("node-surabaya-1", "10.0.0.4")

    print("\n--- Pendaftaran Kurir ---")
    ring.register_kurir("kurir-001", "192.168.1.10")
    ring.register_kurir("kurir-002", "192.168.1.11")
    ring.register_kurir("kurir-003", "192.168.1.12")

    print("\n--- Lookup Sebelum Perubahan Topologi ---")
    print("kurir-001 ->", ring.lookup("kurir-001"))
    print("kurir-002 ->", ring.lookup("kurir-002"))

    print("\n--- Node Baru Bergabung ---")
    ring.join("node-medan-1", "10.0.0.5")
    print("kurir-001 ->", ring.lookup("kurir-001"))

    print("\n--- Sebuah Node Keluar ---")
    ring.leave("node-jakarta-1")
    print("kurir-001 ->", ring.lookup("kurir-001"))
    print("kurir-002 ->", ring.lookup("kurir-002"))


if __name__ == "__main__":
    main()