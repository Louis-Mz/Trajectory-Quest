import pygame
#game constantes

WIDTH = 1080
HEIGHT = 720
NUM_PLANETS = 9
SPACING = WIDTH // (NUM_PLANETS + 1)
SIZE_SCALE = 2

G = 6 #constante d'attraction gravitationnelle
FPS = 60
VEL_SCALE = 1000 #to reduce by 500 the velocity that is defined by the distance with the mouse

#colors
WHITE = (255, 255, 255)
LIGHT_BLUE = "#E0FBFC"
MEDIUM_LIGHT_BLUE = "#98C1D9"
MEDIUM_DARK_BLUE = "#3D5A80"
DARK_BLUE = "#293241"
RED = "#EE6C4D"
GREEN = "#00d500"
GRAY = "#646464"

#creation des niveaux
level1 = {"mercure" : [4 * SPACING, 500], "venus" : [6 * SPACING, 220], "earth" : [8 * SPACING, 600]}
level2 = {"earth" : [4 * SPACING, 130], "mars" : [5 * SPACING, 560], "jupiter" : [7 * SPACING, 240]}
level3 = {"jupiter" : [4 * SPACING, 610], "saturn" : [6 * SPACING, 200], "uranus" : [8 * SPACING, 550]}
level4 = {"uranus" : [4 * SPACING, 240], "neptune" : [6 * SPACING, 520], "pluton" : [8 * SPACING, 210]}
levels = [level1, level2, level3, level4]

#planètes
MERCURE_MASS = 6
MERCURE_SIZE = 80 * SIZE_SCALE
MERCURE_X = 1 * SPACING
MERCURE_COLOR = RED
MERCURE_IMAGE = pygame.image.load("games/gravitySlingshot/assets/mercury.png")

VENUS_MASS = 8
VENUS_SIZE = 90 * SIZE_SCALE
VENUS_X = 2 * SPACING
VENUS_COLOR = RED
VENUS_IMAGE = pygame.image.load("games/gravitySlingshot/assets/venus.png")

EARTH_MASS = 9
EARTH_SIZE = 100 * SIZE_SCALE
EARTH_X = 3 * SPACING
EARTH_COLOR = MEDIUM_LIGHT_BLUE
EARTH_IMAGE = pygame.image.load("games/gravitySlingshot/assets/earth.png")

MARS_MASS = 7
MARS_SIZE = 80 * SIZE_SCALE
MARS_X = 4 * SPACING
MARS_COLOR = RED
MARS_IMAGE = pygame.image.load("games/gravitySlingshot/assets/mars.png")

JUPITER_MASS = 30
JUPITER_SIZE = 180 * SIZE_SCALE
JUPITER_X = 5 * SPACING
JUPITER_COLOR = RED
JUPITER_IMAGE = pygame.image.load("games/gravitySlingshot/assets/jupiter.png")

SATURN_MASS = 20
SATURN_SIZE = 140 * SIZE_SCALE
SATURN_X = 6 * SPACING
SATURN_COLOR = RED
SATURN_IMAGE = pygame.image.load("games/gravitySlingshot/assets/saturn.png")

URANUS_MASS = 15
URANUS_SIZE = 100 * SIZE_SCALE
URANUS_X = 7 * SPACING
URANUS_COLOR = LIGHT_BLUE
URANUS_IMAGE = pygame.image.load("games/gravitySlingshot/assets/uranus.png")

NEPTUNE_MASS = 16
NEPTUNE_SIZE = 110 * SIZE_SCALE
NEPTUNE_X = 8 * SPACING
NEPTUNE_COLOR = MEDIUM_LIGHT_BLUE
NEPTUNE_IMAGE = pygame.image.load("games/gravitySlingshot/assets/neptune.png")

PLUTON_MASS = 4
PLUTON_SIZE = 70 * SIZE_SCALE
PLUTON_X = 9 * SPACING
PLUTON_COLOR = RED
PLUTON_IMAGE = pygame.image.load("games/gravitySlingshot/assets/pluton.png")

HOLE_MASS = 6
HOLE_SIZE = 45 * SIZE_SCALE
HOLE_X = 9.5 * SPACING

PLANET_COLOR = "#EE6C4D"

SHIP_MASS = 3
SHIP_SIZE = 30
BOOST_CHARGE = 250
BOOST = 0.01