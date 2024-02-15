import random
import math
# calculates Euclidean distance between sensor and stimulus
def distance(x,y,sx,sy):
    return sqrt((x-sx)**2+(y-sy)**2)

# i : activation due to i'th stimulus
# index : refers to index of sensor (in case of multiple)
def activation(x,y,sx,sy,behav):
    r = distance(x,y,sx,sy)
    if(behav == "1b" or behav == "3a" or behav == "3b"):
        k=.1
        k1=1
        k2=.00001
        return k*(k1+k2*r*r)
    elif(behav == "1a" or behav == "2a" or behav == "2b"):
        k=30000
        k1=1
        k2=1
        return k/(k1+k2*r*r)

