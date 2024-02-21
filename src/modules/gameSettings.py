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

import pickle
import argparse
import os
from random import randrange

from .utils import getPackagePath
from .infiniteOulu import setupPreGeneratedInfiniteOulu, getPreGeneratedInfiniteOulu
from .lookupPngReader import extractPngLookups, extractPngLookupsFromFile
from .imageDownloader import downloadMapSurfacesBasedOnUrl

def numRestrict(minVal, maxVal):
    def numChecker(val):
        if float(val) < float(minVal):
            return float(minVal)
        elif float(val) > float(maxVal):
            return float(maxVal)
        return float(val)
    return numChecker

def returnSettings():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mapFileName", type=str, help="sprint orienteering map, png format", default='')
    parser.add_argument("--lookupPngName", type=str, help="pre-calculated lookup tables for the API, png format", default='')
    parser.add_argument("--routeFileName", type=str, help="pickled ordered list of tuples (track control points)", default='')
    parser.add_argument("--trackLength", type=numRestrict(500,5500), help="the minimum track length in meters", default=2200)
    parser.add_argument("--miniLegProbability", type=numRestrict(0.0,0.99), help="prob. of mini legs (0.0-0.99)", default=0.20)
    parser.add_argument("--shortLegProbability", type=numRestrict(0.0,0.99), help="prob. of short legs (0.0-0.99)", default=0.30)
    parser.add_argument("--mediumLegProbability", type=numRestrict(0.0,0.99), help="prob. of medium length legs (0.0-0.99)", default=0.30)
    parser.add_argument("--longLegProbability", type=numRestrict(0.0,0.99), help="prob. of long legs (0.0-0.99)", default=0.15)
    parser.add_argument("--extraLongLegProbability", type=numRestrict(0.0,0.99), help="prob. of extra long legs (0.0-0.99)", default=0.05)
    parser.add_argument("--zoom", type=int, choices=range(1, 5), help="zoom factor (1, 2 or 4)", default=1)
    parser.add_argument("--soundRoot", type=str, help="Root folder of the sound resources", default=os.path.join("sounds", ""))
    parser.add_argument("--imageRoot", type=str, help="Root folder of the sound resources", default=os.path.join("images", ""))
    parser.add_argument("--continuous", type=str, choices=["no", "yes"], help="Continuous game loop (or one-shot play)", default="yes")
    parser.add_argument("--pacemaker", type=int,choices=range(0, 4), help="A pacemaker runner to compete against", default=1)
    parser.add_argument("--metersPerPixel", type=numRestrict(0, 1.8), help="How many meters per map pixel. 0 for autodetect.", default=0)
    parser.add_argument("--autoTest", type=str, choices=["no", "yes"], help="An automatic test mode", default="no")
    parser.add_argument("--infoBox", type=str, choices=["no", "yes"], help="An info box feature", default="no")
    parser.add_argument("--noUiTest", type=str, choices=["no", "yes"], help="DO not show UI during automatic test mode", default="no")
    parser.add_argument("--fullScreen", type=str, choices=["no", "yes"], help="Whether to use a full-screen mode or not", default="yes")
    parser.add_argument("--infiniteOulu", type=str, choices=["no", "yes"], help="Whether to use the automatic Oulu-style map generator", default="no")
    parser.add_argument("--analysis", type=str, choices=["no", "yes"], help="Whether to write the route analyses into a file", default="no")
    parser.add_argument("--ownMasterListing", type=str, help="Override the default wew listing", default="")
    parser.add_argument("--externalExample", type=str, help="The map selection from a web listing", default="")
    parser.add_argument("--externalExampleTeam", type=str, help="The team selection from a web listing", default="")
    parser.add_argument("--infiniteOuluTerrain", type=str, choices=["shortLeg", "mediumLeg", "longLeg"], help="Select the terrain good for a given leg length", default="shortLeg")
    parser.add_argument("--speed", type=str, choices=["regular", "superfast"], help="The speed of the player", default="regular")

    gameSettings = parser.parse_args()

    if getPackagePath():
        gameSettings.soundRoot = os.path.join(getPackagePath(), gameSettings.soundRoot)
        gameSettings.imageRoot = os.path.join(getPackagePath(), gameSettings.imageRoot)

    gameSettings.distributionOfControlLegs = [
    #    m   -   m      probability
        [20.0,    50.0, gameSettings.miniLegProbability],
        [50.0,   100.0, gameSettings.shortLegProbability],
        [100.0,  200.0, gameSettings.mediumLegProbability],
        [200.0,  300.0, gameSettings.longLegProbability],
        [300.0,  500.0, gameSettings.extraLongLegProbability]
    ]
    gameSettings.continuous = True if gameSettings.continuous=="yes" else False
    gameSettings.fullScreen = True if gameSettings.fullScreen=="yes" else False
    gameSettings.infiniteOulu = True if gameSettings.infiniteOulu=="yes" else False
    gameSettings.autoTest = True if gameSettings.autoTest=="yes" else False
    gameSettings.infoBox = True if gameSettings.infoBox=="yes" else False
    gameSettings.analysis = True if gameSettings.analysis=="yes" else False

    setupPreGeneratedInfiniteOulu([
        [(160, 160), (4, 5), 40 + randrange(0, 20), "shortLeg"],
        [(160, 160), (5, 6), 40 + randrange(0, 20), "mediumLeg"],
        [(160, 160), (6, 7), 40 + randrange(0, 20), "longLeg"]
        ])

    if (gameSettings.lookupPngName != '' and gameSettings.mapFileName == '') or (gameSettings.mapFileName != '' and gameSettings.lookupPngName == ''):
        print("Error: please specify --lookupPngName and --mapFileName together")
        gameSettings.lookupPngName = ''
        gameSettings.mapFileName = ''

    return gameSettings


def returnConfig(gameSettings, externalImageData):

    metersPerPixel = 0
    png = None

    if gameSettings.infiniteOulu:
        preGenResult = getPreGeneratedInfiniteOulu(gameSettings.infiniteOuluTerrain)
        png = preGenResult[0]
        pngMask = preGenResult[1]

        faLookup, saLookup, ssaLookup, vsaLookup, tunnelLookup, config = extractPngLookups(pngMask)

    elif not gameSettings.lookupPngName and (gameSettings.externalExampleTeam and gameSettings.externalExample):
        for item in externalImageData:
            if gameSettings.externalExampleTeam == item["team-name"]:
                for subitem in item["sub-listing"]:
                    if gameSettings.externalExample == subitem["name"]:
                        png, pngMask = downloadMapSurfacesBasedOnUrl(subitem)
                        if "meters-per-pixel" in subitem:
                            metersPerPixel = subitem["meters-per-pixel"]
        # I use these to test lost internet connection
        #png = None
        #pngMask = None
        faLookup, saLookup, ssaLookup, vsaLookup, tunnelLookup, config = extractPngLookups(pngMask)

    if gameSettings.lookupPngName: # map given at command line
        faLookup, saLookup, ssaLookup, vsaLookup, tunnelLookup, config = extractPngLookupsFromFile(gameSettings.lookupPngName)
        metersPerPixel = gameSettings.metersPerPixel

    controls = []
    if gameSettings.routeFileName:
        if os.path.isfile(gameSettings.routeFileName):
            with open(gameSettings.routeFileName, 'rb') as f:
                controls = pickle.load(f)

    return config, controls, faLookup, saLookup, ssaLookup, vsaLookup, tunnelLookup, png, metersPerPixel
