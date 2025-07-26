import pygame
import random
import math
from util import *

Posisi = tuple[int, int]
Vektor = tuple[float, float]
Genom = list[Vektor]

class Roket(pygame.sprite.Sprite):

    def __init__(self, posisi: Posisi, genom: Genom) -> None:
        super().__init__()
        self.posisi: Posisi = posisi
        self.warna: tuple[int, int, int] = HITAM
        self.kecepatan: int = 10
        self.rect: pygame.Rect = pygame.Rect(
            self.posisi[0], self.posisi[1], LEBAR_ROKET, TINGGI_ROKET
        )

        self.genom: Genom = genom
        self.fitness: float = 0.0
        self.langkah: int = 0
        self.mati: bool = False  
        self.mencapai_target: bool = False  
        self.tabrakan_dengan_blok: bool = False  
        self.keluar_dari_batas: bool = False
        self.hukuman_tabrakan: int = 10
        self.hukuman_genom_lengkap: int = 5
        self.genom_lengkap: bool = False

    def gambar(self, jendela: pygame.Surface) -> None:
        pygame.draw.rect(jendela, self.warna, self.rect)

    def gerak(self) -> None:
        if self.langkah < len(self.genom) and not self.mati:
            vektor: Vektor = self.genom[self.langkah]  
            self.rect.x += int(vektor[0])
            self.rect.y += int(vektor[1])
            self.langkah += 1

            if self.langkah >= len(self.genom):
                self.genom_lengkap = True
        else:
            self.mati = True

    def di_luar_batas(self) -> bool:
        if self.rect.x <= 0 or self.rect.x + self.rect.width >= LEBAR_LAYAR:
            return True
        if self.rect.y <= 0 or self.rect.y + self.rect.height >= TINGGI_LAYAR:
            return True
        return False

    def selesai_langkah(self) -> bool:
        return self.langkah >= len(self.genom)

    def evaluasi_fitness(self, target) -> None:
        jarak_ke_target = math.sqrt(
            (self.rect.x - target.rect.x) ** 2 + (self.rect.y - target.rect.y) ** 2
        )
        self.fitness = 1 / (jarak_ke_target + 1) 

        if self.mencapai_target:
            self.fitness += 5
        if self.tabrakan_dengan_blok or self.keluar_dari_batas:
            self.fitness /= 2  

    def mutasi(self, laju_mutasi: float) -> None:
        genom_termutasi: Genom = []
        for gen in self.genom:
            if random.random() < laju_mutasi:
                gen_termutasi = (
                    gen[0] + random.uniform(-1, 1),
                    gen[1] + random.uniform(-1, 1)
                )
            else:
                gen_termutasi = gen
            genom_termutasi.append(gen_termutasi)
        self.genom = genom_termutasi
