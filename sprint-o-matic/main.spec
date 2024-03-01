# -*- mode: python ; coding: utf-8 -*-

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

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('./images/lemesoftnostalgic/*','./images/lemesoftnostalgic'), ('./fonts/*','./fonts'), ('./sounds/*','./sounds/'),('./sounds/*','./sounds/'), ('./sounds/21608__ali_6868__gravel-footsteps/*', './sounds/21608__ali_6868__gravel-footsteps'), ('./sounds/berdnikov2004/*', './sounds/berdnikov2004'),  ('./sounds/cgoulao/*', './sounds/cgoulao'), ('./sounds/crk365/*', './sounds/crk365'),  ('./sounds/frodo89/*', './sounds/frodo89'), ('./sounds/furbyguy/*', './sounds/furbyguy'),  ('./sounds/jackslay/*', './sounds/jackslay'), ('./sounds/josefpres/*', './sounds/josefpres'),  ('./sounds/szymalix/*', './sounds/szymalix'), ('./sounds/badoink/*', './sounds/badoink'),  ('./sounds/bronxio/*', './sounds/bronxio'), ('./sounds/craigsmith/*', './sounds/craigsmith'),  ('./sounds/fran_ky/*', './sounds/fran_ky'), ('./sounds/fupicat/*', './sounds/fupicat'),  ('./sounds/iykqic0/*', './sounds/iykqic0'), ('./sounds/johaynes/*', './sounds/johaynes'),  ('./sounds/nomiqbomi/*', './sounds/nomiqbomi'), ('./sounds/seth/*', './sounds/seth'),  ('./sounds/the_loner/*', './sounds/the_loner') ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='sprintomatic.ico'
)
