import time

import pygame
import math
import random
from constants import *
from starship import Starship
from planet import Planet
from black_hole import Hole

#classe du jeu
class Game:
    def __init__(self, screen):
        self.screen = screen
        self.key_pressed = {}
        self.running = True
        self.clock = pygame.time.Clock()
        self.starship = None
        self.planets = []
        self.black_hole = Hole(self.screen, HOLE_X, HEIGHT//2, HOLE_MASS, HOLE_SIZE)
        self.temp_ship_pos = None
        self.mouse_pos = None
        self.level = 1
        self.win = False

    #fonctions utiles
    def create_starship(self, temp_pos, mouse_pos): #créer le vaisseau avec la souris
        t_x, t_y = temp_pos
        m_x, m_y = mouse_pos
        vel_x = (-m_x + t_x) / VEL_SCALE #calcul du vecteur vitesse selon l'axe x
        vel_y = (-m_y + t_y) / VEL_SCALE #calcul du vecteur vitesse selon l'axe y
        starship = Starship(self.screen, t_x, t_y, vel_x, vel_y, SHIP_MASS)
        return starship

    def create_solar_system(self): #créer le système solaire entier (fonction qui n'est plus utile lorsqu'on s'arrête au niveau 4)
        Mercure = Planet(self.screen, MERCURE_X, random.randint(0, HEIGHT), MERCURE_MASS, MERCURE_SIZE, MERCURE_IMAGE)
        self.planets.append(Mercure)

        Venus = Planet(self.screen, VENUS_X, random.randint(0, HEIGHT), VENUS_MASS, VENUS_SIZE, VENUS_IMAGE)
        self.planets.append(Venus)

        Terre = Planet(self.screen, EARTH_X, random.randint(0, HEIGHT), EARTH_MASS, EARTH_SIZE, EARTH_IMAGE)
        self.planets.append(Terre)

        Mars = Planet(self.screen, MARS_X, random.randint(0, HEIGHT), MARS_MASS, MARS_SIZE, MARS_IMAGE)
        self.planets.append(Mars)

        Jupiter = Planet(self.screen, JUPITER_X, random.randint(0, HEIGHT), JUPITER_MASS, JUPITER_SIZE, JUPITER_IMAGE)
        self.planets.append(Jupiter)

        Saturn = Planet(self.screen, SATURN_X, random.randint(0, HEIGHT), SATURN_MASS, SATURN_SIZE, SATURN_IMAGE)
        self.planets.append(Saturn)

        Uranus = Planet(self.screen, URANUS_X, random.randint(0, HEIGHT), URANUS_MASS, URANUS_SIZE, URANUS_IMAGE)
        self.planets.append(Uranus)

        Neptune = Planet(self.screen, NEPTUNE_X, random.randint(0, HEIGHT), NEPTUNE_MASS, NEPTUNE_SIZE, NEPTUNE_IMAGE)
        self.planets.append(Neptune)

        Pluton = Planet(self.screen, PLUTON_X, random.randint(0, HEIGHT), PLUTON_MASS, PLUTON_SIZE, PLUTON_IMAGE)
        self.planets.append(Pluton)

    def create_level(self): #fonction qui créer les niveaux définis dans le fichier constantes
        #fichier utilisé pour communiquer entre les mini-jeux et l'interface menu
        variable_file = "shared_data.txt"

        if self.level <= 4:
            current_level = levels[self.level - 1]
        if self.level == 1:
            Mercure = Planet(self.screen, current_level["mercure"][0], current_level["mercure"][1], MERCURE_MASS, MERCURE_SIZE, MERCURE_IMAGE)
            self.planets.append(Mercure)

            Venus = Planet(self.screen, current_level["venus"][0], current_level["venus"][1], VENUS_MASS, VENUS_SIZE, VENUS_IMAGE)
            self.planets.append(Venus)

            Terre = Planet(self.screen, current_level["earth"][0], current_level["earth"][1], EARTH_MASS, EARTH_SIZE, EARTH_IMAGE)
            self.planets.append(Terre)

        elif self.level == 2:
            Terre = Planet(self.screen, current_level["earth"][0], current_level["earth"][1], EARTH_MASS, EARTH_SIZE, EARTH_IMAGE)
            self.planets.append(Terre)

            Mars = Planet(self.screen, current_level["mars"][0], current_level["mars"][1], MARS_MASS, MARS_SIZE, MARS_IMAGE)
            self.planets.append(Mars)

            Jupiter = Planet(self.screen, current_level["jupiter"][0], current_level["jupiter"][1], JUPITER_MASS, JUPITER_SIZE,
                             JUPITER_IMAGE)
            self.planets.append(Jupiter)

        elif self.level == 3:
            Jupiter = Planet(self.screen, current_level["jupiter"][0], current_level["jupiter"][1], JUPITER_MASS, JUPITER_SIZE,
                             JUPITER_IMAGE)
            self.planets.append(Jupiter)

            Saturn = Planet(self.screen, current_level["saturn"][0], current_level["saturn"][1], SATURN_MASS, SATURN_SIZE, SATURN_IMAGE)
            self.planets.append(Saturn)

            Uranus = Planet(self.screen, current_level["uranus"][0], current_level["uranus"][1], URANUS_MASS, URANUS_SIZE, URANUS_IMAGE)
            self.planets.append(Uranus)

        elif self.level == 4:
            Uranus = Planet(self.screen, current_level["uranus"][0], current_level["uranus"][1], URANUS_MASS, URANUS_SIZE, URANUS_IMAGE)
            self.planets.append(Uranus)

            Neptune = Planet(self.screen, current_level["neptune"][0], current_level["neptune"][1], NEPTUNE_MASS, NEPTUNE_SIZE,
                             NEPTUNE_IMAGE)
            self.planets.append(Neptune)

            Pluton = Planet(self.screen, current_level["pluton"][0], current_level["pluton"][1], PLUTON_MASS, PLUTON_SIZE, PLUTON_IMAGE)
            self.planets.append(Pluton)

        else:
            self.win = True
            self.create_solar_system()

            #modifie la valeur de LEVEL dans le fichier texte partagé
            try:
                with open(variable_file, "r") as f:
                    value = int(f.read())

                value += 1

                with open(variable_file, "w") as f:
                    f.write(str(value))

            except Exception as e:
                print("Erreur d'accès au fichier :", e)

    #fonction d'affichage de victoire/fin de mini-jeu
    def end_game(self):
        GAME_END_MENU = pygame.Rect(0, 0, 900, 300)  # rectangle size
        GAME_END_MENU.center = (WIDTH // 2, HEIGHT // 2 + 10)  # Center in the screen
        pygame.draw.rect(self.screen, WHITE, GAME_END_MENU)
        end_text_font = pygame.font.SysFont(None, 20)
        end_text = """Bravo, aventurier de l’espace !\n
        \n
        Tu as brillamment maîtrisé les lois de la gravitation et piloté ta fusée à travers l’univers instable des champs planétaires.\n
        \n
        Grâce à ton sens de l'anticipation et à ta compréhension des forces cosmiques, tu as atteint le redoutable trou noir sans te perdre\ndans le vide intersidéral.\n
        \n
        Ta mission est loin d’être terminée ! Une dernière épreuve t’attend : le Spiderman Spatial.\n
        \n
        Ferme ce mini-jeu pour retourner au menu principal, et poursuis ta quête intergalactique vers le titre de Maître du Mouvement !"""
        lines = end_text.split("\n")
        y = HEIGHT // 2 - 300//2 + 40  # Position Y de départ
        for line in lines:
            rendered_line = end_text_font.render(line.strip(), True, (0, 0, 0))  # Black text
            self.screen.blit(rendered_line, (100, y))
            y += 10  # Space between lines

    ### fonctions de base du jeu ###

    #méthode qui gère les événements clavier/souris
    def handling_events(self):
        self.mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if not self.temp_ship_pos:
                    if self.starship == None:
                        if self.mouse_pos[0] < 2.8 * SPACING:
                            self.temp_ship_pos = self.mouse_pos

            if event.type == pygame.KEYDOWN:
                self.key_pressed[event.key] = True #utilisation d'un dictionnaire pour connaître toutes les touches pressées simultanément

            elif event.type == pygame.KEYUP:
                self.key_pressed[event.key] = False

            elif event.type == pygame.MOUSEBUTTONUP:
                if self.temp_ship_pos:
                    if self.starship == None:
                        x, y = self.temp_ship_pos
                        self.starship = self.create_starship((x, y),
                                                             self.mouse_pos)  # Starship(self.screen, x, y, 1, 1, SHIP_MASS)
                        self.temp_ship_pos = None

    #méthode d'affichage du jeu
    def display(self):
        self.screen.fill(DARK_BLUE)

        dotted_limit_image = pygame.image.load("games/gravitySlingshot/assets/dotted_limit.png")
        self.screen.blit(dotted_limit_image, (2.8 * SPACING - dotted_limit_image.get_width()//2, 20))

        for planet in self.planets:
            planet.draw()
        self.black_hole.draw(self.black_hole.x, self.black_hole.y, self.screen)

        if self.temp_ship_pos:
            pygame.draw.line(self.screen, WHITE, self.temp_ship_pos, self.mouse_pos, 2)

            #dessin des pointillés : on calcule sur 20 itération la position future du vaisseau avec équations horaires
            pt_x, pt_y = self.temp_ship_pos
            pt_acc_x = 0
            pt_acc_y = 0
            pt_vel_x = (-self.mouse_pos[0] + pt_x) * 0.4 / VEL_SCALE
            pt_vel_y = (-self.mouse_pos[1] + pt_y) * 0.4 / VEL_SCALE

            for i in range(0, 200, 10):
                for planet in self.planets:
                    dx = planet.x - pt_x #distance planète/pointillé selon x
                    dy = planet.y - pt_y #distance planète/pointillé selon y
                    distance = math.sqrt(dx ** 2 + dy ** 2) #distance planète/pointillé

                    force = (SHIP_MASS * planet.mass) / (distance ** 2) #3eme loi de Newton F = (m1 * m2)/d²
                    angle = math.atan2(dy, dx)

                    #2eme loi de Newton : F = ma => a = F/m
                    pt_acc_x = (force / SHIP_MASS) * math.cos(angle) #accélération selon x
                    pt_acc_y = (force / SHIP_MASS) * math.sin(angle) #accélération selon y

                    #équation horaire de position : 1/2 * accélération * t² + vitesse * t
                    pt_x += pt_vel_x * i + 0.5 * pt_acc_x * i ** 2
                    pt_y += pt_vel_y * i + 0.5 * pt_acc_y * i ** 2

                    #équation horaire de la vitesse : vitesse = accélération * t
                    pt_vel_x += pt_acc_x * i
                    pt_vel_y += pt_acc_y * i

                pygame.draw.circle(self.screen, WHITE, (pt_x, pt_y), 5)

            if self.starship != None:
                self.starship.draw(self.temp_ship_pos[0], self.temp_ship_pos[1], self.screen)

    #méthode de mise à jour des composants du jeu
    def update(self):
        if self.starship != None:
            # ---------------- contrôle du vaisseau (boost et direction) -------------------
            if self.key_pressed.get(pygame.K_LEFT):
                self.starship.rotate(-1)
            elif self.key_pressed.get(pygame.K_RIGHT):
                self.starship.rotate(1)

            self.starship.draw(self.starship.x, self.starship.y, self.screen)

            if self.key_pressed.get(pygame.K_SPACE):
                self.starship.is_boosted = True
            else:
                self.starship.is_boosted = False
            # --------------------------------------------------------------------------------

            planet_collided = False
            hole_collided = False

            self.starship.move(self.planets)
            ## collisions avec planètes
            for planet in self.planets:
                # Calculez l'offset entre les positions des deux objets
                offset = (planet.rect.x - self.starship.rect.x, planet.rect.y - self.starship.rect.y)

                # Vérifiez la collision avec les masques
                if self.starship.mask.overlap(planet.mask, offset): #les masques permettent de s'adapter à la forme circulaire des planètes
                    planet_collided = True
                    break

            ## collisions avec le trou noir
            # Calculez l'offset entre les positions des deux objets
            offset = (self.black_hole.rect.x - self.starship.rect.x, self.black_hole.rect.y - self.starship.rect.y)

            # Vérifiez la collision avec les masques
            if self.starship.mask.overlap(self.black_hole.mask, offset):
                hole_collided = True

            ## sortie de l'écran
            off_screen = self.starship.x < 0 or self.starship.x > WIDTH or self.starship.y < 0 or self.starship.y > HEIGHT  # bool

            if off_screen or planet_collided:
                self.starship = None

            #changement de niveau en cas de collision avec le trou noir
            if hole_collided:
                self.starship = None
                self.planets = []
                self.level += 1
                self.create_level()

        if self.win:
            self.end_game()

        pygame.display.flip()

    # boucle du jeu qui appelle toutes les méthodes nécessaires
    def run(self):
        pygame.mixer.init()
        pygame.mixer.music.load("games/gravitySlingshot/assets/stellar.mp3")
        pygame.mixer.music.play(-1)
        while self.running:
            self.handling_events()
            self.display()
            self.update()
            self.clock.tick(FPS)