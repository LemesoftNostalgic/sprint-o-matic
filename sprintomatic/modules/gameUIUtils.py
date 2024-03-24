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
import pygame
import os
import time
import math

from .mathUtils import triangleCreator, rotateVector, angleOfLine
from .utils import getPackagePath

xReference = 1920
yReference = 1080
xCurrent = 1920
yCurrent = 1080

bigScreen = None

pacemakerColor = [pygame.Color(255, 0, 0), pygame.Color(255, 0, 0), pygame.Color(140, 95, 25), pygame.Color(0, 255, 0)]

def getApplicationTitle():
    return "Sprint-O-Matic"

def getAnalysisResultsFileBase():
    return getApplicationTitle() + "-analysis-"

def getMasterFont():
    font = os.path.join('fonts', 'Aclonica-Regular.ttf')
    if getPackagePath():
        font = os.path.join(getPackagePath(), font)
    return font

def getStopKey():
    return 41

def getPerfKey():
    return 19

def getBackKey():
    return 42

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

def getShortestRouteColor():
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

def convertXCoordinateSpecificSurface(specificSurface, xCoord):
    xSpecificSurface, yDummy = specificSurface.get_size()
    return int((xCoord * xSpecificSurface) / xReference)

def convertYCoordinateSpecificSurface(specificSurface, yCoord):
    xDummy, ySpecificSurface = specificSurface.get_size()
    return int((yCoord * ySpecificSurface) / yReference)

def convertYCoordinate(yCoord):
    return int((yCoord * yCurrent) / yReference)

def getBigScreen():
    return bigScreen

def getTimerStep():
    return 100

def getTimerStepSeconds(speedMode):
    if speedMode == "superfast":
        return 0.050
    return 0.080

def getEffectStepStart(benchmark):
    if benchmark == "phone":
        return 64
    else:
        return 64


def uiEarlyInit(fullScreen, benchmark):
    global xCurrent
    global yCurrent
    global bigScreen

    pygame.init()
#    if benchmark == "phone":
#        bigScreen = pygame.display.set_mode((640,480))
    if fullScreen:
        bigScreen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
    else:
        bigScreen = pygame.display.set_mode((0,0))
    pygame.mouse.set_visible(False)
    xCurrent, yCurrent = bigScreen.get_size()

    portrait = False
    if xCurrent < yCurrent:
        portrait = True
    return portrait

    
def uiDrawLine(surfa, color, start, end, width):
    angle = angleOfLine([start, end])

    for ind in range(1, width):
        for dir in [-1, 1]:
            inc = rotateVector(angle + dir * math.pi / 2, 0.5)
            st = (start[0] + ind * inc[0], start[1] + ind * inc[1])
            ed = (end[0] + ind * inc[0], end[1] + ind * inc[1])
            pygame.draw.aalines(surfa, color, False, [st, ed])

    pygame.draw.aalines(surfa, color, False, [start, end])


def uiDrawCircle(surfa, color, center, radius, width):
    numSteps = int(radius) * 4
    angleStep = (2 * math.pi) / numSteps
    for ind in range(numSteps):
        startV = rotateVector(ind * angleStep, radius)
        endV = rotateVector((ind + 1) * angleStep, radius)
        start = (center[0]+startV[0], center[1]+startV[1])
        end = (center[0]+endV[0], center[1]+endV[1])
        uiDrawLine(surfa, color, start, end, width)
    

def uiDrawTriangle(surfa, radius, angle, pos, wd):
    triangle = triangleCreator(radius, angle, pos)
    uiDrawLine(surfa, getTrackColor(), triangle[0], triangle[1], wd)
    uiDrawLine(surfa, getTrackColor(), triangle[1], triangle[2], wd)
    uiDrawLine(surfa, getTrackColor(), triangle[2], triangle[0], wd)



slideCtrStart = 12
slideCtrStartUp = 12
slideCtrStartDown = 12
slideCtr = 0
bigScreenCopy = None
bigScreenNew = None
bigScreenMul = None
def uiSubmitSlide(textStr, portrait):
    global slideCtr
    global bigScreenCopy
    global bigScreenNew
    global slideCtrStart
    if bigScreen:
        if not portrait:
            fs = convertXCoordinate(48)
        else:
            fs = int(convertYCoordinate(48) / 1.8)
        slideCtr = slideCtrStartUp
        sideCtrStart = slideCtrStartUp
        bigScreenCopy = bigScreen.copy()
        bigScreenNew = bigScreen.copy()
        bigScreenNew.fill(getBlackColor())
        middle = tuple(ti/2.0 for ti in bigScreenNew.get_size())
        slideText = pygame.font.Font(getMasterFont(), fs).render(textStr, True, getCreditColor())
        slideTextRect = slideText.get_rect()
        slideTextRect.center = middle
        bigScreenNew.blit(slideText, slideTextRect)


def uiSubmitTwoSlides(textStr1, textStr2, portrait):
    global slideCtr
    global bigScreenCopy
    global bigScreenNew
    global slideCtrStart
    if bigScreen:
        if not portrait:
            fs = convertXCoordinate(48)
        else:
            fs = int(convertYCoordinate(48) / 1.8)
        slideCtr = slideCtrStartUp
        sideCtrStart = slideCtrStartUp
        bigScreenCopy = bigScreen.copy()
        bigScreenNew = bigScreen.copy()
        bigScreenNew.fill(getBlackColor())
        middle = tuple(ti/2.0 for ti in bigScreenNew.get_size())
        slideText = pygame.font.Font(getMasterFont(), fs).render(textStr1, True, getCreditColor())
        slideTextRect = slideText.get_rect()
        slideTextRect.center = middle
        bigScreenNew.blit(slideText, slideTextRect)

        middle = tuple(ti/2.0 for ti in bigScreenNew.get_size())
        middle = (middle[0], middle[1] + slideTextRect[3])
        slideText = pygame.font.Font(getMasterFont(), fs).render(textStr2, True, getCreditColor())
        slideTextRect = slideText.get_rect()
        slideTextRect.center = middle
        bigScreenNew.blit(slideText, slideTextRect)

def uiSubmitTextListSlide(textStrList, portrait):
    global slideCtr
    global bigScreenCopy
    global bigScreenNew
    global slideCtrStart
    if bigScreen:
        if not portrait:
            fs = convertXCoordinate(32)
        else:
            fs = int(convertYCoordinate(32) / 2.2)
        slideCtr = slideCtrStartUp
        sideCtrStart = slideCtrStartUp
        bigScreenCopy = bigScreen.copy()
        bigScreenNew = bigScreen.copy()
        bigScreenNew.fill(getBlackColor())
        ind = 2
        for textStr in textStrList:
            ind = ind + 1
            middle = (bigScreenNew.get_size()[0]//2, (ind * bigScreenNew.get_size()[0])//(2*(len(textStrList) + 5)))

            slideText = pygame.font.Font(getMasterFont(), fs).render(textStr, True, getCreditColor())
            slideTextRect = slideText.get_rect()
            slideTextRect.center = middle
            bigScreenNew.blit(slideText, slideTextRect)


def uiFadeVisibleSlide():
    global slideCtr
    global bigScreenCopy
    global bigScreenNew
    global slideCtrStart
    if bigScreen:
        slideCtr = slideCtrStartDown
        slideCtrStart = slideCtrStartDown
        if bigScreenCopy == None:
            bigScreenCopy = bigScreen.copy()
        bigScreenCopy.fill(getBlackColor())
        bigScreenNew = bigScreen.copy()


def uiFadeUnVisibleSlide():
    global slideCtr
    global bigScreenCopy
    global bigScreenNew
    global slideCtrStart
    if bigScreen:
        slideCtr = slideCtrStartDown
        slideCtrStart = slideCtrStartDown
        if bigScreenNew == None:
            bigScreenNew = bigScreen.copy()
        bigScreenNew.fill(getBlackColor())
        bigScreenCopy = bigScreen.copy()


def uiUnSubmitSlide():
    global slideCtr
    global bigScreenCopy
    global bigScreenNew
    global slideCtrStart
    if bigScreen:
        slideCtr = slideCtrStartDown
        slideCtrStart = slideCtrStartDown
        bigScreenCopy = bigScreenNew
        bigScreenNew = bigScreen.copy()


def uiSubFlip():
    global slideCtr
    global slideCtrStart
    global bigScreenMul
    if bigScreen:
        step = slideCtr * (255 // slideCtrStart)
        stepBack = 255 - step
        stepCol = (step, step, step)
        stepBackCol = (stepBack, stepBack, stepBack)
        bigScreen.fill(stepCol)
        if bigScreenMul == None:
            bigScreenMul = bigScreen.copy()
        bigScreenMul.fill(stepBackCol)
        bigScreen.blit(bigScreenCopy, (0,0), special_flags=pygame.BLEND_MULT)
        bigScreenMul.blit(bigScreenNew, (0,0), special_flags=pygame.BLEND_MULT)
        bigScreen.blit(bigScreenMul, (0,0), special_flags=pygame.BLEND_ADD)


uiFlipFreq = 0.05
async def uiFlip(fast):
    global slideCtr
    if not fast:
        if slideCtr > 0:
            while slideCtr > 0:
                slideCtr = slideCtr - 1
                uiSubFlip()
                if slideCtr > 0:
                    pygame.display.flip()
                    await asyncio.sleep(uiFlipFreq)
    else:
        if slideCtr > 0:
            slideCtr = slideCtr - 1
            uiSubFlip()

    # and then the final flip
    pygame.display.flip()


def uiLateQuit():
    getBigScreen().fill(getWhiteColor())
    pygame.display.flip()
    pygame.quit()


async def uiFlushEvents():
    retval = False
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.scancode == getStopKey():
                retval = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[1]:
                retval = True
        elif event.type == pygame.QUIT:
            retval = True

    # attach a slideware starter here
    await uiFlip(True)

    return retval
