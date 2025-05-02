import pygame

#classe pour la collision du sol
class Sol(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(x, y, width, height)
        self.position = (x, y)

#classe pour la collision avec les obstacles
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.position = (x, y)

#classe pour la collision avec les pieux
class Pieu(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.position = (x, y)

#classe pour la collision avec l'arrivée
class Arrivee(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(x, y, width, height)
        self.position = (x, y)