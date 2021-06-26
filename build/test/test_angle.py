D = 600
import random
import math


def setup(): 
    size(2*D, D)
    background(0)
    noStroke()
    fill(102)



def draw():
    background(100)
    insideFoV(300,300,200,0,60)




def dist(x,y,sx,sy):
    return sqrt((x-sx)**2+(y-sy)**2)




    # alpha: orientiation of agent
    # theta: scope of view


def insideFoV(x0,y0,r,alpha,theta):
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
    #arc(x0, y0, 2*r, 2*r, PI*(alpha-theta/2)/180, PI*(alpha+theta/2)/180,PIE)
    #angle = 180 * math.atan((y-y0)/(x-x0)) / PI
    #print(180 * math.atan((400-y0)/(400-x0)) / PI, 180 * math.atan((400-y0)/(200-x0)) / PI, 180 * math.atan((200-y0)/(200-x0)) / PI, 180 * math.atan((200-y0)/(400-x0)) / PI)
    circle(400, 400, 5)
    circle(200, 400, 5)
    circle(200, 200, 5)
    circle(400, 200, 5)
    x = 400, 200, 200, 400
    y = 400, 400, 200, 200

    for i in range(4):
        h = y[i]-y0
        b = x[i]-x0
        textSize(16)
        if(h>0 and b>0):
            text(180 * math.atan(h/b) / PI, x[i], y[i])
        if(b<0):
            text(180 * math.atan(h/b) / PI + 180, x[i], y[i])
        if(h<0 and b>0):
            text(180 * math.atan(h/b) / PI + 360, x[i], y[i])




