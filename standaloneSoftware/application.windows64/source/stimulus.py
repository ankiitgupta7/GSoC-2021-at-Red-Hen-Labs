import math
import random
class stimulus(object):
    def __init__(self, img, type, aAge, x, y, maxSpeed, orient, avoidLocations, lastKill, swf, eLevel, eMax):
        self.img = img   # stimulus as image
        self.type = type
        self.aAge = aAge # adult age of predator
        # position of stimulus: (x,y)
        self.x = x
        self.y = y
        self.maxSpeed = maxSpeed    # maxSpeed of predator
        self.orient = orient    # orientation of predator
        self.avoidLocations = avoidLocations # corresponding hideout location
        self.lastKill = lastKill
        self.swf = swf # no. of days it can survive without food
        self.eLevel = eLevel
        self.eMax = eMax

        
    # to display stimulus
    def display(self):
        colorGradient = int(255*self.eLevel/self.eMax)
        strokeWeight(6) 
        if(self.type == "leopard"):
            stroke(0,0,colorGradient)
        elif(self.type == "hawk"):
            stroke(0,colorGradient,0)
        elif(self.type == "python"):
            stroke(colorGradient,0,0)
        rect(self.x-20,self.y-15,40,30)
        image(self.img,self.x-20,self.y-15,40,30)
        strokeWeight(1)

    def location(self):
        return self.x,self.y


    # takes care of vehicle movement
    def move(self, oneHour):
        oneDay = 24*oneHour
        closestAvoidDist, safeDist = getClosestAvoidDist(self)
        hLevel = self.eMax - self.eLevel
        v = self.maxSpeed * hLevel / self.eMax
        vx = v * math.cos(self.orient)
        vy = v * math.sin(self.orient)


        if(closestAvoidDist<=safeDist):  # rebound from refuge area where vervets are safe from this predator
            vx *= -1
            vy *= -1
            self.orient += math.pi

        # predators don't move for 1hr equivalent frames after kill, don't kill for about 300 frames after kill
        if self.lastKill > oneHour:
            self.x = self.x + vx
            self.y = self.y + vy
        else:
            v = 0
        
        # time elapsed after last kill
        self.lastKill += 1

        # energy decay per frame
        edr = self.eMax / (oneDay*self.swf) # energy decay rate (per frame)
        self.eLevel -= (.1*edr*v/self.maxSpeed + edr) # to be tuned later
 
 
       # to make the stimuli rebound from boundaries
        if self.x >= .9*width or self.x <=0 or self.y >= height or self.y <=0:
            self.orient += math.pi/2


def dist(x,y,sx,sy):
    return sqrt((x-sx)**2+(y-sy)**2)

    
def getClosestAvoidDist(self):
    closestDist = width + height    # 'width' and 'height' are processing variables for the same
    avoidL = self.avoidLocations
    for i in range(len(avoidL)):
        avoidX,avoidY = avoidL[i][0], avoidL[i][1]    # acquiring location of ith refuge
        if(dist(avoidX,avoidY,self.x,self.y)<closestDist):
            closestDist = dist(avoidX,avoidY,self.x,self.y)
            safeDist = math.sqrt(avoidL[i][2]**2+avoidL[i][3]**2)

    return closestDist, safeDist/2  # closestDist, safeRadius