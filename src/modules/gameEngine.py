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

    if speed == "superfast":
        xStep = xStep * superSpeedupFactor * speedupFactor
        yStep = yStep * superSpeedupFactor * speedupFactor
            
    if lookupContains(saLookup, (pos[0] + xStep, pos[1] + yStep)):
        xStep = xStep * speedupFactor / getSlowdownFactor()
        yStep = yStep * speedupFactor / getSlowdownFactor()
    elif lookupContains(ssaLookup, (pos[0] + xStep, pos[1] + yStep)):
        xStep = xStep * speedupFactor / getSemiSlowdownFactor()
        yStep = yStep / getSemiSlowdownFactor()
    elif lookupContains(vsaLookup, (pos[0] + xStep, pos[1] + yStep)):
        xStep = xStep * speedupFactor / getVerySlowdownFactor()
        yStep = yStep * speedupFactor / getVerySlowdownFactor()

    return (pos[0] + xStep, pos[1] + yStep)


# tries to behave naturally with buildings, bushes, etc.
def calculateNextStep(faLookup, saLookup, ssaLookup, vsaLookup, tunnelLookup, pos, angle, movement, speed, metersPerPixel):
    global angleStep
    dangles = [0, -math.pi/32, math.pi/32, -math.pi/16, math.pi/16, -math.pi/8, math.pi/8, -math.pi/4, math.pi/4, -(math.pi/4 + math.pi/8), (math.pi/4 + math.pi/8)]
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
        pos = stepAdvancer(saLookup, ssaLookup, vsaLookup, pos, angle, speed, 1.0 / metersPerPixel)

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
    path.reverse()
    pos = path[index]
    dist = distanceBetweenPoints(path[index], path[index + 1])
    angle = angleOfLine([path[index], path[index + 1]])
    for step in range(steps):
        pos = stepAdvancer(saLookup, ssaLookup, vsaLookup, pos, angle, speed, pacemakerFactors[pacemakerInd] / metersPerPixel)
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
