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

from .pathPruning import pruneShortestRoute, pruneEnsureLineOfSight
from .mathUtils import getBoundingBox, getNearestPointOfList
from .utils import getSlowdownFactor, getSemiSlowdownFactor, getVerySlowdownFactor, getAiPoolMaxTimeLimit

minScoreInit = 10000
maxScoreInit = -10000

tfs = [1, 2, 4, 8, 16]

start_time = None
refreshCtr = 5000

# Provide the 4 primitive directions to nearest points and the distance to them
def getDirections(point):
    return [
        [(point[0] - 1, point[1]), 1.0],
        [(point[0] + 1, point[1]), 1.0],
        [(point[0], point[1] - 1), 1.0],
        [(point[0], point[1] + 1), 1.0]
    ]


def lookupContains(lookups, point):
    contains = False
    for tf in tfs:
        if tf in lookups and lookups[tf]:
            # found a valid tf
            if (int(point[0]/tf), int(point[1]/tf)) in lookups[tf]:
                contains = True
            break
    return contains


# This shortest route finder is my genuine creation.
# Finding a fast enough algorithm was not easy, so I decided to take the
# time and think this through. Not the most beautiful one, but does the
# trick very fast.

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

        # The algorithm is time-restricted, be less accurate if takes too long
        if time.time() - start_time > getAiPoolMaxTimeLimit(tf):
            continue

        # Find a rudimentary angular route with a sort of painter algo with A* flavour
        tfA = (int(pointA[0]/tf), int(pointA[1]/tf))
        tfB = (int(pointB[0]/tf), int(pointB[1]/tf))
        startScore = 1.0
        routeLookup[tfA] = startScore
        backRouteLookup[tfB] = startScore
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
                            nextPruning = True if randrange(refreshCtr) == 0 else False
                            backPoint = getNearestPointOfList(backPoints, newPoint)
                            pointsInBetween = pruneEnsureLineOfSight(backPoint, newPoint, forbiddenLookup)
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
        if tf > 1 and time.time() - start_time < getAiPoolMaxTimeLimit(tf) / 5:
            continue
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
aiNumberOfSlots = 3
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
