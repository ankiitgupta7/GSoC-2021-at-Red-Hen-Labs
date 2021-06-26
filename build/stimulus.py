import math
import random
class stimulus(object):
    def __init__(self, img, type, x, y, xspeed, yspeed,hl):
        self.xspeed = xspeed    # horizontal velocity
        self.yspeed = yspeed    # vertical velocity
        # position of stimulus: (x,y)
        self.x = x
        self.y = y
        self.img = img   # stimulus as image
        self.type = type
        self.hl = hl # corresponding hideout location

    # to display stimulus
    def display(self):
        stroke(0)
        image(self.img,self.x-40,self.y-30,40,30)
        #circle(self.x,self.y,800)

    def location(self):
        return self.x,self.y
    # takes care of vehicle movement
    def move(self):
        hx,hy = self.hl
        hd = dist(self.x,self.y,hx,hy)  # distance from hideout
        
       # to make the stimuli rebound from boundaries
        if self.x > .9*width or self.x <=0:
            self.xspeed *= -1
        if self.y > height or self.y <=0:
            self.yspeed *= -1
        if(hd<85):
            self.xspeed *= -1
            self.yspeed *= -1

        self.x = self.x + self.xspeed
        self.y = self.y + self.yspeed
 



def dist(x,y,sx,sy):
    return sqrt((x-sx)**2+(y-sy)**2)