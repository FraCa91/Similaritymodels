import csv
import os
import glob
import numpy as np
from math import *

# Initialisation (variables)
amountObjects=134
amountNewObjects=4
amountFeatures=7
amountGroups=29
sensitivity = 1 # sensitivity paramater for similarity-function
prototypes=np.chararray((amountObjects/4,amountFeatures))
prototypes=np.chararray(prototypes.shape, itemsize=200)
indexMaterial=6
categories=np.zeros((amountObjects/4,amountObjects/3))

#Activ Directory
os.chdir("/Users/carole/Documents/Uni/Informatik_Master/Masterarbeit/Code/Kernel/csv")

#kernel functuion (similarity function)-> becomes bigger with increasing similarity
#linear kernel
def linear(x,y):
    return np.dot(x,y)
#polynomial kernel
def polynomial(x,y,p=2):
    return (1+linear(x,y))**p
    
#histogram intersection kernel
#Alexander C. Berg, Jitendra Malik, "Classification using intersection kernel support vector machines is efficient" CVPR, 2008
def histogram_intersection(x,y):
    sum = 0
    for i in range(amountFeatures):
        feature = []
        feature.append(x[i])
        feature.append(y[i])
        sum = sum + min(feature)
    return sum
    

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

#calculate similarity of item to all the other kitchenObjects
def overallSimilarity(item):
    sims = []
    count = 0
    for i in kitchenObjects:
        # sims.append([round(linear(i,item)), str(count+1)])
        # sims.append([round(polynomial(i,item)), str(count+1)])
        sims.append([histogram_intersection(i,item), str(count+1)])
        count = count + 1
    return sorted(sims, key=lambda result: result[0], reverse=True)
    
    
objects=np.zeros((amountObjects,amountFeatures))
kitchenObjects=np.copy(getData(objects,'kitchenObjects_study.csv'))
    
clusterData = overallSimilarity(kitchenObjects[0])
# print clusterData
with open('similarity_k.csv', 'wb') as f:
    writer = csv.writer(f)
    writer.writerows(clusterData)
    
