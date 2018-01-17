import csv
import os
import glob
import numpy as np
from math import *
from random import randint

# a = [3,1,1,3,3,5,7,8]
# a = [[319,"Teller"], [935,"Teller"], [738,"Teller"], [348,"Teller"], [619,"Teller"]]


def randomArray(size):
    result = []
    for i in range(size):
        result.append([randint(0,1000),"Teller"])
    return result
a = randomArray(134)

# def greatestDist(arr):
#     maxDist=0
#     maxDistPos=0
#     for i in range(len(arr)):
#         if (i!=0):
#             if(abs(arr[i-1]-arr[i])>maxDist):
#                 maxDist=abs(arr[i-1]-arr[i])
#                 maxDistPos =i
#     return [maxDist,maxDistPos]
#
# # greatestDist(a)
#
# def cluster(arr,clusters):
#     result =[arr]
#     maxDist=0
#     segment=0
#     lastCut=0
#     partArray=[]
#     buffer=[]
#     for i in range(clusters-1):
#         # buffer=greatestDist(result[i])
#         # print arr[:buffer[1]]
#         # print arr[buffer[1]:]
#         for u in range(len(result)):
#             if(range(len(result[u])))>1:
#                 buffer=greatestDist(result[u])
#                 if(maxDist<buffer[0]):
#                     maxDist=buffer[0]
#                     segment=u
#     # print segment
#     # print buffer[1]
#     # print result[segment][:buffer[1]]
#         partArray=result[segment]
#         result[segment] = result[segment][:buffer[1]]
#         result.append(partArray[buffer[1]:])
#     return result
#
#
#
# print cluster(a,4)




def generateDistanceArray(arr):
    workArray = sorted(arr, key=lambda arr: arr[0])
    # print workArray
    result=[]
    for i in range(len(workArray)):
        if (i==0):
            result.append(i)
        else:
            result.append(abs(workArray[i][0]-workArray[i-1][0]))
    return result
    
# sorted(result, key=lambda result: result[0])

def splitDistanceArray(distArr):
    result=[]
    for i in range(len(distArr)):
        result.append([distArr[i],i])
    return sorted(result, key=lambda result: result[0], reverse=True)

def countDistanceAmount(distArr):
    result = 0
    for i in distArr:
        if (i[0] != 0):
            result += 1
    return result

def clusterArray(arr,distArr,cluster):
    workArray = sorted(arr, key=lambda arr: arr[0])
    buffer = workArray
    # print "arrayw:"
    # print workArray
    # print "distance:"
    # print distArr
    # print "cluster"
    # print cluster
    if (cluster == 0):
        print "seriously?"
    elif (cluster == 1):
        return workArray
    elif (cluster > len(workArray)):
        return "ERROR: Too many clusters"
    elif (countDistanceAmount(distArr)+1 < cluster):
        print "WARNING: Spillover of clusters. Editing Cluster Parameter to " +str(countDistanceAmount(distArr)+1)
        return clusterArrayProcedure(workArray,distArr,countDistanceAmount(distArr)+1)
    else:
        return clusterArrayProcedure(workArray,distArr,cluster)
        # if (i == 0):
        #     result.append(arr[i])
        # return result

def clusterArrayProcedure(arr,distArr,cluster):
    result = []
    breaks = []
    for u in range(cluster-1):
        if (distArr[u][1] == 0):
            breaks.append(distArr[u+1])
        else:
            breaks.append(distArr[u])
    breaks = sorted(breaks, key=lambda breaks: breaks[1])
    # print "breaks: "
    # print breaks
    for t in range(cluster):
        if (t == 0):
            result.append(arr[:breaks[t][1]])
        elif (t == (cluster - 1)):
            # result.append(arr[len(arr)-breaks[t-1][1]:])
            result.append(arr[breaks[t-1][1]:])
        else:
            result.append(arr[breaks[t-1][1]:breaks[t][1]])
    # print "result: "
    return result
    

# print a
# print generateDistanceArray(a)


# print splitDistanceArray(generateDistanceArray(a))
# clusterArray(5)
# print sorted(a, key=lambda a: a)
distanceArray = splitDistanceArray(generateDistanceArray(a))
# print distanceArray
# print splitDistanceArray(generateDistanceArray(a))
printcluster = clusterArray(a,distanceArray,23)
for i in printcluster:
    print i
# print countDistanceAmount(distanceArray)