import random
import math
import vehicle_tools  as tools
import stimulus
import resource

alarm = 0

# repository of alarm call details

alarms = [] 
_alarms = [] 

class vehicle(object):
    def __init__(self, xpos, ypos, maxSpeed, aAge, z, stim, alpha, movement, recentlySeenPredator, threat, eLevel, eMax, fLevel, fMax, rfd, swf, patch):
        # co-ordinates of the agent
        self.xpos = xpos
        self.ypos = ypos
        self.maxSpeed = maxSpeed    # maximum speed of vervet
        self.aAge = aAge # adult age of vervet
        self.z = z # vehicle size scale
        self.stim = stim    # agent having access to all the stimuli present in the environment
        self.alpha = alpha # vehicle's orienation angle wrt +ve x-axis
        self.movement = movement # agent's movement rule
        self.recentlySeenPredator = recentlySeenPredator    # information about having recently seen predator
        self.threat = threat    # threat awareness about predators
        self.eLevel = eLevel # energy level of the agent
        self.eMax = eMax # max energy level of the agent
        self.fLevel = fLevel # fear level of the agent
        self.fMax = fMax # max fear level of the agent
        self.rfd = rfd # ready for death parameter after being predated
        self.swf = swf # no. of days it can survive without food
        self.patch = patch  # details about each resource patch in the environment



    def sensorLocation(self):
        ex1 = self.xpos + self.z * math.cos((self.alpha - math.pi/6) - math.pi/6)   # first eye's x-coordinates
        ey1 = self.ypos + self.z * math.sin((self.alpha - math.pi/6) - math.pi/6)   # first eye's y-coordinates
        ex2 = self.xpos + self.z * math.cos((self.alpha - math.pi/6) + math.pi/2)
        ey2 = self.ypos + self.z * math.sin((self.alpha - math.pi/6) + math.pi/2)
        return ex1, ey1, ex2, ey2

    def move(self,idNum,r,fov,index,refuge,nAgents,alarmPotency,first2See,frameNumber,scanFreq,oneMeter,oneMinute,width,height):
        global v, alarm, alarms, _alarms
        v, alarm = 0, 0
        self.movement = 1 # default is to forage
        #setting up hunger level
        hLevel = self.eMax - self.eLevel

        # setting up energyDecayRate
        oneDay  = 24*60*oneMinute
        energyDecayRate = self.eMax / (oneDay*self.swf) # energy decay rate (per frame)

        # return if there's no predators
        if len(self.stim)<1:
            if self.eLevel < .5 * self.eMax:
                v, self.alpha, self.eLevel = moveToForage(self, self.xpos, self.ypos, self.patch, self.eLevel, oneMinute, width, height)
            updateEnergyAndPosition(self, v, oneMinute, energyDecayRate)
            return

        # checking whether the agent is inside a refuge
        checkhideout = isInsideHO(self, refuge)

        # checking any alarm call in the last frame
        if(len(_alarms)>0 and alarmPotency>0):
            alarm = checkAlarmCall(self.xpos, self.ypos, _alarms, r, width, height)

        # letting the closest predator to vervet attempt to kill
        closest, closestDist = closestPredator(self, width, height)
    
        # getting details of closest predator and setting up vervet awareness accordingly
        type = self.stim[closest].type    # type of predator
        x,y = self.stim[closest].location()    # acquiring location of ith stimulus
        # to be tuned
        if(type == "leopard"):
            awareRadius = 2.5*r
        elif(type == "hawk"):
            awareRadius = 2*r
        elif(type == "python"):
            awareRadius = r

        # setting auditory awareness thresold of vervets to hear alarm calls
        auditoryAware = 3*r

        # check if predator is very close (<10 meters) to agent
        # check if there was no recent kill by this predator - don't kills for a while unless less on eLevel
        # check if predator eLevel is not more than 50% of self.eMax    # to be tuned - eat only when < 50% of eMax
        # probability of predation success in this attempt = 80%

        predationDist = 10*oneMeter # to be tuned
        if(closestDist<10*oneMeter and self.stim[closest].eLevel<.5*self.stim[closest].eMax and random.uniform(0,1)>.2):    # conditions for predation
            # the agent is ready for death with a 80% probability!
            if(self.stim[closest].type == "leopard"):
                self.rfd = [1,1]
            elif(self.stim[closest].type == "hawk"):
                self.rfd = [1,2]    # 1 refers to death cnf, while 2 refers to death by 2nd predator, i.e., hawk
            elif(self.stim[closest].type == "python"):
                self.rfd = [1,3]

            self.stim[closest].lastKill = 0

            self.stim[closest].eLevel += .5*self.stim[closest].eMax # 10% of eMax   - to be tuned - get eLevel of prey been preyed

            if self.stim[closest].eLevel >  self.stim[closest].eMax:
                self.stim[closest].eLevel  =  self.stim[closest].eMax

        # if vervet has recently seen a predator
        if(self.fLevel>hLevel and self.recentlySeenPredator > 0 and checkhideout != self.threat):
            self.movement = 3
            self.threat = self.recentlySeenPredator

        # alarm call was perceived in the last frame
        elif(alarm>0 and checkhideout != alarm):      
            self.threat = alarm    # update fear level and corresponding alarm call
            self.fLevel = .6*self.fMax   # fear level due to alarms is less than actual sight
            if(checkhideout!=alarm and hLevel<self.fLevel):
                self.movement = 2
                if(alarmPotency == 1):  # just to assign dummy alarm type
                    v, self.alpha, self.threat = moveToNearestRefuge(self, refuge, width, height)

        # checking residual alarm in the vervets
        elif(self.fLevel>hLevel and self.threat>0 and checkhideout != self.threat):
            self.movement = 2

        # scanning frequency is more while having higher order movements - 4 & 9 times when moving to refuge & avoiding predator resp. - to be tuned 
        scanFreq = int(scanFreq/self.movement**2)

                
        # visual periodic scan of environment 
        if(frameNumber % scanFreq == 0):   # scanning begins
            self.eLevel -= 2*energyDecayRate   # cost of scanning - double than usual energyDecayRate - to be tuned

            # to check on whether stimulus lies in the Field of View (FoV) and vervet is outside its corresponding refuge
            # i.e. to check if agent can visually spot the stimulus [visual scan]
            if(isInsideFoV(self.xpos,self.ypos,awareRadius,self.alpha*180/math.pi,fov,x,y)):
                # getting alarmed about a predator (if agent is not in refuge) as it the vervet sees the predator
                if(type == "leopard"):
                    if(checkhideout != 1):
                        alarm = 1
                        self.fLevel = .9*self.fMax  # to be tuned
                        self.threat = 1

                elif(type == "hawk"):
                    if(checkhideout != 2):
                        alarm = 2
                        self.fLevel = .8*self.fMax
                        self.threat = 2

                elif(type == "python"):
                    if(checkhideout != 3):
                        alarm = 3
                        self.fLevel = .7*self.fMax
                        self.threat = 3

                self.recentlySeenPredator = self.threat

                if(self.fLevel>hLevel):
                    self.movement = 3 # move in direction opposite to line of sight of predator
                

                # storing and representing vervet alarm call data as it spots a predator, 
                # only if it's the first one to see the predator. And closest one sees if it can
                if(first2See[closest]== 0 and alarm>0 and alarmPotency>0):
                    temp = self.xpos, self.ypos, alarm  
                    alarms.append(temp)   # storing alarm call data to be used in next frame
                    first2See[closest] = 1    # as this vervet is first to see the predator


        # Acting upon movement information
        if(self.movement == 1 and checkhideout != self.threat and self.eLevel < .5 * self.eMax):    # forage only if on less than half eLevel - to be tuned
            v, self.alpha, self.eLevel = moveToForage(self, self.xpos, self.ypos, self.patch, self.eLevel, oneMinute, width, height)
        elif(self.movement == 2 and alarmPotency == 1):
            v, self.alpha, self.threat = moveToNearestRefuge(self, refuge, width, height)
        elif(self.movement == 2 and alarmPotency == 2):
            v, self.alpha = moveToRefuge(self, refuge, self.threat, width, height)
        elif(self.movement == 3):
            v, self.alpha = moveToAvoidBV(self, closest)


        # disappearance of fear level
        if(self.fLevel < self.fMax * .01):
            self.fLevel = 0
            self.recentlySeenPredator = 0
            self.threat = 0
        else:
            # fear level keeps decreasing by fearDecayRate levels per frame after being recently alarmed or seeing predator
            fearDecayRate = self.fMax/(60*oneMinute)  # to be tuned - current they remain in fear for 60 minutes
            self.fLevel -= (.1*fearDecayRate*v + fearDecayRate) # to be tuned later


        # update coordinate based on velocity, orientation
        updateEnergyAndPosition(self, v, oneMinute, energyDecayRate)

        if(index == nAgents-1): # end of a particular frame
            for j in range(0,len(self.stim)):
                first2See[j]=0
            # use alarm lists of this frame for next frame
            _alarms = alarms
            alarms = []




def updateEnergyAndPosition(self, v, oneMinute, energyDecayRate):
    # energy decay in agents
    # energy level decreases continuously after each frame even if agent is stagnant or decreases wrt agent speed
    self.eLevel -= (.1*energyDecayRate*v/self.maxSpeed + energyDecayRate) # to be tuned later
    vx = v * math.cos(self.alpha)
    vy = v * math.sin(self.alpha)

    # updating the new position as vehicle moves
    self.xpos = self.xpos + vx
    self.ypos = self.ypos + vy

# returns the index of closest predator to an agent
def closestPredator(self, width, height):
    m = len(self.stim)
    closest = 0
    closestDist = width + height
    for i in range(m):
        x,y = self.stim[i].location()    # acquiring location of ith stimulus
        if(dist(x,y,self.xpos,self.ypos)<closestDist):
            closestDist = dist(x,y,self.xpos,self.ypos)
            closest = i
    return closest, closestDist    

    
def threatRefugeInfo(self, refuge):
    refugeInfo = list()
    for i in range(len(refuge)):
        refugeCode = refuge[i][2]
        refugeSize = refuge[i][3], refuge[i][4]
        if(self.threat == (refugeCode+1)):  # threat code is 1,2,3 while refugeCode is 0,1,2
            refugeInfo.append([refuge[i][0],refuge[i][1],refugeCode,refuge[i][3],refuge[i][4]])  # refugeX, refugeY, refugeCode, refugeSizeX, refugeSizeY

    return refugeInfo

def getClosestRefuge(self, refugeLocations, width, height):
    closest = 0
    closestDist = width + height
    for i in range(len(refugeLocations)):
        x,y = refugeLocations[i][0], refugeLocations[i][1]    # acquiring location of ith refuge
        if(dist(x,y,self.xpos,self.ypos)<closestDist):
            closestDist = dist(x,y,self.xpos,self.ypos)
            closestRefuge = x,y
            refugeCode = refugeLocations[i][2]
            refugeSize = refugeLocations[i][3], refugeLocations[i][4]
    return refugeCode, closestRefuge, closestDist, refugeSize


# a funtion to orient towards refuge when the agent is alarmed
def moveToRefuge(self, refuge, alarm, width, height):

    relevantRefuges = threatRefugeInfo(self, refuge)
    refugeCode, closestRefuge, closestRefugeDist, refugeSize = getClosestRefuge(self, relevantRefuges, width, height)
    closestRefugeX, closestRefugeY = closestRefuge
    orienation = orientAlpha(closestRefugeX, closestRefugeY,self.xpos, self.ypos)

    if closestRefugeDist < refugeSize[0]/6 or closestRefugeDist < refugeSize[1]/6:
        velocity = 0
    else:
        velocity = self.maxSpeed * self.fLevel / self.fMax # updates velocity in case of alarm


    return velocity, orienation

def moveToNearestRefuge(self, refuge, width, height):

    refugeCode, closestRefuge, closestRefugeDist, refugeSize = getClosestRefuge(self, refuge, width, height)
    closestRefugeX, closestRefugeY = closestRefuge
    orienation = orientAlpha(closestRefugeX, closestRefugeY,self.xpos, self.ypos)

    if closestRefugeDist < refugeSize[0]/6 or closestRefugeDist < refugeSize[1]/6:
        velocity = 0
    else:
        velocity = self.maxSpeed * self.fLevel / self.fMax # updates velocity in case of alarm

    
    return velocity, orienation, refugeCode+1


def moveToAvoid(self,closest): # to guide vervets
    x,y = self.stim[closest].location()
    self.alpha = math.pi + orientAlpha(x,y,self.xpos,self.ypos)
    vel = self.maxSpeed * self.fLevel / self.fMax
    return vel, self.alpha



# a function to respond to predator
def moveToAvoidBV(self,closest):
    x,y = self.stim[closest].location()    # acquiring location of ith stimulus

    # acquiring instantaneous co-ordinates of sensors
    s1x,s1y,s2x,s2y = self.sensorLocation()
    type = self.stim[closest].type    # type of predator

    # setting behavioural wiring based on type
    if(type == "leopard" or type == "hawk" or type == "python"):
        behav = "2a"

    # decide on wiring weights based on vehicle type
    if(behav == "1a" or behav == "1b"):
        w1,w2,w3,w4 = 1,1,1,1
    elif(behav == "2a" or behav == "3a"):
        w1,w2,w3,w4 = 1,1,0,0           # parallel wiring
    elif(behav == "2b" or behav == "3b"):
        w1,w2,w3,w4 = 0,0,1,1           # crossed wiring
    else:
        w1,w2,w3,w4 = 0,0,0,0

    # in case we want agent to be affected by multiple stimuli, we'll have a1 + = ...
    # but as here the agent decides to react to the nearest stimuli, we don't have cumulative activation
    a1 = tools.activation(x,y,s1x,s1y,behav)  # activation in 1st sensor due to ith stimulus
    a2 = tools.activation(x,y,s2x,s2y,behav)  # activation in 2nd sensor due to ith stimulus
    v1 = w1*a1 + w4*a2  # velocity activation in 1st wheel
    v2 = w3*a1 + w2*a2  # velocity activation in 2nd wheel
    
    vel = self.maxSpeed * self.fLevel / self.fMax 

    v = (v1 + v2) / 2 # net velocity of vehicle

    # capping max speed depending on eLevel 
    if v>vel:
        v = vel

    self.alpha += (v1 - v2) * .08 # the rotating factor = 0.08

    return v, self.alpha


def checkAlarmCall(x,y,alarms,r,width,height):
    alarmIndex = 0
    alarmDist = width + height
    for i in range(len(alarms)):
        alarmX,alarmY,alarm = alarms[i]
        if(dist(x,y,alarmX,alarmY)<alarmDist):
            alarmDist = dist(x,y,alarmX,alarmY)
            alarmIndex = i

    alarmX,alarmY,alarm = alarms[alarmIndex]
    alarmDist = dist(x,y,alarmX,alarmY)
    if(alarmDist < 3*r):
        return alarm
    return 0


def moveToForage(self,x,y,patch,eLevel, oneMinute, width, height):
    oneHour = 60 * oneMinute
    patchDist = width + height  # setting this as max value
    nearestPatch = 0 # dummy
    for i in range(0,len(patch)):
        totalR, maxR = resourceData(patch[i], patch[i].resourceRichness)
        # assign this patch only if it is atleast at 10% of it's maximum resource level - to be tuned
        if(patchDist>dist(patch[i].patchX,patch[i].patchY,x,y) and totalR/maxR>.1): 
            patchDist = dist(patch[i].patchX,patch[i].patchY,x,y)
            nearestPatch = i
    
    alpha = orientAlpha(patch[nearestPatch].patchX,patch[nearestPatch].patchY,x,y)
    totalR, maxR = resourceData(patch[nearestPatch], patch[nearestPatch].resourceRichness)

    if(patchDist > patch[nearestPatch].tempX/3):
        hLevel = self.eMax - eLevel
        vel = self.maxSpeed * hLevel / self.eMax
    else:
        vel = 0
        if(eLevel<.9*self.eMax):    # deprecated
            consumptionFactor = .2 / oneHour  # agent consumption per frame with 20% consumption of their eMax per hour   # to be tuned
            consumptionPerFrame = self.eMax * consumptionFactor
            eLevel += consumptionPerFrame
            nPoints = int(maxR/(255*patch[nearestPatch].resourceRichness))   # number of resource points in the patch
            for i in range(nPoints):   
                # rLevel of each patchPoint equally decreases by (total consumption by agent/total patchPoints) per frame
                patch[nearestPatch].patchPoints[2][i] -= consumptionPerFrame/nPoints    

    if(eLevel > self.eMax):
        eLevel = self.eMax

    return vel, alpha, eLevel


def resourceData(ithPatch, resourceRichness):
    d1,d2,rLevel = ithPatch.patchPoints
    maxR = len(rLevel) * 255 * resourceRichness
    totalR = 0
    for i in range(len(rLevel)):
        totalR += rLevel[i]
    return totalR, maxR



def isInsideHO(self, refuge):
    for i in range(len(refuge)):
        cx, cy = refuge[i][0], refuge[i][1] # centre coordinates of refuge
        tempCode = refuge[i][2]
        w, h = refuge[i][3], refuge[i][4]   # width and height of refuge

        xRange = [cx-w/2,cx+w/2]
        yRange = [cy-h/2,cy+h/2]
        if self.xpos > xRange[0] and self.xpos < xRange[1] and self.ypos > yRange[0] and self.xpos < yRange[1] :
            return tempCode+1 # because threat code is 1,2,3 while refugeCode is 0,1,2

    return -1


def orientAlpha(x0,y0,x,y): # returns alpha at x,y oriented towards x0,y0
        h = y0-y
        b = x0-x
        if(h>0 and b>0):
            return math.atan(h/b)
        if(b<0):
            return math.atan(h/b) + math.pi
        if(h<0 and b>0):
            return math.atan(h/b) + 2*math.pi

def isInsideFoV(x0,y0,r,alpha,theta,x,y):
    # x0,y0: point of view
    # x,y: point to be checked for being inside FoV
    # alpha: agent orientation
    # theta: scope angle of view
    # r: distance that agent can see
    la = math.pi*(alpha+theta/2)/180 # anglular co-ordinate of left extreme FoV
    ra = math.pi*(alpha-theta/2)/180 # anglular co-ordinate of right extreme FoV
    # co-ordinates of extreme left and right points of FoV
    xr  = x0 + r*math.cos(la)
    yr  = y0 + r*math.sin(la)
    xl  = x0 + r*math.cos(ra)
    yl  = y0 + r*math.sin(ra)

    # criteria to verify if a point lies within a sector of a circle
    # check this link for details: https://stackoverflow.com/questions/13652518/efficiently-find-points-inside-a-circle-sector#:~:text=For%20a%20point%20to%20be,circle%20than%20the%20sector's%20radius.
    l_check = (yl-y0)*(x-x0) + (x0-xl)*(y-y0)
    r_check = (yr-y0)*(x-x0) + (x0-xr)*(y-y0)

    proximity = dist(x0,y0,x,y) # distance between the agent and stimulus

    if(l_check<la and r_check>ra and proximity<r and theta<180):
        return 1
    if(l_check<la and r_check>ra and proximity<r and theta == 180):
        return 1
    elif(l_check<la and r_check<ra and proximity<r and theta>180):
        return 1
    elif(l_check>la and r_check>ra and proximity<r and theta>180):
        return 1
    elif(l_check<la and r_check>ra and proximity<r and theta>180):
        return 1

    else:            
        return 0

def dist(x,y,sx,sy):
    return math.sqrt((x-sx)**2+(y-sy)**2)

