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

import argparse
import os
from random import randrange

import pygame

from .pathPruning import pruneWeightedDistance
from .utils import getForbiddenAreaMask, getSlowAreaMask, getSemiSlowAreaMask, getVerySlowAreaMask, getControlMask, getTunnelMask


def getTfs():
    return [1, 2, 4, 8, 16]



def extractPngLookups(oMapMask):
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

    for y in range(0, size[1]):
        for x in range(0, size[0]):
            col = oMapMask.get_at((x, y))
            if col == getSlowAreaMask():
                for tf in getTfs():
                    saLookup[tf][(int(x/tf), int(y/tf))] = True
            elif col == getTunnelMask():
                for tf in getTfs():
                    tunnelLookup[tf][(int(x/tf), int(y/tf))] = True
            elif col == getSemiSlowAreaMask():
                for tf in getTfs():
                    ssaLookup[tf][(int(x/tf), int(y/tf))] = True
            elif col == getVerySlowAreaMask():
                for tf in getTfs():
                    vsaLookup[tf][(int(x/tf), int(y/tf))] = True
            elif col == getForbiddenAreaMask():
                for tf in getTfs():
                    faLookup[tf][(int(x/tf), int(y/tf))] = True
            elif col == getControlMask():
                controls.append((x, y))

    return faLookup, saLookup, ssaLookup, vsaLookup, tunnelLookup, controls


def extractPngLookupsFromFile(pngFileName):
    try:
        oMapMask = pygame.image.load(pngFileName)
    except Exception as err:
        print(f"Cannot load map from file: {err=}, {type(err)=}")
        return {}, {}, {}, {}, {}, []

    faLookup, saLookup, ssaLookup, vsaLookup, tunnelLookup, controls = extractPngLookups(oMapMask)
    return faLookup, saLookup, ssaLookup, vsaLookup, tunnelLookup, controls
