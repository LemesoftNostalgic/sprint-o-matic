#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements. See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF 7licenses this file
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

import argparse
import os
from random import randrange

import pygame
import asyncio

from .pathPruning import pruneWeightedDistance
from .utils import getForbiddenAreaMask, getSlowAreaMask, getSemiSlowAreaMask, getVerySlowAreaMask, getControlMask, getTunnelMask

from .perfSuite import perfAddStart, perfAddStop
boundaryThreshold = 10
spacingBetweenControls = 16

def getTfs():
    return [1, 4, 16]
tfsShort = [1, 4]


async def extractPngLookups(oMapMask, benchmark):
    faLookup = {}
    saLookup = {}
    ssaLookup = {}
    vsaLookup = {}
    tunnelLookup = {}
    controls = []
    if oMapMask == None:
        return faLookup, saLookup, ssaLookup, vsaLookup, tunnelLookup, controls

    size = oMapMask.get_size()

    for tf in getTfs():
        faLookup[tf] = {}
        saLookup[tf] = {}
        ssaLookup[tf] = {}
        vsaLookup[tf] = {}
        tunnelLookup[tf] = {}

    fam = getForbiddenAreaMask()
    tm = getTunnelMask()
    cm = getControlMask()
    sm = getSlowAreaMask()
    ssm = getSemiSlowAreaMask()
    vsm = getVerySlowAreaMask()
    phone = True if benchmark == "phone" else False
    for y in range(0, size[1]):
        for x in range(0, size[0]):
            col = oMapMask.get_at((x, y))
            if col == fam:
                for tf in tfsShort:
                    faLookup[tf][(int(x/tf), int(y/tf))] = True
            elif col == tm:
                for tf in tfsShort:
                    tunnelLookup[tf][(int(x/tf), int(y/tf))] = True
            elif col == cm:
                controls.append((x, y))
            elif not phone:
                if col == sm:
                    for tf in tfsShort:
                        saLookup[tf][(int(x/tf), int(y/tf))] = True
                elif col == ssm:
                    for tf in tfsShort:
                        ssaLookup[tf][(int(x/tf), int(y/tf))] = True
                elif col == vsm:
                    for tf in tfsShort:
                        vsaLookup[tf][(int(x/tf), int(y/tf))] = True
                    
    prunedControls = []
    steps = len(controls) // 500
    step = 0
    for item in controls:
        x = item[0]
        y = item[1]
        step = step + 1
        thisStep = steps
        if steps:
            thisStep = randrange(steps)
        if step > thisStep:
            step = 0
        if step == 0:
            if x > boundaryThreshold and x < size[0] - boundaryThreshold and y > boundaryThreshold and y < size[1] - boundaryThreshold:
                if not ((x, y-1) in faLookup[1] and (x, y+1) in faLookup[1]) and not ((x-1, y) in faLookup[1] and (x+1, y) in faLookup[1]):
                    prunedControls.append(item)

    return faLookup, saLookup, ssaLookup, vsaLookup, tunnelLookup, prunedControls


async def extractPngLookupsFromFile(pngFileName, benchmark):
    try:
        oMapMask = pygame.image.load(pngFileName, benchmark)
    except Exception as err:
        print(f"Cannot load map from file: {err=}, {type(err)=}")
        return {}, {}, {}, {}, {}, []

    faLookup, saLookup, ssaLookup, vsaLookup, tunnelLookup, controls = await extractPngLookups(oMapMask)
    return faLookup, saLookup, ssaLookup, vsaLookup, tunnelLookup, controls
