import pygame
import sys

from util import *
from roket import Roket
from blok import Blok
from target import Target
from populasi import Populasi

pygame.init()
pygame.font.init()

populasi = Populasi(jumlah_individu=50, posisi_spawn=(350, 700))
blok1 = Blok(posisi=(300, 400), lebar=LEBAR_LAYAR - 300, tinggi=15)
blok2 = Blok(posisi=(0, 150), lebar=300, tinggi=15)
target = Target(posisi=(370, 20), lebar=50, tinggi=50)


def gass() -> None:
    jam = pygame.time.Clock()

    while True:
        jam.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        JENDELA.fill(ABU_ABU_2)

        blok1.gambar(JENDELA)
        blok2.gambar(JENDELA)
        target.gambar(JENDELA)

        populasi.gambar_populasi(JENDELA)
        populasi.gerak()
        populasi.cek_tabrakan(blok1, blok2, target)

        populasi.tampilkan_informasi(cetak=True)

        if populasi.apakah_populasi_mati():
            populasi.tampilkan_informasi(cetak=True)
            populasi.buat_generasi_baru()
        pygame.display.update()


if __name__ == "__main__":
    gass()
