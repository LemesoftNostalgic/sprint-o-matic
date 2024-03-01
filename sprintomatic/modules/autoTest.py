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

from random import randrange
import math

# test state
controlCtr = 0
valueCtrs = [0, 0, 0, 0]
continuous = False

def fakeUiEvent():
    events = []
    if randrange(2) == 0:
        events.append("left")
    else:
        events.append("right")
    if randrange(2) == 0:
        events.append("tick")
    if randrange(2) == 0:
        events.append("release")
    if randrange(2) == 0:
        events.append("tick")

    if not continuous and randrange(1000) == 0:
        events.append("quit")
    elif continuous and randrange(100) == 0:
        events.append("quit")
        
    return events


def fakeInitScreen(imagePath, gameSettings, externalImageData):
    global valueCtrs
    global continuous
    values = [
        [400, 1000, 1600, 2200,  3200,  4800],
        [ [0.60, 0.30, 0.10, 0.00, 0.00],
           [0.40, 0.30, 0.20, 0.10, 0.00],
           [0.20, 0.30, 0.30, 0.15, 0.05],
           [0.10, 0.25, 0.30, 0.25, 0.10],
           [0.10, 0.10, 0.20, 0.30, 0.30],
           [0.00, 0.05, 0.15, 0.35, 0.45]
           ],
        ["repeat", "one-shot", "superfast", "pacemaker"],
        ["infinite-oulu", "Fantasy", "Tartu"],
        ]
    infiniteOuluTerrains = ["shortLeg", "mediumLeg", "mediumLeg", "mediumLeg", "longLeg", "longLeg"]

    gameSettings.trackLength = values[0][valueCtrs[0]]
    for ind in range(len(values[1][valueCtrs[1]])):
        gameSettings.distributionOfControlLegs[ind][2] = values[1][valueCtrs[1]][ind]
    gameSettings.infiniteOuluTerrain = infiniteOuluTerrains[values[1].index(values[1][valueCtrs[1]])]
    if valueCtrs[2] < 2:
        gameSettings.continuous = True if values[2][valueCtrs[2]]=="repeat" else False
        continuous = gameSettings.continuous
        gameSettings.speed = "regular"
        gameSettings.pacemaker = 0
    elif values[2][valueCtrs[2]] == "pacemaker":
        gameSettings.pacemaker = 1
        gameSettings.speed = "regular"
        gameSettings.continuous = False
    else:
        gameSettings.speed = "superfast"
        gameSettings.pacemaker = 0
        gameSettings.continuous = True

    if values[3][valueCtrs[3]] == "infinite-oulu":
        gameSettings.infiniteOulu = True
        gameSettings.externalExample = ""
    else:
        gameSettings.infiniteOulu = False
        gameSettings.externalExample = values[3][valueCtrs[3]]

    # loop tests
    valueCtrs[0] = valueCtrs[0] + 1
    if valueCtrs[0] >= len(values[0]):
        valueCtrs[0] = 0
        valueCtrs[1] = valueCtrs[1] + 1
        if valueCtrs[1] >= len(values[1]):
            valueCtrs[1] = 0
            valueCtrs[2] = valueCtrs[2] + 1
            if valueCtrs[2] >= len(values[2]):
                valueCtrs[2] = 0
                valueCtrs[3] = valueCtrs[3] + 1
                if valueCtrs[3] >= len(values[3]):
                    valueCtrs[3] = 0

    print(valueCtrs)
    print(gameSettings.infiniteOuluTerrain, gameSettings.continuous, gameSettings.speed, gameSettings.pacemaker, gameSettings.infiniteOulu, gameSettings.externalExample)
    controlCtr = 0

    return False, gameSettings


def fakeResetAgain():
    global controlCtr
    controlCtr = 0


def fakeCalculateNextStep(controls):
    global controlCtr
    angle = (randrange(360) * math.pi) / 180.0

    if controlCtr % 2 == 0 and controlCtr//2 < len(controls):
        pos = controls[controlCtr//2]
        controlCtr = controlCtr + 1
    elif controlCtr//2 >= len(controls) - 1:
        pos = controls[-1]
        controlCtr = 0
        
    else:
        pos = ((controls[controlCtr//2][0] + controls[controlCtr//2 + 1][0])/2, (controls[controlCtr//2][1] + controls[controlCtr//2 + 1][1])/2)
        controlCtr = controlCtr + 1
    # print("  ->", pos, angle)

    return pos, angle
