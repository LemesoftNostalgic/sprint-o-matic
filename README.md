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

* [Sprint-O-Matic 4.0: new "AMaze" feature to practice the first-control problem](https://youtu.be/nepM0oAiFn8)
* [Sprint-O-Matic 3.0: faster, webapp, hundreds of sprint orienteering maps all around the world](https://youtu.be/lmbBzbUQUbc)
* [Sprint-O-Matic early prototype, generated map, pacemaker mode, treadmill stunt](https://youtu.be/VikFxwu9e0Q).
* [Trying out Sprint-O-Matic route analysis mode with a fantasy map](https://youtu.be/rI9zinYGOmc)
* [Using a real sprint orienteering map with Sprint-O-Matic. Fast mode.](https://youtu.be/Kn53WGpEUgo)

I have high hopes that exercising with the application will improve the
sprint orienteering skills for beginners, and even for seasoned runners.
Unfortunately, I don't yet have evidence other than my own results,
which have improved a little bit during this winter.

## Table of Contents

  * [Installation](#installation)
  * [Usage](#usage)
  * [Adding new maps to Sprint-O-Matic](#adding-new-maps-to-sprint-o-matic)
  * [Software developent and license](#software-developent-and-license)
  * [Misc topics](#misc-topics)
  * [Command-line usage](#command-line-usage)

## Installation

### Web application

Use the web version if you want to try the application quickly, or you are using a MacBook. It might also work with a tablet, if you have a Bluetooth mouse paired with the tablet. The web version is not a full version, for example the sounds are awful and there is smaller amount of maps, but it gives you an idea what the application is like.
You may need to restart the browser, if the app does not start properly.

  * [Web application starts here](https://lemesoftnostalgic.github.io/sprint-o-matic/)

### Windows

[Windows installation](/WINDOWS.md)

### Linux

[Linux installation](/LINUX.md)

### MacBook

[MacBook installation](/MACBOOK.md)

### Hardware requirements

The application has been tested against Ubuntu 20.04 and
Windows 10. The web version requires a relatively modern browser.
Using the **--accurate** command-line parameter requires relatively modern
Linux PC due to
its search algorithms that run in separate processes.

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
parameter **--analysis** when starting the application. Use also **--accurate** parameter, if you have a fast Linux PC and you want the shortest-route finder to
be more accurate.

The graphical analysis result looks like this:

![Sprint-O-Matic Analysis result by Jyrki Leskela](/doc/Analysis.png)

### Pacemaker mode

![Sprint-O-Matic gameplay in pacemaker mode by Jyrki Leskelä](/doc/GeneratedMapWithPacemaker.png)

In the pacemaker mode, you complete the track together with a pacemaker,
your personal virtual coach. The pacemaker waits you at each control,
and competes against/with you in between the controls.

### A Maze

![Sprint-O-Matic gameplay in a maze mode by Jyrki Leskelä](/doc/AMaze.png)

In the A Maze -mode, you exercise the 1st control challenge. You get five maps with only the first control shown. You have 10 seconds to turn the map in
the best running direction.

After 10 seconds, you get the verdict, and the Sprint-O-Matic proposal
for the best direction.

### Map types (World series / Infinite Oulu / External)

There are three different categories of maps in Sprint-O-Matic.

**Infinite Oulu** is an automatically generated city-block-map, different map every time. The Infinite Oulu is also an internal system of the Sprint-O-Matic application.

![Sprint-O-Matic gameplay with a Barcelona map by Jyrki Leskelä](/doc/Barcelona.png)

**World sprint maps** is available from Sprint-O-Matic v2.0.0 onwards. It is a growing collection of hand-picked sprint orienteering maps from the best cityscapes all around the world. From Oulu to Helsinki, Tokio to Paris, I've got you covered. The initial numbers are 72 cities and 662 maps, and it is expected to grow fast. The World sprint maps is also an automatic system internally using Map data from OpenStreetMap. You don't have to do to anything to get more maps. In fact, you can propose a city or a coordinate with a simple e-mail to sprint.o.matic at gmail.com.

![Sprint-O-Matic gameplay map with an external map by Jyrki Leskelä](/doc/tartu/ExternalMapWithRouteAnalysis.png)

The Sprint-O-Matic can also link to **external** maps. All you have to do is to send necessary details of a map to sprint.o.matic at gmail.com. If the license of the map is permissive enough, I will then list it at [https://github.com/LemesoftNostalgic/sprint-o-matic-external-map-links](https://github.com/LemesoftNostalgic/sprint-o-matic-external-map-links) and it will become playable. I can even grant some teams a permission to maintain their own list of maps, if there is interest. The application checks the lists every time it starts, and shows the map selection one-by-one when user toggles the "external/team" and "external/map" buttons of the home screen. In the beginning there is one example team with some maps already. I hope more is coming.

See the following chapter for the data that is needed, to make a map playable in Sprint-O-Matic.

## Adding new maps to Sprint-O-Matic

There are two ways to provide maps so Sprint-O-Matic:

- Find an interesting place from e.g. Google Maps and send a hint about it to sprint.o.matic at gmail.com.
- Use a real sprint orienteering map with the Sprint-O-Matic: [Guide of using maps with Sprint-O-Matic](/README-MAPS.md)

## Software developent and license

The application internals are written in python, using the pygame library.
It is a hobby project, so the quality is perhaps at the level of a casual indie
game.

The software is licensed under Apache-2.0 license. You are therefore free to
branch it for extra development or propose pull requests for it.

The following ideas are next on the table:

* more maps to the map listing [using this procedure](/README-MAPS.md)
* Gradient slow terrain, for better modeling of staircases and hills
* Add control numbering, control descriptions, etc.
* Graphics beautification
* Score-O mode (collect contols with score in any order, time limit)
* Allow creation of hand-crafted track designs for a given map
* events/multiplayer support (might have to be a paid subcription to cover the
server costs)

A bit more involved:

* Automatic creation of terrain descriptions, making [this procedure](/README-MAPS.md) easier.
* 3d mode

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

### About the author

You may wonder about LemesoftNostalgic, the nickname of this github account.
I used to develop games for 8-bit computers in the
80's, using a pseudonym Lemesoft. At the present day, there exists at least one
Lemesoft (company) in Spain so I chose a new alias LemesoftNostalgic for this
hobby project, to avoid the name conflict.

I also live, work, sleep, and exercise.
there is no infinite time for hobby programming. If you
find some bugs or awkward programming patterns, it is probably due to
the scarcity of time more than anything else. I still try to be awake
regarding the biggest issues, if reported to the sprint.o.matic at gmail.com.

### About the track generator

By default, the Sprint-O-Matic generates a new track for every run.
Usually the tracks are decent, but not every time. If you happen to get a
poor track, just hit the esc-button and start again. There is no good
reason to run without a proper track.

### Advisory: Usage of interactive applications while running in a treadmill

The Sprint-O-Matic is an interactive application similar to games.
Warning: the Sprint-O-Matic has not been properly tested for safety regarding
the treadmill use. If you do it, please consider it is not one of the
planned use-cases of the software.

### Support

Map proposals, team proposals, and application improvement
ideas can be sent to sprint.o.matic at gmail.com.

## Command-line usage

For the advanced users, there are more detailed options in the form of
command-line options.

It is also possible to play either fullscreen or in a window.

**--fullScreen** Whether to play fullscreen, yes or no.

Route analyses.

**--analysis** Whether to write the route analyses into a file. yes or no.

**--accurate** Use the slow but a bit more accurate route analysis, Linux only. yes or no.

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
