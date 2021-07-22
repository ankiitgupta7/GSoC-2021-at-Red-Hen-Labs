add_library('controlP5')
import random
import math
import stimulus
import vehicle
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
    global stim
    global objs
    global n
    global d
    global r
    global fov, toggleAlarm
    global lh, hh, ph, lhx, lhy, hhx, hhy, phx, phy, resourceX, resourceY, hideout


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


        resourceX = random.sample(range(int(.2*2*D),int(.7*2*D)),int(.5*2*D/16))
        resourceY = random.sample(range(0, D), int(D/16))



            
        cp5 = ControlP5(this)   

        option = "Moving","Fixed"
        cp5.addScrollableList("Opt for Stimuli Motion").setPosition(.9*width, 5).setSize(100, 50).setBarHeight(10).setItemHeight(10).addItems(option)
        cp5.get(ScrollableList, "Opt for Stimuli Motion").setType(ControlP5.LIST)

        
        textSize(10)
        text("Choose No. of Stimulus", .9*width, 60)

        p1 = cp5.addSlider("leopard")
        p1.setPosition(.9*width,80).setSize(80,20).setRange(0, 9).setValue(1).setNumberOfTickMarks(10).setSliderMode(Slider.FLEXIBLE)

        p2 = cp5.addSlider("hawk")
        p2.setPosition(.9*width,120).setSize(80,20).setRange(0, 9).setValue(1).setNumberOfTickMarks(10).setSliderMode(Slider.FLEXIBLE)

        p3 = cp5.addSlider("python")
        p3.setPosition(.9*width,160).setSize(80,20).setRange(0, 9).setValue(1).setNumberOfTickMarks(10).setSliderMode(Slider.FLEXIBLE)



        aToggle = cp5.addSlider("Toggle Alarms")
        aToggle.setPosition(.9*width,300).setSize(40,20).setRange(0, 1).setValue(1).setNumberOfTickMarks(2).setSliderMode(Slider.FLEXIBLE)


        nAgent = cp5.addSlider("Agents")
        nAgent.setPosition(.9*width,400).setSize(80,20).setRange(0, 900).setValue(200).setNumberOfTickMarks(10).setSliderMode(Slider.FLEXIBLE)

        
        scale = cp5.addSlider("scale")
        scale.setPosition(.9*width,430).setSize(80,20).setRange(1, 10).setValue(2).setNumberOfTickMarks(10).setSliderMode(Slider.FLEXIBLE)

        fov_dist = cp5.addSlider("r of FoV")
        fov_dist.setPosition(.9*width,460).setSize(80,20).setRange(10, 100).setValue(40).setNumberOfTickMarks(10).setSliderMode(Slider.FLEXIBLE)

        angle =  cp5.addSlider("FoV Angle")
        angle.setPosition(.9*width,490).setSize(80,20).setRange(0, 360).setValue(200).setNumberOfTickMarks(10).setSliderMode(Slider.FLEXIBLE)


        
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


        for i in range(n1):
            if(flag==0):    # 0: moving, 1: fixed
                stim.append(stimulus.stimulus(img1, 'leopard', .9*width/2, D/2, random.uniform(0,4), random.uniform(0,4), lh, 0))
            elif(flag==1):
                stim.append(stimulus.stimulus(img1, 'leopard', random.uniform(0,.9*width), random.uniform(0,D), 0, 0, lh, 0)) # lh: leopard hideout


        for i in range(n2):
            if(flag==0):
                stim.append(stimulus.stimulus(img2, 'hawk', .9*width/2, D/2, random.uniform(0,8), random.uniform(0,8), hh, 0))
            elif(flag==1):
                stim.append(stimulus.stimulus(img2, 'hawk', random.uniform(0,.9*width), random.uniform(0,D), 0, 0, hh, 0))



        for i in range(n3):
            if(flag==0):
                stim.append(stimulus.stimulus(img3, 'python', .9*width/2, D/2, random.uniform(0,1), random.uniform(0,1), ph, 0))
            elif(flag==1):
                stim.append(stimulus.stimulus(img3, 'python', random.uniform(0,.9*width), random.uniform(0,D), 0, 0, ph, 0))



        objs = list()   # creating an array of vehicles
        for i in range(n):
            alpha = 2 * math.pi * random.uniform(0,1)
            objs.append(vehicle.vehicle(random.uniform(0,.9*width), random.uniform(0,D), d, stim, alpha))


        
        start = 1


    if(start==1):
        bc = color(0,100,100)
        background(bc)     # background of environment

    # resource representation
        fill(255,255,0)

        for i in range(len(resourceX)):
            for j in range(len(resourceY)):
                noStroke()
                circle(resourceX[i], resourceY[j],2)

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

        for i in range(n):
            # processing display and movement of stimulus
            objs[i].move(r, fov, i, hideout, n, toggleAlarm)  
            objs[i].display()
