import pygame
import math
from constants import *

#classe du vaisseau
class Starship:
    def __init__(self, screen, x, y, vel_x, vel_y, mass):
        self.screen = screen
        self.x = x
        self.y = y
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.acc_x = 0
        self.acc_y = 0
        self.angle = 0
        self.boost_charge = BOOST_CHARGE
        self.is_boosted = False
        self.mass = mass
        self.pts = []
        self.image = pygame.image.load("games/gravitySlingshot/assets/starship.png")
        self.image = pygame.transform.scale(self.image, (SHIP_SIZE, SHIP_SIZE))
        self.rect = self.image.get_rect(center=(x, y))
        self.mask = pygame.mask.from_surface(self.image)  # Créez un masque pour le vaisseau
        self.last_update = pygame.time.get_ticks()  # Temps en millisecondes pour les équations horaires


    def move(self, planets):
        current_time = pygame.time.get_ticks()  # Récupérer le temps actuel
        dt = (current_time - self.last_update) / 5 #calcul l'intervalle de temps entre les frames
        self.last_update = current_time  # Mise à jour du temps

        if dt == 0:
            return

        for planet in planets:
            self.move_planet(planet) #applique l'attraction gravitationnelle des planètes au vaisseau
            if self.is_boosted:
                self.boost() #applique la force de propultion du boost

            #équations horaires de position du vaisseau
            self.x += self.vel_x * dt + 0.5 * self.acc_x * dt ** 2
            self.y += self.vel_y * dt + 0.5 * self.acc_y * dt ** 2
            # équations horaires de vitesse du vaisseau
            self.vel_x += self.acc_x * dt
            self.vel_y += self.acc_y * dt

        self.rect.center = (self.x, self.y)

    def move_planet(self, planet):
        dx = planet.x - self.x
        dy = planet.y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2) #distance entre le vaisseau et la planète

        if distance == 0:
            return

        force = (G * self.mass * planet.mass) / (distance ** 2) #3eme loi de Newton F = (m1 * m2)/d²
        angle = math.atan2(dy, dx)

        self.acc_x = (force / self.mass) * math.cos(angle) #accélération selon x
        self.acc_y = (force / self.mass) * math.sin(angle) #accélération selon y

    def boost(self): #boost qui augmente la norme du vecteur accélération selon l'angle du vaisseau
        if self.boost_charge > 0:
            angle_radian = math.radians(self.angle)
            self.acc_x += BOOST * math.cos(angle_radian)
            self.acc_y += BOOST * math.sin(angle_radian)
            self.boost_charge -= 1

    def rotate(self, angle_change): #méthode de rotation du vaisseau
        self.angle += angle_change
        rotated_image = pygame.transform.rotate(
            pygame.transform.scale(pygame.image.load("games/gravitySlingshot/assets/starship.png"), (SHIP_SIZE, SHIP_SIZE)), -self.angle)

        self.image = rotated_image
        self.rect = self.image.get_rect(center=self.rect.center)
        self.mask = pygame.mask.from_surface(self.image)


    def draw(self, x, y, screen): #méthode d'affichage du vaisseau et de la barre de boost
        screen.blit(self.image, (x - SHIP_SIZE//2, y - SHIP_SIZE//2))

        #affichage de la barre de boost
        back_boost_bar = [20, 650, BOOST_CHARGE, 50]
        bar_boost = [25, 655, self.boost_charge - 10, 40]
        pygame.draw.rect(screen, GRAY, back_boost_bar)
        red = 255 - 255 * self.boost_charge / BOOST_CHARGE
        green = 255 * self.boost_charge / BOOST_CHARGE
        blue = 0
        pygame.draw.rect(screen, (red, green, blue), bar_boost)