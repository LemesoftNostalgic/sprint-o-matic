import pygame
import asyncio
import os
import json
from math import cos, radians
from random import randrange, random, uniform
import time

from .utils import getSlowAreaMask, getSemiSlowAreaMask, getVerySlowAreaMask, getForbiddenAreaMask, getControlMask, getNoMask, getPackagePath
from .mathUtils import calculatePathDistance
from .gameUIUtils import uiFlushEvents, uiDrawLine

offlineMapDataFolder = os.path.join("data", "offline-map-data", "")
spotnessFactor = 4
countoursMinOutOf = 1
countoursMaxOutOf = 4
countoursMinKernelWidth = 4
countoursMaxKernelWidth = 7

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
TMPASPHALT = '§'
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
    TMPASPHALT:         (251, 211, 176),
    BROWNX:          (224, 113, 30),
    BLACKX:          (40,45,50),
    STONE:           (40,45,50),
    BROWNSTONE:      (224, 113, 30),
    MARSH:           (55, 206, 245),
    GREENCIRCLE:     (35,180,90)
    }


overlapkind = [colors[FOREST], colors[OPENAREA], colors[ASPHALT]]
spotmodifying = [colors[FOREST], colors[DEEPFOREST],  colors[OPENAREA],    colors[ASPHALT]]
newspotvalues = [STONE,  STONE,       GREENCIRCLE, BLACKX]


spotArray = [
    ["amenity", ["fountain","clinic","recycling","bench","place_of_worship","bicycle_parking","waste_disposal","toilets"]],
    ["barrier", ["bollard"]],
    ["historic", ["ruins"]]
    ]

stoneArray = [
    ["natural", ["shingle","bare_rock","rock"]]
    ]

treeArray = [
    ["natural", ["tree"]]
    ]


solidFence = [
    ["barrier", ["retaining_wall","wall","wire_fence","guard_rail","gate","fence"]]
    ]

solidGreenFence = [
    [ "barrier", ["hedge", "planter"]]
    ]

solidGreenArea = [
    ["landuse", ["flowerbed"]],
    ["natural", ["shrubbery","tree_row","scrub"]]
    ]

thinFence = [
    ["barrier", ["chain","kerb"]],
    ["power", ["line","cable","minor_line"]]
    ]

houseArray = [
    [ "building", ["storage_tank","sports_centre","commercial","kindergarten","semidetached_house","generator","toilets","cabin","garages","hotel","kiosk","hangar","industrial","power","minor","carport","detached","fire_station","stable","supermarket","chapel","grandstand","transportation","garage","ship","yes","school","civic","dormitory","retail","silo","service","construction","office","tower","residential","sports_hall","bank","no","church","warehouse","observatory","public","apartments","train_station","hospital","bungalow","government","house","manufacture","parking"] ]
    ]

shelterArray = [
    ["building", ["hut","ruins","garbage_shed","terrace","grandstand","shelter","shed", "canopy", "greenhouse", "barn", "cowshed", "roof","farm_auxiliary"]],
    ["highway", ["corridor","bridleway", "steps"]]
]

wideWayWidthMeters = 20
wideWay = [
    ["highway", ["trunk","primary","trunk_link","road","raceway"]]
    ]

midWayWidthMeters = 10
midWay = [
    ["highway", ["living_street","residential","secondary","tertiary_link","tertiary","secondary_link"]]
    ]

unclassifiedWayWidthMeters = 10
unclassifiedWay = [
    ["highway", ["unclassified","service","proposed","platform","construction","rest_area"]]
    ]
    

smallWayWidthMeters = 5
smallWay = [
    ["highway", ["pedestrian","cycleway","footway","path","track"]]
    ]


steps = [
    ["highway", ["steps"]]
    ]

railWayWidthMeters = 20
railWay = [
    ["railway", ["rail"]]
    ]

oliveArea = [
    ["amenity", ["kindergarten", "stage"]],
    ["aerialway", [""]],
    ["aeroway", [""]],
    ["craft", [""]],
    ["emergency", [""]],
    ["geological", [""]],
    ["Healthcare", [""]],
    ["leisure", [""]],
    ["man_made", [""]],
    ["military", [""]],
    ["office", [""]],
    ["place", [""]],
    ["public_transport", [""]],
    ["route", [""]],
    ["shop", [""]],
    ["sport", [""]],
    ["telecom", [""]],
    ["tourism", [""]],

    [ "power", [ "generator","substation","plant" ] ],
    ["amenity", ["library","theatre","school","pub","restaurant","cafe","bank","fast_food","fuel","cinema","social_facility","ice_cream"] ]
    ]

asphaltArea = [
    ["landuse", ["railway","commercial","industrial","education","civic","retail","residential","observatory"]],
    ["railway", ["platform_edge","construction","platform","abandoned","turntable","disused","razed"]],
    ["amenity", ["events_venue","parking_space","parking","marketplace","bus_station","construction"]]
    ]

brownArea = [
    ["landuse", ["greenhouse_horticulture","construction","quarry","brownfield","landfill"]]
]

# reef is stony
forestArea = [
    ["landuse", ["snowfill","churchyard","reservoir"]],
    ["natural", ["forest","wood","cemetery","religious", "reef"]]
    ]

# meadow,heath semiopen; sand is sand
openArea = [
    ["landuse", ["grass","farmyard","recreation_ground","orchard","greenfield","allotments","farmland","grassland","meadow"]],
    ["natural", ["heath", "grassland","sand","beach"]]
    ]

cliffArea = [
    ["natural", ["cliff"]]
    ]

waterArea = [
    ["water", ["river","wastewater","pond","lake","basin","cove","reservoir","ditch","canal","fish_pass"]],
    ["natural", ["wetland","water"]],
    ["waterway",["river", "boatyard"]]
    ]

coastLine = [
    ["natural", ["coastline","dam","weir"]]
    ]

waterLine = [
    ["waterway",["drain","stream", "canal", "ditch", "weir", "fish_pass"]],
    ["natural",["drain","stream", "canal", "strait"]]
    ]


seaHintThreshold = 10
seaHints = {
    ("s", "w"): ["sw"],
    ("n", "w"): ["nw"],
    ("s", "e"): ["se"],
    ("n", "e"): ["ne"],
    ("w", "s"): ["sw"],
    ("w", "n"): ["nw"],
    ("e", "s"): ["se"],
    ("e", "n"): ["ne"],
    ("e", "w"): ["se","sw","ne","nw"],
    ("w", "e"): ["sw","se","nw","ne"],
    ("s", "n"): ["se","ne","sw","nw"],
    ("n", "s"): ["ne","se","nw","sw"]
    }
seaX = { "sw": 0, "nw": 0, "se": 1, "ne": 1 }
seaY = { "sw": 1, "nw": 0, "se": 1, "ne": 0 }

def coastlineToPolygon(points, size):
    if len(points) < 2:
        return []

    pts = []
    previous = ""
    previousbad = ""
    for point in points:
        pts.append(point)

    if len(pts) < 2:
        return []

    start = ""
    end = ""
    if pts[0][0] < seaHintThreshold:
        if pts[0][1] < pts[0][0]:
            start = "s"
        elif size[1] - pts[0][1] < pts[0][0]:
            start = "n"
        else:
            start = "w"
    elif size[0] - pts[0][0] < seaHintThreshold:
        if pts[0][1] < size[0] - pts[0][0]:
            start = "s"
        elif size[1] - pts[0][1] < size[0] - pts[0][0]:
            start = "n"
        else:
            start = "e"
    elif pts[0][1] < seaHintThreshold:
        start = "s"
    elif size[1] - pts[0][1] < seaHintThreshold:
        start = "n"

    if pts[-1][0] < seaHintThreshold:
        if pts[-1][1] < pts[-1][0]:
            end = "s"
        elif size[1] - pts[-1][1] < pts[-1][0]:
            end = "n"
        else:
            end = "w"
    elif size[0] - pts[-1][0] < seaHintThreshold:
        if pts[-1][1] < size[0] - pts[-1][0]:
            end = "s"
        elif size[1] - pts[-1][1] < size[0] - pts[-1][0]:
            end = "n"
        else:
            end = "e"
    elif pts[-1][1] < seaHintThreshold:
        end = "s"
    elif size[1] - pts[-1][1] < seaHintThreshold:
        end = "n"

    if start == "" or end == "":
        return []

    if start == end:
        return pts

    if (start, end) not in seaHints:
        return []

    if len(seaHints[(start, end)]) == 1:
        hint = seaHints[(start, end)][0]
        pts.append((size[0] * seaX[hint], size[1] * seaY[hint]))
        return pts

    if len(seaHints[(start, end)]) != 4:
        return []

    hint = seaHints[(start, end)][0]    
    route1pt1 = (size[0] * seaX[hint], size[1] * seaY[hint])
    hint = seaHints[(start, end)][1]    
    route1pt2 = (size[0] * seaX[hint], size[1] * seaY[hint])
    hint = seaHints[(start, end)][2]    
    route2pt1 = (size[0] * seaX[hint], size[1] * seaY[hint])
    hint = seaHints[(start, end)][3]    
    route2pt2 = (size[0] * seaX[hint], size[1] * seaY[hint])

    if calculatePathDistance([pts[-1], route1pt1, route1pt2, pts[0]]) < calculatePathDistance([pts[-1], route2pt1, route2pt2, pts[0]]):
        pts.append(route1pt1)
        pts.append(route1pt2)
        return pts
    else:
        pts.append(route2pt1)
        pts.append(route2pt2)
        return pts
    return []

waytypes = ["building", "power", "highway", "landuse", "natural", "water", "waterway", "barrier", "amenity", "railway","aerialway","aeroway","craft","emergency","geological","Healthcare","leisure","man_made","military","office","place","public_transport","route","shop","sport","telecom","tourism"]


def toPictureCoordinates(latlonMapOrigo, latlonPointToConvert, xyPictureSize, metersPerPixel):
    lat_to_meters = 111132
    lon_to_meters = lat_to_meters * cos(radians(latlonMapOrigo[0]))

    latlonOffset = (latlonPointToConvert[0] - latlonMapOrigo[0], latlonPointToConvert[1] - latlonMapOrigo[1])
    xyPos = (latlonOffset[1] * lon_to_meters / metersPerPixel, latlonOffset[0] * lat_to_meters / metersPerPixel)
    return xyPos

def oppositeToLatLonCoordinates(latlonMapOrigo, xyPictureSize, metersPerPixel):
    lat_to_meters = 111132
    lon_to_meters = lat_to_meters * cos(radians(latlonMapOrigo[0]))


    latlonOffset = (xyPictureSize[1] / lat_to_meters *metersPerPixel, xyPictureSize[0] / lon_to_meters *metersPerPixel)
    latlonPos = (latlonMapOrigo[0] + latlonOffset[0], latlonMapOrigo[1] + latlonOffset[1])
    return latlonPos

def checkIfWaydbInLocalCache(latlonMapOrigo):
    waydb = {}
    offlineMapData = offlineMapDataFolder + str(round(latlonMapOrigo[0] ,5)) + "_" + str(round(latlonMapOrigo[1],5)) + ".json"
    fname = os.path.join(getPackagePath(), offlineMapData)
    if os.path.isfile(fname):
        with open(fname, 'rb') as f:
            waydb = json.load(f)
    return waydb
    

async def constructWayDb(latlonMapOrigo, xyPictureSize, metersPerPixel):
    waydb = checkIfWaydbInLocalCache(latlonMapOrigo)
    if waydb:
        return waydb

    # if not cached then do the hard way and download fresh one
    try:
        import overpy

        latlonMapOppositeCorner = oppositeToLatLonCoordinates(latlonMapOrigo, xyPictureSize, metersPerPixel)

        api = overpy.Overpass()

    
        for waytype in waytypes:
            result = api.query("""
                way("""+str(latlonMapOrigo[0])+""","""+str(latlonMapOrigo[1])+""","""+str(latlonMapOppositeCorner[0])+""","""+str(latlonMapOppositeCorner[1])+""") [\"""" + waytype + """\"];
                (._;>;);
                out body;
                """)

            if waytype not in waydb:
                waydb[waytype] = {}
            if await uiFlushEvents():
                return None

            for way in result.ways:
                subway = way.tags.get(waytype, "n/a")
                if subway not in waydb[waytype]:
                    waydb[waytype][subway] = []
                if await uiFlushEvents():
                    return None
                poslistToAppend = []
                for node in way.nodes:
                    xyPos = toPictureCoordinates(latlonMapOrigo, (float(node.lat), float(node.lon)), xyPictureSize, metersPerPixel)
                    poslistToAppend.append(xyPos)
                waydb[waytype][subway].append(poslistToAppend)
    except Exception as err:
        waydb = {}

    if not waydb:
        waydb = checkIfWaydbInLocalCache(latlonMapOrigo)

    return waydb


def queryForbiddenSpot(mask, x, y):
    rect = mask.get_rect()
    if x <= rect[0]+1 or x >= rect[0] + rect[2] -1 or y <= rect[1]+1 or y >= rect[1] + rect[3] -1:
        return False
    currentMask = mask.get_at((int(x), int(y)))
    if currentMask == getForbiddenAreaMask():
        return True
    return False

def markControlSpot(mask, x, y):
    if not queryForbiddenSpot(mask, x, y):
        mask.fill(getControlMask(), ((int(x),int(y)), (1, 1)))
    else:
       for shift in [(0, 4), (4,0), (-4, 0), (0, -4)]:
           if not queryForbiddenSpot(mask, int(x + shift[0]), int(y + shift[1])):
               mask.fill(getControlMask(), ((int(x + shift[0]), int(y + shift[1])), (1, 1)))


def uiDrawLines(surf, color, pointlist, width):
    for ind in range(len(pointlist) - 1):
        uiDrawLine(surf, color, pointlist[ind], pointlist[ind+1], width)


def drawPolylineWithWidth(png, mask, pointlist, polylineColor, polylineMaskColor,polylineWidth, accurate):
    if len(pointlist) > 1:
        if accurate:
            uiDrawLines(png, polylineColor, pointlist, int(polylineWidth))
        else:
            pygame.draw.lines(png, polylineColor, False, pointlist, width=int(polylineWidth))
        pygame.draw.lines(mask, polylineMaskColor, False, pointlist, width=int(polylineWidth))
        if pointlist:
            markControlSpot(mask, pointlist[0][0], pointlist[0][1])
            markControlSpot(mask, pointlist[-1][0], pointlist[-1][1])


def drawPolygonWithBounds(png, mask, pointlist, polyInternalColor, polyBoundaryColor, polyMaskColor):
    if len(pointlist) > 2:
        pygame.draw.polygon(mask, polyMaskColor, pointlist)
        pygame.draw.polygon(png, polyInternalColor, pointlist)
        uiDrawLines(png, polyBoundaryColor, pointlist + [pointlist[0]], 1)
        for point in pointlist:
            markControlSpot(mask, point[0], point[1])


def drawContours(kernelWidth, contourArr, keepOneOf):
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
                contourLookup[(x*2, y*2)] = True

    for point in contourLookup:
        for shift in [(-2, 0), (2, 0), (0, 2), (0, -2), (-2, 2), (2, 2), (2, -2), (-2, -2)]:
            point2 = (point[0] + shift[0], point[1] + shift[1])
            if point2 in contourLookup:
                uiDrawLine(contourArr, colors[BROWNX], point, point2, 1)

    return sumArr, contourArr


def drawSpot(png, mask, pointlist, filltype):
    radius = 3
    crossradius = 2
    marshradius = 2
    x = pointlist[0][0]
    y = pointlist[0][1]
    if filltype == BROWNX or filltype == BLACKX:
        pygame.draw.line(png, colors[filltype], (x-crossradius, y-crossradius), (x+crossradius, y+crossradius))
        pygame.draw.line(png, colors[filltype], (x-crossradius, y+crossradius), (x+crossradius, y-crossradius))
    elif filltype == STONE or filltype == BROWNSTONE:
        pygame.draw.circle(png, colors[filltype], (x, y), radius)
    elif filltype == GREENCIRCLE:
        pygame.draw.circle(png, colors[filltype], (x, y), radius = 2)
    markControlSpot(mask, x, y)
        

def boundarize(png, tmpColorToBoundarize, colorToBoundarize, boundaryColor):
    size = png.get_size()
    pngCopy = png.copy()
    for y in range(1, size[1]-1):
        for x in range(1, size[0]-1):
            if png.get_at((x, y)) == tmpColorToBoundarize:
                if (png.get_at((x, y-1)) != tmpColorToBoundarize or png.get_at((x, y+1)) != tmpColorToBoundarize or png.get_at((x-1, y)) != tmpColorToBoundarize or png.get_at((x+1, y)) != tmpColorToBoundarize):
                    pngCopy.set_at((x, y), boundaryColor)
                else:
                    pngCopy.set_at((x, y), colorToBoundarize)
    return pngCopy


def drawHouses(png, mask, waydb):
    for waytypelist in houseArray:
        waytype = waytypelist[0]
        subwaylist = waytypelist[1]
        for subway in subwaylist:
            if waytype in waydb and subway in waydb[waytype]:
                subwayarray = waydb[waytype][subway]
                waydb[waytype].pop(subway)
                for house in subwayarray:
                    drawPolygonWithBounds(png, mask, house, colors[HOUSEINTERNAL], colors[SOLIDBLACK], getForbiddenAreaMask())
    for waytypelist in shelterArray:
        waytype = waytypelist[0]
        subwaylist = waytypelist[1]
        for subway in subwaylist:
            if waytype in waydb and subway in waydb[waytype]:
                subwayarray = waydb[waytype][subway]
                waydb[waytype].pop(subway)
                for shelter in subwayarray:
                    drawPolygonWithBounds(png, mask, shelter, colors[SHELTERINTERNAL], colors[SOLIDBLACK], getSlowAreaMask())
    return png, mask


def drawCliff(png, mask, waydb):
    for waytypelist in cliffArea:
        waytype = waytypelist[0]
        subwaylist = waytypelist[1]
        for subway in subwaylist:
            if waytype in waydb and subway in waydb[waytype]:
                subwayarray = waydb[waytype][subway]
                waydb[waytype].pop(subway)
                for way in subwayarray:
                    drawPolylineWithWidth(png, mask, way, colors[SOLIDBLACK], getForbiddenAreaMask(), 4, True)
    return png, mask


def drawWater(png, mask, waydb):
    for waytypelist in waterArea:
        waytype = waytypelist[0]
        subwaylist = waytypelist[1]
        for subway in subwaylist:
            if waytype in waydb and subway in waydb[waytype]:
                subwayarray = waydb[waytype][subway]
                waydb[waytype].pop(subway)
                for house in subwayarray:
                    drawPolygonWithBounds(png, mask, house, colors[WATER], colors[WATER], getForbiddenAreaMask())
    png = boundarize(png,  colors[WATER], colors[WATER], colors[SOLIDBLACK])
    for waytypelist in coastLine:
        waytype = waytypelist[0]
        subwaylist = waytypelist[1]
        for subway in subwaylist:
            if waytype in waydb and subway in waydb[waytype]:
                subwayarray = waydb[waytype][subway]
                waydb[waytype].pop(subway)
                for way in subwayarray:
                    polygonWay = coastlineToPolygon(way, png.get_size())
                    if polygonWay:
                        drawPolygonWithBounds(png, mask, polygonWay, colors[WATER], colors[WATER], getForbiddenAreaMask())
                    drawPolylineWithWidth(png, mask, way, colors[SOLIDBLACK], getForbiddenAreaMask(), 2, True)
    for waytypelist in waterLine:
        waytype = waytypelist[0]
        subwaylist = waytypelist[1]
        for subway in subwaylist:
            if waytype in waydb and subway in waydb[waytype]:
                subwayarray = waydb[waytype][subway]
                waydb[waytype].pop(subway)
                for way in subwayarray:
                    drawPolylineWithWidth(png, mask, way, colors[WATER], getForbiddenAreaMask(), 2, True)
    return png, mask


def drawFences(png, mask, waydb):
    for waytypelist in solidFence:
        waytype = waytypelist[0]
        subwaylist = waytypelist[1]
        for subway in subwaylist:
            if waytype in waydb and subway in waydb[waytype]:
                subwayarray = waydb[waytype][subway]
                waydb[waytype].pop(subway)
                for way in subwayarray:
                    drawPolylineWithWidth(png, mask, way, colors[SOLIDBLACK], getForbiddenAreaMask(), 2, True)
    for waytypelist in solidGreenFence:
        waytype = waytypelist[0]
        subwaylist = waytypelist[1]
        for subway in subwaylist:
            if waytype in waydb and subway in waydb[waytype]:
                subwayarray = waydb[waytype][subway]
                waydb[waytype].pop(subway)
                for way in subwayarray:
                    drawPolylineWithWidth(png, mask, way, colors[SOLIDGREEN], getForbiddenAreaMask(), 2, True)
    for waytypelist in thinFence:
        waytype = waytypelist[0]
        subwaylist = waytypelist[1]
        for subway in subwaylist:
            if waytype in waydb and subway in waydb[waytype]:
                subwayarray = waydb[waytype][subway]
                waydb[waytype].pop(subway)
                for way in subwayarray:
                    drawPolylineWithWidth(png, mask, way, colors[SOLIDBLACK], getVerySlowAreaMask(), 1, True)
    return png, mask


def drawOpenArea(png, mask, waydb):
    for waytypelist in openArea:
        waytype = waytypelist[0]
        subwaylist = waytypelist[1]
        for subway in subwaylist:
            if waytype in waydb and subway in waydb[waytype]:
                subwayarray = waydb[waytype][subway]
                waydb[waytype].pop(subway)
                for area in subwayarray:
                    drawPolygonWithBounds(png, mask, area, colors[OPENAREA], colors[OPENAREA], getSemiSlowAreaMask())
    return png, mask


def drawForestArea(png, mask, waydb):
    for waytypelist in forestArea:
        waytype = waytypelist[0]
        subwaylist = waytypelist[1]
        for subway in subwaylist:
            if waytype in waydb and subway in waydb[waytype]:
                subwayarray = waydb[waytype][subway]
                waydb[waytype].pop(subway)
                for area in subwayarray:
                    drawPolygonWithBounds(png, mask, area, colors[FOREST], colors[FOREST], getSlowAreaMask())
    return png, mask


def drawBrownArea(png, mask, waydb):
    for waytypelist in brownArea:
        waytype = waytypelist[0]
        subwaylist = waytypelist[1]
        for subway in subwaylist:
            if waytype in waydb and subway in waydb[waytype]:
                subwayarray = waydb[waytype][subway]
                waydb[waytype].pop(subway)
                for area in subwayarray:
                    drawPolygonWithBounds(png, mask, area, colors[BROWNX], colors[BROWNX], getSlowAreaMask())
    return png, mask


def drawAsphaltArea(png, mask, waydb):
    for waytypelist in asphaltArea:
        waytype = waytypelist[0]
        subwaylist = waytypelist[1]
        for subway in subwaylist:
            if waytype in waydb and subway in waydb[waytype]:
                subwayarray = waydb[waytype][subway]
                waydb[waytype].pop(subway)
                for area in subwayarray:
                    drawPolygonWithBounds(png, mask, area, colors[ASPHALT], colors[ASPHALT], getNoMask())
    return png, mask


def drawOliveArea(png, mask, waydb):
    for waytypelist in oliveArea:
        waytype = waytypelist[0]
        subwaylist = waytypelist[1]
        for subway in subwaylist:
            if waytype in waydb and subway in waydb[waytype]:
                subwayarray = waydb[waytype][subway]
                waydb[waytype].pop(subway)
                for area in subwayarray:
                    drawPolygonWithBounds(png, mask, area, colors[OLIVEGREEN], colors[OLIVEGREEN], getForbiddenAreaMask())
            elif waytype in waydb and subway == "":
                for subwayarray in waydb[waytype]:
                    for area in subwayarray:
                        drawPolygonWithBounds(png, mask, area, colors[OLIVEGREEN], colors[OLIVEGREEN], getForbiddenAreaMask())
                
    return png, mask


def drawSolidGreenArea(png, mask, waydb):
    for waytypelist in solidGreenArea:
        waytype = waytypelist[0]
        subwaylist = waytypelist[1]
        for subway in subwaylist:
            if waytype in waydb and subway in waydb[waytype]:
                subwayarray = waydb[waytype][subway]
                waydb[waytype].pop(subway)
                for area in subwayarray:
                    drawPolygonWithBounds(png, mask, area, colors[SOLIDGREEN], colors[SOLIDGREEN], getForbiddenAreaMask())
    return png, mask


def drawSpots(png, mask, waydb):
    for waytypelist in spotArray:
        waytype = waytypelist[0]
        subwaylist = waytypelist[1]
        for subway in subwaylist:
            if waytype in waydb and subway in waydb[waytype]:
                subwayarray = waydb[waytype][subway]
                waydb[waytype].pop(subway)
                for area in subwayarray:
                    drawSpot(png, mask, area, BLACKX)
    for waytypelist in stoneArray:
        waytype = waytypelist[0]
        subwaylist = waytypelist[1]
        for subway in subwaylist:
            if waytype in waydb and subway in waydb[waytype]:
                subwayarray = waydb[waytype][subway]
                waydb[waytype].pop(subway)
                for area in subwayarray:
                    drawSpot(png, mask, area, STONE)
    for waytypelist in treeArray:
        waytype = waytypelist[0]
        subwaylist = waytypelist[1]
        for subway in subwaylist:
            if waytype in waydb and subway in waydb[waytype]:
                subwayarray = waydb[waytype][subway]
                waydb[waytype].pop(subway)
                for area in subwayarray:
                    drawSpot(png, mask, area, GREENCIRCLE)
    return png, mask


def drawRailway(png, mask, waydb, metersPerPixel):
    for waytypelist in railWay:
        waytype = waytypelist[0]
        subwaylist = waytypelist[1]
        for subway in subwaylist:
            if waytype in waydb and subway in waydb[waytype]:
                subwayarray = waydb[waytype][subway]
                waydb[waytype].pop(subway)
                for way in subwayarray:
                    drawPolylineWithWidth(png, mask, way, colors[OLIVEGREEN], getForbiddenAreaMask(), railWayWidthMeters / metersPerPixel, False)
    return png, mask


def drawRoads(png, mask, waydb, metersPerPixel):
    for waytypelist in wideWay:
        waytype = waytypelist[0]
        subwaylist = waytypelist[1]
        for subway in subwaylist:
            if waytype in waydb and subway in waydb[waytype]:
                subwayarray = waydb[waytype][subway]
                waydb[waytype].pop(subway)
                for way in subwayarray:
                    drawPolylineWithWidth(png, mask, way, colors[TMPASPHALT], getNoMask(), wideWayWidthMeters / metersPerPixel, False)
    for waytypelist in midWay:
        waytype = waytypelist[0]
        subwaylist = waytypelist[1]
        for subway in subwaylist:
            if waytype in waydb and subway in waydb[waytype]:
                subwayarray = waydb[waytype][subway]
                waydb[waytype].pop(subway)
                for way in subwayarray:
                    drawPolylineWithWidth(png, mask, way, colors[TMPASPHALT], getNoMask(), midWayWidthMeters / metersPerPixel, False)
    for waytypelist in unclassifiedWay:
        waytype = waytypelist[0]
        subwaylist = waytypelist[1]
        for subway in subwaylist:
            if waytype in waydb and subway in waydb[waytype]:
                subwayarray = waydb[waytype][subway]
                waydb[waytype].pop(subway)
                for way in subwayarray:
                    drawPolylineWithWidth(png, mask, way, colors[TMPASPHALT], getNoMask(), unclassifiedWayWidthMeters / metersPerPixel, False)
    for waytypelist in smallWay:
        waytype = waytypelist[0]
        subwaylist = waytypelist[1]
        for subway in subwaylist:
            if waytype in waydb and subway in waydb[waytype]:
                subwayarray = waydb[waytype][subway]
                waydb[waytype].pop(subway)
                for way in subwayarray:
                    drawPolylineWithWidth(png, mask, way, colors[TMPASPHALT], getNoMask(), smallWayWidthMeters / metersPerPixel, False)
    png = boundarize(png,  colors[TMPASPHALT], colors[ASPHALT], colors[SOLIDBLACK])
    return png, mask


def checkSpotNeighbourhood(png, x, y, kind):
    
    if png.get_at((x, y)) in kind and png.get_at((x, y - 1)) in kind and png.get_at((x, y + 1)) in kind and png.get_at((x - 1, y)) in kind and png.get_at((x + 1, y)) in kind and png.get_at((x - 1, y - 1)) in kind and png.get_at((x - 1, y + 1)) in kind and png.get_at((x + 1, y - 1)) in kind and png.get_at((x + 1, y + 1)) in kind:
        return True
    return False


def drawArtificialSpot(png, mask):
    xmax, ymax = png.get_size()

    x = randrange(2, xmax - 2)
    y = randrange(2, ymax - 2)

    if not checkSpotNeighbourhood(png, x, y, overlapkind):
        return png, mask
        
    if checkSpotNeighbourhood(png, x, y, spotmodifying):
        prevind = spotmodifying.index(png.get_at((x, y)))
        newval = newspotvalues[prevind]
        if newval == STONE:
            lottery = randrange(0, 5)
            if lottery == 0:
                newval = BROWNX
            if lottery == 1:
                newval = BROWNSTONE
            elif lottery == 2:
                newval = MARSH
        drawSpot(png, mask, [(x, y)], newval)
    return png, mask


def drawArtificialSpots(png, mask):
    x, y = png.get_size()
    minNumSpots = (x*y)//(4*400*spotnessFactor)
    maxNumSpots = 4 * minNumSpots
    for ind in range(randrange(minNumSpots,maxNumSpots)):
        png, mask = drawArtificialSpot(png, mask)
    return png, mask


async def initWorldCreator(size, imagePath):
    png = pygame.Surface(size)
    mask = pygame.Surface(size)
    pattern = pygame.image.load(os.path.join(imagePath, "lemesoftnostalgic/OpenPattern.png"))
    psize = pattern.get_size()
    for x in range(size[0]//psize[0]):
        for y in range(size[1]//psize[1]):
            png.blit(pattern, (x * psize[0], y * psize[1]))
    mask.fill(getSlowAreaMask())
    return png, mask


async def getInfiniteWorld(latlonMapOrigo, xyPictureSize, metersPerPixel, imagePath, offline):
    world, worldMask = await initWorldCreator(xyPictureSize, imagePath)
    if world == None:
        return None, None

    await asyncio.sleep(0)
    db = await constructWayDb(latlonMapOrigo, xyPictureSize, metersPerPixel)

    if db == None:
        return None, None

    await asyncio.sleep(0)
    if await uiFlushEvents():
        return None, None
    world, worldMask = drawForestArea(world, worldMask, db)

    await asyncio.sleep(0)
    if await uiFlushEvents():
        return None, None
    world, worldMask = drawOpenArea(world, worldMask, db)

    await asyncio.sleep(0)
    if await uiFlushEvents():
        return None, None
    world, worldMask = drawBrownArea(world, worldMask, db)

    await asyncio.sleep(0)
    if await uiFlushEvents():
        return None, None
    world, worldMask = drawAsphaltArea(world, worldMask, db)

    await asyncio.sleep(0)
    if await uiFlushEvents():
        return None, None
    world, worldMask = drawOliveArea(world, worldMask, db)

    await asyncio.sleep(0)
    if await uiFlushEvents():
        return None, None
    world, worldMask = drawSolidGreenArea(world, worldMask, db)

    dummy_heightmap, world = drawContours(randrange(countoursMinKernelWidth, countoursMaxKernelWidth), world, randrange(countoursMinOutOf, countoursMaxOutOf))

    await asyncio.sleep(0)
    if await uiFlushEvents():
        return None, None
    world, worldMask = drawWater(world, worldMask, db)

    await asyncio.sleep(0)
    if await uiFlushEvents():
        return None, None
    world, worldMask = drawCliff(world, worldMask, db)

    await asyncio.sleep(0)
    if await uiFlushEvents():
        return None, None
    world, worldMask = drawRailway(world, worldMask, db, metersPerPixel)

    await asyncio.sleep(0)
    if await uiFlushEvents():
        return None, None
    world, worldMask = drawArtificialSpots(world, worldMask)

    await asyncio.sleep(0)
    if await uiFlushEvents():
        return None, None
    world, worldMask = drawRoads(world, worldMask, db, metersPerPixel)

    await asyncio.sleep(0)
    if await uiFlushEvents():
        return None, None
    world, worldMask = drawFences(world, worldMask, db)

    await asyncio.sleep(0)
    if await uiFlushEvents():
        return None, None
    world, worldMask = drawHouses(world, worldMask, db)

    await asyncio.sleep(0)
    if await uiFlushEvents():
        return None, None
    world, worldMask = drawSpots(world, worldMask, db)
    x, y = worldMask.get_size()
    pygame.draw.rect(worldMask, getForbiddenAreaMask(), [(2,2), ((x-2, y-2))], width=2)

    return world, worldMask


def getInfiniteWorldPlace(city, citymap):
    currmap = []
    for tentative in citymap:
        if tentative[0] == city:
            currmap = tentative[1]
            break
    if currmap:
        setup = currmap[randrange(len(currmap))]
        place = tuple(setup[0])
        placeName = ""
        if len(setup) > 2:
            placeName = setup[2]
        if placeName == 1.0:
            placeName = ""
        return place, placeName
    return None, None


async def getInfiniteWorldDefault(place, imagePath, offline):
    latlonMapOrigo = tuple(place)
    metersPerPixel = (0.9 + 0.2 *random())
    xyPictureSize = (1024, 720)
    return await getInfiniteWorld(latlonMapOrigo, xyPictureSize, metersPerPixel, imagePath, offline)
