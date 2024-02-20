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

from random import randrange

from .mathUtils import distanceBetweenPoints
from .utils import getSlowdownFactor, getSemiSlowdownFactor, getVerySlowdownFactor


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
    steps = max(abs(ptA[0]- ptB[0]), abs(ptA[1] - ptB[1]))
    incr = (float(ptB[0] - ptA[0]) / float(steps), float(ptB[1] - ptA[1]) / float(steps))
    incrDist = distanceBetweenPoints((0.0, 0.0), incr)
    start = (float(ptA[0]), float(ptA[1]))

    for ind in range(steps):
        testPt = (int(start[0] + ind * incr[0]), int(start[1] + ind * incr[1]))
        testPtList.append(testPt)
        if lookup and testPt in lookup:
            return None
    return testPtList


# Check if decent direct route between point A and B
slowCheckPeriod = 4
def pruneEnsureGoodShortcut(ptA, ptB, lookup1, lookup2, lookup3):
    testPtList = []
    if ptA == ptB:
        return testPtList
    steps = max(abs(ptA[0]- ptB[0]), abs(ptA[1] - ptB[1]))
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
    origScore = pruneWeightedDistance(ptA, ptMid, slowLookup, semiSlowLookup, verySlowLookup) + pruneWeightedDistance(ptMid, ptB, slowLookup, semiSlowLookup, verySlowLookup)
    if pruneEnsureLineOfSight(ptA, ptB, forbiddenLookup) != None:
        newScore = pruneWeightedDistance(ptA, ptB, slowLookup, semiSlowLookup, verySlowLookup)
        if newScore < origScore:
            return True, origScore - newScore
    return False, 0.0

# Straighten the rudimentary angular route that was found intially
def pruneShortestRoute(route, forbiddenLookup, slowLookup, semiSlowLookup, verySlowLookup, iterations):
    prunedRoute = route.copy()

    while len(prunedRoute) > 2:
        nextRoute = []

        maxDelta = 0
        maxDeltaInd = 0
        for index in range(len(prunedRoute) - 2):
            pt1 = prunedRoute[index]
            ptMid = prunedRoute[index + 1]
            pt2 = prunedRoute[index + 2]

            shortcutFound, delta = pruneCheckLineOfSight(pt1, pt2, ptMid, forbiddenLookup, slowLookup, semiSlowLookup, verySlowLookup)
            if shortcutFound:
                if delta > maxDelta:
                    maxDelta = delta
                    maxDeltaInd = index + 1

        if maxDeltaInd == 0:
            break
        prunedRoute.pop(maxDeltaInd)
        if iterations > 0:
            iterations = iterations - 1
            if iterations == 0:
                break

    return prunedRoute
