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

import asyncio
import time
from random import randrange

import sys

from .pathPruning import pruneShortestRouteAsync, pruneEnsureGoodShortcut, pruneEnsureLineOfSight
from .mathUtils import getBoundingBox, getNearestPointOfList, distanceBetweenPoints, calculatePathDistance
from .utils import getSlowdownFactor, getSemiSlowdownFactor, getVerySlowdownFactor, getAiPoolMaxTimeLimit, getPreRouteCount

minScoreInit = 10000
maxScoreInit = -10000

tfs = [1, 2, 4, 16]

bddTimeThreshold = 1.5
sleepTimeThreshold = 0.05

start_time = None


#maxX = 16 + 4
#maxY = 16 + 4
#def dump(title, tf, pointA, pointB, forbiddenAreaLookup, otherLookup):
#    ptA = (pointA[0] // tf, pointA[1] // tf)
#    ptB = (pointB[0] // tf, pointB[1] // tf)
#    print(title, ":")
#    for y in range(maxY // tf):
#        for x in range(maxX // tf):
#            if (x, y) == ptA:
#                print("A", end="")
#            elif (x, y) == ptB:
#                print("B", end="")
#            elif (x, y) in forbiddenAreaLookup[tf]:
#                print("X", end="")
#            elif (x, y) in otherLookup:
#                print(".", end="")
#            else:
#                print(" ", end="")
#        print("")


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
            if (point[0]//tf, point[1]//tf) in lookups[tf]:
                contains = True
            break
    return contains


closenessThreshold = 4.0
movementDirections = [(1, 0), (0, -1), (-1, 0), (0, 1)]
sideDirections = [(1, -1), (-1, -1), (-1, 1), (1, 1)]

def turnLeft(directionIndex):
    directionIndex = (directionIndex - 1) % len(movementDirections)
    return directionIndex

def turnRight(directionIndex):
    directionIndex = (directionIndex + 1) % len(movementDirections)
    return directionIndex

def calculateLeftSpot(spot, directionIndex):
    direction = movementDirections[(directionIndex - 1) % len(movementDirections)]
    return (spot[0] + direction[0], spot[1] + direction[1])

def calculateRightSpot(spot, directionIndex):
    direction = movementDirections[(directionIndex + 1) % len(movementDirections)]
    return (spot[0] + direction[0], spot[1] + direction[1])

def setInitialLeftGuyDirection(spot, lookup):
    directionIndex = 0
    for dummy in range(4):
        if calculateLeftSpot(spot, directionIndex) in lookup:
            return directionIndex
        directionIndex = turnLeft(directionIndex)
    return -1

def setInitialRightGuyDirection(spot, lookup):
    directionIndex = 0
    for dummy in range(4):
        if calculateRightSpot(spot, directionIndex) in lookup:
            return directionIndex
        directionIndex = turnRight(directionIndex)
    return -1

def calculateNextSpot(spot, directionIndex):
    direction = movementDirections[directionIndex]
    return (spot[0] + direction[0], spot[1] + direction[1])

def moveToWallSide(currentPt, lookup):
    for m in movementDirections:
        movePt = (currentPt[0] + m[0], currentPt[1] + m[1])
        if movePt in lookup:
            return currentPt

    for sInd in range(len(sideDirections)):
        s = sideDirections[sInd]
        sidePt = (currentPt[0] + s[0], currentPt[1] + s[1])
        if sidePt in lookup:
            m = movementDirections[sInd]
            newPt = (currentPt[0] + m[0], currentPt[1] + m[1])
            return newPt

    # should not end here
    return None

    
def getTestPointList(ptA, ptB, lookup):
    testPtList = []
    testScoreList = []
    testScore = 1.0
    if ptA == ptB:
        testPtList.append(ptA)
        testScoreList.append(testScore)
        return testPtList, testScoreList
    steps = max(abs(ptA[0]- ptB[0]), abs(ptA[1] - ptB[1]))
    incr = (float(ptB[0] - ptA[0]) / float(steps), float(ptB[1] - ptA[1]) / float(steps))
    incrDist = distanceBetweenPoints((0.0, 0.0), incr)
    start = (float(ptA[0]), float(ptA[1]))

    for ind in range(steps):
        testPt = (int(start[0] + ind * incr[0]), int(start[1] + ind * incr[1]))
        if testPt not in lookup:
            if not testPtList or testPtList[-1] != testPt:
                testPtList.append(testPt)
                testScoreList.append(testScore)
                testScore = testScore + 0.1
        else:
            if ind < 1 or ind > steps - 2:
                return [], []
                
            testScore = testScore + 1000.0
    return testPtList, testScoreList


def nearby(ptA, ptB):
    if abs(ptA[0] - ptB[0]) <= 1 and abs(ptA[1] - ptB[1]) <= 1:
        return True
    return False


# and fastest checker for route availability
def calculateCoarseRoute(ptA, ptB, forbiddenLookup, left, right, maxdist):
    currentPt2 = (-100, -100)

    leftGuyIndex = 0
    prevEasy = True
    jumps = 0
    ptList, scoreList = getTestPointList(ptA, ptB, forbiddenLookup)
    ptListOld = []

    if not ptList:
        return [], 0

    start_time = time.time()
    timeThreshold = bddTimeThreshold
    if left != right:
        timeThreshold = timeThreshold / 4

    shortestRoute = []
    dist = 0

    currentPt = ptList.pop(0) # turn to pop() to give a bit more perf?
    ptListOld.append(currentPt)
    currentScore=scoreList.pop(0)
    shortestRoute.append(currentPt)

    state = 0

    while distanceBetweenPoints(currentPt, ptB) > closenessThreshold and distanceBetweenPoints(currentPt2, ptB) > closenessThreshold:
        if time.time() - start_time > timeThreshold:
            return [], 0

        if not ptList:
            break

        if state == 0:
            # currentscore test not madatory?
            if scoreList[0] > currentScore and nearby(ptList[0], currentPt):
                currentPt = ptList.pop(0)
                ptListOld.append(currentPt)
                currentPt2 = (-100, -100)
                currentScore = scoreList.pop(0)
                shortestRoute.append(currentPt)
                dist = dist + 1
            else:
                state = 1
                prevEasy = True
                stucked = False
                stucked2 = False
        else:
            if prevEasy:
                currentPt = moveToWallSide(currentPt, forbiddenLookup)
                currentPt2 = moveToWallSide(currentPt, forbiddenLookup)
                leftGuyIndex = setInitialLeftGuyDirection(currentPt, forbiddenLookup)
                rightGuyIndex = setInitialRightGuyDirection(currentPt2, forbiddenLookup)
                if leftGuyIndex == -1 or rightGuyIndex == -1:
                    return [], 0
                leftGuyRoute = []
                rightGuyRoute = []
                prevEasy = False
                jumps = jumps + 1

            anyMoves = False
            # the clockwise-moving seeker
            if left:
                if calculateNextSpot(currentPt, leftGuyIndex) not in forbiddenLookup:
                    anyMoves = True
                    currentPt = calculateNextSpot(currentPt, leftGuyIndex)
                    currentScore = currentScore + 0.0001
                    if calculateLeftSpot(currentPt, leftGuyIndex) not in forbiddenLookup:
                        leftGuyIndex = turnLeft(leftGuyIndex)
                        currentPt = calculateNextSpot(currentPt, leftGuyIndex)

                for dummy in range(4):
                    if calculateNextSpot(currentPt, leftGuyIndex) in forbiddenLookup:
                        leftGuyIndex = turnRight(leftGuyIndex)

            # the counter-clockwise-moving seeker
            if right:
                if calculateNextSpot(currentPt2, rightGuyIndex) not in forbiddenLookup:
                    anyMoves = True
                    currentPt2 = calculateNextSpot(currentPt2, rightGuyIndex)
                    if calculateRightSpot(currentPt2, rightGuyIndex) not in forbiddenLookup:
                        rightGuyIndex = turnRight(rightGuyIndex)
                        currentPt2 = calculateNextSpot(currentPt2, rightGuyIndex)

                for dummy in range(4):
                    if calculateNextSpot(currentPt2, rightGuyIndex) in forbiddenLookup:
                        rightGuyIndex = turnLeft(rightGuyIndex)

            if not anyMoves:
                return [], 0

            leftGuyRoute.append(currentPt)
            if left and len(leftGuyRoute) > 1:
                dist = dist + 1
            rightGuyRoute.append(currentPt2)
            if right and len(rightGuyRoute) > 1:
                dist = dist + 1

            if maxdist and dist > maxdist:
                return [], 0
                
            if currentPt in ptList:
                ind = ptList.index(currentPt)
                for subind in range(ind):
                    ptList.pop(0)
                    scoreList.pop(0)
                currentPt = ptList.pop(0)
                ptListOld.append(currentPt)
                currentScore = scoreList.pop(0)
                shortestRoute = shortestRoute + leftGuyRoute
                state = 0
            elif currentPt2 in ptList:
                ind = ptList.index(currentPt2)
                for subind in range(ind):
                    ptList.pop(0)
                    scoreList.pop(0)
                currentPt = ptList.pop(0)
                ptListOld.append(currentPt)
                currentScore = scoreList.pop(0)
                shortestRoute = shortestRoute + rightGuyRoute
                state = 0
            else:
                if currentPt in ptListOld:
                    stucked = True
                if currentPt2 in ptListOld:
                    stucked2 = True
                if stucked and stucked2:
                    return [], 0

    if state == 1:
        if distanceBetweenPoints(currentPt, ptB) <= 4.0:
            shortestRoute = shortestRoute + leftGuyRoute
        elif distanceBetweenPoints(currentPt2, ptB) <= 4.0:
            shortestRoute = shortestRoute + rightGuyRoute

    shortestRoute.append(ptB)

    return shortestRoute, jumps


def calculateCoarseRouteExt(pointA, pointB, forbiddenAreaLookup, tfNum, left, right, maxdist):
    tf = tfs[tfNum]
    forbiddenLookup = forbiddenAreaLookup[tf]
    ptA = (pointA[0] // tf, pointA[1] // tf)
    ptB = (pointB[0] // tf, pointB[1] // tf)
    tmpShortestRoute, jumps = calculateCoarseRoute(ptA, ptB, forbiddenLookup, left, right, maxdist // tf)
    shortestRoute = []
    for item in tmpShortestRoute:
        shortestRoute.append((item[0]*tf, item[1]*tf))
    return shortestRoute, jumps



# fastest one so far
async def calculateShortestRouteAsync(setupList):
    left = True
    right = True
    pointA = setupList[0]
    pointB = setupList[1]
    forbiddenAreaLookup = setupList[2]
    slowAreaLookup = setupList[3]
    semiSlowAreaLookup = setupList[4]
    verySlowAreaLookup = setupList[5]
    tf = tfs[setupList[6]]
    pacemakerInd = setupList[7]
    preComputed = []
    if len(setupList) > 8:
        preComputed = setupList[8]
    if len(setupList) > 9:
        left = setupList[9]
    if len(setupList) > 10:
        right = setupList[10]

    forbiddenLookup = forbiddenAreaLookup[tf]
    slowLookup = slowAreaLookup[tf]
    semiSlowLookup = semiSlowAreaLookup[tf]
    verySlowLookup = verySlowAreaLookup[tf]

    ptA = (pointA[0] // tf, pointA[1] // tf)
    ptB = (pointB[0] // tf, pointB[1] // tf)
    preComputedScaled = []
    for item in preComputed:
        preComputedScaled.append((item[0] // tf, item[1] // tf))
    if preComputedScaled:
        shortestRoute = preComputedScaled
    else:
        shortestRoute, dummy_jumps = calculateCoarseRoute(ptA, ptB, forbiddenLookup, left, right, 0)

    if len(shortestRoute) < 2:
        return []

    # Straighten the route into a beautiful one
    if pacemakerInd != 2:
        shortestRoute = await pruneShortestRouteAsync(shortestRoute, forbiddenLookup, slowLookup, semiSlowLookup, verySlowLookup)

    shortestRoute = [(x[0] * tf, x[1] * tf) for x in shortestRoute.copy()]

    if len(shortestRoute) < 2:
        return []

    return shortestRoute


# Calculate shortest route between A and B, using pre-submitted lookups
async def slowAccurateCalculateShortestRouteAsync(setupList):

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
        sleep_time = time.time()
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
        while not stop:
            somethingHappened = False
            for point in backRouteLookup.copy():
                directions = getDirections(point)
                for direction in directions:
                    newPoint = direction[0]
                    if newPoint not in forbiddenLookup:
                        factor = 1.0
                        if newPoint in slowLookup:
                            factor = getSlowdownFactor()
                        elif newPoint in semiSlowLookup:
                            factor = getSemiSlowdownFactor()
                        elif newPoint in verySlowLookup:
                            factor = getVerySlowdownFactor()
                        newScore = direction[1] * factor
                        if newPoint not in backRouteLookup or backRouteLookup[point] + newScore < backRouteLookup[newPoint]:
                            backRouteLookup[newPoint] = backRouteLookup[point] + newScore
                            somethingHappened = True

                if time.time() - sleep_time > sleepTimeThreshold:
                    sleep_time = time.time()
                    await asyncio.sleep(0)

            for point in routeLookup.copy():
                directions = getDirections(point)
                for direction in directions:
                    newPoint = direction[0]
                    if newPoint not in forbiddenLookup:
                        factor = 1.0
                        if newPoint in slowLookup:
                            factor = getSlowdownFactor()
                        elif newPoint in semiSlowLookup:
                            factor = getSemiSlowdownFactor()
                        elif newPoint in verySlowLookup:
                            factor = getVerySlowdownFactor()
                        newScore = direction[1] * factor
                        if newPoint not in routeLookup or routeLookup[point] + newScore < routeLookup[newPoint]:
                            routeLookup[newPoint] = routeLookup[point] + newScore
                            somethingHappened = True
                            if newPoint in backRouteLookup:
                                stop = True
                                intersectionPoint = newPoint
                                break

                if time.time() - sleep_time > sleepTimeThreshold:
                    sleep_time = time.time()
                    await asyncio.sleep(0)

                if stop:
                    break


            if time.time() - start_time > getAiPoolMaxTimeLimit(tf):
                break

            # no progress, take next precision
            if not somethingHappened:
                break

        # this is also intentional!
        if not stop:
            continue

        # this is also intentional!
        if time.time() - start_time > getAiPoolMaxTimeLimit(tf):
            continue

        # Pick up the rudimentary angular route out of the painted data
        point = intersectionPoint
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

            if time.time() - sleep_time > sleepTimeThreshold:
                sleep_time = time.time()
                await asyncio.sleep(0)

        point = intersectionPoint
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

            if time.time() - sleep_time > sleepTimeThreshold:
                sleep_time = time.time()
                await asyncio.sleep(0)

        scaledShortestRoute = []
        for point in shortestRoute:
            scaledShortestRoute.append((point[0] * tf, point[1] * tf))

        # Straighten the route into a beautiful one
        if pacemakerInd != 2:
            scaledShortestRoute = await pruneShortestRouteAsync(scaledShortestRoute, forbiddenAreaLookup[1], slowAreaLookup[1], semiSlowAreaLookup[1], verySlowAreaLookup[1])
        return scaledShortestRoute
    return []


def slowAccurateCalculateShortestRoute(setupList):
    return asyncio.run(slowAccurateCalculateShortestRouteAsync(setupList))


def lookupPow2(lookup):
    startScore = 1.0
    pow2lookup = {}
    for point in lookup:
        base = lookup[point]
        left = (point[0] - 1, point[1])
        right = (point[0] + 1, point[1])
        up = (point[0], point[1] - 1)
        down = (point[0], point[1] + 1)
        scoreLU = base
        scoreLD = base
        scoreRU = base
        scoreRD = base
        pointLU = (point[0]*2, point[1]*2)
        pointLD = (point[0]*2, point[1]*2 + 1)
        pointRU = (point[0]*2 + 1, point[1]*2)
        pointRD = (point[0]*2 + 1, point[1]*2 + 1)
        if base != startScore:
            if left in lookup:
                scoreLU = (scoreLU + scoreLU + scoreLU + lookup[left]) / 4
                scoreLD = (scoreLD + scoreLD + scoreLD + lookup[left]) / 4
            elif up in lookup:
                scoreLU = (scoreLU + scoreLU + scoreLU + lookup[up]) / 4
            elif down in lookup:
                scoreLD = (scoreLD + scoreLD + scoreLD + lookup[down]) / 4

            if left in lookup and up in lookup and lookup[up] < lookup[left]:
                scoreLU = (scoreLU + scoreLU + scoreLU + lookup[up]) / 4
            if left in lookup and down in lookup and lookup[down] < lookup[left]:
                scoreLD = (scoreLD + scoreLD + scoreLD + lookup[down]) / 4

            if right in lookup:
                scoreRU = (scoreRU + scoreRU + scoreRU + lookup[right]) / 4
                scoreRD = (scoreRD + scoreRD + scoreRD + lookup[right]) / 4
            elif up in lookup:
                scoreRU = (scoreRU + scoreRU + scoreRU + lookup[up]) / 4
            elif down in lookup:
                scoreRD = (scoreRD + scoreRD + scoreRD + lookup[down]) / 4

            if right in lookup and up in lookup and lookup[up] < lookup[right]:
                scoreRU = (scoreRU + scoreRU + scoreRU + lookup[up]) / 4
            if right in lookup and down in lookup and lookup[down] < lookup[right]:
                scoreRD = (scoreRD + scoreRD + scoreRD + lookup[down]) / 4

        pow2lookup[pointLU] = scoreLU
        pow2lookup[pointLD] = scoreLD
        pow2lookup[pointRU] = scoreRU
        pow2lookup[pointRD] = scoreRD
    return pow2lookup


# Calculate shortest route between A and B, with higher precision re-iterations
async def ultimateCalculateShortestRouteAsync(setupList):

    pointA = setupList[0]
    pointB = setupList[1]
    forbiddenAreaLookup = setupList[2]
    slowAreaLookup = setupList[3]
    semiSlowAreaLookup = setupList[4]
    verySlowAreaLookup = setupList[5]
    maxPrecision = setupList[6]
    fromPrecision = setupList[7]
    pacemakerInd = setupList[8]

    sft = tfs[fromPrecision:maxPrecision]
    sft.reverse()

    backRouteLookups = {}
    routeLookups = {}
    intersectionPoints = {}
    prevIntersectionScore = None
    prevIntersectionBackScore = None

    # this algorithm requires power of two series
    for ind in range(len(sft) - 1):
        assert sft[ind] / 2 == sft[ind + 1]

    for tf in sft:
        if not tf in forbiddenAreaLookup or not forbiddenAreaLookup[tf]:
            backRouteLookups[tf] = {}
            routeLookups[tf] = {}
            intersectionPoints[tf] = None
            if tf != sft[-1]:
                routeLookup = lookupPow2(backRouteLookup)
                backRouteLookup = lookupPow2(backRouteLookup)
            continue
        start_time = time.time()
        sleep_time = time.time()
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
            backRouteLookups[tf] = {}
            routeLookups[tf] = {}
            intersectionPoints[tf] = None
            if tf != sft[-1]:
                routeLookup = lookupPow2(routeLookup)
                backRouteLookup = lookupPow2(backRouteLookup)
            continue

        tfA = (int(pointA[0]/tf), int(pointA[1]/tf))
        tfB = (int(pointB[0]/tf), int(pointB[1]/tf))
        startScore = 1.0
        intersectionPoint = None
        intersectionScore = None
        intersectionBackScore = None

        if tf == sft[0]:
            routeLookup = {}
            backRouteLookup = {}
            routeLookup[tfA] = startScore
            backRouteLookup[tfB] = startScore

        # Find a rudimentary angular route with a painter algo with A* flavour
        stop = False
        while not stop:
            somethingHappened = False
            for point in backRouteLookup.copy():
                directions = getDirections(point)
                for direction in directions:
                    newPoint = direction[0]
                    if newPoint not in forbiddenLookup:
                        factor = 1.0
                        if newPoint in slowLookup:
                            factor = getSlowdownFactor()
                        elif newPoint in semiSlowLookup:
                            factor = getSemiSlowdownFactor()
                        elif newPoint in verySlowLookup:
                            factor = getVerySlowdownFactor()
                        newScore = direction[1] * factor
                        if newPoint not in backRouteLookup or backRouteLookup[point] + newScore < backRouteLookup[newPoint]:
                            if prevIntersectionBackScore is None or backRouteLookup[point] + newScore < prevIntersectionBackScore:
                                backRouteLookup[newPoint] = backRouteLookup[point] + newScore
                                somethingHappened = True

                if time.time() - sleep_time > sleepTimeThreshold:
                    sleep_time = time.time()
                    await asyncio.sleep(0)

            for point in routeLookup.copy():
                directions = getDirections(point)
                for direction in directions:
                    newPoint = direction[0]
                    if newPoint not in forbiddenLookup:
                        factor = 1.0
                        if newPoint in slowLookup:
                            factor = getSlowdownFactor()
                        elif newPoint in semiSlowLookup:
                            factor = getSemiSlowdownFactor()
                        elif newPoint in verySlowLookup:
                            factor = getVerySlowdownFactor()
                        newScore = direction[1] * factor
                        if newPoint not in routeLookup or routeLookup[point] + newScore < routeLookup[newPoint]:
                            if prevIntersectionScore is None or routeLookup[point] + newScore < prevIntersectionScore:
                                routeLookup[newPoint] = routeLookup[point] + newScore
                                somethingHappened = True
                                if newPoint in backRouteLookup:
                                    if prevIntersectionScore is None:
                                        stop = True
                                        intersectionPoint = newPoint
                                        break
                                    elif routeLookup[newPoint] + backRouteLookup[newPoint] < prevIntersectionScore + prevIntersectionBackScore:
                                        intersectionPoint = newPoint

                if time.time() - sleep_time > sleepTimeThreshold:
                    sleep_time = time.time()
                    await asyncio.sleep(0)

                if stop:
                    break

            if time.time() - start_time > getAiPoolMaxTimeLimit(tf):
                break

            # no progress, take next precision
            if not somethingHappened:
                break

        backRouteLookups[tf] = backRouteLookup.copy()
        routeLookups[tf] = routeLookup.copy()
        intersectionPoints[tf] = intersectionPoint
        if tf != sft[-1]:
            routeLookup = lookupPow2(routeLookup)
            backRouteLookup = lookupPow2(backRouteLookup)
            if intersectionPoint is not None:
                intersectionPointTf = (intersectionPoint[0]*2, intersectionPoint[1]*2)
                if intersectionPointTf in routeLookup:
                    prevIntersectionScore = routeLookup[intersectionPointTf]
                    prevIntersectionBackScore = backRouteLookup[intersectionPointTf]

    # pick up routelookup, backroutelookups, intersectionpoint and tf
    intersectionPoint = None
    backRouteLookup = {}
    routeLookup = {}

    tmpsInOrder = []
    for tmpTf in sft:
        if tmpTf in intersectionPoints and intersectionPoints[tmpTf] is not None:
            tmpsInOrder.append(tmpTf)
    tmpsInOrder.reverse()

    if not tmpsInOrder:
        return []

    for tmpTf in tmpsInOrder:
        intersectionPoint = intersectionPoints[tmpTf]
        routeLookup = routeLookups[tmpTf]
        backRouteLookup = backRouteLookups[tmpTf]
        tf = tmpTf

        # Pick up the rudimentary angular route out of the painted data
        shortestRoute = []
        point = intersectionPoint
        score = backRouteLookup[point]
        while score > startScore:
            directions = getDirections(point)
            minScore = minScoreInit
            minPoint = None
            for direction in directions:
                 newPoint = direction[0]
                 if newPoint in backRouteLookup and backRouteLookup[newPoint] < minScore and newPoint not in shortestRoute:
                     minScore = backRouteLookup[newPoint]
                     minPoint = newPoint
            score = minScore
            if minPoint is None:
                return []
            point = minPoint
            shortestRoute.insert(0, point)
    
            if time.time() - sleep_time > sleepTimeThreshold:
                sleep_time = time.time()
                await asyncio.sleep(0)
    
        point = intersectionPoint
        shortestRoute.append(point)
        score = routeLookup[point]
        while score > startScore:
            directions = getDirections(point)
            minScore = minScoreInit
            minPoint = None
            for direction in directions:
                 newPoint = direction[0]
                 if newPoint in routeLookup and routeLookup[newPoint] < minScore and newPoint not in shortestRoute:
                     minScore = routeLookup[newPoint]
                     minPoint = newPoint
            score = minScore
            if minPoint is None:
                return []
            point = minPoint
            shortestRoute.append(point)
    
            if time.time() - sleep_time > sleepTimeThreshold:
                sleep_time = time.time()
                await asyncio.sleep(0)

        scaledShortestRoute = []
        for point in shortestRoute:
            scaledShortestRoute.append((point[0] * tf, point[1] * tf))

        # Straighten the route into a beautiful one
        if pacemakerInd != 2:
            scaledShortestRoute = await pruneShortestRouteAsync(scaledShortestRoute, forbiddenAreaLookup[1], slowAreaLookup[1], semiSlowAreaLookup[1], verySlowAreaLookup[1])
        return scaledShortestRoute
    return []


def ultimateCalculateShortestRoute(setupList):
    return asyncio.run(ultimateCalculateShortestRouteAsync(setupList))


# Global variables for the AI pools
aiNumberOfSlots = 2 # not too much pressure for the PC
aiSlots = []
readyRoutesArray = []




def initializeAITables():
    import multiprocessing
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
        readyRoutesArray.append({"setuplist": [[ctrls[index], ctrls[index+1], faLookup, saLookup, ssaLookup, vsaLookup, 2, 0, pacemakerInd]], "route": None})

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
            route = aiResult.get(timeout=getAiPoolMaxTimeLimit(1) * 2 + 2).copy()[0]
            route.reverse()
            readyRoutesArray[aiIndex]["route"] = [route]
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
                    aiSlots[ind]["aiResult"] = aiSlots[ind]["aiPool"].map_async(ultimateCalculateShortestRoute, readyRoutesArray[index]["setuplist"])
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















readyRoutesArrayAsync = []

async def initializeAINextTrackAsync(ctrls, faLookup, saLookup, ssaLookup, vsaLookup, pacemakerInd, preShortestRoutes):
    global asyncSlot
    global readyRoutesArrayAsync

    # if previous one exists, cancel everything and start a new one
    if readyRoutesArrayAsync:
        for item in readyRoutesArrayAsync:
            if item["task"] is not None:
                item["task"].cancel()
                try:
                    await item["task"]
                except asyncio.CancelledError:
                    pass
                item["task"] = None
            if item["task2"] is not None:
                item["task2"].cancel()
                try:
                    await item["task2"]
                except asyncio.CancelledError:
                    pass
                item["task2"] = None
    readyRoutesArrayAsync = []

    # initialize structure
    for index in range(len(ctrls) - 1):
        if sys.platform == 'emscripten':
            if index < getPreRouteCount():
                readyRoutesArrayAsync.append({"setuplist": [ctrls[index], ctrls[index+1], faLookup, saLookup, ssaLookup, vsaLookup, 0, pacemakerInd, []], "setuplist2": [ctrls[index], ctrls[index+1], faLookup, saLookup, ssaLookup, vsaLookup, 2, 1, pacemakerInd], "task": None, "task2": None, "route": preShortestRoutes[index][0], "route2": None, "index": index})
            else:
                readyRoutesArrayAsync.append({"setuplist": [ctrls[index], ctrls[index+1], faLookup, saLookup, ssaLookup, vsaLookup, 0, pacemakerInd, []], "setuplist2": [ctrls[index], ctrls[index+1], faLookup, saLookup, ssaLookup, vsaLookup, 2, 1, pacemakerInd], "task": None, "task2": None, "route": None, "route2": None, "index": index})
        else:
            readyRoutesArrayAsync.append({"setuplist": [ctrls[index], ctrls[index+1], faLookup, saLookup, ssaLookup, vsaLookup, 2, 1, pacemakerInd], "setuplist2": [ctrls[index], ctrls[index+1], faLookup, saLookup, ssaLookup, vsaLookup, 2, 0, pacemakerInd], "task": None, "task2": None, "route": None, "route2": None, "index": index})


async def getReadyShortestRoutesAsync(reachedControl):
    global  readyRoutesArrayAsync

    # handle possible ready tasks
    for item in readyRoutesArrayAsync:
        if item["task"] is not None:
            if item["task"].done():
                if item["route"] == None:
                    item["route"] = item["task"].result()
                item["task"] = None
        if item["task2"] is not None:
            if item["task2"].done():
                if item["route2"] == None:
                    item["route2"] = item["task2"].result()
                item["task2"] = None

    # cancel overtime tasks
    preReachedControl = reachedControl - 1
    if preReachedControl < 0:
        preReachedControl = 0
    for item in readyRoutesArrayAsync[:preReachedControl]:
        if item["task"] is not None:
            item["task"].cancel()
            try:
                await item["task"]
            except asyncio.CancelledError:
                pass
            item["task"] = None
        if item["task2"] is not None:
            item["task2"].cancel()
            try:
                await item["task2"]
            except asyncio.CancelledError:
                pass
            item["task2"] = None

    # check if any non-overtime task running
    tasksRunning = False
    tasksRunning2 = False
    for item in readyRoutesArrayAsync[preReachedControl:]:
        if item["task"] is not None:
            tasksRunning = True
            break
        if item["task2"] is not None:
            tasksRunning2 = True
            break

    # if not, start a new one
    if not tasksRunning:
        for item in readyRoutesArrayAsync[preReachedControl:]:
            if item["route"] == None:
                if sys.platform == 'emscripten':
                    item["task"] = asyncio.create_task(calculateShortestRouteAsync(item["setuplist"]))
                else:
                    item["task"] = asyncio.create_task(ultimateCalculateShortestRouteAsync(item["setuplist"]))
                break
    if not tasksRunning2:
        for item in readyRoutesArrayAsync[preReachedControl:]:
            if item["route2"] == None:
                if sys.platform == 'emscripten':
                    item["task2"] = asyncio.create_task(ultimateCalculateShortestRouteAsync(item["setuplist2"]))
                else:
                    item["task2"] = asyncio.create_task(ultimateCalculateShortestRouteAsync(item["setuplist2"]))
                break

    # finally, compose a return list
    returnRoutesArray = []
    for item in readyRoutesArrayAsync:
        if (item["route"] is None or len(item["route"]) == 0) and (item["route2"] is None or len(item["route2"]) == 0):
            returnRoutesArray.append([])
        elif (item["route2"] is None or len(item["route2"]) == 0):
            returnRoutesArray.append(item["route"])
        else:
            returnRoutesArray.append(item["route2"])
    return returnRoutesArray
