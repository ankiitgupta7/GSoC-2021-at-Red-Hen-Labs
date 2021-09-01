import math
alpha = 0
x = 300
y = 300
r = 20

def setup():
    frameRate(100)
    size(600,600)

def draw(): 
    background(100,100,0)

    global x,y,r
    global alpha
    display(alpha)
    #point(x, y)
  #  r = 2 * math.sqrt(5) * z
    #alpha = alpha + math.pi/5000
def display(alpha):
    displayOutline(alpha)

def displayOutline(alpha):    
    #noFill()
    #arc(x, y + r, 2*r, 2*r, alpha-PI/6, alpha+7*PI/6)
    #arc(x - r*math.cos(alpha + PI/6), y - r * math.sin(alpha + PI/6), 2*r, 2*r, alpha + PI/2, alpha + 11*PI/6)
    #arc(x + r*math.cos(alpha + PI/6), y - r * math.sin(alpha + PI/6), 2*r, 2*r, alpha- 5*PI/6, alpha + PI/2)
    #arc(300, 300, z, z, alpha+3*PI/2,alpha+PI/6)
    noStroke()
    fill(255)
    circle(x + r*math.cos(alpha - PI/6), y + r * math.sin(alpha - PI/6), 2*r)
    circle(x + r*math.cos(alpha + PI/2), y + r * math.sin(alpha + PI/2), 2*r)
    circle(x + r*math.cos(alpha + 7*PI/6), y + r * math.sin(alpha + 7*PI/6), 2*r)
    stroke(0)
    triangle(x + .5 * r * math.cos(alpha + PI/4), y + .5 * r * math.sin(alpha + PI/4), x + .5 * r * math.cos(alpha + 3 * PI / 4), y + .5 * r * math.sin(alpha + 3 * PI / 4), x + 1.1 * r * math.cos(alpha + PI/2), y + 1.1 * r * math.sin(alpha + PI/2))
    circle(x + r*math.cos(alpha - PI/6), y + r * math.sin(alpha - PI/6), r/4)
    circle(x + r*math.cos(alpha + 7*PI/6), y + r * math.sin(alpha + 7*PI/6), r/4)
    noStroke()
    circle(x + 2.1 * r * math.cos(alpha - PI/6), y + 2.1 * r * math.sin(alpha - PI/6), r/2)
    circle(x + 2.1 * r * math.cos(alpha + 7*PI/6), y + 2.1 * r * math.sin(alpha + 7*PI/6), r/2)

