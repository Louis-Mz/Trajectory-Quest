import pyxel as py
import math as m
import random

FENETRE = 1500
GRAVITE = 0.1  # Constante de gravité
VITESSE_FENETRE = 7

PLANETE = (48, 0)
LUNE = (32,0)
SATURN = (0, 24)
METEOR = (16,0)

#fonction qui calcule le vecteur de la différence
def vect(tpl1, tpl2 = (0, 0)):
    return (tpl2[0]-tpl1[0], tpl2[1]-tpl1[1])

#fonction qui calcule la norme d'un vecteur
def lng(tpl1, tpl2 = (0, 0)):
    v = vect(tpl1, tpl2)
    return m.sqrt(v[0]**2 + v[1]**2)

def dans_fenetre(tuple):
    return -50 < tuple[0] < FENETRE + 50 and -50 < tuple[1] < FENETRE + 50

#fonction qui génère un vecteur aléatoire avec la bibliothèque random
def vect_aleatoire(longeur):
    val = m.radians(random.randint(0, 360))
    return (longeur * m.cos(val), longeur*m.sin(val))

#classe de l'application pyxel
class App:
    def __init__(self):
        py.init(FENETRE, FENETRE, title="Pendule", fps=60)
        py.load("mec.pyxres")
        
        self.game = True
        self.cmds = {py.KEY_S : self.BAS, py.KEY_Z : self.HAUT, py.KEY_D : self.DROITE, py.KEY_Q :self.GAUCHE}
        self.mobs = Mob()
        self.time = 0
        self.centres = [(random.randint(0, FENETRE), random.randint(0, FENETRE)) for i in range(500)]
        self.pendule = Pendule(m.pi / 2, (FENETRE / 2, FENETRE / 4), 100)  # Angle initial
        self.entity = Entity(FENETRE / 2, FENETRE / 2, 2, -3)
        self.joueur = Joueur()
        self.meteor = [Meteor().generer(self.centres) for i in range(2)]
        self.token = Token()
        self.score = 0
        self.cd = 0
        self.cd_restart = 0
        self.BG = Background().generer()
        
        py.run(self.update, self.draw)

    #------------------------------------ commandes ZQSD ------------------------------------------
    def BAS(self):
        #défile tous les éléments du jeu vers le haut pour donner l'impression que l'on se déplace vers le bas
        self.centres = [(i[0], i[1] - VITESSE_FENETRE) for i in self.centres]
        self.token.y -= VITESSE_FENETRE
        for i in self.meteor:
            i.y -= VITESSE_FENETRE
        self.mobs.y -= VITESSE_FENETRE
        if self.pendule.actif:
            self.pendule.centre = (self.pendule.centre[0], self.pendule.centre[1] - VITESSE_FENETRE)
            self.pendule.y -= VITESSE_FENETRE
        else:
            self.entity.y -= VITESSE_FENETRE
        
        self.centres += [(random.randint(0, FENETRE), random.randint(FENETRE, FENETRE + 50)) for i in range(2)]
        for bg_elm in self.BG.planets:
            bg_elm.y -= VITESSE_FENETRE
        for bg_elm in self.BG.lune:
            bg_elm.y -= VITESSE_FENETRE
        for bg_elm in self.BG.saturn:
            bg_elm.y -= VITESSE_FENETRE
        for bg_elm in self.BG.meteor:
            bg_elm.y -= VITESSE_FENETRE
        #self.centres.append((random.randint(0, FENETRE), random.randint(FENETRE, FENETRE + 50)))
    
    def HAUT(self):
        # défile tous les éléments du jeu vers le bas pour donner l'impression que l'on se déplace vers le haut
        self.centres = [(i[0], i[1] + VITESSE_FENETRE) for i in self.centres]
        self.token.y += VITESSE_FENETRE
        for i in self.meteor:
            i.y += VITESSE_FENETRE
        self.mobs.y += VITESSE_FENETRE
        if self.pendule.actif:
            self.pendule.centre = (self.pendule.centre[0], self.pendule.centre[1] + VITESSE_FENETRE)
            self.pendule.y += VITESSE_FENETRE
        else:
            self.entity.y += VITESSE_FENETRE
            
        self.centres += [(random.randint(0, FENETRE), random.randint(-50, 0)) for i in range(2)]
        for bg_elm in self.BG.planets:
            bg_elm.y += VITESSE_FENETRE
        for bg_elm in self.BG.lune:
            bg_elm.y += VITESSE_FENETRE
        for bg_elm in self.BG.saturn:
            bg_elm.y += VITESSE_FENETRE
        for bg_elm in self.BG.meteor:
            bg_elm.y += VITESSE_FENETRE
        #self.centres.append((random.randint(0, FENETRE), random.randint(-50, 0)))
    
    def DROITE(self):
        # défile tous les éléments du jeu vers la gauche pour donner l'impression que l'on se déplace vers la droite
        self.centres = [(i[0] - VITESSE_FENETRE, i[1]) for i in self.centres]
        self.token.x -= VITESSE_FENETRE
        for i in self.meteor:
            i.x -= VITESSE_FENETRE
        self.mobs.x -= VITESSE_FENETRE
        if self.pendule.actif:
            self.pendule.centre = (self.pendule.centre[0] - VITESSE_FENETRE, self.pendule.centre[1])
            self.pendule.x -= VITESSE_FENETRE
        else:
            self.entity.x -= VITESSE_FENETRE
            
        self.centres += [(random.randint(FENETRE, FENETRE + 50), random.randint(0, FENETRE)) for i in range(2)]
        #self.centres.append((random.randint(FENETRE, FENETRE + 50), random.randint(0, FENETRE)))
        for bg_elm in self.BG.planets:
            bg_elm.x -= VITESSE_FENETRE
        for bg_elm in self.BG.lune:
            bg_elm.x -= VITESSE_FENETRE
        for bg_elm in self.BG.saturn:
            bg_elm.x -= VITESSE_FENETRE
        for bg_elm in self.BG.meteor:
            bg_elm.x -= VITESSE_FENETRE
    
    def GAUCHE(self):
        # défile tous les éléments du jeu vers la droite pour donner l'impression que l'on se déplace vers la gauche
        self.centres = [(i[0] + VITESSE_FENETRE, i[1]) for i in self.centres]
        self.token.x += VITESSE_FENETRE
        for i in self.meteor:
            i.x += VITESSE_FENETRE
        self.mobs.x += VITESSE_FENETRE
        if self.pendule.actif:
            self.pendule.centre = (self.pendule.centre[0] + VITESSE_FENETRE, self.pendule.centre[1])
            self.pendule.x += VITESSE_FENETRE
        else:
            self.entity.x += VITESSE_FENETRE
        self.centres += [(random.randint(-50, 0), random.randint(0, FENETRE)) for i in range(2)]
        #self.centres.append((random.randint(-50, 0), random.randint(0, FENETRE)))
        for bg_elm in self.BG.planets:
            bg_elm.x += VITESSE_FENETRE
        for bg_elm in self.BG.lune:
            bg_elm.x += VITESSE_FENETRE
        for bg_elm in self.BG.saturn:
            bg_elm.x += VITESSE_FENETRE
        for bg_elm in self.BG.meteor:
            bg_elm.x += VITESSE_FENETRE

    #méthode pour relancer le jeu
    def restart(self):
        if py.btn(py.KEY_R) and self.cd_restart == 0:
            self.token = Token()
            self.centres = [(random.randint(0, FENETRE), random.randint(0, FENETRE)) for i in range(500)]
            self.pendule = Pendule(m.pi / 2, (FENETRE / 2, FENETRE / 4), 100)  # Angle initial
            self.entity = Entity(FENETRE / 2, FENETRE / 2, 2, -3)
            self.meteor = [Meteor().generer(self.centres) for i in range(2)]
            self.mobs = Mob()
            self.game = True
            self . score = 0
            self.cd_restart = 60

    # méthode qui gère les collisions avec les météors
    def collision_meteor(self):
        for i in self.meteor:
            if self.pendule.actif:
                if lng((self.pendule.x + 8, self.pendule.y + 8), (i.x, i.y)) < i.size:
                    #print("pendule meteor")
                    return True
            elif lng((self.entity.x, self.entity.y), (i.x, i.y)) < i.size:
                #print("entity meteor")
                return True
        return False
    
    # méthode qui gère les collisions avec le monstre araigné
    def collision_mob(self):
        if self.pendule.actif:
            if lng((self.pendule.x, self.pendule.y), (self.mobs.x, self.mobs.y)) < 7:

                return True
        elif lng((self.entity.x, self.entity.y), (self.mobs.x, self.mobs.y)) < 7:

            return True
        return False

    #méthode de mort : retourne vrai si l'une des collisions se produit
    def die(self):
        return self.collision_mob() or self.collision_meteor() or (self.entity.on and self.entity.y > 2500)

    #écran de défaite
    def game_over(self):
        py.cls(0)
        py.text(FENETRE/2, FENETRE/2, "GAME OVER", 7)

    #méthode de mise à jour des objet du jeu
    def update(self):
        if self.game:
            self.time += 1
            if self.token.upd(self.pendule, self.entity):
                self.token = Token()
                self.score += 1
                #print(self.score)
            self.centres = [i for i in self.centres if dans_fenetre(i)]
            for i in self.cmds:
                if py.btn(i):
                    self.cmds[i]()
            self.entity.upd(self.time, self.pendule)
            self.joueur.upd(self.entity, self.centres)
            self.pendule.update(self.entity, self.joueur)
            self.meteor = [i for i in self.meteor if i.time_to_live > 0]
            for meteor in self.meteor:
                meteor.upd()

            #ajout de météors tous les 90 FPS
            if not self.time % 90:
                self.meteor.append(Meteor().generer(self.centres))
            self.mobs.upd(self.pendule, self.entity, self.centres)

        if self.cd != 0:
            self.cd -= 1
        if self.cd_restart != 0:
            self.cd_restart -= 1
        self.restart() # Vérifie si on doit redémmarer
        
    #méthode d'affichage de l'application
    def draw(self):
        #py.cls(0)
        self.BG.afficher()
        self.token.draw(self.pendule, self.entity)
        self.mobs.draw()
        for i in self.meteor:
            i.draw()
        self.pendule.draw()
        self.entity.draw()

        for i in self.centres:
            py.rect(i[0], i[1], 2, 2, 7)  # Dessine les centres
            
        self.joueur.draw()
        
        if self.die():
            self.game = False
        if not self.game :
            self.game_over()
        py.text(50, 300, str(self.score), 10)

#classe du pendule
class Pendule:
    def __init__(self, angle, centre, longeur):
        self.centre = centre
        self.longeur = longeur
        self.actif = True
        self.angle = angle
        self.vitesse_angulaire = 0
        self.acceleration_angulaire = 0
        self.x = 0
        self.y = 0
        self.cd = 0

    def update(self, entity, joueur):
        # calcul de l'accélération angulaire
        self.acceleration_angulaire = -GRAVITE / self.longeur * m.sin(self.angle) #formule du couple (Torque) τ=−mgLsin(θ)
        # mise à jour de la vitesse angulaire
        self.vitesse_angulaire += self.acceleration_angulaire
        # mise à jour de l'angle
        self.angle += self.vitesse_angulaire
        # calcul des nouvelles coordonnées
        self.x, self.y = self.centre[0] + self.longeur * m.sin(self.angle), self.centre[1] + self.longeur * m.cos(
            self.angle) # coordonnées cartésiennes x = x0 + Lsin(θ) et y = y0 + Lcos(θ)

        # application d'un léger amortissement
        self.vitesse_angulaire *= 0.997

        #cooldown : un "temps de recharge"
        if self.cd > 0:
            self.cd -= 1
            
        self.swich(entity, joueur.centre_proches) #gère la transition entre pendule et entités

    def draw(self):
        if self.actif:
            # Calcul des coordonnées du pendule
            x = self.centre[0] + self.longeur * m.sin(self.angle) #fluidifie l'affichage
            y = self.centre[1] + self.longeur * m.cos(self.angle)

            # Dessin du fil et de la masse
            if self.vitesse_angulaire > 0:
                py.blt(self.x , self.y, 0, 0, 0, -16, 16, colkey=0)
                py.line(self.centre[0], self.centre[1], x + 16, y, 7)
            else: #affiche en fonction de si on regarde à gauche ou a droite
                py.line(self.centre[0], self.centre[1], x, y, 7)
                py.blt(self.x, self.y, 0, 0, 0, 16, 16, colkey = 0)

    #méthode de passage à la chute libre
    def to_entity(self, entity, centres_proches):
        self.actif = False
        entity.on = True
        entity.x, entity.y = self.x, self.y
        
        #donner les bonnes CI à l'entité
        if self.x > self.centre[0]:
            entity.vx = self.longeur * self.vitesse_angulaire * m.sin(self.angle)
            entity.vy = -self.longeur * self.vitesse_angulaire * m.cos(self.angle)
        else:
            entity.vx = -self.longeur * self.vitesse_angulaire * m.sin(self.angle)
            entity.vy = self.longeur * self.vitesse_angulaire * m.cos(self.angle)

        if entity.vy < 0 and not -m.pi/6 < self.angle < m.pi/6:
            entity.vy -= 2
    
    # méthode de passage au pendule
    def to_pendule(self, entity, centres_proches):
        #éviter les out of range
        if centres_proches != []:
            
            #MAJ des variables d'etat
            self.actif = True
            entity.on = False
            
            #séléction du centtre d'accrochage parmi les centres proches de la souris
            self.centre = random.choice(centres_proches)
            
            #initialisation du pendule
            self.longeur = lng((entity.x, entity.y), self.centre)
            vecteur = vect(self.centre, (entity.x, entity.y))
            self.vitesse_angulaire = 0
            angle = m.atan2(vecteur[0], vecteur[1])
            self.angle = angle
            
            #légère vitesse initiale pour fluidifier le mouvement
            if entity.x > self.centre[0]:
                self.vitesse_angulaire = -0.02
            else:
                self.vitesse_angulaire = 0.02
                
    #changement de physique entre pendule et chute libre
    def swich(self, entity, centres_proches):

        if py.btn(py.MOUSE_BUTTON_LEFT) and self.cd == 0:
            if self.actif:
                self.to_entity(entity, centres_proches)
                
            else:
                self.to_pendule(entity, centres_proches)

            self.cd = 30


class Entity:
    def __init__(self, x, y, vx, vy):
        self.x, self.y, self.vx, self.vy = x, y, vx, vy
        self.on = False
        self.closest = None
        self.cd = 0
        self.img = True
        
    def upd(self, time, pendule):
        if self.on:
            self.vy += GRAVITE
            self.x += self.vx
            self.y += self.vy
        else:
            self.x = pendule.x
            self.y = pendule.y
        if self.cd > 0:
            self.cd -= 1
        self.boost_vertical()
        if time % 7 == 0 :
            self.img = not self.img
            
    # offre au joueur un saut avec la touche ESPACE
    def boost_vertical(self):
        if py.btn(py.KEY_SPACE) and self.cd == 0 and self.on:
            self.vy -= 8
            self.cd = 200

    #dessine l'image du joueur
    def draw(self):
        if self.on:
            if self.img:
                py.blt(self.x - 8, self.y - 8, 0, 32, 0, 16, 16, colkey=0)
            else:
                py.blt(self.x - 8 , self.y - 8, 0, 32, 0, 16, -16, colkey=0) #affichage mirroir


class Joueur:
    def __init__(self):
        self.x = 1
        self.y = 1
        self.centre_proches = []  # Variable pour stocker les centres proches
        
    def upd(self, entity, centres):
        # Mise à jour des coordonnées du joueur avec la position de la souris
        self.x = py.mouse_x
        self.y = py.mouse_y
        
        # Filtrage des centres proches (distance inférieure à 200)
        self.centre_proches = [centre for centre in centres if lng((self.x, self.y), centre) < 100]

            
    def draw(self):
        py.rect(self.x, self.y, 5, 5, 7)
        for centre in self.centre_proches:
            py.rect(centre[0], centre[1], 2, 2, 8)  # Dessin des centres proches
            #py.line(self.x, self.y, centre[0], centre[1], 7)

            
    
class Meteor:
    def __init__(self):
        self.time_to_live = 1000
        self.x = random.choice([random.randint(-100, 0), random.randint(FENETRE, FENETRE+100)])
        self.y = random.choice([random.randint(-100, 0), random.randint(FENETRE, FENETRE+100)])
        self.vx = None
        self.vy = None
        self.size = random.randint(20, 30)
        self.scale = self.size / 8  # Facteur de mise à l'échelle basé sur la taille
        self.img = True

    #méthode qui génère des météors
    def generer(self, centres):
        centre_aleatoire = random.choice(centres)
        long = lng((self.x, self.y), centre_aleatoire)
        vecteur = vect((self.x, self.y), centre_aleatoire)
        speed = random.uniform(5, 7)
        self.vx = speed*vecteur[0]/long
        self.vy = speed*vecteur[1]/long

        return self

    #méthode qui met à jour la position des météor
    def upd(self):
        self.x += self.vx
        self.y += self.vy
        if self.time_to_live % 7 == 0:
            self.img = not self.img
        self.time_to_live -= 1

    #méthode de dessin des météor
    def draw(self):
        py.circ(self.x, self.y, self.size, 4)
        if self.img:
            py.blt(self.x - 32, self.y - 32, 0, 0, 80, 64, 64, colkey = 11)
        else:
            py.blt(self.x - 32, self.y - 32, 0, 0, 80, 64, -64, colkey = 11) #affichage mirroir

class Mob:
    def __init__(self):
        #self.time_to_live = 500
        self.id_difficulte = 1
        self.vitesse_hors_fenetre = 1 #sert à ce que le mob continue de bouger même s'il est hors fenetre et donc qu'il n'a pas de centre
        self.x = FENETRE/2
        self.y = 3*FENETRE/4
        self.vx = 0
        self.vy = 0
        self.vecteur = (0, 0)
        self.id_vitesse = 1
        self.centres = []

    # méthode de déplacement du monstre
    def upd(self, pendule, entity, centres):
        if pendule.actif:
            self.vecteur = vect((self.x, self.y), (pendule.x, pendule.y))
        else:
            self.vecteur = vect((self.x, self.y), (entity.x, entity.y))
        long = lng(self.vecteur)
        self.vx = self.vitesse_hors_fenetre * self.id_difficulte * self.id_vitesse * self.vecteur[0]/long
        self.vy = self.vitesse_hors_fenetre * self.id_difficulte * self.id_vitesse * self.vecteur[1]/long
        self.x += self.vx
        self.y += self.vy
        self.centres = [i for i in centres if lng((self.x, self.y), i) < 100]
        if self.centres == []:
            self.id_vitesse = 0.5
        else:
            #plus le mob a de centres, plus il est rapide
            #vitesse logarithmique
            self.id_vitesse = m.log(len(self.centres)) + 1
            
            #vitesse proportionelle
            #self.id_vitesse = len(self.centres) * 0.5

        #self.time_to_live -= 1
        if dans_fenetre((self.x, self.y)):
            self.vitesse_hors_fenetre = 1
        else:
            self.vitesse_hors_fenetre = 30

    # dessin du monstre
    def draw(self):
        py.circ(self.x, self.y, 5, 3) #corps
        for i in self.centres:
            py.line(self.x, self.y, i[0], i[1], 7) #pattes

#classe des pièces
class Token :
    def __init__(self):
        self.x = random.randint(0, FENETRE)
        self.y = random.randint(0, FENETRE)
        self.ax = 0
        self.ay = 0
        self.vx = 0
        self.vy = 0

    #méthode qui déplace les pièces lorsqu'elles sont à côté du joueur (effet aimant)
    def upd(self, pendule, entity):
        vector = (0, 0)
        long = -1
        flag = False
        if pendule.actif :
            long = lng((pendule.x, pendule.y), (self.x, self.y))
            if  long < 250 and long != 0:
                vector = vect((self.x, self.y), (pendule.x, pendule.y))
                self.ax = vector[0]/long
                self.ay = vector[1]/long
        elif entity.on:
            long = lng((entity.x, entity.y), (self.x, self.y))
            if  long < 250 and long != 0:
                vector = vect((self.x, self.y), (entity.x, entity.y))
                self.ax = vector[0]/long
                self.ay = vector[1]/long
        if long < 20:
            flag = True
        if long > 250:
            self.ax = 0
            self.ay = 0
        self.vx += self.ax 
        self.vy += self.ay 
        self.x += self.vx
        self.y += self.vy
        self.vx *= 0.75
        self.vy *= 0.75
        return flag

    
    def draw(self, pendule, entity):
        py.blt(self.x - 16, self.y - 16, 0, 0, 16, 32, 32, colkey=0)
        #py.circ(self.x, self.y, 20, 10)
        vector = 0
        long = -1
        cod_centre = (0, 0)
        cod1 = (0, 0)
        cod2 = (0, 0)
        cod3 = (0, 0)

        if pendule.actif:
            vector = vect((pendule.x, pendule.y), (self.x, self.y))
            long = lng((pendule.x, pendule.y), (self.x, self.y))
            vector = (vector[0]/long, vector[1]/long)
            cod_centre = (pendule.x + 60 * vector[0], pendule.y + 60 * vector[1])
        else:
            vector = vect((entity.x, entity.y), (self.x, self.y))
            long = lng((entity.x, entity.y), (self.x, self.y))
            vector = (vector[0]/long, vector[1]/long)
            cod_centre = (entity.x + 60 * vector[0], entity.y + 60 * vector[1])
            
        vect_normal = (-vector[1], vector[0])
        cod1 = (cod_centre[0] + 20 * vector[0], cod_centre[1] + 20 * vector[1])
        cod2 = (cod_centre[0] + 5 * vect_normal[0], cod_centre[1] + 5 * vect_normal[1])
        cod3 = (cod_centre[0] - 5 * vect_normal[0], cod_centre[1] - 5 * vect_normal[1])
        #py.rect(cod_centre[0], cod_centre[1], 10, 10, 12)
        py.tri(cod1[0], cod1[1], cod2[0], cod2[1], cod3[0], cod3[1], 2)
#         py.rect(cod1[0], cod1[1], 10, 10, 2)
#         py.rect(cod2[0], cod2[1], 10, 10, 2)
#         py.rect(cod3[0], cod3[1], 10, 10, 2)

        
class Image:
    def __init__(self, nature, dimention):
        self.nature = nature
        self.x = py.rndi(0, 1500)
        self.y = py.rndi(0, 1500)
        self.dim = dimention
        
    def afficher(self):
        py.blt(self.x,self.y, 1, self.nature[0], self.nature[1], self.dim, self.dim, colkey = 0)

class Background:
    def __init__(self):
        self.planets = []
        self.lune= []
        self.saturn = []
        self.meteor = []
        self.generer()

    def generer(self):
        for i in range (2):
            self.lune.append(Image(LUNE, 16))
        for i in range(2):
            self.planets.append(Image(PLANETE, 16))
        for i in range (2):
            self.saturn.append(Image(SATURN, 16))
        for i in range(3):
            self.meteor.append(Image(METEOR, 16))
        return self

    def afficher(self):
        py.cls(0)
        for i in self.planets:
            i.afficher()
        for i in self.lune:
            i.afficher()
        for i in self.saturn:
            i.afficher()
        for i in self.meteor:
            i.afficher()
App()