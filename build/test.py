import random

'''
while(1):
    x+=1
    if(x>66):
        break
    elif(x%5 == 0):
        if(x%10==0):
            continue
  
    print(x," ")

###

x = [[0]*3]*1
y = 1,2,4
x.append(y)
print(x)


'''

x = [(0,0,0)]

def A():
    global x
    y = 1,2,4
    z = 1,3,5
    x.append((1,2,4))
    x.append(z)
   # x = 3,3,4
def B():
    print x

def C():
    A()
    B()

C()










