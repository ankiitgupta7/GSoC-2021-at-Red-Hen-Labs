import math
import random
class resource(object):
    def __init__(self, patchX, patchY, patchPoints, tempX, tempY, resourceRichness):
        self.patchX = patchX
        self.patchY = patchY
        self.patchPoints = patchPoints
        self.tempX = tempX
        self.tempY = tempY
        self.resourceRichness = resourceRichness

    # to display patches
    def display(self):
        fill(0,189,135)
        #circle(self.patchX,self.patchY,5)
        noFill()
        stroke(0,189,135)
      #  rect(self.patchX - self.tempX/2 , self.patchY - self.tempY/2, self.tempX, self.tempY)
        x,y,rLevel = self.patchPoints # rLevel: resource level

        noStroke()
        for j in range(len(x)):
            colorGradient = rLevel[j]/self.resourceRichness
            fill(colorGradient,colorGradient,0)
            circle(x[j],y[j],5)


    def regrow(self, oneDay, growthRate):
        # assuming their growthRate% growth in 1 day
        x,y,rLevel = self.patchPoints # rLevel: resource level
        rMax = 255*self.resourceRichness    # maximum possible value of resource level - rLevel
        for j in range(len(rLevel)):
            if(rLevel[j]<rMax):
                growthPercentInOneFrame = growthRate / 60  # to be tuned - now it is 
                rLevel[j] += rMax*growthPercentInOneFrame/100 # net growth of resource levels per frame 
                if(rLevel[j]>rMax):
                    rLevel[j] = rMax
        return x,y,rLevel
