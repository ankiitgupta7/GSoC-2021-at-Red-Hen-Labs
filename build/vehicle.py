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
    def __init__(self, xpos, ypos, aAge, z, stim, alpha, movement, recentlySeenPredator, threat, eLevel, fLevel, rfd, patch):
        # co-ordinates of the agent
        self.xpos = xpos
        self.ypos = ypos
        self.aAge = aAge # adult age of vervet
        self.z = z # vehicle size scale
        self.stim = stim    # agent having access to all the stimuli present in the environment
        self.alpha = alpha # vehicle's orienation angle wrt +ve x-axis
        self.movement = movement # agent's movement rule
        self.recentlySeenPredator = recentlySeenPredator    # information about having recently seen predator
        self.threat = threat    # threat awareness about predators
        self.eLevel = eLevel # energy level of the agent
        self.fLevel = fLevel # fear level of the agent
        self.rfd = rfd # ready for death parameter after being predated
        self.patch = patch  # details about each resource patch in the environment

    def display(self, idNum):
        self.displayMonkey(idNum)

        noStroke()
        fill(0)



    def displayMonkey(self, idNum):  
        sc = self.z    # calibrating scale
        dispAngle = self.alpha - math.pi/6

        c_outline = color(int(255*(10000-self.aAge)/10000))


        # draw outline
        stroke(c_outline)
        strokeWeight(sc/3)
        noFill()
        circle(self.xpos + sc*math.cos(dispAngle - math.pi/6), self.ypos + sc * math.sin(dispAngle - math.pi/6), 2*sc)    #eye1cover
        circle(self.xpos + sc*math.cos(dispAngle + math.pi/2), self.ypos + sc * math.sin(dispAngle + math.pi/2), 2*sc)    #mouthcover
        circle(self.xpos + sc*math.cos(dispAngle + 7*math.pi/6), self.ypos + sc * math.sin(dispAngle + 7*math.pi/6), 2*sc)    #eye2cover
        
        circle(self.xpos + 2.1 * sc * math.cos(dispAngle - math.pi/6), self.ypos + 2.1 * sc * math.sin(dispAngle - math.pi/6), sc)  #ear1
        circle(self.xpos + 2.1 * sc * math.cos(dispAngle + math.pi/2), self.ypos + 2.1 * sc * math.sin(dispAngle + math.pi/2), sc)  #ear2

        # fill outline
        noStroke()

        colorGradient = 255*self.eLevel/1000          
        if(colorGradient > 255):
            colorGradient = 255   
        c = color(int(colorGradient)) 

        fill(c) 

        dispAngle = self.alpha - math.pi/6
        circle(self.xpos + sc*math.cos(dispAngle - math.pi/6), self.ypos + sc * math.sin(dispAngle - math.pi/6), 2*sc)    #eye1cover
        circle(self.xpos + sc*math.cos(dispAngle + math.pi/2), self.ypos + sc * math.sin(dispAngle + math.pi/2), 2*sc)    #mouthcover
        circle(self.xpos + sc*math.cos(dispAngle + 7*math.pi/6), self.ypos + sc * math.sin(dispAngle + 7*math.pi/6), 2*sc)    #eye2cover
        
        strokeWeight(1)
        stroke(0)
        

        # mouth
        triangle(self.xpos + 0.5 * sc * math.cos(dispAngle + 11*math.pi/12), self.ypos + 0.5 * sc * math.sin(dispAngle + 11*math.pi/12), self.xpos + 0.5 * sc * math.cos(dispAngle + 17 * math.pi / 12), self.ypos + 0.5 * sc * math.sin(dispAngle + 17 * math.pi / 12), self.xpos + 1.1 * sc * math.cos(dispAngle + 7*math.pi/6), self.ypos + 1.1 * sc * math.sin(dispAngle + 7*math.pi/6))
        
        if self.movement == 3:
            colorGradient = 255*self.fLevel/1000
            if(self.threat==1):
                c_eyes = color(0,0,int(colorGradient))
            elif(self.threat==2):
                c_eyes = color(0,int(colorGradient),0)
            elif(self.threat==3):
                c_eyes = color(int(colorGradient),0,0)   
            else:   # case where there's no threat but the vervet is still avoiding
                c_eyes = c 

            fill(c_eyes)
            noStroke()
            circle(self.xpos + sc*math.cos(dispAngle - math.pi/6), self.ypos + sc * math.sin(dispAngle - math.pi/6), 3*sc/4)    #eye1
            circle(self.xpos + sc*math.cos(dispAngle + math.pi/2), self.ypos + sc * math.sin(dispAngle + math.pi/2), 3*sc/4)    #eye2


        circle(self.xpos + sc*math.cos(dispAngle - math.pi/6), self.ypos + sc * math.sin(dispAngle - math.pi/6), sc/4)    #eye1
        circle(self.xpos + sc*math.cos(dispAngle + math.pi/2), self.ypos + sc * math.sin(dispAngle + math.pi/2), sc/4)    #eye2

        noStroke()
        fill(c)
        
        if self.movement == 2:        
            colorGradient = 255*self.fLevel/1000
            if(self.threat==1):
                c = color(0,0,int(colorGradient))
            elif(self.threat==2):
                c = color(0,int(colorGradient),0)
            elif(self.threat==3):
                c = color(int(colorGradient),0,0)       
            fill(c)

        circle(self.xpos + 2.1 * sc * math.cos(dispAngle - math.pi/6), self.ypos + 2.1 * sc * math.sin(dispAngle - math.pi/6), sc)  #ear1
        circle(self.xpos + 2.1 * sc * math.cos(dispAngle + math.pi/2), self.ypos + 2.1 * sc * math.sin(dispAngle + math.pi/2), sc)  #ear2


    def sensorLocation(self):
        ex1 = self.xpos + self.z * math.cos((self.alpha - math.pi/6) - math.pi/6)   # first eye's x-coordinates
        ey1 = self.ypos + self.z * math.sin((self.alpha - math.pi/6) - math.pi/6)   # first eye's y-coordinates
        ex2 = self.xpos + self.z * math.cos((self.alpha - math.pi/6) + math.pi/2)
        ey2 = self.ypos + self.z * math.sin((self.alpha - math.pi/6) + math.pi/2)
        return ex1, ey1, ex2, ey2


    def move(self,idNum,r,fov,index,refuge,nAgents,alarmPotency,first2See,frameNumber,scanFreq,showSim):
        global v, alarm, alarms, _alarms
        v, alarm = 0, 0
        self.movement = 1 # default is to forage
        #setting up hunger level
        hLevel = 1000 - self.eLevel

        # return if there's no predators
        if len(self.stim)<1:
            v, self.alpha, self.eLevel = moveToForage(self.xpos, self.ypos, self.patch, self.eLevel)
            updatePosition(self, v)
            return

        # checking whether the agent is inside a refuge
        checkhideout = isInsideHO(self, refuge)

        # checking any alarm call in the last frame
        if(len(_alarms)>0 and alarmPotency>0):
            alarm = checkAlarmCall(self.xpos, self.ypos, _alarms, r)

        # letting the closest predator to vervet attempt to kill
        closest, closestDist = closestPredator(self)
    
        # getting details of closest predator and setting up vervet awareness accordingly
        type = self.stim[closest].type    # type of predator
        x,y = self.stim[closest].location()    # acquiring location of ith stimulus
        if(type == "leopard"):
            awareRadius = 2.5*r
        elif(type == "hawk"):
            awareRadius = 2*r
        elif(type == "python"):
            awareRadius = r

        # setting auditory awareness thresold of vervets to hear alarm calls
        auditoryAware = 3*r

        # check if predator is very close to agent
        # check if there was no recent kill by this predator - don't kills for a while unless less on eLevel
        # check if predator eLevel is not more than 9000
        # probability of predation success in this attempt = 80%
        if(closestDist<20 and self.stim[closest].lastKill>abs(300 - int(100000/self.stim[closest].eLevel)) and self.stim[closest].eLevel<9000 and random.uniform(0,1)>.2):    # conditions for predation
            # the agent is ready for death with a 80% probability!
            if(self.stim[closest].type == "leopard"):
                self.rfd = [1,1]
            elif(self.stim[closest].type == "hawk"):
                self.rfd = [1,2]    # 1 refers to death cnf, while 2 refers to death by 2nd predator, i.e., hawk
            elif(self.stim[closest].type == "python"):
                self.rfd = [1,3]

            self.stim[closest].lastKill = 0


        # if vervet has recently seen a predator
        if(self.fLevel>hLevel and self.recentlySeenPredator > 0 and checkhideout != self.threat):
            self.movement = 3
            self.threat = self.recentlySeenPredator

        # alarm call was perceived in the last frame
        elif(alarm>0 and checkhideout != alarm):      
            self.threat = alarm    # update fear level and corresponding alarm call
            self.fLevel = 600   # fear level due to alarms is less than actual sight
            if(checkhideout!=alarm and hLevel<self.fLevel):
                self.movement = 2
                if(alarmPotency == 1):  # just to assign dummy alarm type
                    v, self.alpha, self.threat = moveToNearestRefuge(self, refuge)

        # checking residual alarm in the vervets
        elif(self.fLevel>hLevel and self.threat>0 and checkhideout != self.threat):
            self.movement = 2


        scanFreq = int(scanFreq/self.movement**2)

                
        # visual periodic scan of environment 
        if(frameNumber % scanFreq == 0):   # scanning begins
            self.eLevel -= 20   # cost of scanning
                    
            # check if there are more than one predator
            # check if fear level is more than hunger level
            # check if there was no recent kill by this predator
            if(self.stim[closest].lastKill>50):
                # to check on whether stimulus lies in the Field of View (FoV) and vervet is outside its corresponding refuge
                # i.e. to check if agent can visually spot the stimulus [visual scan]
                if(isInsideFoV(self.xpos,self.ypos,awareRadius,self.alpha*180/PI,fov,x,y)):
                    # getting alarmed about a predator (if agent is not in refuge) as it the vervet sees the predator
                    if(type == "leopard"):
                        if(checkhideout != 1):
                            alarm = 1
                            self.fLevel = 900
                            self.threat = 1

                    elif(type == "hawk"):
                        if(checkhideout != 2):
                            alarm = 2
                            self.fLevel = 800
                            self.threat = 2

                    elif(type == "python"):
                        if(checkhideout != 3):
                            alarm = 3
                            self.fLevel = 700
                            self.threat = 3

                    self.recentlySeenPredator = self.threat

                    if(self.fLevel>hLevel):
                        self.movement = 3 # move in direction opposite to line of sight of predator
                    

                    # storing and representing vervet alarm call data as it spots a predator, 
                    # only if it's the first one to see the predator.
                    if(first2See[closest]== 0 and alarm>0 and alarmPotency>0):
                        temp = self.xpos, self.ypos, alarm  
                        alarms.append(temp)   # storing alarm call data to be used in next frame
                        first2See[closest] = 1    # as this vervet is first to see the predator

                        if showSim == 1:
                            showAlarm(self, alarm, alarmPotency, auditoryAware)


        # Acting upon movement information
        if(self.movement == 1 and checkhideout != self.threat):
            v, self.alpha, self.eLevel = moveToForage(self.xpos, self.ypos, self.patch, self.eLevel)
        elif(self.movement == 2 and alarmPotency == 1):
            v, self.alpha, self.threat = moveToNearestRefuge(self, refuge)
        elif(self.movement == 2 and alarmPotency == 2):
            v, self.alpha = moveToRefuge(self, refuge, self.threat)
        elif(self.movement == 3):
            v, self.alpha = moveToAvoid(self, closest)


            
        # disappearance of fear level
        if(self.fLevel < 0):
            self.fLevel = 0
            self.recentlySeenPredator = 0
            self.threat = 0

        # fear level keeps decreasing by 1% per frame after being recently alarmed, if not further alarmed
        self.fLevel -= self.fLevel*.001


        # energy decay in agents
        # energy level decreases continuously after each frame even if agent is stagnant or decreases wrt agent speed

        self.eLevel -= (.05*v + .005 * self.eLevel) # to be tuned later

        # update coordinate based on velocity, orientation
        updatePosition(self, v)

        if(index == nAgents-1): # end of a particular frame
            for j in range(0,len(self.stim)):
                first2See[j]=0
            # use alarm lists of this frame for next frame
            _alarms = alarms
            alarms = []




def updatePosition(self,v):
    vx = v * math.cos(self.alpha)
    vy = v * math.sin(self.alpha)

    # updating the new position as vehicle moves
    self.xpos = self.xpos + vx
    self.ypos = self.ypos + vy




def showAlarm(self, alarm, alarmPotency, auditoryAware):
    # representing undifferentiable alarm calls
    if(alarmPotency == 1):
        fill(0)
        circle(self.xpos,self.ypos,10)
        stroke(0)
        noFill()
        circle(self.xpos,self.ypos,2*auditoryAware)

    # representing alarm calls visually in the environment
    if(alarm == 1 and alarmPotency == 2):
        fill(0)
        circle(self.xpos,self.ypos,10)
        stroke(0,0,255)
        noFill()
        circle(self.xpos,self.ypos,2*auditoryAware)
    elif(alarm == 2 and alarmPotency == 2):
        fill(0)
        circle(self.xpos,self.ypos,10)
        stroke(0,255,0)
        noFill()
        circle(self.xpos,self.ypos,2*auditoryAware)
    elif(alarm == 3 and alarmPotency == 2):
        fill(0)
        circle(self.xpos,self.ypos,10)
        stroke(255,0,0)
        noFill()
        circle(self.xpos,self.ypos,2*auditoryAware)
    noStroke()

# returns the index of closest predator to an agent
def closestPredator(self):
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

def getClosestRefuge(self, refugeLocations):
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
def moveToRefuge(self, refuge, alarm):

    relevantRefuges = threatRefugeInfo(self, refuge)
    refugeCode, closestRefuge, closestRefugeDist, refugeSize = getClosestRefuge(self, relevantRefuges)
    closestRefugeX, closestRefugeY = closestRefuge
    orienation = orientAlpha(closestRefugeX, closestRefugeY,self.xpos, self.ypos)

    if closestRefugeDist < refugeSize[0]/6 or closestRefugeDist < refugeSize[1]/6:
        velocity = 0
    else:
        velocity = 2 * self.fLevel / 1000 # updates velocity in case of alarm


    return velocity, orienation

def moveToNearestRefuge(self, refuge):

    refugeCode, closestRefuge, closestRefugeDist, refugeSize = getClosestRefuge(self, refuge)
    closestRefugeX, closestRefugeY = closestRefuge
    orienation = orientAlpha(closestRefugeX, closestRefugeY,self.xpos, self.ypos)

    if closestRefugeDist < refugeSize[0]/6 or closestRefugeDist < refugeSize[1]/6:
        velocity = 0
    else:
        velocity = 2 * self.fLevel / 1000 # updates velocity in case of alarm

    
    return velocity, orienation, refugeCode+1


def moveToAvoid(self,closest): # to guide vervets
    x,y = self.stim[closest].location()
    self.alpha = math.pi + orientAlpha(x,y,self.xpos,self.ypos)
    vel = 2 * self.fLevel / 1000
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
    
    vel = 2 * self.fLevel / 1000 

    v = (v1 + v2) / 2 # net velocity of vehicle

    # capping max speed depending on eLevel 
    if v>vel:
        v = vel

    self.alpha += (v1 - v2) * .08 # the rotating factor = 0.08

    return v, self.alpha


def checkAlarmCall(x,y,alarms,r):
    alarmIndex = 0
    alarmDist = 1500
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


def moveToForage(x,y,patch,eLevel):
    patchDist = width + height  # setting this as max value
    nearestPatch = 0 # dummy
    for i in range(0,len(patch)):
        totalR, maxR = resourceData(patch[i])
        if(patchDist>dist(patch[i].patchX,patch[i].patchY,x,y) and totalR/maxR>.1):
            patchDist = dist(patch[i].patchX,patch[i].patchY,x,y)
            nearestPatch = i
    
    alpha = orientAlpha(patch[nearestPatch].patchX,patch[nearestPatch].patchY,x,y)
    totalR, maxR = resourceData(patch[nearestPatch])

    if(patchDist > patch[nearestPatch].tempX/3):
        hLevel = 1000 - eLevel
        vel = 2 * hLevel / 1000
    else:
        vel = 0
        if(eLevel<900):
            eLevel += totalR * .01  # agent consuming 1% of total resources per frame
            for i in range(maxR/255):   # number of resource points in the patch
                patch[nearestPatch].patchPoints[2][i] -= patch[nearestPatch].patchPoints[2][i] * .01    # rLevel decreases with consumption

    if(eLevel > 1000):
        eLevel = 1000
    return vel, alpha, eLevel


def resourceData(ithPatch):
    d1,d2,rLevel = ithPatch.patchPoints
    maxR = len(rLevel) * 255
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
            return math.atan(h/b) + PI
        if(h<0 and b>0):
            return math.atan(h/b) + 2*PI

def isInsideFoV(x0,y0,r,alpha,theta,x,y):
    # x0,y0: point of view
    # x,y: point to be checked for being inside FoV
    # alpha: agent orientation
    # theta: scope angle of view
    # r: distance that agent can see
    la = PI*(alpha+theta/2)/180 # anglular co-ordinate of left extreme FoV
    ra = PI*(alpha-theta/2)/180 # anglular co-ordinate of right extreme FoV
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
    return sqrt((x-sx)**2+(y-sy)**2)

