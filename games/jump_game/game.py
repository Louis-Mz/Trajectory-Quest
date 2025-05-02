from time import sleep

#import des bibliothèques
import pytmx
import pyscroll
import math
import time
import pygame

#import des classes d'autres fichiers
from player import Player, PLAYER_PARABOLIC, PLAYER_INLINE
from player import Fleche
from player import Bande
from player import Curseur

from collision import Sol
from collision import Obstacle
from collision import Pieu

#constantes
STATE_RUNNING = 0
STATE_WIN = 1
STATE_GAMEOVER = 2
STATE_PIEUX = 3

#classe du jeu
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

        # créer la fleche
        self.fleche = Fleche((self.player.x + 150)*self.map_layer.zoom, (self.player.y-50 )*self.map_layer.zoom)
        self.fleche.add(self.group)
        self.angle = -90

        #initialise la position de la bande de puissance en fonction de la position du joueur
        self.bande=Bande((self.player.x + 90) * self.map_layer.zoom,(self.player.y - 30) * self.map_layer.zoom)
        self.bande_up = True
        self.bande_down = False

        self.liveIcon = pygame.transform.scale(pygame.image.load("games/jump_game/images/Heart-icon.png"), (48,48))

        # initialise la position du curseur selon la position du joueur
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
            #print(objGroups.name)
            for obj in objGroups: #ajout d'instances dans les objets du jeu
                if obj.type == "sol":
                    #print(obj.type, obj.x, obj.y)
                    self.sol.add(Sol(obj.x, obj.y, obj.width, obj.height))
                if obj.type == "obstacle":
                    self.obstacles.add(Obstacle(obj.x, obj.y, obj.width, obj.height))
                if obj.type == "pieu":
                    #print(obj.type, obj.x, obj.y)
                    self.pieux.add(Pieu(obj.x, obj.y, obj.width, obj.height))

    #méthode qui gère les événements clavier/souris
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

    #méthode qui gère les affichages
    def display(self):
        #affichage selon les différentes phase du saut
        if self.phase == 1:
            self.bande.remove(self.group)
            self.curseur.remove(self.group)
            self.fleche.add(self.group)

        elif self.phase == 2 or self.phase == 3:
            if not self.group.has(self.bande):
                self.bande.add(self.group)
            if not self.group.has(self.curseur):
                self.curseur.add(self.group)

        else:
            self.fleche.remove(self.group)
            self.curseur.remove(self.group)
            self.bande.remove(self.group)

        self.group.draw(self.screen)
        ## affichage des victoires et défaites
        #défaite
        if self.state == STATE_GAMEOVER:
            if not self.state == self.previousstate:
                print("Perdu!!!!")
            image = pygame.transform.scale(pygame.image.load("games/jump_game/images/loose.png"), (292, 49))
            rect = image.get_rect()
            rect.center = (int(pygame.display.get_surface().get_width()/2),int(pygame.display.get_surface().get_height() /2))
            self.screen.blit(image,rect)

        #victoire
        elif self.state == STATE_WIN:
            if not self.state == self.previousstate:
                print("Bravo tu as gagné !!!!")
                #modifie la valeur du niveau dans le fichier texte partagé avec le menu principal
                variable_file = "shared_data.txt"
                try:
                    with open(variable_file, "r") as f:
                        value = int(f.read())

                    value += 1

                    with open(variable_file, "w") as f:
                        f.write(str(value))

                except Exception as e:
                    print("Erreur d'accès au fichier :", e)

            ## affichage des instructions en cas de victoire
            GAME_END_MENU = pygame.Rect(0, 0, 900, 300)  # taille du rectangle d'instruction
            GAME_END_MENU.center = (pygame.display.get_surface().get_width()//2, pygame.display.get_surface().get_height()//2 + 10)  # Center in the screen
            pygame.draw.rect(self.screen, (255, 255, 255), GAME_END_MENU)
            end_text_font = pygame.font.SysFont(None, 20)
            end_text = """Mission accomplie, acrobate cosmique !\n
            \n
            Tu as su dompter la gravité et exploiter la puissance de ton saut avec précision.\nChaque trajectoire que tu as dessinée dans l’espace témoigne de ton talent pour la physique du mouvement.\n
            \n
            Tu viens de franchir la première étape de ta quête interstellaire !
            \n
            Mais ce n’était qu’un échauffement... Il est temps de prendre les commandes d’une fusée et de défier les lois\nde l’attraction gravitationnelle dans le mini-jeu suivant : Slingshot Gravity.\n
            \n
            Appuie sur la touche ESPACE pour fermer ce mini-jeu et retourner au menu principal.\n
            \n
            La suite de l’aventure t’attend, astronaute courageux !"""
            lines = end_text.split("\n")
            y = pygame.display.get_surface().get_height()//2 - 300 // 2 + 40  # Position Y de départ
            for line in lines:
                rendered_line = end_text_font.render(line.strip(), True, (0, 0, 0))
                self.screen.blit(rendered_line, (350, y))
                y += 10  # espace entre les lignes

        else:
            #affiche les vies
            for i in range (0,self.lives):
                rectlive =self.liveIcon.get_rect()
                rectlive.center = (25+(50 *i),30)
                self.screen.blit(self.liveIcon, rectlive)
        pygame.display.update()

    def setvariables(self): #méthode qui permet de modifier les valeurs des variables du jeu en cours d'exécution
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

    def managecolisions(self): #méthode de gestion des collisions
       #test collision avec le sol
       colision_list =  pygame.sprite.spritecollide(self.player,self.sol,False)
       for obj in colision_list:
            self.collision_coordinate = (self.player.x, obj.rect.top)
            #print("collision avec le sol (", self.collision_coordinate[0], " , ", self.collision_coordinate[1], ") !!!")
            self.player.setposition(self.collision_coordinate[0], self.collision_coordinate[1]-5)
            self.initphase1()
            return True

       # test si le joueur touche des obstacles
       colision_list = pygame.sprite.spritecollide(self.player, self.obstacles, False)
       for obj in colision_list:
           self.collision_coordinate = (self.player.x, obj.rect.bottom+self.player.rect.height+1)
           #print("collision avec un obstacle (",self.collision_coordinate[0]," , ",self.collision_coordinate[1],") !!!")
           self.player.setposition(self.collision_coordinate[0], self.collision_coordinate[1])
           self.player.movement=PLAYER_INLINE
           return True

       # test si le joueur touche des pieux
       colision_list = pygame.sprite.spritecollide(self.player, self.pieux, False)
       if len(colision_list)>0: # si pieux touché, perd une vie
           #print("collision avec un pieu !!!")
           self.lives=self.lives-1
           #print("il me reste ",self.lives," vie")
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

    def run(self): #boucle du jeu
        self.initphase1()
        blink = 12
        while self.running:
            if self.state == STATE_PIEUX:
                self.player.load_player(1+(blink % 2))
                blink = blink - 1
                if blink == 0:
                    self.player.setposition(self.start_point.x, self.start_point.y)
                    self.map_layer.center((int(pygame.display.get_surface().get_width() / 2),
                                           self.map_layer.map_rect.bottom + int(
                                               pygame.display.get_surface().get_height() / 2)))
                    self.player.load_player(1)
                    self.initphase1()
                    blink = 12
                    self.state = STATE_RUNNING
            self.handling_events()
            self.setvariables()

            if self.phase == 4: #dans l'étape déplacement du joueur
                if self.player.movement == PLAYER_PARABOLIC:
                    # Calcul du déplacement horizontal (deltax) en fonction de la vitesse initiale, de l'angle de tir et du temps écoulé
                    # On convertit l'angle de degrés en radians
                    deltax = (self.vitesse * math.cos((self.angle * math.pi) / 180) * self.temps)
                    # Si l'angle est négatif, c'est un tir vers la gauche, donc on inverse le déplacement horizontal
                    if self.angle < 0:
                        deltax = -deltax
                    # Calcul du déplacement vertical (deltay) en utilisant l'équation de la trajectoire parabolique
                    # Cette équation prend en compte l'angle de tir, la vitesse initiale, le temps écoulé et l'accélération due à la gravité (9.81 m/s²)
                    deltay = deltax * math.tan((self.angle * math.pi) / 180) - ((9.81 * deltax ** 2) / (
                                2 * self.vitesse ** 2 * (math.cos((self.angle * math.pi) / 180) ** 2)))

                    # Application du déplacement au joueur. On multiplie par 10 pour ajuster l'échelle du déplacement en pixels
                    # Le déplacement vertical est négatif car dans Pygame, l'axe Y pointe vers le bas
                    self.player.move_ip(int(10 * deltax), int(-10 * deltay))

                    # défilement horizontal de la carte si le joueur atteint le milieu de l'écran
                    if self.player.x >= (pygame.display.get_surface().get_width() / 2) - self.player.rect.width:
                        self.map_layer.scroll((int(10 * deltax), 0))

                    # défilement vertical de la carte si le joueur atteint le milieu de l'écran verticalement
                    if self.player.y <= (pygame.display.get_surface().get_width() / 2):
                        # Si le joueur monte (deltay est négatif), on fait défiler la carte vers le haut
                        if deltay < 0:
                            self.map_layer.scroll((0, int(-10 * deltay)))
                        # Si le joueur descend (deltay est positif), on fait défiler la carte vers le bas
                        elif deltay > 0:
                            self.map_layer.scroll((0, int(10 * deltay)))

                    # Incrémentation du temps écoulé depuis le début du saut
                    # inverse du nombre d'images par seconde (fps) pour obtenir le temps écoulé entre chaque frame (car f = 1/T)
                    self.temps += (1 / self.clock.get_fps())
                    # si le joueur est en haut de l'écran, on change le mode de déplacement du joueur à PLAYER_INLINE (mouvement linéaire ou au sol)
                    if self.player.y <= 0:
                        self.player.setmotion(PLAYER_INLINE)
                else:
                    #si le mode de déplacement du joueur n'est pas parabolique, on applique un mouvement vertical de -30 vers le bas pour simuler la chute
                    self.player.move_ip(0, 30)

                self.managecolisions()

                #veririfier si le player est hors de l'écran x < 0 x > width
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
                self.clock.tick(60)
            self.display()
            self.previousstate=self.state