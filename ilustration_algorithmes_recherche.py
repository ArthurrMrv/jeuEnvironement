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

    
def reccur_disque( pos, max_dist = None, dist = 1, idx = 1) -> tuple:
    
    global g
    
    couleur = ['blue', "green", "yellow", "red", "pink"][idx%5]
        
    if dist > max_dist:
        
        return None
    
    else:
        
        for v in range(dist+1):
            
            for p in ((pos[0] + (dist-v), pos[1] + v), (pos[0] - (dist-v), pos[1] - v), (pos[0] + (dist-v), pos[1] - v), (pos[0] - (dist-v), pos[1] + v)):
            #for p in ((pos[0] + dist, pos[1] + v), (pos[0] - dist, pos[1] - v), (pos[0] + dist, pos[1] - v), (pos[0] - dist, pos[1] + v), (pos[0] + v, pos[1] + dist), (pos[0] - v, pos[1] - dist), (pos[0] + v, pos[1] - dist), (pos[0] - v, pos[1] + dist)):
            #for p in ((pos[0] + v, pos[1] + v), (pos[0] - v, pos[1] - v), (pos[0] + v, pos[1] - v), (pos[0] - v, pos[1] + v)):
                
                time.sleep(0.02)
                g.actualiser()
                g.dessinerCercle(p[0], p[1], 1, couleur)
    
    return reccur_disque(pos, max_dist, dist+1, idx + 1)
