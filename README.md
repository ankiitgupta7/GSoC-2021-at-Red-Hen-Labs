# Google Summer of Code 2021 & 2022 at Red Hen Labs

This is repository for the project proposal accepted at Google Summer of Code 2021 & being continued in 2022 at Red Hen Labs. The project summary can be found [here](https://summerofcode.withgoogle.com/programs/2022/projects/3gJf6UQy) at the official GSoC website. 


# Simulation Details

**Environment Summary &amp; Actions**

- **All Time Constants**
  - Refuge Area / Hideouts

    - Circular areas at the corner of the environment colored differently refer to refuge areas for agents (preys) where they are safe from a specific type of predator depending on the color of the refuge area as that predator can not enter the corresponding refuge area.
    - location of the refuge area is partially randomly generated.

  - The control panel
    - Reproduction: to toggle between reproduction feature in agents and predators
    - Scan Frequency: frequency at which agents visually scan the environment
    - No. of stimuli: choosing the number of specific predators at start of simulation
    - Toggle Alarm
      - 0: no alarm call
      - 1: indifferentiable alarm call
      - 2: differentiable (representative) alarm call
    - Patch Ratio: decides how densely the patchPoints (resource points - yellow dots) are arranged; also decides how big or small the patch size is
    - Patch Density: decides how densely (0,1) the patches (squares) are arranged
    - Agents: number of agents at start of simulation
    - Scale: decides the relative size of agents
    - R of FOV: refers to the visual awareness radius of agents in their field of view
    - Angle of FOV: refers to the visual awareness scope of agents, e.g., primates having forward-facing eyes generally have a field of view of 200 degrees.
- **At start of simulation**
  - A specified number (as in the control panel) of randomly oriented agents, at random energy levels, appear at random places within the environment.
  - A specified number of predators appear, initially with certain energy level at the center of the environment moving randomly
  - Resource points with randomly generated resource level appear in patches
- **Movement/Action rules for Agents/Predators**
  - Predators: move at certain randomly generated speed components within a certain range specific to that type of predator
  - Agents:
    - Default action of agents is to move towards the nearest resource area and forage to maximize their energy levels.
    - In case they encounter a predator or become aware of it through alarm calls - a certain fear level is aroused in them which diminishes with time
      - if they are more in fear than hunger (fLevel > hLevel) they move to the refuge area where they are safe from predators. And vice versa.
      - if they are visually aware of a predator they avoid it (modeled using cowardness behavior of Braitenberg Vehicles)
- **As a result of reproduction**
  - After a certain number of frames agents and predators duplicate
  - Agents
    - duplicate 50% of the time if they have more than half the energy level of their maximum capacity
    - new agents have random energy level to start with and zero fear level
    - they appear at random spots within the environment
    - these new agents can be thought to be taken in consideration after they become adult and hence appear at random spots with random energy level
  - Predators
    - duplicate if their energy level is more than 30% of their maximum capacity
    - new predators appear at the center of the environment
    - they have half the energy level of their maximum capacity

- **Ending simulation &amp; Data Saving**
  - Depending on the state of toggle alarm simulation data is saved specific to the state of 'toggle alarm'

**Display Features of Agents/Predators/ResourcePoints**

- Agents
  - If agents are gray, they are whiter if they have more eLevel &amp; vice versa. It also means they are more in _hunger_ than _fear_ (fLevel < hLevel).
  - If they are colored red/green/blue, it means their fLevel>hLevel as they are aware of the python/hawk/leopard predator. They are brighter if the fLevel is higher and vice versa.
  - In case of death by predation - a black circular spot is displayed on the death spot for some time. In case of death by starvation (running out of eLevel) - a square spot is displayed for a while at the death spot.
  - If the agent makes an alarm call (auditory), a circular ring of a certain radius appears briefly corrending to equivalent color code for a specific predator. All agents within this circle become aware of a predator nearby as a result of this.
- Predators
  - An image is displayed corresponding to each predator representing its location.
  - It has a colored outline too, representing its energy level, the brighter outline indicates higher energy level.
- Resource Points
  - Within each resource patch (square) there are several resource points represented by tiny yellow dots. Brighter dots indicate a higher resource level of resource points within that particular patch and vice versa.
  - Note that resource points become darker as agent forage leading to decrease in the resource levels in the resource patches.
  - There is a natural recharge mechanism of resource points as the resource level increases with time.

**Parameter Documentation**

- Certain number of agents (preys) appear
  - with parameters (xpos, ypos, z, stim, alpha, eLevel, fLevel, rfd, patch);
  - _( __xpos, ypos__ )_: randomly generated coordinates within the environment where the agents appear initially
  - _z_: proportionate scale(size) of agent displayed
  - _stim_: feeding the stimulus (predator) information to the agent (prey)
  - _alpha_: initially randomly generated initial orientation (direction of vision) of agent
  - _ __eLevel__ _: energy level of agents that keeps them alive; randomly assigned eLevel between (0-1000); decays over time depending on their movement; recharged by foraging
  - _fLevel_: fear level of agents due to predators that decides if they would forage food or flee to hideout; initially assigned zero; updates as agents become aware of predators
  - _rfd_: ready for death parameter, keeps track if agent is predated
  - _patch_: feeding details about each resource patch in the environment

- Certain number stimuli (predators) appear
  - with parameters(img, type, x, y, xspeed, yspeed, hl, nextAlarm, lastKill, eLevel)
  - _ __img__ :_ image of predator
  - _type_: if the predator is leopard, hawk, or python
  - _( __x, y__ )_: initial coordinates of predators they appear initially set at center of environment
  - _( __xspeed, yspeed__ )_: randomly generated speed components within a certain range specific to type of predator
  - _ __hl__ _: hideout location for agents corresponding to this specific type of predator (randomly generated fixed locations in different parts of environment)
  - _ __nextAlarm__ _: gives information about no. of frames after which an alarm is given for this predator if it remains visible (as alarms are periodic)
  - _ __lastKill__ _: keeping track of the last successful kill by this specific predator (as it won't kill again for certain duration)
  - _eLevel_: energy level of stimuli that keeps them alive; initially assigned to be 5000; decays over time depending on their movement; recharged with every predation

- A pattern of resource distribution appears
  - with parameters (patchX, patchY, patchPoints, tempX, tempY)
  - (_patchX, patchY_): center of a square patch; depends on Patch Ratioand Patch Density
  - _patchPoints_: contains information about location (x,y) and resource level (rLevel) of each resource point within a patch
  - (_tempX, tempY_): decides dimensions of entire resource patch area

**Glossary**

- **eLevel:** energy level of agents that keeps them alive
- **hLevel:** 1000 - eLevel
- **fLevel:** fear level due to a predator; decreases with time and no further exposure; gets updates on new encounter
- **rLevel**
- **Patch Density** (patchDensity): decides how densely (0,1) the patches (the squares) are arranged
- **Patch Ratio** (k): decides how densely the patchPoints (resource points - yellow dots) are arranged; also decides how big or small the patch size is


# Vervet Action Flowchart
![alt text](https://github.com/ankiitgupta7/Google-Summer-of-Code-at-Red-Hen-Labs/blob/master/Images/simFlow.png?raw=true "Vervet Action Flowchart")