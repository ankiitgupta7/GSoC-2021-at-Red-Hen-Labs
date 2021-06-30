import random
import math
import vehicle_tools  as tools
import stimulus

alarm = 0
flag = 0
safeTime = []
for i in range(0,900):
    safeTime.append(0)

class vehicle(object):
    def __init__(self, xpos, ypos, z, stim, alpha):
        self.xpos = xpos
        self.ypos = ypos
        self.z = z # vehicle size scale
        self.stim = stim
        self.alpha = alpha # takes care of vehicle orienation

    def display(self):
        # sets up vehicle color intensity as per net velocity
        if(math.isnan(v)):
            c = color(0)
        elif(alarm == 1):
            c = color(0,133,195)    # aware of leopard
        elif(alarm == 2):
            c = color(0,195,133)    # aware of hawk
        elif(alarm == 3):
            c = color(189,100,0)    # aware of python
        else:
            c = color(int(255*(1-math.exp(-v))))
        stroke(c)
        # print("angle = ",self.alpha)
        self.displayBody()
        self.displayW1()
        self.displayW2()
        self.displaySensors()


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



    def move(self,r,fov,index,hideout):
        global v, safeTime, alarm, flag, lx, ly, hx, hy, px, py, minProxim
        v, v1, v2, a1, a2, alarm, minProxim = 0, 0, 0, 0, 0, 0, 1200
        lx, ly, hx, hy, px, py = hideout


        checkhideout = isInsideHO(self.xpos, self.ypos, lx, ly, hx, hy, px, py)


        # acquiring instantaneous co-ordinates of sensors
        s1x,s1y,s2x,s2y = self.sensorLocation()
        m = len(self.stim)
        # processing each of m stimuli at a time
        for i in range(m):   
            type = self.stim[i].type
            hox,hoy = self.stim[i].hl  # corresponding hideout co-ordinates
            x,y = self.stim[i].location()    # acquiring location of ith stimulus

            # updating behavioural wiring based on type
            if(type == "leopard" or type == "hawk" or type == "python"):
                behav = "2a"

            if(type == "leopard"):
                awareRadius = 3*r
            elif(type == "hawk"):
                awareRadius = 2*r
            elif(type == "python"):
                awareRadius = r



            # to check on whether stimulus lies in the Field of View (FoV) and vervet is outside its corresponding hideout
            if(isInsideFoV(self.xpos,self.ypos,awareRadius,self.alpha*180/PI,fov,x,y)):
                # decide on wiring weights based on vehicle type
                #print(self.alpha)

                proxim = dist(x,y,self.xpos,self.ypos)  # distance between agent and stimulus
                # to select the nearest stimuli to react to
                if(minProxim>proxim):
                    minProxim = proxim
                else:
                    # print (minProxim,proxim)
                    continue    # to ensure a vervet react to only the nearest preadtor

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

                safeTime[index] = 100   # time window till vervets moves towards the hideout after being aware

                if(type == "leopard"):
                    if(checkhideout != 1):
                        alarm = 1

                elif(type == "hawk"):
                    if(checkhideout != 2):
                        alarm = 2

                elif(type == "python"):
                    if(checkhideout != 3):
                        alarm = 3

                if(checkhideout != alarm and alarm!=0):
                    self.alpha = orientAlpha(hox,hoy,self.xpos,self.ypos)     
        
        v = (v1 + v2) / 2 # net velocity of vehicle

        if(checkhideout == alarm or (checkhideout>0 and alarm == 0)):
            v,v1,v2 = 0,0,0  
        
        elif(alarm == 0 and safeTime[index] > 0):    # vervets keeps moving till safetime becomes 0
            v = 2
            safeTime[index] = safeTime[index] - 1
            #print index,safeTime[index]

        vx = v * math.cos(self.alpha)
        vy = v * math.sin(self.alpha)

        self.alpha += (v1 - v2) * .08 # the rotating factor = 0.08
        # updating the new position as vehicle moves
        self.xpos = self.xpos + vx
        self.ypos = self.ypos + vy

        # to make vervets take a 180 degree turn as they hit boundary
        if self.xpos > .9*width:
            self.alpha += math.pi
        elif self.xpos <= 0:
            self.alpha += math.pi
        if self.ypos >= height:
            self.alpha += math.pi
        elif self.ypos <= 0:
            self.alpha += math.pi

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

