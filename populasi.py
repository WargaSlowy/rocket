import pygame, random
from blok import Blok
from roket import Roket
from target import Target
from util import Warna, Konfigurasi


Posisi = tuple[int, int]


class Populasi:
    def __init__(self, jumlah_individu: int, posisi_spawn: Posisi) -> None:
        self.jumlah_individu: int = jumlah_individu
        self.posisi_spawn: Posisi = posisi_spawn
        self.kromosom: list[Roket] = []
        self.panjang_genom: int = 250
        self.pembuatan_populasi()
        self.roket_induk: list[Roket] = []
        self.ukuran_turnamen: int = 25
        self.nomor_generasi: int = 1
        self.laju_mutasi: float = 0.05

        self.maks_reached_target: int = 0
        self.maks_fitness: float = -1.0
        self.min_fitness: float = -1.0
        self.rata_rata_fitness: float = -1.0

    def pembuatan_populasi(self) -> None:
        for _ in range(self.jumlah_individu):
            genom = self._genom_acak()
            roket = Roket(posisi=self.posisi_spawn, genom=genom)
            self.kromosom.append(roket)

    def gambar_populasi(self, jendela: pygame.Surface) -> None:
        for roket in self.kromosom:
            roket.gambar(jendela)

    def gerak(self) -> None:
        for roket in self.kromosom:
            roket.gerak()

    def _genom_acak(self) -> list[tuple[float, float]]:
        genom: list[tuple[float, float]] = []
        for _ in range(self.panjang_genom):
            vx = random.randint(-Konfigurasi.KECEPATAN_MAKSIMAL_ROKET, Konfigurasi.KECEPATAN_MAKSIMAL_ROKET)
            vy = random.randint(-Konfigurasi.KECEPATAN_MAKSIMAL_ROKET, 0)
            genom.append((vx, vy))
        return genom

    def cek_tabrakan(self, blok1: Blok, blok2: Blok, target: Target) -> None:
        for roket in self.kromosom:
            if roket.mati:
                continue

            if roket.rect.colliderect(blok1.rect) or roket.rect.colliderect(blok2.rect):
                roket.mati = True
                roket.tabrakan_dengan_blok = True

            if roket.rect.colliderect(target.rect):
                roket.mencapai_target = True
                roket.mati = True

            if roket.di_luar_batas():
                roket.mati = True
                roket.keluar_dari_batas = True

            if roket.mati:
                roket.evaluasi_fitness(target)

    def apakah_populasi_mati(self) -> bool:
        return all(roket.mati for roket in self.kromosom)

    def buat_generasi_baru(self) -> None:
        self.nomor_generasi += 1
        self.seleksi_roket_terbaik_turnamen()
        self.kromosom.clear()

        for _ in range(self.jumlah_individu // 2):
            induk1 = random.choice(self.roket_induk)
            induk2 = random.choice(self.roket_induk)

            anak1, anak2 = self._crossover_satu_titik(induk1, induk2)
            anak1.mutasi(self.laju_mutasi)
            anak2.mutasi(self.laju_mutasi)

            self.kromosom.append(anak1)
            self.kromosom.append(anak2)

    def seleksi_roket_terbaik_elit(self) -> None:
        terurut = sorted(self.kromosom, key=lambda r: r.fitness, reverse=True)
        self.roket_induk = terurut[:2]

    def seleksi_roket_terbaik_turnamen(self) -> None:
        self.roket_induk.clear()
        for _ in range(self.jumlah_individu):
            pemenang = self._seleksi_turnamen()
            self.roket_induk.append(pemenang)

    def _crossover_satu_titik(
        self, induk1: Roket, induk2: Roket
    ) -> tuple[Roket, Roket]:
        titik_crossover = random.randint(1, len(induk1.genom) - 1)
        genom1 = induk1.genom[:titik_crossover] + induk2.genom[titik_crossover:]
        genom2 = induk1.genom[titik_crossover:] + induk2.genom[:titik_crossover]

        anak1 = Roket(posisi=self.posisi_spawn, genom=genom1)
        anak2 = Roket(posisi=self.posisi_spawn, genom=genom2)
        return anak1, anak2

    def _seleksi_turnamen(self) -> Roket:
        peserta = random.sample(self.kromosom, self.ukuran_turnamen)
        peserta.sort(key=lambda r: r.fitness, reverse=True)
        return peserta[0]

    def tampilkan_informasi(
        self, cetak: bool = True
    ) -> None:
        semua_fitness = [r.fitness for r in self.kromosom]
        jumlah_mencapai_target = sum(1 for r in self.kromosom if r.mencapai_target)
        self.maks_fitness = max(semua_fitness)
        self.min_fitness = min(semua_fitness)
        self.rata_rata_fitness = sum(semua_fitness) / len(semua_fitness)
        self.maks_reached_target = max(self.maks_reached_target, jumlah_mencapai_target)

        if cetak:
            print(f"\nGenerasi #{self.nomor_generasi}")
            print(f"Fitness maks: {self.maks_fitness:}")
            print(f"Fitness min: {self.min_fitness:}")
            print(f"Rata-rata fitness: {self.rata_rata_fitness:}")
            print(f"Jumlah capai target: {jumlah_mencapai_target}")
        teks = [
            Konfigurasi.FONT.render(f"Generasi #{self.nomor_generasi}", 1, Warna.PUTIH),
            Konfigurasi.FONT.render(f"Fitness maks: {self.maks_fitness:}", 1, Warna.PUTIH),
            Konfigurasi.FONT.render(f"Fitness min: {self.min_fitness:}", 1, Warna.PUTIH),
            Konfigurasi.FONT.render(f"Rata-rata: {self.rata_rata_fitness:}", 1, Warna.PUTIH),
            Konfigurasi.FONT.render(f"Capai target: {jumlah_mencapai_target}", 1, Warna.PUTIH),
        ]

        x, y, jarak = 30, 600, 30
        for t in teks:
            Konfigurasi.JENDELA.blit(t, (x, y))
            y += jarak
