import time
import math
import pygame
import pytmx
import pyscroll
from player import Player

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.running = True
        self.rotation_droite = True
        self.player = Player()
        self.rotation_gauche = False
        self.clock = pygame.time.Clock()
        self.original_fleche = pygame.image.load('images/fleche.jpg')
        self.original_fleche = pygame.transform.scale(self.original_fleche, (100,100))
        self.rect = self.original_fleche.get_rect(center=(180, 750))
        self.rotated_fleche = self.original_fleche
        self.rotated_rect = self.rect
        self.angle = 0
        self.bande_up = False
        self.bande_down = False
        self.bande = pygame.image.load('images/bande_couleur.png')
        self.bande = pygame.transform.scale(self.bande, (40,220))
        self.curseur = pygame.image.load('images/curseur.png')
        self.curseur = pygame.transform.scale(self.curseur, (50, 20))
        self.phase1 = True
        self.phase2 = False
        self.phase3 = False
        self.phase3 = False
        self.phase4 = False
        self.x_player = 0
        self.y_player = 700
        self.x_bande = self.x_player+90
        self.y_bande = self.y_player-130
        self.vitesse = 0
        self.temps = 0


        #charger la carte tmx
        tmx_data = pytmx.util_pygame.load_pygame('map/map.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data,self.screen.get_size())
        #afficher les calques
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer = 1)

    def handling_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_SPACE]:
            if self.phase3:
                self.bande_up= False
                self.bande_down = False
                self.phase4 = True
                self.phase3 = False
                self.vitesse = -(self.y_bande - 800)/100
                time.sleep(1)
            if self.phase2:
                self.bande_up = False
                self.bande_down = True
                self.phase2 = False
                self.phase3 = True
                time.sleep(0.2)
            if self.phase1:
                self.rotation_droite = False
                self.rotation_gauche = False
                self.bande_down = True
                self.phase2 = True
                self.phase1 = False

        if self.phase4 :
            self.x_player = self.vitesse * math.cos(self.angle) * self.temps
            self.y_player = -(4.9 * (self.temps)**2 + self.vitesse * math.sin(self.angle) * self.temps - (self.y_player - 800))-800
            self.temps += 0.5

        if self.rotation_droite:
            self.angle = (self.angle - 1.3)
            self.rotated_fleche = pygame.transform.rotate(self.original_fleche, self.angle)
            self.rotated_rect = self.rotated_fleche.get_rect(center=self.rect.center)
            if self.angle < -180 :
                self.rotation_droite = False
                self.rotation_gauche = True
        if self.rotation_gauche:
            self.angle = (self.angle + 1.3)
            self.rotated_fleche = pygame.transform.rotate(self.original_fleche, self.angle)
            self.rotated_rect = self.rotated_fleche.get_rect(center=self.rect.center)
            if self.angle > 0 :
                self.rotation_droite = True
                self.rotation_gauche = False
        if self.bande_down:
            self.y_bande += 3
            if self.y_bande >= self.y_player+80:
                self.bande_down = False
                self.bande_up = True
        if self.bande_up:
            self.y_bande -= 3
            if self.y_bande <= self.y_player-140:
                self.bande_down = True
                self.bande_up = False

    def update(self):
        pass

    def display(self):
        self.screen.fill('white')
        self.screen.blit(self.player, (self.x_player, self.y_player))
        if self.phase1 or self.phase2 or self.phase3:
            self.screen.blit(self.rotated_fleche, self.rotated_rect)
            if self.phase2 or self.phase3:
                self.screen.blit(self.bande, (self.x_player+90, self.y_player-130))
                self.screen.blit(self.curseur, (self.x_bande-5,self.y_bande))
        pygame.display.flip()
