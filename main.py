import pygame
import subprocess

# Initialisation de pygame
pygame.init()

# Dimensions de la fenêtre
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Menu Principal")

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)

# Police d'écriture
font = pygame.font.Font(None, 40)

# Boutons
buttons = [
    {"label": "Gravity Slingshot", "pos": (300, 200), "command": "python games/gravitySlingshot/main.py"},
    {"label": "Mini-Jeu 2 (pygame)", "pos": (300, 300), "command": "python games/jeu2_pygame/main.py"},
    {"label": "Mini-Jeu 3 (pixel)", "pos": (300, 400), "command": "python games/jeu3_pixel/main.py"},
]

running = True
while running:
    screen.fill(WHITE)

    # Dessiner les boutons
    for button in buttons:
        rect = pygame.Rect(button["pos"], (250, 50))
        pygame.draw.rect(screen, GREEN, rect)
        text = font.render(button["label"], True, BLACK)
        screen.blit(text, (button["pos"][0] + 10, button["pos"][1] + 10))

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for button in buttons:
                rect = pygame.Rect(button["pos"], (250, 50))
                if rect.collidepoint(event.pos):
                    subprocess.run(button["command"], shell=True)  # Lancer le mini-jeu

pygame.quit()