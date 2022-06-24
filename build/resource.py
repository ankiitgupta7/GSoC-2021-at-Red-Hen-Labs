import math
import random
class resource(object):
    def __init__(self, patchX, patchY, patchPoints, tempX, tempY):
        self.patchX = patchX
        self.patchY = patchY
        self.patchPoints = patchPoints
        self.tempX = tempX
        self.tempY = tempY

    # to display patches
    def display(self):
        fill(0,189,135)
        #circle(self.patchX,self.patchY,5)
        noFill()
        stroke(0,189,135)
        rect(self.patchX - self.tempX/2 , self.patchY - self.tempY/2, self.tempX, self.tempY)
        x,y,rLevel = self.patchPoints # rLevel: resource level

        noStroke()
        for j in range(len(x)):
            fill(rLevel[j],rLevel[j],0)
            circle(x[j],y[j],5)


    def regrow(self):
        x,y,rLevel = self.patchPoints # rLevel: resource level
        for j in range(len(x)):
            if(rLevel[j]<255):
                rLevel[j] += .5
                if(rLevel[j]>255):
                    rLevel[j] = 255
