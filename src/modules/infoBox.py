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
from .gameUIUtils import getMasterFont

# These are generic UI utils, now temporarily here
xReference = 1920
yReference = 1080
xCurrent = 1920
yCurrent = 1080
def convertXCoordinate(xCoord):
    return int((xCoord * xCurrent) / xReference)
def convertYCoordinate(yCoord):
    return int((yCoord * yCurrent) / yReference)
blackColor =         pygame.Color(0, 0, 0)
greyColor =         pygame.Color(234, 234, 234)


infoBoxTxt = ""

infoKeys1 = [20, 26, 8, 21, 23, 28, 24, 12, 18, 76]
infoTexts1 = ["This is the Sprint-O-Matic", "an app that I created for my sprint orienteering training", "now I try to use it while running in a treadmill...", "let's select the track parameters", "I choose to run with a pacemaker", "it is possible to use a real Sprint-O map", "however, let's use an automatically generated map", "the game control is via the mouse buttons", "now I start the treadmill...", "That was it, thanks for watching!"]

infoKeys2 = [40, 42, 44]
infoTexts2 = ["I'm going to win this one!", 'An "oh shit!" moment!', "Getting tired..."]


infoBoxTxt = ""
def showInfoBoxTxt(where):
    if infoBoxTxt:
        fontSize = 48
        middle = tuple(ti/2.0 for ti in where.get_size())
        textCenter = (middle[0], middle[1] * 1.5)
        aText = pygame.font.Font(getMasterFont(), convertXCoordinate(fontSize)).render(infoBoxTxt, True, blackColor)
        textRect = aText.get_rect()
        textRect.center = textCenter
        shift = 20
        rounding = 100
        textRectExtended = [textRect[0] - shift * 2, textRect[1] - shift, textRect[2] + convertXCoordinate(shift) * 4, textRect[3] +  convertXCoordinate(shift) * 2]
        pygame.draw.rect(where, greyColor, textRectExtended, 0, convertXCoordinate(100))
        where.blit(aText, textRect)


def updateInfoTxtByEvent(event, keySet):
    global infoBoxTxt

    if keySet == 1:
        infoKeys = infoKeys1
        infoTexts = infoTexts1
    elif keySet == 2:
        infoKeys = infoKeys2
        infoTexts = infoTexts2
    else:
        return ""

    if event.type == pygame.KEYUP:
        infoBoxTxt = ""
    elif event.type == pygame.KEYDOWN:
        if event.scancode in infoKeys:
            infoBoxTxt = infoTexts[infoKeys.index(event.scancode)]
