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

import sys, os

def getSemiSlowdownFactor():
    return 1.5

def getSlowdownFactor():
    return 2.0

def getVerySlowdownFactor():
    return 4.0

def getNoMask():
    return (255,255,255)

def getAiPoolMaxTimeLimit(tf):
    return 20.0 / tf

def getSemiSlowAreaMask():
    return (0, 255, 255)

def getSlowAreaMask():
    return (0, 0, 255)

def getVerySlowAreaMask():
    return (0, 0, 128)

def getForbiddenAreaMask():
    return (255, 0, 255)

def getTunnelMask():
    return (0, 0, 0)

def getControlMask():
    return (255, 0, 0)

def getPackagePath():
    return getattr(
        sys,
        '_MEIPASS',
        os.path.dirname(os.path.abspath(__file__))).removesuffix('/modules').removesuffix('\modules')
