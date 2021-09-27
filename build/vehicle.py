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
    def __init__(self, xpos, ypos, z, stim, alpha, eLevel, fLevel, rfd, patch):
        # co-ordinates of the agent
        self.xpos = xpos
        self.ypos = ypos
        self.z = z # vehicle size scale
        self.stim = stim    # agent having access to all the stimuli present in the environment
        self.alpha = alpha # vehicle's orienation angle wrt +ve x-axis
        self.eLevel = eLevel # energy level of the agent
        self.fLevel = fLevel # fear level of the agent
        self.rfd = rfd # ready for death parameter after being predated
        self.patch = patch  # details about each resource patch in the environment

    def display(self, index, population, safeTime, frameNumber):
        colorGradient = 255*self.eLevel/1000          
        if(self.eLevel > 1000):
            colorGradient = 255   
        c = color(int(colorGradient))  
        if(safeTime[index][0] > (1000 - self.eLevel)):
            if(safeTime[index][1]==1):
                c = color(0,0,int(colorGradient))
            elif(safeTime[index][1]==2):
                c = color(0,int(colorGradient),0)
            elif(safeTime[index][1]==3):
                c = color(int(colorGradient),0,0)       

        fill(c)
        self.displayMonkey()
        noStroke()
        fill(0)
        text(population,10,635)
        text("Agents Alive",35,635)


    def displayMonkey(self):   
        noStroke()
        sc = self.z    # calibrating scale
        dispAngle = self.alpha - math.pi/6
        circle(self.xpos + sc*math.cos(dispAngle - math.pi/6), self.ypos + sc * math.sin(dispAngle - math.pi/6), 2*sc)    #eye1cover
        circle(self.xpos + sc*math.cos(dispAngle + math.pi/2), self.ypos + sc * math.sin(dispAngle + math.pi/2), 2*sc)    #mouthcover
        circle(self.xpos + sc*math.cos(dispAngle + 7*math.pi/6), self.ypos + sc * math.sin(dispAngle + 7*math.pi/6), 2*sc)    #eye2cover
        stroke(0)
        # mouth
        triangle(self.xpos + 0.5 * sc * math.cos(dispAngle + 11*math.pi/12), self.ypos + 0.5 * sc * math.sin(dispAngle + 11*math.pi/12), self.xpos + 0.5 * sc * math.cos(dispAngle + 17 * math.pi / 12), self.ypos + 0.5 * sc * math.sin(dispAngle + 17 * math.pi / 12), self.xpos + 1.1 * sc * math.cos(dispAngle + 7*math.pi/6), self.ypos + 1.1 * sc * math.sin(dispAngle + 7*math.pi/6))
        circle(self.xpos + sc*math.cos(dispAngle - math.pi/6), self.ypos + sc * math.sin(dispAngle - math.pi/6), sc/4)    #eye1
        circle(self.xpos + sc*math.cos(dispAngle + math.pi/2), self.ypos + sc * math.sin(dispAngle + math.pi/2), sc/4)    #eye2
        noStroke()
        circle(self.xpos + 2.1 * sc * math.cos(dispAngle - math.pi/6), self.ypos + 2.1 * sc * math.sin(dispAngle - math.pi/6), sc)  # ear1
        circle(self.xpos + 2.1 * sc * math.cos(dispAngle + math.pi/2), self.ypos + 2.1 * sc * math.sin(dispAngle + math.pi/2), sc)  #ear2


    def sensorLocation(self):
        ex1 = self.xpos + self.z * math.cos((self.alpha - math.pi/6) - math.pi/6)   # first eye's x-coordinates
        ey1 = self.ypos + self.z * math.sin((self.alpha - math.pi/6) - math.pi/6)   # first eye's y-coordinates
        ex2 = self.xpos + self.z * math.cos((self.alpha - math.pi/6) + math.pi/2)
        ey2 = self.ypos + self.z * math.sin((self.alpha - math.pi/6) + math.pi/2)
        return ex1, ey1, ex2, ey2


    def move(self,r,fov,index,refuge,nAgents,toggleAlarm,safeTime,first2See,frameNumber,scanFreq):
        global v, alarm, lx, ly, hx, hy, px, py, alarms, _alarms
        v, alarm = 0, 0
        lx, ly, hx, hy, px, py = refuge # obtaining refuge locations

        # checking whether the agent is inside a refuge
        checkhideout = isInsideHO(self.xpos, self.ypos, lx, ly, hx, hy, px, py)

        # checking any existing alarm call
        if(len(_alarms)>0 and toggleAlarm>0):
            alarm = checkAlarmCall(self.xpos, self.ypos, _alarms, r)


        # letting the closest predator to vervet attempt to kill
        i, proxim = closestPredator(self)  

        # check if predator is very close to agent
        # check if there was no recent kill by this predator
        # check if predator eLevel is not more than 9000
        # probability of predation success in this attempt = 80%
        if(proxim<20 and self.stim[i].lastKill>300 and self.stim[i].eLevel<9000 and random.uniform(0,1)>.2):    # conditions for predation
            # the agent is ready for death with a 80% probability!
            if(self.stim[i].type == "leopard"):
                self.rfd = [1,1]
            elif(self.stim[i].type == "hawk"):
                self.rfd = [1,2]    # 1 refers to death cnf, while 2 refers to death by 2nd predator, i.e., hawk
            elif(self.stim[i].type == "python"):
                self.rfd = [1,3]

            self.stim[i].lastKill = 0

        #setting up hunger level
        hLevel = 1000 - self.eLevel

        if(alarm>0):    # alarm call is there      
            self.fLevel = 600
            safeTime[index] = [self.fLevel, alarm]
            if(hLevel>self.fLevel): # hunger vs fear to decide forage or flee
                v, self.alpha, self.eLevel = moveToForage(self.xpos, self.ypos, self.patch, self.eLevel)
            elif(toggleAlarm == 1 and checkhideout!=alarm):
                v, self.alpha, safeTime[index][1] = moveToNearestRefuge(self, lx, ly, hx, hy, px, py)
            elif(toggleAlarm == 2 and alarm!=checkhideout):
                v, self.alpha = moveToRefuge(self, lx, ly, hx, hy, px, py, alarm)
        else:   # no alarm call
            # foraging and visual periodic scan of environment 
            if(frameNumber % scanFreq != 0):
                v, self.alpha, self.eLevel = moveToForage(self.xpos, self.ypos, self.patch, self.eLevel)
            else:   # scanning begins
                self.eLevel -= 50   # cost of scanning
                closest, closestDist = closestPredator(self)   # to choose the closest predator to react to
                        
                # check if there are more than one predator
                # check if fear level is more than hunger level
                # check if there was no recent kill by this predator
                if(len(self.stim)>0 and self.stim[closest].lastKill>50):
                    type = self.stim[closest].type    # type of predator
                    x,y = self.stim[closest].location()    # acquiring location of ith stimulus

                    # setting visual awareness radius for each vervet for different predator
                    if(type == "leopard"):
                        awareRadius = 2.5*r
                    elif(type == "hawk"):
                        awareRadius = 2*r
                    elif(type == "python"):
                        awareRadius = r

                    # setting auditory awareness thresold of vervets to hear alarm calls
                    auditoryAware = 3*r

                    # to check on whether stimulus lies in the Field of View (FoV) and vervet is outside its corresponding refuge
                    # i.e. to check if agent can visually spot the stimulus [visual scan]
                    if(isInsideFoV(self.xpos,self.ypos,awareRadius,self.alpha*180/PI,fov,x,y)):
                        # getting alarmed about a predator (if agent is not in refuge) as it the vervet sees the predator
                        if(type == "leopard"):
                            if(checkhideout != 1):
                                alarm = 1
                                self.fLevel = 900

                        elif(type == "hawk"):
                            if(checkhideout != 2):
                                alarm = 2
                                self.fLevel = 800

                        elif(type == "python"):
                            if(checkhideout != 3):
                                alarm = 3
                                self.fLevel = 700

                        safeTime[index] = [self.fLevel, alarm]   # time window till vervets moves towards the hideout after being aware
                        
                        if(self.fLevel>hLevel):
                            # figuring out resultant vevlocity on spotting a predator
                           # v, self.alpha = moveToAvoid(self, closest)
                            v, self.alpha = moveToRefuge(self, lx, ly, hx, hy, px, py, alarm)
                           # v2, alpha2 = 0, 0
                            # finding resultant movement data from the above to actions
                          #  vx = v1 * math.cos(alpha1) + v2 * math.cos(alpha2)
                          #  vy = v1 * math.sin(alpha1) + v2 * math.sin(alpha2)
                          #  v = math.sqrt(vx**2 + vy**2)
                          #  self.alpha = alpha1
                            #self.alpha = math.acos((math.cos(alpha1) + v2 * math.cos(alpha2))/v)
                        
                        else:
                            v, self.alpha, self.eLevel = moveToForage(self.xpos, self.ypos, self.patch, self.eLevel)


                        # storing and representing vervet alarm call data as it spots a predator, 
                        # only if it's the first one to see the predator.
                        if(first2See[closest]== 0 and alarm>0 and toggleAlarm>0):
                            temp = self.xpos, self.ypos, alarm  
                            alarms.append(temp)   # storing alarm call data to be used in next frame
                            first2See[closest] = 1    # as this vervet is first to see the predator

                            # representing undifferentiable alarm calls
                            if(toggleAlarm == 1):
                                fill(0)
                                circle(self.xpos,self.ypos,10)
                                stroke(0)
                                noFill()
                                circle(self.xpos,self.ypos,2*auditoryAware)


                            if(alarm == 1 and toggleAlarm == 2):
                                # representing alarm calls visually in the environment
                                fill(0)
                                circle(self.xpos,self.ypos,10)
                                stroke(0,0,255)
                                noFill()
                                circle(self.xpos,self.ypos,2*auditoryAware)
                            elif(alarm == 2 and toggleAlarm == 2):
                                fill(0)
                                circle(self.xpos,self.ypos,10)
                                stroke(0,255,0)
                                noFill()
                                circle(self.xpos,self.ypos,2*auditoryAware)
                            elif(alarm == 3 and toggleAlarm == 2):
                                fill(0)
                                circle(self.xpos,self.ypos,10)
                                stroke(255,0,0)
                                noFill()
                                circle(self.xpos,self.ypos,2*auditoryAware)

                    else:   # if scanning results in no threat
                        v, self.alpha, self.eLevel = moveToForage(self.xpos, self.ypos, self.patch, self.eLevel)
        # checkpoint    
        if(alarm == 0 and safeTime[index][0] > hLevel):    # vervets keeps moving until fear level is more than hunger
            v = 2 * safeTime[index][0] / 1000
            if(safeTime[index][1] == 1):
                self.alpha = orientAlpha(lx,ly,self.xpos,self.ypos)
            elif(safeTime[index][1] == 2):
                self.alpha = orientAlpha(hx,hy,self.xpos,self.ypos)
            elif(safeTime[index][1] == 3):
                self.alpha = orientAlpha(px,py,self.xpos,self.ypos)
        elif(alarm == 0 and safeTime[index][0]< 10):
            safeTime[index][0] = 0
            safeTime[index][1] = 0
        # fear level keeps decreasing by .8% per frame after being recently alarmed, if not further alarmed
        safeTime[index][0] -= safeTime[index][0]*.008

        vx = v * math.cos(self.alpha)
        vy = v * math.sin(self.alpha)

        # updating the new position as vehicle moves
        self.xpos = self.xpos + vx
        self.ypos = self.ypos + vy
        
        # energy level decreases continuously after each frame even if agent is stagnant or decreases wrt agent speed
        if(v==0):
            self.eLevel -= .0005 * self.eLevel
        else:
            self.eLevel -= (.5*v + .0005 * self.eLevel) # to be tuned later

        # to make vervets take a 180 degree turn as they hit boundary
        if self.xpos > .9*width:
            self.alpha += math.pi
        elif self.xpos <= 0:
            self.alpha += math.pi
        if self.ypos >= height:
            self.alpha += math.pi
        elif self.ypos <= 0:
            self.alpha += math.pi

        if(index == nAgents-1): # end of a particular frame
            for j in range(0,len(self.stim)):
                first2See[j]=0
            # use alarm lists of this frame for next frame
            _alarms = alarms
            alarms = []

# returns the index of closest predator to an agent
def closestPredator(self):
    m = len(self.stim)
    closest = 0
    closestDist = 5000
    for i in range(m):
        x,y = self.stim[i].location()    # acquiring location of ith stimulus
        if(dist(x,y,self.xpos,self.ypos)<closestDist):
            closestDist = dist(x,y,self.xpos,self.ypos)
            closest = i
    return closest, closestDist           

# a funtion to orient towards refuge when the agent is alarmed
def moveToRefuge(self, lx, ly, hx, hy, px, py, alarm):
    v = 2 * self.fLevel / 1000 # updates velocity in case of alarm

    if(alarm == 1):
        return v, orientAlpha(lx,ly,self.xpos,self.ypos)
    elif(alarm == 2):
        return v, orientAlpha(hx,hy,self.xpos,self.ypos)
    elif(alarm == 3):
        return v, orientAlpha(px,py,self.xpos,self.ypos)
    else:
        return v, self.alpha

def moveToNearestRefuge(self, lx, ly, hx, hy, px, py):
    v = 2 * self.fLevel / 1000 # updates velocity in case of alarm
    lrd = dist(self.xpos,self.ypos,lx,ly)   # leopard refuse distance
    hrd = dist(self.xpos,self.ypos,hx,hy)
    prd = dist(self.xpos,self.ypos,px,py)

    if(lrd<hrd and lrd<prd):
        return v, orientAlpha(lx,ly,self.xpos,self.ypos), 1
    elif(hrd<lrd and hrd<prd):
        return v, orientAlpha(hx,hy,self.xpos,self.ypos), 2
    elif(prd<hrd and prd<lrd):
        return v, orientAlpha(px,py,self.xpos,self.ypos), 3
    else:
        return v, self.alpha


# a function to respond to predator
def moveToAvoid(self,i):
    x,y = self.stim[i].location()    # acquiring location of ith stimulus

    # acquiring instantaneous co-ordinates of sensors
    s1x,s1y,s2x,s2y = self.sensorLocation()
    type = self.stim[i].type    # type of predator

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
    
    v = (v1 + v2) / 2 # net velocity of vehicle
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
    patchDist = 1200
    nearestPatch = 0 # dummy
    for i in range(0,len(patch)):
        totalR, maxR = resourceData(patch[i])
        if(patchDist>dist(patch[i].patchX,patch[i].patchY,x,y) and totalR/maxR>.1):
            patchDist = dist(patch[i].patchX,patch[i].patchY,x,y)
            nearestPatch = i
    
    alpha = orientAlpha(patch[nearestPatch].patchX,patch[nearestPatch].patchY,x,y)
    totalR, maxR = resourceData(patch[nearestPatch])

    if(patchDist > patch[nearestPatch].tempX/3):
        vel = 2000 / (eLevel + 1000)
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



def isInsideHO(x, y, lx, ly, hx, hy, px, py):
    # confirms hideout presence
    if(dist(x,y,lx,ly)<60):
        return 1    # leopard
    elif(dist(x,y,hx,hy)<60):
        return 2    # hawk
    elif(dist(x,y,px,py)<60):
        return 3    # python
    else:
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

