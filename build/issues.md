* agents moving automatically at start of simulation
* agents behaving strangely when in hideout with 2 predators with one corresponding to the hideout. 
* safetime not activated when agent is in hideout.
* predators appearing in their refuge at start
* agents escaping environment never to come back
* some agents mysteriously develop show fear suddenly after foraging
* agents show signs of foraging even when hunger < fear TBV

------------------------------------------------
# Properly implementing non-differentiable alarm calls.
# initially random eLevel
# mystery alarmed agents at random location mostly just after alarm call in somewhere else
# abandon nextAlarm as there is already periodic scanning
# agent / predator reproduction: to make only fit ones duplicate
# Implementing the periodic scan feature of agents.
* Logging cumulative distance traveled by each agent over time.
# Having a toggle button to skip data logging or to only log data.
* To discuss tuning all the parameters to a reasonable value. I will make a list of all the crucial parameters that decide the fate of the simulation.
# Having a monkey-type outline of the agent instead of the currently shown insect-like look.
# Letting agents move as per the resultant velocity while they see a predator, resulting from avoiding the predator and fleeing to the refuge.
* first2See is buggy
* when last vervet dies: ZeroDivisionError: integer division or modulo by zero at 348:0 in run.py
# when stimuli die: IndexError: index out of range: 0 at 339:0 in vehicle.py

* IndexError: index out of range: 0 at 339:0 in vehicle.py
* TypeError: cos(): 1st arg can't be coerced to double at 237:0 in vehicle.py

* Develop a data logging system that saves simulation data in batches with varying conditions, i.e., simulation parameters.
* Draw plots from these data and draw the appropriate conclusions.

