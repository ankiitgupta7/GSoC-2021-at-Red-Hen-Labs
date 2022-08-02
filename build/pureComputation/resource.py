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

    def regrow(self, oneDay, growthRate):
        # assuming their growthRate% growth in 1 day
        x,y,rLevel = self.patchPoints # rLevel: resource level
        rMax = 255*self.resourceRichness    # maximum possible value of resource level - rLevel
        for j in range(len(rLevel)):
            if(rLevel[j]<rMax):
                growthPercentInOneFrame = growthRate/oneDay
                rLevel[j] += rMax*growthPercentInOneFrame/100 # net growth of resource levels per frame 
                if(rLevel[j]>rMax):
                    rLevel[j] = rMax
        return x,y,rLevel
