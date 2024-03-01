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
from .utils import getPackagePath


listingOfTeamsWithListing = "https://raw.githubusercontent.com/LemesoftNostalgic/sprint-o-matic-external-map-links/main/teams-hosting-their-own-map-listing.json"
listingOfMapsInCities = "https://raw.githubusercontent.com/LemesoftNostalgic/sprint-o-matic-external-map-links/main/world-city-maps.json"
newsUrl= "https://raw.githubusercontent.com/LemesoftNostalgic/sprint-o-matic-external-map-links/main/NEWS.txt"

offlineNews = "data/sprint-o-matic-external-map-links-main/NEWS.txt"
offlineTeamsWithListing = "data/sprint-o-matic-external-map-links-main/teams-hosting-their-own-map-listing.json"
offlineMapsInCities = "data/sprint-o-matic-external-map-links-main/world-city-maps.json"

offlineExamplePath = "data/sprint-o-matic-map-image-example-main"

async def downloadNews():
    news = ""
    try:
        import requests
        import io
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
        import requests
        import io
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
        import requests
        import io
        if ownMasterListing:
            response = requests.get(ownMasterListing)
        else:
            response = requests.get(listingOfTeamsWithListing)
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
        import requests
        import io
        name = item["map-url"]
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
        import requests
        import io
        name = item["lookup-png-url"]
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
