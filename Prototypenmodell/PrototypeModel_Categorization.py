#
# PrototypeModel_Categorization.py
#

import csv
import os
import glob
# https://docs.scipy.org/doc/numpy/reference/
import numpy as np
from math import *

amountNewObjects=4
amountFeatures=15
objects=np.zeros((amountNewObjects,amountFeatures))
countRow = 0

os.chdir("/Users/carole/Documents/Uni/Informatik_Master/Masterarbeit/Code/Prototypenmodell/csv")

# read data
def getData(arr, readFile):
    j=0
    #print("Read data")
    with open( readFile, 'rb') as csvFile:
        reader = csv.reader(csvFile, delimiter='\n')
        for row in reader:
            # use split so that it reads the values as
            # multiple ints in a row and not as an
            # invalid float value
            tmp=row[0].split(",")
            for h in range(len(tmp)):
                arr[j,h]=tmp[h]
            #print(arrayOSM[j,])
            j=j+1
    return(arr)

def getCategory(arr):
    m = np.amax(arr)
    # for i in arr:
    #     if(i == m):
    #         return arr.index(i)
    
    a = 1
    for element in arr:
        if(element == m):
            return a
        else:
            a = a + 1
    # return "Something is not quite right"
    return a

        
results=np.zeros((amountNewObjects,1))    
SimNewObjects=getData(objects,'measureOfSimilarities_new.csv') 
# print(SimNewObjects)

# print(SimNewObjects)

for i in range(amountNewObjects):
    results[i,0] = getCategory(SimNewObjects[i])
    
print(results)

with open('Categories_p.csv', 'wb') as f:
    writer = csv.writer(f)
    writer.writerows(results)

# 
# results[0,0] = 1
# results[0,1] = 1
# results[0,2] = 1


# print(getCategory(SimNewObjects[0]))


# with open('Categorisation', 'wb') as f:
#     writer = csv.writer(f)
#     writer.writerows(standardDeviations_All[:amountNewObjects])

