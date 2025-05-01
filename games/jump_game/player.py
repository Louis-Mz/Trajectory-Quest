import pygame

PLAYER_PARABOLIC=0
PLAYER_INLINE=1

class Player(pygame.sprite.Sprite) :

    def __init__(self, x, y):
#        pygame.sprite.Sprite.__init__(self, self.groups)
        self._layer = 2
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("games/jump_game/images/perso1.png"), (64,104))
        self.rect = self.image.get_rect()
        self.rect.bottomleft =(x,y)
        self.x = x
        self.y = y
        self.movement=PLAYER_PARABOLIC

    def load_player(self,item):
        self.image = pygame.transform.scale(pygame.image.load("games/jump_game/images/perso"+str(item)+".png"), (64, 104))

    def setmotion( self,motion):
        self.movement = motion

    def getposition(self):
        return self.x,self.y

    def move_ip(self,deltax,deltay):
        self.rect.move_ip(deltax,deltay)
        self.x=self.rect.left
        self.y=self.rect.bottom
        print("player position (", self.x, " ,", self.y,")")

    def setposition(self,x,y):
        self.rect.bottomleft =(x,y)
        self.x = self.rect.left
        self.y = self.rect.bottom


class Fleche(pygame.sprite.Sprite):

    def __init__(self, x, y):
        self._layer = 2
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("games/jump_game/images/fleche.jpg"), (80, 80))
        self.surface = self.image.copy()
        self.rect = self.image.get_rect()
        #self.rotated_rect = self.rect
        self.position= (0,0)
        self.setposition (x, y)

    def setposition(self,x,y):
        self.rect.center=(x,y)
        self.position = (x, y)

    def rotate(self,angle,screen):
        self.image = pygame.transform.rotate(self.surface, angle)
        self.rect = self.image.get_rect(center=self.position)

    def update(self):
        self.rotated_rect.center = self.position

class Bande(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self._layer = 2
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("games/jump_game/images/bande_couleur.png"), (36, 176))
        self.rect = self.image.get_rect()
        self.setposition (x, y)

    def update(self):
        self.rect.center = self.position

    def draw(self, screen):
        self.rect.center = self.position
        screen.blit(self.image, self.rect)

    def setposition(self,x,y):
        self.rect.center=(x,y)
        self.position = (x, y)

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

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def setposition(self,x,y):
        self.rect.centerx = x
        self.rect.bottom = y
