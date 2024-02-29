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
import os
from random import randrange

stepsChannelNumber = 0
effectChannelNumber = 1
birdsChannelNumber = 2
melodyChannelNumber = 3
stepsChannel = None
effectChannel = None
birdsChannel = None
melodyChannel = None


soundPath = "21608__ali_6868__gravel-footsteps"
leftSteps = [
    "384873__ali_6868__left-gravel-footstep-1.ogg",
    "384871__ali_6868__left-gravel-footstep-2.ogg",
    "384872__ali_6868__left-gravel-footstep-3.ogg",
    "384875__ali_6868__left-gravel-footstep-4.ogg",
    "384874__ali_6868__left-gravel-footstep-5.ogg"
]
leftSounds = []

rightSteps = [
    "384877__ali_6868__right-gravel-footstep-1.ogg",
    "384876__ali_6868__right-gravel-footstep-2.ogg",
    "384879__ali_6868__right-gravel-footstep-3.ogg",
    "384878__ali_6868__right-gravel-footstep-4.ogg",
    "384880__ali_6868__right-gravel-footstep-5.ogg"
]
rightSounds = []

melodyPaths = [
    os.path.join("jackslay", "380848__jackslay__futuristic.ogg"),
    os.path.join("berdnikov2004", "641751__berdnikov2004__vibe-tracker-drum-loop-8-bit16-bit.ogg"),
    os.path.join("badoink", "519621__badoink__jazzloop_120_bpm.ogg"),
    os.path.join("bronxio", "239549__bronxio__drumloop-for-chaos-bass-no-hihat-4-bar-95-bpm-swing.ogg"),
    os.path.join("cgoulao", "431538__cgoulao__fiesta.ogg"),
    os.path.join("fran_ky", "350702__fran_ky__120-num-chrome-7.ogg"),
    os.path.join("furbyguy", "388101__furbyguy__90s-game-loop.ogg"),
    os.path.join("iykqic0", "253489__iykqic0__pringle-rhythm-industrial-ghost-echo-delay.ogg"),
    os.path.join("johaynes", "659527__johaynes__jos-genedrums-150bpm-43.ogg"),
    os.path.join("badoink", "547095__badoink__awesome-arp.ogg"),
    os.path.join("josefpres", "609809__josefpres__random-loop-001-simple-mix-120-bpm.ogg"),
    os.path.join("nomiqbomi", "579059__nomiqbomi__transist-4.ogg"),
    os.path.join("seth", "680840__seth_makes_sounds__homemade.ogg"),
    os.path.join("szymalix", "588569__szymalix__risemix.ogg"),
    os.path.join("the_loner", "705439__the_loner__weird_loop02.ogg")
    ]

melodySounds = []
melodyCtr = None

birdsPath = os.path.join("crk365", "38895__crk365__urban-birds.ogg")
birdsSound = None

shoutPath = os.path.join("craigsmith", "481757__craigsmith__r21-22-cowboy-shouts-at-cattle.ogg")
shoutSound = None

pacemakerShoutPath = os.path.join("craigsmith", "481757__craigsmith__r21-22-cowboy-shouts-at-cattle-truncated.ogg")
pacemakerShoutSound = None

finishPath = os.path.join("fupicat", "521645__fupicat__winfantasia.ogg")
finishSound = None

startPath = os.path.join("frodo89", "84456__frodo89__standard-beep-pre-start.ogg")
startSound = None

stepPath = os.path.join("21608__ali_6868__gravel-footsteps", "384873__ali_6868__left-gravel-footstep-1.ogg")
stepSound = None

left = False

def initSounds(soundRoot):
    global stepsChannel
    global birdsChannel
    global effectChannel
    global melodyChannel
    global melodyCtr
    global leftSounds
    global rightSounds
    global melodySounds
    global birdsSound
    global shoutSound
    global pacemakerShoutSound
    global startSound
    global stepSound
    global finishSound
    
    pygame.mixer.init()
    pygame.mixer.set_num_channels(4)

    for leftStep in leftSteps:
        leftSounds.append(pygame.mixer.Sound(os.path.join(soundRoot, soundPath, leftStep)))
        leftSounds[-1].set_volume(0.1 + 0.02 * randrange(0, 3))
    for rightStep in rightSteps:
        rightSounds.append(pygame.mixer.Sound(os.path.join(soundRoot, soundPath, rightStep)))
        rightSounds[-1].set_volume(0.1 + 0.02 * randrange(0, 3))
    for melodyPath in melodyPaths:
        sound = pygame.mixer.Sound(os.path.join(soundRoot, melodyPath))
        sound.set_volume(0.8)
        melodySounds.append(sound)
    melodyCtr = len(melodySounds) - 1
    birdsSound = pygame.mixer.Sound(os.path.join(soundRoot,  birdsPath))
    birdsSound.set_volume(0.8)
    shoutSound = pygame.mixer.Sound(os.path.join(soundRoot, shoutPath))
    shoutSound.set_volume(0.3)
    pacemakerShoutSound = pygame.mixer.Sound(os.path.join(soundRoot, pacemakerShoutPath))
    pacemakerShoutSound.set_volume(0.5)
    finishSound = pygame.mixer.Sound(os.path.join(soundRoot, finishPath))
    finishSound.set_volume(0.6)
    startSound = pygame.mixer.Sound(os.path.join(soundRoot, startPath))
    startSound.set_volume(1.0)
    stepSound = pygame.mixer.Sound(os.path.join(soundRoot, stepPath))
    stepSound.set_volume(0.8)

    stepsChannel = pygame.mixer.Channel(stepsChannelNumber)
    birdsChannel = pygame.mixer.Channel(birdsChannelNumber)
    effectChannel = pygame.mixer.Channel(effectChannelNumber)
    melodyChannel = pygame.mixer.Channel(melodyChannelNumber)


def stopSounds():
    pygame.mixer.stop()


def maintainRunningStepEffect():
    global left

    if not stepsChannel.get_busy():
        maxInd = min(len(leftSounds), len(rightSounds)) - 1
        ind = randrange(0, maxInd)
        if left:
            left = False
            sound = rightSounds[ind]
        else:
            left = True
            sound = leftSounds[ind]
        stepsChannel.play(sound, maxtime=300)


def startMelody():
    global melodyCtr
    melodyCtr = melodyCtr + 1
    if melodyCtr >= len(melodySounds):
        melodyCtr = 0
    melodyChannel.play(melodySounds[melodyCtr], loops=-1, fade_ms=20000)

def stopMelody():
    melodyChannel.stop()

def startBirds():
    melodyChannel.play(birdsSound, loops=-1)

def stopBirds():
    global melodyCtr
    melodyCtr = len(melodySounds) - 1
    melodyChannel.stop()

def shoutEffect():
    effectChannel.play(shoutSound, maxtime=1000)

def pacemakerShoutEffect():
    effectChannel.play(pacemakerShoutSound)

def startEffect():
    effectChannel.play(startSound)

def stopEffects():
    effectChannel.stop()

def stepEffect():
    effectChannel.play(stepSound)

def finishEffect():
    effectChannel.play(finishSound)
