from time import sleep

import pytmx
import pyscroll
import math
import time
import pygame
from pygame.sprite import Sprite, AbstractGroup

from player import Player, PLAYER_PARABOLIC, PLAYER_INLINE
from player import Fleche
from player import Bande
from player import Curseur

from collision import Sol
from collision import Obstacle
from collision import Pieu

STATE_RUNNING = 0
STATE_WIN = 1
STATE_GAMEOVER = 2
STATE_PIEUX = 3

class Game:

    def __init__(self, screen):
        self.screen = screen
        self.running = True
        self.state= STATE_RUNNING
        self.previousstate = STATE_RUNNING
        self.rotation_droite = True
        self.rotation_gauche = False
        self.clock = pygame.time.Clock()
        self.previous_phase=0
        self.lives = 3

        # charger la carte tmx
        tmx_data = pytmx.util_pygame.load_pygame('games/jump_game/map/map.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        self.map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())

        #calcule le zoom pour que la map s'affiche en pleine hauteur
        self.map_layer.zoom = 1 #self.screen.get_size()[1]/self.map_layer.map_rect.height # 0.8
        self.map_layer.scroll((0,self.map_layer.map_rect.height-self.screen.get_size()[1]))

        # afficher les calques
        self.group = pyscroll.PyscrollGroup(map_layer=self.map_layer, default_layer=1)

        # generer joueur
        self.start_point = tmx_data.get_object_by_name("point_apparition")
        self.finish_point =  tmx_data.get_object_by_name("point_arrivee")

        #self.player_position = self.start_point
        self.player = Player(self.start_point.x*self.map_layer.zoom, self.start_point.y*self.map_layer.zoom)
        self.player.add(self.group)
        self.player_previous_position = self.player.getposition()

        # créer fleche
        self.fleche = Fleche((self.player.x + 150)*self.map_layer.zoom, (self.player.y-50 )*self.map_layer.zoom)
        self.fleche.add(self.group)
        self.angle = -90

        #init bande position according to player position
        self.bande=Bande((self.player.x + 90) * self.map_layer.zoom,(self.player.y - 30) * self.map_layer.zoom)
        self.bande_up = True
        self.bande_down = False

        self.liveIcon = pygame.transform.scale(pygame.image.load("games/jump_game/images/Heart-icon.png"), (48,48))

        # init curseur position according to player position
        self.curseur=Curseur(self.bande.rect.centerx * self.map_layer.zoom,self.bande.rect.bottom * self.map_layer.zoom)

        self.phase = 1
        self.vitesse = 0
        self.temps = 0

        #rectangles de collision
        self.sol = pygame.sprite.Group()
        self.obstacles = pygame.sprite.Group()
        self.pieux = pygame.sprite.Group()

        self.collision_coordinate = (0, 0)

        for objGroups in tmx_data.objectgroups:
            print(objGroups.name)
            for obj in objGroups:
                if obj.type == "sol":
                    print(obj.type, obj.x, obj.y)
                    self.sol.add(Sol(obj.x, obj.y, obj.width, obj.height))
                if obj.type == "obstacle":
                    self.obstacles.add(Obstacle(obj.x, obj.y, obj.width, obj.height))
                if obj.type == "pieu":
                    print(obj.type, obj.x, obj.y)
                    self.pieux.add(Pieu(obj.x, obj.y, obj.width, obj.height))

    def handling_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_SPACE]:
            if self.state > 0 : #gagné ou perdu
                self.running = False
            if self.phase==3:
                self.bande_up = False
                self.bande_down = False
                self.phase= 4
                self.vitesse = (self.bande.rect.bottom - self.curseur.rect.centery ) / 15
                time.sleep(1)
            if self.phase==2:
                self.bande_up = False
                self.bande_down = True
                self.phase = 3
                time.sleep(0.2)
            if self.phase==1:
                self.bande_down = True
                self.phase=2
                self.angle=abs(self.angle)-90 # on remet l'angle entre -90° et 90°, 0° est la verticale

    def display(self):
        if self.phase ==1:
            self.bande.remove(self.group)
            self.curseur.remove(self.group)
            self.fleche.add(self.group)
        elif self.phase==2 or self.phase==3:
            if not   self.group.has(self.bande):
                self.bande.add(self.group)
            if not self.group.has(self.curseur):
                self.curseur.add(self.group)
        else:
            self.fleche.remove(self.group)
            self.curseur.remove(self.group)
            self.bande.remove(self.group)
        self.group.draw(self.screen)
        if self.state ==  STATE_GAMEOVER:
            if not self.state == self.previousstate:
                print("Perdu!!!!")
            image = pygame.transform.scale(pygame.image.load("games/jump_game/images/loose.png"), (292, 49))
            rect = image.get_rect()
            rect.center = (int(pygame.display.get_surface().get_width()/2),int(pygame.display.get_surface().get_height() /2))
            self.screen.blit(image,rect)
        elif self.state == STATE_WIN:
            if not self.state == self.previousstate:
                print("Bravo tu as gagné !!!!")
            image = pygame.transform.scale(pygame.image.load("games/jump_game/images/win.png"), (292, 49))
            rect = image.get_rect()
            rect.center = (int(pygame.display.get_surface().get_width()/2),int(pygame.display.get_surface().get_height() /2))
            self.screen.blit(image,rect)
        else:
            #affiche les vies
            for i in range (0,self.lives):
                rectlive =self.liveIcon.get_rect()
                rectlive.center = (25+(50 *i),30)
                self.screen.blit(self.liveIcon, rectlive)
        pygame.display.update()

    def setvariables(self):
        if self.phase == 1:
            if self.rotation_droite:
                self.angle = self.angle - 1.3
                self.fleche.rotate(self.angle,self.screen)
                if self.angle < -180:
                    self.rotation_droite = False
                    self.rotation_gauche = True
            if self.rotation_gauche:
                self.angle = self.angle + 1.3
                self.fleche.rotate(self.angle,self.screen)
                if self.angle > 0:
                    self.rotation_droite = True
                    self.rotation_gauche = False
        if self.phase == 2 or self.phase ==  3:
            if self.bande_down:
                self.curseur.move(0,3)
                if self.curseur.rect.bottom >= self.bande.rect.bottom:
                    self.bande_down = False
                    self.bande_up = True
            if self.bande_up:
                self.curseur.move(0,-3)
                if self.curseur.rect.top <= self.bande.rect.top:
                    self.bande_down = True
                    self.bande_up = False

    def managecolisions(self):
       #test collision avec le sol
       colision_list =  pygame.sprite.spritecollide(self.player,self.sol,False)
       for obj in colision_list:
            self.collision_coordinate = (self.player.x, obj.rect.top)
            print("collision avec le sol (", self.collision_coordinate[0], " , ", self.collision_coordinate[1], ") !!!")
            self.player.setposition(self.collision_coordinate[0], self.collision_coordinate[1]-5)
            self.initphase1()
            return True

       # test si le joueur touche des obstacles
       colision_list = pygame.sprite.spritecollide(self.player, self.obstacles, False)
       for obj in colision_list:
           self.collision_coordinate = (self.player.x, obj.rect.bottom+self.player.rect.height+1)
           print("collision avec un obstacle (",self.collision_coordinate[0]," , ",self.collision_coordinate[1],") !!!")
           self.player.setposition(self.collision_coordinate[0], self.collision_coordinate[1])
           self.player.movement=PLAYER_INLINE
           return True

       # test si le joueur touche des pieux
       colision_list = pygame.sprite.spritecollide(self.player, self.pieux, False)
       #pygame.sprite.spritecollideany(self.player, self.pieux)
       if len(colision_list)>0: # si pieux touché, perd une vie
           print("collision avec un pieu !!!")
           self.lives=self.lives-1
           print("il me reste ",self.lives," vie")
           if self.lives == 0: # si plus de vie alors perdu
               self.player.load_player(2)
               self.state = STATE_GAMEOVER
               self.phase = 5
           else: # sinon retour au point de départ
               self.state = STATE_PIEUX
               self.phase = 5
           return True

        # verifie si on est arrivee
       if  self.player.rect.collidepoint(self.finish_point.x,self.finish_point.y) :
            self.state = STATE_WIN
            self.phase = 5
            return True
       return False

    def initphase1(self):
        self.phase = 1
        self.temps = 0
        self.rotation_droite = True
        self.rotation_gauche = False
        self.angle = -90
        self.player.setmotion(PLAYER_PARABOLIC)
        # on repositionne les objets à côté du player après son déplacement
        self.fleche.setposition((self.player.x + 150 * self.map_layer.zoom), self.player.y - (50 * self.map_layer.zoom))
        self.bande.setposition(self.player.x + (90 * self.map_layer.zoom), self.player.y - (30 * self.map_layer.zoom))
        self.curseur.setposition(self.bande.rect.centerx, self.bande.rect.bottom)

    def run(self):
        self.initphase1()
        blink = 12
        while self.running:
            if self.state==STATE_PIEUX:
                self.player.load_player(1+(blink % 2))
                blink = blink -1
                if blink == 0:
                    self.player.setposition(self.start_point.x, self.start_point.y)
                    self.map_layer.center((int(pygame.display.get_surface().get_width() / 2),
                                           self.map_layer.map_rect.bottom + int(
                                               pygame.display.get_surface().get_height() / 2)))
                    self.player.load_player(1)
                    self.initphase1()
                    blink=12
                    self.state = STATE_RUNNING
            self.handling_events()
            self.setvariables()
            if self.phase == 4: #dans l'étape déplacement du player
                if self.player.movement == PLAYER_PARABOLIC:
                    deltax = (self.vitesse * math.cos((self.angle * math.pi) / 180) * self.temps)
                    if self.angle<0:
                        deltax = -deltax
                    deltay = deltax * math.tan((self.angle * math.pi) / 180) - ((9.81 * deltax ** 2) / (2 * self.vitesse ** 2 * (math.cos((self.angle * math.pi) / 180) ** 2)))
                    self.player.move_ip(int(10 * deltax), int(-10 * deltay))
                    if self.player.x >= (pygame.display.get_surface().get_width()/2) - self.player.rect.width :
                        self.map_layer.scroll((int(10 * deltax ), 0))
                    if self.player.y <= (pygame.display.get_surface().get_width()/2) :
                        if deltay<0:
                            self.map_layer.scroll((0,int(-10 * deltay)))
                        elif deltay>0:
                            self.map_layer.scroll((0, int(10 * deltay)))
                    #if self.player.y >= (pygame.display.get_surface().get_width() / 2) + self.player.rect.height:
                        #self.map_layer.scroll((0, int(10 * deltay)))
                    self.temps += (1 / self.clock.get_fps() )
                    if self.player.y <= 0:
                        self.player.setmotion(PLAYER_INLINE)
                else:
                    self.player.move_ip(0, 30)

                self.managecolisions()

                #veririfier si le player est hors de l'écran x<0 x>width
                if self.player.x <= 0:
                    self.player.setposition(20,self.player.y)
                    self.player.setmotion(PLAYER_INLINE)
                if self.player.x >= self.map_layer.map_rect.width-150:
                    self.player.setposition(self.map_layer.map_rect.width-180, self.player.y)
                    self.player.setmotion(PLAYER_INLINE)
                if self.player.y>=self.map_layer.map_rect.height:
                    self.player.setposition(self.player.x, self.map_layer.map_rect.height-100)
                    self.initphase1()
                self.clock.tick(25)
            else:
                #self.temps=0
                self.clock.tick(60)
            self.display()
            self.previousstate=self.state