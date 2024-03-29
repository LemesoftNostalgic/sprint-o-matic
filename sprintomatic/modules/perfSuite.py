import time

import pygame
from .gameUIUtils import getBigScreen, getMasterFont, getTrackColor, getWhiteColor
from .routeAI import slowAccurateCalculateShortestRouteAsync
import asyncio

perfDBFlag = False
perfDB = {}
maxQueue = 10

def perfClearSuite():
    global perfDB
    perfDB.clear()    

def perfActivate():
    global perfDBFlag
    perfDBFlag = True
    
def perfDeActivate():
    global perfDBFlag
    perfDBFlag = False

def perfAddStart(key):
    global perfDBFlag
    global perfDB
    if perfDBFlag:
        startTime = (time.time(), None)
        if key not in perfDB:
            perfDB[key] = [startTime]
        elif perfDB[key][-1][1] is None:
            perfDB[key][-1] = startTime
        else:
            perfDB[key].append(startTime)
            perfDB[key].pop(0)

def perfAddStop(key):
    global perfDBFlag
    global perfDB
    if perfDBFlag:
        stopTime = time.time()
        if key not in perfDB:
            pass
        elif perfDB[key][-1][1] is None:
            perfDB[key][-1] = (perfDB[key][-1][0], stopTime)

def perfShowResults(titleStr):
    global perfDBFlag
    global perfDB
    if perfDBFlag:
        y = 30
        x = 0
        perfText = pygame.font.Font(getMasterFont(), 20).render(titleStr, True, getTrackColor())
        perfRect = perfText.get_rect()
        perfRect.x = x
        perfRect.y = y
        getBigScreen().blit(perfText, perfRect)
        for item in perfDB:
            numDeltas = 0
            totDelta = 0.0
            for queueItem in perfDB[item]:
                if queueItem[1] is not None:
                    numDeltas = numDeltas + 1
                    totDelta = totDelta + queueItem[1] - queueItem[0]
            if numDeltas:
                trueDelta = round(totDelta / numDeltas, 5)
                y = y + 30
                perfStr = item + ": " + str(trueDelta)
                perfText = pygame.font.Font(getMasterFont(), 20).render(perfStr, True, getTrackColor())
                perfRect = perfText.get_rect()
                perfRect.x = x
                perfRect.y = y
                pygame.draw.rect(getBigScreen(), getWhiteColor(), perfRect, 0)
                getBigScreen().blit(perfText, perfRect)


async def perfBenchmark():
    start_time = time.time()
    await slowAccurateCalculateShortestRouteAsync([(0,20), (40,20), {1: {(20,20): True}}, {1: {}}, {1:{}}, {1:{}}, 1, 0])
    perfAddStop("benchmark")
    full_time = time.time() - start_time
    if full_time < 0.04:
        return "pc"
    elif full_time < 0.4:
        return "web"
    else:
        return "phone"

