import pygame
from game import *
from constants import *

pygame.init()

#création de la fenêtre
pygame.display.set_caption("Gravity Slingshot !") #titre
pygame.display.set_icon(pygame.image.load("mini-jeux/gravitySlingshot/assets/starship.png")) #icon
screen = pygame.display.set_mode((WIDTH, HEIGHT))
game = Game(screen)
game.create_level()
game.run()

pygame.quit()