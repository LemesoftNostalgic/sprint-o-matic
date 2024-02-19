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

import pygame
import os

from .mathUtils import triangleCreator
from .utils import getPackagePath

xReference = 1920
yReference = 1080
xCurrent = 1920
yCurrent = 1080

bigScreen = None

pacemakerColor = [pygame.Color(255, 0, 0), pygame.Color(255, 0, 0), pygame.Color(140, 95, 25), pygame.Color(0, 255, 0)]

def getApplicationTitle():
    return "Sprint-O-Matic"

def getMasterFont():
    font = os.path.join('fonts', 'Aclonica-Regular.ttf')
    if getPackagePath():
        font = os.path.join(getPackagePath(), font)
    return font

def getStopKey():
    return 41

# an easter egg to get the autotest running from UI
autoTestCode = [23, 22, 8, 23, 18, 23, 24, 4]
def checkAutoTestKey(key):
    global autoTestCode
    if autoTestCode and key == autoTestCode[-1]:
        autoTestCode.pop()
        if autoTestCode == []:
            return True
        return False
    return False

def getUpKey():
    return 82

def getLeftKey():
    return 80

def getRightKey():
    return 79

def getDownKey():
    return 81

def getEnterKey():
    return 40

def getSpaceKey():
    return 44

def getPlayerColor():
    return pygame.Color(0,0,255)

def getTrackColor():
    return pygame.Color(255, 0, 0)

def getCreditColor():
    return pygame.Color(255, 215, 0)

def getPacemakerColor(pacemakerInd):
    return pacemakerColor[pacemakerInd]

def getPlayerRouteColor():
    return pygame.Color(0, 0, 255)

def getBlackColor():
    return pygame.Color(0, 0, 0)

def getFinishTextColor():
    return pygame.Color(0, 64,32)

def getWhiteColor():
    return pygame.Color(255, 255, 255)

def getGreyColor():
    return pygame.Color(234, 234, 234)

def convertXCoordinate(xCoord):
    return int((xCoord * xCurrent) / xReference)

def convertYCoordinate(yCoord):
    return int((yCoord * yCurrent) / yReference)

def getBigScreen():
    return bigScreen

def getTimerStep():
    return 100


def uiEarlyInit(fullScreen):
    global xCurrent
    global yCurrent
    global bigScreen

    pygame.init()
    if fullScreen:
        bigScreen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
    else:
        bigScreen = pygame.display.set_mode((0,0))
    pygame.mouse.set_visible(False)
    xCurrent, yCurrent = bigScreen.get_size()


def uiFlushEvents():
    for event in pygame.event.get():
        pass

def uiDrawTriangle(surf, radius, angle, pos, wd):
    triangle = triangleCreator(radius, angle, pos)
    pygame.draw.line(surf, getTrackColor(), triangle[0], triangle[1], width = wd)
    pygame.draw.line(surf, getTrackColor(), triangle[1], triangle[2], width = wd)
    pygame.draw.line(surf, getTrackColor(), triangle[2], triangle[0], width = wd)


def uiLateQuit():
    pygame.quit()
