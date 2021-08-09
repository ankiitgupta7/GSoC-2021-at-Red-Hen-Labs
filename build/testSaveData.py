import random
# Create a file in the sketch directory
output = createWriter("testData.csv")
numbers = []
for i in range(1000):
    numbers.append(random.uniform(0,1))
for i in range(len(numbers)):
    output.print(i+1)
    output.print(",")
    output.print(numbers[i]) # Write the datum to the file
    output.print("\n")

output.flush()# Writes the remaining data to the file
output.close()# Finishes the file
exit()# Stops the program