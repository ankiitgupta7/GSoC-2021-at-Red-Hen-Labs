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
    global cp5, n, d, r, stim, objs, patch, start, img1, img2, img3
    global fov, toggleAlarm, safeTime, startOfSim, popGrowth, scanFreq, showSim
    global lh, hh, ph, lhx, lhy, hhx, hhy, phx, phy, hideout
    global noAlarmStarveDeath, noAlarmPredationDeaths, noAlarmTotalDeath, noAlarmAvgs, noAlarmPopulation
    global diffAlarmStarveDeath, diffAlarmPredationDeaths, diffAlarmTotalDeath, diffAlarmAvgs, diffAlarmPopulation
    global sDeath, prDeath, lDeath, hDeath, pDeath, deathLocation
    
    showSim = 1
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

        #option = "Moving","Fixed"
        #cp5.addScrollableList("Opt for Stimuli Motion").setPosition(.9*width, 5).setSize(100, 50).setBarHeight(10).setItemHeight(10).addItems(option)
        #cp5.get(ScrollableList, "Opt for Stimuli Motion").setType(ControlP5.LIST)

        pToggle = cp5.addSlider("Reproduction")
        pToggle.setPosition(.9*width,10).setSize(30,10).setRange(0, 1).setValue(1).setNumberOfTickMarks(2).setSliderMode(Slider.FLEXIBLE)
        
        pToggle = cp5.addSlider("Scan Freq")
        pToggle.setPosition(.9*width,35).setSize(80,10).setRange(10, 100).setValue(30).setNumberOfTickMarks(10).setSliderMode(Slider.FLEXIBLE)
        
        textSize(10)
        text("Choose No. of Stimulus", .9*width, 75)

        p1 = cp5.addSlider("leopard")
        p1.setPosition(.9*width,80).setSize(80,15).setRange(0, 9).setValue(1).setNumberOfTickMarks(10).setSliderMode(Slider.FLEXIBLE)

        p2 = cp5.addSlider("hawk")
        p2.setPosition(.9*width,120).setSize(80,15).setRange(0, 9).setValue(1).setNumberOfTickMarks(10).setSliderMode(Slider.FLEXIBLE)

        p3 = cp5.addSlider("python")
        p3.setPosition(.9*width,160).setSize(80,15).setRange(0, 9).setValue(1).setNumberOfTickMarks(10).setSliderMode(Slider.FLEXIBLE)



        aToggle = cp5.addSlider("Toggle Alarms")
        aToggle.setPosition(.9*width,250).setSize(60,15).setRange(0, 2).setValue(2).setNumberOfTickMarks(3).setSliderMode(Slider.FLEXIBLE)

        
        pRatio = cp5.addSlider("Patch Ratio")
        pRatio.setPosition(.9*width,300).setSize(60,15).setRange(2, 20).setValue(12).setNumberOfTickMarks(10).setSliderMode(Slider.FLEXIBLE)


        pDensity = cp5.addSlider("Patch Density")
        pDensity.setPosition(.9*width,330).setSize(60,15).setRange(.1, 1.0).setValue(.6).setNumberOfTickMarks(10).setSliderMode(Slider.FLEXIBLE)


        nAgent = cp5.addSlider("Agents")
        nAgent.setPosition(.9*width,400).setSize(100,15).setRange(50, 5000).setValue(200).setNumberOfTickMarks(100).setSliderMode(Slider.FLEXIBLE)

        
        scale = cp5.addSlider("scale")
        scale.setPosition(.9*width,430).setSize(80,15).setRange(3, 30).setValue(9).setNumberOfTickMarks(10).setSliderMode(Slider.FLEXIBLE)

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
        n1 = int(cp5.getController("leopard").getValue())
        n2 = int(cp5.getController("hawk").getValue())
        n3 = int(cp5.getController("python").getValue())
        n = int(cp5.getController("Agents").getValue())
        d = int(cp5.getController("scale").getValue())  # accessing vehicle scale parameter
        r = int(cp5.getController("r of FoV").getValue())
        fov = int(cp5.getController("FoV Angle").getValue())
        toggleAlarm = cp5.getController("Toggle Alarms").getValue()
        popGrowth = int(cp5.getController("Reproduction").getValue())
        scanFreq = int(cp5.getController("Scan Freq").getValue())

        if(toggleAlarm==0):
            noAlarmStarveDeath = createWriter(dataDirectory + "/noAlarmStarveDeath.csv")   # to write the output file

            noAlarmPredationDeaths = createWriter(dataDirectory + "/noAlarmPredationDeaths.csv")   # to write the output file
            noAlarmPredationDeaths.print("Time Unit")
            noAlarmPredationDeaths.print(",")
            noAlarmPredationDeaths.print("Leopard Deaths")
            noAlarmPredationDeaths.print(",")
            noAlarmPredationDeaths.print("Hawk Deaths")
            noAlarmPredationDeaths.print(",")
            noAlarmPredationDeaths.print("Python Deaths")
            noAlarmPredationDeaths.print(",")
            noAlarmPredationDeaths.print("Total Predation Deaths")
            noAlarmPredationDeaths.print("\n")

            noAlarmTotalDeath = createWriter(dataDirectory + "/noAlarmTotalDeath.csv")   # to write the output file

            noAlarmAvgs = createWriter(dataDirectory + "/noAlarmAvgs.csv")   # to write the average values
            noAlarmAvgs.print("Time Unit")
            noAlarmAvgs.print(",")
            noAlarmAvgs.print("Average Fear Level")
            noAlarmAvgs.print(",")
            noAlarmAvgs.print("Average Hunger Level")
            noAlarmAvgs.print(",")
            noAlarmAvgs.print("Average Energy Level")
            noAlarmAvgs.print("\n")

            noAlarmPopulation = createWriter(dataDirectory + "/noAlarmPopulation.csv")   # to write the output file
            noAlarmPopulation.print("Time Unit")
            noAlarmPopulation.print(",")
            noAlarmPopulation.print("Vervet Population")
            noAlarmPopulation.print(",")
            noAlarmPopulation.print("Predator Population")
            noAlarmPopulation.print("\n")

        elif(toggleAlarm==2):
            diffAlarmStarveDeath = createWriter(dataDirectory + "/diffAlarmStarveDeath.csv")   # to write the output file
            diffAlarmPredationDeaths = createWriter(dataDirectory + "/diffAlarmPredationDeaths.csv")   # to write the output file
            diffAlarmPredationDeaths.print("Time Unit")
            diffAlarmPredationDeaths.print(",")
            diffAlarmPredationDeaths.print("Leopard Deaths")
            diffAlarmPredationDeaths.print(",")
            diffAlarmPredationDeaths.print("Hawk Deaths")
            diffAlarmPredationDeaths.print(",")
            diffAlarmPredationDeaths.print("Python Deaths")
            diffAlarmPredationDeaths.print(",")
            diffAlarmPredationDeaths.print("Total Predation Deaths")
            diffAlarmPredationDeaths.print("\n")

            diffAlarmTotalDeath = createWriter(dataDirectory + "/diffAlarmTotalDeath.csv")   # to write the output file

            diffAlarmAvgs = createWriter(dataDirectory + "/diffAlarmAvgs.csv")   # to write the average values
            diffAlarmAvgs.print("Time Unit")
            diffAlarmAvgs.print(",")
            diffAlarmAvgs.print("Average Fear Level")
            diffAlarmAvgs.print(",")
            diffAlarmAvgs.print("Average Hunger Level")
            diffAlarmAvgs.print(",")
            diffAlarmAvgs.print("Average Energy Level")
            diffAlarmAvgs.print("\n")

            diffAlarmPopulation = createWriter(dataDirectory + "/diffAlarmPopulation.csv")   # to write the output file
            diffAlarmPopulation.print("Time Unit")
            diffAlarmPopulation.print(",")
            diffAlarmPopulation.print("Vervet Population")
            diffAlarmPopulation.print(",")
            diffAlarmPopulation.print("Predator Population")
            diffAlarmPopulation.print("\n")

        sDeath, prDeath, lDeath, hDeath, pDeath = 0, 0, 0, 0, 0
        safeTime = []
        for i in range(100*n):   # if agent population crosses 10*n, an error would pop
            safeTime.append([0,0]) # first value is safeTime value, second is alarm type
            
        for i in range(n1):
            # img, type, x, y, xspeed, yspeed, hl, nextAlarm, lastKill, eLevel
            stim.append(stimulus.stimulus(img1, 'leopard', .9*width/2, D/2, random.uniform(-3,3), random.uniform(-3,3), lh, 0, 1000, 5000))   # lh: leopard refuge

        for i in range(n2):
            stim.append(stimulus.stimulus(img2, 'hawk', .9*width/2, D/2, random.uniform(-4,4), random.uniform(-4,4), hh, 0, 1000, 5000))

        for i in range(n3):
            stim.append(stimulus.stimulus(img3, 'python', .9*width/2, D/2, random.uniform(-1.5,1.5), random.uniform(-1.5,1.5), ph, 0, 1000, 5000))


# creating resource patches in the environment
        patch = list() 
        k = int(cp5.getController("Patch Ratio").getValue())   # decides how densely the patchPoints (resource points - yellow dots) are arranged; also decides how big or small the patch size is
        patchDensity = cp5.getController("Patch Density").getValue()   # decides how densely (0,1) the patches (the squares) are arranged
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
        for i in range(n):
            eLevel = 1000 * random.uniform(0,1) # assigning initial energy level to be a random between 0-1000
            alpha = 2 * math.pi * random.uniform(0,1)
            objs.append(vehicle.vehicle(random.uniform(0,.9*width), random.uniform(0,D), d, stim, alpha, eLevel, 0, [0,0], patch))

        start = 1
        startOfSim = frameCount
        saveSimulationParameters(n, n1, n2, n3, r, fov, k, patchDensity, d)
        deathLocation = []

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

        # processing predators
        i=0
        while(i<len(stim)):
            if(stim[i].eLevel<100 and len(stim)>0):  # death by starvation
                del stim[i]
                i -= 1
            else:
                stim[i].move()
                if(showSim == 1):
                    stim[i].display()
            i += 1

        # processing patches
        for i in range(len(patch)):
            # display each resource patch
            patch[i].display()

        # processing vervets
        i = 0
        totalFear = 0
        totalHunger = 0
        totalEnergy = 0
        
        first2See = []
        for i in range(0,len(stim)):
            first2See.append(0)

        while(i<len(objs)):
            # processing display and movement of vervets
            if(objs[i].eLevel<10 and len(objs)>1):  # death by starvation
                deathLocation.append([objs[i].xpos,objs[i].ypos,0,1])
                if(toggleAlarm==0):
                    sDeath += 1
                    tempData = [sDeath]
                    logData(noAlarmStarveDeath,startOfSim,tempData)
                elif(toggleAlarm==2):
                    sDeath += 1
                    tempData = [sDeath]
                    logData(diffAlarmStarveDeath,startOfSim,tempData)

                del objs[i]
                del safeTime[i]
                i -= 1

            elif(objs[i].rfd[0] == 1 and len(objs)>1): # death by predation
                deathLocation.append([objs[i].xpos,objs[i].ypos,0,2])
                if(toggleAlarm==0 and objs[i].rfd[1]==1):
                    lDeath += 1
                elif(toggleAlarm==2 and objs[i].rfd[1]==1):
                    lDeath += 1

                if(toggleAlarm==0 and objs[i].rfd[1]==2):
                    hDeath += 1
                elif(toggleAlarm==2 and objs[i].rfd[1]==2):
                    hDeath += 1

                if(toggleAlarm==0 and objs[i].rfd[1]==3):
                    pDeath += 1
                elif(toggleAlarm==2 and objs[i].rfd[1]==3):
                    pDeath += 1

                if(toggleAlarm==0):
                    prDeath += 1
                elif(toggleAlarm==2):
                    prDeath += 1

                tempData = [lDeath, hDeath, pDeath, prDeath]
                if(toggleAlarm == 0):
                    logData(noAlarmPredationDeaths,startOfSim,tempData)
                elif(toggleAlarm == 2):
                    logData(diffAlarmPredationDeaths,startOfSim,tempData)

                del objs[i]
                del safeTime[i]
                i -= 1
            else:
                objs[i].move(r, fov, i, hideout, len(objs), toggleAlarm, safeTime, first2See, frameCount - startOfSim + 1, scanFreq)  
                
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
                if(stim[i].type == 'leopard' and stim[i].eLevel > 3000):
                    stim.append(stimulus.stimulus(img1, 'leopard', .9*width/2, D/2, random.uniform(-3,3), random.uniform(-3,3), lh, 0, 1000, 5000))   # lh: leopard refuge

                elif(stim[i].type == 'hawk' and stim[i].eLevel > 3000):
                    stim.append(stimulus.stimulus(img2, 'hawk', .9*width/2, D/2, random.uniform(-4,4), random.uniform(-4,4), hh, 0, 1000, 5000))

                elif(stim[i].type == 'python' and stim[i].eLevel > 3000):
                    stim.append(stimulus.stimulus(img3, 'python', .9*width/2, D/2, random.uniform(-1.5,1.5), random.uniform(-1.5,1.5), ph, 0, 1000, 5000))

        # represeting death
        x = 0
        while(x<len(deathLocation)):      
            if(deathLocation[x][2]<20):    # represents recent death for 20 frames
                deathLocation[x][2] += 1
                if(deathLocation[x][3]==1):    # death by starvation
                    fill(0)
                    square(deathLocation[x][0]-10,deathLocation[x][1]-10,20)
                elif(deathLocation[x][3]==2):  # death by predation
                    fill(0)
                    circle(deathLocation[x][0],deathLocation[x][1],20)
            else:
                del deathLocation[x]
                x -= 1
            x += 1


        # to log total cumulative death per frame
        if(toggleAlarm==0):
            tempData = [prDeath + sDeath]
            logData(noAlarmTotalDeath, startOfSim, tempData)

            tempData = [len(objs),len(stim)]
            logData(noAlarmPopulation, startOfSim, tempData)

            tempData = [totalFear/len(objs),totalHunger/len(objs),totalEnergy/len(objs)]
            logData(noAlarmAvgs, startOfSim, tempData)
        elif(toggleAlarm==2):
            tempData = [prDeath + sDeath]
            logData(diffAlarmTotalDeath, startOfSim, tempData)

            tempData = [len(objs),len(stim)]
            logData(diffAlarmPopulation, startOfSim, tempData)

            tempData = [totalFear/len(objs),totalHunger/len(objs),totalEnergy/len(objs)]
            logData(diffAlarmAvgs, startOfSim, tempData)

        if((frameCount-startOfSim+1) == 5000 and toggleAlarm == 0):
            closeOutputFiles(noAlarmStarveDeath, noAlarmPredationDeaths, noAlarmTotalDeath, noAlarmAvgs, noAlarmPopulation)
            #exit()
            print("Data has been saved for 5000 frames.")
        elif((frameCount-startOfSim+1 == 5000) and toggleAlarm == 2):
            closeOutputFiles(diffAlarmStarveDeath, diffAlarmPredationDeaths, diffAlarmTotalDeath, diffAlarmAvgs, diffAlarmPopulation)
            #exit()
            print("Data has been saved for 5000 frames.")

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

def logData(output, startOfSim, data):
    output.print(frameCount-startOfSim+1)
    for i in range(len(data)):
        output.print(",")
        output.print(data[i]) # Write the datum to the file
    output.print("\n") 

def closeOutputFiles(f1,f2,f3,f4,f5):
    f1.flush()  # Writes the remaining data to the file
    f1.close()  # Finishes the file
    f2.flush()
    f2.close()
    f3.flush()
    f3.close()
    f4.flush()
    f4.close()
    f5.flush()
    f5.close()