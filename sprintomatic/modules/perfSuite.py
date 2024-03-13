import time

import pygame
from .gameUIUtils import getBigScreen, getMasterFont, getTrackColor

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

def perfShowResults():
    global perfDBFlag
    global perfDB
    if perfDBFlag:
        y = 0
        x = 0
        for item in perfDB:
            numDeltas = 0
            totDelta = 0.0
            for queueItem in perfDB[item]:
                if queueItem[1] is not None:
                    numDeltas = numDeltas + 1
                    totDelta = totDelta + queueItem[1] - queueItem[0]
            trueDelta = round(totDelta / numDeltas, 5)
            y = y + 30
            perfStr = item + ": " + str(trueDelta)
            perfText = pygame.font.Font(getMasterFont(), 20).render(perfStr, True, getTrackColor())
            perfRect = perfText.get_rect()
            perfRect.x = x
            perfRect.y = y
            getBigScreen().blit(perfText, perfRect)
    pygame.display.flip()

    
