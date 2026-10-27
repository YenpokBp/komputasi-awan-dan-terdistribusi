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

    def join(self, node_id: str, ip_node: str):
        node_hash = hash_id(node_id)

        print(f"\n[JOIN] Node {node_id} (hash={node_hash}, IP={ip_node}) bergabung")

    # Jika belum ada node, langsung tambahkan
        if not self.nodes:
            self.nodes[node_hash] = ip_node
            print(f"[JOIN] Node {node_id} menjadi node pertama di ring")
            return

    # Cari successor lama sebelum node baru ditambahkan
        old_successor = self.find_successor(node_hash)

    # Tambahkan node baru ke ring menggunakan hash sebagai ID
        self.nodes[node_hash] = ip_node

    # Cari predecessor node baru setelah node ditambahkan
        predecessor_baru = self._get_predecessor(node_hash)

        print(
            f"[JOIN] Node {node_id} (hash={node_hash}) berada di antara "
            f"node {predecessor_baru} dan node {old_successor}"
        )

    # Cari data yang sekarang menjadi tanggung jawab node baru
        migrated = 0

        for key_hash, (kurir_id, ip_kurir) in self.data.items():
            if self._in_interval(
                key_hash,
                predecessor_baru,
                node_hash,
                inclusive_right=True
            ):
                print(
                    f"[MIGRASI] {kurir_id} "
                    f"(hash={key_hash}) : "
                    f"node {old_successor} -> node {node_hash}"
                )
                migrated += 1

        print(
            f"[JOIN] {migrated} data perlu dimigrasikan "
            f"ke node {node_hash}"
        )

    def leave(self, node_id: str):
        node_hash = hash_id(node_id)

        if node_hash not in self.nodes:
            print(f"[LEAVE] Node {node_id} (hash={node_hash}) tidak ditemukan")
            return

        print(
            f"\n[LEAVE] Node {node_id} "
            f"(hash={node_hash}) meninggalkan ring"
        )

    # Cari successor dari node yang akan keluar
        keys_sorted = sorted(self.nodes.keys())
        index = keys_sorted.index(node_hash)

        successor_id = keys_sorted[(index + 1) % len(keys_sorted)]

    # Cari predecessor dari node yang akan keluar
        predecessor_id = self._get_predecessor(node_hash)

        print(
            f"[LEAVE] Node {node_id} (hash={node_hash}) memiliki "
            f"predecessor {predecessor_id} dan successor {successor_id}"
        )

    # Cari data yang harus dimigrasikan ke successor
        migrated = 0

        for key_hash, (kurir_id, ip_kurir) in self.data.items():
            if self._in_interval(
                key_hash,
                predecessor_id,
                node_hash,
                inclusive_right=True
            ):
                print(
                    f"[MIGRASI] {kurir_id} "
                    f"(hash={key_hash}) : "
                    f"node {node_hash} -> node {successor_id}"
                )
                migrated += 1

        print(
            f"[LEAVE] {migrated} data perlu dimigrasikan "
            f"dari node {node_hash} ke node {successor_id}"
        )

    # Hapus node setelah proses migrasi selesai
        del self.nodes[node_hash]

        print(
            f"[LEAVE] Node {node_id} (hash={node_hash}) "
            f"berhasil dihapus dari ring"
        )

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

        target_node = self.find_successor(key_hash)

        print(
            f"[LOOKUP] {kurir_id} -> hash={key_hash}"
            f"-> node-{target_node}"
        )
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