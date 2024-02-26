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

from .mathUtils import angleBetweenLineSegments, distanceBetweenPoints
from .pathPruning import pruneEnsureLineOfSight
from .routeAI import checkRouteExists


firstControlMinDistance = 100
pickMaxTime = 0.1
pickDistMaxTime = 1.0
totMaxTime = 30.0

def pickLegLen(distribution, metersPerPixel):
    a = random.random()
    tot = 0.0
    for slot in distribution:
        if a >= tot and a < tot + slot[2]:
            return slot[0] / metersPerPixel, slot[1] / metersPerPixel
        tot = tot + slot[2]

    # just in case, should never end up here
    return distribution[0][0] / metersPerPixel, distribution[-1][1] / metersPerPixel


def pickAutoControl(cfg, ctrls):
    index = 0
    start_time = time.time()
    while True:
        index = int(len(cfg) * random.random())
        if type(cfg[index]) is not tuple:
            if time.time() - start_time > pickMaxTime:
                return None
            continue
        if cfg[index] in ctrls:
            if time.time() - start_time > pickMaxTime:
                return None
            continue
        break
    return cfg[index]


def pickDistAutoControl(cfg, ctrls, distribution, metersPerPixel, faLookup):
    start_time = time.time()
    easyOneOutOf = 2
    isDifficultControl = True
    while True:
        minlen, maxlen = pickLegLen(distribution, metersPerPixel)
        if len(ctrls) == 1:
            lenadjust =  max(minlen, firstControlMinDistance) - minlen
            maxlen = maxlen + lenadjust
            minlen = minlen + lenadjust
        for index in range(0,50):
            candidate = pickAutoControl(cfg, ctrls)
            if candidate is None:
                return None, None, None
            # compare to all the ones so far
            nearnessGood = True
            for ctrl in ctrls[:-1]:
                if distanceBetweenPoints(candidate, ctrl) < minlen/2:
                    nearnessGood = False
            if not nearnessGood:
                continue
            # then more strictly to the previous one
            dist = distanceBetweenPoints(candidate, ctrls[-1])
            if dist >= minlen and dist < maxlen:
                break
        if time.time() - start_time > pickDistMaxTime:
            return None, None, None

        if dist < minlen or dist >= maxlen:
            continue
        if len(ctrls) > 1 and angleBetweenLineSegments([ctrls[-2], ctrls[-1]], [ctrls[-1], candidate]) > 0.65 * math.pi:
            continue

        if pruneEnsureLineOfSight(candidate, ctrls[-1], faLookup) != None:
            isDifficultControl = False

        if not isDifficultControl and random.randrange(easyOneOutOf) != 0:
            continue

        # first time no continue -> success
        return candidate, dist, isDifficultControl


def createAutoControls(cfg, trackLength, distribution, metersPerPixel, faLookup, isWorld):
    totdist = 0
    ctrls = []
    start_tot_time = time.time()
    ctrl = pickAutoControl(cfg, ctrls)
    ctrls.append(ctrl)
    numDifficultControls = 0
    while (len(ctrls) < 25 and totdist < trackLength) or len(ctrls) < 3:
        ctrl, dist, isDifficultControl = pickDistAutoControl(cfg, ctrls, distribution, metersPerPixel, faLookup)
        if isDifficultControl:
            numDifficultControls = numDifficultControls + 1
        if ctrl is None:
            return [], 0
        if isWorld:
            if checkRouteExists(ctrl, ctrls[-1], faLookup):
                ctrls.append(ctrl)
                totdist = totdist + dist
            elif len(ctrls) < 2:
                ctrls = []
                ctrl = pickAutoControl(cfg, ctrls)
                ctrls.append(ctrl)
        else:
            ctrls.append(ctrl)
            totdist = totdist + dist

        if time.time() - start_tot_time > totMaxTime:
            break

    return ctrls, numDifficultControls


def createPairedList(trivialList):
    pairedList = []
    for index in range(len(trivialList) - 1):
        pairedList.append([trivialList[index], trivialList[index + 1]])
    return pairedList
        
