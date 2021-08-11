import random
array = list()
for i in range(0,50):
    array.append(int(random.uniform(0,25)))
print(array)

i=0
while(i<len(array)):
    if(array[i]%2==0):    
        del array[i]
        i -= 1
    i+=1

print(array)