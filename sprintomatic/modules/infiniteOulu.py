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

from random import randrange, uniform
import pygame
import asyncio
import math

from .mathUtils import rotateVector, rotatePoint, getBoundingBox, polygonCreate, polygonContainsWithLookup
from .gameUIUtils  import uiFlushEvents
from .perfSuite import perfAddStart, perfAddStop

# types
FOREST = '.'
DEEPFOREST = ':'
VERYDEEPFOREST = ';'
OPENAREA = '^'
SOLIDBLACK = '*'
NARROWBLACK = 'I'
SOLIDGREEN = 'G'
OLIVEGREEN = '/'
HOUSEINTERNAL = 'h'
SHELTERINTERNAL = 's'
WATER = '~'
ASPHALT = '#'
BROWNX = 'x'
BLACKX = 'X'
STONE = 'o'
BROWNSTONE = 'p'
MARSH = '='
GREENCIRCLE = 'O'
PATHBLACK = '('
PATHWHITE = ')'

colors = {
    FOREST:          (255,255,255),
    DEEPFOREST:      (195,230,200),
    VERYDEEPFOREST:  (175,220,180),
    OPENAREA:        (255,190,70),
    SOLIDBLACK:      (40,45,50),
    PATHBLACK:       (40,45,50),
    PATHWHITE:       (255,255,255),
    NARROWBLACK:     (45,50,55),
    SOLIDGREEN:      (35,180,90),
    OLIVEGREEN:      (170,167,56),
    HOUSEINTERNAL:   (130, 135, 140),
    SHELTERINTERNAL: (215, 216, 217),
    WATER:           (55, 205, 245),
    ASPHALT:         (250, 210, 175),
    BROWNX:          (224, 113, 30),
    BLACKX:          (40,45,50),
    STONE:           (40,45,50),
    BROWNSTONE:      (224, 113, 30),
    MARSH:           (55, 206, 245),
    GREENCIRCLE:     (35,180,90)
    }


controlBend = 1
fenceDeltaMax = 4
fenceDeltaGap = 3
holeDeltaMax = 4
rotateOneOutOf = 2
minMarkedLineSegment = 12

countoursMinOutOf = 3
countoursMaxOutOf = 4
countoursMinKernelWidth = 4
countoursMaxKernelWidth = 5

terrains = ["shortLeg", "mediumLeg", "longLeg"]

def terranizer(terrain):
    global forestBlockOneOutOf
    global lakeInForestOneOutOf
    global pathInForestOneOutOf
    global shelterOutOfHouse
    global streamInForestOneOutOf
    global hutOutOfCottages
    global verticalFenceOneOutOf
    global holeInForestOneOutOfInverse
    global difficultForestHowMany
    global houseRotOrientations
    global bushHowMany
    global miniBlockOneOutOf
    global spotnessFactor
    global maxNumCottages
    global maxHouseForms

    if terrain == terrains[0]:
        forestBlockOneOutOf = 12
        lakeInForestOneOutOf = 2
        pathInForestOneOutOf = 2
        shelterOutOfHouse = 7
        streamInForestOneOutOf = 3
        hutOutOfCottages = 3
        verticalFenceOneOutOf = 3
        holeInForestOneOutOfInverse = 5
        difficultForestHowMany = 3
        houseRotOrientations = 4
        bushHowMany = 4
        miniBlockOneOutOf = 2
        spotnessFactor = 4
        maxNumCottages = 4
        maxHouseForms = 6
    elif terrain == terrains[1]:
        forestBlockOneOutOf = 8
        lakeInForestOneOutOf = 20
        pathInForestOneOutOf = 8
        shelterOutOfHouse = 6
        streamInForestOneOutOf = 1
        hutOutOfCottages = 6
        verticalFenceOneOutOf = 5
        holeInForestOneOutOfInverse = 2
        difficultForestHowMany = 8
        houseRotOrientations = 3
        bushHowMany = 6
        miniBlockOneOutOf = 4
        spotnessFactor = 2
        maxNumCottages = 2
        maxHouseForms = 5
    elif terrain == terrains[0]:
        forestBlockOneOutOf = 6
        lakeInForestOneOutOf = 2
        pathInForestOneOutOf = 4
        shelterOutOfHouse = 15
        streamInForestOneOutOf = 10
        hutOutOfCottages = 2
        verticalFenceOneOutOf = 2
        holeInForestOneOutOfInverse = 10
        difficultForestHowMany = 1
        houseRotOrientations = 2
        bushHowMany = 2
        miniBlockOneOutOf = 6
        spotnessFactor = 8
        maxNumCottages = 10
        maxHouseForms = 2

# some initial setting
terranizer(terrains[0])

# categories
fencekind = [SOLIDBLACK, SOLIDBLACK, SOLIDBLACK, NARROWBLACK, SOLIDGREEN]
partialfencekind = [SOLIDBLACK, SOLIDBLACK, NARROWBLACK, SOLIDGREEN]
overlapkind = [FOREST, OPENAREA, ASPHALT]
reolivekind = [FOREST, OPENAREA, ASPHALT, SHELTERINTERNAL, DEEPFOREST, VERYDEEPFOREST]
fencefiller = [NARROWBLACK, FOREST, FOREST]
housekind = [SOLIDBLACK, HOUSEINTERNAL]
shelterkind = [NARROWBLACK, SHELTERINTERNAL]
slowing = [DEEPFOREST, NARROWBLACK]
semislowing = [FOREST]
veryslowing = [VERYDEEPFOREST]
forbidden = [SOLIDGREEN, OLIVEGREEN, SOLIDBLACK, HOUSEINTERNAL, WATER]
spotmodifying = [FOREST, DEEPFOREST,  OPENAREA,    ASPHALT]
newspotvalues = [STONE,  STONE,       GREENCIRCLE, BLACKX]
frontyardkind = [SOLIDGREEN, OLIVEGREEN, OPENAREA, ASPHALT]
backyardkind = [OLIVEGREEN, OPENAREA, ASPHALT]
yardkind = [OPENAREA, ASPHALT, ASPHALT]
specialareakind = [OPENAREA, ASPHALT, SHELTERINTERNAL]
specialareaportkind = [FOREST, NARROWBLACK]

# this one as color too, due to contours
contouroverlapkindcol = [colors[FOREST], colors[DEEPFOREST], colors[VERYDEEPFOREST], colors[OPENAREA], colors[OLIVEGREEN], colors[ASPHALT]]

# multiple houseforms, each containing a rectlist-pointlist pair
houseforms = [
      [ [[(0,0), (1, 1)]],
        [(0,0), (0,1), (1,1), (1,0)] ],

      [ [[(0, 0), (0.5, 1)], [(0.5, 0.5), (1, 1)]],
        [(0, 0), (0,1), (0.5,0.0), (0.5, 0.5), (1, 0.5), (1, 1)] ],

      # two repeats to add the likelihood of these
      [ [[(0,0), (1, 1)]],
        [(0,0), (0,1), (1,1), (1,0)] ],

      [ [[(0, 0), (0.5, 1)], [(0.5, 0.5), (1, 1)]],
        [(0, 0), (0,1), (0.5,0.0), (0.5, 0.5), (1, 0.5), (1, 1)] ],

      [ [[(0,0), (1, 0.33)], [(0, 0.33), (0.33, 0.66)]],
        [(0,0), (1,0), (1, 0.33), (0,0.66), (0.33,0.66), (0.33, 0.33)] ],

     [ [[(0,0), (0.33, 0.66)], [(0.33, 0.33), (0.66, 0.66)], [(0.66, 0), (1, 0.66)]],
       [(0,0), (0, 0.66), (0.33, 0.33), (0.33, 0.66), (1, 0), (1, 0.33)] ]
]


# generic functions
def createArea(dim):
    area = []
    for y in range(dim[1]):
        subArea = []
        for x in range(dim[0]):
            subArea.append(ASPHALT)
        area.append(subArea)
    png = pygame.Surface(dim)
    png.fill(colors[ASPHALT])
    mask = { "faLookup": {}, "saLookup": {}, "ssaLookup": {}, "vsaLookup": {}, "tunnelLookup": {}, "controls": []}
    return area, png, mask


def installOuluBlock(ouluPng, png, ouluMask, mask, position, blockSize, boundary):
    ouluPng.blit(png, (boundary + position[1] * (blockSize[1] + boundary), boundary + position[0] * (blockSize[0] + boundary)))
    xShift = boundary + position[1] * (blockSize[1] + boundary)
    yShift = boundary + position[0] * (blockSize[0] + boundary)
    for key in mask["faLookup"]:
        ouluMask["faLookup"][(xShift + key[0], yShift + key[1])] = True
    for key in mask["saLookup"]:
        ouluMask["saLookup"][(xShift + key[0], yShift + key[1])] = True
    for key in mask["ssaLookup"]:
        ouluMask["ssaLookup"][(xShift + key[0], yShift + key[1])] = True
    for key in mask["vsaLookup"]:
        ouluMask["vsaLookup"][(xShift + key[0], yShift + key[1])] = True
    for key in mask["tunnelLookup"]:
        ouluMask["tunnelLookup"][(xShift + key[0], yShift + key[1])] = True
    for control in mask["controls"]:
        ouluMask["controls"].append((xShift + control[0], yShift + control[1]))
    return ouluPng, ouluMask


def copyArea(area, png, mask):
    new, newPng, newMask = createArea((len(area[0]), len(area)))
    for y in range(len(area)):
        for x in range(len(area[0])):
            new[y][x] = area[y][x]
    return new, png, mask


def makeForest(area, png, mask):
    for y in range(len(area)):
        for x in range(len(area[0])):
            area[y][x] = FOREST
            mask["saLookup"][(x, y)] = True
    png.fill(colors[FOREST])
    return area, png, mask


# just a wrapper due to speed optimization
def copyAreaShallow(area, png, mask):
    return area, png, mask


def dumpArea(area, title):
    print(title, ":")
    for line in area:
        for elem in line:
            print(" ", elem, end="")
        print("")


def areaSetAt(area, png, mask, y, x, filltype):
    area[int(y)][int(x)] = filltype
    pt = (int(x), int(y))
    png.fill(colors[filltype], (pt, (1, 1)))
    if filltype in forbidden:
        mask["faLookup"][pt] = True
    elif filltype in slowing:
        mask["saLookup"][pt] = True
        mask["faLookup"].pop(pt, None)
    elif filltype in semislowing:
        mask["ssaLookup"][pt] = True
        mask["faLookup"].pop(pt, None)
    elif filltype in veryslowing:
        mask["vsaLookup"][pt] = True
        mask["faLookup"].pop(pt, None)
    elif filltype in SHELTERINTERNAL:
        mask["tunnelLookup"][pt] = True
        mask["faLookup"].pop(pt, None)
        mask["vsaLookup"].pop(pt, None)
        mask["saLookup"].pop(pt, None)
        mask["ssaLookup"].pop(pt, None)
    else:
        mask["faLookup"].pop(pt, None)


def areaSetAtVisualOnly(png, mask, y, x, filltype):
    pt = (int(x), int(y))
    if pt not in mask["faLookup"]:
        png.fill(colors[filltype], ((x, y), (1, 1)))


def queryForbiddenSpot(mask, y, x):
    pt = (int(x), int(y))
    if pt in mask["faLookup"]:
        return True
    return False


def markControlSpot(mask, y, x):
    if not queryForbiddenSpot(mask, y, x):
        pt = (int(x), int(y))
        if pt not in mask["controls"]:
            mask["controls"].append(pt)


def queryControlSpot(mask, y, x):
    pt = (int(x), int(y))
    if pt in mask["controls"]:
        return True
    return False


def removeControlSpot(mask, y, x):
    pt = (int(x), int(y))
    try:
        while True:
            mask["controls"].remove(pt)
    except ValueError:
        pass


def areaDrawSpot(area, png, mask, y, x, filltype):
    if area is not None:
        area[y][x] = filltype
    radius = 3
    crossradius = 2
    marshradius = 2
    markControlSpot(mask, y, x)
    if filltype == BROWNX or filltype == BLACKX:
        pygame.draw.line(png, colors[filltype], (x-crossradius, y-crossradius), (x+crossradius, y+crossradius))
        pygame.draw.line(png, colors[filltype], (x-crossradius, y+crossradius), (x+crossradius, y-crossradius))
    elif filltype == MARSH:
        pygame.draw.line(png, colors[filltype], (x-marshradius, y-marshradius), (x+marshradius, y-marshradius))
        pygame.draw.line(png, colors[filltype], (x-marshradius, y+marshradius), (x+marshradius, y+marshradius))
    elif filltype == STONE or filltype == BROWNSTONE:
        pygame.draw.circle(png, colors[filltype], (x, y), radius)
    elif filltype == GREENCIRCLE:
        pygame.draw.circle(png, colors[filltype], (x, y), radius = 2)


def rotateArea(area, png, mask):
    rotated, pngCopy, maskCopy = createArea((len(area[0]), len(area)))
    for y in range(len(area)):
        for x in range(len(area[0])):
            rotated[y][x] = area[(len(area[0])-1) - x][y]
    pngCopy = pygame.transform.rotate(png, -90)
    for key in mask["faLookup"]:
        maskCopy["faLookup"][((len(area[0])-1) - key[1], key[0])] = True
    for key in mask["saLookup"]:
        maskCopy["saLookup"][((len(area[0])-1) - key[1], key[0])] = True
    for key in mask["ssaLookup"]:
        maskCopy["ssaLookup"][((len(area[0])-1) - key[1], key[0])] = True
    for key in mask["vsaLookup"]:
        maskCopy["vsaLookup"][((len(area[0])-1) - key[1], key[0])] = True
    for key in mask["tunnelLookup"]:
        maskCopy["tunnelLookup"][((len(area[0])-1) - key[1], key[0])] = True
    for control in mask["controls"]:
        maskCopy["controls"].append(((len(area[0])-1) - control[1], control[0]))
    return rotated, pngCopy, maskCopy


def checkSpotNeighbourhood(area, y, x, kind):
    if area[y][x] in kind and area[y - 1][x] in kind and area[y + 1][x] in kind and area[y][x - 1] in kind and area[y][x + 1] in kind and area[y - 1][x - 1] in kind and area[y + 1][x - 1] in kind and area[y - 1][x + 1] in kind and area[y + 1][x + 1] in kind:
        return True
    return False


def checkForGoodToGo(area, rect, kind):
    for y in range(rect[0][1], rect[1][1]):
        for x in range(rect[0][0], rect[1][0]):
            if area[y][x] not in kind:
                return False
    return True


def unevenLoopPoints(center, avgRadius):
    ptList = []
    accelMax = 2
    speedMax = 5
    shapeZoom = avgRadius * 0.01
    flatten = randrange(7, 11) / 10.0
    angleSteps = 90 + randrange(50)
    shapeLenInitial = angleSteps
    maxInd = angleSteps//4

    while True:
        ptListDelta = []
        shapeLen = shapeLenInitial
        shapeDir = 0
        for ind in range(maxInd):
            ang = (ind * 2 * math.pi * 2) / angleSteps
            shapeDir = shapeDir + randrange(-accelMax, accelMax+1)
            if shapeDir < -speedMax:
                shapeDir = -speedMax
            elif shapeDir > speedMax:
                shapeDir = speedMax
            shapeLen = shapeLen + shapeDir
            pos = rotateVector(ang, shapeLen)
            ptListDelta.append((pos[0], pos[1]))
        if shapeDir == 0:
            break

    yShift = shapeLen - shapeLenInitial
    for ind in range(maxInd):
        pos = (ptListDelta[ind][0], ptListDelta[ind][1])
        ptList.append((-pos[0], -pos[1] -yShift))
        ptList.insert(ind, (+pos[0], +pos[1]))
    ptListRotated = []
    angRotated = (randrange(0, angleSteps//2) * math.pi * 2) / angleSteps
    for pt in ptList:
        pos = rotatePoint((0, 0), pt, angRotated)
        ptListRotated.append((center[0] + pos[0]*shapeZoom, center[1] + pos[1]*shapeZoom*flatten))
    return ptListRotated


def addSolidFenceSegment(area, png, mask, outer, fenceStyle, xMin, xMax):
    modified, pngModified, maskModified = copyAreaShallow(area, png, mask)

    y = 0
    dy = 1
    if not outer:
        y = len(area)//2
        dy = -1
    
    for x in range(xMin, xMax):
        if modified[y][x] in overlapkind:
            areaSetAt(modified, pngModified, maskModified, y+dy, x, fenceStyle)
            if fenceStyle != NARROWBLACK:
                areaSetAt(modified, pngModified, maskModified, y, x, fenceStyle)
    if outer and xMax - xMin > minMarkedLineSegment:
        for delta in range(fenceDeltaMax):
            if fenceStyle == NARROWBLACK or fenceStyle == SOLIDBLACK:
                areaSetAtVisualOnly(pngModified, maskModified, 1 + delta, (xMin + xMax)//2 + delta, fenceStyle)
            if fenceStyle == SOLIDBLACK:
                areaSetAtVisualOnly(pngModified, maskModified, 1 + delta, (xMin + xMax)//2 + delta + fenceDeltaGap, fenceStyle)

    return modified, pngModified, maskModified


def addFenceHoleSegment(area, png, mask, outer, fenceHoleFiller, xMin, xMax):
    modified, pngModified, maskModified = copyAreaShallow(area, png, mask)

    y = 0
    dy = 1
    if not outer:
        y = len(area)//2
        dy = -1

    for x in range(xMin, xMax):
        if modified[y][x] in overlapkind and fenceHoleFiller != FOREST:
            areaSetAt(modified, pngModified, maskModified, y+dy, x, fenceHoleFiller)
            if fenceHoleFiller != NARROWBLACK:
                areaSetAt(modified, pngModified, maskModified, y, x, fenceHoleFiller)
    if outer:
        for delta in range(fenceDeltaMax):
            if fenceHoleFiller == NARROWBLACK:
                areaSetAtVisualOnly(pngModified, maskModified, 1 + delta, (xMin+xMax)//2 + delta + fenceDeltaGap, fenceHoleFiller)
    markControlSpot(maskModified, y, xMin)
    if xMax - xMin > controlBend + 1:
        markControlSpot(maskModified, y, xMax - controlBend)

    return modified, pngModified, maskModified


def addSolidFence(area, png, mask, outer, fenceStyle1):
    modified, pngModified, maskModified = copyAreaShallow(area, png, mask)

    xMin = 0
    xMax = len(area[0])
    if not outer:
        xMax = len(area[0])//2

    area, png, mask = addSolidFenceSegment(modified, pngModified, maskModified, outer, fenceStyle1, xMin, xMax)
    markControlSpot(maskModified, 1 + controlBend, 1 + controlBend)
    return modified, pngModified, maskModified


def addOneHoleFence(area, png, mask, outer, fenceStyle1, fenceStyle2, fenceHole1filler, fenceHole1width):
    modified, pngModified, maskModified = copyAreaShallow(area, png, mask)

    xMax = len(area[0])
    if not outer:
        xMax = len(area[0])//2

    fenceHole1start = randrange(1, xMax - fenceHole1width - 1)
    fenceHole1stop = fenceHole1start + fenceHole1width

    modified, pngModified, maskModified = addSolidFenceSegment(modified, pngModified, maskModified, outer, fenceStyle1, 0, fenceHole1start)
    modified, pngModified, maskModified = addFenceHoleSegment(modified, pngModified, maskModified, outer, fenceHole1filler, 0, xMax)
    modified, pngModified, maskModified = addSolidFenceSegment(modified, pngModified, maskModified, outer, fenceStyle2, fenceHole1stop, xMax)
    markControlSpot(maskModified, 1 + controlBend, 1 + controlBend)

    return modified, pngModified, maskModified


def addTwoHoleFence(area, png, mask, outer, fenceStyle1, fenceStyle2, fenceStyle3, fenceHole1filler, fenceHole2filler, fenceHole1width, fenceHole2width):
    modified, pngModified, maskModified = copyAreaShallow(area, png, mask)

    xMax = len(area[0])
    if not outer:
        xMax = len(area[0])//2

    fenceHole1start = randrange(1, xMax//2 - fenceHole1width - 1)
    fenceHole1stop = fenceHole1start + fenceHole1width
    fenceHole2start = randrange(xMax//2, xMax - fenceHole2width - 1)
    fenceHole2stop = fenceHole2start + fenceHole2width

    modified, pngModified, maskModified = addSolidFenceSegment(modified, pngModified, maskModified, outer, fenceStyle1, 0, fenceHole1start)
    modified, pngModified, maskModified = addFenceHoleSegment(modified, pngModified, maskModified, outer, fenceHole1filler, fenceHole1start, fenceHole1stop)
    modified, pngModified, maskModified = addSolidFenceSegment(modified, pngModified, maskModified, outer, fenceStyle2, fenceHole1stop, fenceHole2start)
    modified, pngModified, maskModified = addFenceHoleSegment(modified, pngModified, maskModified, outer, fenceHole2filler, fenceHole2start, fenceHole2stop)
    modified, pngModified, maskModified = addSolidFenceSegment(modified, pngModified, maskModified, outer, fenceStyle3, fenceHole2stop, xMax)
    markControlSpot(maskModified, 1 + controlBend, 1 + controlBend)
    return modified, pngModified, maskModified


def addContours(kernelWidth, contourArr, keepOneOf):
    width = contourArr.get_size()[0]
    height = contourArr.get_size()[1]
    maxDim = max(width, height) + kernelWidth
    iZoom = maxDim // kernelWidth

    # constants
    softeningZoom = 2
    theMax = 256

    sumArr = pygame.Surface((kernelWidth*iZoom, kernelWidth*iZoom))
    sumArr.fill((0,0,0))
    thresholdArr = pygame.Surface((width//softeningZoom, height//softeningZoom))
    thresholdArr.fill((0,0,0))

    initArrs = []
    for ind in [1, 2, 4]:
        initialSize = kernelWidth * ind
        zoom = iZoom // ind

        arr = pygame.Surface((initialSize,initialSize))
        for x in range(arr.get_size()[0]):
            for y in range(arr.get_size()[1]):
                height = int(uniform(0, (theMax/2)/ind))
                arr.set_at((x, y), (height, height, height))

        tmpArr = pygame.transform.smoothscale_by(arr, zoom)
        sumArr.blit(tmpArr, (0,0, width, height), special_flags=pygame.BLEND_ADD)

    origThresholds = [240, 230, 220, 210, 200, 190, 180, 170, 160, 150, 140, 130, 120, 110, 100, 90, 80, 70, 60, 50, 40, 30, 20, 10]
    thresholds = []
    thresholdShift = 10
    for item in origThresholds:
        if randrange(keepOneOf) == 0:
            thresholds.append(item)

    yvals = []
    for y in range(sumArr.get_size()[1]):
        yvals.append(sumArr.get_at((0, y))[0])

    for x in range(1, thresholdArr.get_size()[0] - 1):
        val = sumArr.get_at((x, 0))[0]
        for y in range(1,thresholdArr.get_size()[1] - 1):
            newVal = sumArr.get_at((x, y))[0]
            yvals[y] = (10 * yvals[y] + newVal) / 11
            val = (10 * val + newVal) / 11
            val = (val + yvals[y]) / 2
            for threshold in thresholds:
                if val > threshold:
                    col = threshold - thresholdShift
                    thresholdArr.set_at((x, y), (col, col, col))
                    break

    contourLookup = {}
    for x in range(1, thresholdArr.get_size()[0] - 1):
        for y in range(1, thresholdArr.get_size()[1] - 1):
            mid = thresholdArr.get_at((x, y))[0]
            left = thresholdArr.get_at((x -1, y))[0]
            right = thresholdArr.get_at((x +1, y))[0]
            up = thresholdArr.get_at((x, y-1))[0]
            down = thresholdArr.get_at((x, y+ 1))[0]
            if left + right + up + down < 4 * mid:
                if contourArr.get_at((x*2, y*2)) in contouroverlapkindcol:
                    contourLookup[(x*2, y*2)] = True
    return sumArr, contourArr


def addFence(area, png, mask, outer):

    noFence = []
    solidFence = [1, 2, 3]
    oneHoleFence = [4, 5, 6]
    twoHoleFence = [6, 7]
    fenceType = randrange(0, twoHoleFence[-1] + 1)

    fenceStyle1 = partialfencekind[randrange(0, len(partialfencekind))]
    fenceStyle2 = partialfencekind[randrange(0, len(partialfencekind))]
    fenceStyle3 = partialfencekind[randrange(0, len(partialfencekind))]

    fenceHole1width = randrange(2, len(area[0])//10)
    fenceHole1filler = fencefiller[randrange(0, len(fencefiller))]
    fenceHole2width = randrange(2, len(area[0])//10)
    fenceHole2filler = fencefiller[randrange(0, len(fencefiller))]

    if fenceType in solidFence and outer:
        area, png, mask = addSolidFence(area, png, mask, outer, fenceStyle1)
    elif fenceType in oneHoleFence:
        area, png, mask = addOneHoleFence(area, png, mask, outer, fenceStyle1, fenceStyle2, fenceHole1filler, fenceHole1width)
    elif fenceType in twoHoleFence:
        area, png, mask = addTwoHoleFence(area, png, mask, outer, fenceStyle1, fenceStyle2, fenceStyle3, fenceHole1filler, fenceHole2filler, fenceHole1width, fenceHole2width)
    
    return area, png, mask


# could split
def addPathOrStream(area, png, mask, pathType):
    modified, pngModified, maskModified = copyAreaShallow(area, png, mask)

    xMin = 0
    yMin = 0
    xMax = len(area[0])
    yMax = len(area)
    pathMaxLen = randrange(xMax//16, xMax + yMax)

    blackColor = True
    blackColorCtrStart = 20
    blackColorCtr = blackColorCtrStart
    blackColorUnBlackThreshold = 5

    angleSteps = 32
    angMaxDelta = math.pi / 6
    origAng = - angMaxDelta + (angMaxDelta * randrange(angleSteps)) / angleSteps 
    ang = origAng
    shapeDir = 0
    pos = (randrange(xMax // 16, xMax - xMax//16), yMin + 1)
    shapeDirMax = 3
    pathMaxLen = randrange(xMax//16, xMax + yMax)
    if pathType == "stream":
        pos = (randrange(xMax // 16, xMax - xMax//16), yMin + 1 + randrange(yMax // 16))
        shapeDirMax = 1
        pathMaxLen = randrange(xMax//16, xMax // 2)
    elif pathType == "fence":
        origAng = 0
        ang = 0
        pos = (randrange(xMax // 16, xMax - xMax//16), yMin + 5)
        shapeDirMax = 0
        pathMaxLen = randrange(xMax//16, xMax // 2 - 5)
    markControlSpot(maskModified, pos[1], pos[0])

    while pos[0] > xMin + 1 and pos[0] < xMax - 1 and pos[1] > yMin and pos[1] < yMax:
        if pathType == "stream":
            pathStyle = WATER
        elif pathType == "fence":
            pathStyle = SOLIDBLACK
            if modified[int(pos[1])][int(pos[0])] in forbidden or modified[int(pos[1])][int(pos[0] + 1)] in forbidden:
                break
        else:
            pathStyle = PATHWHITE
            if blackColor:
                pathStyle = PATHBLACK

        areaSetAt(modified, pngModified, maskModified, pos[1], pos[0], pathStyle)
        if pathType == "stream" or pathType == "fence":
            areaSetAt(modified, pngModified, maskModified, pos[1], pos[0] + 1, pathStyle)
        else:
            if modified[int(pos[1])][int(pos[0] - 1)] != PATHBLACK:
                areaSetAt(modified, pngModified, maskModified, pos[1], pos[0] - 1, PATHWHITE)
            if modified[int(pos[1])][int(pos[0] + 1)] != PATHBLACK:
                areaSetAt(modified, pngModified, maskModified, pos[1], pos[0] + 1, PATHWHITE)

        shapeDir = shapeDir + randrange(-1, 2)
        if shapeDir < -shapeDirMax:
            shapeDir = -shapeDirMax
        elif shapeDir > shapeDirMax:
            shapeDir = shapeDirMax
        if ang > origAng - angMaxDelta and ang < origAng + angMaxDelta:
            ang = ang + shapeDir * (math.pi / 90)
        dPos = rotateVector(ang, 1.0)
        pos = (pos[0] + dPos[0], pos[1] + dPos[1])
    
        blackColorCtr = blackColorCtr - 1
        if blackColorCtr <= 0:
            blackColorCtr = blackColorCtrStart
            blackColor = True
        elif blackColorCtr <= blackColorUnBlackThreshold:
            blackColor = False

        pathMaxLen = pathMaxLen - 1
        if pathMaxLen <= 0:
            break
    markControlSpot(maskModified, pos[1], pos[0])
    return modified, pngModified, maskModified


def houseFormRotate(houseForm, houseControlList):
    rotated = []
    rotatedControls = []
    for item in houseForm:
        rotatedItem = [(1 - item[0][1], item[0][0]), (1 - item[1][1], item[1][0])]
        if rotatedItem[0][0] > rotatedItem[1][0]:
            tmp = rotatedItem[0][0]
            rotatedItem[0] = (rotatedItem[1][0], rotatedItem[0][1])
            rotatedItem[1] = (tmp, rotatedItem[1][1])
        if rotatedItem[0][1] > rotatedItem[1][1]:
            tmp = rotatedItem[0][1]
            rotatedItem[0] = (rotatedItem[0][0], rotatedItem[1][1])
            rotatedItem[1] = (rotatedItem[1][0], tmp)
        rotated.append(rotatedItem)

    for item in houseControlList:
        rotatedItem = (1 - item[1], item[0])
        rotatedControls.append(rotatedItem)

    return rotated, rotatedControls


def houseFormScaleAndShift(houseForm, houseControlList, xScale, yScale, xShift, yShift):
    scaled = []
    scaledControls = []
    for item in houseForm:
        scaledItem = [(int(item[0][0] * xScale + xShift), int(item[0][1] * yScale + yShift)), (int(item[1][0] * xScale + xShift), int(item[1][1] * yScale + yShift))]
        scaled.append(scaledItem)
    for item in houseControlList:
        scaledItem = (int(item[0] * xScale + xShift), int(item[1] * yScale + yShift))
        scaledControls.append(scaledItem)
    return scaled, scaledControls


def houseYardDraw(area, png, mask, houseControlList, myStyle, startY, endY, startX, endX):
    modified, pngModified, maskModified = copyAreaShallow(area, png, mask)
    for y in range(startY, endY):
        for x in range(startX, endX + 1):
            if modified[y][x] not in housekind and modified[y][x] not in fencekind:
                areaSetAt(modified, pngModified, maskModified, y, x, myStyle)
            if (x, y) in houseControlList and myStyle == OLIVEGREEN:
                houseControlList.remove((x, y))
    return modified, pngModified, maskModified, houseControlList


def houseBorderPainter(area, modified, pngModified, maskModified, comparetype, comparekind, bordertype):

    for y in range(len(area)//2):
        for x in range(len(area[0])//2):
            if area[y][x] == comparetype and (area[y-1][x] not in comparekind or area[y+1][x] not in comparekind or area[y][x-1] not in comparekind or area[y][x+1] not in comparekind or area[y-1][x-1] not in comparekind or area[y+1][x+1] not in comparekind or area[y-1][x+1] not in comparekind or area[y+1][x-1] not in comparekind):
                areaSetAt(modified, pngModified, maskModified, y, x, bordertype)


def addHouse(area, png, mask):  # not so cube, closer to street
    modified, pngModified, maskModified = copyAreaShallow(area, png, mask)

    houseFormInd = randrange(0, min(len(houseforms), maxHouseForms))
    houseForm = houseforms[houseFormInd][0]
    houseControlList = houseforms[houseFormInd][1]
    for rot in range(randrange(0, houseRotOrientations)):
        houseForm, houseControlList = houseFormRotate(houseForm, houseControlList)

    xScale = randrange(len(area[0])//4, len(area[0])//2 - 1 - 2)
    yScale = randrange(len(area)//8, len(area)//4 - 1)
    xShift = randrange(2, len(area[0])//2 - xScale)
    yShift = randrange(2, len(area)//3 - yScale)
    houseForm, houseControlList = houseFormScaleAndShift(houseForm, houseControlList, xScale, yScale, xShift, yShift)
 
    # check the area for house is clean
    for rect in houseForm:
        if not checkForGoodToGo(modified, rect, overlapkind):
            return modified, pngModified, maskModified

    smallestX = len(area[1])//2
    biggestX = 0
    smallestY = len(area[1])//2
    biggestY = 0

    # could use getBoundingBox(), but what the heck
    for rect in houseForm:
        for y in range(rect[0][1], rect[1][1] + 1):
            for x in range(rect[0][0], rect[1][0] + 1):
                if x < smallestX:
                    smallestX = x
                if y < smallestY:
                    smallestY = y
                if x > biggestX:
                    biggestX = x
                if y > biggestY:
                    biggestY = y

    smallestYardY = 0
    halfWay = len(area[1])//2
    biggestYardY = halfWay if biggestY >= halfWay else randrange(biggestY, halfWay)
    midYardY =  (smallestY + biggestY)//2

    frontYardStyle = frontyardkind[randrange(0, len(frontyardkind))]
    backYardStyle = backyardkind[randrange(0, len(backyardkind))]

    if midYardY > smallestYardY:
        if checkForGoodToGo(modified, [(smallestX, smallestYardY + 2),(biggestX + 1, midYardY)], overlapkind):
            markControlSpot(maskModified, smallestYardY - controlBend, smallestX - controlBend)
            markControlSpot(maskModified, smallestYardY - controlBend, biggestX + controlBend)
            modified, pngModified, maskModified, houseControlList = houseYardDraw(area, png, mask, houseControlList, frontYardStyle, smallestYardY, midYardY, smallestX, biggestX + 1)

    if midYardY < biggestYardY:
        if checkForGoodToGo(modified, [(smallestX, midYardY),(biggestX + 1, biggestYardY - 2)], overlapkind):
            markControlSpot(maskModified, biggestYardY + controlBend, smallestX - controlBend)
            markControlSpot(maskModified, biggestYardY + controlBend, biggestX + controlBend)
            modified, pngModified, maskModified, houseControlList = houseYardDraw(area, png, mask, houseControlList, backYardStyle, midYardY, biggestYardY, smallestX, biggestX + 1)

    for rect in houseForm:
        houseInternalStyle = SHELTERINTERNAL if randrange(0, shelterOutOfHouse) == 0 and abs(rect[0][1]-rect[1][1]) * abs(rect[0][0]-rect[1][0]) < 100 else HOUSEINTERNAL
        for y in range(rect[0][1], rect[1][1]):
            for x in range(rect[0][0], rect[1][0]):
                areaSetAt(modified, pngModified, maskModified, y, x, houseInternalStyle)

    modifiedCopy, pngModifiedCopy, maskModifiedCopy = copyArea(modified, pngModified, maskModified)
    houseBorderPainter(modified, modifiedCopy, pngModifiedCopy, maskModifiedCopy, HOUSEINTERNAL, housekind, SOLIDBLACK)
    houseBorderPainter(modified, modifiedCopy, pngModifiedCopy, maskModifiedCopy, SHELTERINTERNAL, shelterkind, NARROWBLACK)

    for item in houseControlList:
       if not (modifiedCopy[item[0]][item[1]] in forbidden and modifiedCopy[item[0] - 1][item[1]] in forbidden and modifiedCopy[item[0] +1][item[1]] in forbidden and modifiedCopy[item[0]][item[1] - 1] in forbidden and modifiedCopy[item[0]][item[1] + 1] in forbidden):
           markControlSpot(maskModifiedCopy, item[1], item[0])

    return modifiedCopy, pngModifiedCopy, maskModifiedCopy


def addFences(area, png, mask, bigBlock):
    for ind in range(4):
        area, png, mask = addFence(area, png, mask, True)
        if randrange(0, verticalFenceOneOutOf) == 0:
            area, png, mask = addPathOrStream(area, png, mask, "fence")
        if not bigBlock and randrange(0,3) != 0:
            area, png, mask = addFence(area, png, mask, False)
        area, png, mask = rotateArea(area, png, mask)
    return area, png, mask


def addHouses(area, png, mask):
    for ind in range(4):
        area, png, mask = addHouse(area, png, mask)
        area, png, mask = rotateArea(area, png, mask)
    if randrange(0, rotateOneOutOf) == 0:
        area, png, mask = rotateArea(area, png, mask)
    return area, png, mask


def addCottage(area, png, mask, isHut):
    modified, pngModified, maskModified = copyAreaShallow(area, png, mask)

    xScale = randrange(len(area[0])//32, len(area[0])//16)
    yScale = randrange(len(area)//32, len(area)//16)
    xShift = randrange(4, len(area[0]) - 4 - xScale)
    yShift = randrange(4, len(area) - 4 - yScale)

    if isHut:
        cottageStyle = SHELTERINTERNAL
        cottageFenceStyle = NARROWBLACK
    else:
        cottageStyle = HOUSEINTERNAL
        cottageFenceStyle = SOLIDBLACK

    if not checkForGoodToGo(modified, [(xShift - 1, yShift - 1), (xShift + xScale + 1, yShift + yScale + 1)], overlapkind):
        return area, png, mask

    for y in range(yShift + 1, yShift + yScale):
        for x in range(xShift + 1, xShift + xScale):
            areaSetAt(modified, pngModified, maskModified, y, x, cottageStyle)

    markControlSpot(maskModified, yShift - controlBend, xShift - controlBend)
    markControlSpot(maskModified, yShift + yScale + controlBend, xShift - controlBend)
    markControlSpot(maskModified, yShift - controlBend, xShift + xScale + controlBend)
    markControlSpot(maskModified, yShift + yScale + controlBend, xShift + xScale + controlBend)

    for x in range(xShift, xShift + xScale + 1):
         areaSetAt(modified, pngModified, maskModified, yShift, x, cottageFenceStyle)
         areaSetAt(modified, pngModified, maskModified, yShift + yScale, x, cottageFenceStyle)
    for y in range(yShift, yShift + yScale + 1):
         areaSetAt(modified, pngModified, maskModified, y, xShift, cottageFenceStyle)
         areaSetAt(modified, pngModified, maskModified, y, xShift + xScale, cottageFenceStyle)

    return area, png, mask


def addSpecialtyVerticalHole(area, png, mask, xStart, xEnd, xShift, yShift, specialAreaStyle, specialAreaPortStyle):
    modified, pngModified, maskModified = copyAreaShallow(area, png, mask)

    for x in range(xStart, xEnd):
        if specialAreaPortStyle == FOREST:
            areaSetAt(modified, pngModified, maskModified, yShift - 1, xShift + x, specialAreaStyle)
            areaSetAt(modified, pngModified, maskModified, yShift, xShift + x, specialAreaStyle)
        elif specialAreaPortStyle == NARROWBLACK:
            areaSetAt(modified, pngModified, maskModified, yShift - 1, xShift + x, specialAreaStyle)
            areaSetAt(modified, pngModified, maskModified, yShift, xShift + x, specialAreaPortStyle)
        else:
            areaSetAt(modified, pngModified, maskModified, yShift - 1, xShift + x, specialAreaPortStyle)
            areaSetAt(modified, pngModified, maskModified, yShift, xShift + x, specialAreaPortStyle)

    return modified, pngModified, maskModified


def addSpecialtyHorizontalHole(area, png, mask, yStart, yEnd, xShift, yShift, specialAreaStyle, specialAreaPortStyle):
    modified, pngModified, maskModified = copyAreaShallow(area, png, mask)

    for y in range(yStart, yEnd):
        if specialAreaPortStyle == FOREST:
            areaSetAt(modified, pngModified, maskModified, yShift + y, xShift, specialAreaStyle)
            areaSetAt(modified, pngModified, maskModified, yShift + y, xShift + 1, specialAreaStyle)
        elif specialAreaPortStyle == NARROWBLACK:
            areaSetAt(modified, pngModified, maskModified, yShift + y, xShift, specialAreaPortStyle)
            areaSetAt(modified, pngModified, maskModified, yShift + y, xShift + 1, specialAreaStyle)
        else:
            areaSetAt(modified, pngModified, maskModified, yShift + y, xShift, specialAreaPortStyle)
            areaSetAt(modified, pngModified, maskModified, yShift + y, xShift + 1, specialAreaPortStyle)

    return modified, pngModified, maskModified


def addSpecialty(area, png, mask):
    modified, pngModified, maskModified = copyAreaShallow(area, png, mask)

    xScale = randrange(len(area[0])//6, len(area[0])//3 - 2)
    yScale = randrange(len(area)//6, len(area)//3 - 2)
    xShift = randrange(4, len(area[0]) - 4 - xScale)
    yShift = randrange(4, len(area) - 4 - yScale)
    
    if yScale//4 == yScale//3:
        yHoleLeft = 0
        yHoleRight = 0
    else:
        yHoleLeft = randrange(0, 2)
        yHoleRight = randrange(0, 2)
        yHoleLeftWid = randrange(yScale//4, yScale//3)
        yHoleRightWid = randrange(yScale//4, yScale//3)
    if xScale//4 == xScale//3:
        xHoleUp = 0
        xHoleDown = 0
    else:
        xHoleUp = randrange(0, 2)
        xHoleDown = randrange(0, 2)
        xHoleUpWid = randrange(xScale//4, xScale//3)
        xHoleDownWid = randrange(xScale//4, xScale//3)

    fenceStyle = fencekind[randrange(0, len(fencekind))]
    specialAreaStyle = specialareakind[randrange(0, len(specialareakind))]
    specialAreaPortStyle = specialareaportkind[randrange(0, len(specialareaportkind))]

    if fenceStyle in forbidden and yHoleLeft == 0 and yHoleRight == 0 and xHoleUp == 0 and xHoleDown == 0:
        specialAreaStyle = OLIVEGREEN        

    if not checkForGoodToGo(modified, [(xShift - 1, yShift - 1),(xShift + xScale + 1, yShift + yScale + 1)], overlapkind):
        return area, png, mask

    for y in range(yShift + 1, yShift + yScale):
        for x in range(xShift + 1, xShift + xScale):
            areaSetAt(modified, pngModified, maskModified, y, x, specialAreaStyle)

    markControlSpot(maskModified, yShift - controlBend, xShift - controlBend)
    markControlSpot(maskModified, yShift + controlBend, xShift + controlBend)
    markControlSpot(maskModified, yShift + yScale - controlBend, xShift + controlBend)
    markControlSpot(maskModified, yShift + yScale + controlBend, xShift - controlBend)
    markControlSpot(maskModified, yShift - controlBend, xShift + xScale + controlBend)
    markControlSpot(maskModified, yShift + controlBend, xShift + xScale - controlBend)
    markControlSpot(maskModified, yShift + yScale - controlBend, xShift + xScale - controlBend)
    markControlSpot(maskModified, yShift + yScale + controlBend, xShift + xScale + controlBend)

    for x in range(xShift, xShift + xScale + 1):
         areaSetAt(modified, pngModified, maskModified, yShift, x, fenceStyle)
         areaSetAt(modified, pngModified, maskModified, yShift + yScale, x, fenceStyle)
         if fenceStyle != NARROWBLACK:
             areaSetAt(modified, pngModified, maskModified, yShift - 1, x, fenceStyle)
             areaSetAt(modified, pngModified, maskModified, yShift + yScale - 1, x, fenceStyle)
    for y in range(yShift, yShift + yScale + 1):
         areaSetAt(modified, pngModified, maskModified, y, xShift, fenceStyle)
         areaSetAt(modified, pngModified, maskModified, y, xShift + xScale, fenceStyle)
         if fenceStyle != NARROWBLACK:
             areaSetAt(modified, pngModified, maskModified, y, xShift + 1, fenceStyle)
             areaSetAt(modified, pngModified, maskModified, y, xShift + xScale - 1, fenceStyle)

    if xHoleUp:
        markControlSpot(maskModified, yShift, xHoleUpWid)
        markControlSpot(maskModified, yShift, xScale - xHoleUpWid)
        modified, pngModified, maskModified = addSpecialtyVerticalHole(modified, pngModified, maskModified, xHoleUpWid, xScale - xHoleUpWid, xShift, yShift, specialAreaStyle, specialAreaPortStyle)

    if xHoleDown:
        markControlSpot(maskModified, yShift + yScale, xHoleDownWid)
        markControlSpot(maskModified, yShift + yScale, xScale - xHoleDownWid)
        modified, pngModified, maskModified = addSpecialtyVerticalHole(modified, pngModified, maskModified, xHoleDownWid, xScale - xHoleDownWid, xShift, yShift, specialAreaStyle, specialAreaPortStyle)

    if yHoleLeft:
        markControlSpot(maskModified, yHoleLeftWid, xShift)
        markControlSpot(maskModified, yScale - yHoleLeftWid, xShift)
        modified, pngModified, maskModified = addSpecialtyHorizontalHole(modified, pngModified, maskModified, yHoleLeftWid, yScale - yHoleLeftWid, xShift, yShift, specialAreaStyle, specialAreaPortStyle)
    if yHoleRight:
        markControlSpot(maskModified, yHoleLeftWid, xShift + xScale)
        markControlSpot(maskModified, yScale - yHoleLeftWid, xShift + xScale)
        modified, pngModified, maskModified = addSpecialtyHorizontalHole(modified, pngModified, maskModified, yHoleRightWid, yScale - yHoleRightWid, xShift, yShift, specialAreaStyle, specialAreaPortStyle)

    return modified, pngModified, maskModified


def addCottages(area, png, mask):
    if randrange(0, rotateOneOutOf) == 0:
        for ind in range(randrange(0, maxNumCottages)):
            isHutCottage = False
            if randrange(0, hutOutOfCottages) == 0:
                isHutCottage = True
            area, png, mask = addCottage(area, png, mask, isHutCottage)
    return area, png, mask


def addHuts(area, png, mask):
    if randrange(0, rotateOneOutOf) == 0:
        area, png, mask = addCottage(area, png, mask, True)
    return area, png, mask


def addSpecialties(area, png, mask):
    area, png, mask = addSpecialty(area, png, mask)
    area, png, mask = rotateArea(area, png, mask)
    return area, png, mask


def addSpot(area, png, mask):
    modified, pngModified, maskModified = copyAreaShallow(area, png, mask)

    x = randrange(1, len(area[0]) - 1)
    y = randrange(1, len(area) - 1)

    if not checkSpotNeighbourhood(area, y, x, overlapkind):
        return modified, pngModified, maskModified
        
    if checkSpotNeighbourhood(area, y, x, spotmodifying):
        prevind = spotmodifying.index(area[y][x])
        newval = newspotvalues[prevind]
        if newval == STONE:
            lottery = randrange(0, 5)
            if lottery == 0:
                newval = BROWNX
            if lottery == 1:
                newval = BROWNSTONE
            elif lottery == 2:
                newval = MARSH
        areaDrawSpot(modified, pngModified, maskModified, y, x, newval)
    return modified, pngModified, maskModified

def addSpots(area, png, mask, isForest):
    minNumSpots = (len(area)*len(area[0]))//(4*400*spotnessFactor)
    maxNumSpots = 4 * minNumSpots
    for ind in range(randrange((1+isForest)*minNumSpots,(1+isForest)*maxNumSpots)):
        area, png, mask = addSpot(area, png, mask)
    return area, png, mask


def interleaveArea(area, miniarea, png, mask, miniPng, miniMask):
    modified, pngModified, maskModified = copyAreaShallow(area, png, mask)
    for y in range(len(miniarea)):
        for x in range(len(miniarea[0])):
            areaSetAt(modified, pngModified, maskModified, y, x, miniarea[y][x])
    return modified, pngModified, maskModified


def addWeirdArea(area, png, mask, radius, areaType):
    modified, pngModified, maskModified = copyArea(area, png, mask)

    width = len(area[0])
    height = len(area)
    margin = radius * 2
    center = (randrange(margin, 3*margin), randrange(margin, 3*margin))
    points = unevenLoopPoints(center, radius)
    bbox = getBoundingBox([points[0], points[0]], points)
    if bbox[0][0] > 2 and bbox[0][1] > 2 and bbox[1][0] < width-2 and bbox[1][1] < width-2:
        polygonLookup = polygonCreate(bbox, points)
        for y in range(height):
            for x in range(width):
                if polygonContainsWithLookup(polygonLookup, (x, y)):
                    if areaType == DEEPFOREST:
                        if area[x][y] not in forbidden:
                            areaSetAt(modified, pngModified, maskModified, y, x, DEEPFOREST)
                    elif areaType == SOLIDGREEN:
                        if area[x][y] not in forbidden:
                            areaSetAt(modified, pngModified, maskModified, y, x, SOLIDGREEN)
                    elif areaType == WATER:
                        if not polygonContainsWithLookup(polygonLookup, (x-1, y)) or not polygonContainsWithLookup(polygonLookup, (x+1, y)) or not polygonContainsWithLookup(polygonLookup, (x, y - 1)) or not polygonContainsWithLookup(polygonLookup, (x, y + 1)):
                            areaSetAt(modified, pngModified, maskModified, y, x, SOLIDBLACK)
                        else:
                            areaSetAt(modified, pngModified, maskModified, y, x, WATER)
                    elif areaType == BROWNX:
                        if not polygonContainsWithLookup(polygonLookup, (x-1, y)) or not polygonContainsWithLookup(polygonLookup, (x+1, y)) or not polygonContainsWithLookup(polygonLookup, (x, y - 1)) or not polygonContainsWithLookup(polygonLookup, (x, y + 1)):
                            areaSetAt(modified, pngModified, maskModified, y, x, BROWNX)

        leftMost = points[0]
        rightMost = points[0]
        upMost = points[0]
        downMost = points[0]
        for point in points:
            if point[0] < leftMost[0]:
                leftMost = point
            if point[0] > rightMost[0]:
                rightMost = point
            if point[1] < upMost[1]:
                upMost = point
            if point[1] < downMost[1]:
                downMost = point
        if modified[int(leftMost[1])][int(leftMost[0] - controlBend)] in overlapkind:
            markControlSpot(maskModified, leftMost[1], leftMost[0] - controlBend)
        if modified[int(rightMost[1])][int(leftMost[0] + controlBend)] in overlapkind:
            markControlSpot(maskModified, rightMost[1], rightMost[0] + controlBend)
        if modified[int(upMost[1] - controlBend)][int(upMost[0])] in overlapkind:
            markControlSpot(maskModified, upMost[1] - controlBend, upMost[0])
        if modified[int(downMost[1] + controlBend)][int(downMost[0])] in overlapkind:
            markControlSpot(maskModified, downMost[1] + controlBend, downMost[0])

        if areaType == BROWNX and randrange(0, 2) == 0:
            for dx in range (2, holeDeltaMax + 2):
                areaSetAt(modified, pngModified, maskModified, upMost[1] + dx, upMost[0], BROWNX)
        
    return modified, pngModified, maskModified


def addLake(area, png, mask):
    if randrange(0, lakeInForestOneOutOf) == 0:
        lakeRadius = len(area[0])//8
        area, png, mask = addWeirdArea(area, png, mask, lakeRadius, WATER)
    return area, png, mask


def addHole(area, png, mask):
    if randrange(0, holeInForestOneOutOfInverse) != 0:
        holeRadius = len(area[0])//16
        area, png, mask = addWeirdArea(area, png, mask, holeRadius, BROWNX)
    return area, png, mask


def addDifficultForest(area, png, mask):
    for ind in range(randrange(0, difficultForestHowMany)):
        difficultRadius = len(area[0])//12
        area, png, mask = addWeirdArea(area, png, mask, difficultRadius, DEEPFOREST)
    return area, png, mask


def addBush(area, png, mask):
    for ind in range(randrange(0, bushHowMany)):
        bushRadius = len(area[0])//16
        area, png, mask = addWeirdArea(area, png, mask, bushRadius, SOLIDGREEN)
    return area, png, mask


def addPathsAndStreams(area, png, mask):
    for ind in range(4):
        if randrange(0, pathInForestOneOutOf) == 0:
            area, png, mask = addPathOrStream(area, png, mask, "path")
        if randrange(0, streamInForestOneOutOf) == 0:
            area, png, mask = addPathOrStream(area, png, mask, "stream")
        area, png, mask = rotateArea(area, png, mask)
    return area, png, mask


def addStreams(area, png, mask):
    for ind in range(4):
        area, png, mask = rotateArea(area, png, mask)
    return area, png, mask


def addOpen(area, png, mask):
    modified, pngModified, maskModified = copyAreaShallow(area, png, mask)
    yardStyle = yardkind[randrange(0, len(yardkind))]
    for y in range(len(area)):
        for x in range(len(area[0])):
            if area[y][x] in overlapkind:
                areaSetAt(modified, pngModified, maskModified, y, x, yardStyle)
    if yardStyle == OPENAREA:
        modified, pngModified, maskModified = addBush(modified, pngModified, maskModified)
    return modified, pngModified, maskModified


def addOpens(area, png, mask): # must be more natural
    # could add better distribution, too
    area, png, mask = addOpen(area, png, mask)
    return area, png, mask


def recolorForbiddenPlaces(area, png, mask, region):
    modified, pngModified, maskModified = copyAreaShallow(area, png, mask)

    hole = False
    if region == "big":
        minY = 0
        minX = 0
        maxY = len(area)
        maxX = len(area[0])
    elif region == "topLeft":
        minY = 0
        minX = 0
        maxY = len(area)//2
        maxX = len(area[0])//2
    elif region == "topRight":
        minY = 0
        minX = len(area[0])//2
        maxY = len(area)//2
        maxX = len(area[0])
    elif region == "bottomLeft":
        minY = len(area)//2
        minX = 0
        maxY = len(area)
        maxX = len(area[0])//2
    elif region == "bottomRight":
        minY = len(area)//2
        minX = len(area[0])//2
        maxY = len(area)
        maxX = len(area[0])

    for x in range(minX + 2, maxX - 2):
        if modified[minY][x] not in forbidden and modified[minY+1][x] not in forbidden:
            hole = True
        if modified[maxY-1][x] not in forbidden and modified[maxY-2][x] not in forbidden:
            hole = True
    for y in range(minY + 2, maxY - 2):
        if modified[y][minX] not in forbidden and modified[y][minX+1] not in forbidden:
            hole = True
        if modified[y][maxX-1] not in forbidden and modified[y][maxX-2] not in forbidden:
            hole = True

    if not hole:
        for y in range(minY, maxY):
            for x in range(minX, maxX):
                if modified[y][x] in reolivekind:
                    areaSetAt(modified, pngModified, maskModified, y, x, OLIVEGREEN)

    return modified, pngModified, maskModified


def filterProblematicControls(area, png, mask):
    modified, pngModified, maskModified = copyAreaShallow(area, png, mask)
    minY = 1
    minX = 1
    maxY = len(area) - 1
    maxX = len(area[0]) - 1

    for y in range(minY, maxY):
        for x in range(minX, maxX):
            if queryControlSpot(maskModified, y, x):
                if area[y - 1][x] in forbidden and area[y + 1][x] in forbidden and  area[y + 1][x] in forbidden and area[y + 1][x] in forbidden:
                    removeControlSpot(maskModified, y, x)
                ct = area[y][x + 1]
                if y > minY + 1 and y < maxY - 1 and x > minX + 1 and x < maxX - 1 and area[y - 1][x] == ct and area[y - 2][x] == ct and area[y + 1][x] == ct and area[y + 2][x] == ct and area[y - 1][x - 1] == ct and area[y - 2][x - 1] == ct and area[y + 1][x - 1] == ct and area[y + 2][x - 1] == ct and area[y - 1][x - 2] == ct and area[y - 2][x - 2] == ct and area[y + 1][x - 2] == ct and area[y + 2][x - 2] == ct and area[y - 1][x + 1] == ct and area[y - 2][x + 1] == ct and area[y + 1][x + 1] == ct and area[y + 2][x + 1] == ct and area[y - 1][x + 2] == ct and area[y - 2][x + 2] == ct and area[y + 1][x + 2] == ct and area[y + 2][x + 2] == ct and area[y][x - 2] == ct and area[y][x - 1] == ct and area[y][x + 2] == ct:
                    removeControlSpot(maskModified, y, x)
    return modified, pngModified, maskModified


async def addBlock(dim, bigBlock):
    area, png, mask = createArea(dim)
    if randrange(0, forestBlockOneOutOf) != 0:
        area, png, mask = addOpens(area, png, mask)
        if await uiFlushEvents():
            return None, None, None
        area, png, mask = addHouses(area, png, mask)
        if await uiFlushEvents():
            return None, None, None
        if dim[0] > 100 and randrange(0, miniBlockOneOutOf) == 0:
            miniarea, minipng, minimask = await addBlock((dim[0]//2, dim[1]//2), False)
            area, png, mask = interleaveArea(area, miniarea, png, mask, minipng, minimask)
        if await uiFlushEvents():
            return None, None, None
        area, png, mask = addFences(area, png, mask, bigBlock)
        if await uiFlushEvents():
            return None, None, None
        area, png, mask = addSpecialties(area, png, mask)
        if await uiFlushEvents():
            return None, None, None
        area, png, mask = addHuts(area, png, mask)
        if await uiFlushEvents():
            return None, None, None
        area, png, mask = recolorForbiddenPlaces(area, png, mask, "big")
        if await uiFlushEvents():
            return None, None, None
        area, png, mask = recolorForbiddenPlaces(area, png, mask, "topLeft")
        if await uiFlushEvents():
            return None, None, None
        area, png, mask = recolorForbiddenPlaces(area, png, mask, "topRight")
        if await uiFlushEvents():
            return None, None, None
        area, png, mask = recolorForbiddenPlaces(area, png, mask, "bottomLeft")
        if await uiFlushEvents():
            return None, None, None
        area, png, mask = recolorForbiddenPlaces(area, png, mask, "bottomRight")
        if await uiFlushEvents():
            return None, None, None
        area, png, mask = filterProblematicControls(area, png, mask)
        if dim[0] > 100:
            area, png, mask = addSpots(area, png, mask, False)
    else:
        area, png, mask = makeForest(area, png, mask)
        area, png, mask = addDifficultForest(area, png, mask)
        if await uiFlushEvents():
            return None, None, None
        area, png, mask = addHole(area, png, mask)
        if await uiFlushEvents():
            return None, None, None
        area, png, mask = addPathsAndStreams(area, png, mask)
        if await uiFlushEvents():
            return None, None, None
        area, png, mask = addLake(area, png, mask)
        if await uiFlushEvents():
            return None, None, None
        area, png, mask = addSpecialties(area, png, mask)
        if await uiFlushEvents():
            return None, None, None
        area, png, mask = addCottages(area, png, mask)
        if await uiFlushEvents():
            return None, None, None
        area, png, mask = filterProblematicControls(area, png, mask)
        if await uiFlushEvents():
            return None, None, None
        if dim[0] > 100:
            area, png, mask = addSpots(area, png, mask, True)
    return area, png, mask


def initOuluCreator(blockSize, gridSize, boundary):
    walkwayWidth = 5
    crossingProb = 4
    pedestrianStreetProb = 4
#    pedestrianFenceProb = 2
    minCrosses = 2
    maxCrosses = 4
    circleProb = 2
    forbiddenCircleProb = 3
    shortdist = boundary/5
    x = gridSize[0] * (blockSize[0] + boundary) + boundary
    y = gridSize[1] * (blockSize[1] + boundary) + boundary
    png = pygame.Surface((y, x))
    png.fill(colors[ASPHALT])
    mask = { "faLookup": {}, "saLookup": {}, "ssaLookup": {}, "tunnelLookup": {}, "vsaLookup": {}, "controls": [], "size": (y, x)}

    # city blocks
    for dx in range(gridSize[1]):
        for dy in range(gridSize[0]):
            xShift = boundary + dx * (blockSize[0] + boundary) - walkwayWidth
            yShift = boundary + dy * (blockSize[1] + boundary) - walkwayWidth
            xScale = blockSize[1] + 2 * walkwayWidth
            yScale = blockSize[0] + 2 * walkwayWidth
            pygame.draw.rect(png, colors[SOLIDBLACK], [(xShift, yShift), ((xScale, yScale))], width=1)

    # beautify the crossings
    for dx in range(1, gridSize[1]):
        for dy in range(1, gridSize[0]):
            xShift = boundary/2 + dx * (blockSize[0] + boundary)
            yShift = boundary/2 + dy * (blockSize[1] + boundary)
            if randrange(crossingProb) == 0:
                if randrange(circleProb) == 0:
                    whatInCircle = randrange(forbiddenCircleProb)
                    if whatInCircle == 0:
                        pygame.draw.circle(png, colors[OLIVEGREEN], (xShift, yShift), shortdist, width=0)
                        for xx in range(int(xShift - shortdist), int(xShift + shortdist)):
                            for yy in range(int(yShift - shortdist), int(yShift + shortdist)):
                                pt = (xx, yy)
                                if png.get_at(pt) == colors[OLIVEGREEN]:
                                    mask["faLookup"][pt] = True
                    elif whatInCircle == 1:
                        pygame.draw.circle(png, colors[OPENAREA], (xShift, yShift), shortdist, width=0)
                    pygame.draw.circle(png, colors[SOLIDBLACK], (xShift, yShift), shortdist, width=1)
                pygame.draw.lines(png, colors[SOLIDBLACK], True, [(xShift-shortdist/3, yShift - shortdist*2),(xShift+shortdist/3, yShift - shortdist*2),(xShift, yShift - shortdist*4)], width=1)
                pygame.draw.lines(png, colors[SOLIDBLACK], True, [(xShift-shortdist/3, yShift + shortdist*2),(xShift+shortdist/3, yShift + shortdist*2),(xShift, yShift + shortdist*4)], width=1)
            pygame.draw.lines(png, colors[SOLIDBLACK], True, [(xShift - shortdist*2, yShift-shortdist/3),(xShift - shortdist*2, yShift+shortdist/3),(xShift - shortdist*4, yShift)], width=1)
            pygame.draw.lines(png, colors[SOLIDBLACK], True, [(xShift + shortdist*2, yShift-shortdist/3),(xShift + shortdist*2, yShift+shortdist/3),(xShift + shortdist*4, yShift)], width=1)

    # add some pedestrian streets
    for dx in range(1, gridSize[1]):
        for dy in range(1, gridSize[0]):
            xShift = boundary/2 + dx * (blockSize[0] + boundary)
            yShift = boundary/2 + dy * (blockSize[1] + boundary)
            if randrange(pedestrianStreetProb) == 0:
                x1 = xShift-boundary/2+walkwayWidth/2
                y1 = yShift+boundary/2 - walkwayWidth
                w1 = boundary - walkwayWidth
                h1 = blockSize[0] + walkwayWidth * 2 - 1
                pygame.draw.rect(png, colors[ASPHALT], [x1, y1 - shortdist/2, w1, h1 + shortdist], width = 0)
                pygame.draw.line(png, colors[SOLIDBLACK], (x1, y1), (x1+w1, y1))
                pygame.draw.line(png, colors[SOLIDBLACK], (x1, y1+h1), (x1+w1, y1+h1))
                numCrosses = randrange(minCrosses, maxCrosses)
                for ind in range(numCrosses):
                    areaDrawSpot(None, png, mask, y1 + h1/(numCrosses*2) + ind * h1/numCrosses, xShift, BLACKX)
                fenceInd = randrange(numCrosses)
                x2 = x1 - walkwayWidth
                y2 = y1 + h1/(numCrosses*3) + fenceInd * h1/numCrosses
                w2 = w1 + 3*walkwayWidth

                pygame.draw.line(png, colors[WATER], (x2, y2 - 1), (x2-2, y2 + 1), width=4)
                pygame.draw.line(png, colors[WATER], (x2+w2+2, y2 - 1), (x2+w2+2, y2 + 1), width=4)

    # do not allow escape
    for xx in range(2, y-2):
        mask["faLookup"][(xx, x-2)] = True
        mask["faLookup"][(xx, x-1)] = True
    for yy in range(2, x-2):
        mask["faLookup"][(y-2, yy)] = True
        mask["faLookup"][(y-1, yy)] = True

    # sealine
    pygame.draw.rect(png, colors[WATER], [y-boundary//2, 0, boundary//2, x], width = 0)
    pygame.draw.line(png, colors[SOLIDBLACK], (y-boundary//2, 0), (y-boundary//2, x), width=1)

    for xx in range(y-boundary//2, y):
        for yy in range(0, x):
            pt = (xx, yy)
            mask["faLookup"][pt] = True
    
    return png, mask


async def getInfiniteOulu(blockSize, gridSize, boundary):
    terranizer(terrains[randrange(len(terrains))])
    perfAddStart("oCreator")    
    oulu, ouluMask = initOuluCreator(blockSize, gridSize, boundary)
    perfAddStop("oCreator")    
    for x in range(gridSize[0]):
        for y in range(gridSize[1]):
            if await uiFlushEvents():
                return None, None
            perfAddStart("oBlock")
            yard, png, mask = await addBlock(blockSize, True)
            perfAddStop("oBlock")    
            await asyncio.sleep(0)
            if yard == None:
                return None, None
            perfAddStart("oInstal")    
            oulu, ouluMask = installOuluBlock(oulu, png, ouluMask, mask, (x, y), blockSize, boundary)
            perfAddStop("oInstal")    
            await asyncio.sleep(0)

    return oulu, ouluMask
