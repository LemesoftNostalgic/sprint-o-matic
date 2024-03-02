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

from .gameUIUtils import getApplicationTitle, getMasterFont, getStopKey, getUpKey, getLeftKey, getRightKey, getDownKey, getEnterKey, getSpaceKey, getBackKey, getPlayerColor, getPacemakerColor, getTrackColor, getCreditColor, getGreyColor, convertXCoordinate, convertYCoordinate, getBigScreen, getTimerStep, uiDrawTriangle, checkAutoTestKey

from .mathUtils import distanceBetweenPoints
from .infoBox import showInfoBoxTxt, updateInfoTxtByEvent
from .gameSounds import stepEffect, finishEffect
from random import randrange


selections = [
    False, True, False, False, False, False,
    False, True, False, False, False, False,
    True, False, False, False,
    True, False, False, False]

arrowScale = 4
initCircleRadius = 30

# these are for reference display screen of size (1920, 1080)
xStepOrig = 160
yStepOrig = 200
xStartOrig = 280
yStartOrig = 300


def showTextShadowed(textCenter, fontSize, textStr, textColor, textShadowShift):
        textShadow = pygame.font.Font(getMasterFont(), convertXCoordinate(fontSize)).render(textStr, True, getGreyColor())
        textShadowRect = textShadow.get_rect()
        textShadowRect.center = (textCenter[0] + textShadowShift, textCenter[1] + textShadowShift)
        getBigScreen().blit(textShadow, textShadowRect)

        aText = pygame.font.Font(getMasterFont(), convertXCoordinate(fontSize)).render(textStr, True, textColor)
        textRect = aText.get_rect()
        textRect.center = textCenter
        getBigScreen().blit(aText, textRect)


def showInitArrow(surf, spot, inScale):
    scale = convertXCoordinate(inScale)
    arrow1 = tuple(map(lambda i, j: i + j, spot, (0, 0)))
    arrow2 = tuple(map(lambda i, j: i + j, spot, (0, 10 * scale)))
    arrow3 = tuple(map(lambda i, j: i + j, spot, (4 * scale, 5 * scale)))
    arrow4 = tuple(map(lambda i, j: i + j, spot, (-4 * scale, 5 * scale)))
    pygame.draw.line(surf, getPlayerColor(), arrow1, arrow2, width=scale)
    pygame.draw.line(surf, getPlayerColor(), arrow1, arrow3, width=scale)
    pygame.draw.line(surf, getPlayerColor(), arrow1, arrow4, width=scale)


def uiRenderImmediate(pos, textStr):
    showTextShadowed(pos, 32, textStr, getTrackColor(), 2)
    pygame.display.flip()


def showInitSelections(surf, positions, selections, inScale, texts, titleTexts, titleTextPositions, creditTexts, creditTextPositions, externalOverallText, externalOverallPos, externalTeamText, externalTeamPosition, externalText, externalPosition, ouluText, ouluPosition, news, newsPosition, worldText, worldPosition):
    # scale for the current display
    xStep = convertXCoordinate(xStepOrig)
    yStep = convertYCoordinate(yStepOrig)
    xStart = convertXCoordinate(xStartOrig)
    yStart = convertYCoordinate(yStartOrig)
    scale = convertXCoordinate(inScale)

    titleColorRandomElem = randrange(56, 64)
    creditColor = getCreditColor()
    titleColorRandom = (creditColor[0] - titleColorRandomElem, creditColor[1] - titleColorRandomElem, creditColor[2])
    for ind in range(len(positions) - 1):
        pos = (positions[ind][0], positions[ind][1])
        selectedColor = titleColorRandom if selections[ind] else getGreyColor()
        pygame.draw.circle(surf, selectedColor, pos, scale)
        pygame.draw.circle(surf, getTrackColor(), pos, (scale * 1.6), width = int(scale / 5))
        theTextCenter = (pos[0], pos[1] - scale * 2.0)
        showTextShadowed(theTextCenter, 32, texts[ind], getTrackColor(), 2)
        lineItself = (pos[0] - positions[ind + 1][0], pos[1] - positions[ind + 1][1])
        fraction = 2 * scale / distanceBetweenPoints((0,0), lineItself)
        lineDelta = (lineItself[0]*fraction, lineItself[1]*fraction)
        previousControlShrinked = (pos[0]-lineDelta[0], pos[1]-lineDelta[1])
        controlShrinked = (positions[ind + 1][0]+lineDelta[0], positions[ind + 1][1]+lineDelta[1])
        pygame.draw.line(surf, getTrackColor(), previousControlShrinked, controlShrinked, width=int(scale / 5))
    pygame.draw.line(surf, getTrackColor(), (positions[0][0] - xStep + 3 * scale, positions[0][1]), (positions[0][0] - 2 * scale, positions[0][1]), width=int(scale / 5))
    uiDrawTriangle(surf, 2 * scale, math.pi/2, (positions[0][0] - xStep * 0.8, positions[0][1]), int(scale / 5))
    pos = (positions[len(positions) - 1][0], positions[len(positions) - 1][1])
    pygame.draw.circle(surf, getTrackColor(), pos, scale, width = int(scale / 5))
    pygame.draw.circle(surf, getTrackColor(), pos, scale * 1.6, width = int(scale / 5))
    theTextCenter = (positions[len(positions) - 1][0], positions[len(positions) - 1][1] - scale * 2.0)
    showTextShadowed(theTextCenter, 32, texts[len(positions) - 1], getTrackColor(), 2)

    for ind in range(len(titleTextPositions)):
        pos = titleTextPositions[ind]
        theTextCenter = (pos[0], pos[1] - scale * 2.0)
        showTextShadowed(theTextCenter, 40, titleTexts[ind], getTrackColor(), 2)
    for ind in range(len(creditTextPositions)):
        showTextShadowed(creditTextPositions[ind], 24, creditTexts[ind], getTrackColor(), 2)
    titleTextCenter = (surf.get_size()[0] / 2, xStart / 3)
    showTextShadowed(titleTextCenter, 128, getApplicationTitle(), titleColorRandom, 5)
    showTextShadowed(externalOverallPos, 32, externalOverallText, getTrackColor(), 2)
    extTeamTextSize = 32
    extTextThreshold = 8
    extTextUpperThreshold = 14
    if len(externalTeamText) >= extTextUpperThreshold:
            externalTeamText = externalTeamText[:extTextUpperThreshold] + ".."
    if len(externalTeamText) >= extTextThreshold:
        extTeamTextSize = (extTeamTextSize * extTextThreshold) // len(externalTeamText)
    showTextShadowed(externalTeamPosition, extTeamTextSize, externalTeamText, getTrackColor(), 2)
    extTextSize = 32
    if len(externalText) >= extTextUpperThreshold:
            externalText = externalText[:extTextUpperThreshold] + ".."
    if len(externalText) >= extTextThreshold:
        extTextSize = (extTextSize * extTextThreshold) // len(externalText)
    showTextShadowed(externalPosition, extTextSize, externalText, getTrackColor(), 2)
    showTextShadowed(ouluPosition, 32, ouluText, getTrackColor(), 2)
    showTextShadowed(worldPosition, 32, worldText, getTrackColor(), 2)
    if news:
        showTextShadowed(newsPosition, 24, "News: " + news, getPacemakerColor(2), 2)


initScreenPos = 0
externalExampleTeamCtr = 0
externalExampleCtr = 0
worldExampleCtr = 0
async def initScreen(imagePath, gameSettings, externalImageData, externalWorldCityMap, news):
    global selections
    global externalExampleTeamCtr
    global externalExampleCtr
    global worldExampleCtr
    global initScreenPos

    # scale for the current display
    xStep = convertXCoordinate(xStepOrig)
    yStep = convertYCoordinate(yStepOrig)
    xStart = convertXCoordinate(xStartOrig)
    yStart = convertYCoordinate(yStartOrig)

    newsPosition = (xStart + 7 * xStep, yStart - yStep * 2 / 3)
    positions = [
        # first row 6
        (xStart, yStart), (xStart + xStep, yStart), (xStart + 2 * xStep, yStart), (xStart + 3 * xStep, yStart), (xStart + 4 * xStep, yStart), (xStart + 5 * xStep, yStart), 
        # second row 6
        (xStart + 2* xStep, yStart + yStep), (xStart + 3 * xStep, yStart + yStep), (xStart + 4 * xStep, yStart + yStep), (xStart + 5 * xStep, yStart + yStep), (xStart + 6 * xStep, yStart + yStep), (xStart + 7 * xStep, yStart + yStep),
        # third row 4
         (xStart + 5 * xStep, yStart + 2 * yStep),(xStart + 6 * xStep, yStart + 2 * yStep), (xStart + 7 * xStep, yStart + 2 * yStep), (xStart + 8 * xStep, yStart + 2 * yStep),
        # fourth row 4
        (xStart + 5.6 * xStep, yStart + 3 * yStep), (xStart + 6.6 * xStep, yStart + 3 * yStep), (xStart + 7.6 * xStep, yStart + 3 * yStep), (xStart + 8.6 * xStep, yStart + 3 * yStep), (xStart + 9.6 * xStep, yStart + 3 * yStep)]
    titleTexts = [
        "track length:",
        "leg length:",
        "play mode:",
        "map select:"
        ]
    creditTexts = [
        "A trainer app for sprint orienteering,",
        "developer Jyrki Leskelä, Oulu. License: Apache-2.0.",
        "Use mouse keys or keyboard arrows",
        "select: SPACE/BACKSPACE, quit: ESC",
        "Credits for the 'World' map data: OpenStreetMap",
        "Credits for sound effects (freesound.org):",
        "CC 1.0 DEED:",
        "ali, craigsmith, crk365, frodo89, fupicat, jackslay, furbyguy",
        "berdnikov2004, badoink, bronxio, cgoulao, fran_ky, iykqic0",
        "johaynes, josefpres, nomiqbomi, seth, szymalix, the_loner",
        "CC BY 3.0 DEED:",
        "frodo89 for 84456__frodo89__standard-beep-pre-start.ogg"
        ]
    titleTextPositions = [
        (xStart, yStart - yStep/5),
        (xStart + 1 * xStep - xStep / 10, yStart + 1 * yStep + yStep/4),
        (xStart + 4 * xStep - xStep / 10, yStart + 2 * yStep + yStep/4),
        (xStart + 4.6 * xStep - xStep / 7, yStart + 3 * yStep + yStep/4)
        ]
    creditTextPositions = [
        (xStart + xStep, yStart + 1.7 * yStep),
        (xStart + xStep, yStart + 1.8 * yStep),
        (xStart + xStep, yStart + 2.0 * yStep),
        (xStart + xStep, yStart + 2.1 * yStep),
        (xStart + xStep, yStart + 2.3 * yStep),
        (xStart + xStep, yStart + 2.4 * yStep),
        (xStart + xStep, yStart + 2.6 * yStep),
        (xStart + xStep, yStart + 2.7 * yStep),
        (xStart + xStep, yStart + 2.8 * yStep),
        (xStart + xStep, yStart + 2.9 * yStep),
        (xStart + xStep, yStart + 3.1 * yStep),
        (xStart + xStep, yStart + 3.2 * yStep),
        ]
    # "external" always last
    texts = [
        # first row 6
        "micro", "mini", "short", "regular", "longish", "long",
        # second row 6
        "micro", "    mini", "short", "regular", "longish", "long",
        # third row 2
        "once", "    repeat", "fast  ", "pacemaker",
        # fourth row 3
            "World", "", "team", "map", "start"
        ]
    indexes = [
        [0, 1, 2, 3,  4,  5],
        [6, 7, 8, 9, 10, 11],
        [12, 13, 14, 15],
        [16, 17, 18, 19],
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
        ["one-shot", "repeat", "superfast", "pacemaker"],
        ["infinite-world", "infinite-oulu", "external-team", "external-map"],
        ]
    infiniteOuluTerrains = ["shortLeg", "mediumLeg", "mediumLeg", "mediumLeg", "longLeg", "longLeg"]
    externalExampleOverallPosition = (xStart + 8.1 * xStep, yStart + 2.55 * yStep)
    externalExampleTeamSelectionPosition = (xStart + 7.6 * xStep, yStart + 3.3 * yStep)
    externalExampleSelectionPosition = (xStart + 8.6 * xStep, yStart + 3.3 * yStep)
    loadingPosition = (xStart + 9.6 * xStep, yStart + 3.3 * yStep)
    ouluExampleSelectionPosition = (xStart + 6.6 * xStep, yStart + 3.3 * yStep)

    worldExampleSelectionPosition = (xStart + 5.6 * xStep, yStart + 3.3 * yStep)

    running = True
    quitting = False
    TIMER_EVENT = pygame.USEREVENT + 1
    backgroundImageFile = imagePath + "lemesoftnostalgic/SettingsBackgroundImage.jpg"
    backgroundImage = pygame.transform.scale(pygame.image.load(backgroundImageFile), getBigScreen().get_size())
    externalExampleTeamText = ""
    externalExampleText = ""
    worldExampleText = ""
    externalExampleOverallText = "external"
    ouluExampleText = "iOulu"
    loadingText = "Loading..."

    pygame.key.set_repeat(200, 50)
    pygame.time.set_timer(TIMER_EVENT, getTimerStep())

    while running:
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
                elif checkAutoTestKey(event.scancode):
                    gameSettings.autoTest = True
                    running = False
                elif event.scancode == getEnterKey() or event.scancode == getSpaceKey():
                    if initScreenPos == len(positions) - 1:
                        running = False
                        if not gameSettings.offline:
                            finishEffect()
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
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    if initScreenPos > 0:
                        initScreenPos = initScreenPos - 1
                elif pygame.mouse.get_pressed()[2]:
                    if initScreenPos < len(positions) - 1:
                        initScreenPos = initScreenPos + 1
            elif event.type == pygame.FINGERDOWN:
                finger_x, finger_y = event.pos
                leftThreshold = getBigScreen().get_size()[0] // 3
                rightThreshold = leftThreshold * 2
                upThreshold = getBigScreen().get_size()[1] // 3
                if finger_x < leftThreshold:
                    if initScreenPos > 0:
                        initScreenPos = initScreenPos - 1
                elif finger_x > rightThreshold:
                    if initScreenPos < len(positions) - 1:
                        initScreenPos = initScreenPos + 1
                elif finger_y < upThreshold:
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

            if event.type == pygame.QUIT:
                quitting = True
                running = False

        if pygame.mouse.get_pressed()[1]:
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

        getBigScreen().blit(backgroundImage, backgroundImage.get_rect())
        showInitSelections(getBigScreen(), positions, selections, initCircleRadius, texts, titleTexts, titleTextPositions, creditTexts, creditTextPositions, externalExampleOverallText, externalExampleOverallPosition, externalExampleTeamText, externalExampleTeamSelectionPosition, externalExampleText, externalExampleSelectionPosition, ouluExampleText, ouluExampleSelectionPosition, news, newsPosition, worldExampleText, worldExampleSelectionPosition)
        showInitArrow(getBigScreen(), positions[initScreenPos], arrowScale)
        if gameSettings.infoBox:
            showInfoBoxTxt(getBigScreen())
        pygame.display.flip()
        await asyncio.sleep(0)

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
    elif retSettings[2] == "pacemaker":
        gameSettings.pacemaker = randrange(1, 4)
        gameSettings.speed = "regular"
        gameSettings.continuous = False
    else:
        gameSettings.speed = "superfast"
        gameSettings.pacemaker = 0
        gameSettings.continuous = False

    if retSettings[3] == "infinite-oulu":
        gameSettings.infiniteOulu = True
        gameSettings.infiniteWorld = False
        gameSettings.externalExample = ""
    if retSettings[3] == "infinite-world":
        gameSettings.infiniteOulu = False
        gameSettings.infiniteWorld = True
        gameSettings.infiniteWorldCity = worldExampleText
        gameSettings.externalExample = ""
        uiRenderImmediate(loadingPosition, loadingText)
    elif retSettings[3] == "external-team" or retSettings[3] == "external-map":
        gameSettings.infiniteOulu = False
        gameSettings.infiniteWorld = False
        gameSettings.externalExample = externalExampleText
        gameSettings.externalExampleTeam = externalExampleTeamText
    pygame.time.set_timer(TIMER_EVENT, 0)
    return quitting, gameSettings
