add_library('controlP5')
import random
import math
import stimulus
import vehicle
import resource
import os
# Remember to check on path of the stimulus image file at line 16-18

# Please note that this code requires the library "controlP5", 
# in order to execute it on the command line with "java -jar processing-py.jar run.py",
# please make sure to have the unzipped controlP5 files in the "libraries" folder 
# other than the "processing-py.jar" file in build directory

D = 650 #canvas dimensions

dataDirectory = os.path.join("./data", str(day()) + "-" + str(month()) + "-" + str(year()) + " " + str(hour()) + "-" + str(minute()))

img1 = loadImage("leopard2.jpg")
img2 = loadImage("hawk1.jpg")
img3 = loadImage("python5.jpg")



img = img1, img2, img3

start = 0

# setting up the environment window interface
def setup():
    size(2*D,D)


def draw():
    global cp5, n, d, r, stim, objs, patch, start, img1, img2, img3, n_leopard, n_hawk, n_python
    global fov, showSim, saveData, alarmPotency, safeTime, startOfSim, popGrowth, scanFreq, showSim
    global lh, hh, ph, lhx, lhy, hhx, hhy, phx, phy, hideout
    global sDeath, prDeath, lDeath, hDeath, pDeath, deathLocation
    global dataFile
    
    if(frameCount == 1):    # setting up control panel on executing run.py
        background('#004477')
        fill(126)
        rect(.9*width, 550, 80, 20)
        fill(0)
        textSize(16)
        text("     Run", .9*width, 566)

        # locating refuge (hideout) locations
        lhx, lhy = random.uniform(75+.7*2*D,.9*2*D-75), random.uniform(75,D-75)    # leopard hideout centre
        lh = lhx, lhy
        hhx, hhy = random.uniform(75,.2*2*D-75), random.uniform(75,D/2-75)    # hawk hideout centre
        hh = hhx, hhy
        phx, phy = random.uniform(75,.2*2*D-75), random.uniform(75 + D/2,D-75)    # python hideout centre
        ph = phx, phy
        hideout = lhx, lhy, hhx, hhy, phx, phy

        # setting up control panel inputs    
        cp5 = ControlP5(this)   

        #option = "Moving","Fixed"
        #cp5.addScrollableList("Opt for Stimuli Motion").setPosition(.9*width, 5).setSize(100, 50).setBarHeight(10).setItemHeight(10).addItems(option)
        #cp5.get(ScrollableList, "Opt for Stimuli Motion").setType(ControlP5.LIST)

        pToggle = cp5.addSlider("Enable Reproduction")
        pToggle.setPosition(.9*width,10).setSize(20,10).setRange(0, 1).setValue(1).setNumberOfTickMarks(2).setSliderMode(Slider.FLEXIBLE)
        
        pToggle = cp5.addSlider("Scan Freq")
        pToggle.setPosition(.9*width,35).setSize(60,10).setRange(10, 100).setValue(30).setNumberOfTickMarks(10).setSliderMode(Slider.FLEXIBLE)
        
        textSize(10)
        text("Choose No. of Stimulus", .9*width, 75)

        p1 = cp5.addSlider("leopard")
        p1.setPosition(.9*width,80).setSize(60,10).setRange(0, 9).setValue(1).setNumberOfTickMarks(10).setSliderMode(Slider.FLEXIBLE)

        p2 = cp5.addSlider("hawk")
        p2.setPosition(.9*width,110).setSize(60,10).setRange(0, 9).setValue(1).setNumberOfTickMarks(10).setSliderMode(Slider.FLEXIBLE)

        p3 = cp5.addSlider("python")
        p3.setPosition(.9*width,140).setSize(60,10).setRange(0, 9).setValue(1).setNumberOfTickMarks(10).setSliderMode(Slider.FLEXIBLE)

        showSimUI = cp5.addSlider("Show Simulation?")
        showSimUI.setPosition(.9*width,180).setSize(20,10).setRange(0, 1).setValue(1).setNumberOfTickMarks(2).setSliderMode(Slider.FLEXIBLE)

        logSimData = cp5.addSlider("Save Data?")
        logSimData.setPosition(.9*width,210).setSize(20,10).setRange(0, 1).setValue(0).setNumberOfTickMarks(2).setSliderMode(Slider.FLEXIBLE)

        aToggle = cp5.addSlider("Alarm Potency")
        aToggle.setPosition(.9*width,240).setSize(45,10).setRange(0, 2).setValue(2).setNumberOfTickMarks(3).setSliderMode(Slider.FLEXIBLE)

        
        pRatio = cp5.addSlider("P-Ratio")
        pRatio.setPosition(.9*width,300).setSize(60,10).setRange(4, 20).setValue(12).setNumberOfTickMarks(5).setSliderMode(Slider.FLEXIBLE)


        pDensity = cp5.addSlider("P-Density")
        pDensity.setPosition(.9*width,330).setSize(60,10).setRange(.3, .9).setValue(.6).setNumberOfTickMarks(3).setSliderMode(Slider.FLEXIBLE)


        nAgent = cp5.addSlider("Agents")
        nAgent.setPosition(.9*width,400).setSize(60,10).setRange(50, 500).setValue(200).setNumberOfTickMarks(10).setSliderMode(Slider.FLEXIBLE)

        
        scale = cp5.addSlider("scale")
        scale.setPosition(.9*width,430).setSize(60,10).setRange(3, 30).setValue(9).setNumberOfTickMarks(10).setSliderMode(Slider.FLEXIBLE)

        fov_dist = cp5.addSlider("r of FoV")
        fov_dist.setPosition(.9*width,460).setSize(60,10).setRange(10, 100).setValue(60).setNumberOfTickMarks(10).setSliderMode(Slider.FLEXIBLE)

        angle =  cp5.addSlider("FoV Angle")
        angle.setPosition(.9*width,490).setSize(60,10).setRange(0, 360).setValue(240).setNumberOfTickMarks(10).setSliderMode(Slider.FLEXIBLE)

    # triggering start / restart of simulation on clicking the "Run" button on control panel
    if mousePressed and (mouseButton == LEFT ) and mouseX>.9*width and mouseX<(.9*width+80) and mouseY>550 and mouseY<570:
        stim = list()  # creating an array of stimulus
        sDeath, prDeath, lDeath, hDeath, pDeath = 0, 0, 0, 0, 0 # to help in death data logging

        # feeding panel (default or altered) input into code
        n1 = int(cp5.getController("leopard").getValue())
        n2 = int(cp5.getController("hawk").getValue())
        n3 = int(cp5.getController("python").getValue())
        n_leopard, n_hawk, n_python = n1, n2, n3
        n = int(cp5.getController("Agents").getValue()) # initial number of agents at the start of simulation
        d = int(cp5.getController("scale").getValue())  # accessing vehicle scale parameter
        r = int(cp5.getController("r of FoV").getValue())   # radius of field of view
        fov = int(cp5.getController("FoV Angle").getValue())    # angle of filed of view
        showSim = cp5.getController("Show Simulation?").getValue()   # decision to show simulation or just make computations in background
        saveData = cp5.getController("Save Data?").getValue()   # decision to log simulation data on PC
        alarmPotency = cp5.getController("Alarm Potency").getValue() # alarm conditions
        popGrowth = int(cp5.getController("Enable Reproduction").getValue())   # option of reproduction
        scanFreq = int(cp5.getController("Scan Freq").getValue())   # visual scan frequency

        # to keep track of agent state - fear level and alarm state
        safeTime = []
        for i in range(1000*n):   # if agent population crosses 1000*n, an error would pop
            safeTime.append([0,0]) # first value is safeTime value, second is alarm type


        # generating stimuli at the start of simulation    
        for i in range(n1):
            # img, type, x, y, xspeed, yspeed, hl, nextAlarm, lastKill, eLevel
            stim.append(stimulus.stimulus(img1, 'leopard', .9*width/2, D/2, random.uniform(-3,3), random.uniform(-3,3), lh, 0, 1000, 5000))   # lh: leopard refuge

        for i in range(n2):
            stim.append(stimulus.stimulus(img2, 'hawk', .9*width/2, D/2, random.uniform(-4,4), random.uniform(-4,4), hh, 0, 1000, 5000))

        for i in range(n3):
            stim.append(stimulus.stimulus(img3, 'python', .9*width/2, D/2, random.uniform(-1.5,1.5), random.uniform(-1.5,1.5), ph, 0, 1000, 5000))


        # creating resource patches in the environment
        patch = list() 
        k = int(cp5.getController("P-Ratio").getValue())   # decides how densely the patchPoints (resource points - yellow dots) are arranged; also decides how big or small the patch size is
        patchDensity = cp5.getController("P-Density").getValue()   # decides how densely (0,1) the patches (the squares) are arranged
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

        # creating an array of agents at the start of simulation 
        objs = list()   
        for i in range(n):
            eLevel = 1000 * random.uniform(0,1) # assigning initial energy level to be a random between 0-1000
            alpha = 2 * math.pi * random.uniform(0,1)
            objs.append(vehicle.vehicle(random.uniform(0,.9*width), random.uniform(0,D), d, stim, alpha, eLevel, 0, [0,0], patch))
        

        # creating and initializing headers for simulation data to be saved
        if(saveData == 1):
            dataFile = saveSimData(alarmPotency)
            saveSimulationParameters(n, n1, n2, n3, r, fov, k, patchDensity, d)

        start = 1   # as simulation is ready to run now!
        startOfSim = frameCount # assigning the framenumber when simulation starts
        deathLocation = []  # to keep track of death of agents

    if(start==1):
        bc = color(0,100,100)
        background(bc)     # background of environment

        if showSim == 1:    # representing refuges
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

        elif showSim == 0 and saveData == 1:
            text("Simulation Data Being Saved, Don't Worry!", .5*width, 300)

        textAlign(LEFT)

        # rerun button - to restart the simulation afresh
        fill(126)
        rect(.9*width, 0, .1*width, height)
        fill(255)
        rect(.9*width, 550, 80, 20)
        fill(0)
        textSize(16)
        text("Run Again", .9*width, 566)
        

        # processing predators - death, movement & display
        i=0
        while(i<len(stim)):
            if(stim[i].eLevel<100 and len(stim)>0):  # death by starvation
                if(stim[i].type=='leopard'):
                    n_leopard -= 1
                elif(stim[i].type=='hawk'):
                    n_hawk -= 1
                elif(stim[i].type=='python'):
                    n_python -= 1
                del stim[i]
                i -= 1
            else:
                stim[i].move()
                if(showSim == 1):
                    stim[i].display()
            i += 1

        # processing patches
        for i in range(len(patch)):
            patch[i].patchPoints = patch[i].regrow()
            if showSim == 1:
                patch[i].display()  # display each resource patch
                
        # processing vervets - death, movement & display
        i = 0
        totalFear = 0
        totalHunger = 0
        totalEnergy = 0
        
        first2See = []
        for i in range(0,len(stim)):
            first2See.append(0)

        while(i<len(objs)):
            if(objs[i].eLevel<10 and len(objs)>1):  # death by starvation
                deathLocation.append([objs[i].xpos,objs[i].ypos,0,1])
                sDeath += 1

                del objs[i]
                del safeTime[i]
                i -= 1

            elif(objs[i].rfd[0] == 1 and len(objs)>1): # death by predation
                deathLocation.append([objs[i].xpos,objs[i].ypos,0,2])
                if(objs[i].rfd[1]==1):
                    lDeath += 1
                elif(objs[i].rfd[1]==2):
                    hDeath += 1
                elif(objs[i].rfd[1]==3):
                    pDeath += 1

                prDeath += 1

                del objs[i]
                del safeTime[i]
                i -= 1
                
            else:
                objs[i].move(r, fov, i, hideout, len(objs), alarmPotency, safeTime, first2See, frameCount - startOfSim + 1, scanFreq, showSim)  
                
                if(showSim == 1):
                    objs[i].display(i,len(objs),safeTime,frameCount - startOfSim + 1)

                totalFear += objs[i].fLevel
                totalHunger += (1000 - objs[i].eLevel)
                totalEnergy += objs[i].eLevel
            i += 1

        # modeling agent reproduction
        if((frameCount-startOfSim+1)%1000==0 and popGrowth==1):
            for i in range(len(objs)):
                if(objs[i].eLevel > 500 and random.uniform(0,1) > .5):
                    alpha = 2 * math.pi * random.uniform(0,1)
                    objs.append(vehicle.vehicle(random.uniform(0,.9*width), random.uniform(0,D), d, stim, alpha, 1000 * random.uniform(0,1), 0, [0,0], patch))

        # modelling predator reproduction
        if((frameCount-startOfSim+1)%1000==0 and popGrowth==1):
            for i in range(len(stim)):    
                if(stim[i].type == 'leopard' and stim[i].eLevel > 3000 and random.uniform(0,1) > .5):
                    stim.append(stimulus.stimulus(img1, 'leopard', .9*width/2, D/2, random.uniform(-3,3), random.uniform(-3,3), lh, 0, 1000, 5000))   # lh: leopard refuge
                    n_leopard += 1

                elif(stim[i].type == 'hawk' and stim[i].eLevel > 3000 and random.uniform(0,1) > .5):
                    stim.append(stimulus.stimulus(img2, 'hawk', .9*width/2, D/2, random.uniform(-4,4), random.uniform(-4,4), hh, 0, 1000, 5000))
                    n_hawk += 1

                elif(stim[i].type == 'python' and stim[i].eLevel > 3000 and random.uniform(0,1) > .5):
                    stim.append(stimulus.stimulus(img3, 'python', .9*width/2, D/2, random.uniform(-1.5,1.5), random.uniform(-1.5,1.5), ph, 0, 1000, 5000))
                    n_python += 1

        # represeting death
        x = 0
        while(x<len(deathLocation)):      
            if(deathLocation[x][2]<20):    # represents recent death for 20 frames
                deathLocation[x][2] += 1
                if(deathLocation[x][3]==1 and showSim == 1):    # death by starvation
                    fill(0)
                    square(deathLocation[x][0]-10,deathLocation[x][1]-10,20)
                elif(deathLocation[x][3]==2 and showSim == 1):  # death by predation
                    fill(0)
                    circle(deathLocation[x][0],deathLocation[x][1],20)
            else:
                del deathLocation[x]
                x -= 1
            x += 1

        
        # displaying simulation states live
        textSize(12)
        text("Time Unit:",10,635)
        text(frameCount-startOfSim+1,70,635)

        fill(255,0,0)
        text("#Python:", .9*width + 5, 605)
        text(n_python, .9*width + 5 + 60,605)
        fill(0,255,0)
        text("#Hawk:", .9*width + 5, 620)
        text(n_hawk, .9*width + 5 + 60,620)
        fill(0,0,255)
        text("#Leopard:", .9*width + 5, 635)
        text(n_leopard, .9*width + 5 + 60,635)
        
        fill(0,0,0)
        textSize(12)
        text("#Vervets:", .9*width + 2, 590)
        text(len(objs), .9*width + 2 + 55, 590)

        # to log data specific to each frame
        if saveData == 1:
            tempData = [len(objs), n_leopard, n_hawk, n_python, len(stim), lDeath, hDeath, pDeath, prDeath, sDeath, totalFear/len(objs), totalHunger/len(objs), totalEnergy/len(objs)]
            logData(dataFile, startOfSim, tempData)
          
        # revoke simulation data saving
        if((frameCount-startOfSim+1) == 1000000 and saveData == 1):
            closeOutputFiles(dataFile)
            print("Data has been saved for 1000000 frames.")
            #exit()

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

def saveSimulationParameters(n, n1, n2, n3, r, fov, k, patchDensity, d):
    simParam = createWriter(dataDirectory + "/simParameters.txt")
    simParam.print("Total number of Vervets = ")
    simParam.print(n)
    simParam.print("\n")
    simParam.print("Total number of Predators = ")
    simParam.print(n1+n2+n3)
    simParam.print("\n") 
    simParam.print("Total number of Leopards = ")
    simParam.print(n1)
    simParam.print("\n") 
    simParam.print("Total number of Hawks = ")
    simParam.print(n2)
    simParam.print("\n") 
    simParam.print("Total number of Pythons = ")
    simParam.print(n3)
    simParam.print("\n")
    simParam.print("The distance factor perceptible to Vervets = ")
    simParam.print(r)
    simParam.print("\n")
    simParam.print("Frontal Field of view of Vervets (in degrees) = ")
    simParam.print(fov)
    simParam.print("\n")
    simParam.print("Number of grids resource area to be divided into = ")
    simParam.print(k*k)
    simParam.print("\n")
    simParam.print("Density factor of resource grids = ")
    simParam.print(patchDensity)
    simParam.print("\n")
    simParam.print("Scale of Agent representation = ")
    simParam.print(d)
    simParam.print("\n")

    simParam.print("\n")
    simParam.flush()
    simParam.close()    

def saveSimData(alarmPotency):
    if alarmPotency == 0:
        dataFile = createWriter(dataDirectory + "/noAlarmData.csv")
        fillHeader(dataFile)
    elif alarmPotency == 1:
        dataFile = createWriter(dataDirectory + "/unDiffAlarmData.csv")
        fillHeader(dataFile)
    elif alarmPotency == 2:
        dataFile = createWriter(dataDirectory + "/diffAlarmData.csv")
        fillHeader(dataFile)
    return dataFile

def fillHeader(dataFile):
    dataFile.print("Time Unit")
    dataFile.print(",")
    dataFile.print("Vervet Population")
    dataFile.print(",")
    dataFile.print("Leopard Population")
    dataFile.print(",")
    dataFile.print("Hawk Population")
    dataFile.print(",")
    dataFile.print("Python Population")
    dataFile.print(",")
    dataFile.print("Predator Population")
    dataFile.print(",")
    dataFile.print("Deaths due to Leopard")
    dataFile.print(",")
    dataFile.print("Deaths due to Hawk")
    dataFile.print(",")
    dataFile.print("Deaths due to Python")
    dataFile.print(",")
    dataFile.print("Total Predation Deaths")
    dataFile.print(",")
    dataFile.print("Starvation Deaths")
    dataFile.print(",")
    dataFile.print("Average Fear Level")
    dataFile.print(",")
    dataFile.print("Average Hunger Level")
    dataFile.print(",")
    dataFile.print("Average Energy Level")
    dataFile.print("\n")

def logData(output, startOfSim, data):
    output.print(frameCount-startOfSim+1)
    for i in range(len(data)):
        output.print(",")
        output.print(data[i]) # Write the datum to the file
    output.print("\n") 

def closeOutputFiles(f1):
    f1.flush()  # Writes the remaining data to the file
    f1.close()  # Finishes the file