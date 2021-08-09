import random
import math
import vehicle_tools  as tools
import stimulus
import resource

alarm = 0
flag = 0
first2See = []
for i in range(0,30):
    first2See.append(0)


# repository of alarm call details

lAlarms = [] 
hAlarms = [] 
pAlarms = []
_lAlarms = [] 
_hAlarms = [] 
_pAlarms = []

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

    def display(self, index, population,safeTime):
        colorGradient = 255*self.eLevel/1000            
        if(self.eLevel > 1000):
            colorGradient = 255        
        c = color(int(colorGradient))  
        if(self.fLevel > (1000 - self.eLevel)):
            if(safeTime[index][1]==1):
                c = color(0,0,int(colorGradient))
            elif(safeTime[index][1]==2):
                c = color(0,int(colorGradient),0)
            elif(safeTime[index][1]==3):
                c = color(int(colorGradient),0,0)       

        stroke(c)
        self.displayBody()
        self.displayW1()
        self.displayW2()
        self.displaySensors()
        noStroke()
        fill(0)
        text(population,10,635)
        text("Agents Alive",35,635)


    def displayBody(self):
        r = math.sqrt(20) * self.z
        angle = math.atan(1.0/2)
        theta = [2 * math.pi - angle, angle , math.pi - angle, math.pi + angle]
        # adding alpha to each theta
        theta = list(map(lambda t : t + self.alpha, theta))

        x1 = self.xpos+ r*math.cos(theta[0])
        y1 = self.ypos+ r*math.sin(theta[0])
        x2 = self.xpos+ r*math.cos(theta[1])
        y2 = self.ypos+ r*math.sin(theta[1])
        x3 = self.xpos+ r*math.cos(theta[2])
        y3 = self.ypos+ r*math.sin(theta[2])
        x4 = self.xpos+ r*math.cos(theta[3])
        y4 = self.ypos+ r*math.sin(theta[3])

        line(x1, y1, x2, y2)
        line(x2, y2, x3, y3)
        line(x3, y3, x4, y4)
        line(x4, y4, x1, y1)




    def displayW1(self):
        r = [math.sqrt(13) * self.z, math.sqrt(18) * self.z, math.sqrt(34) * self.z, math.sqrt(29) * self.z]
        angle = [math.atan(2.0/3), math.atan(1.0), math.atan(3.0/5), math.atan(2.0/5)]
        theta = [math.pi - angle[0], math.pi - angle[1] , math.pi - angle[2], math.pi - angle[3]]
        # adding alpha to each theta
        theta = list(map(lambda t : t + self.alpha, theta))

        x5 = self.xpos+ r[0]*math.cos(theta[0])
        y5 = self.ypos+ r[0]*math.sin(theta[0])
        x6 = self.xpos+ r[1]*math.cos(theta[1])
        y6 = self.ypos+ r[1]*math.sin(theta[1])
        x7 = self.xpos+ r[2]*math.cos(theta[2])
        y7 = self.ypos+ r[2]*math.sin(theta[2])
        x8 = self.xpos+ r[3]*math.cos(theta[3])
        y8 = self.ypos+ r[3]*math.sin(theta[3])

        line(x5, y5, x6, y6)
        line(x6, y6, x7, y7)
        line(x7, y7, x8, y8)
        line(x8, y8, x5, y5)




    def displayW2(self):
        r = [math.sqrt(13) * self.z, math.sqrt(18) * self.z, math.sqrt(34) * self.z, math.sqrt(29) * self.z]
        angle = [math.atan(2.0/3), math.atan(1.0), math.atan(3.0/5), math.atan(2.0/5)]
        theta = [math.pi + angle[0], math.pi + angle[1] , math.pi + angle[2], math.pi + angle[3]]
        # adding alpha to each theta
        theta = list(map(lambda t : t + self.alpha, theta))

        x9 = self.xpos+ r[0]*math.cos(theta[0])
        y9 = self.ypos+ r[0]*math.sin(theta[0])
        x10 = self.xpos+ r[1]*math.cos(theta[1])
        y10 = self.ypos+ r[1]*math.sin(theta[1])
        x11 = self.xpos+ r[2]*math.cos(theta[2])
        y11 = self.ypos+ r[2]*math.sin(theta[2])
        x12 = self.xpos+ r[3]*math.cos(theta[3])
        y12 = self.ypos+ r[3]*math.sin(theta[3])

        line(x9, y9, x10, y10)
        line(x10, y10, x11, y11)
        line(x11, y11, x12, y12)
        line(x12, y12, x9, y9)


    def displaySensors(self):
        r = [math.sqrt(40) * self.z, math.sqrt(40) * self.z, math.sqrt(16+4.0/9) * self.z, math.sqrt(16+4.0/9) * self.z]
        angle = [math.atan(1.0/3), math.atan(1.0/3), math.atan(1.0/6), math.atan(1.0/6)]
        theta = [2 * math.pi - angle[0], angle[1] , angle[2], 2 * math.pi - angle[3]]
        # adding alpha to each theta
        theta = list(map(lambda t : t + self.alpha, theta))

        x13 = self.xpos+ r[0]*math.cos(theta[0])
        y13 = self.ypos+ r[0]*math.sin(theta[0])
        x14 = self.xpos+ r[1]*math.cos(theta[1])
        y14 = self.ypos+ r[1]*math.sin(theta[1])
        x15 = self.xpos+ r[2]*math.cos(theta[2])
        y15 = self.ypos+ r[2]*math.sin(theta[2])
        x16 = self.xpos+ r[3]*math.cos(theta[3])
        y16 = self.ypos+ r[3]*math.sin(theta[3])

    #    line(x13, y13, x14, y14)
        line(x14, y14, x15, y15)
    #    line(x15, y15, x16, y16)
        line(x16, y16, x13, y13)

    def sensorLocation(self):
        r = [math.sqrt(40) * self.z, math.sqrt(40) * self.z, math.sqrt(16+4.0/9) * self.z, math.sqrt(16+4.0/9) * self.z]
        angle = [math.atan(1.0/3), math.atan(1.0/3), math.atan(1.0/6), math.atan(1.0/6)]
        theta = [2 * math.pi - angle[0], angle[1] , angle[2], 2 * math.pi - angle[3]]
        # adding alpha to each theta
        theta = list(map(lambda t : t + self.alpha, theta))
        x13 = self.xpos+ r[0]*math.cos(theta[0])
        y13 = self.ypos+ r[0]*math.sin(theta[0])
        x14 = self.xpos+ r[1]*math.cos(theta[1])
        y14 = self.ypos+ r[1]*math.sin(theta[1])
        return x13, y13, x14, y14

    def location(self):
        return self.xpos,self.ypos

    def move(self,r,fov,index,hideout,nAgents,toggleAlarm,safeTime):
        global v, alarm, flag, lx, ly, hx, hy, px, py, first2See, lAlarms, hAlarms, pAlarms, _lAlarms, _hAlarms, _pAlarms
        v, a1, a2, alarm = 0, 0, 0, 0
        lx, ly, hx, hy, px, py = hideout

        #setting up hunger level
        hLevel = 1000 - self.eLevel

        # checking whether the agent is inside a refuge
        checkhideout = isInsideHO(self.xpos, self.ypos, lx, ly, hx, hy, px, py)

        # finding the closest predator in the environment to react to
        i, proxim = closestPredator(self)

        # check if predator is very close to agent
        # check if there was no recent kill by this predator
        # probability of predation success in this attempt = 80%
        if(proxim<20 and self.stim[i].lastKill>300 and random.uniform(0,1)>.2):    # conditions for predation
            self.rfd = 1    # the agent is ready for death with a 80% probability!
            self.stim[i].lastKill = 0
            fill(0)
            circle(self.xpos,self.ypos,25)

        # calculate movement based on resource locations
        if(hLevel > self.fLevel):
            v, self.alpha, self.eLevel = moveToForage(self.xpos, self.ypos, self.patch, self.eLevel)

        # check if there are more than one predator
        # check if fear level is more than hunger level
        # check if there was no recent kill by this predator
        elif(len(self.stim)>0 and hLevel < self.fLevel and self.stim[i].lastKill>50):  
            type = self.stim[i].type    # type of predator
            x,y = self.stim[i].location()    # acquiring location of ith stimulus

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
            # i.e. to check if agent can visually spot the stimulus
            if(isInsideFoV(self.xpos,self.ypos,awareRadius,self.alpha*180/PI,fov,x,y)):
                v, self.alpha = moveToAvoid(self,i)

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

                # vervet giving Alarm Calls as it spots a predator, 
                # only if it's the first one to see the predator. Also at an interval.
                if(first2See[i]==0 and self.stim[i].nextAlarm == 0 and alarm>0):
                    temp = self.xpos,self.ypos,alarm,auditoryAware  
                    self.stim[i].nextAlarm = 100    # interval between two consecutive alarms
                    first2See[i] = 1    # as this vervet is first to see the predator

                    if(alarm==1):
                        lAlarms.append(temp)   # storing alarm call data to be used in next frame
                        if(toggleAlarm > 0): 
                            # representing alarm calls visually in the environment
                            fill(0,0,255)
                            circle(self.xpos,self.ypos,10)
                            stroke(0,0,255)
                            noFill()
                            circle(self.xpos,self.ypos,2*auditoryAware)
                    elif(alarm==2):
                        hAlarms.append(temp)
                        if(toggleAlarm > 0):
                            fill(0,255,0)
                            circle(self.xpos,self.ypos,10)
                            stroke(0,255,0)
                            noFill()
                            circle(self.xpos,self.ypos,2*auditoryAware)
                    elif(alarm==3):
                        pAlarms.append(temp)
                        if(toggleAlarm > 0):
                            fill(255,0,0)
                            circle(self.xpos,self.ypos,10)
                            stroke(255,0,0)
                            noFill()
                            circle(self.xpos,self.ypos,2*auditoryAware)

            # if doesn't spots this predator or isn't alarmed, checks for it's alarm
            elif(alarm == 0 and toggleAlarm>0):
                alarm = checkAlarmCall(self.xpos,self.ypos,_lAlarms, _hAlarms, _pAlarms,type)
        
                # in case there's an alarm
                if(toggleAlarm == 1 and alarm>0 and alarm!=checkhideout):
                    self.fLevel = 600
                    safeTime[index] = [self.fLevel, alarm]
                    v, self.alpha = moveToRefuge(self,i,checkhideout,alarm)
                elif(toggleAlarm == 2 and checkhideout<1 and alarm>0):
                    self.fLevel = 600
                    v,self.alpha,alarm = moveToNearestRefuge(self, lx, ly, hx, hy, px, py, alarm)
                    safeTime[index] = [self.fLevel, alarm]
            
            if(self.stim[i].nextAlarm>0):
                self.stim[i].nextAlarm -= 1
        
        # if agent is in refuge of a predator, it doesn't move
        if(checkhideout == alarm or (checkhideout>0 and alarm == 0 and hLevel<self.fLevel)):
            v = 0  
        elif(alarm == 0 and safeTime[index][0] > 50):    # vervets keeps moving till safetime becomes 0
            v = 2 * safeTime[index][0] / 1000
            # fear level keeps decreasing by .8% per frame after being recently alarmed, if not further alarmed
            safeTime[index][0] -= safeTime[index][0]*.008 
        elif(safeTime[index][0] < 50):  # if fear level drops below 50 then update alarm status to zero
            safeTime[index][1] = 0

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
            for j in range(0,30):
                first2See[j]=0
            # use alarm lists of this frame for next frame
            _lAlarms, _hAlarms, _pAlarms = lAlarms, hAlarms, pAlarms
            lAlarms, hAlarms, pAlarms = [], [], []

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
def moveToRefuge(self,i,checkhideout,alarm):
    hox,hoy = self.stim[i].hl  # corresponding hideout co-ordinates
    v = 2 * self.fLevel / 1000 # updates velocity in case of alarm

    if(checkhideout != alarm and alarm!=0):
        self.alpha = orientAlpha(hox,hoy,self.xpos,self.ypos)
    return v, self.alpha

def moveToNearestRefuge(self, lx, ly, hx, hy, px, py, alarm):
    v = 2 * self.fLevel / 1000 # updates velocity in case of alarm
    lrd = dist(self.xpos,self.ypos,lx,ly)   # leopard refuse distance
    hrd = dist(self.xpos,self.ypos,hx,hy)
    prd = dist(self.xpos,self.ypos,px,py)

    if(lrd<hrd and lrd<prd):
        return v,orientAlpha(lx,ly,self.xpos,self.ypos),1
    elif(hrd<lrd and hrd<prd):
        return v,orientAlpha(hx,hy,self.xpos,self.ypos),2
    elif(prd<hrd and prd<lrd):
        return v,orientAlpha(px,py,self.xpos,self.ypos),3
    else:
        return v,self.alpha,alarm


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


def checkAlarmCall(x,y,lAlarms,hAlarms,pAlarms,type):
    # TBD which alarm to consider finally
    if(type=="leopard"):
        for i in range(len(lAlarms)):
            lAlarmX,lAlarmY,alarm,lAwareRadius = lAlarms[i]
            if(dist(x,y,lAlarmX,lAlarmY)<lAwareRadius):
                return 1

    elif(type=="hawk"):
        for i in range(len(hAlarms)):
            hAlarmX,hAlarmY,alarm,hAwareRadius = hAlarms[i]
            if(dist(x,y,hAlarmX,hAlarmY)<hAwareRadius):
                return 2

    elif(type=="python"):
        for i in range(len(pAlarms)):
            pAlarmX,pAlarmY,alarm,pAwareRadius = pAlarms[i]
            if(dist(x,y,pAlarmX,pAlarmY)<pAwareRadius):
                return 3
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
        if(eLevel<1000):
            eLevel += totalR * .1  # agent consuming 10% of total resources per frame
            for i in range(maxR/255):   # number of resource points in the patch
                patch[nearestPatch].patchPoints[2][i] -= patch[nearestPatch].patchPoints[2][i] * .1    # rLevel decreases with consumption

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

