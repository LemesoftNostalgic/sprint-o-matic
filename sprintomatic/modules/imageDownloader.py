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
import json
import asyncio
import os
import sys
from .utils import getPackagePath


soundUrl = "https://raw.githubusercontent.com/LemesoftNostalgic/sprint-o-matic-sounds/main/"
listingOfTeamsWithListing = "https://raw.githubusercontent.com/LemesoftNostalgic/sprint-o-matic-external-map-links/main/teams-hosting-their-own-map-listing.json"
listingOfMapsInCities = "https://raw.githubusercontent.com/LemesoftNostalgic/sprint-o-matic-external-map-links/main/world-city-maps.json"
newsUrl= "https://raw.githubusercontent.com/LemesoftNostalgic/sprint-o-matic-external-map-links/main/NEWS.txt"

offlineNews = "data/sprint-o-matic-external-map-links-main/NEWS.txt"
offlineTeamsWithListing = "data/sprint-o-matic-external-map-links-main/teams-hosting-their-own-map-listing.json"
offlineMapsInCities = "data/sprint-o-matic-external-map-links-main/world-city-maps.json"

offlineExamplePath = "data/sprint-o-matic-map-image-example-main"


osmQueryPathBase = "https://overpass-api.de/api/interpreter?data=[out%3Ajson]%3B("
osmQueryWayStart = "way("
osmQueryWayBtwNum = "%2C"
osmQueryWayBefWaytype = ")[%22"
osmQueryWayAftWaytype = "%22]%3B"
osmQueryPathEnd = ")%3B%20(._%3B%3E%3B)%3B%20out%20body%3B"

async def downloadOsmData(latlonMapOrigo, latlonMapOppositeCorner, waytypes):

    # compose query, raw manner due to emscripten issues
    osmUrl = osmQueryPathBase
    for waytype in waytypes:
        osmUrl = osmUrl + osmQueryWayStart + str(latlonMapOrigo[0]) + osmQueryWayBtwNum + str(latlonMapOrigo[1]) + osmQueryWayBtwNum + str(latlonMapOppositeCorner[0]) + osmQueryWayBtwNum + str(latlonMapOppositeCorner[1]) + osmQueryWayBefWaytype + waytype + osmQueryWayAftWaytype
    osmUrl = osmUrl + osmQueryPathEnd

    try:
        if sys.platform == 'emscripten':
            import platform
            from pathlib import Path
            pth = Path(osmUrl)
            data = ""
            async with platform.fopen(pth, "r") as textfile:
                data = textfile.read()
        else:
            import requests
            response = requests.get(osmUrl)
            data = response.text
        osmDb = json.loads(data)
    except Exception as err:
        osmDb = []
    return osmDb


async def downloadNews():
    news = ""
    try:
        if sys.platform == 'emscripten':
            import platform
            from pathlib import Path
            pth = Path(newsUrl)
            news = ""
            async with platform.fopen(pth, "r") as textfile:
                news = textfile.read()
        else:
            import requests
            response = requests.get(newsUrl)
            news = response.text
    except Exception as err:
        news = ""

    if not news:
        fname = os.path.join(getPackagePath(), offlineNews)
        if os.path.isfile(fname):
            with open(fname, 'r') as f:
                news = f.read()
    return news


async def downloadExternalWorldCityMap():
    listingofmaps = []
    try:
        if sys.platform == 'emscripten':
            import platform
            from pathlib import Path
            pth = Path(listingOfMapsInCities)
            data = ""
            async with platform.fopen(pth, "r") as textfile:
                data = textfile.read()
        else:
            import requests
            response = requests.get(listingOfMapsInCities)
            data = response.text
        listingofmaps = json.loads(data)
    except Exception as err:
        listingofmaps = []

    if not listingofmaps:
        fname = os.path.join(getPackagePath(), offlineMapsInCities)
        if os.path.isfile(fname):
            with open(fname, 'rb') as f:
                listingofmaps = json.load(f)
    return listingofmaps


async def downloadExternalImageData(ownMasterListing):
    listingofteams = []

    offline = False
    try:
        listingUrl = listingOfTeamsWithListing
        if ownMasterListing:
            listingUrl = ownMasterListing

        if sys.platform == 'emscripten':
            import platform
            from pathlib import Path
            pth = Path(listingUrl)
            data = ""
            async with platform.fopen(pth, "r") as textfile:
                data = textfile.read()
        else:
            import requests
            response = requests.get(listingUrl)
            data = response.text
        listingofteams = json.loads(data)
    except Exception as err:
        listingofteams = []

    if not listingofteams:
        offline = True
        fname = os.path.join(getPackagePath(), offlineTeamsWithListing)
        if os.path.isfile(fname):
            with open(fname, 'rb') as f:
                listingofteams = json.load(f)

    returndata = []
    for team in listingofteams:
        teamdata = None

        try:
            if sys.platform == 'emscripten':
                import platform
                from pathlib import Path
                pth = Path(teamMapListingUrl)
                data = ""
                async with platform.fopen(pth, "r") as textfile:
                    data = textfile.read()
            else:
                teamMapListingUrl = team["map-listing-url"]
                response = requests.get(teamMapListingUrl)
                data = response.text
            teamdata = json.loads(data)
        except Exception as err:
            teamdata = None
        if teamdata is None:
            offline = True
            teamMapListingFile = "data/sprint-o-matic-external-map-links-main/" + team["map-listing-url"].rsplit('/', 1)[-1]
            fname = os.path.join(getPackagePath(), teamMapListingFile)
            if os.path.isfile(fname):
                with open(fname, 'rb') as f:
                    teamdata = json.load(f)

        if teamdata is not None:
            team["sub-listing"] = teamdata
            returndata.append(team)

    return returndata, offline


async def downloadMapSurfacesBasedOnUrl(item):

    imgsurf = None
    pngsurf = None

    try:
        name = item["map-url"]
        if sys.platform == 'emscripten':
            import platform
            from pathlib import Path
            pth = Path(name)
            r_content = b''
            async with platform.fopen(pth, "rb") as binfile:
                r_content = binfile.read()
            img = io.BytesIO(r_content)
            imgsurf = pygame.image.load(img) # -> Surface
        else:
            import requests
            import io
            r = requests.get(name)
            img = io.BytesIO(r.content)
            imgsurf = pygame.image.load(img) # -> Surface
    except Exception as err:
        imgsurf = None

    if imgsurf is None:
        name = "data/sprint-o-matic-map-image-example-main/" + item["map-url"].rsplit('/', 1)[-1].rsplit('?', 1)[0]
        img = os.path.join(getPackagePath(), name)
        imgsurf = pygame.image.load(img) # -> Surface

    try:
        name = item["lookup-png-url"]
        if sys.platform == 'emscripten':
            import platform
            from pathlib import Path
            pth = Path(name)
            r_content = b''
            async with platform.fopen(pth, "rb") as binfile:
                r_content = binfile.read()
            img = io.BytesIO(r_content)
            imgsurf = pygame.image.load(img) # -> Surface
        else:
            import requests
            import io
            r = requests.get(name)
            png = io.BytesIO(r.content)
            pngsurf = pygame.image.load(png) # -> Surface
    except Exception as err:
        pngsurf = None

    if pngsurf is None:
        name = "data/sprint-o-matic-map-image-example-main/" + item["lookup-png-url"].rsplit('/', 1)[-1].rsplit('?', 1)[0]
        img = os.path.join(getPackagePath(), name)
        pngsurf = pygame.image.load(img) # -> Surface

    return imgsurf, pngsurf


async def downloadSoundBasedOnUrl(name):
    sound = None
    try:
        if sys.platform == 'emscripten':
            import platform
            from pathlib import Path
            pth = Path(soundUrl + name)
            r_content = b''
            async with platform.fopen(pth, "rb") as binfile:
                r_content = binfile.read()
            snd = io.BytesIO(r_content)
            sound = pygame.mixer.Sound(snd) # -> Sound
        else:
            import requests
            import io
            r = requests.get(soundUrl + name)
            snd = io.BytesIO(r.content)
            sound = pygame.mixer.Sound(snd) # -> Sound
    except Exception as err:
        sound = None
    return sound
