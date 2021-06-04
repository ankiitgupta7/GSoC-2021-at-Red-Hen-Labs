D = 600
x = list()
y = list()
import random
import math


def setup(): 
    size(2*D, D)
    background(0)
    noStroke()
    fill(102)
    for i in range(1000):
        x.append(random.uniform(0,2*D))
        y.append(random.uniform(0,D))


def draw():
    background(100)
    insideFoV(300,300,200,209,61)




def dist(x,y,sx,sy):
    return sqrt((x-sx)**2+(y-sy)**2)




    # alpha: orientiation of agent
    # theta: scope of view


def insideFoV(x0,y0,r,alpha,theta):
    global x
    global y
    la = PI*(alpha+theta/2)/180 # left 
    ra = PI*(alpha-theta/2)/180
    xr  = x0 + r*math.cos(la)
    yr  = y0 + r*math.sin(la)
    xl  = x0 + r*math.cos(ra)
    yl  = y0 + r*math.sin(ra)
    fill(255)
    circle(x0, y0, 5)
    stroke(0)   
    line(x0,y0,xl,yl)
    line(x0,y0,xr,yr)
    noStroke()
  #  print(dist(xl,yl,x0,y0),dist(xr,yr,x0,y0))
    arc(x0, y0, 2*r, 2*r, PI*(alpha-theta/2)/180, PI*(alpha+theta/2)/180,PIE)
    
    for i in range(1000):

        l_check = (yl-y0)*(x[i]-x0) + (x0-xl)*(y[i]-y0)
        r_check = (yr-y0)*(x[i]-x0) + (x0-xr)*(y[i]-y0)

        h = y[i]-y0
        b = x[i]-x0
        if(h>0 and b>0):
            angle = math.atan(h/b)
        if(b<0):
            angle = math.atan(h/b) + PI
        if(h<0 and b>0):
            angle = math.atan(h/b) + 2 * PI

        d = dist(x0,y0,x[i],y[i])

        if(ra<0):
            ra = ra + 2 * PI
        if(la<0):
            la = la + 2 * PI
        if(angle<0):
            angle = angle + 2 * PI
        
        print(la,ra,angle)
        if(l_check<la and r_check>ra and d<r and theta<180):
            fill(200,0,0)
            circle(x[i], y[i], 5)
        elif(l_check<la and r_check<ra and d<r and theta>180):
            fill(200,0,0)
            circle(x[i], y[i], 5)
        elif(l_check>la and r_check>ra and d<r and theta>180):
            fill(200,0,0)
            circle(x[i], y[i], 5)
        elif(l_check<la and r_check>ra and d<r and theta>180):
            fill(200,0,0)
            circle(x[i], y[i], 5)
        
        else:            
            fill(0,105,0)
            circle(x[i], y[i], 5)

        

