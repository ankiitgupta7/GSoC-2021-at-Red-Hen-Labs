add_library('controlP5')
import random
import math
import stimulus
import vehicle
import resource
# Remember to check on path of the stimulus image file at line 16-18

# Please note that this code requires the library "controlP5", 
# in order to execute it on the command line with "java -jar processing-py.jar run.py",
# please make sure to have the unzipped controlP5 files in the "libraries" folder 
# other than the "processing-py.jar" file in build directory

D = 650 #canvas dimensions


img1 = loadImage("E:/Work/Active/Red Hen Lab/Images/leopard2.jpg")
img2 = loadImage("E:/Work/Active/Red Hen Lab/Images/hawk1.jpg")
img3 = loadImage("E:/Work/Active/Red Hen Lab/Images/python5.jpg")



img = img1, img2, img3

start = 0

# setting up the environment window interface
def setup():
    size(2*D,D)


def draw():
    global cp5  
    global start
    global stim, objs, patch
    global n
    global d
    global r
    global fov, toggleAlarm, safeTime
    global lh, hh, ph, lhx, lhy, hhx, hhy, phx, phy, hideout


    if(frameCount == 1):
        background('#004477')
        fill(126)
        rect(.9*width, 550, 80, 20)
        fill(0)
        textSize(16)
        text("     Run", .9*width, 566)

        # locating hideouts
        lhx, lhy = random.uniform(75+.7*2*D,.9*2*D-75), random.uniform(75,D-75)    # leopard hideout centre
        lh = lhx, lhy
        hhx, hhy = random.uniform(75,.2*2*D-75), random.uniform(75,D/2-75)    # hawk hideout centre
        hh = hhx, hhy
        phx, phy = random.uniform(75,.2*2*D-75), random.uniform(75 + D/2,D-75)    # python hideout centre
        ph = phx, phy
        hideout = lhx, lhy, hhx, hhy, phx, phy





            
        cp5 = ControlP5(this)   

        option = "Moving","Fixed"
        cp5.addScrollableList("Opt for Stimuli Motion").setPosition(.9*width, 5).setSize(100, 50).setBarHeight(10).setItemHeight(10).addItems(option)
        cp5.get(ScrollableList, "Opt for Stimuli Motion").setType(ControlP5.LIST)

        
        textSize(10)
        text("Choose No. of Stimulus", .9*width, 60)

        p1 = cp5.addSlider("leopard")
        p1.setPosition(.9*width,80).setSize(80,15).setRange(0, 9).setValue(1).setNumberOfTickMarks(10).setSliderMode(Slider.FLEXIBLE)

        p2 = cp5.addSlider("hawk")
        p2.setPosition(.9*width,120).setSize(80,15).setRange(0, 9).setValue(1).setNumberOfTickMarks(10).setSliderMode(Slider.FLEXIBLE)

        p3 = cp5.addSlider("python")
        p3.setPosition(.9*width,160).setSize(80,15).setRange(0, 9).setValue(1).setNumberOfTickMarks(10).setSliderMode(Slider.FLEXIBLE)



        aToggle = cp5.addSlider("Toggle Alarms")
        aToggle.setPosition(.9*width,250).setSize(40,15).setRange(0, 2).setValue(1).setNumberOfTickMarks(3).setSliderMode(Slider.FLEXIBLE)


        pFactor = cp5.addSlider("Patch Factor")
        pFactor.setPosition(.9*width,300).setSize(60,15).setRange(2, 20).setValue(12).setNumberOfTickMarks(10).setSliderMode(Slider.FLEXIBLE)


        pDensity = cp5.addSlider("Patch Density")
        pDensity.setPosition(.9*width,330).setSize(60,15).setRange(.1, 1.0).setValue(.6).setNumberOfTickMarks(10).setSliderMode(Slider.FLEXIBLE)


        nAgent = cp5.addSlider("Agents")
        nAgent.setPosition(.9*width,400).setSize(80,15).setRange(30, 300).setValue(120).setNumberOfTickMarks(10).setSliderMode(Slider.FLEXIBLE)

        
        scale = cp5.addSlider("scale")
        scale.setPosition(.9*width,430).setSize(80,15).setRange(1, 10).setValue(2).setNumberOfTickMarks(10).setSliderMode(Slider.FLEXIBLE)

        fov_dist = cp5.addSlider("r of FoV")
        fov_dist.setPosition(.9*width,460).setSize(80,15).setRange(10, 100).setValue(60).setNumberOfTickMarks(10).setSliderMode(Slider.FLEXIBLE)

        angle =  cp5.addSlider("FoV Angle")
        angle.setPosition(.9*width,490).setSize(80,15).setRange(0, 360).setValue(240).setNumberOfTickMarks(10).setSliderMode(Slider.FLEXIBLE)


        
#        cp5.addScrollableList("2a stimulus population").setPosition(.9*width, 100).setSize(100, 80).setBarHeight(10).setItemHeight(10).addItems(l)
 #      cp5.addScrollableList("2b stimulus population").setPosition(.9*width, 200).setSize(100, 80).setBarHeight(10).setItemHeight(10).addItems(l)
  #      cp5.addScrollableList("3a stimulus population").setPosition(.9*width, 300).setSize(100, 80).setBarHeight(10).setItemHeight(10).addItems(l)
   #     cp5.get(ScrollableList, "2a stimulus population").setType(ControlP5.LIST)
    #    cp5.get(ScrollableList, "2b stimulus population").setType(ControlP5.LIST)
     #   cp5.get(ScrollableList, "3a stimulus population").setType(ControlP5.LIST)





    if mousePressed and (mouseButton == LEFT ) and mouseX>.9*width and mouseX<(.9*width+80) and mouseY>550 and mouseY<570:
        stim = list()  # creating an array of stimulus
        flag = int(cp5.getController("Opt for Stimuli Motion").getValue())
        n1 = int(cp5.getController("leopard").getValue())
        n2 = int(cp5.getController("hawk").getValue())
        n3 = int(cp5.getController("python").getValue())
        n = int(cp5.getController("Agents").getValue())
        d = int(cp5.getController("scale").getValue())  # accessing vehicle scale parameter
        r = int(cp5.getController("r of FoV").getValue())
        fov = int(cp5.getController("FoV Angle").getValue())
        toggleAlarm = int(cp5.getController("Toggle Alarms").getValue())


        safeTime = []
        for i in range(n):
            safeTime.append([0,0]) # first value is safeTime value, second is alarm type

        for i in range(n1):
            if(flag==0):    # 0: moving, 1: fixed
                stim.append(stimulus.stimulus(img1, 'leopard', .9*width/2, D/2, random.uniform(-3,3), random.uniform(-3,3), lh, 0))
            elif(flag==1):
                stim.append(stimulus.stimulus(img1, 'leopard', random.uniform(0,.9*width), random.uniform(0,D), 0, 0, lh, 0)) # lh: leopard hideout


        for i in range(n2):
            if(flag==0):
                stim.append(stimulus.stimulus(img2, 'hawk', .9*width/2, D/2, random.uniform(-4,4), random.uniform(-4,4), hh, 0))
            elif(flag==1):
                stim.append(stimulus.stimulus(img2, 'hawk', random.uniform(0,.9*width), random.uniform(0,D), 0, 0, hh, 0))



        for i in range(n3):
            if(flag==0):
                stim.append(stimulus.stimulus(img3, 'python', .9*width/2, D/2, random.uniform(-1.5,1.5), random.uniform(-1.5,1.5), ph, 0))
            elif(flag==1):
                stim.append(stimulus.stimulus(img3, 'python', random.uniform(0,.9*width), random.uniform(0,D), 0, 0, ph, 0))


# creating resource patches in the environment
        patch = list() 
        k = int(cp5.getController("Patch Factor").getValue())   # number of patches decider, no. of times width/height to be divided
        patchDensity = cp5.getController("Patch Density").getValue()   # how dense (0,1) the resource point are going to be
        tempX = .5*2*D/k    # because width of resource field is .7 - .2 = .5 times of total width 2*D
        tempY = D/k
       

        for i in range(1,k-1):
            for j in range(1,k-1):
                if(random.uniform(0,1) < patchDensity):
                    # patchPoints contain all the resource points coordinates as well as their resource levels
                    patchPoints = genPatchPoints([.2*2*D + i*tempX,.2*2*D + (i+1)*tempX], [j*tempY,(j+1)*tempY], k)
                    patchX = .2*2*D + i*tempX + tempX/2
                    patchY = j*tempY + tempY/2
                    patch.append(resource.resource(patchX, patchY, patchPoints,tempX,tempY))      

# creating an array of agents
        objs = list()   
        eLevel = 500 # assigning initial energy level to be 50% of maximum eLevel = 1000
        for i in range(n):
            alpha = 2 * math.pi * random.uniform(0,1)
            objs.append(vehicle.vehicle(random.uniform(0,.9*width), random.uniform(0,D), d, stim, alpha, eLevel, 50, patch))

        start = 1

    if(start==1):
        bc = color(0,100,100)
        background(bc)     # background of environment

        # representing Refuges

        fill(0,0,255)
        textSize(16)
        textAlign(CENTER, CENTER)
        circle(lhx,lhy,150)

        fill(0,255,0)
        circle(hhx,hhy,150)


        fill(255,0,0)
        circle(phx,phy,150)
        fill(0)
        text("Leopard Refuge",lhx,lhy)
        text("Hawk Refuge",hhx,hhy)
        text("Python Refuge",phx,phy)

        textAlign(LEFT)


        # UI 
        fill(126)
        rect(.9*width, 0, .1*width, height)
        fill(255)
        rect(.9*width, 550, 80, 20)
        fill(0)
        textSize(16)
        text("Run Again", .9*width, 566)
        
        textSize(12)
        text("Color Mapping", .9*width + 2, 590)
        fill(255,0,0)
        text("Red: Python", .9*width + 5, 605)
        fill(0,255,0)
        text("Green: Hawk", .9*width + 5, 620)
        fill(0,0,255)
        text("Blue: Leopard", .9*width + 5, 635)


        for i in range(len(stim)):
            # processing display and movement of stimulus
            stim[i].display()
            stim[i].move()

        for i in range(len(patch)):
            # display each resource patch
            patch[i].display()

        i = 0
        while(i<len(objs)):
            # processing display and movement of stimulus
            if(objs[i].eLevel<10):
                del objs[i]
                i -= 1
            else:
                objs[i].move(r, fov, i, hideout, len(objs), toggleAlarm, safeTime)  
                objs[i].display(i,len(objs),safeTime)
            i += 1

def genPatchPoints(xRange, yRange, n):  # generates initial resource levels at each resource points generated for each patch
    x0 = list()
    y0 = list()
    rLevel = list()
    x1, x2 = xRange
    y1, y2 = yRange
    for i in range(2*n):
        x0.append(random.uniform(x1, x2))
        y0.append(random.uniform(y1, y2))
        rLevel.append(random.uniform(55,255))
    return x0, y0, rLevel     # returns lists of randomly generated points along with their resource level
