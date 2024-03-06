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

import math
import random
import pygame

from .utils import getNoMask, getForbiddenAreaMask

longDistance = 10000000.0

def fromRadiansToDegrees(angle):
    return angle/(math.pi/180)


def angleDifference(angle1, angle2):
    while angle1 < 0.0:
        angle1 = angle1 + 2*math.pi
    while angle2 < 0.0:
        angle2 = angle2 + 2*math.pi
    while angle1 > 2*math.pi:
        angle1 = angle1 - 2*math.pi
    while angle2 > 2*math.pi:
        angle2 = angle2 - 2*math.pi
    first = (angle1 - angle2) % (2*math.pi)
    second = (angle2 - angle1) % (2*math.pi)
    num = abs(second)
    if first < second:
        num = abs(first)
    if num > math.pi:
        num = (2*math.pi) - num
    return num


def triangleCreator(radius, angle, pos):
    return [
        tuple(map(lambda i, j: i + j, pos, (radius * math.sin(angle), (radius * math.cos(angle))))),
        tuple(map(lambda i, j: i + j, pos, (radius * math.sin(angle + 0.667 * math.pi), (radius * math.cos(angle + 0.667 * math.pi))))),
        tuple(map(lambda i, j: i + j, pos, (radius * math.sin(angle + 1.333 * math.pi), (radius * math.cos(angle + 1.333 * math.pi)))))
    ]


def rotateVector(angle, length):
    return math.sin(angle) * length, math.cos(angle) * length


def rotatePoint(origin, point, angle):
    ox, oy = origin
    px, py = point
    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
    return qx, qy


def angleBetweenLineSegments(lineA, lineB):
    vA = [(lineA[0][0]-lineA[1][0]), (lineA[0][1]-lineA[1][1])]
    vB = [(lineB[0][0]-lineB[1][0]), (lineB[0][1]-lineB[1][1])]
    dot_prod = vA[0]*vB[0]+vA[1]*vB[1]
    magA = (vA[0]*vA[0]+vA[1]*vA[1])**0.5
    magB = (vB[0]*vB[0]+vB[1]*vB[1])**0.5
    if magA == 0 or magB == 0:
        return 0
    beforeAcos = dot_prod/magB/magA
    if beforeAcos < -1 or beforeAcos > 1:
        return 0
    return math.acos(beforeAcos)


def angleOfLine(line):
    dPosition = tuple(map(lambda i, j: i - j, line[1],  line[0]))
    if dPosition[0] == 0:
        angle = math.pi / 2 - math.atan(dPosition[1]/0.01)
    else:
        angle = math.pi / 2 - math.atan(dPosition[1]/dPosition[0])
    if dPosition[0] < 0:
        angle = angle + math.pi
    return angle


def distanceBetweenPoints(point1, point2):
    return math.sqrt((point1[0]-point2[0])**2 + (point1[1]-point2[1])**2)


def angleOfPath(path, maxdist):
    if len(path) < 2:
        return 0.0
    dist = 0
    previous = path[0]
    current = (0,0)
    for item in path[1:]:
        current = item
        dist = dist + distanceBetweenPoints(previous, current)
        previous = current
        if dist > maxdist:
            break
    return angleOfLine([path[0], previous])


def getRandomAngle():
    return random.random() * math.pi * 2


def getNearestPointOfList(backrouteLookupAdditions, newPoint):
    shortest = longDistance
    nearest = backrouteLookupAdditions[0]
    for point in backrouteLookupAdditions:
        thisDistance = distanceBetweenPoints(point, newPoint)
        if thisDistance < shortest:
            shortest = thisDistance
            nearest = point
    return nearest


def calculatePathDistance(path):
    dist = 0.0
    for index in range(len(path) - 1):
        dist = dist + distanceBetweenPoints(path[index], path[index + 1])
    return dist
    

# Grow a bounding box rectangle with a list of points, can use repeatedly
def getBoundingBox(previousRect, pointList):
    for point in pointList:
        if int(point[0]) < previousRect[0][0]:
            previousRect[0] = (int(point[0]) - 1, previousRect[0][1])
        if int(point[0]) > previousRect[1][0]:
            previousRect[1] = (int(point[0]) + 1, previousRect[1][1])
        if int(point[1]) < previousRect[0][1]:
            previousRect[0] = (previousRect[0][0], int(point[1]) - 1)
        if int(point[1]) > previousRect[1][1]:
            previousRect[1] = (previousRect[1][0], int(point[1]) + 1)
    return previousRect


def polygonCreate(bbox, areaPolygon):
    polygonLookup = {}
    yStart = int(bbox[0][1])
    yEnd = int(bbox[1][1])
    xStart = int(bbox[0][0])
    xEnd = int(bbox[1][0])

    surf = pygame.Surface((xEnd-xStart, yEnd-yStart))
    surf.fill(getNoMask())
    imagePolygon = []
    for pos in areaPolygon:
        imagePolygon.append((pos[0]-xStart, pos[1]-yStart))
    pygame.draw.polygon(surf, getForbiddenAreaMask(), imagePolygon)    

    for y in range(yStart, yEnd):
        for x in range(xStart, xEnd):
            if surf.get_at((x - xStart, y - yStart)) == getForbiddenAreaMask():
                polygonLookup[(x, y)] = True
    return polygonLookup


def polygonContainsWithLookup(polygonLookup, point):
    return point in polygonLookup
