* While there is no location in the vervets’ habitat where they can seek effective shelter from all three predator types, they seek out bushes to conceal themselves from hawks, trees to escape from leopards, and stoney ground to stay safe from snakes.
* Steering Behaviors For Autonomous Characters background and update by Craig Reynolds: http://www.red3d.com/cwr/steer/
* Schiffman's Video on 5.3 Flee, Pursue, Evade - The Nature of Code: https://www.youtube.com/watch?v=Q4MU7pkDYmQ
* https://en.wikipedia.org/wiki/Lotka%E2%80%93Volterra_equations
 '''
                if(first2See[i]==0 and alarmGap[i] == 0):
                    giveAlarm(self.xpos,self.ypos,alarm,awareRadius)
                    alarmGap[i] = 100 * nAgents
                    first2See[i] = 1 * nAgents

            else:   # if doesn't spots this predator, checks for it's alarm
                alarm = checkAlarmCall(self.xpos,self.ypos,type)
                # TBD: in case of multiple alarms chose closest
                if(alarm>0):
                    safeTime[index] = 100
                    v1,v2 = 2,2 # updates velocity in case of alarm

                else:
                    safeTime[index] = 0 # else ensures vervets don't move un-neccesarily

            alarmGap[i] -= 1
            first2See[i] -= 1
'''