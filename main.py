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

__version__ = "1.0.3"

import time
import math
import asyncio
from datetime import datetime, timedelta

from sprintomatic.modules.routeAI import initializeAITables, closeAITables, initializeAINextTrack, initializeAINextTrackAsync, getReadyShortestRoutes, getReadyShortestRoutesAsync
from sprintomatic.modules.gameSettings import returnSettings, returnConfig
from sprintomatic.modules.mathUtils import angleOfLine, angleOfPath, getRandomAngle, calculatePathDistance, angleDifference, fromRadiansToDegrees
from sprintomatic.modules.trackCreator import createAutoControls, createAmazeControls
from sprintomatic.modules.gameUIUtils import uiEarlyInit, uiLateQuit, uiFlushEvents
from sprintomatic.modules.initScreenUI import initScreen, veryFirstTime
from sprintomatic.modules.gameUI import uiInit, uiInitStartTriangle, uiStartControlEffect, uiControlEffectEnded, uiCenterTurnZoomTheMap, uiAnimatePlayer, uiAnimatePacemaker, uiRenderRoutes, uiRenderControls, uiCompleteRender, uiEvent, uiClearCanvas, raiseControlApproachZoom, lowerControlApproachZoom, uiRenderPacemakerText, uiRenderAIText, uiControlEffectRestart, uiRenderExternalMapInfo, uiStoreAnalysis, uiClearBuffers
from sprintomatic.modules.gameEngine import startOverPlayerRoute, playerRoute, calculateNextStep, closeToControl, quiteCloseToControl, longLapEveryOther, generateAngleStep, normalizeAngleStep, defaultAngle, getPlayerRoute, getPacemakerThreshold, getPacemakerPos
from sprintomatic.modules.pathPruning import calculatePathWeightedDistance
from sprintomatic.modules.gameSounds import initSounds, stopSounds, maintainRunningStepEffect, startMelody, startElevatorMelody, stopMelody, startBirds, stopBirds, shoutEffect, pacemakerShoutEffect, finishEffect, startEffect, stopEffects
from sprintomatic.modules.imageDownloader import downloadExternalImageData, downloadExternalWorldCityMap, downloadNews

from sprintomatic.modules.perfSuite import perfClearSuite, perfActivate, perfAddStart, perfAddStop, perfBenchmark


# Re-initialize the game state, done each time a new run is started
async def setTheStageForNewRound(cfg):
    global angle
    global position
    global startTime
    global finishTexts
    global nextControl
    global reachedControl
    global playerRoutes
    global playerRoutesArray
    global shortestDistance
    global playerDistance
    global shortestWeightedDistance
    global playerWeightedDistance
    global autoControls
    global pacemakerPath
    global pacemakerSteps
    global pacemakerStartThreshold
    global pacemakerPosition
    global pacemakerAngle
    global pacemakerStep
    global aiCounter
    global shortestRoutesArray
    global shortestRoutesArrayAsync
    global shortestRoutes
    global futureShortestRoutes
    global trackLengthInPixels
    global amazeCounter
    global difficulty
    global beautifiedLeft
    global beautifiedRight
    global amazeThresholdWaiting
    global phoneRenderSkipCtr
    global phoneRenderSkipMax

    phoneRenderSkipMax = 0
    phoneRenderSkipCtr = 0

    # Ensure we have a list of controls
    ctrls = []
    if gameSettings.amaze:
#        perfAddStart("crAmaze")
        ctrls, shortestRoutesArray, beautifiedLeft, beautifiedRight, difficulty = await createAmazeControls(cfg, gameSettings.distributionOfControlLegs, gameSettings.metersPerPixel, faLookup, saLookup, ssaLookup, vsaLookup)
        beautifiedLeft.reverse()
#        perfAddStop("crAmaze")

    else:
#        perfAddStart("crTrack")
        ctrls, shortestRoutesArray = await createAutoControls(cfg, trackLengthInPixels, gameSettings.distributionOfControlLegs, gameSettings.metersPerPixel, faLookup, saLookup, ssaLookup, vsaLookup, gameSettings.pacemaker)
#        perfAddStop("crTrack")

#    perfAddStart("crOth")
    news = await downloadNews()

    # Initialize evereything that has to be initialized for a new run
    if ctrls and len(ctrls) > 1:

        # effects initialization
        uiControlEffectRestart()
        startEffect()
        await asyncio.sleep(0)
        uiStartControlEffect(0)

        zoom = gameSettings.zoom
        angle = angleOfLine(ctrls[:2])
        position = ctrls[0]
        uiInitStartTriangle(angle, position)
        if gameSettings.amaze:
            angle = getRandomAngle()
        nextControl = 1
        reachedControl = 0
        inTunnel = False
        playerRoutesArray = []
        playerRoutes = []
        startOverPlayerRoute()
        if gameSettings.accurate:
            initializeAINextTrack(ctrls, faLookup, saLookup, ssaLookup, vsaLookup, gameSettings.pacemaker)
            shortestRoutesArray = getReadyShortestRoutes()
        await initializeAINextTrackAsync(ctrls, faLookup, saLookup, ssaLookup, vsaLookup, gameSettings.pacemaker)
        shortestRoutesArrayAsync = await getReadyShortestRoutesAsync(reachedControl)
        shortestRoutes = []
        futureShortestRoutes = []
        startTime = datetime.now()
        finishTexts = ["", "", ""]
        shortestDistance = 0.0
        playerDistance = 0.0
        shortestWeightedDistance = 0.0
        playerWeightedDistance = 0.0
        state = "running"
        inTunnelPacmaker = False
        pacemakerPath = None
        pacemakerSteps = 0
        pacemakerStartThreshold = 0
        pacemakerPosition = None
        amazeThresholdWaiting = 0
        pacemakerAngle = 0
        pacemakerStep = -5
        aiCounter = 0
    else:
        ctrls = []
#    perfAddStop("crOth")
    return ctrls


# Some convenience functions
def controlFound(ctrls, pos, ctrl):
    return ctrl and closeToControl(pos, ctrls[ctrl]) and ctrl + 1 < len(controls)

def controlApproached(ctrls, pos, ctrl):
    return ctrl and quiteCloseToControl(pos, ctrls[ctrl]) and ctrl + 1 < len(controls)


def finishFound(ctrls, pos, ctrl):
    return ctrl and closeToControl(pos, ctrls[ctrl]) and ctrl + 1 >= len(controls)

def generateFinishTexts(totTime, shortestDistance, shortestWeightedDistance, playerWeightedDistance):
    percentage = 0
    if shortestWeightedDistance != 0:
        percentage = int(100.0 * (playerWeightedDistance - shortestWeightedDistance) / shortestWeightedDistance)
    return [str(totTime).split('.', 2)[0], str(int(shortestDistance * gameSettings.metersPerPixel)), str(percentage)]


def startControlFanfare(nextC):
    return nextC, nextC + 1


def startFinishFanfare(nextC):
    return nextC, 0

def stripMapName(mapUrl):
  endInd = mapUrl.rfind(".")
  startInd = mapUrl.rfind("/")
  if endInd + 4 <= len(mapUrl):
      endInd = endInd + 4
  return mapUrl[startInd + 1: endInd]


def finishFanfareStarted(reachedC, nextC):
    return reachedC > 0 and nextC == 0


# Update the player and pacemaker route statistics at each control and at finish
async def updateRoutesAndDistances(amaze):
    global playerRoutes
    global playerRoutesArray
    global playerDistance
    global shortestDistance
    global shortestWeightedDistance
    global playerWeightedDistance
    global shortestRoutesArray
    global shortestRoutes
    global futureShortestRoutes
    if not amaze or not playerRoutes:
        playerRoutes = [ getPlayerRoute() ]
    playerRoutesArray.append(playerRoutes)
    playerDistance = playerDistance + calculatePathDistance(playerRoutes[0])
    if gameSettings.accurate:
        shortestRoutesArray = getReadyShortestRoutes()
    shortestRoutesArrayAsync = await getReadyShortestRoutesAsync(reachedControl)
    shortestRoutes = shortestRoutesArray[reachedControl - 1] if reachedControl > 0 else []
    futureShortestRoutes = shortestRoutesArray[reachedControl] if reachedControl > 0 and reachedControl < len(shortestRoutesArray) else []
    if not gameSettings.accurate and reachedControl > 0:
        shortestRoutesProposal = shortestRoutesArrayAsync[reachedControl - 1]
        if shortestRoutesProposal:
            if calculatePathWeightedDistance(shortestRoutesProposal, saLookup, ssaLookup, vsaLookup) < calculatePathWeightedDistance(shortestRoutes[0], saLookup, ssaLookup, vsaLookup):
                shortestRoutes = [shortestRoutesProposal]
                shortestRoutesArray[reachedControl - 1] = shortestRoutes
        if reachedControl < len(shortestRoutesArrayAsync):
            futureShortestRoutesProposal = shortestRoutesArrayAsync[reachedControl]
            futureShortestRoutesProposal.reverse()
            if futureShortestRoutesProposal:
                futureShortestRoutes = [futureShortestRoutesProposal]

    await uiFlushEvents()
    if shortestRoutes:
        shortestDistance = shortestDistance + calculatePathDistance(shortestRoutes[0])
        shortestWeightedDistance = shortestWeightedDistance + calculatePathWeightedDistance(shortestRoutes[0], saLookup, ssaLookup, vsaLookup)
        await asyncio.sleep(0)
        playerWeightedDistance = playerWeightedDistance + calculatePathWeightedDistance(playerRoutes[0], saLookup, ssaLookup, vsaLookup)
    startOverPlayerRoute()


# This is the main loop
async def main():
    global aiCounter
    global angle
    global autoControls
    global config
    global controls
    global externalImageData
    global externalWorldCityMap
    global externalZoom
    global faLookup
    global finishTexts
    global futureShortestRoutes
    global gameMovingStartThreshold
    global gameSettings
    global generatedOrDownloadedMap
    global inTunnel
    global inTunnelPacemaker
    global news
    global nextControl
    global pacemakerAngle
    global pacemakerPath
    global pacemakerPosition
    global pacemakerPrepareForShout
    global pacemakerStartThreshold
    global pacemakerStep
    global pacemakerSteps
    global playerDistance
    global playerRoutes
    global playerRoutesArray
    global playerWeightedDistance
    global position
    global quitting
    global reachedControl
    global saLookup
    global shortestDistance
    global shortestRoutes
    global shortestRoutesArray
    global shortestRoutesArrayAsync
    global shortestWeightedDistance
    global showInitScreen
    global ssaLookup
    global startTime
    global tmpMetersPerPixel
    global trackLengthInPixels
    global tunnelLookup
    global vsaLookup
    global amazeCounter
    global difficulty
    global beautifiedLeft
    global beautifiedRight
    global amazeThresholdWaiting
    global benchmark
    global phoneRenderSkipCtr
    global phoneRenderSkipMax

    benchmark = await perfBenchmark()

    # all the initialization that happens only once at the startup
    perfClearSuite()

    # this can be used in debugging
#    perfActivate()

#    perfAddStart("ini")
    gameSettings = returnSettings()
    if gameSettings.accurate:
        # start AI processes
        initializeAITables()
    portrait = uiEarlyInit(gameSettings.fullScreen, benchmark)
    veryFirstT = await veryFirstTime(benchmark, portrait)
    externalImageData, offline = await downloadExternalImageData(gameSettings.ownMasterListing)
    if offline:
         gameSettings.offline = offline
    externalWorldCityMap = await downloadExternalWorldCityMap()
    news = await downloadNews()
    initSounds(gameSettings.soundRoot, benchmark)
    
    # statistics and route display initial values
    shortestRoutesArray = []
    playerRoutesArray = []
    shortestRoutes = []
    futureShortestRoutes = []
    playerRoutes = []
    startTime = None
    totalTime = None
    inTunnel = False
    shortestDistance = None
    playerDistance = None
    shortestWeightedDistance = None
    playerWeightedDistance = None
    finishTexts = ["", "", ""]

    # pacemaker parameters
    pacemakerSteps = 0
    amazeCounter = 0
    pacemakerStartThreshold = 0
    pacemakerPosition = None
    pacemakerPath = None
    inTunnelPacemaker = False
    pacemakerAngle = 0
    pacemakerPrepareForShout = True
    pacemakerStep = -5

    # some counters to time the flushing/progressing the AI pools
    aiCounter = 0
    aiCounterThreshold = 30

    # threshold for the game to really start
    gameMovingStartThreshold = 5
    amazeThresholdWaiting = 0
    amazeTimeThreshold = 10
    amazeMidTimeThreshold = 15
    amazeSecondTimeThreshold = 20
    amazeAcceptedAngleDifference = math.pi / 10
    difficulty = 0

    # the choice between specific route file and an automatic route
    autoControls = True
    if gameSettings.routeFileName:
        autoControls = False

    # Show init screen only if no specific map file provided in command line
    showInitScreen = False 
    if not gameSettings.mapFileName:
        showInitScreen = True
    
    # these basically contain the game state
    nextControl = None
    reachedControl = None
    quitting = False
    firstTime = True
    preInitSleep = 0 # after first start, turn this to 1
#    perfAddStop("ini")

    # This is the main loop
    while not quitting:
        running = True
        if showInitScreen:
            startBirds()
            await asyncio.sleep(preInitSleep)
            preInitSleep = 1
            await uiFlushEvents()
            (quitting, gameSettings, fingerInUse) = await initScreen(gameSettings.imageRoot, gameSettings, externalImageData, externalWorldCityMap, news, benchmark, portrait)
            running = True
            if quitting:
                running = False
            stopBirds()
            await asyncio.sleep(0)
            startElevatorMelody()
            await asyncio.sleep(0)
        if not quitting:
#            perfAddStart("cfg")
            config, controls, faLookup, saLookup, ssaLookup, vsaLookup, tunnelLookup, generatedOrDownloadedMap, tmpMetersPerPixel, externalZoom = await returnConfig(gameSettings, externalImageData, externalWorldCityMap, benchmark, portrait)
#            perfAddStop("cfg")
#            perfAddStart("stage")

            # scale from multiple sources...
            if gameSettings.infiniteOulu:
                gameSettings.metersPerPixel = 1
            else:
                gameSettings.metersPerPixel = 1
                if tmpMetersPerPixel > 0:
                    gameSettings.metersPerPixel = tmpMetersPerPixel

            # if received externalZoom
            angle = defaultAngle()
            zoom = gameSettings.zoom
            if externalZoom > 0:
                zoom = externalZoom

            amazeCounter = 0

            # Special case: in case external map selected but network down
            if generatedOrDownloadedMap is None and not gameSettings.mapFileName:
                running = False
            else:
                # Ok for init...

                # generic default unless modified when setting the stage
                position = uiInit(gameSettings.mapFileName, gameSettings.imageRoot, generatedOrDownloadedMap, gameSettings.metersPerPixel, benchmark)

                trackLengthInPixels = gameSettings.trackLength / gameSettings.metersPerPixel

                # initializations specific to a particular track
                controls = await setTheStageForNewRound(config)
                uiClearBuffers()
                firstTime = True

                # Flush events again
                await uiFlushEvents()

            # Stop the elevator music
            stopMelody()
            await asyncio.sleep(0)
#            perfAddStop("stage")

        # main loop of the gameplay itself:
        while running and controls and not quitting:
            # Keep on running (sound)
            if datetime.now() - startTime > timedelta(seconds=gameMovingStartThreshold):
                maintainRunningStepEffect()
                await asyncio.sleep(0)

            # If we just moved or not
            movement = False

            # Event handling
            events = await uiEvent(gameSettings.infoBox, gameSettings.speed)

            for event in events:
                if datetime.now() - startTime > timedelta(seconds=gameMovingStartThreshold) and not (gameSettings.amaze and datetime.now() - startTime > timedelta(seconds=amazeTimeThreshold)):
                    if event == "left":
                        angle = angle + generateAngleStep()
                        movement = True
                    elif event == "right":
                        angle = angle - generateAngleStep()
                        movement = True
                if event == "release":
                    normalizeAngleStep()
                elif event == "quit":
                    running = False
                    stopMelody()
                    await asyncio.sleep(0)
                    stopEffects()
                    if not showInitScreen:
                        quitting = True
                    break
                elif event == "tick":
                    if datetime.now() - startTime > timedelta(seconds=gameMovingStartThreshold):
                        # Progress the player position
                        if not gameSettings.amaze:
                            position, angle, inTunnel = calculateNextStep(faLookup, saLookup, ssaLookup, vsaLookup, tunnelLookup, position, angle, movement, gameSettings.speed, gameSettings.metersPerPixel)

                        # Progress the pacemaker position
                        if pacemakerPath is not None:
                            pacemakerSteps = pacemakerSteps + 1
                            pacemakerAdvancement = 0
                            if pacemakerSteps > pacemakerStartThreshold:
                                pacemakerAdvancement = pacemakerSteps - pacemakerStartThreshold
                            pacemakerSpeeder = 1.0
                            if benchmark == "phone" and not portrait:
                                pacemakerSpeeder = 2.0
                            pacemakerPosition, pacemakerAngle, inTunnelPacemaker = getPacemakerPos(saLookup, ssaLookup, vsaLookup, tunnelLookup, pacemakerPath, pacemakerAdvancement, gameSettings.speed, gameSettings.metersPerPixel / pacemakerSpeeder, gameSettings.pacemaker)

                    # Flush the AI pools every now and then
                    aiCounter = aiCounter + 1
                    if aiCounter > aiCounterThreshold:
                        aiCounter = 0
                        if gameSettings.accurate:
                            shortestRoutesArray = getReadyShortestRoutes()
                        shortestRoutesArrayAsync = await getReadyShortestRoutesAsync(reachedControl)


                    # this "state machine" is run only when there is controls
                    if controls:
                        # we have three explicit transitions at this level
                        # 1. a control is found
                        if controlApproached(controls, position, nextControl):
                            raiseControlApproachZoom()
                        else:
                            lowerControlApproachZoom()
                        if controlFound(controls, position, nextControl):
                            reachedControl, nextControl = startControlFanfare(nextControl)
                            stopMelody()
                            await asyncio.sleep(0)
                            shoutEffect()
                            await asyncio.sleep(0)
                            if longLapEveryOther(controls[reachedControl], controls[nextControl]):
                                startMelody()
                            await updateRoutesAndDistances(gameSettings.amaze)
                            if futureShortestRoutes and len(futureShortestRoutes[0]) > 1:
                                pacemakerPath = futureShortestRoutes[0].copy()
                                pacemakerStartThreshold = getPacemakerThreshold(pacemakerPath, gameSettings.pacemaker)
                                pacemakerSteps = 0
                            uiStartControlEffect(reachedControl)

                        # 1.99 separate ending for "amaze"
                        elif gameSettings.amaze and datetime.now() - startTime > timedelta(seconds=amazeSecondTimeThreshold):
                            amazeThresholdWaiting = 0
                            amazeCounter = amazeCounter + 1
                            position = controls[-1]
                            reachedControl = len(controls) - 1
                            nextControl = 0
                            if amazeCounter >= 5:
                                running = False
                            else:
                                controls = await setTheStageForNewRound(config)
                                uiClearBuffers()
                                firstTime = True

                        elif gameSettings.amaze and datetime.now() - startTime > timedelta(seconds=amazeMidTimeThreshold):
                            beautifiedLeftDistance = calculatePathDistance(beautifiedLeft)
                            beautifiedRightDistance = calculatePathDistance(beautifiedRight)
                            if beautifiedLeftDistance > 2 * beautifiedRightDistance:
                                playerRoutes = [ beautifiedRight ]
                            elif beautifiedRightDistance > 2 * beautifiedLeftDistance:
                                playerRoutes = [ beautifiedLeft ]
                            else:
                                playerRoutes = [ beautifiedLeft + beautifiedRight ]

                        # 1.999 separate pre-ending for "amaze"
                        elif gameSettings.amaze and datetime.now() - startTime > timedelta(seconds=amazeTimeThreshold):
                            if amazeThresholdWaiting == 0:
                                amazeThresholdWaiting = amazeMidTimeThreshold
                                reachedControl, nextControl = startFinishFanfare(nextControl)
                                stopMelody()
                                await updateRoutesAndDistances(gameSettings.amaze)
                                shortestRoutes = shortestRoutesArray[reachedControl - 1]
                                sRoutes = shortestRoutes[0].copy()
                                sRoutes.reverse()
                                uiStartControlEffect(reachedControl)
                                wantedAngle = angleOfPath(sRoutes, 7)
                                angleDiff = angleDifference(angle, wantedAngle)
                                if angleDiff < amazeAcceptedAngleDifference:
                                    finishTexts[1] = "I AGREE!"
                                    shoutEffect()
                                    await asyncio.sleep(0)
                                elif angleDiff < amazeAcceptedAngleDifference * 2:
                                    finishTexts[1] = "ALMOST RIGHT..."
                                    shoutEffect()
                                    await asyncio.sleep(0)
                                else:
                                    finishTexts[1] = "REALLY?"
                                    pacemakerShoutEffect()
                                    await asyncio.sleep(0)
                                finishTexts[2] = str(round(fromRadiansToDegrees(angleDiff), 0))
                                finishTexts[0] = str(difficulty)

                        # 2. the finish line is found
                        elif finishFound(controls, position, nextControl):
                            reachedControl, nextControl = startFinishFanfare(nextControl)
                            pacemakerRunning = False
                            stopMelody()
                            await asyncio.sleep(0)
                            finishEffect()
                            await asyncio.sleep(0)
                            await updateRoutesAndDistances(gameSettings.amaze)
                            shortestRoutes = shortestRoutesArray[reachedControl - 1]
                            if not gameSettings.accurate:
                                shortestRoutesProposal = shortestRoutesArrayAsync[reachedControl - 1]
                                if shortestRoutesProposal:
                                    if calculatePathWeightedDistance(shortestRoutesProposal, saLookup, ssaLookup, vsaLookup) < calculatePathWeightedDistance(shortestRoutes[0], saLookup, ssaLookup, vsaLookup):
                                        shortestRoutes = [shortestRoutesProposal]
                                        shortestRoutesArray[reachedControl - 1] = shortestRoutes
                            futureShortestRoutes = []
                            uiStartControlEffect(reachedControl)
                            # calculate statistics at finish
                            if startTime is not None:
                                totalTime = datetime.now() - startTime - timedelta(seconds=gameMovingStartThreshold)
                            else:
                                totalTime = timedelta(seconds=0)
                            finishTexts = generateFinishTexts(totalTime, shortestDistance, shortestWeightedDistance, playerWeightedDistance)
                            if gameSettings.analysis:
                                mergedArray = shortestRoutesArray.copy()
                                if not gameSettings.accurate:
                                    shortestRoutesArrayAsync = await getReadyShortestRoutesAsync(len(mergedArray)-1)
                                    for ind in range(len(mergedArray)):
                                        if ind < len(shortestRoutesArrayAsync) and shortestRoutesArrayAsync[ind]:
                                            mergedArray[ind] = [shortestRoutesArrayAsync[ind]]
                                uiStoreAnalysis(mergedArray, playerRoutesArray, controls, finishTexts)

                        # 3. the track is totally done
                        elif finishFanfareStarted(reachedControl, nextControl) and uiControlEffectEnded():
                            if not autoControls or not gameSettings.continuous: # then run only once
                                running = False
                            else:
                                controls = await setTheStageForNewRound(config)
                                uiClearBuffers()
                                firstTime = True
                                # There might have been a delay
                                await uiFlushEvents()


                        # Now the render phase, need to sort out the pacemaker code

                        if phoneRenderSkipCtr == 0:
                            if running:
                                # Now enter the rendering phase
                                shift = uiClearCanvas(controls, shortestRoutesArray, reachedControl, benchmark)

                                if gameSettings.pacemaker == 0:
                                    uiRenderRoutes(shortestRoutes, "shortest", shift)
                                    uiRenderRoutes(playerRoutes, "player", shift)
                                uiRenderControls(controls, gameSettings.pacemaker, gameSettings.amaze, shift)

                                extraScale = 1.0
                                if benchmark == "phone":
                                    extraScale = 1.5

                                if gameSettings.pacemaker != 0 and pacemakerPath is not None and pacemakerPosition is not None:
                                    if pacemakerPosition == pacemakerPath[-1]:
                                        uiAnimatePacemaker(pacemakerPosition, pacemakerAngle, 1.0 * extraScale, gameSettings.pacemaker, inTunnelPacemaker, True, shift)
                                        pacemakerStep = -5
                                        if pacemakerPrepareForShout:
                                            pacemakerShoutEffect()
                                            pacemakerPrepareForShout = False
                                    elif pacemakerPosition == pacemakerPath[0]:
                                        pacemakerStep = pacemakerStep + 1
                                        if pacemakerStep > 5:
                                            pacemakerStep = -5

                                        uiAnimatePacemaker(pacemakerPosition, pacemakerAngle, extraScale * (1.5 + abs(pacemakerStep) * 0.1), gameSettings.pacemaker, inTunnelPacemaker, True, shift)
                                        pacemakerPrepareForShout = True
                                    else:
                                        pacemakerStep = -5
                                        pacemakerPrepareForShout = True
                                        uiAnimatePacemaker(pacemakerPosition, pacemakerAngle, 1.0 * extraScale, gameSettings.pacemaker, inTunnelPacemaker, True, shift)
                                elif gameSettings.pacemaker != 0 and pacemakerPath == None:
                                    pacemakerStep = pacemakerStep + 1
                                    if pacemakerStep > 5:
                                        pacemakerStep = -5
                                    pacemakerPrepareForShout = True
                                    uiAnimatePacemaker(controls[nextControl], pacemakerAngle, extraScale * (1.5 + abs(pacemakerStep) * 0.1), gameSettings.pacemaker, inTunnelPacemaker, True, shift)

                            uiCenterTurnZoomTheMap(position, zoom, angle, benchmark, shift)

                            # After that it is ok to draw to "big screen"
                            moveLegs = True if datetime.now() - startTime > timedelta(seconds=gameMovingStartThreshold) else False
                            aiTextNeeded = False
                            pacemakerTextNeeded = False
                            amazeTextNeeded = False
                            if gameSettings.pacemaker != 0:
                                if (len(futureShortestRoutes) == 0 or len(futureShortestRoutes[0]) == 0) and (reachedControl > 0 and reachedControl < len(controls) - 1):
                                    aiTextNeeded = True
                                else:
                                    pacemakerTextNeeded = True

                            externalMapInfoTexts = []
                            if gameSettings.externalExampleTeam and gameSettings.externalExample:
                                for item in externalImageData:
                                    if gameSettings.externalExampleTeam == item["team-name"]:
                                        for subitem in item["sub-listing"]:
                                            if gameSettings.externalExample == subitem["name"]:
                                                externalMapInfoTexts = [stripMapName(subitem["map-url"]), subitem["map-license"], subitem["map-credits"], stripMapName(subitem["lookup-png-url"]), subitem["lookup-png-license"], subitem["lookup-png-credits"]]
                                                break
                            if gameSettings.noUiTest != "yes":
                                await uiCompleteRender(finishTexts, externalMapInfoTexts, gameSettings.pacemaker, pacemakerTextNeeded, aiTextNeeded, gameSettings.amaze, difficulty, firstTime, moveLegs, inTunnel, portrait, fingerInUse)
                            firstTime = False

                        if benchmark == "phone":
                            phoneRenderSkipCtr = phoneRenderSkipCtr + 1
                            if phoneRenderSkipCtr > phoneRenderSkipMax:
                                phoneRenderSkipCtr = 0

            await asyncio.sleep(0)

    # Final freeing of resources
    stopSounds()
    uiLateQuit()

    if gameSettings.accurate:
        # free multiprocessing resources, too
        closeAITables()

if __name__ == "__main__":
    asyncio.run(main())
