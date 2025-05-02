import pygame
from constants import *

#classe du trou noir
class Hole:
    def __init__(self, screen, x, y, mass, size):
        self.screen = screen
        self.x = x
        self.y = y
        self.mass = mass
        self.size = size
        self.image = pygame.image.load("games/gravitySlingshot/assets/black-hole.png")
        self.image = pygame.transform.scale(self.image, (HOLE_SIZE, HOLE_SIZE))
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.mask = pygame.mask.from_surface(self.image)

    #méthode de dessin du trou noir
    def draw(self, x, y, screen):
        screen.blit(self.image, (x - HOLE_SIZE // 2, y - HOLE_SIZE // 2))
