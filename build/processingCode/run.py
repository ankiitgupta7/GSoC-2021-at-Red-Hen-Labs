# add_library('controlP5')

from controlP5 import ControlP5, Slider, ScrollableList

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

D = 900 # canvas dimensions
fps = 60    # number of desired frames per second


dataDirectory = os.path.join("./data", str(day()) + "-" + str(month()) + "-" + str(year()) + " " + str(hour()) + "-" + str(minute()))

img1 = loadImage("./Images/leopard2.jpg")
img2 = loadImage("./Images/hawk1.jpg")
img3 = loadImage("./Images/python5.jpg")

img = img1, img2, img3


leopard_trees = loadImage("./Images/tree.jpg")
hawk_bush = loadImage("./Images/bush.jpg")
pyhton_stones = loadImage("./Images/stony-ground.jpg")

refugeImage = [leopard_trees, hawk_bush, pyhton_stones] 

start = 0

# setting up the environment window interface
def setup():
    size(2*D,D)	
    frameRate(fps)


def draw():
    global cp5, n, n1, n2, n3, agentSize, r, stim, objs, patch, refuge, notEmptySpace, start, img1, img2, img3, refugeImage 
    global n_leopard, n_hawk, n_python, k, tempX, tempY, lRefuge, hRefuge, pRefuge, lastKill
    global fov, showSim, saveData, alarmPotency, startOfSim, popGrowth, scanFreq, dataFile
    global sDeath, prDeath, lDeath, hDeath, pDeath, deathLocation, resourceRichness
    global rsm, fMax, eMax, fBreed, growthRate, oneMeter
    global oneGeneration, breedingProbability, eIntakeFactor, forageFactor, predationSuccessProb

    eMax = 1000 # max energy level
    fMax = 1000 # max fear level

    if(frameCount == 1):    # setting up control panel on executing run.py
        background('#004477')
        fill(126)
        rect(.9*width, 550, 80, 20)
        fill(0)
        textSize(16)
        text("     Run", .9*width, 566)


        # setting up control panel inputs    
        cp5 = ControlP5(this)   

        #option = "Moving","Fixed"
        #cp5.addScrollableList("Opt for Stimuli Motion").setPosition(.9*width, 5).setSize(100, 50).setBarHeight(10).setItemHeight(10).addItems(option)
        #cp5.get(ScrollableList, "Opt for Stimuli Motion").setType(ControlP5.LIST)

        pToggle = cp5.addSlider("Enable Reproduction")
        pToggle.setPosition(.9*width,10).setSize(20,10).setRange(0, 1).setValue(1).setNumberOfTickMarks(2).setSliderMode(Slider.FLEXIBLE)
        
        pToggle = cp5.addSlider("Scan Freq")
        pToggle.setPosition(.9*width,35).setSize(60,10).setRange(10, 100).setValue(60).setNumberOfTickMarks(10).setSliderMode(Slider.FLEXIBLE)
        
        textSize(10)
        text("# of Stimulus", .9*width, 75)

        p1 = cp5.addSlider("leopard")
        p1.setPosition(.9*width,80).setSize(60,10).setRange(2, 20).setValue(12).setNumberOfTickMarks(10).setSliderMode(Slider.FLEXIBLE)

        p2 = cp5.addSlider("hawk")
        p2.setPosition(.9*width,110).setSize(60,10).setRange(2, 20).setValue(12).setNumberOfTickMarks(10).setSliderMode(Slider.FLEXIBLE)

        p3 = cp5.addSlider("python")
        p3.setPosition(.9*width,140).setSize(60,10).setRange(2, 20).setValue(12).setNumberOfTickMarks(10).setSliderMode(Slider.FLEXIBLE)

        showSimUI = cp5.addSlider("Show Simulation?")
        showSimUI.setPosition(.9*width,180).setSize(20,10).setRange(0, 1).setValue(1).setNumberOfTickMarks(2).setSliderMode(Slider.FLEXIBLE)

        logSimData = cp5.addSlider("Save Data?")
        logSimData.setPosition(.9*width,210).setSize(20,10).setRange(0, 1).setValue(0).setNumberOfTickMarks(2).setSliderMode(Slider.FLEXIBLE)

        aToggle = cp5.addSlider("Alarm Potency")
        aToggle.setPosition(.9*width,240).setSize(45,10).setRange(0, 2).setValue(2).setNumberOfTickMarks(3).setSliderMode(Slider.FLEXIBLE)

        
        rGrowth = cp5.addSlider("rGrowth%")
        rGrowth.setPosition(.9*width,270).setSize(60,10).setRange(6, 60).setValue(30).setNumberOfTickMarks(10).setSliderMode(Slider.FLEXIBLE)

        
        pRatio = cp5.addSlider("# of Refuge")
        pRatio.setPosition(.9*width,300).setSize(60,10).setRange(1, 5).setValue(3).setNumberOfTickMarks(5).setSliderMode(Slider.FLEXIBLE)


        pDensity = cp5.addSlider("P-Density")
        pDensity.setPosition(.9*width,330).setSize(60,10).setRange(.3, .9).setValue(.6).setNumberOfTickMarks(3).setSliderMode(Slider.FLEXIBLE)


        replProb = cp5.addSlider("Replication Probability")
        replProb.setPosition(.9*width,360).setSize(60,10).setRange(0.0, 0.9).setValue(.1).setNumberOfTickMarks(10).setSliderMode(Slider.FLEXIBLE)


        eIntake = cp5.addSlider("Energy Intake Factor")
        eIntake.setPosition(.9*width,390).setSize(60,10).setRange(0.1, 1.0).setValue(.5).setNumberOfTickMarks(10).setSliderMode(Slider.FLEXIBLE)


        nAgent = cp5.addSlider("Agents")
        nAgent.setPosition(.9*width,440).setSize(60,10).setRange(50, 500).setValue(350).setNumberOfTickMarks(10).setSliderMode(Slider.FLEXIBLE)

        
        genScale = cp5.addSlider("One Generation")
        genScale.setPosition(.9*width,470).setSize(60,10).setRange(1000, 10000).setValue(10000).setNumberOfTickMarks(10).setSliderMode(Slider.FLEXIBLE)

        fFactor = cp5.addSlider("Forage Factor")
        fFactor.setPosition(.9*width,500).setSize(60,10).setRange(0.1, 0.9).setValue(.9).setNumberOfTickMarks(10).setSliderMode(Slider.FLEXIBLE)

        predRate =  cp5.addSlider("Predation Success Rate")
        predRate.setPosition(.9*width,530).setSize(60,10).setRange(0.1, 0.9).setValue(.5).setNumberOfTickMarks(10).setSliderMode(Slider.FLEXIBLE)

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
        oneGeneration = int(cp5.getController("One Generation").getValue())  # number of frames in one generation
        forageFactor = float(cp5.getController("Forage Factor").getValue())   # radius of field of view
        predationSuccessProb = float(cp5.getController("Predation Success Rate").getValue())    # angle of filed of view
        showSim = cp5.getController("Show Simulation?").getValue()   # decision to show simulation or just make computations in background
        saveData = cp5.getController("Save Data?").getValue()   # decision to log simulation data on PC
        alarmPotency = cp5.getController("Alarm Potency").getValue() # alarm conditions
        popGrowth = int(cp5.getController("Enable Reproduction").getValue())   # option of reproduction
        scanFreq = int(cp5.getController("Scan Freq").getValue())   # visual scan frequency
        breedingProbability = float(cp5.getController("Replication Probability").getValue())  # probability of breeding after fBreed frames
        eIntakeFactor = float(cp5.getController("Energy Intake Factor").getValue())  # energy intake from kill
        growthRate = cp5.getController("rGrowth%").getValue()   # resource % growth in a day

        # oneGeneration = 10000 # means 10,000 frames reprepresenting total adult age of the vervet and the predators
        oneMeter = 1 # makes 1 m to 1 px

        rsm = .5 # speed multiplier: makes 10 m/s to 1 px/frame
        r = 50  # distance factor perceptible to vervets
        fov = 200  # frontal field of view of vervets in degrees
        agentSize = 10  # size of vervet agents

        fBreed = oneGeneration/10.0 # frequency of breeding, i.e., 10% of total age
        scanFreq = fBreed/20.0 # visual scan frequency

        r = r * oneMeter
        resourceRichness = 1
        growthRate = 1000.0 * growthRate/ oneGeneration



        print("n1: ", n1, "n2: ", n2, "n3: ", n3, "n: ", n, "agentSize: ", agentSize, "forageFactor: ", forageFactor, "predationSuccessProb: ", predationSuccessProb, "fBreed: ", fBreed, "r: ", r, "alarmPotency: ", alarmPotency, "popGrowth: ", popGrowth, "scanFreq: ", scanFreq, "breedingProbability: ", breedingProbability, "eIntakeFactor: ", eIntakeFactor, "growthRate: ", growthRate)
        
        # creating resource patches in the environment
        refuge = list()
        patch = list() 
        patchSizeControl = 3*int(cp5.getController("# of Refuge").getValue())   # decides how densely the patchPoints (resource points - yellow dots) are arranged; also decides how big or small the patch size is
        patchDensity = cp5.getController("P-Density").getValue()   # decides how densely (0,1) the patches (the squares) are arranged

        refuge, patch = createResourceRefugePatch(patchSizeControl, patchDensity, refuge, patch, resourceRichness)
      

        # obtain co-ordinates and size of refuges to avoid for predators
        avoidLocations = list()
        for i in range(3):
            avoidLocations.append(avoidRefugeLocations(i, refuge))

        lRefuge, hRefuge, pRefuge = avoidLocations

        lastKill = oneGeneration/100.0  # assuming lastKill was oneGeneration/100.0 frames ago, just to make them ready to hunt


        # generating stimuli at the start of simulation 
        intialAge = 0   # age of predators at the start of simulation

        for i in range(n1):
            # img, type, aAge, x, y, xspeed, yspeed, hl, lastKill, eLevel
            lx, ly = getInitialPredatorLocations(lRefuge)
            eLevel = eMax 
            lMaxSpeed = 15 * rsm    # max speed of leopard = 15 m/sec
            lOrient = 2 * math.pi * random.uniform(0,1) # intial orientation of leopard
            swf = 14
            stim.append(stimulus.stimulus(img1, 'leopard', intialAge, lx, ly, lMaxSpeed, lOrient, lRefuge, lastKill, swf, eLevel, eMax))   # lh: leopard refuge

        for i in range(n2):
            hx, hy = getInitialPredatorLocations(hRefuge)
            eLevel = eMax
            hMaxSpeed = 15 * rsm    # predFactor kept same for all predators - one factors also changed to same are fearFactor, swf, awarenessFactor
            hOrient = 2 * math.pi * random.uniform(0,1)
            swf = 14
            stim.append(stimulus.stimulus(img2, 'hawk', intialAge, hx, hy, hMaxSpeed, hOrient, hRefuge, lastKill, swf, eLevel, eMax))

        for i in range(n3):
            px, py = getInitialPredatorLocations(pRefuge)
            eLevel = eMax 
            pMaxSpeed = 15 * rsm
            pOrient = 2 * math.pi * random.uniform(0,1)
            swf = 365
            stim.append(stimulus.stimulus(img3, 'python', intialAge, px, py, pMaxSpeed, pOrient, pRefuge, lastKill, swf, eLevel, eMax))


        # creating an array of agents at the start of simulation 
        objs = list()   
        for i in range(n):
            eLevel = eMax
            alpha = 2 * math.pi * random.uniform(0,1)
            movement = 1    # movemevent rule, default is to forage
            recentlySeenPredator = 0    # information about having recently seen predator
            threat = 0  # awareness about predator
            aAge = 0 # adult age at start of simulation
            maxSpeed = 10 * rsm
            swf = 30 # to be tuned
            objs.append(vehicle.vehicle(random.uniform(0,.9*width), random.uniform(0,D), maxSpeed, aAge, agentSize, stim, alpha, movement, recentlySeenPredator, threat, eLevel, eMax, 0, fMax, [0,0], swf, patch))
        

        # creating and initializing headers for simulation data to be saved
        if(saveData == 1):
            dataFile = saveSimData(alarmPotency)
            saveSimulationParameters(n, n1, n2, n3, r, fov, patchSizeControl, patchDensity, d)

        start = 1   # as simulation is ready to run now!
        startOfSim = frameCount # assigning the framenumber when simulation starts
        deathLocation = []  # to keep track of death of agents

    if(start==1):
        bc = color(114,81,48)
        background(bc)     # background of environment

        if showSim == 1:    # displaying refuge locations
            for i in range(len(refuge)):
                image(refugeImage[i%3], refuge[i][0] - refuge[i][3]/2, refuge[i][1] - refuge[i][4]/2, refuge[i][3], refuge[i][4])


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
            if((stim[i].eLevel< .01*stim[i].eMax or stim[i].aAge >= oneGeneration) and len(stim)>0):  # death by starvation/aging
                if(stim[i].type=='leopard'):
                    n_leopard -= 1
                elif(stim[i].type=='hawk'):
                    n_hawk -= 1
                elif(stim[i].type=='python'):
                    n_python -= 1
                del stim[i]
                i -= 1
            else:
                stim[i].move(oneGeneration)
                if(showSim == 1):
                    stim[i].display()
                stim[i].aAge += 1
            i += 1

        # processing patches
        for i in range(len(patch)):
            patch[i].patchPoints = patch[i].regrow(growthRate)
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

        i=0
        while(i<len(objs) and len(objs)>0):
            if(objs[i].eLevel<.01*objs[i].eMax):  # death by starvation
                deathLocation.append([objs[i].xpos,objs[i].ypos,0,1])
                sDeath += 1

                del objs[i]
                i -= 1

            elif(objs[i].rfd[0] == 1): # death by predation
                deathLocation.append([objs[i].xpos,objs[i].ypos,0,2])
                if(objs[i].rfd[1]==1):
                    lDeath += 1
                elif(objs[i].rfd[1]==2):
                    hDeath += 1
                elif(objs[i].rfd[1]==3):
                    pDeath += 1

                prDeath += 1

                del objs[i]
                i -= 1

            elif(objs[i].aAge >= oneGeneration): # death due to aging
                deathLocation.append([objs[i].xpos,objs[i].ypos,0,3])
                del objs[i]
                i -= 1

                
            else:
                objs[i].move(i,r, fov, i, refuge, len(objs), alarmPotency, first2See, frameCount - startOfSim + 1, scanFreq, showSim, oneMeter, eIntakeFactor, forageFactor, predationSuccessProb, oneGeneration)  
                
                if(showSim == 1):
                    objs[i].display(i)

                objs[i].aAge += 1
                totalFear += objs[i].fLevel
                totalHunger += (eMax - objs[i].eLevel)
                totalEnergy += objs[i].eLevel
            i += 1

        # modeling agent reproduction
        vervetBreedingProbability = .5
        if((frameCount-startOfSim+1)%fBreed==0 and popGrowth==1):   # fBreed: breeding frequency
            for i in range(len(objs)):
                if(objs[i].eLevel > .5 * eMax and random.uniform(0,1) < vervetBreedingProbability):
                    alpha = 2 * math.pi * random.uniform(0,1)
                    movement = 1
                    recentlySeenPredator = 0
                    threat = 0
                    aAge = 0
                    maxSpeed = 10 * rsm
                    eLevel = eMax 
                    swf = 30
                    objs.append(vehicle.vehicle(random.uniform(0,.9*width), random.uniform(0,D), maxSpeed, aAge, agentSize, stim, alpha, movement, recentlySeenPredator, threat, eLevel, eMax, 0, fMax, [0,0], swf, patch))

        # modelling predator reproduction
        predadtorBreedingProbability = breedingProbability
        if((frameCount-startOfSim+1)%fBreed==0 and popGrowth==1):
            for i in range(len(stim)):    
                stim_aAge = 0

                if(stim[i].type == 'leopard' and stim[i].eLevel > .5 * eMax and random.uniform(0,1) < predadtorBreedingProbability):       
                    lx, ly = getInitialPredatorLocations(lRefuge)
                    eLevel = eMax 
                    lMaxSpeed = 15 * rsm    # max speed of leopard = 15 m/sec
                    lOrient = 2 * math.pi * random.uniform(0,1) # intial orientation of leopard
                    swf = 14    # not used for now
                    stim.append(stimulus.stimulus(img1, 'leopard', stim_aAge, lx, ly, lMaxSpeed, lOrient, lRefuge, lastKill, swf, eLevel, eMax))
                    n_leopard += 1

                elif(stim[i].type == 'hawk' and stim[i].eLevel > .5 * eMax and random.uniform(0,1) < predadtorBreedingProbability):
                    hx, hy = getInitialPredatorLocations(hRefuge)
                    eLevel = eMax 
                    hMaxSpeed = 15 * rsm
                    hOrient = 2 * math.pi * random.uniform(0,1)
                    swf = 14
                    stim.append(stimulus.stimulus(img2, 'hawk', stim_aAge, hx, hy, hMaxSpeed, hOrient, hRefuge, lastKill, swf, eLevel, eMax))
                    n_hawk += 1

                elif(stim[i].type == 'python' and stim[i].eLevel > .5 * eMax and random.uniform(0,1) < predadtorBreedingProbability):
                    px, py = getInitialPredatorLocations(pRefuge)
                    eLevel = eMax 
                    pMaxSpeed = 15 * rsm
                    pOrient = 2 * math.pi * random.uniform(0,1)
                    swf = 365
                    stim.append(stimulus.stimulus(img3, 'python', stim_aAge, px, py, pMaxSpeed, pOrient, pRefuge, lastKill, swf, eLevel, eMax))
                    n_python += 1

        # represeting death
        x = 0
        while(x<len(deathLocation)):      
            if(deathLocation[x][2] < 20):    # represents recent death for 20 frames
                deathLocation[x][2] += 1
                if(deathLocation[x][3]==1 and showSim == 1):    # death by starvation
                    fill(0)
                    square(deathLocation[x][0]-10,deathLocation[x][1]-10,20*agentSize/9)
                elif(deathLocation[x][3]==2 and showSim == 1):  # death by predation
                    fill(0)
                    circle(deathLocation[x][0],deathLocation[x][1],20*agentSize/9)
                elif(deathLocation[x][3]==3 and showSim == 1):  # death by aging
                    fill(255)
                    square(deathLocation[x][0]-10,deathLocation[x][1]-10,20*agentSize/9)
                    fill(0)
            else:
                del deathLocation[x]
                x -= 1
            x += 1

        
        # displaying simulation states live
        textSize(12)
        text("Generation Count: ",10,635)
        frameNumber = frameCount-startOfSim+1
        text(float(frameNumber)/oneGeneration,125,635)

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
        if saveData == 1 and len(objs) > 0:
            tempData = [len(objs), n_leopard, n_hawk, n_python, len(stim), lDeath, hDeath, pDeath, prDeath, sDeath, totalFear/len(objs), totalHunger/len(objs), totalEnergy/len(objs)]
            logData(dataFile, startOfSim, tempData)
          
        # revoke simulation data saving
        if((frameCount-startOfSim+1) == 50000 and saveData == 1):
            closeOutputFiles(dataFile)
            print("Data has been saved for 30000 frames.")
            #exit()


def dist(x,y,sx,sy):
    return sqrt((x-sx)**2+(y-sy)**2)


def getInitialPredatorLocations(refugeLocations):
    # refugeLocations has [x,y,sizeX,sizeY] - coordinates(x,y); dimensions(sizeX,sizeY)
    x, y = random.uniform(0,1)*.9*width, random.uniform(0,1)*height

    while(isInsideRefuge(x,y,refugeLocations)):
        x, y = random.uniform(0,1)*.9*width, random.uniform(0,1)*height

    return x,y

    
def isInsideRefuge(x,y,refuge):
    for i in range(len(refuge)):
        cx, cy = refuge[i][0], refuge[i][1] # centre coordinates of refuge
        w, h = refuge[i][2], refuge[i][3]   # width and height of refuge

        safeRadius = math.sqrt(w**2+h**2)/2
        if dist(cx,cy,x,y) <= safeRadius:
            return 1
    return 0



def genPatchPoints(xRange, yRange, n, resourceRichness):  # generates initial resource levels at each resource points generated for each patch
    x0 = list()
    y0 = list()
    rLevel = list()
    x1, x2 = xRange
    y1, y2 = yRange
    for i in range(n):
        x0.append(random.uniform(x1, x2))
        y0.append(random.uniform(y1, y2))
        rLevel.append(resourceRichness*random.uniform(0,255))   # resourceRichness is multiplier for richness of resource
    return x0, y0, rLevel     # returns lists of randomly generated points along with their resource level


def createResourceRefugePatch(k, patchDensity, refuge, patch, resourceRichness):
    tempX = .9*width/(2*k)    # because 10% of total width is taken by control panel
    tempY = height/k
    notEmptySpace = list()

    for i in range(0,2*k):
        for j in range(0,k):
            if(random.uniform(0,1) < patchDensity):
                notEmptySpace.append([i*tempX + tempX/2, j*tempY + tempY/2])

    random.shuffle(notEmptySpace) 
        
    for i in range(k):
        # x, y, refugeCode(0,1,2 for leopard, hawk, python resp.), width, height of image
        refuge.append([notEmptySpace[i][0],notEmptySpace[i][1],i%3,tempX,tempY])

    i = k
    while i<len(notEmptySpace):
        patchPoints = genPatchPoints([notEmptySpace[i][0]-tempX/2,notEmptySpace[i][0]+tempX/2], [notEmptySpace[i][1]-tempY/2,notEmptySpace[i][1]+tempY/2], int(240/k), resourceRichness)
        patchX = notEmptySpace[i][0]
        patchY = notEmptySpace[i][1]
        patch.append(resource.resource(patchX, patchY, patchPoints, tempX, tempY, resourceRichness))  
        i+=1

    return refuge, patch



     
def avoidRefugeLocations(avoidRefugeCode, refuge):
    refugeInfo = list()
    for i in range(len(refuge)):
        refugeCode = refuge[i][2]
        if(avoidRefugeCode == refugeCode):  # threat code is 1,2,3 while refugeCode is 0,1,2
            refugeInfo.append([refuge[i][0],refuge[i][1],refuge[i][3],refuge[i][4]])    # x,y coordinates and sizeX, sizeY

    return refugeInfo



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

   