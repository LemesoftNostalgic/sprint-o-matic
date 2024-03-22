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
import math

from .gameUIUtils import getApplicationTitle, getMasterFont, getStopKey, getUpKey, getLeftKey, getRightKey, getDownKey, getEnterKey, getSpaceKey, getBackKey, getPlayerColor, getPacemakerColor, getTrackColor, getCreditColor, getGreyColor, convertXCoordinate, convertYCoordinate, getBigScreen, getTimerStep, uiDrawTriangle, uiFlip, uiSubmitSlide, uiSubmitTextListSlide, uiFlushEvents, uiFadeVisibleSlide, uiFadeUnVisibleSlide, uiDrawLine, uiDrawCircle

from .infiniteWorld import getInfiniteWorldPlace
from .mathUtils import distanceBetweenPoints
from .infoBox import showInfoBoxTxt, updateInfoTxtByEvent
from .gameSounds import stepEffect
from random import randrange

selections = [
    False, True, False, False, False, False,
    False, True, False, False, False, False,
    True, False, False, False, False,
    True, False, False, False]

arrowScale = 4
initCircleRadius = 30
veryFirstTime = True
triangleShift = 1.0

# these are for reference display screen of size (1920, 1080)
xStepOrig = 160
yStepOrig = 200
xStartOrig = 280
yStartOrig = 300


def showTextShadowed(surf, textCenter, fontSize, textStr, textColor, textShadowShift, portrait):
        if not portrait:
            fs = convertXCoordinate(fontSize)
        else:
            fs = int(convertYCoordinate(fontSize) / 1.7)

        textShadow = pygame.font.Font(getMasterFont(), fs).render(textStr, True, getGreyColor())
        textShadowRect = textShadow.get_rect()
        textShadowRect.center = (textCenter[0] + textShadowShift, textCenter[1] + textShadowShift)
        surf.blit(textShadow, textShadowRect)

        aText = pygame.font.Font(getMasterFont(), fs).render(textStr, True, textColor)
        textRect = aText.get_rect()
        textRect.center = textCenter
        surf.blit(aText, textRect)


def showInitArrow(surf, spot, inScale, portrait):
    if not portrait:
        scale = convertXCoordinate(inScale)
    else:
        scale = convertYCoordinate(inScale) // 2

    arrow1 = tuple(map(lambda i, j: i + j, spot, (0, 0)))
    arrow2 = tuple(map(lambda i, j: i + j, spot, (0, 10 * scale)))
    arrow3 = tuple(map(lambda i, j: i + j, spot, (4 * scale, 5 * scale)))
    arrow4 = tuple(map(lambda i, j: i + j, spot, (-4 * scale, 5 * scale)))
    uiDrawLine(surf, getPlayerColor(), arrow1, arrow2, scale*2)
    uiDrawLine(surf, getPlayerColor(), arrow1, arrow3, scale*2)
    uiDrawLine(surf, getPlayerColor(), arrow1, arrow4, scale*2)


async def uiRenderImmediate(pos, textStr, fast, benchmark, portrait):
    shift = 2
    if benchmark == "phone":
        shift = 1
    showTextShadowed(getBigScreen(), pos, 32, textStr, getTrackColor(), shift, portrait)
    await uiFlip(fast)


def showInitSelectionConstantTexts(surf, positions, selections, inScale, texts, titleTexts, titleTextPositions, creditTexts, creditTextPositions, news, newsPosition, externalOverallText, externalOverallPos, benchmark, portrait):
    # scale for the current display
    if not portrait:
        xStep = convertXCoordinate(xStepOrig)
        yStep = convertYCoordinate(yStepOrig)
        xStart = convertXCoordinate(xStartOrig)
        yStart = convertYCoordinate(yStartOrig)
        scale = convertXCoordinate(inScale)
    else:
        xStep = convertXCoordinate(xStepOrig*2)
        yStep = convertYCoordinate((yStepOrig*5)//11)
        xStart = convertXCoordinate((xStartOrig*3)//2)
        yStart = convertYCoordinate(yStartOrig//2)
        scale = (2*convertYCoordinate(inScale)) // 3
    shift = 2
    if benchmark == "phone":
        shift = 1

    titleColorRandomElem = 60
    creditColor = getCreditColor()
    titleColorRandom = (creditColor[0] - titleColorRandomElem, creditColor[1] - titleColorRandomElem, creditColor[2])
    for ind in range(len(positions) - 1):
        pos = (positions[ind][0], positions[ind][1])
        uiDrawCircle(surf, getTrackColor(), pos, (scale * 1.6), int(scale / 5))
        theTextCenter = (pos[0], pos[1] - scale * 2.0)
        showTextShadowed(surf, theTextCenter, 32, texts[ind], getTrackColor(), shift, portrait)
        lineItself = (pos[0] - positions[ind + 1][0], pos[1] - positions[ind + 1][1])
        fraction = 2 * scale / distanceBetweenPoints((0,0), lineItself)
        lineDelta = (lineItself[0]*fraction, lineItself[1]*fraction)
        previousControlShrinked = (pos[0]-lineDelta[0], pos[1]-lineDelta[1])
        controlShrinked = (positions[ind + 1][0]+lineDelta[0], positions[ind + 1][1]+lineDelta[1])
        uiDrawLine(surf, getTrackColor(), previousControlShrinked, controlShrinked, int(scale / 5))
    uiDrawLine(surf, getTrackColor(), (positions[0][0] - xStep + 3 * scale, positions[0][1]), (positions[0][0] - 2 * scale, positions[0][1]), int(scale / 5))
    uiDrawTriangle(surf, 2 * scale, math.pi/2, (positions[0][0] - xStep * triangleShift, positions[0][1]), int(scale / 5))
    pos = (positions[len(positions) - 1][0], positions[len(positions) - 1][1])
    pygame.draw.circle(surf, getTrackColor(), pos, scale, width = int(scale / 5))
    pygame.draw.circle(surf, getTrackColor(), pos, scale * 1.6, width = int(scale / 5))
    theTextCenter = (positions[len(positions) - 1][0], positions[len(positions) - 1][1] - scale * 2.0)
    showTextShadowed(surf, theTextCenter, 32, texts[len(positions) - 1], getTrackColor(), shift, portrait)

    for ind in range(len(titleTextPositions)):
        pos = titleTextPositions[ind]
        theTextCenter = (pos[0], pos[1] - scale * 2.0)
        showTextShadowed(surf, theTextCenter, 40, titleTexts[ind], getTrackColor(), shift, portrait)
    for ind in range(len(creditTextPositions)):
        showTextShadowed(surf, creditTextPositions[ind], 28, creditTexts[ind], getTrackColor(), shift, portrait)
    titleTextCenter = (surf.get_size()[0] / 2, yStart * 0.25)
    showTextShadowed(surf, titleTextCenter, 96, getApplicationTitle(), titleColorRandom, 3 * shift, portrait)
    if news:
        showTextShadowed(surf, newsPosition, 28, "News: " + news, getPacemakerColor(2), shift, portrait)
    showTextShadowed(surf, (newsPosition[0], newsPosition[1] * 1.2), 28, "Homepage: tinyurl.com/sprint-o-matic", getPacemakerColor(2), shift, portrait)
    showTextShadowed(surf, externalOverallPos, 32, externalOverallText, getTrackColor(), shift, portrait)


def showInitSelections(surf, positions, selections, inScale, texts, titleTexts, titleTextPositions, externalTeamText, externalTeamPosition, externalText, externalPosition, ouluText, ouluPosition, worldText, worldPosition, benchmark, portrait):
    # scale for the current display
    if not portrait:
        xStep = convertXCoordinate(xStepOrig)
        yStep = convertYCoordinate(yStepOrig)
        xStart = convertXCoordinate(xStartOrig)
        yStart = convertYCoordinate(yStartOrig)
        scale = convertXCoordinate(inScale)
    else:
        xStep = convertXCoordinate(xStepOrig*2)
        yStep = convertYCoordinate((yStepOrig*5)//11)
        xStart = convertXCoordinate((xStartOrig*3)//2)
        yStart = convertYCoordinate(yStartOrig//2)
        scale = (2*convertYCoordinate(inScale)) // 3
    shift = 2
    if benchmark == "phone":
        shift = 1
    titleColorRandomElem = randrange(56, 64)
    creditColor = getCreditColor()
    titleColorRandom = (creditColor[0] - titleColorRandomElem, creditColor[1] - titleColorRandomElem, creditColor[2])
    for ind in range(len(positions) - 1):
        pos = (positions[ind][0], positions[ind][1])
        selectedColor = titleColorRandom if selections[ind] else getGreyColor()
        pygame.draw.circle(surf, selectedColor, pos, scale)

    extTeamTextSize = 32
    extTextThreshold = 8
    extTextUpperThreshold = 14
    if len(externalTeamText) >= extTextUpperThreshold:
            externalTeamText = externalTeamText[:extTextUpperThreshold] + ".."
    if len(externalTeamText) >= extTextThreshold:
        extTeamTextSize = (extTeamTextSize * extTextThreshold) // len(externalTeamText)
    showTextShadowed(surf, externalTeamPosition, extTeamTextSize, externalTeamText, getTrackColor(), shift, portrait)
    extTextSize = 32
    if len(externalText) >= extTextUpperThreshold:
            externalText = externalText[:extTextUpperThreshold] + ".."
    if len(externalText) >= extTextThreshold:
        extTextSize = (extTextSize * extTextThreshold) // len(externalText)
    showTextShadowed(surf, externalPosition, extTextSize, externalText, getTrackColor(), shift, portrait)
    showTextShadowed(surf, ouluPosition, 32, ouluText, getTrackColor(), shift, portrait)
    showTextShadowed(surf, worldPosition, 32, worldText, getTrackColor(), shift, portrait)


async def veryFirstTime(portrait):
    global veryFirstTime
    creditTextsEarly = [
        "Author: Jyrki Leskelä, Oulu",
        "License: Apache-2.0.",
        "",
        "Credits for the 'World' map data: OpenStreetMap",
        "Credits for sound effects (freesound.org):",
        "CC 1.0 DEED:",
        "ali, craigsmith, crk365, frodo89, fupicat, jackslay, furbyguy",
        "berdnikov2004, badoink, bronxio, cgoulao, fran_ky, iykqic0",
        "johaynes, josefpres, nomiqbomi, seth, szymalix, the_loner",
        "CC BY 3.0 DEED:",
        "frodo89 for 84456__frodo89__standard-beep-pre-start.ogg"
        ]
    if veryFirstTime:
        uiSubmitTextListSlide(creditTextsEarly, portrait)
        await uiFlip(False)
        await asyncio.sleep(1)
        veryFirstTime = False


def getFingerIndex(fingerPos, positions, size, portrait, xStep):
    pos = (fingerPos[0]*size[0], fingerPos[1]*size[1])
    startpos = (positions[0][0] - xStep * triangleShift, positions[0][1])
    if not portrait:
        scale = convertXCoordinate(initCircleRadius)
    else:
        scale = convertYCoordinate(initCircleRadius) // 2

    for ind in range(len(positions)):
        place = positions[ind]
        if distanceBetweenPoints(pos, place) < 1.3 * scale:
            return ind

    if distanceBetweenPoints(pos, startpos) < 1.3 * scale:
        return -1

    return None


initScreenPos = 0
externalExampleTeamCtr = 0
externalExampleCtr = 0
worldExampleCtr = 0
async def initScreen(imagePath, gameSettings, externalImageData, externalWorldCityMap, news, benchmark, portrait):
    global selections
    global externalExampleTeamCtr
    global externalExampleCtr
    global worldExampleCtr
    global initScreenPos
    global veryFirstTime

    firstTime = True


    if not portrait:
        # scale for the current display
        xStep = convertXCoordinate(xStepOrig)
        yStep = convertYCoordinate(yStepOrig)
        xStart = convertXCoordinate(xStartOrig)
        yStart = convertYCoordinate(yStartOrig)

        newsPosition = (xStart + 6.5 * xStep, yStart - yStep * 3 / 4)
        positions = [
            # first row 6
            (xStart, yStart), (xStart + xStep, yStart), (xStart + 2 * xStep, yStart), (xStart + 3 * xStep, yStart), (xStart + 4 * xStep, yStart), (xStart + 5 * xStep, yStart), 
            # second row 6
            (xStart + 2 * xStep, yStart + yStep), (xStart + 3 * xStep, yStart + yStep), (xStart + 4 * xStep, yStart + yStep), (xStart + 5 * xStep, yStart + yStep), (xStart + 6 * xStep, yStart + yStep), (xStart + 7 * xStep, yStart + yStep),
            # third row 4
             (xStart + 5 * xStep, yStart + 2 * yStep),(xStart + 6 * xStep, yStart + 2 * yStep), (xStart + 7 * xStep, yStart + 2 * yStep), (xStart + 8 * xStep, yStart + 2 * yStep), (xStart + 9 * xStep, yStart + 2 * yStep),
            # fourth row 4
            (xStart + 5.6 * xStep, yStart + 3 * yStep), (xStart + 6.6 * xStep, yStart + 3 * yStep), (xStart + 7.6 * xStep, yStart + 3 * yStep), (xStart + 8.6 * xStep, yStart + 3 * yStep), (xStart + 9.6 * xStep, yStart + 3 * yStep)]
        titleTextPositions = [
            (xStart, yStart - yStep/5),
            (xStart + 1 * xStep - xStep / 10, yStart + 1 * yStep + yStep/4),
            (xStart + 4 * xStep - xStep / 10, yStart + 2 * yStep + yStep/4),
            (xStart + 4.6 * xStep - xStep / 7, yStart + 3 * yStep + yStep/4)
            ]
        externalExampleOverallPosition = (xStart + 8.1 * xStep, yStart + 2.50 * yStep)
        externalExampleTeamSelectionPosition = (xStart + 7.6 * xStep, yStart + 3.3 * yStep)
        externalExampleSelectionPosition = (xStart + 8.6 * xStep, yStart + 3.3 * yStep)
        loadingPosition = (xStart + 9.6 * xStep, yStart + 3.3 * yStep)
        ouluExampleSelectionPosition = (xStart + 6.6 * xStep, yStart + 3.3 * yStep)
        worldExampleSelectionPosition = (xStart + 5.6 * xStep, yStart + 3.3 * yStep)
        creditTextPositions = [
            (xStart + xStep, yStart + 2.3 * yStep),
            (xStart + xStep, yStart + 2.45 * yStep),
            (xStart + xStep, yStart + 2.65 * yStep),
            (xStart + xStep, yStart + 2.8 * yStep),
            ]

    else:
        # scale for the current display
        xStep = convertXCoordinate(xStepOrig*2)
        yStep = convertYCoordinate((yStepOrig*5)//11)
        xStart = convertXCoordinate((xStartOrig*3)//2)
        yStart = convertYCoordinate(yStartOrig//2)

        positions = [
            # first row 6
            (xStart, yStart), (xStart, yStart + yStep), (xStart, yStart + 2 * yStep), (xStart, yStart + 3 * yStep), (xStart, yStart + 4 * yStep), (xStart, yStart + 5 * yStep), 
            # second row 6
            (xStart + xStep, yStart + 2 * yStep), (xStart + xStep, yStart + 3 * yStep), (xStart + xStep, yStart + 4 * yStep), (xStart + xStep, yStart + 5 * yStep), (xStart + xStep, yStart + 6 * yStep), (xStart + xStep, yStart + 7 * yStep),
            # third row 4
             (xStart + 2 * xStep, yStart + 5 * yStep),(xStart + 2 * xStep, yStart + 6 * yStep), (xStart + 2 * xStep, yStart + 7 * yStep), (xStart + 2 * xStep, yStart + 8 * yStep), (xStart + 2 * xStep, yStart + 9 * yStep),
            # fourth row 4
            (xStart + 3 * xStep, yStart + 6.6 * yStep), (xStart + 3 * xStep, yStart + 7.6 * yStep), (xStart + 3 * xStep, yStart + 8.6 * yStep), (xStart + 3 * xStep, yStart + 9.6 * yStep), (xStart + 4 * xStep, yStart + 9.6 * yStep)]
        titleTextPositions = [
            (xStart + 0.4 * xStep, yStart - 0.2 * yStep),
            (xStart + 1.30 * xStep, yStart + 1.8 * yStep),
            (xStart + 2.35 * xStep, yStart + 4.8 * yStep),
            (xStart + 3.35 * xStep, yStart + 5.4 * yStep)
            ]
        externalExampleOverallPosition = (xStart + 3.8 * xStep, yStart + 8.16 * yStep)
        externalExampleTeamSelectionPosition = (xStart + 3.8 * xStep, yStart + 8.6 * yStep)
        externalExampleSelectionPosition = (xStart + 3.8 * xStep, yStart + 9.6 * yStep)
        loadingPosition = (xStart + 3 * xStep, yStart + 10.6 * yStep)
        ouluExampleSelectionPosition = (xStart + 3.6 * xStep, yStart + 7.6 * yStep)
        worldExampleSelectionPosition = (xStart + 3.8 * xStep, yStart + 6.6 * yStep)
        creditTextPositions = [
            (xStart + 2.8 * xStep, yStart + 0.35 * yStep),
            (xStart + 2.8 * xStep, yStart + 0.5 * yStep),
            (xStart + 2.8 * xStep, yStart + 0.7 * yStep),
            (xStart + 2.8 * xStep, yStart + 0.85 * yStep),
            ]
        newsPosition = (xStart + 1.8 * xStep, yStart - 1.0 * yStep)

    titleTexts = [
        "track length:",
        "leg length:",
        "play mode:",
        "map select:"
        ]
    creditTexts = [
        "A trainer app for sprint orienteering,",
        "Author: Jyrki Leskelä, Oulu.",
        "Use mouse keys, touchscreen, or keyboard.",
        "move: arrows, select: SPACE/BACKSPACE, quit: ESC",
        ]
    # "external" always last
    texts = [
        # first row 6
        "micro", "mini", "short", "regular", "longish", "long",
        # second row 6
        "micro", "    mini", "short", "regular", "longish", "long",
        # third row 2
        "once", "    repeat", "fast  ", "pacemaker ", " amaze",
        # fourth row 3
        "World", "", "team", "map", "start"
        ]
    indexes = [
        [0, 1, 2, 3,  4,  5],
        [6, 7, 8, 9, 10, 11],
        [12, 13, 14, 15, 16],
        [17, 18, 19, 20],
        ]
    values = [
        [600, 1000, 1400, 2000,  2400,  3000],
        [ [0.60, 0.30, 0.10, 0.00, 0.00],
           [0.40, 0.30, 0.20, 0.10, 0.00],
           [0.20, 0.30, 0.30, 0.15, 0.05],
           [0.10, 0.25, 0.30, 0.25, 0.10],
           [0.10, 0.10, 0.20, 0.30, 0.30],
           [0.00, 0.05, 0.15, 0.35, 0.45]
           ],
        ["one-shot", "repeat", "superfast", "pacemaker", "amaze"],
        ["infinite-world", "infinite-oulu", "external-team", "external-map"],
        ]
    infiniteOuluTerrains = ["shortLeg", "mediumLeg", "mediumLeg", "mediumLeg", "longLeg", "longLeg"]

    running = True
    quitting = False
    TIMER_EVENT = pygame.USEREVENT + 1
    backgroundImageFile = imagePath + "lemesoftnostalgic/SettingsBackgroundImage.jpg"
    backgroundImage = getBigScreen().copy()
    tmpImage = pygame.transform.scale(pygame.image.load(backgroundImageFile), getBigScreen().get_size())
    backgroundImage.blit(tmpImage, (0, 0))
    externalExampleTeamText = ""
    externalExampleText = ""
    worldExampleText = ""
    externalExampleOverallText = "external"
    ouluExampleText = "iOulu"
    loadingText = "Loading..."
    fingerDirection = ""
    fingerInUse = False
    fingerPos = (0,0)

    pygame.key.set_repeat(200, 50)
    pygame.time.set_timer(TIMER_EVENT, getTimerStep())

    while running:
        mousePressed = False
        for event in pygame.event.get():
            if gameSettings.infoBox:
                updateInfoTxtByEvent(event, 1)
            if event.type == pygame.KEYDOWN:
                if event.scancode == getStopKey():
                    running = False
                    quitting = True
                elif event.scancode == getLeftKey() or event.scancode == getUpKey():
                    if initScreenPos > 0:
                        initScreenPos = initScreenPos - 1
                elif event.scancode == getRightKey() or event.scancode == getDownKey():
                    if initScreenPos < len(positions) - 1:
                        initScreenPos = initScreenPos + 1
                elif event.scancode == getEnterKey() or event.scancode == getSpaceKey():
                    if initScreenPos == len(positions) - 1:
                        running = False
                    else:
                        stepEffect()
                        if not (initScreenPos == len(selections) - 1 and len(externalImageData) == 0):
                            for subindexes in indexes:
                                if initScreenPos in subindexes:
                                    for ind in subindexes:
                                        selections[ind] = False
                            selections[initScreenPos] = True
                            if initScreenPos == len(selections) - 2:
                                externalExampleCtr = 0
                                externalExampleTeamCtr = externalExampleTeamCtr + 1
                                if externalExampleTeamCtr >= len(externalImageData):
                                    externalExampleTeamCtr = 0
                            if initScreenPos == len(selections) - 1:
                                externalExampleCtr = externalExampleCtr + 1
                                if externalExampleCtr >= len(externalImageData[externalExampleTeamCtr]["sub-listing"]):
                                    externalExampleCtr = 0
                            if initScreenPos == len(selections) - 4:
                                worldExampleCtr = worldExampleCtr + 1
                                if worldExampleCtr >= len(externalWorldCityMap):
                                    worldExampleCtr = 0
                elif event.scancode == getBackKey():
                    if initScreenPos == len(selections) - 4:
                        worldExampleCtr = worldExampleCtr - 1
                        if worldExampleCtr < 0:
                            worldExampleCtr =  len(externalWorldCityMap) - 1
            elif event.type == pygame.FINGERUP:
                fingerDirection = ""
                fingerInUse = True
                mousePressed = False
            elif event.type == pygame.FINGERDOWN:
                mousePressed = False
                fingerInUse = True
                leftThreshold = 1 / 3
                rightThreshold = 2 / 3
                fingerPos = (event.x, event.y)
                fingerDirection = "pressed"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mousePressed = True
                fingerDirection = ""
            elif event.type == pygame.QUIT:
                quitting = True
                running = False

        if fingerDirection == "pressed":
            mousePressed = False
            screenPos = getFingerIndex(fingerPos, positions, getBigScreen().get_size(), portrait, xStep)
            fingerDirection = ""
            await asyncio.sleep(0.1)
            if screenPos is None:
                pass
            elif screenPos == -1:
                quitting = True
                running = False
            elif screenPos == len(positions) - 1:
                running = False
                initScreenPos = screenPos
            else:
                initScreenPos = screenPos
                stepEffect()
                if not (initScreenPos == len(selections) - 1 and len(externalImageData) == 0):
                    for subindexes in indexes:
                        if initScreenPos in subindexes:
                            for ind in subindexes:
                                selections[ind] = False
                    selections[initScreenPos] = True
                    if initScreenPos == len(selections) - 2:
                        externalExampleCtr = 0
                        externalExampleTeamCtr = externalExampleTeamCtr + 1
                        if externalExampleTeamCtr >= len(externalImageData):
                            externalExampleTeamCtr = 0
                    if initScreenPos == len(selections) - 1:
                        externalExampleCtr = externalExampleCtr + 1
                        if externalExampleCtr >= len(externalImageData[externalExampleTeamCtr]["sub-listing"]):
                            externalExampleCtr = 0
                    if initScreenPos == len(selections) - 4:
                        worldExampleCtr = worldExampleCtr + 1
                        if worldExampleCtr >= len(externalWorldCityMap):
                            worldExampleCtr = 0
        elif mousePressed and not fingerInUse:
            fingerDirection = ""
            if pygame.mouse.get_pressed()[0]:
                if initScreenPos > 0:
                    initScreenPos = initScreenPos - 1
            elif pygame.mouse.get_pressed()[2]:
                if initScreenPos < len(positions) - 1:
                    initScreenPos = initScreenPos + 1
            elif pygame.mouse.get_pressed()[1]:
                stepEffect()
                if initScreenPos == len(positions) - 1:
                    running = False
                else:
                    if not (initScreenPos == len(selections) - 1 and len(externalImageData) == 0):
                        for subindexes in indexes:
                            if initScreenPos in subindexes:
                                for ind in subindexes:
                                    selections[ind] = False
                        selections[initScreenPos] = True
                        if initScreenPos == len(selections) - 2:
                            externalExampleTeamCtr = externalExampleTeamCtr + 1
                            if externalExampleTeamCtr >= len(externalImageData):
                                externalExampleTeamCtr = 0
                        if initScreenPos == len(selections) - 1:
                            externalExampleCtr = externalExampleCtr + 1
                            if externalExampleCtr >= len(externalImageData[externalExampleTeamCtr]["sub-listing"]):
                                externalExampleCtr = 0
                        if initScreenPos == len(selections) - 4:
                            worldExampleCtr = worldExampleCtr + 1
                            if worldExampleCtr >= len(externalWorldCityMap):
                                worldExampleCtr = 0

        if not quitting:
            # renderer
            externalExampleTeamText = ""
            externalExampleText = ""
            if len(externalImageData) > 0 and (selections[-2] == True or selections[-1] == True):
                externalExampleTeamText = externalImageData[externalExampleTeamCtr]["team-name"]
                externalExampleText = externalImageData[externalExampleTeamCtr]["sub-listing"][externalExampleCtr]["name"]
                selections[-2] = True
                selections[-1] = True

            worldExampleText = ""
            if len(externalWorldCityMap) > 0 and selections[-4] == True:
                worldExampleText = externalWorldCityMap[worldExampleCtr][0]
                selections[-4] = True

            if firstTime:
                showInitSelectionConstantTexts(backgroundImage, positions, selections, initCircleRadius, texts, titleTexts, titleTextPositions, creditTexts, creditTextPositions, news, newsPosition, externalExampleOverallText, externalExampleOverallPosition, benchmark, portrait)
            getBigScreen().blit(backgroundImage, backgroundImage.get_rect())
            showInitSelections(getBigScreen(), positions, selections, initCircleRadius, texts, titleTexts, titleTextPositions, externalExampleTeamText, externalExampleTeamSelectionPosition, externalExampleText, externalExampleSelectionPosition, ouluExampleText, ouluExampleSelectionPosition, worldExampleText, worldExampleSelectionPosition, benchmark, portrait)
            showInitArrow(getBigScreen(), positions[initScreenPos], arrowScale, portrait)
            if gameSettings.infoBox:
                showInfoBoxTxt(getBigScreen())
            if firstTime:
                    uiFadeVisibleSlide()
                    firstTime = False
            await uiFlip(False)
            await asyncio.sleep(0)
        else:
            uiFadeUnVisibleSlide()
            await uiFlip(False)
            await asyncio.sleep(0)
    if not quitting:
        retSettings = []
        for subindexes in indexes:
            for index in subindexes:
                if selections[index]:
                    retSettings.append(values[indexes.index(subindexes)][subindexes.index(index)])
        gameSettings.trackLength = retSettings[0]
        for ind in range(len(retSettings[1])):
            gameSettings.distributionOfControlLegs[ind][2] = retSettings[1][ind]
        gameSettings.infiniteOuluTerrain = infiniteOuluTerrains[values[1].index(retSettings[1])]
        if retSettings[2] in values[2][:2]:
            gameSettings.continuous = True if retSettings[2]=="repeat" else False
            gameSettings.speed = "regular"
            gameSettings.pacemaker = 0
            gameSettings.amaze = False
        elif retSettings[2] == "pacemaker":
            gameSettings.pacemaker = randrange(1, 4)
            gameSettings.speed = "regular"
            gameSettings.continuous = False
            gameSettings.amaze = False
        elif retSettings[2] == "amaze":
            gameSettings.amaze = True
            gameSettings.pacemaker = False
            gameSettings.speed = "regular"
            gameSettings.continuous = True
        else:
            gameSettings.speed = "superfast"
            gameSettings.pacemaker = 0
            gameSettings.continuous = False
            gameSettings.amaze = False

        if retSettings[3] == "infinite-oulu":
            gameSettings.infiniteOulu = True
            gameSettings.infiniteWorld = False
            gameSettings.externalExample = ""
            uiSubmitSlide(str(randrange(100000,999999)) + "th Street of Infinite Oulu!", portrait)
            await uiRenderImmediate(loadingPosition, loadingText, False, benchmark, portrait)
        elif retSettings[3] == "infinite-world":
            gameSettings.infiniteOulu = False
            gameSettings.infiniteWorld = True
            gameSettings.infiniteWorldCity = worldExampleText
            gameSettings.place, placeName = getInfiniteWorldPlace(worldExampleText, externalWorldCityMap)
            gameSettings.externalExample = ""
            if placeName:
               uiSubmitSlide("Welcome to " + placeName + "...", portrait)
            else:
               uiSubmitSlide("Somewhere in " + worldExampleText + "...", portrait)
            await uiRenderImmediate(loadingPosition, loadingText, False, benchmark, portrait)
        elif retSettings[3] == "external-team" or retSettings[3] == "external-map":
            gameSettings.infiniteOulu = False
            gameSettings.infiniteWorld = False
            gameSettings.externalExample = externalExampleText
            gameSettings.externalExampleTeam = externalExampleTeamText
            uiSubmitSlide("Welcome to " + externalExampleText, portrait)
            await uiRenderImmediate(loadingPosition, loadingText, False, benchmark, portrait)

    pygame.time.set_timer(TIMER_EVENT, 0)
    return quitting, gameSettings, fingerInUse
