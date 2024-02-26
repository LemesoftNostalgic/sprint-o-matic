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
import requests
import io


listingOfTeamsWithListing = "https://raw.githubusercontent.com/LemesoftNostalgic/sprint-o-matic-external-map-links/main/teams-hosting-their-own-map-listing.json"

listingOfMapsInCities = "https://raw.githubusercontent.com/LemesoftNostalgic/sprint-o-matic-external-map-links/main/world-city-maps.json"

newsUrl= "https://raw.githubusercontent.com/LemesoftNostalgic/sprint-o-matic-external-map-links/main/NEWS.txt"

def downloadNews():
    news = ""
    try:
        response = requests.get(newsUrl)
        news = response.text
    except Exception as err:
        print(f"Cannot load news: {err=}, {type(err)=}")
    return news


def downloadExternalWorldCityMap():
    try:
        response = requests.get(listingOfMapsInCities)
        data = response.text
        listingofmaps = json.loads(data)
    except Exception as err:
        print(f"Cannot load listing of map coords in cities: {err=}, {type(err)=}")
        return []
    return listingofmaps


def downloadExternalImageData(ownMasterListing):

    try:
        if ownMasterListing:
            response = requests.get(ownMasterListing)
        else:
            response = requests.get(listingOfTeamsWithListing)
        data = response.text
        listingofteams = json.loads(data)
    except Exception as err:
        print(f"Cannot load listing of teams hosting maps: {err=}, {type(err)=}")
        return []

    returndata = []
    for team in listingofteams:
        teamMapListingUrl = team["map-listing-url"]
        teamdata = None

        try:
            response = requests.get(teamMapListingUrl)
            data = response.text
            teamdata = json.loads(data)
        except Exception as err:
            print(f"Cannot load map listing: {err=}, {type(err)=}")
            pass

        if teamdata is not None:
            team["sub-listing"] = teamdata
            returndata.append(team)

    return returndata

def downloadMapSurfacesBasedOnUrl(item):

    imgsurf = None
    pngsurf = None

    try:
        name = item["map-url"]
        r = requests.get(name)
        img = io.BytesIO(r.content)
        imgsurf = pygame.image.load(img) # -> Surface
    except Exception as err:
        print(f"Cannot load image {name=}: {err=}, {type(err)=}")
        pass

    try:
        name = item["lookup-png-url"]
        r = requests.get(name)
        png = io.BytesIO(r.content)
        pngsurf = pygame.image.load(png) # -> Surface
    except Exception as err:
        print(f"Cannot load image {name=}: {err=}, {type(err)=}")
        pass

    return imgsurf, pngsurf
