import random
import math
import stimulus
import vehicle
import resourcePatch

import datetime
import time
import os
import csv

from pathlib import Path


Path("./data").mkdir(parents=True, exist_ok=True)



start = 0

def runSim(endSimFrame, simParam):
    count = 1
    simData = []
    while count<=endSimFrame:
        global cp5, n, n1, n2, n3, d, r, stim, objs, patch, refuge, notEmptySpace, start, img1, img2, img3, refugeImage 
        global n_leopard, n_hawk, n_python, k, tempX, tempY, lRefuge, hRefuge, pRefuge, lastKill
        global fov, showSim, saveData, alarmPotency, startOfSim, popGrowth, scanFreq, dataFile
        global sDeath, prDeath, lDeath, hDeath, pDeath, deathLocation, resourceRichness
        global rtm, rdm, rsm, fMax, eMax, fBreed, oneSecond, oneMinute, oneHour, oneDay, oneYear, growthRate, oneMeter
        global oneGeneration

        eMax = 1000 # max energy level
        fMax = 1000 # max fear level

        # if count == 1:    # setting up control panel on executing run.py
        #     print("No control panel for the time being, but you may use console or use tKinter later")

        # triggering start / restart of simulation on clicking the "Run" button on control panel
        if count == 1:
            stim = list()  # creating an array of stimulus
            sDeath, prDeath, lDeath, hDeath, pDeath = 0, 0, 0, 0, 0 # to help in death data logging

            fps, simAreaParam, n_predator, n_vervet, vervet_size, radiusFOV, angleFOV, alarmPotency, popGrowth, scanFreq, timeScale, spaceScale, resourceGrowthRate = simParam

            width = simAreaParam
            height = simAreaParam

            # feeding panel (default or altered) input into code
            n1 = n_predator
            n2 = n_predator
            n3 = n_predator
            n_leopard, n_hawk, n_python = n1, n2, n3
            n = n_vervet # initial number of agents at the start of simulation
            d = vervet_size  # accessing agent size scaling parameter
            r = radiusFOV   # radius of field of view
            fov = angleFOV    # angle of filed of view
            alarmPotency = alarmPotency # alarm conditions
            popGrowth = popGrowth   # option of reproduction - 0 or 1
            # scanFreq = scanFreq   # visual scan frequency - minutes
            rtm = timeScale   # real time multipier    [/second to /frame]
            rdm = spaceScale  # real distance multipier   [meter to px] 
            growthRate = resourceGrowthRate   # resource % growth in a day

            # rsm = 10/float(rdm*fps) # real speed multiplier [m/s to px/frame]
            oneSecond = fps/rtm # number of frames in a second
            oneMinute = 60*oneSecond # number of frames in a minute
            oneHour = math.ceil(60*oneMinute)  # number of frames in a hour
            oneDay = math.ceil(24*oneHour)  # number of frames in a day
            oneYear = math.ceil(365*oneDay)  # number of frames in a year
            oneMeter = 1/rdm



            oneGeneration = 10000 # means 10,000 frames reprepresenting total adult age of the vervet and the predators
            oneYear = 1000  # number of frames in a year in the simulation
            oneMeter = 1 # makes 1 m to 1 px

            rsm = .5 # speed multiplier: makes 10 m/s to 1 px/frame


            # fBreed = oneYear    # to be tuned
            # scanFreq = math.ceil(scanFreq * oneMinute)

            fBreed = oneGeneration / 10 # frequency of breeding

            r = r * oneMeter
            resourceRichness = 1
                
            # creating resource patches in the environment
            refuge = list()
            patch = list() 

            numberOfRefuges = 3 # number of refuges in the environment from each predator
            patchSizeControl = 3*numberOfRefuges   # decides how densely the patchPoints (resource points - yellow dots) are arranged; also decides how big or small the patch size is
            patchDensity = .6   # decides how densely (0,1) the patches (the squares) are arranged

            refuge, patch = createResourceRefugePatch(patchSizeControl, patchDensity, refuge, patch, resourceRichness, width, height)
        

            # obtain co-ordinates and size of refuges to avoid for predators
            avoidLocations = list()
            for i in range(3):
                avoidLocations.append(avoidRefugeLocations(i, refuge))

            lRefuge, hRefuge, pRefuge = avoidLocations

            lastKill = 300  # assuming lastKill was 300 frames ago, just to make them ready to hunt

            # generating stimuli at the start of simulation    
            for i in range(n1):
                lx, ly = getInitialPredatorLocations(lRefuge, width, height)
                randAge = int(10 * oneYear * random.uniform(0,1))
                eLevel = eMax
                lMaxSpeed = 15 * rsm    # max speed of leopard = 15 m/sec
                lOrient = 2 * math.pi * random.uniform(0,1) # intial orientation of leopard
                swf = 14
                stim.append(stimulus.stimulus('leopard', randAge, lx, ly, lMaxSpeed, lOrient, lRefuge, lastKill, swf, eLevel, eMax))   # lh: leopard refuge

            for i in range(n2):
                hx, hy = getInitialPredatorLocations(hRefuge, width, height)
                randAge = int(10 * oneYear * random.uniform(0,1))
                eLevel = eMax
                hMaxSpeed = 45 * rsm
                hOrient = 2 * math.pi * random.uniform(0,1)
                swf = 14
                stim.append(stimulus.stimulus('hawk', randAge, hx, hy, hMaxSpeed, hOrient, hRefuge, lastKill, swf, eLevel, eMax))

            for i in range(n3):
                px, py = getInitialPredatorLocations(pRefuge, width, height)
                randAge = int(10 * oneYear * random.uniform(0,1))
                eLevel = eMax
                pMaxSpeed = .45 * rsm
                pOrient = 2 * math.pi * random.uniform(0,1)
                swf = 365
                stim.append(stimulus.stimulus('python', randAge, px, py, pMaxSpeed, pOrient, pRefuge, lastKill, swf, eLevel, eMax))


            # creating an array of agents at the start of simulation 
            objs = list()   
            for i in range(n):
                eLevel = eMax 
                alpha = 2 * math.pi * random.uniform(0,1)
                movement = 1    # movemevent rule, default is to forage
                recentlySeenPredator = 0    # information about having recently seen predator
                threat = 0  # awareness about predator
                aAge = int(10 * oneYear * random.uniform(0,1)) # random adult age at start of simulation
                maxSpeed = 10 * rsm
                swf = 30 # to be tuned
                objs.append(vehicle.vehicle(random.uniform(0,width), random.uniform(0,height), maxSpeed, aAge, d, stim, alpha, movement, recentlySeenPredator, threat, eLevel, eMax, 0, fMax, [0,0], swf, patch))
            

            start = 1   # as simulation is ready to run now!
            startOfSim = count # assigning the framenumber when simulation starts
            deathLocation = []  # to keep track of death of agents

        #    showOnConsoleAfterRun(fps, rtm, rdm, eMax, fMax, growthRate, scanFreq, r, resourceRichness, simAreaParam)

        if(start==1):
            # processing predators - death, movement & display
            i=0
            while(i<len(stim)):
                if((stim[i].eLevel< .01*stim[i].eMax or stim[i].aAge >= 10 * oneYear) and len(stim)>0):  # death by starvation/aging
                    if(stim[i].type=='leopard'):
                        n_leopard -= 1
                    elif(stim[i].type=='hawk'):
                        n_hawk -= 1
                    elif(stim[i].type=='python'):
                        n_python -= 1
                    del stim[i]
                    i -= 1
                else:
                    stim[i].move(oneHour, width, height)
                    stim[i].aAge += 1
                i += 1

            # processing patches
            for i in range(len(patch)):
                patch[i].patchPoints = patch[i].regrow(oneDay, growthRate)
                    
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

                elif(objs[i].aAge >= 10 * oneYear): # death due to aging
                    deathLocation.append([objs[i].xpos,objs[i].ypos,0,3])
                    del objs[i]
                    i -= 1

                    
                else:
                    objs[i].move(i,r, fov, i, refuge, len(objs), alarmPotency, first2See, count - startOfSim + 1, scanFreq, oneMeter, oneMinute, width, height)  
                    

                    objs[i].aAge += 1
                    totalFear += objs[i].fLevel
                    totalHunger += (eMax - objs[i].eLevel)
                    totalEnergy += objs[i].eLevel
                i += 1

            # modeling agent reproduction
            if((count-startOfSim+1)%fBreed==0 and popGrowth==1):   # fBreed: breeding frequency
                for i in range(len(objs)):
                    if(objs[i].eLevel > .5 * eMax and random.uniform(0,1) > .5):
                        alpha = 2 * math.pi * random.uniform(0,1)
                        movement = 1
                        recentlySeenPredator = 0
                        threat = 0
                        aAge = 0
                        maxSpeed = 10 * rsm
                        eLevel = eMax
                        swf = 30
                        objs.append(vehicle.vehicle(random.uniform(0,width), random.uniform(0,height), maxSpeed, aAge, d, stim, alpha, movement, recentlySeenPredator, threat, eLevel, eMax, 0, fMax, [0,0], swf, patch))

            # modelling predator reproduction
            if((count-startOfSim+1)%fBreed==0 and popGrowth==1):
                for i in range(len(stim)):    
                    stim_aAge = 0

                    expectedNumberOfEachPredator = len(objs) / (10 * 3)

                    if(stim[i].type == 'leopard' and stim[i].eLevel > .5 * eMax and random.uniform(0,1) > (n_leopard/expectedNumberOfEachPredator)):       
                        lx, ly = getInitialPredatorLocations(lRefuge, width, height)
                        eLevel = eMax 
                        lMaxSpeed = 15 * rsm    # max speed of leopard = 15 m/sec
                        lOrient = 2 * math.pi * random.uniform(0,1) # intial orientation of leopard
                        swf = 14
                        stim.append(stimulus.stimulus('leopard', stim_aAge, lx, ly, lMaxSpeed, lOrient, lRefuge, lastKill, swf, eLevel, eMax))
                        n_leopard += 1

                    elif(stim[i].type == 'hawk' and stim[i].eLevel > .5 * eMax and random.uniform(0,1) > (n_hawk/expectedNumberOfEachPredator)):
                        hx, hy = getInitialPredatorLocations(hRefuge, width, height)
                        eLevel = eMax 
                        hMaxSpeed = 45 * rsm
                        hOrient = 2 * math.pi * random.uniform(0,1)
                        swf = 14
                        stim.append(stimulus.stimulus('hawk', stim_aAge, hx, hy, hMaxSpeed, hOrient, hRefuge, lastKill, swf, eLevel, eMax))
                        n_hawk += 1

                    elif(stim[i].type == 'python' and stim[i].eLevel > .5 * eMax and random.uniform(0,1) > (n_python/expectedNumberOfEachPredator)):
                        px, py = getInitialPredatorLocations(pRefuge, width, height)
                        eLevel = eMax 
                        pMaxSpeed = .45 * rsm
                        pOrient = 2 * math.pi * random.uniform(0,1)
                        swf = 365
                        stim.append(stimulus.stimulus('python', stim_aAge, px, py, pMaxSpeed, pOrient, pRefuge, lastKill, swf, eLevel, eMax))
                        n_python += 1

            # to log data specific to each frame
            if len(objs)>0:
                tempData = [count, len(objs), n_leopard, n_hawk, n_python, len(stim), lDeath, hDeath, pDeath, prDeath, sDeath, totalFear/len(objs), totalHunger/len(objs), totalEnergy/len(objs)]
                simData.append(tempData)
            else:
                return simData

        count += 1

    # print("count=",count)

    return simData

def dist(x,y,sx,sy):
    return math.sqrt((x-sx)**2+(y-sy)**2)


def getInitialPredatorLocations(refugeLocations, width, height):
    # refugeLocations has [x,y,sizeX,sizeY] - coordinates(x,y); dimensions(sizeX,sizeY)
    x, y = random.uniform(0,1)*width, random.uniform(0,1)*height

    while(isInsideRefuge(x,y,refugeLocations)):
        x, y = random.uniform(0,1)*width, random.uniform(0,1)*height

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


def createResourceRefugePatch(k, patchDensity, refuge, patch, resourceRichness, width, height):
    tempX = width/(2*k)    # because 10% of total width is taken by control panel
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
        patch.append(resourcePatch.resourcePatch(patchX, patchY, patchPoints, tempX, tempY, resourceRichness))  
        i+=1

    return refuge, patch



     
def avoidRefugeLocations(avoidRefugeCode, refuge):
    refugeInfo = list()
    for i in range(len(refuge)):
        refugeCode = refuge[i][2]
        if(avoidRefugeCode == refugeCode):  # threat code is 1,2,3 while refugeCode is 0,1,2
            refugeInfo.append([refuge[i][0],refuge[i][1],refuge[i][3],refuge[i][4]])    # x,y coordinates and sizeX, sizeY

    return refugeInfo





def getParamRange():
    fps = [60]
    vervet_size = [9]
    simAreaParam = [1000]
    n_predator = [10]
    n_vervet = [300]
    radiusFOV = [50]
    angleFOV = [200]
    alarmPotency = [0,1,2]
    popGrowth = [1]
    scanFreq = [10]
    timeScale = [10000]
    spaceScale = [1]
    resourceGrowthRate = [3,6]
    return fps, simAreaParam, n_predator, n_vervet, vervet_size, radiusFOV, angleFOV, alarmPotency, popGrowth, scanFreq, timeScale, spaceScale, resourceGrowthRate
 
def getParamList(x):
    doneCount = 0
    params = []
    
    while doneCount<1000*len(x):
        simParam = []
        for i in range(len(x)):
            simParam.append(x[i][math.floor(random.uniform(0,len(x[i])))])
            i += 1
        params.append(simParam)
        doneCount += 1

    # remove duplicates
    paramList = []
    for i in params:
        if i not in paramList:
            paramList.append(i)

    print("total ", len(paramList), " input parameter sets to execute")
    return sorted(paramList, key=lambda x : x[7])

def saveSimData(simData, savePath): 
    Path(savePath).mkdir(parents=True, exist_ok=True)
    with open(savePath+"/simData.csv","w+", newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        header = ["Time Unit","Vervet Population","Leopard Population","Hawk Population","Python Population","Predator Population","Deaths due to Leopard","Deaths due to Hawk","Deaths due to Python","Total Predation Deaths","Starvation Deaths","Average Fear Level","Average Hunger Level","Average Energy Level"]
        writer.writerow(header)
        writer.writerows(simData)

def saveSimDetails(simParam, savePath):
    Path(savePath).mkdir(parents=True, exist_ok=True)
    with open(savePath+"/simParams.csv","w+", newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        header = ["fps", "simAreaParam", "n_predator", "n_vervet", "vervet_size", "radiusFOV", "angleFOV", "alarmPotency", "popGrowth", "scanFreq", "timeScale", "spaceScale", "resourceGrowthRate"]
        writer.writerow(header)
        writer.writerow(simParam)



def runMultipleSims():
    startTime = time.time()

    paramRange = getParamRange()

    paramList = getParamList(paramRange)
    

    print("Please enter number of generations to run the simulation for each condition: ")
    endSimGeneration = float(input())


    now = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')
    simSavePath = "./data/"+str(now)
    Path(simSavePath).mkdir(parents=True, exist_ok=True)

    for i in range(len(paramList)):
        oneGeneration = 10000
        endSimFrame = int(endSimGeneration * oneGeneration)

        print("no. of frames to run for this condition:", endSimFrame)
        simData = runSim(endSimFrame, paramList[i])
        savePath = simSavePath+"/sim"+str(i)+"Alarm"+str(paramList[i][7])
        saveSimDetails(paramList[i], savePath)
        saveSimData(simData, savePath)

    endTime = time.time()
    timeElapsed = endTime - startTime

    print("timeElapsed, runSpeed (iteration per second): ", timeElapsed, len(paramList)*endSimFrame/timeElapsed)


runMultipleSims()