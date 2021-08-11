
import random
import math

D = 600
k = 10
patch = list()
patchPoints = list()
tempX = 2*D/k
tempY = D/k

def setup(): 
    size(2*D, D)
    background(0)
    noStroke()
    fill(102)

    for i in range(1,k-1):
        for j in range(1,k-1):
            if(random.uniform(0,1)>.5):
                patch.append((i*tempX + tempX/2, j*tempY + tempY/2))
                x,y,rLevel = genRandomPoints([i*tempX,(i+1)*tempX], [j*tempY,(j+1)*tempY], k)
                patchPoints.append((x,y,rLevel))
        

def draw():
    global patch, tempX, tempY, patchPoints
    background(100)

  #  print(patch)
    for i in range(len(patch)):
        fill(0,189,135)
        circle(patch[i][0],patch[i][1],5)
        noFill()
        stroke(0,189,135)
        rect(patch[i][0]-tempX/2,patch[i][1]-tempY/2,tempX,tempY)
        x,y,rLevel = patchPoints[i] # rLevel: resource level

        noStroke()
        for j in range(len(x)):
            fill(rLevel[j],rLevel[j],0)
            circle(x[j],y[j],5)

            if(rLevel[j]<255):
                rLevel[j] += 0.1

    fill(189,135,0,255*.6)
    circle(300,300,50)
    fill(189*.6,135*.6,0)
    circle(300,400,50)
    fill(189,135,0)
    circle(300,500,50)



def dist(x,y,sx,sy):
    return sqrt((x-sx)**2+(y-sy)**2)


def genRandomPoints(xRange, yRange, n):
    x0 = list()
    y0 = list()
    rLevel = list()
    x1, x2 = xRange
    y1, y2 = yRange
    for i in range(n):
        x0.append(random.uniform(x1, x2))
        y0.append(random.uniform(y1, y2))
        rLevel.append(random.uniform(10,255))
    return x0, y0, rLevel     # returns lists of randomly generated points along with their resource level
