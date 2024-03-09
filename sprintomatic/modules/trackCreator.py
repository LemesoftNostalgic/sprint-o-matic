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

import math
import random
import time
import asyncio

from .mathUtils import angleBetweenLineSegments, distanceBetweenPoints, distanceBetweenPointAndLine, calculatePathDistance
from .gameUIUtils import uiFlushEvents
from .pathPruning import pruneEnsureLineOfSightExt, pruneShortestRouteExt
from .routeAI import calculateCoarseRouteExt, calculateShortestRoute, slowAccurateCalculateShortestRouteAsync


firstControlMinDistance = 100
maxDifficultAttempts = 10
pickDistMaxTime = 1.0
pickMaxTime = pickDistMaxTime / maxDifficultAttempts
totMaxTime = 15.0
totMaxTimeAmaze = 40.0

def pickLegLen(distribution, metersPerPixel):
    a = random.random()
    tot = 0.0
    for slot in distribution:
        if a >= tot and a < tot + slot[2]:
            return slot[0] / metersPerPixel, slot[1] / metersPerPixel
        tot = tot + slot[2]

    # just in case, should never end up here
    return distribution[0][0] / metersPerPixel, distribution[-1][1] / metersPerPixel


def fastGetDecentControl(cfg, ctrls, minlen, maxlen):
    startingPoint = int(len(cfg) * random.random())
    if not ctrls:
        return startingPoint
    length = len(cfg)
    for ind in range(length):
        realInd = int((startingPoint + ind) % length)
        dist = distanceBetweenPoints(cfg[realInd], ctrls[-1])
        if dist > minlen and dist < maxlen * 3:
            return realInd
    return None


def pickAutoControl(cfg, ctrls, minlen, maxlen):
    index = 0
    start_time = time.time()
    secondBestIndex = None
    secondBestDist = 0
    secondBestScore = 10000000000
    dist = 0.0

    while True:
        index = fastGetDecentControl(cfg, ctrls, minlen, maxlen)
        if index == None:
            return None, None

        dist = 0.0
        toContinue = False
        smallestOvershoot = 10000
        smallestAngleOvershoot = 10000
        biggestAvgNearness = 0
        biggestAvgLineNearness = 0

        if type(cfg[index]) is not tuple:
            if time.time() - start_time > pickMaxTime:
                return None, None
            continue

        elif cfg[index] in ctrls:
            if time.time() - start_time > pickMaxTime:
                return None, None
            continue

        elif ctrls:

            dist = distanceBetweenPoints(cfg[index], ctrls[-1])
            if dist < minlen:
                if time.time() - start_time > pickMaxTime:
                    return None, None
                continue
            elif dist > maxlen:
                if dist < smallestOvershoot:
                    smallestOvershoot = dist
                toContinue = True

            if len(ctrls) > 1:
                anglebtw = angleBetweenLineSegments([ctrls[-2], ctrls[-1]], [ctrls[-1], cfg[index]])
                while anglebtw < 0:
                    anglebtw = anglebtw + 2 * math.pi
                while anglebtw > 2 * math.pi:
                    anglebtw = anglebtw - 2 * math.pi
                if anglebtw > math.pi:
                    anglebtw = 2 * math.pi - anglebtw
                if anglebtw > 0.55 * math.pi:
                    if anglebtw < smallestAngleOvershoot:
                        smallestAngleOvershoot = anglebtw
                    toContinue = True

            totNearness = 0
            totLineNearness = 0
            for ctrl in ctrls[:-1]:
                nearness = distanceBetweenPoints(cfg[index], ctrl)
                if nearness < minlen / 2:
                    if time.time() - start_time > pickMaxTime:
                        return None, None
                    continue
                totNearness = totNearness + nearness
                lineNearness = distanceBetweenPointAndLine(cfg[index], [ctrl, ctrls[-1]], nearness/2)
                totLineNearness = totLineNearness + lineNearness

            if len(ctrls) > 1:
                if totNearness / (len(ctrls) - 1) > biggestAvgNearness:
                    biggestAvgNearness = totNearness / (len(ctrls) - 1)
                if totLineNearness / (len(ctrls) - 1) > biggestAvgLineNearness:
                    biggestAvgLineNearness = totLineNearness / (len(ctrls) - 1)

        if toContinue:
            score = (smallestOvershoot - maxlen) / maxlen + 2 * (smallestAngleOvershoot - 0.65 * math.pi ) / (0.65 * math.pi) + 6 * biggestAvgNearness + 2 * biggestAvgLineNearness
            if score < secondBestScore:
                secondBestIndex = index
                secondBestScore = score
                secondBestDist = smallestOvershoot

            if time.time() - start_time > pickMaxTime:
                return cfg[secondBestIndex], secondBestDist

            continue

        break
    return cfg[index], dist


def pickDistAutoControl(cfg, ctrls, distribution, metersPerPixel, faLookups):
    start_time = time.time()
    easyOneOutOf = 2
    isDifficultControl = True
    difficultAttemptCtr = maxDifficultAttempts
    while True:
        minlen, maxlen = pickLegLen(distribution, metersPerPixel)

        # first leg cannot be very short
        if len(ctrls) == 1:
            lenadjust =  max(minlen, firstControlMinDistance) - minlen
            maxlen = maxlen + lenadjust
            minlen = minlen + lenadjust

        candidate, dist = pickAutoControl(cfg, ctrls, minlen, maxlen)
        if candidate is None:
                return None, None, None

        if time.time() - start_time > pickDistMaxTime:
            return None, None, None

        if pruneEnsureLineOfSightExt(candidate, ctrls[-1], faLookups, 0) != None:
            isDifficultControl = False

        if not isDifficultControl and difficultAttemptCtr > 0:
            difficultAttemptCtr = difficultAttemptCtr - 1
            continue

        # first time no continue -> success
        return candidate, dist, isDifficultControl


async def createAutoControls(cfg, trackLength, distribution, metersPerPixel, faLookups, saLookups, ssaLookups, vsaLookups, pacemakerInd):
    cfgCopy = cfg.copy()
    totdist = 0
    precision = 0 #two is too big
    ctrls = []
    shortests = []
    start_tot_time = time.time()
    ctrl, dummy_dist = pickAutoControl(cfgCopy, ctrls, 0, 1000000)
    ctrls.append(ctrl)
    cfgCopy.pop(cfgCopy.index(ctrl))
    numDifficultControls = 0
    while (len(ctrls) < 25 and totdist < trackLength) or len(ctrls) < 3:
        ctrl, dist, isDifficultControl = pickDistAutoControl(cfgCopy, ctrls, distribution, metersPerPixel, faLookups)
        if isDifficultControl:
            numDifficultControls = numDifficultControls + 1
        if ctrl is None or await uiFlushEvents():
            return [], []

        preComputed, dummy_jumps = calculateCoarseRouteExt(ctrls[-1], ctrl, faLookups, precision, True, True, 0)
        if len(preComputed) > 1:
            ctrls.append(ctrl)
            cfgCopy.pop(cfgCopy.index(ctrl))
            totdist = totdist + dist
            shortests.append([preComputed])
        elif len(ctrls) < 2: # also change first one in this case
            ctrls = []
            cfgCopy = cfg.copy()
            ctrl, dummy_dist = pickAutoControl(cfgCopy, ctrls, 0, 1000000)
            ctrls.append(ctrl)
            cfgCopy.pop(cfgCopy.index(ctrl))
        if time.time() - start_tot_time > totMaxTime:
            break

        await asyncio.sleep(0)

    # only complete the work afterwards
    start_tot_time = time.time()
    for ind in range(len(shortests)):
        shortests[ind] = [calculateShortestRoute([ctrls[ind], ctrls[ind + 1], faLookups, saLookups, ssaLookups, vsaLookups, precision, pacemakerInd, shortests[ind][0].copy()])]
        if time.time() - start_tot_time > totMaxTime:
            break

    return ctrls, shortests


deAmazeFactor = 4 # how small challenges are accepted. the bigger the smaller
async def createAmazeControls(cfg, distribution, metersPerPixel, faLookups, saLookups, ssaLookups, vsaLookups):
    normalizedDifference = 0.0
    start_tot_time = time.time()

    secondBestCtr = 4
    secondBestBeautifiedRight = []
    secondBestBeautifiedLeft = []
    secondBestNormalizedDifference = 0.0
    secondBestCtrls = []
    secondBestCtrl = (0,0)
    
    while True:
        if time.time() - start_tot_time > totMaxTimeAmaze or await uiFlushEvents():
            return [], [], [], [], 0.0
        ctrls = []
        ctrl, dummy_dist = pickAutoControl(cfg, ctrls, 0, 1000000)
        ctrls.append(ctrl)

        ctrl, dist, isDifficultControl = pickDistAutoControl(cfg, ctrls, distribution, metersPerPixel, faLookups)
        if ctrl is None:
            continue
        if not isDifficultControl:
            continue
        dist = distanceBetweenPoints(ctrls[-1], ctrl)

        # check there is both right and left alternative
        preComputedLeft, jumps = calculateCoarseRouteExt(ctrls[-1], ctrl, faLookups, 2, True, False, dist * 20)
        if jumps < 1 or len(preComputedLeft) < 3 or calculatePathDistance(preComputedLeft) < dist + dist / deAmazeFactor:
            continue
        if time.time() - start_tot_time > totMaxTimeAmaze or await uiFlushEvents():
            return [], [], [], [], 0.0

        preComputedRight, jumps = calculateCoarseRouteExt(ctrls[-1], ctrl, faLookups, 2, False, True, dist * 20)
        if len(preComputedRight) < 3 or calculatePathDistance(preComputedRight) < dist + dist / deAmazeFactor:
            continue
        if time.time() - start_tot_time > totMaxTimeAmaze or await uiFlushEvents():
            return [], [], [], [], 0.0

        beautifiedLeft = preComputedLeft
        beautifiedRight = preComputedRight
        beautifiedLeft = pruneShortestRouteExt(preComputedLeft, faLookups, saLookups, ssaLookups, vsaLookups, 0)
        if time.time() - start_tot_time > totMaxTimeAmaze or await uiFlushEvents():
            return [], [], [], [], 0.0

        beautifiedRight = pruneShortestRouteExt(preComputedRight, faLookups, saLookups, ssaLookups, vsaLookups, 0)
        if time.time() - start_tot_time > totMaxTimeAmaze or await uiFlushEvents():
            return [], [], [], [], 0.0

        normalizedDifference = 2 * abs(calculatePathDistance(beautifiedRight) - calculatePathDistance(beautifiedLeft)) / abs(calculatePathDistance(beautifiedRight) + calculatePathDistance(beautifiedLeft))
        if normalizedDifference < 0.01 or normalizedDifference > 0.2:
            if secondBestCtr > 0:
                secondBestCtr = secondBestCtr - 1
                secondBestBeautifiedRight = beautifiedRight.copy()
                secondBestBeautifiedLeft = beautifiedLeft.copy()
                secondBestNormalizedDifference = normalizedDifference
                secondBestCtrls = ctrls.copy()
                secondBestCtrl = ctrl
                continue
            else:
                beautifiedRight = secondBestBeautifiedRight
                beautifiedLeft = secondBestBeautifiedLeft
                normalizedDifference = secondBestNormalizedDifference
                ctrls = secondBestCtrls
                ctrl = secondBestCtrl
                # proceed bravely ahead

        ctrls.append(ctrl)
        break

        await asyncio.sleep(0)

    shortests = []
    for ind in range(len(ctrls) - 1):
        shortests.append([await slowAccurateCalculateShortestRouteAsync([ctrls[ind], ctrls[ind + 1], faLookups, saLookups, ssaLookups, vsaLookups, 2, 0])])
        if await uiFlushEvents():
            return [], [], [], [], 0.0
        if not shortests[ind][0]:
            shortests[ind] = [await slowAccurateCalculateShortestRouteAsync([ctrls[ind], ctrls[ind + 1], faLookups, saLookups, ssaLookups, vsaLookups, 3, 0])]
            if not shortests[ind][0]:
                return [], [], [], [], 0.0

    return ctrls, shortests, beautifiedLeft, beautifiedRight, normalizedDifference


def createPairedList(trivialList):
    pairedList = []
    for index in range(len(trivialList) - 1):
        pairedList.append([trivialList[index], trivialList[index + 1]])
    return pairedList
        
