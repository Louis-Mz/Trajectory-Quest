import sys
import pygame

from game import Game

pygame.init()
pygame.display.set_caption("Jump Plateformer !") #titre
DESKTOP_SIZE=pygame.display.get_desktop_sizes()[0]
SCREEN_WIDTH=1500
SCREEN_HEIGHT=800

if DESKTOP_SIZE[0] < SCREEN_WIDTH:
    SCREEN_WIDTH = DESKTOP_SIZE[0]-100
if DESKTOP_SIZE[1] < SCREEN_HEIGHT:
    SCREEN_HEIGHT = DESKTOP_SIZE[1] - 100
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
#lancement du jeu
game = Game(screen)
game.run()
pygame.quit()
#sys.exit()