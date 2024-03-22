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
import math
import time
import asyncio
from datetime import datetime
from random import randrange

from .gameUIUtils import getMasterFont, getStopKey, getLeftKey, getRightKey, getPlayerColor, getTrackColor, getShortestRouteColor, getCreditColor, getPacemakerColor, getPlayerRouteColor, getFinishTextColor, getWhiteColor, convertXCoordinate, convertXCoordinateSpecificSurface, convertYCoordinateSpecificSurface, convertYCoordinate, getBigScreen, getTimerStepSeconds, getAnalysisResultsFileBase, uiFlip, uiUnSubmitSlide, uiDrawLine, uiDrawCircle, getEffectStepStart
from .mathUtils import rotatePoint, fromRadiansToDegrees, distanceBetweenPoints, triangleCreator, getBoundingBox
from .infoBox import showInfoBoxTxt, updateInfoTxtByEvent
from .perfSuite import perfShowResults, perfAddStart, perfAddStop

circleRadius = 15
circleSpacing = 5
circleRadiusMargin = 18
triangleRadius = 15
controlApproachZoom = 1.2
controlApproachZoomUsed = False
metersPerPixel = 1
fingerDirection = ""
prevReachedControl = 999999
bboxThresh = 64
prevBigRect = None

finishTextStr =      "Finish time: "
finishTextStr2 =     "    Distance: "
finishTextStr3 =     " m"
finishTextStr4 =     "    Runner error: "
finishTextStr5 =     " %"

amazeStr1 =      "          A MAZE BEGINS!   LEVEL: "
amazeStr2 =      "   TURN TO RUNNING DIRECTION          "

amazeTextStr =      "          LEVEL: "
amazeTextStr2 =     "    RESULT: "
amazeTextStr3 =     "  "
amazeTextStr4 =     "    ANGLE DIFFERENCE: "
amazeTextStr5 =     "°           "

pacemakerTextStr =    ["", "Pacemaker: Aino Inkeri (A.I.) Kiburtz", "Pacemaker: Pertti-Uolevi (P.A.) Keinonen, e.v.v.k.", "Pacemaker: Lex Martin Luthoer, Chem. Engr."]
pacemakerInitTextStr =    "Prepare, a pacemaker waiting in 1st control!"
aiTextStr =    "AI computing dilemma, sorry for the inconvenience..."

mapInfoTextTitles = [ "map: ", "map license: ", "created by: ", "terrain png: ", "terrain png license: ", "created by:" ]

# Intermediate surfaces for the gameplay
oMapEarly = None
leftImage = None
rightImage = None
stopImage = None
oMap = None
oMapMid = None
oMapCopy = None
surf = None
screen = None
screen_rect = None
me = None
surfMe = None

feetPlusStart = 3.0

mousePressed = False

effectControl = 0
effectStep = 0
previousEffectStep = 0
effectStepStart = 64


def uiInit(fileName, imagePath, generatedMap, metersPerPixerInput, benchmark):
    global effectStepStart
    global surfMe
    global leftImage
    global rightImage
    global stopImage
    effectStepStart = getEffectStepStart(benchmark)
    global oMap, oMapEarly, surf, screen, bigScreen, me, metersPerPixel
    if generatedMap is not None:
        oMapEarly = generatedMap
    else:
        oMapEarly = pygame.image.load(fileName)
    leftImage = pygame.image.load(imagePath + "lemesoftnostalgic/turnLeft.png")
    rightImage = pygame.image.load(imagePath + "lemesoftnostalgic/turnRight.png")
    stopImage = pygame.image.load(imagePath + "lemesoftnostalgic/stop.png")

    size = oMapEarly.get_size()
    surfSize = size
    if benchmark == "phone":
        surfWidth = min(getBigScreen().get_size()[0], getBigScreen().get_size()[1])
        surfSize = (surfWidth, surfWidth)
    surf = pygame.Surface(surfSize)
    screen = pygame.Surface(size)

    surf = surf.convert_alpha()
    screen = screen.convert_alpha()
    oMapEarly = oMapEarly.convert_alpha()
    me = tuple(ti/2.0 for ti in size)
    surfMe = tuple(ti/2.0 for ti in surfSize)
    metersPerPixel = metersPerPixerInput
    oMap = None
    oMapMid = None

    pygame.key.set_repeat(200, 50)

    return me


def uiShowFinishText(someSurface, finishTexts, amaze, portrait):
    timeConsumed = finishTexts[0]
    distance = finishTexts[1]
    error = finishTexts[2]

    if not portrait:
        fs = convertXCoordinateSpecificSurface(someSurface, 32)
    else:
        fs = int(convertYCoordinateSpecificSurface(someSurface, 32) / 2.0)

    if timeConsumed and distance and error:
        middle = tuple(ti/2.0 for ti in someSurface.get_size())
        finishTextCenter = (middle[0], middle[1] * 0.05)
        textItself = finishTextStr + timeConsumed + finishTextStr2 + distance + finishTextStr3 + finishTextStr4 + error + finishTextStr5
        if amaze:
            textItself = amazeTextStr + timeConsumed + amazeTextStr2 + distance + amazeTextStr3 + amazeTextStr4 + error + amazeTextStr5
        finishText = pygame.font.Font(getMasterFont(), fs).render(textItself, True, getFinishTextColor())
        finishTextRect = finishText.get_rect()
        finishTextRect.center = finishTextCenter
        pygame.draw.rect(someSurface, getWhiteColor(), finishTextRect, 0)
        someSurface.blit(finishText, finishTextRect)


def uiRenderAmazeText(amazeNum, portrait):
    if not portrait:
        fs = convertXCoordinate(32)
    else:
        fs = int(convertYCoordinate(32) / 2.0)

    if effectStep and effectControl < 1:
        middle = tuple(ti/2.0 for ti in getBigScreen().get_size())
        pacemakerTextCenter = (middle[0], middle[1] * 0.05)
        pacemakerText = pygame.font.Font(getMasterFont(), fs).render(amazeStr1 + str(amazeNum) + amazeStr2, True, getPacemakerColor(2))
        pacemakerTextRect = pacemakerText.get_rect()
        pacemakerTextRect.center = pacemakerTextCenter
        pygame.draw.rect(getBigScreen(), getWhiteColor(), pacemakerTextRect, 0)
        getBigScreen().blit(pacemakerText, pacemakerTextRect)


def uiRenderPacemakerText(pacemakerInd, portrait):

    if effectStep and effectControl <= 1:
        if not portrait:
            fs = convertXCoordinate(48)
        else:
            fs = int(convertYCoordinate(48) / 1.9)
        if effectControl == 1:
            warningStr = pacemakerTextStr[pacemakerInd]
        else:
            warningStr = pacemakerInitTextStr
        middle = tuple(ti/2.0 for ti in getBigScreen().get_size())
        pacemakerTextCenter = (middle[0], middle[1] * 0.1)
        pacemakerText = pygame.font.Font(getMasterFont(), fs).render(warningStr, True, getPacemakerColor(pacemakerInd))
        pacemakerTextRect = pacemakerText.get_rect()
        pacemakerTextRect.center = pacemakerTextCenter
        pygame.draw.rect(getBigScreen(), getWhiteColor(), pacemakerTextRect, 0)
        getBigScreen().blit(pacemakerText, pacemakerTextRect)


def uiRenderAIText(portrait):
    if not portrait:
        fs = convertXCoordinate(32)
    else:
        fs = int(convertYCoordinate(32) / 1.9)

    middle = tuple(ti/2.0 for ti in getBigScreen().get_size())
    aiTextCenter = (middle[0], middle[1] * 0.05)
    aiText = pygame.font.Font(getMasterFont(), fs).render(aiTextStr, True, getCreditColor())
    aiTextRect = aiText.get_rect()
    aiTextRect.center = aiTextCenter
    getBigScreen().blit(aiText, aiTextRect)


def uiRenderExternalMapInfo(mapInfoTextList, fingerInUse, portrait):
    if not portrait:
        fs = convertXCoordinate(16)
    else:
        fs = int(convertYCoordinate(16) / 1.5)

    middle = tuple(ti/2.0 for ti in getBigScreen().get_size())
    xShift = 0.0
    yShift = 0.0
    if fingerInUse:
        if portrait:
            xShift = - middle[0] / 2
        else:
            yShift = - middle[1] / 3
    for ind in range(len(mapInfoTextList)):
        mapTextStr = mapInfoTextTitles[ind] + mapInfoTextList[ind]
        mapTextCenter = (xShift + middle[0], yShift + middle[1] + middle[1] * (0.6 + 0.05 * ind))
        mapText = pygame.font.Font(getMasterFont(), fs).render(mapTextStr, True, getFinishTextColor())
        mapTextRect = mapText.get_rect()
        mapTextRect.center = mapTextCenter
        pygame.draw.rect(getBigScreen(), getWhiteColor(), mapTextRect, 0)
        getBigScreen().blit(mapText, mapTextRect)


def raiseControlApproachZoom():
    global controlApproachZoomUsed
    controlApproachZoomUsed = True


def lowerControlApproachZoom():
    global controlApproachZoomUsed
    controlApproachZoomUsed = False


def uiCenterTurnZoomTheMap(pos, zoom, angle, benchmark, shift):
    global screen
    global screen_rect
    perfAddStart("renTurnZoom")
    if benchmark == "phone":
        surf.blit(oMapCopy, tuple(map(lambda i, j, k: i - j + k, surfMe, pos, shift)))
#        surf.blit(oMapCopy, (0,0))
        zoom = 1.0
    else:
        if uiControlEffectEnded():
            zoom = zoom * 1.8
        elif effectStep < 10:
            zoom = zoom * (1.8 - effectStep / 20)
        else:
            zoom = zoom * 1.3
        zoom = zoom * metersPerPixel
        if controlApproachZoomUsed:
            zoom = zoom * controlApproachZoom
        surf.blit(pygame.transform.smoothscale_by(oMapCopy, zoom), tuple(map(lambda i, j: i - j * zoom, surfMe, pos)))

    screen = pygame.transform.rotate(surf, fromRadiansToDegrees(math.pi - angle))
    screenCenter = surf.get_rect().center
    screen_rect = screen.get_rect(center = screenCenter)
    perfAddStop("renTurnZoom")


characterCloudCtr = 0
characterCloudCtrMid = 10
characterCloudCtrMax = 14
def uiAnimateCharacter(where, origin, angle, color, scale, feetPlus, inTunnel, background, amaze):
    global characterCloudCtr
    feetPlus = feetPlus - 1.0
    if feetPlus <= -feetPlusStart:
        feetPlus = feetPlusStart

    if angle != 0 and effectStep and background and characterCloudCtr < characterCloudCtrMid//2:
        return feetPlus

    if not inTunnel:

        if background and characterCloudCtr > characterCloudCtrMid:
            pygame.draw.circle(where, getWhiteColor(), origin, int(7 * scale))
        characterCloudCtr = characterCloudCtr + 1
        if characterCloudCtr > characterCloudCtrMax:
            characterCloudCtr = 0

        leftFootStart = rotatePoint(origin, (origin[0] - 2 * scale, origin[1]), angle)
        rightFootStart = rotatePoint(origin, (origin[0] + 2 * scale, origin[1]), angle)
        leftFootEnd = rotatePoint(origin, (origin[0] - 2 * scale, origin[1] + scale  * (3 + feetPlusStart - abs(feetPlus*1.5))), angle)
        rightFootEnd = rotatePoint(origin, (origin[0] + 3 * scale, origin[1] + scale * (3 + abs(feetPlus*1.5))), angle)
        leftHand = (origin[0] - 5 * scale, origin[1] + scale * (-feetPlusStart/2 + abs(feetPlus)))
        rightHand = rotatePoint(origin, (origin[0] + 5 * scale, origin[1] + scale * (-feetPlusStart/2 + (feetPlusStart - abs(feetPlus)))), angle)

        uiDrawLine(where, color, leftFootStart, leftFootEnd, int(3 * scale))
        uiDrawLine(where, color, rightFootStart, rightFootEnd, int(3 * scale))
        uiDrawLine(where, color, leftHand, rightHand, int(3 * scale))

    pygame.draw.circle(where, color, origin, int(3 * scale))

    if amaze:
        uiDrawLine(where, color, (origin[0], origin[1]  - 7 * scale), (origin[0], origin[1]  - 17 * scale), width=int(3 * scale))
        uiDrawLine(where, color, (origin[0] - 3 * scale, origin[1]  - 12 * scale), (origin[0], origin[1]  - 17 * scale), width=int(3 * scale))
        uiDrawLine(where, color, (origin[0] + 3 * scale, origin[1]  - 12 * scale), (origin[0], origin[1]  - 17 * scale), width=int(3 * scale))

    return feetPlus


feetPlusPlayer = feetPlusStart
def uiAnimatePlayer(legsMoving, inTunnel, amaze, position):
    global feetPlusPlayer
    if not legsMoving:
        uiAnimateCharacter(getBigScreen(), position, 0, getPlayerColor(), 1, 0, inTunnel, True, amaze)
    else:
        feetPlusPlayer = uiAnimateCharacter(getBigScreen(), position, 0, getPlayerColor(), 1, feetPlusPlayer, inTunnel, False, amaze)


feetPlusPacemaker = feetPlusStart
def uiAnimatePacemaker(pos, angle, scale, pacemakerInd, inTunnel, background, shift):
    global feetPlusPacemaker
    p = tuple(map(lambda i, j: i - j, pos, shift))
    if p[0] > 0 and p[0] < oMapCopy.get_size()[0] and p[1] > 0 and p[1] < oMapCopy.get_size()[1]:
        feetPlusPacemaker = uiAnimateCharacter(oMapCopy, p, math.pi - angle, getPacemakerColor(pacemakerInd), 0.6 * scale / metersPerPixel, feetPlusPacemaker, inTunnel, background, False)


async def uiCompleteRender(finishTexts, mapInfoTextList, pacemakerInd, pacemakerTextNeeded, aiTextNeeded, amaze, amazeNumber, firstTime, moveLegs, inTunnel, portrait, fingerInUse):
    global prevBigRect
    perfAddStart("renComlete")
    xShift = (getBigScreen().get_size()[0]//2 - surfMe[0])
    yShift = (getBigScreen().get_size()[1]//2 - surfMe[1])
    pos = (getBigScreen().get_size()[0]//2, getBigScreen().get_size()[1]//2)
    bigRect = (screen_rect[0] + xShift, screen_rect[1] + yShift, screen_rect[2], screen_rect[3])
    if prevBigRect:
        pygame.draw.rect(getBigScreen(), getWhiteColor(), prevBigRect)
    getBigScreen().blit(screen, bigRect)
    if fingerInUse:
        getBigScreen().blit(leftImage, dest=(leftImage.get_size()[0]*0.2, getBigScreen().get_size()[1]-1.2*leftImage.get_size()[1]))
        getBigScreen().blit(rightImage, dest=(getBigScreen().get_size()[0]-1.2*leftImage.get_size()[0], getBigScreen().get_size()[1]-1.2*leftImage.get_size()[1]))
        getBigScreen().blit(stopImage, dest=((getBigScreen().get_size()[0]-leftImage.get_size()[0])//2, getBigScreen().get_size()[1]-1.2*leftImage.get_size()[1]))
    prevBigRect = bigRect
    uiAnimatePlayer(moveLegs, inTunnel, amaze, pos)

    if pacemakerTextNeeded:
        uiRenderPacemakerText(pacemakerInd, portrait)
    if amaze:
        uiRenderAmazeText(amazeNumber, portrait)
    if aiTextNeeded:
        uiRenderAIText(portrait)

    uiShowFinishText(getBigScreen(), finishTexts, amaze, portrait)
    if mapInfoTextList:
        uiRenderExternalMapInfo(mapInfoTextList, fingerInUse, portrait)
    showInfoBoxTxt(getBigScreen())
    if firstTime:
        uiUnSubmitSlide()
    perfAddStop("renComlete")
    perfShowResults("coarse")
    await uiFlip(False)


previousTime = time.time()
async def uiEvent(showInfoTexts, speedMode):
    global mousePressed
    global previousTime
    global fingerDirection
    events = []
    # regular events
#    perfAddStart("uiEvent")
    for event in pygame.event.get():
        if showInfoTexts:
            updateInfoTxtByEvent(event, 2)
        if event.type == pygame.KEYUP:
            events.append("release")
        elif event.type == pygame.KEYDOWN:
            if event.scancode == getStopKey():
                events.append("quit")
        # maybe move these to scancode-level too
        elif event.type == pygame.FINGERDOWN:
            leftThreshold = 1 / 3
            rightThreshold = 2 / 3
            downThreshold = 2 / 3
            if event.y > downThreshold:
                if event.x < leftThreshold:
                    fingerDirection = "left"
                elif event.x > rightThreshold:
                    fingerDirection = "right"
                else:
                    events.append("quit")
        elif event.type == pygame.FINGERUP:
            fingerDirection = ""

    # scancode events for speed
    if time.time() - previousTime > getTimerStepSeconds(speedMode):
        keys = pygame.key.get_pressed()
        if fingerDirection:
            events.append(fingerDirection)
        elif keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
            events.append("left")
        elif keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]:
            events.append("right")
        elif pygame.mouse.get_pressed()[0]:
            events.append("left")
            mousePressed = True
        elif pygame.mouse.get_pressed()[2]:
            events.append("right")
            mousePressed = True
        elif pygame.mouse.get_pressed()[1]:
            events.append("quit")
            mousePressed = True
        else:
            if mousePressed:
                events.append("release")
                mousePressed = False
        previousTime = time.time()
        events.append("tick")
#    perfAddStop("uiEvent")
    return events


def uiStartControlEffect(ctrl):
    global effectControl
    global effectStep
    global previousEffectStep
    global fingerDirection
    if ctrl:
        effectControl = ctrl
    previousEffectStep = effectStep
    effectStep = effectStepStart
    fingerDirection = ""


def uiControlEffectEnded():
    if not effectStep:
        return True
    return False


def uiClearBuffers():
    global oMap, oMapMid
    oMap = None
    oMapMid = None


def uiControlEffectRestart():
    global effectControl
    global effectStep
    effectControl = 0
    effectStep = 0


def uiInitStartTriangle(angle, pos):
    global triangle
    triangle = triangleCreator(triangleRadius / metersPerPixel, angle, pos)


def uiRenderControls(controls, usePacemaker, amaze, shift):
    global effectStep
    global effectControl

#    perfAddStart("renCtrls")
    if effectStep:
        if amaze:
            effectStep = effectStep - 0.5
        else:
            effectStep = effectStep - 1
        if effectStep <= 0:
            getBigScreen().fill(getWhiteColor())

    previousControl = None
    for control in controls:
        tmpEffectStep = 0
        if effectStep and effectControl < len(controls) and control == controls[effectControl]:
            tmpEffectStep = effectStep

        if control != controls[0]:
            c = tuple(map(lambda i, j: i - j, control, shift))
            if c[0] > 0 and c[0] < oMapCopy.get_size()[0] and c[1] > 0 and c[1] < oMapCopy.get_size()[1]:
                if controlApproachZoomUsed:
                    pygame.draw.circle(oMapCopy, getTrackColor(), c, int(2/metersPerPixel))

                if control == controls[-1] and not amaze:
                    uiDrawCircle(oMapCopy, (255, tmpEffectStep * 3, tmpEffectStep * 2), c, (circleRadius - circleSpacing)/metersPerPixel, max(2, int(2/metersPerPixel)))
        previousControl = control
#    perfAddStop("renCtrls")


def uiClearCanvas(controls, shortestRoutesArray, reachedControl, benchmark):
    global oMapCopy, oMapEarly, oMap, oMapMid, prevReachedControl, bboxStartX, bboxStartY

    surf.fill(getWhiteColor())
    if oMap is None:
        oMap = oMapEarly.copy()
        prevReachedControl = 999999
        bboxStartX = 0
        bboxStartY = 0

        previousControl = None
        for control in controls:
            getBigScreen().fill(getWhiteColor())
            if control == controls[0]:
                uiDrawLine(oMap, getTrackColor(), triangle[0], triangle[1], max(2, int(2/metersPerPixel)))
                uiDrawLine(oMap, getTrackColor(), triangle[1], triangle[2], max(2, int( 2/metersPerPixel)))
                uiDrawLine(oMap, getTrackColor(), triangle[2], triangle[0], max(2, int(2/metersPerPixel)))
            else:
                uiDrawCircle(oMap, getTrackColor(), control, circleRadius/metersPerPixel, max(2, int(2/metersPerPixel)))
            if previousControl:
                fraction = (circleRadiusMargin/metersPerPixel) / distanceBetweenPoints(control, previousControl)
                lineItself = (control[0]-previousControl[0], control[1]-previousControl[1])
                if fraction < 0.5:
                    lineDelta = (lineItself[0]*fraction, lineItself[1]*fraction)
                    previousControlShrinked = (previousControl[0]+lineDelta[0], previousControl[1]+lineDelta[1])
                    controlShrinked = (control[0]-lineDelta[0], control[1]-lineDelta[1])
                    uiDrawLine(oMap, getTrackColor(), previousControlShrinked, controlShrinked, max(2, int(2/metersPerPixel)))
            previousControl = control
        oMapMid = oMap.copy()
    if benchmark == "phone" and reachedControl != prevReachedControl:
        prevReachedControl = reachedControl
        getBigScreen().fill(getWhiteColor())
        if reachedControl >= len(shortestRoutesArray):
            reachedControl = len(shortestRoutesArray) - 1
        points = shortestRoutesArray[reachedControl][0]
        tmpBBox = getBoundingBox([points[0], points[0]], points)
        x1 = tmpBBox[0][0]
        x2 = tmpBBox[1][0]
        y1 = tmpBBox[0][1]
        y2 = tmpBBox[1][1]
        dx = x2 - x1
        dy = y2 - y1
        if dx < dy:
            x1 = x1 - dy//2
            x2 = x2 + dy//2
        else:
            y1 = y1 - dx//2
            y2 = y2 + dx//2
        bboxStartX = max(x1 - bboxThresh, 0)
        bboxStartY = max(y1 - bboxThresh, 0)
        bboxEndX = min(x2 + bboxThresh, oMap.get_size()[0])
        bboxEndY = min(y2 + bboxThresh, oMap.get_size()[1])
        brect = pygame.Rect(bboxStartX, bboxStartY, bboxEndX - bboxStartX, bboxEndY - bboxStartY)
        oMapMid = pygame.Surface((bboxEndX - bboxStartX, bboxEndY - bboxStartY))
        oMapMid.blit(oMap, dest=(0,0), area=brect)

    oMapCopy = oMapMid.copy()
    return (bboxStartX, bboxStartY)


def uiRenderRoute(whichmap, shortestRoute, color, shift):
    for i in range(len(shortestRoute) - 1):
        pointA = tuple(map(lambda i, j: i - j, shortestRoute[i], shift))
        pointB = tuple(map(lambda i, j: i - j, shortestRoute[i + 1], shift))
        if pointA[0] > 0 and pointA[0] < whichmap.get_size()[0] and pointA[1] > 0 and pointA[1] < whichmap.get_size()[1] and pointB[0] > 0 and pointB[0] < whichmap.get_size()[0] and pointB[1] > 0 and pointB[1] < whichmap.get_size()[1]:
            uiDrawLine(whichmap, color, pointA, pointB, max(2, int(2/metersPerPixel)))


def uiRenderRoutes(shortestRoutes, whoami, shift):
    colorMapping = { "shortest": getShortestRouteColor(), "player": getPlayerRouteColor() }
    if effectStep:
        for shortestRoute in shortestRoutes:
            uiRenderRoute(oMapCopy, shortestRoute, colorMapping[whoami], shift)


def uiDrawControlCircles(theMap, controls):
    for control in controls:
        if control == controls[0]:
            uiDrawLine(theMap, getTrackColor(), triangle[0], triangle[1], max(2, int(2/metersPerPixel)))
            uiDrawLine(theMap, getTrackColor(), triangle[1], triangle[2], max(2, int( 2/metersPerPixel)))
            uiDrawLine(theMap, getTrackColor(), triangle[2], triangle[0], max(2, int(2/metersPerPixel)))
        else:
            uiDrawCircle(theMap, getTrackColor(), control, circleRadius/metersPerPixel, max(2, int(2/metersPerPixel)))
            if control == controls[-1]:
                uiDrawCircle(theMap, getTrackColor(), control, (circleRadius - circleSpacing)/metersPerPixel, max(2, int(2/metersPerPixel)))
    

def uiStoreAnalysis(shortestRoutesArray, playerRoutesArray, controls, finishTexts):
    theMap = oMap.copy()
    for shortestRoutes in shortestRoutesArray:
        for shortestRoute in shortestRoutes:
            uiRenderRoute(theMap, shortestRoute, getPacemakerColor(1), (0,0))
    for playerRoutes in playerRoutesArray:
        for playerRoute in playerRoutes:
            uiRenderRoute(theMap, playerRoute, getPlayerColor(), (0,0))
    uiDrawControlCircles(theMap, controls)
    uiShowFinishText(theMap, finishTexts, False)

    try:
        pygame.image.save(theMap, getAnalysisResultsFileBase() + datetime.now().strftime("%m-%d-%Y__%H-%M-%S") + ".png")
    except Exception as err:
        print(f"Cannot save analysis results: {err=}, {type(err)=}")
