import pygame
import math
from constants import *

class Starship:
    def __init__(self, screen, x, y, vel_x, vel_y, mass):
        self.screen = screen
        self.x = x
        self.y = y
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.angle = 0
        self.mass = mass
        self.pts = []
        self.image = pygame.image.load("games/gravitySlingshot/assets/starship.png")
        self.image = pygame.transform.scale(self.image, (SHIP_SIZE, SHIP_SIZE))
        self.rect = self.image.get_rect(center=(x, y))
        self.mask = pygame.mask.from_surface(self.image)  # Créez un masque pour le vaisseau

    def move(self, planet = None):
        #Physics : 3rd Newton law !!!
        distance = math.sqrt((self.x - planet.x)**2 + (self.y - planet.y)**2) #distance between planet and starship
        gravitation_force = (G * self.mass * planet.mass) / (distance ** 2) #force vector
        acceleration = gravitation_force / self.mass #2nd Newton law !!! F = ma => a = F/m
        angle = math.atan2(planet.y - self.y, planet.x - self.x) #angle with arctan

        self.vel_x += acceleration * math.cos(angle)
        self.vel_y += acceleration * math.sin(angle)

        self.x += self.vel_x
        self.y += self.vel_y

        self.rect.center = (self.x, self.y)

    def rotate(self, angle_change):
        self.angle += angle_change
        rotated_image = pygame.transform.rotate(
            pygame.transform.scale(pygame.image.load("games/gravitySlingshot/assets/starship.png"), (SHIP_SIZE, SHIP_SIZE)), -self.angle)

        self.image = rotated_image
        self.rect = self.image.get_rect(center=self.rect.center)
        self.mask = pygame.mask.from_surface(self.image)


    def draw(self, x, y, screen):
        #pygame.draw.polygon(self.screen, LIGHT_BLUE, ((self.x, self.y - SHIP_SIZE), (self.x - SHIP_SIZE, self.y + SHIP_SIZE), (self.x + SHIP_SIZE, self.y + SHIP_SIZE)))
        screen.blit(self.image, (x - SHIP_SIZE//2, y - SHIP_SIZE//2))