# Sprint-O-Matic

![Sprint-O-Matic logo by Jyrki Leskela](/doc/logo.png)

## Introduction

Sprint-O-Matic is a training application for sprint orienteering or
Sprint-O for short.
I created it initially for my own pleasure, and to give some variety to my
exercise during cold winter days in Finland. After a while, it came to my
mind that someone else might be interested to try it out, so here it is.

What then is sprint orienteering? It is a fast paced foot navigation
sport arranged usually in urban environments. More description can be found
from the [Wikipedia article on sprint orienteering](https://en.wikipedia.org/wiki/Orienteering#Sprint) or [sprint orienteering content in YouTube](https://www.youtube.com/results?search_query=sprint+orienteering).

The discipline of sprint orienteering requires not only the running speed
but ability to rapidly choose the best route from one control to another.
This is the place where the Sprint-O-Matic comes into the picture.
It provides you an infinite number of sprint orienteering route selection challenges in a
form of an entertaining 2D game. See the following YouTube videos to get an
idea:

* [Sprint-O-Matic early prototype, generated map, pacemaker mode, treadmill stunt](https://youtu.be/VikFxwu9e0Q).
* [Trying out Sprint-O-Matic route analysis mode with a fantasy map](https://youtu.be/rI9zinYGOmc)
* [Using a real sprint orienteering map with Sprint-O-Matic. Fast mode.](https://youtu.be/Kn53WGpEUgo)

## Table of Contents

  * [Installation](#installation)
  * [Usage](#usage)
  * [Linking external maps to Sprint-O-Matic](#linking-external-maps-to-sprint-o-matic)
  * [Software developent and license](#software-developent-and-license)
  * [Misc topics](#misc-topics)
  * [Command-line usage](#command-line-usage)

## Installation

The [Release folder](https://github.com/LemesoftNostalgic/sprint-o-matic/releases/latest) contains pre-built applications for Linux and Windows.
The application can also be run directly from source code if python and
the packages listed below are installed.

As of writing, the application has been verified against Ubuntu 20.04 and
Windows 10. Running the Sprint-O-Matic requires relatively modern PC due to
its search algorithms that run in separate processes.

The application can sometimes be a little bit unresponsive on the way to the
first control especially in Windows environment. That is caused mostly by
the garbage collection of Python programming language, so there is not much
I can do about it. The lag, if any, should stabilize later in the course.

In addition to the ready-built binaries, it is also quite easy to build
the application from sources using dopyinstaller.sh (Linux) or
dopyinstaller.bat (Windows) at the root folder of this repository.
Requirements for the build:

1. python3.10 (python.org/Downloads)
2. pygame (python -m pip install pygame)
3. matplotlib (python -m pip install matplotlib)
4. argparse (python -m pip install argparse)
5. picle (python -m pip install picle)
6. requests (python -m pip install requests)
7. pyinstaller (python -m pip install pyinstaller)


In case the ready-built Windows package gives false virus alarms, like it sometimes does with
pyinstaller-built applications, you can also just install the correct
python version (actually Python3.12 worked fine in Windows) and the other
listed requirements, download the source code, and click the python program
icon (main.py) from the src folder of the source code.

Later on there might be also an Android version. If anyone is interested in
debugging the Android build, be my guest.
The current attempt of a buildozer script dobuildozer.sh is at the root
folder of this repository. It currently stops at the following error:
src_c/_sdl2/sdl2.c:211:12: fatal error: 'longintrepr.h' file not found.

## Usage

### Home screen

![Sprint-O-Matic Home Screen by Jyrki Leskela](/doc/InitialDisplay.png)

The first thing you see when you start the application is the home screen.
It allows for the basic setting of track and leg length, play modes and map selection. The home screen can be used from keyboard (arrow keys to move the blue pointer, enter/space to select, esc to exit) or
with a mouse (left/right button to move the blue pointer and middle button to select. The mouse usage might sound unintuitive, but I want to be able to use the application when the mouse is not at the desk surface.

When you have selected all the settings, move the blue pointer to the finish circle and select it. The game you just configured will then begin.

### Gameplay

The keys and buttons for the gameplay are similar to those in the home screen: Arrow keys or mouse buttons to turn left or right, esc or middle button to quit. The usage is intentionally as straightforward as possible.

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

### Pacemaker mode

![Sprint-O-Matic gameplay in pacemaker mode by Jyrki Leskelä](/doc/GeneratedMapWithPacemaker.png)

In the pacemaker mode, you complete the track together with a pacemaker,
your personal virtual coach. The pacemaker waits you at each control,
and competes against/with you in between the controls.

In some rare circumstances, the pacemaker decides to skip a control,
and wait at the next one. In that case, don't worry. Shit happens.

### Map types (Infinite Oulu / External)

There are two different categories of maps in Sprint-O-Matic.

**Infinite Oulu** is an automatically generated city-block-map, different map every time. The Infinite Oulu is an internal system of the Sprint-O-Matic application. See the previous image for an example.

![Sprint-O-Matic gameplay map with an external map by Jyrki Leskelä](/doc/tartu/ExternalMapWithRouteAnalysis.png)

The Sprint-O-Matic can also link to **external** maps. All you have to do is to send necessary details of a map to sprint-o-matic at gmail com. If the license of the map is permissive enough, I will then list it at [https://github.com/LemesoftNostalgic/sprint-o-matic-external-map-links](https://github.com/LemesoftNostalgic/sprint-o-matic-external-map-links) and it will become playable. I can even grant some teams a permission to maintain their own list of maps, if there is interest. The application checks the lists every time it starts, and shows the map selection one-by-one when user toggles the "external/team" and "external/map" buttons of the home screen. In the beginning there is one example team with some maps already. I hope more is coming.

See the following chapter for the data that is needed, to make a map playable in Sprint-O-Matic.

## Linking external maps to Sprint-O-Matic

To link an external map for the Sprint-O-Matic listing, some information
regarding the map is needed:

- name, short one to fit it in the home screen
- url-link to an image of the map (png format is encouraged)
- license information for the map
- credit text for the owner/creator of the map
- url to a terrain description (equally sized png image as the map)
- license information for the terrain description
- credit text for the owner/creator of the terrain description
- meters-per-pixel factor

Here is an example of an entry in the [https://github.com/LemesoftNostalgic/sprint-o-matic-external-map-links](https://github.com/LemesoftNostalgic/sprint-o-matic-external-map-links):

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
    }
   ```

The two main things to pay attention is a) license of the map and b) creating the terrain description e.g "lookup-png".

a) Regarding the license, it is only possible to include map images
with relatively permissive license to the listing. In practice, the map
image will become visible to all the Sprint-O-Matic users when included.
The best way would be to license an
image of a candidate map with one of the creative commons license types.
This will probably limit the selection to older maps that have no more use
for live sprint orienteering events. For me, that sounds a good trade-off.

There is also a way to use the app with your private maps.
In that case you have to rely on the command line options, and keep the
map content in your own computer.

b) A bit more involved is the creation of the terrain description
e.g. "lookup-png".
Basically, you have to create equally sized image as the map image.
One easy method is to make a copy of the original map image, re-paint
each terrain type with a correct color code and save the result as png.

The color codes are the following:

![Sprint-O-Matic logo by Jyrki Leskelä](/doc/lookupcolors.png)

Please use an editor where you can choose the colors accurately. The
terrain markings must represent exactly the color codes shown in the image
above. Then you need to review the edits. Especially the black color of
sprint map notation is
difficult: usually it marks an area that you cannot run through,
but some black features such as forest paths and fence symbol
slashes are actually runnable, so do not mark them forbidden.

See the [examples repository](https://github.com/LemesoftNostalgic/sprint-o-matic-map-image-example) for some examples of a map image and the
corresponding terrain description. I have also [a YouTube video showing
how to do the edits with GIMP](https://youtu.be/_n0IRG1GfLI).
The best working resolutions for map images and terrain descriptions are
between 1024-2048 pixels (width). The game engine is designed for
sprint map scales approximately from 1:3000 to 1:5000.

If you have an excellent map you wish to be included, but have no time or
skills to create the terrain description, please propose it via sprint-o-matic
at gmail com anyway. I can create a couple of terrain images myself as a
pro-bono effort to get things rolling. A good map for Sprint-O-Matic is
one that has enough fences and other obstacles to pose a challenge.
Also slow green terrain is good but not mandatory.


## Software developent and license

The application internals are written in python, using the pygame library.
It is a hobby project, so the quality is at the level of a casual indie
game. However, there is a hidden automatic test suite that can be
activated from the home screen by typing "autotest". I run it every now and
then to catch the biggest issues, you can do it too, and report issues in
sprint-o-matic at gmail com.

The software is licensed under Apache-2.0 license. You are therefore free to
branch it for extra development or propose changes under the terms of the
license. Due to the nature of a hobby
project, all help is appreciated. An initial wishlist is the following:

Low hanging fruits:

* more external maps linked to the map listing (see above)
* Allow publication of a set of fixed track designs for a map
* Android (buildozer spec exists, does not fully work yet)
* gradient slow terrain, for better modeling of staircases and hills
* marking for sheds and tunnels, so that you can run under the surface
* graphics beautification
* Score-O mode (collect contols with score in any order, time limit)

A bit more involved:

* events/multiplayer support (might have to be a paid subcription to cover the
server costs)
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
command-line options. These are not as well tested and the home screen.

These options are useful if you want to play with your own map:

**--mapFileName** sprint orienteering map, png format

**--lookupPngName** pre-calculated terrain description for the map, png format

**--metersPerPixel** How many meters per map pixel

These are similar options that you can activate from the home screen,
with a bit more detail:

**--trackLength** the minimum track length in meters

**--miniLegProbability** probability of mini legs (0.0-0.99)

**--shortLegProbability** probability of short legs (0.0-0.99)

**--mediumLegProbability** probability of medium length legs (0.0-0.99)

**--longLegProbability** probability of long legs (0.0-0.99)

**--extraLongLegProbability** probability of extra long legs (0.0-0.99)

**--continuous** Continuous game loop (or one-shot play)

**--pacemaker** A pacemaker runner to compete against (1-3, 0 for none)

And in case you want to maintain your own routes or map listings:

**--routeFileName** pickled ordered list of tuples (track control points)

**--ownMasterListing** Override the default web listing with other URL

**--externalExampleTeam** The team selection from the listing

**--externalExample** The map selection from the listing


It is also possible to write the route analyses to a file:

**--analysis** Whether to write the route analyses into a file


There are also some other options that are mainly for application
testing. They are documented only in the code.
