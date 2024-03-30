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
from random import randrange
import time

from .mathUtils import distanceBetweenPoints
from .utils import getSlowdownFactor, getSemiSlowdownFactor, getVerySlowdownFactor

pruneDefaultRes = 16
tfs = [1, 2, 4, 16]
sleepTimeThreshold = 0.02

def pruneDistanceWeighter(testPt, lookup, semilookup, verylookup):
    testPtInt = (int(testPt[0]), int(testPt[1]))
    if lookup and testPtInt in lookup:
        return getSlowdownFactor()
    elif semilookup and testPtInt in semilookup:
        return getSemiSlowdownFactor()
    elif verylookup and testPtInt in verylookup:
        return getVerySlowdownFactor()
    else:
        return 1.0


# Distance between A and B when weighted with slowness
def pruneWeightedDistance(ptA, ptB, lookup, semilookup, verylookup):
    if ptA == ptB:
        return 0.0
    steps = int(max(abs(ptA[0]- ptB[0]), abs(ptA[1] - ptB[1])))
    start = (float(ptA[0]), float(ptA[1]))
    testPt = start
    newScore = 0.0

    if steps:
        incr = (float(ptB[0] - ptA[0]) / float(steps), float(ptB[1] - ptA[1]) / float(steps))
        incrDist = distanceBetweenPoints((0.0, 0.0), incr)

        for ind in range(steps):
            testPt = (start[0] + ind * incr[0], start[1] + ind * incr[1])
            newScore = newScore + incrDist * pruneDistanceWeighter(testPt, lookup, semilookup, verylookup)

    incrDistLast = distanceBetweenPoints(testPt, ptB)
    newScore = newScore + incrDistLast * pruneDistanceWeighter(ptB, lookup, semilookup, verylookup)

    return newScore


def calculatePathWeightedDistance(path, lookup, semilookup, verylookup):
    dist = 0.0
    for index in range(len(path) - 1):
        dist = dist + pruneWeightedDistance(path[index], path[index + 1], lookup, semilookup, verylookup)
    return dist


# Ensure there is no forbidden areas between point A and B
def pruneEnsureLineOfSight(ptA, ptB, lookup):
    testPtList = []
    if ptA == ptB:
        return testPtList
    steps = int(max(abs(ptA[0]- ptB[0]), abs(ptA[1] - ptB[1]))) * 2
    if steps:
        incr = (float(ptB[0] - ptA[0]) / float(steps), float(ptB[1] - ptA[1]) / float(steps))
        incrDist = distanceBetweenPoints((0.0, 0.0), incr)
        start = (float(ptA[0]), float(ptA[1]))

        for ind in range(steps):
            testPt = (int(start[0] + ind * incr[0]), int(start[1] + ind * incr[1]))
            testPtList.append(testPt)
            if lookup and testPt in lookup:
                return None
    return testPtList


def pruneEnsureLineOfSightExt(pointA, pointB, forbiddenAreaLookup, tfNum):
    tf = tfs[tfNum]
    forbiddenLookup = forbiddenAreaLookup[tf]
    ptA = (pointA[0] // tf, pointA[1] // tf)
    ptB = (pointB[0] // tf, pointB[1] // tf)
    tmpTestPtList = pruneEnsureLineOfSight(ptA, ptB, forbiddenLookup)
    if tmpTestPtList is None:
        return None
    testPtList = []
    for item in tmpTestPtList:
        testPtList.append((item[0]*tf, item[1]*tf))
    return testPtList


# Check if decent direct route between point A and B
slowCheckPeriod = 4
def pruneEnsureGoodShortcut(ptA, ptB, lookup1, lookup2, lookup3):
    testPtList = []
    if ptA == ptB:
        return testPtList
    steps = max(abs(ptA[0]- ptB[0]), abs(ptA[1] - ptB[1]))
    if steps:
        incr = (float(ptB[0] - ptA[0]) / float(steps), float(ptB[1] - ptA[1]) / float(steps))
        incrDist = distanceBetweenPoints((0.0, 0.0), incr)
        start = (float(ptA[0]), float(ptA[1]))

        for ind in range(steps):
            testPt = (int(start[0] + ind * incr[0]), int(start[1] + ind * incr[1]))
            testPtList.append(testPt)
            if lookup1 and testPt in lookup1:
                return None
            elif ind % 4 == 0:
                if lookup2 and testPt in lookup2:
                    return None
                if lookup3 and testPt in lookup3:
                    return None

    return testPtList


# check if a line crosses forbidden areas or not
def pruneCheckLineOfSight(ptA, ptB, ptMid, forbiddenLookup, slowLookup, semiSlowLookup, verySlowLookup):
    if pruneEnsureLineOfSight(ptA, ptB, forbiddenLookup) != None:
        origScore = pruneWeightedDistance(ptA, ptMid, slowLookup, semiSlowLookup, verySlowLookup) + pruneWeightedDistance(ptMid, ptB, slowLookup, semiSlowLookup, verySlowLookup)
        newScore = pruneWeightedDistance(ptA, ptB, slowLookup, semiSlowLookup, verySlowLookup)
        if newScore < origScore:
            return True, origScore - newScore
    return False, 0.0


async def pruneCutTheCornersAsync(route, forbiddenLookup, slowLookup, semiSlowLookup, verySlowLookup, split, jump):
    prunedRoute = route.copy()
    sleep_time = time.time()

    index = 0
    while True:
        if index >= len(prunedRoute) - jump - 1:
            break
        pt1 = prunedRoute[index]
        ptMid1 = prunedRoute[index + 1]
        ptMid2 = prunedRoute[index + jump]
        pt2 = prunedRoute[index + jump + 1]
        pt1 = ((pt1[0] * split[0] + ptMid1[0] * (1 - split[0])), (pt1[1] * split[0] + ptMid1[1] * (1 - split[0])))
        pt2 = ((pt2[0] * split[1] + ptMid2[0] * (1 - split[1])), (pt2[1] * split[1] + ptMid2[1] * (1 - split[1])))
        index = index + 1

        shortcutFound, delta = pruneCheckLineOfSight(pt1, pt2, ptMid1, forbiddenLookup, slowLookup, semiSlowLookup, verySlowLookup)
        if shortcutFound:
            for dummy in range(jump):
                prunedRoute.pop(index)
            prunedRoute.insert(index, pt2)
            prunedRoute.insert(index, pt1)
            index = index + 2

        if time.time() - sleep_time > sleepTimeThreshold:
            sleep_time = time.time()
            await asyncio.sleep(0)

    return prunedRoute


# Straighten the rudimentary angular route that was found intially
async def pruneShortestRouteResAsync(route, forbiddenLookup, slowLookup, semiSlowLookup, verySlowLookup, thisStep, maxIt):
    prunedRoute = route.copy()
    sleep_time = time.time()

    index = 0
    for dummy in range(maxIt):
        if index:
            index = 0
        else:
            index = 1

        found = False

        while True:
            if index >= len(prunedRoute) - thisStep * 2:
                break
            pt1 = prunedRoute[index]
            ptMid = prunedRoute[index + thisStep]
            pt2 = prunedRoute[index + thisStep * 2]
            index = index + 1

            shortcutFound, delta = pruneCheckLineOfSight(pt1, pt2, ptMid, forbiddenLookup, slowLookup, semiSlowLookup, verySlowLookup)
            if shortcutFound:
                found = True
                for step in range(0, thisStep * 2 - 1):
                    prunedRoute.pop(index)
                prunedRoute.insert(index, ((pt1[0]+pt2[0])/2, (pt1[1]+pt2[1])/2))

            if time.time() - sleep_time > sleepTimeThreshold:
                sleep_time = time.time()
                await asyncio.sleep(0)

        if not found:
            break

    return prunedRoute


async def pruneShortestRouteAsync(route, forbiddenLookup, slowLookup, semiSlowLookup, verySlowLookup):
    iters = { 13: 1, 7: 1, 3: 1, 1: 3 }
    for res in [13, 7, 3, 1]:
        route = await pruneShortestRouteResAsync(route, forbiddenLookup, slowLookup, semiSlowLookup, verySlowLookup, res, iters[res])
    route = await pruneShortestRouteResAsync(route, forbiddenLookup, slowLookup, semiSlowLookup, verySlowLookup, 1, 4)
    for split in [(0.8, 0.8), (0.7, 0.4), (0.4, 0.7), (0.5, 0.5), (0.2, 0.2)]:
        route = await pruneCutTheCornersAsync(route, forbiddenLookup, slowLookup, semiSlowLookup, verySlowLookup, split, 1)

    return route


async def quickPruneShortestRouteAsync(route, forbiddenLookup, slowLookup, semiSlowLookup, verySlowLookup):
    route = await pruneShortestRouteResAsync(route, forbiddenLookup, slowLookup, semiSlowLookup, verySlowLookup, 13, 1)
    route = await pruneCutTheCornersAsync(route, forbiddenLookup, slowLookup, semiSlowLookup, verySlowLookup, (0.5, 0.5), 1)
    return route


async def pruneShortestRouteExtAsync(route, forbiddenAreaLookup, slowAreaLookup, semiSlowAreaLookup, verySlowAreaLookup, tfNum):
    tf = tfs[tfNum]
    forbiddenLookup = forbiddenAreaLookup[tf]
    slowLookup = slowAreaLookup[tf]
    semiSlowLookup = semiSlowAreaLookup[tf]
    verySlowLookup = verySlowAreaLookup[tf]

    scaledRoute = []
    for item in route:
        scaledRoute.append((item[0] // tf, item[1] // tf))
    tmpRoute = await pruneShortestRouteAsync(scaledRoute, forbiddenLookup, slowLookup, semiSlowLookup, verySlowLookup)
    route = []
    for item in tmpRoute:
        route.append((item[0]*tf, item[1]*tf))
    return route
