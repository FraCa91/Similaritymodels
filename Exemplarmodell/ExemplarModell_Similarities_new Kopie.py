#
# PrototypeModel_Similarities.py
#

import csv
import os
import glob
# https://docs.scipy.org/doc/numpy/reference/
import numpy as np
from math import *


# Initialisation (variables)
amountObjects=134
amountNewObjects=4
amountFeatures=7
amountGroups=29
# sensitivity paramater for similarity-function
sensitivity = 1
prototypes=np.chararray((amountObjects/4,amountFeatures))
prototypes=np.chararray(prototypes.shape, itemsize=200)
indexMaterial=6
categories=np.zeros((amountObjects/4,amountObjects/3))
weights=np.zeros((amountFeatures,1))
#weights[:]=1.0/7.0 # ->gleichverteilte Gewichte
#weights[:]=1.0 #-> so hat Alisa die Weights gesetzt
weights=[0.1,0.1,0.1,0.1,0.1,0.1,0.4]

#Activ Directory
os.chdir("/Users/carole/Documents/Uni/Informatik_Master/Masterarbeit/Code/Exemplarmodell/csv")

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

#generate sourcedata
    #groups of the known kitchenitems
groups =  'GroupsAll.csv'
groups_All=np.copy(getData(categories, groups))
    #kitchenobjects to categorize
newObjects = np.zeros((amountNewObjects,amountFeatures))
kitchenObjects_new = np.copy(getData(newObjects, 'kitchenObjects_new.csv'))
    #all kitchenObjects
objects=np.zeros((amountObjects,amountFeatures))
kitchenObjects=np.copy(getData(objects,'kitchenObjects_study.csv'))

#kitchenObjects_new=np.zeros((amountNewObjects,amountFeatures))
# kitchenObjects_new=np.copy(getData(newObjects,'kitchenObjects_new.csv'))


# calculate distance between item i and exemplar j
# ref: Nosofsky (2)

def distance(item,exemplar):
    res = 0
    items = np.zeros((amountFeatures,1))
    items = item
    exemplars = np.zeros((amountFeatures,1))
    exemplars = exemplar
    for x in range(amountFeatures):
        res = res + weights[x] * pow(fabs(items[x] - exemplars[x]),2)
    return sqrt(res)
    
# calculate similarity from distance of item i and exemplar j
# ref: Nosofsky (3)
def similarity(distance):
    return exp((-1) * sensitivity * distance)
    
#get all items by categorynumber
def getCategory(number):
    items = np.zeros((33,1))
    items = groups_All[number]
    newItems= []
    for i in items:
        if i != 0.:
            newItems.append(int(i))
    return newItems
# print getCategory(1)

#calculate similarity of a category by an item
def catSimilarity(catNumber,item):
     exemplars = np.zeros((33,1))
     exemplars = getCategory(catNumber)
     sim = 0
     for i in exemplars:
         sim = sim + similarity(distance(item,kitchenObjects[int(i)-1]))
         
     return sim
     
# print catSimilarity(0,kitchenObjects[7])
# print "----------------"
# print weights
# print kitchenObjects[7]
# print kitchenObjects[50]
# print similarity(distance(kitchenObjects[32],kitchenObjects[7]))
     
# print catSimilarity(8,kitchenObjects[7])
# print similarity(distance(kitchenObjects[7],kitchenObjects[51]))
    
# cat1 = getCategory(0)
# print cat1[2]
    
# print similarity(distance(kitchenObjects[1],kitchenObjects[7]))

#calculate similarity of all groups by an item
def overAllSimilarity(item):
    result = 0
    for t in range(amountGroups):
        # print catSimilarity(t,item)
        result = result + catSimilarity(t,item)
    return result

# print overAllSimilarity(kitchenObjects[7])
# print catSimilarity(0,kitchenObjects[7])
# print catSimilarity(1,kitchenObjects[7])
# print catSimilarity(2,kitchenObjects[7])
# print catSimilarity(4,kitchenObjects[7])
# print catSimilarity(5,kitchenObjects[7])
# print catSimilarity(3,kitchenObjects[7])

#get the category of an item
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
    
#calculate the probability of an item
def belongingProbabilities(item):
    overallSim = overAllSimilarity(item)
    probs = np.zeros((amountGroups))
    for u in range(amountGroups):
        probs[u] = catSimilarity(u,item) / overallSim
    return probs
 
 
#data for usertests
def usertest(item):
    result = []
    count = 0
    # for c in range(amountGroups):
    #     count = 0
    #     for i in c:
    #         dist = distance(item,i)
    #         entry = str(c) + '/' + str(count)
    #         result.append([distance(item,i), ])
    for i in kitchenObjects:
        sim = similarity(distance(item, i))
        result.append([sim, 'item: ' + str(count)])
        count = count + 1
    return sorted(result, key=lambda result: result[0])

 
#calculate the probability of all new items
probNewObjects = []
for r in kitchenObjects_new:
    # print r
    # print '--'
    # print belongingProbabilities(r)
    # print '--'
    probNewObjects.append(belongingProbabilities(r))
    
# print probNewObjects
# print probNewObjects

categorizationNewObjects = []
for h in probNewObjects:
    categorizationNewObjects.append(getCategory(h))
    
# print categorizationNewObjects

results=np.zeros((amountNewObjects,1))

counter = 0
for y in categorizationNewObjects:
    results[counter,0] = y
    counter = counter + 1
    
print usertest(kitchenObjects[132])
 
 
with open('Categories_e.csv', 'wb') as f:
    writer = csv.writer(f)
    writer.writerows(results)
 
# measureOfSimilarities_All=np.copy(measureOfSimilarities(psychologicalDistances_All))
#
# results=np.zeros((amountNewObjects,1))
# SimNewObjects=getData(objects,'measureOfSimilarities_new.csv')
# # print(SimNewObjects)
#
# print(SimNewObjects)
#
# for i in range(amountNewObjects):
#     results[i,0] = getCategory(SimNewObjects[i])
#
# print(results)
#
# with open('Categories.csv', 'wb') as f:
#     writer = csv.writer(f)
#     writer.writerows(results)
# print getCategory(belongingProbabilities(kitchenObjects[132]))
