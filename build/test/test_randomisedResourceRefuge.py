
import random
import math

D = 650
refuge = 3
k = 3*refuge
patch = list()
patchPoints = list()


lRefuge = loadImage("trees.png")
hRefuge = loadImage("bush.png")
pRefuge = loadImage("stony-ground.jpg")



def setup(): 
    size(2*D, D)
    background(0)
    noStroke()
    fill(102)
    tempX = .9*width/(2*k)
    tempY = height/k
       

    for i in range(0,2*k):
        for j in range(0,k):
            resource = 0
            if random.uniform(0,1) > .5:
                patch.append([i*tempX + tempX/2, j*tempY + tempY/2, resource])

    random.shuffle(patch) 

    
    for i in range(refuge):
        patch[3*i][2] = 1
        patch[3*i+1][2] = 2
        patch[3*i+2][2] = 3

    i = 3*refuge
    while i<len(patch):
        x,y,rLevel = genRandomPoints([patch[i][0]-tempX/2,patch[i][0]+tempX/2], [patch[i][1]-tempY/2,patch[i][1]+tempY/2], int(240/k))
        patchPoints.append((x,y,rLevel))
        i+=1
    
    

def draw():
    global patch, tempX, tempY, patchPoints
    background(100)
    fill(126)
    rect(.9*width, 550, 80, 20)
    tempX = .9*width/(2*k)
    tempY = height/k
  #  print(patch)


  
    for i in range(refuge):
        image(lRefuge, patch[3*i][0] - tempX/2, patch[3*i][1] - tempY/2, tempX, tempY)
        image(hRefuge, patch[3*i+1][0] - tempX/2, patch[3*i+1][1] - tempY/2, tempX, tempY)
        image(pRefuge, patch[3*i+2][0] - tempX/2, patch[3*i+2][1] - tempY/2, tempX, tempY)

    i = 3*refuge
    while i<len(patch):
        fill(0,189,135)
        circle(patch[i][0],patch[i][1],5)
        noFill()
        stroke(0,189,135)
        rect(patch[i][0]-tempX/2,patch[i][1]-tempY/2,tempX,tempY)

        
        x,y,rLevel = patchPoints[i-3*refuge] # rLevel: resource level
        noStroke()

        for j in range(len(x)):
            fill(rLevel[j],rLevel[j],0)
            circle(x[j],y[j],5)
            if(rLevel[j]<255):
                rLevel[j] += 0.1
        
        i+=1


           



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
