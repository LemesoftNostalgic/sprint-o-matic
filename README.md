# Sprint-O-Matic

![Sprint-O-Matic logo by Jyrki Leskela](/doc/logo.png)

## Introduction

_Linkki suomenkieliseen ohjeeseen_: [README-FINNISH.md](/README-FINNISH.md).

Sprint-O-Matic is a training application for sprint orienteering, or
Sprint-O for short.
I created it initially for my own use, to give some variety to my
exercise during cold winter days in Finland. After a while, it came to my
mind, that someone else might be interested to try it out, so here it is.

What then is sprint orienteering? It is a fast paced foot navigation
sport arranged usually in urban environments. More description can be found
from the [Wikipedia article on sprint orienteering](https://en.wikipedia.org/wiki/Orienteering#Sprint) or [sprint orienteering content in YouTube](https://www.youtube.com/results?search_query=sprint+orienteering).

The discipline of sprint orienteering requires, not only the running speed,
but the ability to rapidly choose the best route from one control to another.
This is the place where the Sprint-O-Matic comes into the picture.
It provides you an infinite number of sprint orienteering route selection challenges, in a
form of an entertaining 2D game. See the following YouTube videos to get an
idea:

* [Sprint-O-Matic 2.0: hundreds of sprint orienteering maps all around the world](https://youtu.be/lmbBzbUQUbc)
* [Sprint-O-Matic early prototype, generated map, pacemaker mode, treadmill stunt](https://youtu.be/VikFxwu9e0Q).
* [Trying out Sprint-O-Matic route analysis mode with a fantasy map](https://youtu.be/rI9zinYGOmc)
* [Using a real sprint orienteering map with Sprint-O-Matic. Fast mode.](https://youtu.be/Kn53WGpEUgo)

## Table of Contents

  * [Installation](#installation)
  * [Usage](#usage)
  * [Adding new maps to Sprint-O-Matic](#adding-new-maps-to-sprint-o-matic)
    * [Playing with your private maps](#playing-with-your-private-maps)
    * [Make your map visible to Sprint-O-Matic users](#make-your-map-visible-to-sprint-o-matic-users)
    * [Creating the terrain description](#creating-the-terrain-description)
  * [Software developent and license](#software-developent-and-license)
  * [Misc topics](#misc-topics)
  * [Command-line usage](#command-line-usage)

## Installation

The recommended method is to run the software with python, directly from
source code, because it is easy and safe:

1. Download and unzip the source code package from the [Release folder](https://github.com/LemesoftNostalgic/sprint-o-matic/releases/latest) to your machine
2. Install python3.10 or higher: (python.org/Downloads)
  * In the python installer package, ensure that python is set to path variable, by allowing environment variable modifications
3. Install the required python modules from command prompt
  * python -m pip install pygame
  * python -m pip install requests
  * python -m pip install argparse
  * python -m pip install overpy (sprint-o-matic v2.0.0 onwards)

4. Start the "main.py" from sprint-o-matic folder of sprint-o-matic (click the "main" icon or use command "python main.py" from the command line)
  * or use command "python main.py --fullScreen yes" if you want to play in a fullscreen mode.

The [Release folder](https://github.com/LemesoftNostalgic/sprint-o-matic/releases/latest) contains also pre-built applications for Linux and Windows as executables. The Windows PyInstaller executable is not signed by Microsoft, but I followed the [microsoft answer for cases when Pyinstaller-created executable is incorrectly flagged](https://answers.microsoft.com/en-us/windows/forum/all/where-executables-created-by-pyinstaller-are-being/09e58a6b-01f3-4e72-8765-6542ef7291f4).

If you really want, you can re-build the executables
from sources using dopyinstaller.sh (Linux) or dopyinstaller.bat (Windows)
that are provided with the source code. The usage requires the installation
of pyinstaller:

* python -m pip install pyinstaller
  * Ensure that the pyinstaller is in your PATH.

### Hardware requirements

The application has been tested against Ubuntu 20.04 and
Windows 10. Running the Sprint-O-Matic requires relatively modern PC due to
its search algorithms that run in separate processes. There may be some
lag on the way to the first control, as it often is the case with real life
orienteering, but that lag should settle later on.

The World series maps take a while to start, sometimes even half a minute
or so. The time is well spent on map data downloading and track rendering. 

## Usage

### Home screen

![Sprint-O-Matic Home Screen by Jyrki Leskela](/doc/InitialDisplay.png)

The first thing you see, when you start the application, is the home screen.
It allows for the basic setting of track and leg length, play modes, and map selection. The home screen can be used from keyboard (arrow keys to move the blue pointer, enter/space to select, esc to exit), or
with a mouse (left/right button to move the blue pointer and middle button to select. The mouse usage might sound unintuitive, but I want to be able to use the application when the mouse is not at the desk surface.

When you have selected all the settings, move the blue pointer to the finish circle and select it. The game you just configured will then begin.

### Gameplay

The gameplay keys are similar to the home screen keys: Arrow keys or mouse buttons to turn left or right, esc or middle button to quit. The usage is intentionally simlified.

![Sprint-O-Matic gameplay with a fantasy map by Jyrki Leskela](/doc/ExternalFantasyMap.png)

### Route analysis modes (repeat, once, fast)

In any of the route analysis modes, you proceed from control to control individually.
When you reach a control, your route is shown briefly, together with the
most optimal route that the application was able to find.

At the end of the track, some statistics such as time, length and excess
distance in percentage is shown. There are three different route analysis
modes to choose from:

* repeat: loop random tracks with the same map over and over again
* once: run the track once and return to the home screen
* fast: doubles the runner speed to give a little bit more challenge

It is also possible to get the analysis results as a file to your disk,
after the session. This requires using the [command line](#command-line-usage)
parameter **--analysis** when starting the application.

The graphical analysis result looks like this:

![Sprint-O-Matic Analysis result by Jyrki Leskela](/doc/Analysis.png)

### Pacemaker mode

![Sprint-O-Matic gameplay in pacemaker mode by Jyrki Leskelä](/doc/GeneratedMapWithPacemaker.png)

In the pacemaker mode, you complete the track together with a pacemaker,
your personal virtual coach. The pacemaker waits you at each control,
and competes against/with you in between the controls.

In some rare circumstances, the pacemaker decides to skip a control,
and wait at the next one. In that case, don't worry. Shit happens.

### Map types (World series / Infinite Oulu / External)

There are three different categories of maps in Sprint-O-Matic.

**Infinite Oulu** is an automatically generated city-block-map, different map every time. The Infinite Oulu is also an internal system of the Sprint-O-Matic application. See the previous image for an example.

![Sprint-O-Matic gameplay with a Barcelona map by Jyrki Leskelä](/doc/Barcelona.png)

**World sprint maps** is available from Sprint-O-Matic v2.0.0 onwards. It is a growing collection of hand-picked sprint orienteering maps from the best cityscapes all around the world. From Oulu to Helsinki, Tokio to Paris, I've got you covered. The initial numbers are 72 cities and 662 maps, and it is expected to grow fast. The World sprint maps is also an automatic system internally using Map data from OpenStreetMap. You don't have to do to anything to get more maps.

![Sprint-O-Matic gameplay map with an external map by Jyrki Leskelä](/doc/tartu/ExternalMapWithRouteAnalysis.png)

The Sprint-O-Matic can also link to **external** maps. All you have to do is to send necessary details of a map to sprint-o-matic at gmail com. If the license of the map is permissive enough, I will then list it at [https://github.com/LemesoftNostalgic/sprint-o-matic-external-map-links](https://github.com/LemesoftNostalgic/sprint-o-matic-external-map-links) and it will become playable. I can even grant some teams a permission to maintain their own list of maps, if there is interest. The application checks the lists every time it starts, and shows the map selection one-by-one when user toggles the "external/team" and "external/map" buttons of the home screen. In the beginning there is one example team with some maps already. I hope more is coming.

See the following chapter for the data that is needed, to make a map playable in Sprint-O-Matic.


## Adding new maps to Sprint-O-Matic

### Playing with your private maps

Using the [command line](#command-line-usage) parameters **--mapFileName** and **--lookupPngName** you can play with a map stored in your local filesystem. The map file is just an image of the map, preferably in png format, and the lookup file (i.e. terrain description) is an equally sized png image where the terrain characteristics are marked
with specific colors, see chapter [creating the terrain description](#creating-the-terrain-description).

### Make your map visible to Sprint-O-Matic users

Add a map to the Sprint-O-Matic's map listing, and everyone can play
with it. Some information regarding the map needs to be sent to the
sprint-o-matic gmail com to make the linkage happen:

- name, short one to fit it in the home screen
- url-link to an image of the map (png format is encouraged)
- license information for the map
- credit text for the owner/creator of the map
- url to a terrain description (equally sized png image as the map)
- license information for the terrain description
- credit text for the owner/creator of the terrain description
- meters-per-pixel factor
- default zoom factor

Here is an example of an entry in the [sprint-o-matic's current listing of external maps](https://github.com/LemesoftNostalgic/sprint-o-matic-external-map-links):

   ```json
    {
        "name": "Fantasy",
        "map-url": "https://raw.githubusercontent.com/LemesoftNostalgic/sprint-o-matic-map-image-example/main/FantasySprintMap.png?raw=true",
        "map-license": "CC BY-SA 4.0 Deed",
         "map-credits": "Jyrki Leskelä, 2024",
         "lookup-png-url": "https://raw.githubusercontent.com/LemesoftNostalgic/sprint-o-matic-map-image-example/main/fantasylookup.png?raw=true",
         "lookup-png-license": "CC BY-SA 4.0 Deed",
         "lookup-png-credits": "Jyrki Leskela, 2024",
         "meters-per-pixel": 0.5
         "default-zoom": 1.0
    }
   ```

**Hint:** If you don't know how to publish files in the web to get an
URL of the map: an easy way to do that is to [open a free account and
repository in the GitHub](https://github.com/signup) and drag the files there.
Sprint-o-Matic gmail com understands github repository names so you don't have
to give the precise URL in that case.

The two other things to pay attention is a) license of the map and b) creating the terrain description e.g "lookup-png".

a) Regarding the license, it is only possible to include map images
with relatively permissive license to the listing. In practice, the map
image will become visible to all the Sprint-O-Matic users when included.
The best way would be to license an
image of a candidate map with one of the creative commons license types.
This will probably limit the selection to older maps that have no more use
for live sprint orienteering events. For me, that sounds a good trade-off.

b) A bit more involved is the creation of the terrain description
e.g. "lookup-png". The following subchapter tells how to do that.

### Creating the terrain description

Basically, you have to create equally sized image as the map image.
One easy method is to make a copy of the original map image, re-paint
each terrain type with a correct color code and save the result as png.

The color codes are the following:

![Sprint-O-Matic lookup colors by Jyrki Leskelä](/doc/lookupcolors.png)

Please use an editor where you can choose the colors accurately.
I have used [GIMP](https://www.gimp.org) because I am familiar with it. The
terrain markings must represent exactly the color codes shown in the image
above. Then you need to review the edits. Pay attention to the black color of
sprint map notation: usually it marks an area that you cannot run through,
but some black features such as forest paths and fence symbol
slashes are actually runnable, so do not mark them forbidden.

See the [examples repository](https://github.com/LemesoftNostalgic/sprint-o-matic-map-image-example) for some examples of a map image and the
corresponding terrain description. I have also [a YouTube video showing
how to do the edits with GIMP](https://youtu.be/_n0IRG1GfLI).
The best working resolutions for map images and terrain descriptions are
between 1024-1280 pixels (width). The game engine is designed for
sprint map scales approximately from 1:3000 to 1:5000.

If you have an excellent map you wish to be included, but have no time or
skills to create the terrain description, please propose it via sprint-o-matic
at gmail com anyway. I can create a couple of terrain images myself as a
pro-bono effort to get things rolling. A good map for Sprint-O-Matic is
one that has enough fences and other obstacles to pose a challenge.
Also slow green terrain is good but not mandatory.


## Software developent and license

The application internals are written in python, using the pygame library.
It is a hobby project, so the quality is perhaps at the level of a casual indie
game.

The software is licensed under Apache-2.0 license. You are therefore free to
branch it for extra development or propose pull requests for it.
Due to the nature of a hobby project, all help is of course appreciated.
An initial to-do list is the following:

Low hanging fruits:

* more external maps linked to the map listing (see above)
* Allow publication of hand-crafted track designs for a given map
* Android (the current attempt of a buildozer script dobuildozer.sh is at the root folder of this repository. It currently stops at the following error: src_c/_sdl2/sdl2.c:211:12: fatal error: 'longintrepr.h' file not found.)
* Web application with pygbag (might have to be a lightweight version)
* gradient slow terrain, for better modeling of staircases and hills
* Add control numbering, control descriptions, etc.
* graphics beautification
* Score-O mode (collect contols with score in any order, time limit)
* events/multiplayer support (might have to be a paid subcription to cover the
server costs)

A bit more involved:

* automatic creation of terrain descriptions. With sprint orienteering maps,
the black color is a problem. It is used for symbols that you can run through
and symbols that you can't run through. There is even some variation from map
to map, which makes it difficult for a computer program to determine the
meaning of the markings.
* 3d (human eye is more sensitive to quality when the content is 3d,
therefore this requires more polishing than 2d)
* Integration to a geographical database. Exercise "everywhere".


## Misc topics

### About the player characters

The pixelated runners of the game may look tiny, but if you think
about the scale of the maps, one meter per pixel in the
"infinite Oulu" map, for example, you get the picture. The runners are actually
5-7 meter tall monsters. But there is a story.

The runners are living in a distant future, an era where people spend their
time in virtual environments. In this dystopian world, things have gone
south, and the government
has started to ration the amount of pixels allowed for the regular citizen.
Most of them have responded by growing their avatars bigger in size.
The maximum size of the avatar, according to the law, is 7 meters.

**Sprint-O-Man** The key character of the application, blue giant
passionate on sprint orienteering. Thinks his genes are half cowboy,
half Native American.

**Aino Inkeri (A.I.) Kiburtz** A pacemaker, and an a proud artificial
intelligence loosely based on the ancient documentation found on
Matthias Kiburtz, a distinguished sprint orienteer.
The best friend of Sprint-O-Man.

**Pertti-Uolevi (P.A.) Keinonen, e.v.v.k.** A pacemaker, and an avant-garde
heavy metal afictionado, named after the best known heavy metal guitarist
from the golden age of the genre, the one and only, Pertti Keinonen, RIP.

**Lex Martin Luthoer, Chem. Engr.** A pacemaker, and an extremely vivid
runner. The most controversial figure due to his specialty in chemical
engineering. Under suspicion on doping, but never got caught.

### About the creator of this application

You may wonder about LemesoftNostalgic, the nickname of this github account.
I used to develop games for 8-bit computers in the
80's, using a pseudonym Lemesoft. At the present day, there exists at least one
Lemesoft (company) in Spain so I chose a new alias LemesoftNostalgic for this
hobby project, to avoid the name conflict.

I also live, work, sleep, and exercise.
there is no infinite time for hobby programming. If you
find some bugs or awkward programming patterns, it is probably due to
the scarcity of time more than anything else. I still try to be awake
regarding the biggest issues, if reported to the sprint-o-matic gmail com.

### About the track generator

By default, the Sprint-O-Matic generates a new track for every run.
Usually the tracks are decent, but not every time. If you happen to get a
poor track, just hit the esc-button and start again. There is no good
reason to run without a proper track.

### Advisory: Usage of interactive applications while running in a treadmill

The Sprint-O-Matic is an interactive application similar to games.
Warning: the Sprint-O-Matic has not been properly tested for safety regarding
the treadmill use. Therefore I have to advice against it, even though it is
technically possible with a wireless mouse. Please inform me via sprint-o-matic
at gmail com if your treadmill vendor shows green light for this use-case.

### Support

Map proposals, team proposals, and application improvement
ideas can be sent to sprint-o-matic at gmail com.

## Command-line usage

For the advanced users, there are more detailed options in the form of
command-line options.

It is also possible to play either fullscreen or in a window.

**--fullScreen** Whether to play fullscreen, yes or no.

It is also possible to write the route analyses to a file.

**--analysis** Whether to write the route analyses into a file

These options are useful if you want to play with your own map.
When using them, you don't go to the home screen, but the game starts
immediately:

**--mapFileName** sprint orienteering map, png format

**--lookupPngName** pre-calculated terrain description for the map, png format

**--metersPerPixel** How many meters per map pixel

And since you don't go to the home screen when using your own map file,
there are command line parameters for the options that you would
normally toggle in the in the home screen,
just a bit more detailed:

**--trackLength** the minimum track length in meters

**--miniLegProbability** probability of mini legs (0.0-0.99)

**--shortLegProbability** probability of short legs (0.0-0.99)

**--mediumLegProbability** probability of medium length legs (0.0-0.99)

**--longLegProbability** probability of long legs (0.0-0.99)

**--extraLongLegProbability** probability of extra long legs (0.0-0.99)

**--continuous** Continuous game loop (or one-shot play)

**--pacemaker** A pacemaker runner to compete against (1-3, 0 for none)

And in case you want to design a specific route:

**--routeFileName** ordered list of tuples (control point coordinates) in json

And finally, if you want to host your private map listing.

**--ownMasterListing** Override the default web listing with other URL

**--externalExampleTeam** The team selection from the listing

**--externalExample** The map selection from the listing

There are also some other options that are mainly for application
testing. They are documented only in the code.
