import pygame
from dataclasses import dataclass

pygame.font.init()


@dataclass(frozen=True)
class Warna:
    HITAM: tuple[int, int, int] = (0, 0, 0)
    PUTIH: tuple[int, int, int] = (255, 255, 255)
    MERAH: tuple[int, int, int] = (255, 69, 0)
    ABU_ABU: tuple[int, int, int] = (65, 64, 90)
    BIRU: tuple[int, int, int] = (30, 144, 255)
    HIJAU: tuple[int, int, int] = (0, 255, 0)
    EMAS: tuple[int, int, int] = (255, 185, 15)
    COKLAT: tuple[int, int, int] = (184, 134, 11)
    ABU_ABU_2: tuple[int, int, int] = (100, 100, 100)


@dataclass(frozen=True)
class Konfigurasi:
    LEBAR_LAYAR: int = 700
    TINGGI_LAYAR: int = 750

    FONT: pygame.font.Font = pygame.font.SysFont("Arial", 20)
    FPS: int = 60

    LEBAR_ROKET: int = 10
    TINGGI_ROKET: int = 20
    KECEPATAN_MAKSIMAL_ROKET: int = 5


    JENDELA: pygame.Surface = pygame.display.set_mode(
        (LEBAR_LAYAR, TINGGI_LAYAR)
    )
    JENDELA.fill(Warna.ABU_ABU_2)
