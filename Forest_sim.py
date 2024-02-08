######################
##      VERSION     ## 4.8 (Random seed)
######################

######################
##      IMPORTS     ##
######################

import tkiteasy.tkiteasy as tki
import matplotlib.pyplot as plt
import random
import time
import os

########################
##      Fonctions     ##
########################

        ##1.      Jeu     ##

class Forest_sim:
    
    def __init__(self) -> None:

        self.nouveaux_organismes : dict = {}

        self.clefs : set = {0, 1}
        for i in range(2):
            self.clefs.remove(i)
        #si on n'initialise pas un set avec des valeurs, python le reconnait comme un dictionnaire

        self.grille : dict = {}

        self.age : dict  = {}
        self.en_vie : dict = {}
        self.duree_vie : dict = {}
        self.stamina : dict = {}
        self.gain_stamina : dict = {}
        self.peut_enfanter : dict = {}
        self.vitesse : dict = {}
        self.enfants : dict = {}
        self.victimes : dict = {}
        self.type : dict = {}
        self.vue : dict = {}
        self.tki_objects : dict = {}
        self.graphs : dict = {}
        self.en_traque : dict = {}

        self.population : dict = {
            "proies" : 0,
            "predateurs" : 0,
            "total" : 0,
            "nb_indiv" : 0,
            "avg_vitesse_pred" : 0,
            "avg_vitesse_proi" : 0,
        }

        self.historique_populations : dict = {
            "proies" : (0, 0),
            "predateurs" : (0, 0),
            "total" : (0, 0),
            "nb_indiv" : (0, 0),
            "avg_vitesse_pred" : (0, 0),
            "avg_vitesse_proi" : (0, 0),
            "avg_vue_pred" : (0, 0),
            "avg_vue_proi" : (0, 0),
        }
        #stock les variables de population (tuple => way faster than lists) (en modulo 4 on retrouve nos 4 valeurs ordonnées (pour les graphiques))
    
    def depart(self,
            longueur_fenetre = 1000, 
            hauteur_fenetre = 1000
            ):
        """Initialise la fenetre graphique

        Args:
            longueur_fenetre (int, optional):longueur de la fenetre en pixels. Defaults to 1000.
            hauteur_fenetre (int, optional): hauteur de la fenetre en pixels. Defaults to 1000.
        """
        
        self.tki_objects['fenetre'] = tki.ouvrirFenetre(longueur_fenetre, hauteur_fenetre)
        
    
    def ecran_depart(self):
        """
        Affiche les paramettres de la cession au debut de celle-ci
        """
        
        interval_long = int(self.longueur_fenetre/20)
        interval_haut = int(self.hauteur_fenetre/20)

        if (self.longueur_fenetre >= 100) and (self.hauteur_fenetre >= 100):
            
            self.tki_objects['depart_tire'] = self.tki_objects['fenetre'].afficherTexte('Parametres de session (cliquer pour lancer)', int(self.longueur_fenetre/2), interval_haut)
            
            self.tki_objects['depart_txt_pred'] = self.tki_objects['fenetre'].afficherTexte("Proie", interval_long*4, interval_haut*3)
            self.tki_objects['depart_col_pred'] = self.tki_objects['fenetre'].dessinerDisque(interval_long, interval_haut*3, 3, 'green')

            
            self.tki_objects['depart_txt_proi'] = self.tki_objects['fenetre'].afficherTexte("Predateur",  int(self.longueur_fenetre/2)+interval_long*4, interval_haut*3)
            self.tki_objects['depart_col_proi'] = self.tki_objects['fenetre'].dessinerDisque(int(self.longueur_fenetre/2)+interval_long, interval_haut*3, 3, 'brown')

            
            self.tki_objects['depart_PROIE_VITESSE'] = self.tki_objects['fenetre'].afficherTexte(f"Vitesse : {self.PROIE_VITESSE}", interval_long*4, interval_haut*5)
            self.tki_objects['depart_vit_proie'] = self.tki_objects['fenetre'].dessinerCercle(interval_long, interval_haut*3, self.PROIE_VITESSE, 'green')

            
            self.tki_objects['depart_PROIE_VUE'] = self.tki_objects['fenetre'].afficherTexte(f"Vue : {self.PROIE_VUE}", interval_long*4, interval_haut*6)
            self.tki_objects['depart_vue_proie'] = self.tki_objects['fenetre'].dessinerCercle(interval_long, interval_haut*3, self.PROIE_VUE, 'green')

            
            self.tki_objects['depart_PROIE_DUREE_VIE'] = self.tki_objects['fenetre'].afficherTexte(f"Duree de vie (en tours) : {self.PROIE_DUREE_VIE}", interval_long*4, interval_haut*7)
            self.tki_objects['depart_DISTANCE_REPRODUCTION'] = self.tki_objects['fenetre'].afficherTexte(f"Distance reproduction : {self.DISTANCE_REPRODUCTION}", interval_long*4, interval_haut*8)
            self.tki_objects['depart_DEPART_NOMBRE_PROIES'] = self.tki_objects['fenetre'].afficherTexte(f"Depart nb proies : {self.DEPART_NOMBRE_PROIES}", interval_long*4, interval_haut*9)
            
            
            self.tki_objects['depart_PREDATEUR_VITESSE'] = self.tki_objects['fenetre'].afficherTexte(f"Vitesse : {self.PREDATEUR_VITESSE}", int(self.longueur_fenetre/2)+interval_long*4, interval_haut*5)
            self.tki_objects['depart_vit_pred'] = self.tki_objects['fenetre'].dessinerCercle(int(self.longueur_fenetre/2)+interval_long, interval_haut*3, self.PREDATEUR_VITESSE, 'brown')

            self.tki_objects['depart_PREDATEUR_VUE'] = self.tki_objects['fenetre'].afficherTexte(f"Vue : {self.PREDATEUR_VUE}", int(self.longueur_fenetre/2)+interval_long*4, interval_haut*6)
            self.tki_objects['depart_vue_pred'] = self.tki_objects['fenetre'].dessinerCercle(int(self.longueur_fenetre/2)+interval_long, interval_haut*3, self.PREDATEUR_VUE, 'brown')
            
            self.tki_objects['depart_PREDATEUR_DUREE_VIE'] = self.tki_objects['fenetre'].afficherTexte(f"Duree de vie (en tours) : {self.PREDATEUR_DUREE_VIE}", int(self.longueur_fenetre/2)+interval_long*4, interval_haut*7)
            self.tki_objects['depart_PREDATEUR_BESOIN_COUPLE'] = self.tki_objects['fenetre'].afficherTexte(f"Besoin couple : {self.PREDATEUR_BESOIN_COUPLE}", int(self.longueur_fenetre/2)+interval_long*4, interval_haut*8)
            self.tki_objects['depart_PREDATEUR_STAMINA_DEPART'] = self.tki_objects['fenetre'].afficherTexte(f"Stamina depart : {self.PREDATEUR_STAMINA_DEPART}", int(self.longueur_fenetre/2)+interval_long*4, interval_haut*9)
            self.tki_objects['depart_PREDATEUR_STAMINA_GAIN'] = self.tki_objects['fenetre'].afficherTexte(f"Gain par repas (en stam) : {self.PREDATEUR_STAMINA_GAIN}", int(self.longueur_fenetre/2)+interval_long*4, interval_haut*10)
            self.tki_objects['depart_PREDATEUR_STAMINA_ENFANTS'] = self.tki_objects['fenetre'].afficherTexte(f"Cout enfant (en stam) : {self.PREDATEUR_STAMINA_ENFANTS}", int(self.longueur_fenetre/2)+interval_long*4, interval_haut*11)
            self.tki_objects['depart_DEPART_NOMBRE_PREDATEURS'] = self.tki_objects['fenetre'].afficherTexte(f"Depart nb predateurs : {self.DEPART_NOMBRE_PREDATEURS}", int(self.longueur_fenetre/2)+interval_long*4, interval_haut*12)
            
            self.tki_objects['depart_TOURS'] = self.tki_objects['fenetre'].afficherTexte(f"Nb tours : {self.TOURS}", int(self.longueur_fenetre/2), interval_haut*15)
            self.tki_objects['depart_HAUTEUR_PLATEAU'] = self.tki_objects['fenetre'].afficherTexte(f"Heuteur Plateau : {self.HAUTEUR_PLATEAU}", int(self.longueur_fenetre/2), interval_haut*16)
            self.tki_objects['depart_LONGUEUR_PLATEAU'] = self.tki_objects['fenetre'].afficherTexte(f"Longueur plateau : {self.LONGUEUR_PLATEAU}", int(self.longueur_fenetre/2), interval_haut*17)
            self.tki_objects['depart_affichage_donnees'] = self.tki_objects['fenetre'].afficherTexte(f"Affichage données : {self.affichage_donnees}", int(self.longueur_fenetre/2), interval_haut*18)
            self.tki_objects['depart_affichage_live_graph'] = self.tki_objects['fenetre'].afficherTexte(f"Live graphs : {self.LIVE_GRAPHS}", int(self.longueur_fenetre/2), interval_haut*19)
            
        self.grande_suppression()

    def init_graphique(self,
                       nb_proies = 10, 
                       nb_predateurs = 10):
        """Cree tout les elements necessaires au deroulement de la situation

        Args:
            nb_proies (int, optional): nombre de proies au debut de la simulation. Defaults to 10.
            nb_predateurs (int, optional): nombre de predateurs au debut de la simulation. Defaults to 10.

        Raises:
            Exception: Si il y plus d'annimaux a crrer que de cases disponibles sur la plateau
        """
            
        if "Data" in os.listdir():
            
            if self.BACKGROUND and ("Bc.jpg" in os.listdir("Data")) and (self.HAUTEUR_PLATEAU >= 100 and self.LONGUEUR_PLATEAU >= 100):
                
                try:
                    self.tki_objects['plateau'] = self.tki_objects['fenetre'].afficherImage(0, 0, 'Data/Bc.jpg', self.LONGUEUR_PLATEAU, self.HAUTEUR_PLATEAU)
                
                except:

                    self.tki_objects['plateau'] = self.tki_objects['fenetre'].dessinerRectangle(0, 0, self.LONGUEUR_PLATEAU, self.HAUTEUR_PLATEAU, 'darkblue')
            
            else:
        
                self.tki_objects['plateau'] = self.tki_objects['fenetre'].dessinerRectangle(0, 0, self.LONGUEUR_PLATEAU, self.HAUTEUR_PLATEAU, 'darkblue')
            
        else:
                  
            os.mkdir("Data")

            self.tki_objects['plateau'] = self.tki_objects['fenetre'].dessinerRectangle(0, 0, self.LONGUEUR_PLATEAU, self.HAUTEUR_PLATEAU, 'darkblue')
            #si le dossier Data n'existe pas, on le cree car la suite du programe en a besoin et on met en background le bleu par defaut car le fichier Bc.jpeg n'existe logiquement pas

        self.tki_objects['separatrice_gauche'] = self.tki_objects['fenetre'].dessinerLigne(self.LONGUEUR_PLATEAU, 0, self.LONGUEUR_PLATEAU, self.HAUTEUR_PLATEAU, 'white', 3)
        self.tki_objects['separatrice_bas'] = self.tki_objects['fenetre'].dessinerLigne(0, self.HAUTEUR_PLATEAU, self.LONGUEUR_PLATEAU, self.HAUTEUR_PLATEAU, 'white', 3)
        
        if (nb_predateurs + nb_proies) > len(range(self.HAUTEUR_PLATEAU+self.LONGUEUR_PLATEAU)):
            
            raise Exception(f"Trop d'annimaux pour le nombre d'espace disponible ({nb_predateurs + nb_proies} pour {len(range(self.HAUTEUR_PLATEAU+self.LONGUEUR_PLATEAU))} places)")
        
        for i in range(nb_predateurs):
            
            self.creer_predateur()
        
        for i in range(nb_proies):
        
            self.creer_proie()
        
        if self.affichage_donnees:
            
            colonne = int((self.longueur_fenetre-self.LONGUEUR_PLATEAU)/5)
            hauteau_txt = int(30)
            
            self.tki_objects['txt_total'] = self.tki_objects['fenetre'].afficherTexte('Nombre d\'organismes : ', self.LONGUEUR_PLATEAU+colonne, hauteau_txt)
            self.tki_objects['txt_tour'] = self.tki_objects['fenetre'].afficherTexte('Tour : ', self.LONGUEUR_PLATEAU+colonne, hauteau_txt*2)
            self.tki_objects['txt_proies'] = self.tki_objects['fenetre'].afficherTexte('Nombre de proies : ', self.LONGUEUR_PLATEAU+colonne*3, hauteau_txt)
            self.tki_objects['txt_predateurs'] = self.tki_objects['fenetre'].afficherTexte('Nombre de predateurs : ', self.LONGUEUR_PLATEAU+colonne*3, hauteau_txt*2)

            self.tki_objects['nb_total'] = self.tki_objects['fenetre'].afficherTexte(f'{self.population["total"]}', self.LONGUEUR_PLATEAU+colonne*2, hauteau_txt)
            self.tki_objects['nb_tour'] = self.tki_objects['fenetre'].afficherTexte(f'{self.nb_tour}', self.LONGUEUR_PLATEAU+colonne*2, hauteau_txt*2)
            self.tki_objects['nb_proies'] = self.tki_objects['fenetre'].afficherTexte(f'{self.population["proies"]}', self.LONGUEUR_PLATEAU+colonne*4, hauteau_txt)
            self.tki_objects['nb_predateurs'] = self.tki_objects['fenetre'].afficherTexte(f'{self.population["predateurs"]}', self.LONGUEUR_PLATEAU+colonne*4, hauteau_txt*2)
                    
            if self.DEBUG:
                
                self.tki_objects['txt_total_reel_organismes'] = self.tki_objects['fenetre'].afficherTexte('Total clefs : ', self.LONGUEUR_PLATEAU+95, self.hauteur_fenetre/2)
                self.tki_objects['nb_total_reel_organismes'] = self.tki_objects['fenetre'].afficherTexte(f'{len(self.grille)}', self.LONGUEUR_PLATEAU+95+95, self.hauteur_fenetre/2)

                self.tki_objects['txt_total_objects'] = self.tki_objects['fenetre'].afficherTexte('Total objects : ', self.LONGUEUR_PLATEAU+105, (self.hauteur_fenetre/2)+30)
                self.tki_objects['nb_total_objects'] = self.tki_objects['fenetre'].afficherTexte(f'{len(self.tki_objects.values())}', self.LONGUEUR_PLATEAU+105+105, (self.hauteur_fenetre/2)+30)
        
        if self.LIVE_GRAPHS:
            
            self.tki_objects["green_rectangle"] = self.tki_objects["fenetre"].dessinerRectangle(self.LONGUEUR_PLATEAU, self.hauteur_fenetre/3, self.longueur_fenetre-self.LONGUEUR_PLATEAU+10, int(self.hauteur_fenetre-self.hauteur_fenetre/3)+10, "white")
            
            self.graphs["fig_total"] = plt.figure()
            self.graphs["fig_predateurs"] = plt.figure()
            self.graphs["fig_proies"] = plt.figure()
            
            self.graphs["ax_total"] = self.graphs["fig_total"].add_subplot(1, 1, 1)
            self.graphs["ax_predateurs"] =  self.graphs["fig_predateurs"].add_subplot(1, 1, 1)
            self.graphs["ax_proies"] =  self.graphs["fig_proies"].add_subplot(1, 1, 1)
                
    def grande_suppression(self):
        """
        Supprime tout les elements affichés sur la fenetre graphique
        """
        
        self.tki_objects['fenetre'].attendreClic()
        
        for obj in self.tki_objects.copy().keys():
            
            if obj != "fenetre":
                
                self.tki_objects["fenetre"].supprimer(self.tki_objects[obj])
                self.tki_objects.pop(obj)
    
    @staticmethod
    def distance_euclidienne( coord1 : tuple, coord2 : tuple) -> float:
        """
        Fournit la distance euclidienne etre 2 coordonnées

        Args:
            coord1 (tuple): (x, y)
            coord2 (tuple): (x, y)

        Returns:
            float: distance euclidienne
        """
        
        return pow((pow((coord1[0] - coord2[0]), 2) + pow((coord1[1] - coord2[1]), 2)), 0.5)

    def rand_vecd(self, id):
        """Donne un vecteur random adapté a un individu selon sa vitesse

        Args:
            id (int): ID de l'individu

        Returns:
            tuple: vecteur (x, y) aléatoire
            
        """
        rand_moovement_v1 = random.random()
                            
        (v1, v2) = (int(rand_moovement_v1 * self.vitesse[id]), int((1-rand_moovement_v1) * self.vitesse[id]))
        
        if random.random() > 0.5:
            
            (v1, v2) = (-v1, v2)
        
        if random.random() > 0.5:
            
            (v1, v2) = (v1, -v2)
        
        return (v1, v2)

    def creer_predateur(self, 
                        pos : tuple = None, 
                        stam : int = None, 
                        gain_stam : int = None, 
                        vit: int = None,
                        voir : int = None):
        """Cree un nouveau predateur

        Args:
            pos (tuple, optional): position du nouveau predateur. Defaults to None.
            stam (int, optional): stamina de depart du predateur. Defaults to None.
            gain_stam (int, optional): gain par proie du predateur. Defaults to None.
            vit (int, optional): vitesse du predateur. Defaults to None.
            voir (int, optional): vue du predateur. Defaults to None.
        """
        
        if stam == None:
            
            stam = self.PREDATEUR_STAMINA_DEPART
        
        if gain_stam == None:
            
            gain_stam = self.PREDATEUR_STAMINA_GAIN
        
        if vit == None:
            
            vit = self.PREDATEUR_VITESSE
        
        if voir == None:
            
            voir = self.PREDATEUR_VUE

        if pos == None:
            
            (x, y) = (random.randint(0, self.HAUTEUR_PLATEAU), random.randint(0, self.LONGUEUR_PLATEAU))
            
            while (x, y) in self.grille:
                
                (x, y) = (random.randint(0, self.HAUTEUR_PLATEAU), random.randint(0, self.LONGUEUR_PLATEAU))
                
            self.grille[(x, y)] = self.population["nb_indiv"]
            
            
        elif (pos not in self.grille):
            
            self.grille[pos] = self.population["nb_indiv"]
            (x, y) = pos
            
        else:
            return
        
        if self.genetique:
        
            if random.random() <= self.EPSILON_PROIES_VITESSE:
                
                vit += 1
        
            if random.random() <= self.EPSILON_PREDATEURS_VUE:
                
                voir += 1
        
        self.age[self.population["nb_indiv"]] = 0
        self.duree_vie[self.population["nb_indiv"]] = self.PREDATEUR_DUREE_VIE
        self.stamina[self.population["nb_indiv"]] = stam
        self.gain_stamina[self.population["nb_indiv"]] = gain_stam
            
        self.peut_enfanter[self.population["nb_indiv"]] = False
        self.vitesse[self.population["nb_indiv"]] = vit
        self.enfants[self.population["nb_indiv"]] = 0
        self.victimes[self.population["nb_indiv"]] = 0
        self.type[self.population["nb_indiv"]] = "predateur"
        self.vue[self.population["nb_indiv"]] = voir
        self.en_vie[self.population["nb_indiv"]] = True
        self.en_traque[self.population["nb_indiv"]] = True
        
        self.tki_objects[self.population["nb_indiv"]] = self.tki_objects['fenetre'].dessinerDisque(x, y, 3, 'dark red')
        
        #tki_objects[population["nb_indiv"]] = plateau.afficherImage(position[population["nb_indiv"]][0], position[population["nb_indiv"]][1], "renard.png", 10, 10)
        #images desactivee pour cause de consommation de memoire vive
        
        self.population["predateurs"] += 1
        self.population["nb_indiv"] += 1
        self.population["total"] += 1

    def creer_proie(self,
                    pos : tuple = None, 
                    vit: int = None,
                    voir : int = None):
        """Cree une nouvelle proie

        Args:
            pos (tuple, optional): position de la proie. Defaults to None.
            vit (int, optional): vitesse de la proie. Defaults to None.
            voir (int, optional): vue de la proie. Defaults to None.
        """
        
        if vit == None:
            
            vit = self.PROIE_VITESSE
        
        if voir == None:
            
            voir = self.PROIE_VUE
        
        if pos == None:
            (x, y) = (random.randint(0, self.HAUTEUR_PLATEAU), random.randint(0, self.LONGUEUR_PLATEAU))
            
            while (x, y) in self.grille:
                
                (x, y) = (random.randint(0, self.HAUTEUR_PLATEAU), random.randint(0, self.LONGUEUR_PLATEAU))
            
            self.grille[(x, y)] = self.population["nb_indiv"]
            
        elif (pos not in self.grille) and (len(self.surroundings(pos, self.DISTANCE_REPRODUCTION).keys()) <= 0):

            self.grille[pos] = self.population["nb_indiv"]
            (x, y) = pos
            
        else:
            
            return
            #raise Exception(f"Erreur création, pos : {pos}, vit : {vit}, voir : {voir}, \nsuroundings : {surroundings(pos, DISTANCE_REPRODUCTION)}")
        
        self.age[self.population["nb_indiv"]] = 0
        self.duree_vie[self.population["nb_indiv"]] = self.PROIE_DUREE_VIE
            
        self.peut_enfanter[self.population["nb_indiv"]] = False
        
        
        if self.genetique:
        
            if random.random() <= self.EPSILON_PROIES_VITESSE:
                
                vit += 1
                
            if random.random() <= self.EPSILON_PROIES_VUE:
                
                voir += 1
        
        self.vitesse[self.population["nb_indiv"]] = vit
        
        self.enfants[self.population["nb_indiv"]] = 0
        self.type[self.population["nb_indiv"]] = "proie"
        self.vue[self.population["nb_indiv"]] = voir
        self.en_vie[self.population["nb_indiv"]] = True
        
        self.tki_objects[self.population["nb_indiv"]] = self.tki_objects['fenetre'].dessinerDisque(x, y, 3, 'green')
        
        #tki_objects[population["nb_indiv"]] = plateau.afficherImage(position[population["nb_indiv"]][0], position[population["nb_indiv"]][1], "lapin.png", 5, 5)
        
        self.population["proies"] += 1
        self.population["nb_indiv"] += 1
        self.population["total"] += 1

    def surroundings(self, position_organisme : tuple, distance : float = None) -> tuple:
        """Retourne l'environement autour d'un point à une distance variaable

        Args:
            position_organisme (tuple): point de depart de la recherche (x, y)
            distance (float, optional): etandude de la recherche (en pixels). Defaults to None.

        Returns:
            dict: position -> distance par rapport a position_organisme
        """
        
        if distance == None:
            
            distance = self.vue[self.grille[position_organisme]]
        
        autour : dict = {}
        
        for y in range(int(max(0, position_organisme[1]-distance)), int(min(position_organisme[1]+distance, self.HAUTEUR_PLATEAU))):
            
            for x in range(int(max(0, int(position_organisme[0]-distance))), int(min(int(position_organisme[0]+distance), self.LONGUEUR_PLATEAU))):
                
                if ((x, y) in self.grille) and (self.en_vie[self.grille[(x, y)]]):
                    
                    autour[(x, y)] = self.distance_euclidienne(position_organisme, (x, y))
                    
        return autour
    
    def flair_pred(self, pos, max_dist = None, dist = 1) -> tuple:
        """Permet recursivement de trouver la proie la plus proche d'un certain predateur, dependant de sa zone de recherche

        Args:
            pos (_type_): position du predateur
            max_dist (_type_, optional): distance de recherche maximale. Defaults to None.
            dist (int, optional): distance de recherche actuelle. Defaults to 1.

        Returns:
            tuple: ((position proie), distance par rapport au predateur)
        """
        
        if max_dist == None:
            
            max_dist = self.vue[self.grille[pos]]
        
        if dist > max_dist:
            
            return None
        
        else:
            
            for v in range(dist+1):
                
                for p in ((pos[0] + (dist-v), pos[1] + v), (pos[0] - (dist-v), pos[1] - v), (pos[0] + (dist-v), pos[1] - v), (pos[0] - (dist-v), pos[1] + v)):

                    if (p in self.grille) and (self.en_vie[self.grille[p]]) and (self.type[self.grille[p]] == "proie"):
                        
                        return (p, self.distance_euclidienne(pos, p))
        
        return self.flair_pred(pos, max_dist, dist+1)

        
    def mort(self, id):
        """Supprime les differentes variables qui deffinissent un organisme et l'efface du plateau

        Args:
            id (_type_): clefs d'identification de l'organisme en question
        """

        if id in self.tki_objects:
            
            self.population["total"] -= 1
            
            if self.type[id] == "predateur":
                self.stamina.pop(id)
                self.gain_stamina.pop(id)
                self.victimes.pop(id)
                self.population["predateurs"] -= 1
                self.en_traque.pop(id)
            else:
                
                self.population["proies"] -= 1

            self.age.pop(id)
            self.vitesse.pop(id)
            self.enfants.pop(id)
            self.vue.pop(id)
            self.tki_objects['fenetre'].supprimer(self.tki_objects[id])
            self.tki_objects.pop(id)
            self.peut_enfanter.pop(id)
            self.type.pop(id)
        
    def tour(self):
        """Deroulement d'un tour de jeu

        Raises:
            Exception: Erreur de deplaceement d'objet tkiteasy
        """
        
        for k in self.peut_enfanter.keys():
            
            if self.type[k] == 'proie':
                
                self.peut_enfanter[k] = True
            
            else:
                
                if self.stamina[k] >= self.PREDATEUR_STAMINA_ENFANTS + self.PREDATEUR_STAMINA_DEPART:
                    
                    self.peut_enfanter[k] = True
                
                else:
                    
                    self.peut_enfanter[k] = False
        
        nouveaux_organismes = {}
        
        nouveaux_morts : set = {0, 1}
        for i in range(2):
            nouveaux_morts.remove(i)

        for pos in self.grille.copy():
            
            if self.en_vie[self.grille[pos]] == True:
                
                self.age[self.grille[pos]] += 1
                
                if self.age[self.grille[pos]] >= self.duree_vie[self.grille[pos]]:
                    
                    self.en_vie[self.grille[pos]] = False
                    nouveaux_morts.add(self.grille[pos])
                    continue
                
                elif self.type[self.grille[pos]] == "proie":
                    
                    if self.peut_enfanter[self.grille[pos]]:
                        
                        arround = self.surroundings(pos, self.vitesse[self.grille[pos]])
                        
                        for p in arround.keys():
                            
                            if self.type[self.grille[p]] == "proie" and self.peut_enfanter[self.grille[p]]:
                                
                                (v1, v2) = self.rand_vecd(self.grille[pos])
                                
                                if ((int(pos[0] + v1), int(pos[1] + v2)) not in arround.values()) and (self.HAUTEUR_PLATEAU > (int(pos[0] + v1)) > 0) and (self.LONGUEUR_PLATEAU > int(pos[1] + v2) > 0):
                                    
                                    self.peut_enfanter[self.grille[pos]] = False
                                    self.enfants[self.grille[pos]] += 1
                                    
                                    self.peut_enfanter[self.grille[p]] = False
                                    self.enfants[self.grille[p]] += 1
                                    
                                    parent1 = self.grille[pos]
                                    parent2 = self.grille[p]
                                    nouveaux_organismes[len(nouveaux_organismes.keys())] = {"type" : "proie", 
                                                                                            "position" : (int(pos[0] + v1), int(pos[1] + v2)),
                                                                                            "parents" : (parent1, parent2)}
                                    
                                    continue
                    
                    (v1, v2) = self.rand_vecd(self.grille[pos])
                    
                    if ((int(pos[0] + v1), int(pos[1] + v2)) not in self.grille) and (self.LONGUEUR_PLATEAU > (int(pos[0] + v1)) > 0) and (self.HAUTEUR_PLATEAU > int(pos[1] + v2) > 0):
                        
                        self.grille[(int(pos[0] + v1), int(pos[1] + v2))] = self.grille[pos]
                        self.grille.pop(pos)
                        
                        try:
                            
                            self.tki_objects['fenetre'].deplacer(self.tki_objects[self.grille[(int(pos[0] + v1), int(pos[1] + v2))]], v1, v2)
                            
                        except:
                            
                            raise Exception(f"Session interrompue")
                    
                elif self.type[self.grille[pos]] == "predateur":
                    
                    if self.peut_enfanter[self.grille[pos]]:
                        
                        arround = self.surroundings(pos, self.vitesse[self.grille[pos]])
                        
                        if self.PREDATEUR_BESOIN_COUPLE:
                            
                            for p in arround.keys():
                                
                                if self.type[self.grille[p]] == "predateur" and self.peut_enfanter[self.grille[p]]:
                                    
                                    (v1, v2) = self.rand_vecd(self.grille[pos])
                                    
                                    if ((int(pos[0] + v1), int(pos[1] + v2)) not in self.grille) and (self.LONGUEUR_PLATEAU > (int(pos[0] + v1)) > 0) and (self.HAUTEUR_PLATEAU > int(pos[1] + v2) > 0):
                                        
                                        self.stamina[self.grille[pos]] -= self.PREDATEUR_STAMINA_ENFANTS
                                        self.stamina[self.grille[p]] -= self.PREDATEUR_STAMINA_ENFANTS
                                        
                                        self.peut_enfanter[self.grille[pos]] = False
                                        self.peut_enfanter[self.grille[p]] = False

                                        self.enfants[self.grille[pos]] += 1
                                        self.enfants[self.grille[p]] += 1
                                        
                                        parent1 = self.grille[pos]
                                        parent2 = self.grille[p]

                                        nouveaux_organismes[len(nouveaux_organismes.keys())] = {"type" : "predateur", 
                                                                                                "position" : (int(pos[0] + v1), int(pos[1] + v2)),
                                                                                                "parents" : (parent1, parent2)}
                                        
                                        continue
                            
                        else:

                            (v1, v2) = self.rand_vecd(self.grille[pos])
                            
                            if ((int(pos[0] + v1), int(pos[1] + v2)) not in self.grille) and (self.LONGUEUR_PLATEAU > (int(pos[0] + v1)) > 0) and (self.HAUTEUR_PLATEAU > int(pos[1] + v2) > 0):
                                
                                self.stamina[self.grille[pos]] -= self.PREDATEUR_STAMINA_ENFANTS
                                
                                self.peut_enfanter[self.grille[pos]] = False
                                self.enfants[self.grille[pos]] += 1
                                
                                parent1 = self.grille[pos]

                                nouveaux_organismes[len(nouveaux_organismes.keys())] = {"type" : "predateur", 
                                                                                        "position" : (int(pos[0] + v1), int(pos[1] + v2)),
                                                                                        "parents" : (parent1, parent1)}
                                

                    if self.en_traque[self.grille[pos]]:
                        min_proie = self.flair_pred(pos)
                    else:
                        
                        #print(f"debut : {self.vue[self.grille[pos]]-self.vitesse[self.grille[pos]]}, vue : {self.vue[self.grille[pos]]}, vitesse : {self.vitesse[self.grille[pos]]}")
                        
                        min_proie = self.flair_pred(pos, dist=(self.vue[self.grille[pos]]-self.vitesse[self.grille[pos]]))


                    if min_proie == None:
                        
                        self.en_traque[self.grille[pos]] = False

                        (v1, v2) = self.rand_vecd(self.grille[pos])
                        
                        if ((int(pos[0] + v1), int(pos[1] + v2)) != pos) and ((int(pos[0] + v1), int(pos[1] + v2)) not in self.grille) and (self.LONGUEUR_PLATEAU > (int(pos[0] + v1)) > 0) and (self.HAUTEUR_PLATEAU > int(pos[1] + v2) > 0):
                            
                            self.grille[(int(pos[0] + v1), int(pos[1] + v2))] = self.grille[pos]
                            self.grille.pop(pos)
                            
                            try:
                                
                                self.tki_objects['fenetre'].deplacer(self.tki_objects[self.grille[(int(pos[0] + v1), int(pos[1] + v2))]], v1, v2)
                                
                            except:
                                
                                raise Exception(f"Session interrompue")
                    
                    elif min_proie[1] < self.vitesse[self.grille[pos]]:
                        
                        self.en_traque[self.grille[pos]] = True
                        
                        self.en_vie[self.grille[min_proie[0]]] = False
                        nouveaux_morts.add(self.grille[min_proie[0]])
                        
                        self.grille[min_proie[0]] = self.grille[pos]
                        self.grille.pop(pos)
                        
                        self.victimes[self.grille[min_proie[0]]] += 1
                        self.stamina[self.grille[min_proie[0]]] += self.gain_stamina[self.grille[min_proie[0]]]
                        
                    elif min_proie[1] == self.vitesse[self.grille[pos]]:
                        
                        self.en_traque[self.grille[pos]] = True
                        
                        self.en_vie[self.grille[min_proie[0]]] = False
                        nouveaux_morts.add(self.grille[min_proie[0]])
                        
                        self.grille[min_proie[0]] = self.grille[pos]
                        
                        self.victimes[self.grille[min_proie[0]]] += 1
                        self.stamina[self.grille[min_proie[0]]] += self.gain_stamina[self.grille[min_proie[0]]]
                    
                    else :
                        
                        self.en_traque[self.grille[pos]] = True
                        
                        (delta_x, delta_y) = ((min_proie[0][0] - pos[0]), (min_proie[0][1] - pos[1]))

                        (v1, v2) = (int((delta_x/min_proie[1]) * self.vitesse[self.grille[pos]]), int((delta_y/min_proie[1]) * self.vitesse[self.grille[pos]]))
                        
                        if ((int(pos[0] + v1), int(pos[1] + v2)) != pos) and ((int(pos[0] + v1), int(pos[1] + v2)) not in self.grille) and (self.HAUTEUR_PLATEAU > (int(pos[0] + v1)) > 0) and (self.LONGUEUR_PLATEAU > int(pos[1] + v2) > 0):
                            
                            
                            self.grille[(int(pos[0] + v1), int(pos[1] + v2))] = self.grille[pos]
                            self.grille.pop(pos)
                            
                            self.tki_objects['fenetre'].deplacer(self.tki_objects[self.grille[(int(pos[0] + v1), int(pos[1] + v2))]], v1, v2)
            
        for i in nouveaux_organismes.keys():
            
            if nouveaux_organismes[i]['type'] == 'proie':
                
                self.creer_proie(nouveaux_organismes[i]['position'], vit = max(self.vitesse[nouveaux_organismes[i]['parents'][0]], self.vitesse[nouveaux_organismes[i]['parents'][1]]), voir = max(self.vue[nouveaux_organismes[i]['parents'][0]], self.vue[nouveaux_organismes[i]['parents'][1]]))
            
            else:
                
                self.creer_predateur(nouveaux_organismes[i]['position'],  vit = max(self.vitesse[nouveaux_organismes[i]['parents'][0]], self.vitesse[nouveaux_organismes[i]['parents'][1]]), voir = max(self.vue[nouveaux_organismes[i]['parents'][0]], self.vue[nouveaux_organismes[i]['parents'][1]]))
        
        for k in nouveaux_morts:
            
            self.mort(k)
                
        
        if self.affichage_donnees:
            
            self.tki_objects['fenetre'].changerTexte(self.tki_objects["nb_total"], f'{self.population["total"]}')
            self.tki_objects['fenetre'].changerTexte(self.tki_objects['nb_tour'], f'{self.nb_tour}')
            self.tki_objects['fenetre'].changerTexte(self.tki_objects['nb_proies'], f'{self.population["proies"]}')
            self.tki_objects['fenetre'].changerTexte(self.tki_objects["nb_predateurs"], f'{self.population["predateurs"]}')
            
            if self.DEBUG:
        
                self.tki_objects['fenetre'].changerTexte(self.tki_objects['nb_total_reel_organismes'], f'{len(self.grille)}')
                self.tki_objects['fenetre'].changerTexte(self.tki_objects['nb_total_objects'], f'{len(self.tki_objects.values())}')
        
        if self.LIVE_GRAPHS:
            
            hauteur_image = int((self.hauteur_fenetre-self.hauteur_fenetre/3)/int(self.hauteur_fenetre*0.004))
            
            self.graphs["ax_total"] = self.graphs["fig_total"].add_subplot(1, 1, 1)
            self.graphs["ax_predateurs"] =  self.graphs["fig_predateurs"].add_subplot(1, 1, 1)
            self.graphs["ax_proies"] =  self.graphs["fig_proies"].add_subplot(1, 1, 1)
            
            self.graphs["ax_total"].clear()
            self.graphs["ax_predateurs"].clear()
            self.graphs["ax_proies"].clear()
            
            self.graphs["fig_total"].delaxes(self.graphs["fig_total"].axes[0])
            self.graphs["fig_predateurs"].delaxes(self.graphs["fig_predateurs"].axes[0])
            self.graphs["fig_proies"].delaxes(self.graphs["fig_proies"].axes[0])
            
            x = [i for i in range(1, len(self.historique_populations['total'])+1)]
            
            self.graphs["ax_total"].plot(x, self.historique_populations['total'], c="blue")
            self.graphs["ax_proies"].plot(x, self.historique_populations['proies'], c="green")
            self.graphs["ax_predateurs"].plot(x, self.historique_populations['predateurs'], c="red")
            
            self.graphs["ax_total"].set_title('Total')
            self.graphs["ax_predateurs"].set_title('Predateurs')
            self.graphs["ax_proies"].set_title('Proies')
            
            self.graphs["fig_total"].savefig("Data/live_total.png")
            self.graphs["fig_proies"].savefig("Data/live_proies.png")
            self.graphs["fig_predateurs"].savefig("Data/live_predateurs.png")
            
            if "live_total" in self.tki_objects:
                
                self.tki_objects["fenetre"].supprimer(self.tki_objects["live_total"])
                self.tki_objects["fenetre"].supprimer(self.tki_objects["live_predateurs"])
                self.tki_objects["fenetre"].supprimer(self.tki_objects["live_proies"])
                
                self.tki_objects["live_total"] = self.tki_objects["fenetre"].afficherImage(self.LONGUEUR_PLATEAU, int(self.hauteur_fenetre/3), 'Data/live_total.png', self.longueur_fenetre- (self.LONGUEUR_PLATEAU+15), hauteur_image)
                self.tki_objects["live_predateurs"] = self.tki_objects["fenetre"].afficherImage(self.LONGUEUR_PLATEAU, int(self.hauteur_fenetre/3)+hauteur_image, 'Data/live_predateurs.png', self.longueur_fenetre- (self.LONGUEUR_PLATEAU+15), hauteur_image)
                self.tki_objects["live_proies"] = self.tki_objects["fenetre"].afficherImage(self.LONGUEUR_PLATEAU, int(self.hauteur_fenetre/3)+(hauteur_image*2), 'Data/live_proies.png', self.longueur_fenetre- (self.LONGUEUR_PLATEAU+15), hauteur_image)
                
            else:
                
                self.tki_objects["live_total"] = self.tki_objects["fenetre"].afficherImage(self.LONGUEUR_PLATEAU, int(self.hauteur_fenetre/3), 'Data/live_total.png', self.longueur_fenetre- (self.LONGUEUR_PLATEAU+15), hauteur_image)
                self.tki_objects["live_predateurs"] = self.tki_objects["fenetre"].afficherImage(self.LONGUEUR_PLATEAU, int(self.hauteur_fenetre/3)+hauteur_image, 'Data/live_predateurs.png', self.longueur_fenetre- (self.LONGUEUR_PLATEAU+15), hauteur_image)
                self.tki_objects["live_proies"] = self.tki_objects["fenetre"].afficherImage(self.LONGUEUR_PLATEAU, int(self.hauteur_fenetre/3)+(hauteur_image*2), 'Data/live_proies.png', self.longueur_fenetre- (self.LONGUEUR_PLATEAU+15), hauteur_image)
                
        self.tki_objects['fenetre'].actualiser()
        
        return

    def fin(self):
        """Ferme la fenetre graphique
        """
        
        self.tki_objects['fenetre'].attendreClic()
        self.tki_objects['fenetre'].fermerFenetre()

            ##2.      Analyse     ##

    def dv_graph(self, var_to_plot, save_path, format, title = '', range_xaxis = False, tecklabels_xaxis = False):
        """Sauvegarde un graphique matplotlib des variables demandées sous la forme d'un format donné a une destination donnée

        Args:
            var_to_plot (_dict_): variable et couleur de la ligne ("nom_variable" : "couleur")
            save_path (_str_): Path pour stocker l'image
            format (_str_): format de l'image (jpg recommandé)
            title (str, optional): Titre du graph. Defaults to ''.
            range_xaxis (bool, optional): . Defaults to False.
            tecklabels_xaxis (bool, optional): . Defaults to False.

        Returns:
            fig: graphique matplotlib
            Path: ou est stockée l'image
        """
        
        fig, ax = plt.subplots()

        for i in var_to_plot.keys():

            ax.plot(range(len(self.historique_populations[i])), self.historique_populations[i], c = var_to_plot[i], label = i)

        ax.legend(loc='center left', bbox_to_anchor=(0, 0.9))
        
        #ax.yaxis.grid(True)
        #ax.xaxis.grid(True)
        
        if range_xaxis:
            
            ax.xaxis.set_ticks(range(0, self.TOURS))
        
            if tecklabels_xaxis:
                
                ax.xaxis.set_ticklabels([None if (i%int(self.TOURS/10) and i != (self.TOURS-1)) else i for i in range(0, self.TOURS)])
        
        ax.set_title(title)
        fig.savefig(f'{save_path}.{format}')
        
        return fig, f'{save_path}.{format}'


    def plot_popultaions(self):
        """ecran de fin qui resumme la session a travers les graphiques principaux
        """
        
        hauteur_image = int(self.hauteur_fenetre*0.15)
        
        self.graphs['final_pop_graph'] = self.dv_graph({ "total" : "blue", "predateurs" : "red", "proies" : "green"}, 'Data/final_pop_graph', 'jpeg', 'Resumé propulatio totale', True, True)
        self.tki_objects['final_pop_graph'] = self.tki_objects['fenetre'].afficherImage(int(self.longueur_fenetre/2), int(self.hauteur_fenetre/2), self.graphs['final_pop_graph'][1], int(self.longueur_fenetre/2), int(self.hauteur_fenetre/2)-hauteur_image)
        
        self.graphs['final_vit'] = self.dv_graph({ "avg_vitesse_pred" : "red", "avg_vitesse_proi" : "green"}, 'Data/final_pop_graph', 'jpeg', "Vitesse moyenne selon le type d\'indiv", True, True)
        self.tki_objects['final_vit'] = self.tki_objects['fenetre'].afficherImage(0, int(self.hauteur_fenetre/2), self.graphs['final_vit'][1], int(self.longueur_fenetre/2), int(self.hauteur_fenetre/2)-hauteur_image)
        
        self.graphs['final_vue'] = self.dv_graph({ "avg_vue_pred" : "red", "avg_vue_proi" : "green"}, 'Data/final_pop_graph', 'jpeg', "Vue moyenne selon le type d\'indiv", True, True)
        self.tki_objects['final_vue'] = self.tki_objects['fenetre'].afficherImage(0, hauteur_image, self.graphs['final_vue'][1], int(self.longueur_fenetre/2), int(self.hauteur_fenetre/2)-hauteur_image)
        
        self.tki_objects['fin_titre'] = self.tki_objects['fenetre'].afficherTexte('Résumé de session (cliquer pour finir)', int(self.longueur_fenetre/2), int(hauteur_image/2))
        
    def deroulement(self,
                    
                    hauteur_plateau : int,
                    tours : int,
                    
                    depart_nb_predateurs : int, 
                    depart_nb_proies : int,
                    
                    live_graphs = False, 
                    
                    hauteur_fenetre = 1000,
                    longueur_fenetre = 1000,
                    
                    
                    proies_epsilon_vitesse = 0,
                    proies_epsilon_vue = 0,
                    
                    predateurs_epsilon_vitesse = 0,
                    predateurs_epsilon_vue = 0,
                    
                    affichage_donnees = True,
                    
         
                    predateur_stamina_depart = 60,
                    predateur_stamina_gain = 100,
                    predateur_stamina_enfants = 40,
                    predateur_vitesse = None,
                    predateur_vue = None,
                    predateur_duree_vie = None,
                    
                    proie_vitesse = None,
                    proie_vue = None,
                    proie_duree_vie = None,
                    proie_distance_reprod = None,
                    
                    random_seed = None,
                    
                    background = True, 
                    equilibrage_predateurs = False,
                    predateur_besoin_couple = False,
                    debug = False):
        """Lance la visualisation d'une simulation avec les variables demandées.

        Args:
            hauteur_plateau (int): hauteur du plateau (carre) (en pixels).
            tours (int): nombre de tours de la simulation.
            depart_nb_predateurs (int): nombre de predateurs au debut de la similation.
            depart_nb_proies (int): nombre de proies au debut de la simulation.
            live_graphs (bool, optional): {True, False}. Defaults to False.
            hauteur_fenetre (int, optional): hauteur de la fenetre graphique (en pixels). Defaults to 1000.
            longueur_fenetre (int, optional): longueur de la fenetre graphique (en pixels). Defaults to 1000.
            proies_epsilon_vitesse (float, optional): pourcentage de chance de mutation de vitesse pour les proies. Defaults to 0.1.
            proies_epsilon_vue (float, optional): pourcentage de chance de mutation de vuz pour les proies. Defaults to 0.1.
            predateurs_epsilon_vitesse (float, optional): pourcentage de chance de mutation de vitesse pour les predateurs. Defaults to 0.1.
            predateurs_epsilon_vue (float, optional): pourcentage de chance de mutation de vuz pour les predateurs. Defaults to 0.1.
            affichage_donnees (bool, optional): {True, False}. Defaults to True.
            predateur_stamina_depart (int, optional): Stamina pour les predateurs au la naissance. Defaults to 10.
            predateur_stamina_gain (int, optional): stamina gagnée par chque predateur apres avoir mangé. Defaults to 100.
            predateur_stamina_enfants (int, optional): stamina necessaire pour un predateur pour enfanter. Defaults to 40.
            predateur_vitesse (int, optional): vitesse de depart des predateurs. Defaults to 9.
            predateur_vue (int, optional): vue de depart des predateurs. Defaults to 30.
            predateur_duree_vie (int, optional): duree de vie des predateurs. Defaults to 10.
            proie_vitesse (int, optional): vitesse de depart des proies. Defaults to 10.
            proie_vue (int, optional): vue de depart des proies. Defaults to 35.
            proie_duree_vie (int, optional): duree de vie des proies. Defaults to 30.
            proie_distance_reprod (int, optional): distance minimale pour qu'une proie naisse. Defaults to 10.
            random_seed (int, float, optional): Permet de set une rendom seed. Defaults to None.
            background (bool, optional): {True, False}. Defaults to True.
            equilibrage_predateurs (bool, optional): {True, False}. Defaults to False.
            predateur_besoin_couple (bool, optional): {True, False}. Defaults to False.
            debug (bool, optional): {True, False}. Defaults to False.

        Raises:
            Exception: Plateau plus grand que la fenetre
        """
        
        self.DEBUG = debug   #affiche des informations complementaires tel que le nombre de clefs et la population calculée differement

        self.LIVE_GRAPHS = live_graphs

        self.BACKGROUND = background

        self.EQUILIBRAGE_PREDATEURS = equilibrage_predateurs

        self.DEPART_NOMBRE_PROIES = depart_nb_proies
        self.DEPART_NOMBRE_PREDATEURS = depart_nb_predateurs

        self.TOURS = tours
        self.HAUTEUR_PLATEAU = hauteur_plateau
        self.LONGUEUR_PLATEAU = hauteur_plateau
        
        
        self.PREDATEUR_STAMINA_DEPART = predateur_stamina_depart
            
        if predateur_duree_vie == None:
            self.PREDATEUR_DUREE_VIE = min(max(20, self.HAUTEUR_PLATEAU // 2), 40)
        else:
            self.PREDATEUR_DUREE_VIE = predateur_duree_vie
        
        self.PREDATEUR_BESOIN_COUPLE = predateur_besoin_couple
            
        self.PREDATEUR_STAMINA_GAIN = predateur_stamina_gain
        self.PREDATEUR_STAMINA_ENFANTS = predateur_stamina_enfants
        
        if predateur_vitesse == None:
            self.PREDATEUR_VITESSE = self.HAUTEUR_PLATEAU // 60
        else:
            self.PREDATEUR_VITESSE = predateur_vitesse
        
        if predateur_vue == None:
            self.PREDATEUR_VUE = self.HAUTEUR_PLATEAU // 2
        else:
            self.PREDATEUR_VUE = predateur_vue
        
        if proie_vitesse == None:
            self.PROIE_VITESSE = self.HAUTEUR_PLATEAU // 60
        else:
            self.PROIE_VITESSE = proie_vitesse
        
        if proie_vue == None:
            self.PROIE_VUE = self.HAUTEUR_PLATEAU // 17
        else:
            self.PROIE_VUE = proie_vue
        
        if proie_duree_vie == None: 
            self.PROIE_DUREE_VIE = self.HAUTEUR_PLATEAU// 20
        else:
            self.PROIE_DUREE_VIE = proie_duree_vie
        
        if proie_distance_reprod == None:   
            self.DISTANCE_REPRODUCTION = self.HAUTEUR_PLATEAU // 60
        else:
            self.DISTANCE_REPRODUCTION = proie_distance_reprod  #espace  vital (pts de vue machine : evite une infinite de creation de proie) (pts de vue interface : clareté)

        self.EPSILON_PROIES_VITESSE = proies_epsilon_vitesse
        self.EPSILON_PROIES_VUE = proies_epsilon_vue

        self.EPSILON_PREDATEURS_VITESSE = predateurs_epsilon_vitesse
        self.EPSILON_PREDATEURS_VUE = predateurs_epsilon_vue

        self.affichage_donnees = affichage_donnees
        
        self.reproduction_proies = True
        self.reproduction_predateurs = True
        
        self.longueur_fenetre = max(self.LONGUEUR_PLATEAU+600, longueur_fenetre)
        self.hauteur_fenetre = max(self.HAUTEUR_PLATEAU, hauteur_fenetre)
        
        self.genetique = max(proies_epsilon_vitesse, proies_epsilon_vue, predateurs_epsilon_vitesse, predateurs_epsilon_vue)
        
        self.affichage_fin = True

        self.nb_tour : int = 1
        
        self.rapport_Txt = min(0.7 * self.longueur_fenetre, 0.7 * self.hauteur_fenetre)
        
        if random_seed == None or type(random_seed) not in [float, int]:
            
            pass
        
        else:
            
            self.random_seed = random_seed

            random.seed(self.random_seed)
            
        
        self.depart(self.longueur_fenetre, self.hauteur_fenetre)
        
        self.ecran_depart()

        self.init_graphique(self.DEPART_NOMBRE_PROIES, self.DEPART_NOMBRE_PREDATEURS)
        
        
        if self.longueur_fenetre - self.LONGUEUR_PLATEAU < 0:
    
            raise Exception(f'Le plateau est plus grand que la fenetre dans laquelle il est situé ({self.longueur_fenetre} < {self.LONGUEUR_PLATEAU})')

        elif self.longueur_fenetre - self.LONGUEUR_PLATEAU >= 500:
            
            if self.hauteur_fenetre >= 50:
                
                self.affichage_donnees = True
                self.affichage_depart = True
                self.affichage_fin = True
                
                if (self.LIVE_GRAPHS) and (self.hauteur_fenetre >= 400):
                    
                    self.affichage_live_graph = True
        
        tot = []
        pro = []
        pre = []
        avg_vit_pred = []
        avg_vit_proi = []
        avg_vue_pred = []
        avg_vue_proi = []

        while self.nb_tour <= self.TOURS:
            
            if (self.population["proies"] <= self.DEPART_NOMBRE_PROIES*0.3):
            
                for k in range(random.randint(int(self.DEPART_NOMBRE_PROIES*0.01), int(self.DEPART_NOMBRE_PROIES*0.2))):
            
                    self.creer_proie()
            
            elif self.EQUILIBRAGE_PREDATEURS and (self.population["predateurs"] <= 0):
            
                #reintroduction dans la reserve par les autorités pour reguler la population
                for k in range(random.randint(int(self.DEPART_NOMBRE_PREDATEURS*0.01), int(self.DEPART_NOMBRE_PREDATEURS*0.2))):
            
                    self.creer_predateur()
            
            self.tour()
            
            tot.append(self.population["total"])
            pro.append(self.population["proies"])
            pre.append(self.population["predateurs"])
            
            tamp_pred_vit = [0, 0]
            tamp_proi_vit = [0, 0]
            tamp_pred_vue = [0, 0]
            tamp_proi_vue = [0, 0]
            
            for id in self.vitesse:
                
                if self.type[id] == 'predateur':
                    
                    tamp_pred_vit[0] += self.vitesse[id]
                    tamp_pred_vit[1] += 1
                    
                    tamp_pred_vue[0] += self.vue[id]
                    tamp_pred_vue[1] += 1                
                
                else:
                    
                    tamp_proi_vit[0] += self.vitesse[id]
                    tamp_proi_vit[1] += 1
                    
                    tamp_proi_vue[0] += self.vue[id]
                    tamp_proi_vue[1] += 1

            if self.population['proies'] > 0:
                avg_vit_proi.append(tamp_proi_vit[0]/tamp_proi_vit[1])
                avg_vue_proi.append(round(tamp_proi_vue[0]/tamp_proi_vue[1], 3))
            else:
                avg_vit_proi.append(0)
                avg_vue_proi.append(0)
            
            if self.population['predateurs'] > 0:
                avg_vit_pred.append(tamp_pred_vit[0]/tamp_pred_vit[1])
                avg_vue_pred.append(round(tamp_pred_vue[0]/tamp_pred_vue[1], 2))
            else:
                avg_vit_pred.append(0)
                avg_vue_pred.append(0)
    
            if len(tot) >= 2:

                self.historique_populations["total"] += tuple(tot)
                self.historique_populations["proies"] += tuple(pro)
                self.historique_populations["predateurs"] += tuple(pre)
                self.historique_populations['avg_vitesse_pred'] += tuple(avg_vit_pred)
                self.historique_populations['avg_vitesse_proi'] += tuple(avg_vit_proi)
                self.historique_populations['avg_vue_pred'] += tuple(avg_vue_pred)
                self.historique_populations['avg_vue_proi'] += tuple(avg_vue_proi)
                
                for v in [tot, pro, pre, avg_vit_pred, avg_vit_proi, avg_vue_pred, avg_vue_proi]:
                    
                    v.clear()
            
            self.nb_tour += 1
        
        self.grande_suppression()
        
        if self.affichage_fin:
            
            self.plot_popultaions()

        self.fin()

########################
##      Execution     ##
########################

if __name__ == '__main__':
    
    sim = Forest_sim()
    
    sim.deroulement(600, 200, 50, 50, True, proie_distance_reprod=3, equilibrage_predateurs=True)
    
    #help(sim)  #fonction help compatible
    #help(sim.deroulement) #fonction help compatible (conseillée pour voir les variables dispinibles)