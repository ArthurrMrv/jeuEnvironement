######################
##      IMPORTS     ##
######################

import Forest_sim as Fs
import tkiteasy.tkiteasy as tki

########################
##      Execution     ##
########################

if __name__ == '__main__':

    sim = Fs.Forest_sim()
    
    #sim.deroulement(600, 500, 50, 50, random_seed=72, live_graphs=True, predateur_vue=140, equilibrage_predateurs=True)
    sim.deroulement(600, 500, 50, 50, random_seed=72, live_graphs=True, proie_distance_reprod=5, predateur_vue=70, predateur_duree_vie=20, equilibrage_predateurs=True)
    #sim.deroulement(800, 500, 50, 50, random_seed=42, proie_distance_reprod=3, live_graphs=False)
    #sim.deroulement(400, 500, 50, 50, proie_distance_reprod=5, proies_epsilon_vitesse=0.2, predateurs_epsilon_vue=0.2, predateurs_epsilon_vitesse=0.1, random_seed=31, live_graphs=False)
    
    #help(sim)  #fonction help compatible
    #help(sim.deroulement) #fonction help compatible (conseillée pour voir les variables dispinibles)