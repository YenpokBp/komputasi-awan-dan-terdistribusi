"""
Tugas 6 - Simulasi Chord DHT (single-process, tanpa jaringan sungguhan)

Fungsi hashing & struktur data ring sudah disediakan.
Lengkapi TODO untuk lookup(), join(), dan leave().
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
        # key kurir (hasil hash) -> IP kurir yang disimpan node yang bertanggung jawab
        self.data: dict[int, tuple[str, str]] = {}  # hash -> (kurir_id, ip_kurir)

    def join(self, node_name: str, node_ip: str):
        """Tambahkan node baru ke ring. Pindahkan data yang seharusnya
        menjadi tanggung jawab node baru ini dari successor lamanya."""
        node_id = hash_id(node_name)

        # Cari successor LAMA dulu, SEBELUM node baru dimasukkan ke ring
        old_successor = None
        if self.nodes:
            keys_sorted = sorted(self.nodes.keys())
            candidates = [k for k in keys_sorted if k >= node_id]
            old_successor = candidates[0] if candidates else keys_sorted[0]

        # Masukkan node baru ke ring
        self.nodes[node_id] = node_ip
        print(f"[JOIN] Node '{node_name}' (id={node_id}) bergabung, alamat {node_ip}")

        # Pindahkan key yang sekarang jadi tanggung jawab node baru,
        # yaitu key di interval (predecessor_baru, node_id_baru]
        if old_successor and old_successor != node_id:
            for key_hash in list(self.data.keys()):
                predecessor = self._get_predecessor(node_id)
                if self._in_interval(key_hash, predecessor, node_id, inclusive_right=True):
                    kurir_id, ip = self.data[key_hash]
                    print(f"  -> Migrasi data kurir '{kurir_id}' (hash={key_hash}) ke node baru '{node_name}' (id={node_id})")

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

        # Key yang dipegang node yang mau keluar = interval (predecessor, node_id]
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
        ke node dengan hash terkecil di ring (karena ring melingkar)."""
        # TODO 6: implementasikan logika successor di atas menggunakan
        # self.nodes.keys(). Kembalikan node_id (bukan IP).
        if not self.nodes:
            raise Exception("Ring kosong, tidak ada node tersedia!")

        keys_sorted = sorted(self.nodes.keys())
        for node_id in keys_sorted:
            if node_id >= key_hash:
                return node_id
        return keys_sorted[0]  # wrap-around ke node dengan ID terkecil

    def register_kurir(self, kurir_id: str, ip_kurir: str):
        """Simpan mapping ID Kurir -> IP di node yang bertanggung jawab."""
        key_hash = hash_id(kurir_id)
        # TODO 7: panggil find_successor(key_hash) untuk menentukan node
        # penanggung jawab, lalu simpan (kurir_id, ip_kurir) ke self.data[key_hash].
        target_node = self.find_successor(key_hash)
        self.data[key_hash] = (kurir_id, ip_kurir)
        print(f"[REGISTER] Kurir '{kurir_id}' (hash={key_hash}) disimpan di node ID {target_node} ({self.nodes[target_node]})")

    def lookup(self, kurir_id: str) -> str | None:
        """Cari alamat IP terkini untuk sebuah ID Kurir."""
        key_hash = hash_id(kurir_id)
        # TODO 8: gunakan find_successor(key_hash) untuk menemukan node
        # penanggung jawab, lalu kembalikan ip_kurir dari self.data jika ada.
        if not self.nodes:
            return None

        self.find_successor(key_hash)  # memastikan ring valid / tidak error
        if key_hash in self.data:
            return self.data[key_hash][1]
        return None

    def _get_predecessor(self, node_id: int) -> int:
        """Mendapatkan node ID yang berada tepat sebelum node_id di ring."""
        keys_sorted = sorted(self.nodes.keys())
        if node_id not in keys_sorted:
            keys_sorted.append(node_id)
            keys_sorted.sort()
        idx = keys_sorted.index(node_id)
        pred_idx = (idx - 1) % len(keys_sorted)
        return keys_sorted[pred_idx]

    def _in_interval(self, val: int, start: int, end: int, inclusive_right: bool = False) -> bool:
        """Helper untuk mengecek apakah val berada di dalam interval (start, end] atau (start, end)."""
        if start < end:
            if inclusive_right:
                return start < val <= end
            return start < val < end
        else:  # Wrap-around ring (misal dari 240 ke 15)
            if inclusive_right:
                return val > start or val <= end
            return val > start or val < end


def main():
    ring = ChordRing()

    # Skenario awal: 4 node bergabung
    ring.join("node-jakarta-1", "10.0.0.1")
    ring.join("node-jakarta-2", "10.0.0.2")
    ring.join("node-bandung-1", "10.0.0.3")
    ring.join("node-surabaya-1", "10.0.0.4")

    # Daftarkan beberapa kurir
    ring.register_kurir("kurir-001", "192.168.1.10")
    ring.register_kurir("kurir-002", "192.168.1.11")
    ring.register_kurir("kurir-003", "192.168.1.12")

    print("\n--- Lookup sebelum perubahan topologi ---")
    print("kurir-001 ->", ring.lookup("kurir-001"))
    print("kurir-002 ->", ring.lookup("kurir-002"))

    print("\n--- Node baru bergabung ---")
    ring.join("node-medan-1", "10.0.0.5")
    print("kurir-001 ->", ring.lookup("kurir-001"))

    print("\n--- Sebuah node keluar ---")
    ring.leave("node-jakarta-1")
    print("kurir-001 ->", ring.lookup("kurir-001"))
    print("kurir-002 ->", ring.lookup("kurir-002"))


if __name__ == "__main__":
    main()