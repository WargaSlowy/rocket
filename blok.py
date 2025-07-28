import pygame
from util import Warna


class Blok(pygame.sprite.Sprite):
    def __init__(self, posisi: tuple[int, int], lebar: int, tinggi: int) -> None:
        super().__init__()
        self.posisi: tuple[int, int] = posisi
        self.lebar: int = lebar
        self.tinggi: int = tinggi
        self.rect: pygame.Rect = pygame.Rect(
            self.posisi[0], self.posisi[1], self.lebar, self.tinggi
        )

    def gambar(self, jendela: pygame.Surface) -> None:
        pygame.draw.rect(jendela, Warna.MERAH, self.rect)
