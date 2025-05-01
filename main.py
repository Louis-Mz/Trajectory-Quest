import pygame
import subprocess
import time
import os

# Initialisation de pygame
pygame.init()

# Dimensions de la fenêtre
WIDTH, HEIGHT = 1080, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Menu Principal")

SMALL_BUTTON_SIZE = 40

# Couleurs
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)

# Police d'écriture
font = pygame.font.SysFont(None, 60)
long_text_font = pygame.font.SysFont(None, 20)

#images
W1_BACKGROUND = pygame.image.load("assets/window1_bg.jpg")
BACKGROUND = pygame.image.load("assets/menu_bg.jpg")

BUTTON = pygame.image.load("assets/button.png")
BUTTON = pygame.transform.scale(BUTTON, (BUTTON.get_width()*1.05, BUTTON.get_height()*1.05))

INFO_BUTTON = pygame.image.load("assets/info.png")
INFO_BUTTON = pygame.transform.scale(INFO_BUTTON, (SMALL_BUTTON_SIZE, SMALL_BUTTON_SIZE))

SETTINGS_BUTTON = pygame.image.load("assets/settings.png")
SETTINGS_BUTTON = pygame.transform.scale(SETTINGS_BUTTON, (SMALL_BUTTON_SIZE, SMALL_BUTTON_SIZE))

PLAY_BUTTON = pygame.image.load("assets/play_button.png")
PLAY_BUTTON = pygame.transform.scale(PLAY_BUTTON, (PLAY_BUTTON.get_width(), PLAY_BUTTON.get_height()))

EXIT_BUTTON = pygame.image.load("assets/exit_button.png")
EXIT_BUTTON = pygame.transform.scale(EXIT_BUTTON, (EXIT_BUTTON.get_width(), EXIT_BUTTON.get_height()))

# Boutons
level_buttons = [
    {"label": "1", "pos": (126, 347), "command": "python games/jump_game/main.py"},
    {"label": "2", "pos": (518, 150), "command": "python games/gravitySlingshot/main.py"},
    {"label": "3", "pos": (867, 492), "command": "python games/spiderman/spiderman_spiderman_meteor_graph.py"},
]

other_buttons = [
    {"command":"settings", "pos": (940, 20)},
    {"command":"help", "pos": (1010, 20)}
]

w1_buttons = [
    {"label": "JOUER", "pos": (540 - PLAY_BUTTON.get_width()//2, 250 - PLAY_BUTTON.get_height()//2), "command": "play"},
    {"label": "QUITTER", "pos": (540 - EXIT_BUTTON.get_width()//2, 470 - EXIT_BUTTON.get_height()//2), "command": "exit"},
]

# Texte à afficher (chaque \n créera une nouvelle ligne)
long_text = """\n\nAide du jeu\n
\n
Bienvenue dans "La Quête de l’Espace", un jeu où tu expérimentes les lois de la physique du mouvement à travers trois mini-jeux dynamiques !
\n Gravité, balanciers et trajectoires seront tes meilleurs alliés… ou tes pires ennemis !\n
\n
Ton objectif : réussir les trois mini-jeux pour achever ta mission et triompher de cette aventure interstellaire.\n
\n
Comment jouer ?\n
Depuis le menu principal, lance l’un des mini-jeux. Chacun propose une mécanique physique unique à maîtriser.\n
\n
Good Jump Plateformer\n
Un jeu de plateforme pas comme les autres !\n
Utilise une flèche directionnelle et une jauge de puissance oscillante pour te propulser d’un point à l’autre.\n
La gravité agit sur tes sauts, te faisant tracer de belles trajectoires paraboliques.\n
À toi de viser juste pour atteindre les plateformes sans tomber !\n
\n
Slingshot Gravity\n
Prends les commandes d’une fusée lancée depuis le Soleil, avec pour mission d’atteindre un trou noir situé à l’autre bout de l’écran.\n
Les planètes du système solaire (disposées selon leur distance réelle au Soleil) influencent la trajectoire de ta fusée selon la 3ᵉ loi de Newton.\n
Analyse leur position (elle change à chaque partie !) et anticipe les déviations gravitationnelles pour atteindre ta cible.\n
\n
Spiderman Spatial\n
Utilise un fil pour t’accrocher à des points d’ancrage dans l’espace.\n
Quand tu es suspendu, tu te balances comme un balancier ; sinon, c’est la chute libre !\n
Traverse un champ d’astéroïdes, récupère un maximum de pièces, mais évite les obstacles… et surtout, méfie-toi du monstre !\n
\n
Réussis les trois mini-jeux pour terminer la Quête de l’Espace et devenir le maître du mouvement !\n
\n
Bonne chance, astronaute"""

# Découpe le texte en lignes
lines = long_text.split("\n")

INFO_RECT = pygame.Rect(0, 0, 990, 600)  # Taille du rectangle
INFO_RECT.center = (WIDTH // 2, HEIGHT // 2 + 10)  # On place son centre au milieu de l'écran

SETTINGS_RECT = pygame.Rect(0, 0, 900, 500)  # Taille du rectangle
SETTINGS_RECT.center = (WIDTH // 2, HEIGHT // 2 + 10)  # On place son centre au milieu de l'écran

MINI_GAME_RECT = pygame.Rect(0, 0, WIDTH, HEIGHT)  # Taille du rectangle
MINI_GAME_RECT.center = (WIDTH // 2, HEIGHT // 2)  # On place son centre au milieu de l'écran
PLAYING_MINI_GAME = False

LEVEL = 2
WINDOW = 0 #0 = première fenêtre, 1 = fenêtre menu, 2 = aide ?
HELP_OPENED = 0
SETTINGS_OPENED = 0

# ======================= Crée le fichier partagé s'il n'existe pas ====================
variable_file = "shared_data.txt"
if not os.path.exists(variable_file):
    with open(variable_file, "w") as f:
        f.write(str(LEVEL))
with open(variable_file, "w") as f:
    f.write(str(LEVEL))
# =====================================================================================
"""
def is_playing_display():
    print("fonction yes")
    pygame.draw.rect(screen, (0, 0, 0), MINI_GAME_RECT)
    text = font.render("Allez sur la fenêtre du jeu !", True, WHITE)
    # Calculer la position du texte pour le centrer sur le bouton
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)
"""

running = True
while running:
    if WINDOW == 0:
        screen.blit(W1_BACKGROUND, (0, 0))
        screen.blit(PLAY_BUTTON, w1_buttons[0]["pos"])
        screen.blit(EXIT_BUTTON, w1_buttons[1]["pos"])

        # ----------------------------------- handling event -----------------------------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for button in w1_buttons:
                    rect = pygame.Rect(button["pos"], (PLAY_BUTTON.get_width(), PLAY_BUTTON.get_height()))
                    if rect.collidepoint(event.pos):
                        if button["command"] == "play":
                            WINDOW = 1
                        if button["command"] == "exit":
                            running = False

    elif WINDOW == 1:
        # ----------------------------------- display -----------------------------------
        screen.blit(BACKGROUND, (0, 0))
        screen.blit(INFO_BUTTON, other_buttons[1]["pos"])
        screen.blit(SETTINGS_BUTTON, other_buttons[0]["pos"])

        # ============================ LIRE la variable partagée ===========================
        try:
            with open(variable_file, "r") as f:
                new_value = int(f.read())

            if new_value != LEVEL:
                print(f"LEVEL mis à jour : {new_value}")
                LEVEL = new_value
        except Exception as e:
            print("Erreur lecture fichier :", e)
        # =====================================================================================

        # Dessiner les boutons
        for button in level_buttons[:LEVEL]:
            #rect = pygame.Rect(button["pos"], (250, 50))
            #pygame.draw.rect(screen, GREEN, rect)
            screen.blit(BUTTON, button["pos"])
            text = font.render(button["label"], True, WHITE)
            # Calculer la position du texte pour le centrer sur le bouton
            text_rect = text.get_rect(center=(button["pos"][0] + BUTTON.get_width() // 2, button["pos"][1] + BUTTON.get_height() // 2))
            screen.blit(text, text_rect)

        for button in other_buttons:
            if HELP_OPENED:
                pygame.draw.rect(screen, WHITE, INFO_RECT)
                y = 60  # Position Y de départ
                for line in lines:
                    rendered_line = long_text_font.render(line.strip(), True, (0, 0, 0))  # Texte noir
                    screen.blit(rendered_line, (70, y))
                    y += 10  # Espace entre chaque ligne

            if SETTINGS_OPENED:
                pygame.draw.rect(screen, WHITE, SETTINGS_RECT)

        # ----------------------------------- handling event -----------------------------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for button in level_buttons:
                    rect = pygame.Rect(button["pos"], (BUTTON.get_width(), BUTTON.get_height()))
                    if rect.collidepoint(event.pos) and LEVEL >= int(button["label"]) and HELP_OPENED == 0 and SETTINGS_OPENED == 0:
                        #is_playing_display()
                        subprocess.run(button["command"], shell=True)  # Lancer le mini-jeu

                for button in other_buttons:
                    rect = pygame.Rect(button["pos"], (SMALL_BUTTON_SIZE, SMALL_BUTTON_SIZE))
                    if rect.collidepoint(event.pos):
                        if button["command"] == "help":
                            if HELP_OPENED == 0:
                                HELP_OPENED = 1
                                SETTINGS_OPENED = 0

                            elif HELP_OPENED == 1:
                                HELP_OPENED = 0

                        if button["command"] == "settings":
                            if SETTINGS_OPENED == 0:
                                SETTINGS_OPENED = 1
                                HELP_OPENED = 0

                            elif SETTINGS_OPENED == 1:
                                SETTINGS_OPENED = 0

    pygame.display.flip()

    #-----------------------------------------------------------------------------------



pygame.quit()