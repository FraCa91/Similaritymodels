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

#split the overallSimilarityArray with the correct order
def splitSimilarityArray(oaSimilarity):
    for i in oaSimilarity:
        simItems.append(i[0])
        simValue.append(i[1])

#find category of an item
def getItemCategory(itemNumber):
    groupNumber=1
    for i in groups_All:
        for u in i:
            if (u == int(itemNumber)):
                return groupNumber
        groupNumber += 1
    return "item not found"

#find the most probable category of the calculated similarityvalues
def categorizeItem(oaSimilarity):
    simItems = []
    simValue = []
    for i in oaSimilarity:
        simItems.append(i[1])
        simValue.append(i[0])
    # return simValue
    result =[]
    maxSimilarity = simValue[0]
    for i in range(len(simItems)):
        if(simValue[i] == maxSimilarity):
            result.append(getItemCategory(simItems[i]))
            # print getItemCategory(simItems[i])
    return np.argmax(np.bincount(result))
    # return result
 
# pretty arrayprinter           
def arrayprint(a):
    for i in a:
        print i
    
#generate sourcedata
    #groups of the known kitchenitems
groups =  'GroupsAll.csv'
groups_All=np.copy(getData(categories, groups))
    #all kitchenObjects
objects=np.zeros((amountObjects,amountFeatures))
kitchenObjects=np.copy(getData(objects,'kitchenObjects_study.csv'))
    #kitchenobjects to categorize
newObjects = np.zeros((amountNewObjects,amountFeatures))
kitchenObjects_new = np.copy(getData(newObjects, 'kitchenObjects_new.csv'))



#set the calculated results in place
counter = 0
categorizationNewObjects=np.zeros((amountNewObjects,1))
for h in kitchenObjects_new:
    categorizationNewObjects[counter,0]=categorizeItem(overallSimilarity(h))
    counter += 1
#write it in csv-file
with open('Categories_k.csv', 'wb') as f:
    writer = csv.writer(f)
    writer.writerows(categorizationNewObjects)
    




# print kitchenObjects[1]
# print histogram_intersection(kitchenObjects[1],kitchenObjects[2])
# arrayprint(overallSimilarity(kitchenObjects[7]))
# splitSimilarityArray(overallSimilarity(kitchenObjects[7]))
# print "--"
# print simItems
# print "--"
# print getItemCategory(134)
# arrayprint(overallSimilarity(kitchenObjects[7]))
# print "categorie: " + str(categorizeItem(overallSimilarity(kitchenObjects[7])))
# print categorizeItem(overallSimilarity(kitchenObjects[45]))



    
    
