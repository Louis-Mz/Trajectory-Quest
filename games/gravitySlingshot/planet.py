import pygame
from constants import *

#classe des planètes
class Planet:
    def __init__(self, screen, x, y, mass, size, image):
        self.screen = screen
        self.x = x
        self.y = y
        self.mass = mass
        self.size = size
        self.image = image
        self.image = pygame.transform.scale(self.image, (size, size))
        self.rect = self.image.get_rect(center=(x, y))
        self.mask = pygame.mask.from_surface(self.image)  # Créez un masque pour la planète

    def draw(self):
        self.screen.blit(self.image, (self.x - self.size // 2, self.y - self.size // 2))