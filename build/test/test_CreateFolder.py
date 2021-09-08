# Python program to explain os.mkdir() method

# taken from https://www.geeksforgeeks.org/create-a-directory-in-python/
  
# importing os module
import os

	
dd = day()  # Values from 1 - 31
mm = month()  # Values from 1 - 12
yyyy = year()  # 2003, 2004, 2005, etc.
HH = hour()
MM = minute()

timeStamp = str(dd) + "-" + str(mm) + "-" + str(yyyy) + " " + str(HH) + "-" + str(MM)
print(timeStamp)

  
# Directory
directory = timeStamp

# Parent Directory path
parent_dir = "./data"

# Path
path = os.path.join(parent_dir, directory)
  
# Create the directory
# 'GeeksForGeeks' in
# '/home / User / Documents'
os.mkdir(path)
simParam = createWriter(path+"/simParameters.txt")
simParam.print("Total number of Vervets = ")
simParam.flush()
simParam.close()    
print("Directory '% s' created" % directory)