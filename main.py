import pygame
import subprocess

# Initialisation de pygame
pygame.init()

# Dimensions de la fenêtre
WIDTH, HEIGHT = 1080, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Menu Principal")

# Couleurs
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)

# Police d'écriture
font = pygame.font.SysFont(None, 60)

#images
BACKGROUND = pygame.image.load("assets/menu_bg.jpg")
BUTTON = pygame.image.load("assets/bouton.png")
BUTTON = pygame.transform.scale(BUTTON, (BUTTON.get_width()*1.05, BUTTON.get_height()*1.05))

# Boutons
buttons = [
    {"label": "1", "pos": (126, 347), "command": "python games/jeu3_pixel/main.py"},
    {"label": "2", "pos": (518, 150), "command": "python games/gravitySlingshot/main.py"},
    {"label": "3", "pos": (867, 492), "command": "python games/jeu2_pygame/main.py"},
]

LEVEL = 2

running = True
while running:
    screen.blit(BACKGROUND, (0, 0))

    # Dessiner les boutons
    for button in buttons[:LEVEL]:
        #rect = pygame.Rect(button["pos"], (250, 50))
        #pygame.draw.rect(screen, GREEN, rect)
        screen.blit(BUTTON, button["pos"])
        text = font.render(button["label"], True, WHITE)
        # Calculer la position du texte pour le centrer sur le bouton
        text_rect = text.get_rect(center=(button["pos"][0] + BUTTON.get_width() // 2, button["pos"][1] + BUTTON.get_height() // 2))
        screen.blit(text, text_rect)

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for button in buttons:
                rect = pygame.Rect(button["pos"], (BUTTON.get_width(), BUTTON.get_height()))
                if rect.collidepoint(event.pos):
                    subprocess.run(button["command"], shell=True)  # Lancer le mini-jeu

pygame.quit()