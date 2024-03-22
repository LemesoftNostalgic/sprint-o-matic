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

from .mathUtils import rotateVector, distanceBetweenPoints, angleOfLine, calculatePathDistance
from .utils import getSemiSlowdownFactor, getSlowdownFactor, getVerySlowdownFactor
from .routeAI import lookupContains


superSpeedupFactor = 2.0

angleStepBasic = math.pi / 128
angleStep = angleStepBasic

atControlThreshold = 3
quiteCloseToControlThreshold = 15
longLapThreshold = 80
longLapEveryOtherFlag = True
playerRoute = []

pacemakerHandicapFraction = [0.0, 0.2, 0.0, 0.4]
pacemakerFactors = [1.0, 1.0, 1.1, 1.2]
minPacemakerThresholds = [0, 10, 0, 15]


def stepAdvancer(saLookup, ssaLookup, vsaLookup, pos, angle, speed, speedupFactor):
    xStep, yStep = rotateVector(angle, 1.0)

    xStep = xStep * speedupFactor
    yStep = yStep * speedupFactor

    if lookupContains(saLookup, (pos[0] + xStep, pos[1] + yStep)):
        xStep = xStep / getSlowdownFactor()
        yStep = yStep / getSlowdownFactor()
    elif lookupContains(ssaLookup, (pos[0] + xStep, pos[1] + yStep)):
        xStep = xStep / getSemiSlowdownFactor()
        yStep = yStep / getSemiSlowdownFactor()
    elif lookupContains(vsaLookup, (pos[0] + xStep, pos[1] + yStep)):
        xStep = xStep / getVerySlowdownFactor()
        yStep = yStep / getVerySlowdownFactor()

    return (pos[0] + xStep, pos[1] + yStep)


momentum = 1.0
# tries to behave naturally with buildings, bushes, etc.
def calculateNextStep(faLookup, saLookup, ssaLookup, vsaLookup, tunnelLookup, pos, angle, movement, speed, metersPerPixel):
    global angleStep
    global momentum
    if movement and momentum > 0.55:
        momentum = momentum - 0.1
    if not movement and momentum < 0.95:
        momentum = momentum + 0.1

    dangles = [0, -math.pi/16, math.pi/16, -math.pi/8, math.pi/8, -math.pi/8-math.pi/16, math.pi/8+math.pi/16, -math.pi/4, math.pi/4, -(math.pi/4 + math.pi/16), (math.pi/4 + math.pi/16)]
    safeToRun = True
    for da in dangles:
        xStep, yStep = rotateVector(angle + da, 1.0)

        safeToRun = True
        if lookupContains(faLookup, (pos[0] + xStep, pos[1] + yStep)):
            safeToRun = False
            continue

        if da < 0:
            if not movement:
                angle = angle - angleStep
            safeToRun = False # small step, not safe just yet
        elif da > 0:
            if not movement:
                angle = angle + angleStep
            safeToRun = False # small step, not safe just yet
        break

    if safeToRun:
        halfSafeToRun = True
        for da in dangles:
            xStep, yStep = rotateVector(angle + da, 1.0)
            halfSafeToRun = True
            if lookupContains(faLookup, (pos[0] + 2 * xStep, pos[1] + 2 * yStep)):
                halfSafeToRun = False
                continue

            if da < 0:
                if not movement:
                    angle = angle - angleStep
                halfSafeToRun = False # small step, not safe just yet
            elif da > 0:
                if not movement:
                    angle = angle + angleStep
                halfSafeToRun = False # small step, not safe just yet
            break
        quarterSafeToRun = True
        for da in dangles:
            xStep, yStep = rotateVector(angle + da, 1.0)
            quarterSafeToRun = True
            if lookupContains(faLookup, (pos[0] + 3 * xStep, pos[1] + 3 * yStep)):
                quarterSafeToRun = False
                continue

            if da < 0:
                if not movement:
                    angle = angle - angleStep
                quarterSafeToRun = False # small step, not safe just yet
            elif da > 0:
                if not movement:
                    angle = angle + angleStep
                quarterSafeToRun = False # small step, not safe just yet
            break

        safetyFactor = 1.0
        if not halfSafeToRun:
            safetyFactor = 0.25
        elif not quarterSafeToRun:
            safetyFactor = 0.5
        pos = stepAdvancer(saLookup, ssaLookup, vsaLookup, pos, angle, speed, (momentum * safetyFactor) / metersPerPixel)

    playerRoute.append(pos)

    
    return pos, angle, lookupContains(tunnelLookup, pos)


def closeToControl(pos, ctrl):
    if distanceBetweenPoints(pos, ctrl) < atControlThreshold:
        return True
    return False

def quiteCloseToControl(pos, ctrl):
    if distanceBetweenPoints(pos, ctrl) < quiteCloseToControlThreshold:
        return True
    return False

longLapEveryOtherFlag = True
def longLapEveryOther(ctrl1, ctrl2):
    global longLapEveryOtherFlag
    dist = distanceBetweenPoints(ctrl1, ctrl2)
    if dist >= longLapThreshold:
        retval = longLapEveryOtherFlag
        longLapEveryOtherFlag = False if longLapEveryOtherFlag else True
        return retval
    longLapEveryOtherFlag = True
    return False

def getPacemakerThreshold(inputPath, pacemakerInd):
    return max(minPacemakerThresholds[pacemakerInd], int(calculatePathDistance(inputPath) * pacemakerHandicapFraction[pacemakerInd]))


def getPacemakerPos(saLookup, ssaLookup, vsaLookup, tunnelLookup, inputPath, steps, speed, metersPerPixel, pacemakerInd):
    index = 0
    path = inputPath.copy()
    pos = path[index]
    dist = distanceBetweenPoints(path[index], path[index + 1])
    angle = angleOfLine([path[index], path[index + 1]])
    for step in range(steps):
        pos = stepAdvancer(saLookup, ssaLookup, vsaLookup, pos, angle, 1.0, pacemakerFactors[pacemakerInd] / metersPerPixel)
        if distanceBetweenPoints(path[index], pos) >= dist:
            index = index + 1
            pos = path[index]
            if index + 1 >= len(path):
                break
            dist = distanceBetweenPoints(path[index], path[index + 1])
            angle = angleOfLine([path[index], path[index + 1]])

    return pos, angle, lookupContains(tunnelLookup, pos)


def generateAngleStep():
    global angleStep

    retval = angleStep
    if angleStep < 5 * angleStepBasic:
        angleStep = angleStep + angleStepBasic
    return retval


def normalizeAngleStep():
    global angleStep    
    angleStep = angleStepBasic


def defaultAngle():
    return math.pi


def startOverPlayerRoute():
    global playerRoute
    playerRoute = []


def getPlayerRoute():
    return playerRoute
