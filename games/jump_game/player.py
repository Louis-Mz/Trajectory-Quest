import pygame

PLAYER_PARABOLIC=0
PLAYER_INLINE=1

#classe du joueur
class Player(pygame.sprite.Sprite) :

    def __init__(self, x, y):
#       pygame.sprite.Sprite.__init__(self, self.groups)
        self._layer = 2
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("games/jump_game/images/perso1.png"), (64,104))
        self.rect = self.image.get_rect()
        self.rect.bottomleft =(x,y)
        self.x = x
        self.y = y
        self.movement=PLAYER_PARABOLIC

    #méthode qui charge l'image du joueur
    def load_player(self,item):
        self.image = pygame.transform.scale(pygame.image.load("games/jump_game/images/perso"+str(item)+".png"), (64, 104))

    #méthode qui défini le type de mouvement du joueur (parabole, au sol, ...)
    def setmotion( self,motion):
        self.movement = motion

    #méthode qui renvoie la position du joueur
    def getposition(self):
        return self.x,self.y


    def move_ip(self, deltax, deltay):
        self.rect.move_ip(deltax,deltay)
        # déplace le joueur selon son rect
        self.x = self.rect.left
        self.y = self.rect.bottom
        #print("player position (", self.x, " ,", self.y,")")

    def setposition(self, x, y):
        self.rect.bottomleft = (x, y)
        self.x = self.rect.left
        self.y = self.rect.bottom

#classe de la flèche
class Fleche(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self._layer = 2
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("games/jump_game/images/fleche.jpg"), (80, 80))
        self.surface = self.image.copy()
        self.rect = self.image.get_rect()
        self.position= (0,0)
        self.setposition (x, y)

    #méthode qui place correctement la flèche et son rect
    def setposition(self,x,y):
        self.rect.center = (x,y)
        self.position = (x, y)

    #méthode de rotation de la flèche
    def rotate(self,angle,screen):
        self.image = pygame.transform.rotate(self.surface, angle)
        self.rect = self.image.get_rect(center=self.position)

    def update(self):
        self.rotated_rect.center = self.position

#classe de la bande de puissance de tir
class Bande(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self._layer = 2
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("games/jump_game/images/bande_couleur.png"), (36, 176))
        self.rect = self.image.get_rect()
        self.setposition (x, y)

    def update(self):
        self.rect.center = self.position

    #dessin la bande
    def draw(self, screen):
        self.rect.center = self.position
        screen.blit(self.image, self.rect)

    # méthode qui place correctement la bande et son rect
    def setposition(self,x,y):
        self.rect.center=(x, y)
        self.position = (x, y)

#classe du curseur
class Curseur(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("games/jump_game/images/curseur.png"), (50, 20))
        self.rect = self.image.get_rect()
        self.rect.centerx=x
        self.rect.bottom=y
        self._layer = 3

    def move(self,x, y):
        self.rect.move_ip(x,y)

    #dessin le curseur
    def draw(self, screen):
        screen.blit(self.image, self.rect)

    # méthode qui place correctement le curseur et son rect
    def setposition(self,x,y):
        self.rect.centerx = x
        self.rect.bottom = y