import math
import random
class stimulus(object):
    def __init__(self, img, type, x, y, xspeed, yspeed, hl, nextAlarm, lastKill, eLevel):
        self.xspeed = xspeed    # horizontal velocity
        self.yspeed = yspeed    # vertical velocity
        # position of stimulus: (x,y)
        self.x = x
        self.y = y
        self.img = img   # stimulus as image
        self.type = type
        self.hl = hl # corresponding hideout location
        self.nextAlarm = nextAlarm # gives information about no. of frames after which an alarm is given for this predator if it remains visible
        self.lastKill = lastKill
        self.eLevel = eLevel

        
    # to display stimulus
    def display(self):
        colorGradient = int(255*self.eLevel/10000)
        strokeWeight(6) 
        if(self.type == "leopard"):
            stroke(0,0,colorGradient)
        elif(self.type == "hawk"):
            stroke(0,colorGradient,0)
        elif(self.type == "python"):
            stroke(colorGradient,0,0)
        rect(self.x-40,self.y-30,40,30)
        image(self.img,self.x-40,self.y-30,40,30)
        strokeWeight(1)
    def location(self):
        return self.x,self.y
    # takes care of vehicle movement
    def move(self):
        hx,hy = self.hl
        hd = dist(self.x,self.y,hx,hy)  # distance from hideout
        v = math.sqrt(self.xspeed**2+self.yspeed**2)
        
        # to update eLevel in case of successfull kill
        if(self.lastKill == 5): # energy refill after 5 frames of kill
            self.eLevel += 1000

       # to make the stimuli rebound from boundaries
        if self.x > .9*width or self.x <=0:
            self.xspeed *= -1
        if self.y > height or self.y <=0:
            self.yspeed *= -1
        if(hd<95):  # rebound from refuge area where vervets are safe from this predator
            self.xspeed *= -1
            self.yspeed *= -1
        # predators don't move for 200 frames after kill, don't kill for about 300 frames after kill
        if self.lastKill > 200:
            self.x = self.x + self.xspeed
            self.y = self.y + self.yspeed
            v = 0
        
        # time elapsed after last kill
        self.lastKill += 1

        # energy decay per frame
        if(v==0):
            self.eLevel -= .0005 * self.eLevel
        else:
            self.eLevel -= (.05*v + .0005 * self.eLevel) # to be tuned later
 



def dist(x,y,sx,sy):
    return sqrt((x-sx)**2+(y-sy)**2)