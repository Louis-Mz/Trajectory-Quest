import pygame
import math
import random
from constants import *
from starship import Starship
from planet import Planet
from black_hole import Hole


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.key_pressed = {}
        self.running = True
        self.clock = pygame.time.Clock()
        self.starship = None
        self.planets = []
        self.black_hole = Hole(self.screen, HOLE_X, HEIGHT//2, HOLE_MASS, HOLE_SIZE)
        #self.planet = Planet(self.screen, WIDTH // 2, HEIGHT // 2, PLANET_MASS)
        self.temp_ship_pos = None
        self.mouse_pos = None
        self.level = 1

        #self.rect = pygame.Rect(0, 0, 25, 25)
        #self.test_col = (255, 255, 255)

    #useful fonctions
    def create_starship(self, temp_pos, mouse_pos):
        t_x, t_y = temp_pos
        m_x, m_y = mouse_pos
        vel_x = (-m_x + t_x) / VEL_SCALE #calcul of the velocity vect component x
        vel_y = (-m_y + t_y) / VEL_SCALE #calcul of the velocity vect component y
        starship = Starship(self.screen, t_x, t_y, vel_x, vel_y, SHIP_MASS)
        return starship

    def create_solar_system(self):
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

    def create_level(self):
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
            self.create_solar_system()

    '''
    def test(self):
        pos = pygame.mouse.get_pos()
        self.rect.center = pos
    '''

    #game basic fonctions
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
                self.key_pressed[event.key] = True
                """
                if self.starship != None:
                    if event.key == pygame.K_LEFT:
                        self.starship.rotate(-1.5)
                    elif event.key == pygame.K_RIGHT:
                        self.starship.rotate(1.5)
                """
            elif event.type == pygame.KEYUP:
                self.key_pressed[event.key] = False

            elif event.type == pygame.MOUSEBUTTONUP:
                if self.temp_ship_pos:
                    if self.starship == None:
                        x, y = self.temp_ship_pos
                        self.starship = self.create_starship((x, y),
                                                             self.mouse_pos)  # Starship(self.screen, x, y, 1, 1, SHIP_MASS)
                        self.temp_ship_pos = None

    def display(self):
        self.screen.fill(DARK_BLUE)
        #pygame.draw.rect(self.screen, self.test_col, self.rect)
        #self.test()

        dotted_limit_image = pygame.image.load("games/gravitySlingshot/assets/dotted_limit.png")
        self.screen.blit(dotted_limit_image, (2.8 * SPACING - dotted_limit_image.get_width()//2, 20))

        for planet in self.planets:
            planet.draw() #planet.size, planet.color
        self.black_hole.draw(self.black_hole.x, self.black_hole.y, self.screen)

        if self.temp_ship_pos:
            pygame.draw.line(self.screen, WHITE, self.temp_ship_pos, self.mouse_pos, 2)
            if self.starship != None:
                self.starship.draw(self.temp_ship_pos[0], self.temp_ship_pos[1], self.screen)

    def update(self):
        if self.starship != None:
            if self.key_pressed.get(pygame.K_LEFT):
                self.starship.rotate(-1)
            elif self.key_pressed.get(pygame.K_RIGHT):
                self.starship.rotate(1)

            self.starship.draw(self.starship.x, self.starship.y, self.screen)
            planet_collided = False
            hole_collided = False
            for planet in self.planets:
                self.starship.move(planet)

                # Calculez l'offset entre les positions des deux objets
                offset = (planet.rect.x - self.starship.rect.x, planet.rect.y - self.starship.rect.y)

                # Vérifiez la collision avec les masques
                if self.starship.mask.overlap(planet.mask, offset):
                    planet_collided = True
                    break
                '''
                #planet_collided = math.sqrt((self.starship.x - planet.x) ** 2 + (self.starship.y - planet.y) ** 2) <= planet.size
                if self.starship.rect.colliderect(planet.rect):
                    planet_collided = True
                    print("collision with starship")
                    break
                '''

            self.starship.move(self.black_hole)
            # Calculez l'offset entre les positions des deux objets
            offset = (self.black_hole.rect.x - self.starship.rect.x, self.black_hole.rect.y - self.starship.rect.y)

            # Vérifiez la collision avec les masques
            if self.starship.mask.overlap(self.black_hole.mask, offset):
                hole_collided = True

            off_screen = self.starship.x < 0 or self.starship.x > WIDTH or self.starship.y < 0 or self.starship.y > HEIGHT  # bool
            # planet_collided = math.sqrt((object.x - self.planet.x)*2 + (object.y - self.planet.y)*2) <= PLANET_SIZE #bool

            if off_screen or planet_collided:
                self.starship = None

            if hole_collided:
                self.starship = None
                self.planets = []
                self.level += 1
                self.create_level()

        pygame.display.flip()

    def run(self):
        while self.running:
            self.handling_events()
            self.display()
            self.update()
            self.clock.tick(FPS)