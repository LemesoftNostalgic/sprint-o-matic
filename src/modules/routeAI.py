#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements. See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#

import time
import multiprocessing
from random import randrange

import sys

from .pathPruning import pruneShortestRoute, pruneEnsureGoodShortcut, pruneEnsureLineOfSight, distanceBetweenPoints
from .mathUtils import getBoundingBox, getNearestPointOfList
from .utils import getSlowdownFactor, getSemiSlowdownFactor, getVerySlowdownFactor, getAiPoolMaxTimeLimit

minScoreInit = 10000
maxScoreInit = -10000

tfs = [1, 2, 4, 8, 16]

quickCheckDefaultTf = 4

start_time = None
refreshCtr = 5000

def getSignX(x):
    return (x > 0) - (x < 0)


def getQuickDirections(point, target):
    retList = []
    if point[0] != target[0]:
        retList.append((point[0] + getSignX(target[0] - point[0]), point[1]))
    if point[1] != target[1]:
        retList.append((point[0], point[1] + getSignX(target[1] - point[1])))
    return retList
    

def getDirections(point):
    return [
        [(point[0] - 1, point[1]), 1.0],
        [(point[0] + 1, point[1]), 1.0],
        [(point[0], point[1] - 1), 1.0],
        [(point[0], point[1] + 1), 1.0]
    ]


def moveCloserToEachOther(tfA, tfB, forbiddenLookup):
    moving = True
    while moving:
        moving = False
        dirsToB = getQuickDirections(tfA, tfB)
        for dirToB in dirsToB:
            if dirToB not in forbiddenLookup:
                tfA = dirToB
                moving = True
        dirsToA = getQuickDirections(tfB, tfA)
        for dirToA in dirsToA:
            if dirToA not in forbiddenLookup:
                tfB = dirToA
                moving = True
    return tfA, tfB


def getBubblePoints(ptA, ptB, forbiddenLookup, bubbleSpacing):
    bubblePoints = []
    steps = max(abs(ptA[0]- ptB[0]), abs(ptA[1] - ptB[1]))
    incr = (float(ptB[0] - ptA[0]) / float(steps), float(ptB[1] - ptA[1]) / float(steps))
    start = (float(ptA[0]), float(ptA[1]))

    prevBubble = start
    for ind in range(steps):
        testPt = (int(start[0] + ind * incr[0]), int(start[1] + ind * incr[1]))
        if distanceBetweenPoints(testPt, ptB) < bubbleSpacing:
            break
        if distanceBetweenPoints(prevBubble, testPt) > bubbleSpacing:
            if testPt not in forbiddenLookup:
                bubblePoints.append(testPt)
                prevBubble = testPt

    return bubblePoints


def lookupContains(lookups, point):
    contains = False
    for tf in tfs:
        if tf in lookups and lookups[tf]:
            # found a valid tf
            if (int(point[0]/tf), int(point[1]/tf)) in lookups[tf]:
                contains = True
            break
    return contains


# Quickly check if any chance of route between A and B
def checkRouteExists(pointA, pointB, forbiddenAreaLookup, bubbleSpacing, checkMaxTime):

    tf = quickCheckDefaultTf
    forbiddenLookup = forbiddenAreaLookup[tf]

     # The algorithm is time-restricted
    start_time = time.time()
    
    tfA = (int(pointA[0]/tf), int(pointA[1]/tf))
    tfB = (int(pointB[0]/tf), int(pointB[1]/tf))

    # Try quick win
    if pruneEnsureLineOfSight(tfA, tfB, forbiddenLookup) != None:
        return True
    tfA, tfB = moveCloserToEachOther(tfA, tfB, forbiddenLookup)
    if tfA == tfB:
        return True
    if pruneEnsureLineOfSight(tfA, tfB, forbiddenLookup) != None:
        return True

    # desperately optimized...
    bubblePoints = getBubblePoints(tfA, tfB, forbiddenLookup, bubbleSpacing)

    startScore = 1.0
    routeLookup = {}
    backRouteLookup = {}
    bubbleLookups = []
    prevMidPointsArray = []

    routeLookup[tfA] = startScore
    backRouteLookup[tfB] = startScore
    prevBackPoints = list(backRouteLookup.keys())
    prevFrontPoints = list(routeLookup.keys())
    for bubblePoint in bubblePoints:
        bubbleLookup = {}
        bubbleLookup[bubblePoint] = startScore
        bubbleLookups.append(bubbleLookup)
        prevMidPointsArray.append(list(bubbleLookup.keys()))

    # Find a rudimentary angular route with a painter algo with A* flavour
    # add bubbles and stuff to make it quicker 
    while True:
        backPoints = []
        for point in prevBackPoints:
            directions = getQuickDirections(point, tfA)
            for direction in directions:
                newPoint = direction
                if (newPoint not in backRouteLookup or backRouteLookup[point] + 1.0 < backRouteLookup[newPoint]) and newPoint not in forbiddenLookup:
                    backRouteLookup[newPoint] = backRouteLookup[point] + 1.0
                    backPoints.append(newPoint)
        if not backPoints:
            for point in prevBackPoints:
                directions = getDirections(point)
                for direction in directions:
                    newPoint = direction[0]
                    if (newPoint not in backRouteLookup or backRouteLookup[point] + 1.0 < backRouteLookup[newPoint]) and newPoint not in forbiddenLookup:
                        backRouteLookup[newPoint] = backRouteLookup[point] + 1.0
                        backPoints.append(newPoint)
            if not backPoints:
                return False
        prevBackPoints = backPoints

        for midRouteLookupInd in range(len(bubbleLookups)):
            midRouteLookup = bubbleLookups[midRouteLookupInd]
            prevMidPoints = prevMidPointsArray[midRouteLookupInd]
            midPoints = []
            emergencyBreak = False
            for point in prevMidPoints:
                directions = getDirections(point)
                for direction in directions:
                    newPoint = direction[0]
                    if (newPoint not in midRouteLookup or midRouteLookup[point] + 1.0 < midRouteLookup[newPoint]) and newPoint not in forbiddenLookup:
                        midRouteLookup[newPoint] = midRouteLookup[point] + 1.0
                        midPoints.append(newPoint)
                        if midRouteLookupInd and newPoint in bubbleLookups[midRouteLookupInd - 1]:
                            bubbleLookups[midRouteLookupInd - 1].update(midRouteLookup.copy())
                            prevMidPointsArray[midRouteLookupInd - 1] = list(set(prevMidPointsArray[midRouteLookupInd - 1].copy()) | set(midRouteLookup.keys()).copy())
                            bubbleLookups[midRouteLookupInd] = {}
                            prevMidPointsArray[midRouteLookupInd] = []
                            emergencyBreak = True
                            break
                        elif not midRouteLookupInd and newPoint in backRouteLookup:
                            backRouteLookup.update(midRouteLookup.copy())
                            prevBackPoints = list(set(prevBackPoints.copy()) | set(midRouteLookup.keys()).copy())
                            bubbleLookups[midRouteLookupInd] = {}
                            prevMidPointsArray[midRouteLookupInd] = []
                            emergencyBreak = True
                            break
                if emergencyBreak:
                    break
            if emergencyBreak:
                break

            if bubbleLookups[midRouteLookupInd]:
                prevMidPointsArray[midRouteLookupInd] = midPoints
                bubbleLookups[midRouteLookupInd] = midRouteLookup
                prevLookup = midRouteLookup

        newbubbleLookups = []
        newprevMidPointsArray = []
        for ind in range(len(bubbleLookups)):
            if bubbleLookups[ind]:
                newbubbleLookups.append(bubbleLookups[ind])
                newprevMidPointsArray.append(prevMidPointsArray[ind])
        bubbleLookups = newbubbleLookups
        prevMidPointsArray = newprevMidPointsArray

        frontPoints = []
        for point in prevFrontPoints:
            directions = getQuickDirections(point, tfB)
            for direction in directions:
                newPoint = direction
                if (newPoint not in routeLookup or routeLookup[point] + 1.0 <= routeLookup[newPoint]) and newPoint not in forbiddenLookup:
                    routeLookup[newPoint] = routeLookup[point] + 1.0
                    frontPoints.append(newPoint)
                    if newPoint in backRouteLookup:
                        return True

        if not frontPoints:
            for point in prevFrontPoints:
                directions = getDirections(point)
                for direction in directions:
                    newPoint = direction[0]
                    if (newPoint not in routeLookup or routeLookup[point] + 1.0 <= routeLookup[newPoint]) and newPoint not in forbiddenLookup:
                        routeLookup[newPoint] = routeLookup[point] + 1.0
                        frontPoints.append(newPoint)
                        if newPoint in backRouteLookup:
                            return True
            if not frontPoints:
                return False
        prevFrontPoints = frontPoints

        if time.time() - start_time > checkMaxTime:
            return False


# this may give some ideas, no more. Need to switch to bdd algorithm (ota forb kappaleiden ulkoreuna mukaan massaan)
# kaikki muutkin nopeutukset tähän
def quickCalculateShortestRoute(pointA, pointB, lookup, forbiddenAreaLookup, slowAreaLookup, semiSlowAreaLookup, verySlowAreaLookup, tf, pacemakerInd):
    shortestRoute = []
    routeLookup = {}
    backRouteLookup = {}
    start_time = time.time()
    forbiddenLookup = {}
    if tf in forbiddenAreaLookup:
        forbiddenLookup = forbiddenAreaLookup[tf]
    slowLookup = {}
    if tf in slowAreaLookup:
        slowLookup = slowAreaLookup[tf]
    semiSlowLookup = {}
    if tf in semiSlowAreaLookup:
        semiSlowLookup = slowAreaLookup[tf]
    verySlowLookup = {}
    if tf in verySlowAreaLookup:
        verySlowLookup = slowAreaLookup[tf]
    intersectionPointBack = None
    intersectionPointFront = None

    tfA = (int(pointA[0]/tf), int(pointA[1]/tf))
    tfB = (int(pointB[0]/tf), int(pointB[1]/tf))
    startScore = 1.0
    routeLookup[tfA] = startScore
    backRouteLookup[tfB] = startScore
    prevFrontPoints = [tfA]
    prevBackPoints = [tfB]
        
    # Find a rudimentary angular route with a painter algo with A* flavour
    stop = False

    while not stop:
        backPoints = []
        for point in prevBackPoints:
            directions = getDirections(point)
            for direction in directions:
                newPoint = direction[0]
                if (newPoint not in backRouteLookup or backRouteLookup[point] + 1.0 < backRouteLookup[newPoint]) and newPoint in lookup:
                    factor = 1.0
                    if newPoint in slowLookup:
                        factor = getSlowdownFactor()
                    elif newPoint in semiSlowLookup:
                        factor = getSemiSlowdownFactor()
                    elif newPoint in verySlowLookup:
                        factor = getVerySlowdownFactor()
                    newScore = direction[1] * factor
                    backRouteLookup[newPoint] = backRouteLookup[point] + newScore
                    backPoints.append(newPoint)
        if not backPoints:
            return []
        prevBackPoints = backPoints

        frontPoints = []
        for point in prevFrontPoints:
            directions = getDirections(point)
            for direction in directions:
                newPoint = direction[0]
                if (newPoint not in routeLookup or routeLookup[point] + 1.0 <= routeLookup[newPoint]) and newPoint in lookup:
                    factor = 1.0
                    if newPoint in slowLookup:
                        factor = getSlowdownFactor()
                    elif newPoint in semiSlowLookup:
                        factor = getSemiSlowdownFactor()
                    elif newPoint in verySlowLookup:
                        factor = getVerySlowdownFactor()
                    newScore = direction[1] * factor
                    routeLookup[newPoint] = routeLookup[point] + newScore
                    frontPoints.append(newPoint)
                    if newPoint in backRouteLookup:
                        stop = True
                        intersectionPointBack = newPoint
                        intersectionPointFront = newPoint
                        break
                if stop:
                    break
        if not frontPoints:
            return []
        if time.time() - start_time > getAiPoolMaxTimeLimit(tf):
            return []
        prevFrontPoints = frontPoints

    if intersectionPointBack is None or intersectionPointFront is None:
        return []

    # Pick up the rudimentary angular route out of the painted data
    point = intersectionPointBack
    score = backRouteLookup[point]
    while score > startScore:
        directions = getDirections(point)
        minScore = minScoreInit
        minPoint = None
        for direction in directions:
             newPoint = direction[0]
             if newPoint in backRouteLookup and backRouteLookup[newPoint] < score:
                 minScore = backRouteLookup[newPoint]
                 minPoint = newPoint
        score = minScore
        if not minPoint:
            return []
        point = minPoint
        shortestRoute.insert(0, point)

    point = intersectionPointFront
    shortestRoute.append(point)
    score = routeLookup[point]
    while score > startScore:
        directions = getDirections(point)
        minScore = minScoreInit
        minPoint = None
        for direction in directions:
             newPoint = direction[0]
             if newPoint in routeLookup and routeLookup[newPoint] < score:
                 minScore = routeLookup[newPoint]
                 minPoint = newPoint
        score = minScore
        if not minPoint:
            return []
        point = minPoint
        shortestRoute.append(point)

     # Straighten the route into a beautiful one
    if pacemakerInd != 2:
        shortestRoute = pruneShortestRoute(shortestRoute, forbiddenLookup, slowLookup, semiSlowLookup, verySlowLookup, -1)
    scaledShortestRoute = []
    for point in shortestRoute:
        scaledShortestRoute.append((point[0] * tf, point[1] * tf))
    return scaledShortestRoute


def quickUpdateShortestRoutes(shortestRoutesArray, lookups, controls, faLookup, saLookup, ssaLookup, vsaLookup, first, last, pacemakerInd):
    if first == 0:
        shortestRoutesArray = []
        for ind in range(len(lookups)):
            shortestRoutesArray.append([])

    for ind in range(first, last):
        if ind >= len(lookups):
            break
        lookup = lookups[ind]
        ptA = controls[ind]
        ptB = controls[ind + 1]
        shortestRoutesArray[ind] = [quickCalculateShortestRoute(ptA, ptB, lookup, faLookup, saLookup, ssaLookup, vsaLookup, 4, pacemakerInd)]
        print(ind, shortestRoutesArray[ind])
    return shortestRoutesArray


# Calculate shortest route between A and B, using pre-submitted lookups
def calculateShortestRoute(setupList):

    pointA = setupList[0]
    pointB = setupList[1]
    forbiddenAreaLookup = setupList[2]
    slowAreaLookup = setupList[3]
    semiSlowAreaLookup = setupList[4]
    verySlowAreaLookup = setupList[5]
    maxPrecision = setupList[6]
    pacemakerInd = setupList[7]

    sft = tfs[:maxPrecision]
    sft.reverse()

    for tf in sft:
        if not tf in forbiddenAreaLookup or not forbiddenAreaLookup[tf]:
            continue
        shortestRoute = []
        routeLookup = {}
        backRouteLookup = {}
        start_time = time.time()
        forbiddenLookup = forbiddenAreaLookup[tf]
        slowLookup = {}
        if tf in slowAreaLookup:
            slowLookup = slowAreaLookup[tf]
        semiSlowLookup = {}
        if tf in semiSlowAreaLookup:
            semiSlowLookup = slowAreaLookup[tf]
        verySlowLookup = {}
        if tf in verySlowAreaLookup:
            verySlowLookup = slowAreaLookup[tf]

        # The algorithm is time-restricted
        if time.time() - start_time > getAiPoolMaxTimeLimit(tf):
            continue

        tfA = (int(pointA[0]/tf), int(pointA[1]/tf))
        tfB = (int(pointB[0]/tf), int(pointB[1]/tf))
        startScore = 1.0
        routeLookup[tfA] = startScore
        backRouteLookup[tfB] = startScore
        
        # Find a rudimentary angular route with a painter algo with A* flavour
        stop = False
        nextPruning = True
        pointsInBetween = []
        while not stop:
            pointsInBetween = []
            backPoints = []
            for point in backRouteLookup.copy():
                directions = getDirections(point)
                for direction in directions:
                    newPoint = direction[0]
                    factor = 1.0
                    if newPoint in slowLookup:
                        factor = getSlowdownFactor()
                    elif newPoint in semiSlowLookup:
                        factor = getSemiSlowdownFactor()
                    elif newPoint in verySlowLookup:
                        factor = getVerySlowdownFactor()
                    newScore = direction[1] * factor
                    if (newPoint not in backRouteLookup or backRouteLookup[point] + newScore < backRouteLookup[newPoint]) and newPoint not in forbiddenLookup:
                        backRouteLookup[newPoint] = backRouteLookup[point] + newScore
                        backPoints.append(newPoint)

            for point in routeLookup.copy():
                directions = getDirections(point)
                for direction in directions:
                    newPoint = direction[0]
                    factor = 1.0
                    if newPoint in slowLookup:
                        factor = getSlowdownFactor()
                    elif newPoint in semiSlowLookup:
                        factor = getSemiSlowdownFactor()
                    elif newPoint in verySlowLookup:
                        factor = getVerySlowdownFactor()
                    newScore = direction[1] * factor
                    if (newPoint not in routeLookup or routeLookup[point] + newScore <= routeLookup[newPoint]) and newPoint not in forbiddenLookup:
                        routeLookup[newPoint] = routeLookup[point] + newScore
                        if newPoint in backRouteLookup:
                            stop = True
                            intersectionPointBack = newPoint
                            intersectionPointFront = newPoint
                            break
                        # shortcut
                        elif nextPruning and backPoints:
                            nextPruning = True if randrange(refreshCtr//tf) == 0 else False
                            backPoint = getNearestPointOfList(backPoints, newPoint)
                            pointsInBetween = pruneEnsureGoodShortcut(backPoint, newPoint, forbiddenLookup, slowLookup, verySlowLookup)
                            if pointsInBetween != None:
                                stop = True
                                intersectionPointBack = backPoint
                                intersectionPointFront = newPoint
                                break
                    if stop:
                        break
            if time.time() - start_time > getAiPoolMaxTimeLimit(tf):
                break
        # this is also intentional!

        # perf tuning: always accept coarse result for now...
        # if tf > 1 and time.time()-start_time < getAiPoolMaxTimeLimit(tf) / 5:
        #    continue

        if time.time() - start_time > getAiPoolMaxTimeLimit(tf):
            continue

        # Pick up the rudimentary angular route out of the painted data
        point = intersectionPointBack
        score = backRouteLookup[point]
        while score > startScore:
            directions = getDirections(point)
            minScore = minScoreInit
            minPoint = None
            for direction in directions:
                 newPoint = direction[0]
                 if newPoint in backRouteLookup and backRouteLookup[newPoint] < score:
                     minScore = backRouteLookup[newPoint]
                     minPoint = newPoint
            score = minScore
            if not minPoint:
                return []
            point = minPoint
            shortestRoute.insert(0, point)

        if pointsInBetween != None:
            shortestRoute = shortestRoute + pointsInBetween

        point = intersectionPointFront
        shortestRoute.append(point)
        score = routeLookup[point]
        while score > startScore:
            directions = getDirections(point)
            minScore = minScoreInit
            minPoint = None
            for direction in directions:
                 newPoint = direction[0]
                 if newPoint in routeLookup and routeLookup[newPoint] < score:
                     minScore = routeLookup[newPoint]
                     minPoint = newPoint
            score = minScore
            if not minPoint:
                return []
            point = minPoint
            shortestRoute.append(point)

        # Straighten the route into a beautiful one
        if pacemakerInd != 2:
            shortestRoute = pruneShortestRoute(shortestRoute, forbiddenLookup, slowLookup, semiSlowLookup, verySlowLookup, -1)
        scaledShortestRoute = []
        for point in shortestRoute:
            scaledShortestRoute.append((point[0] * tf, point[1] * tf))
        return scaledShortestRoute
    return []


# Global variables for the AI pools
aiNumberOfSlots = 2 # not too much pressure for the PC
aiSlots = []
readyRoutesArray = []


def initializeAITables():
    multiprocessing.freeze_support()
    for ind in range(aiNumberOfSlots):
        aiSlots.append({"aiIndex": None, "aiPool": multiprocessing.Pool(processes = 1), "aiResult": None})


def closeAITables():
    for ind in range(aiNumberOfSlots):
        aiSlots[ind]["aiPool"].close()
        aiSlots[ind]["aiPool"].join()
        aiSlots[ind]["aiIndex"] = None
        aiSlots[ind]["aiResult"] = None


def initializeAINextTrack(ctrls, faLookup, saLookup, ssaLookup, vsaLookup, pacemakerInd):
    global readyRoutesArray
    readyRoutesArray = []

    for index in range(len(ctrls) - 1):
        readyRoutesArray.append({"setuplist": [[ctrls[index], ctrls[index+1], faLookup, saLookup, ssaLookup, vsaLookup, 3, pacemakerInd]], "route": None})

    for ind in range(aiNumberOfSlots):
        aiSlots[ind]["aiIndex"] = None
        if aiSlots[ind]["aiResult"] != None:
            aiSlots[ind]["aiResult"].wait()
        aiSlots[ind]["aiResult"] = None


def getReadyShortestRoutes():
    global  aiSlots
    global  readyRoutesArray

    # first check out any finished work
    for ind in range(aiNumberOfSlots):
        aiIndex = aiSlots[ind]["aiIndex"]
        aiResult = aiSlots[ind]["aiResult"]
        if aiResult is not None and aiResult.ready():
            readyRoutesArray[aiIndex]["route"] = aiResult.get(timeout=getAiPoolMaxTimeLimit(1) * 2 + 2).copy()
            aiSlots[ind]["aiIndex"] = None
            aiSlots[ind]["aiResult"] = None

    freeSlots = 0
    for ind in range(aiNumberOfSlots):
        if aiSlots[ind]["aiResult"] == None:
            freeSlots = freeSlots + 1

    # then get the free slots running again
    for ind in range(aiNumberOfSlots):
        if aiSlots[ind]["aiResult"] == None:
            for index in range(len(readyRoutesArray)):
                if readyRoutesArray[index]["route"] == None:
                    readyRoutesArray[index]["route"] = []
                    aiSlots[ind]["aiIndex"] = index
                    aiSlots[ind]["aiResult"] = aiSlots[ind]["aiPool"].map_async(calculateShortestRoute, readyRoutesArray[index]["setuplist"])
                    break

    freeSlots = 0
    for ind in range(aiNumberOfSlots):
        if aiSlots[ind]["aiResult"] == None:
            freeSlots = freeSlots + 1

    returnRoutesArray = []
    for item in readyRoutesArray:
        if item["route"] is None:
            returnRoutesArray.append([])
        else:
            returnRoutesArray.append(item["route"])
    return returnRoutesArray


if __name__ == "__main__":
    print(calculateShortestRoute([(10,0), (11,3), {1:{(10,2):True,(11,2):True,(9,2):True}}, {1:{}},
                                  {
                                   ((3,0),2): [((4,0), 2, 2), ((3,1), 2, 2)],
                                   ((4,0),2): [((3,0), 2, 2), ((8,2), 1, 2), ((5,0), 2, 2)],
                                   ((5,0),2):[((6,0), 2, 2), ((4,0), 2, 2)],
                                   ((6,0),2):[((5,0),2, 2), ((6,1),2, 2)],
                                   ((3,1),2):[((3,0),2,2), ((8,2),1,2), ((8,3),1, 2.235)],
                                   ((8,2),1):[((3,1),2, 2),((8,3),1, 1),((4,0), 2, 2)],
                                   ((6,1),2):[((6,0),2, 2)],
                                   ((8,3),1):[((8,2),1, 1), ((9,3),1,1), ((3,1),2, 2.235)],
                                   ((9,3),1):[((8,3),1,1), ((10,3),1, 1)],
                                   ((10,3),1):[((9,3),1, 1), ((11,3),1, 1)],
                                   ((11,3),1):[((10,3),1, 1)],
                                  }
    ]))
