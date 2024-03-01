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
    datas=[('./sprintomatic/images/lemesoftnostalgic/*','./sprintomatic/images/lemesoftnostalgic'), ('./sprintomatic/fonts/*','./sprintomatic/fonts'), ('./sprintomatic/sounds/*','./sprintomatic/sounds/'),('./sprintomatic/sounds/*','./sprintomatic/sounds/'), ('./sprintomatic/sounds/21608__ali_6868__gravel-footsteps/*', './sprintomatic/sounds/21608__ali_6868__gravel-footsteps'), ('./sprintomatic/sounds/berdnikov2004/*', './sprintomatic/sounds/berdnikov2004'),  ('./sprintomatic/sounds/cgoulao/*', './sprintomatic/sounds/cgoulao'), ('./sprintomatic/sounds/crk365/*', './sprintomatic/sounds/crk365'),  ('./sprintomatic/sounds/frodo89/*', './sprintomatic/sounds/frodo89'), ('./sprintomatic/sounds/furbyguy/*', './sprintomatic/sounds/furbyguy'),  ('./sprintomatic/sounds/jackslay/*', './sprintomatic/sounds/jackslay'), ('./sprintomatic/sounds/josefpres/*', './sprintomatic/sounds/josefpres'),  ('./sprintomatic/sounds/szymalix/*', './sprintomatic/sounds/szymalix'), ('./sprintomatic/sounds/badoink/*', './sprintomatic/sounds/badoink'),  ('./sprintomatic/sounds/bronxio/*', './sprintomatic/sounds/bronxio'), ('./sprintomatic/sounds/craigsmith/*', './sprintomatic/sounds/craigsmith'),  ('./sprintomatic/sounds/fran_ky/*', './sprintomatic/sounds/fran_ky'), ('./sprintomatic/sounds/fupicat/*', './sprintomatic/sounds/fupicat'),  ('./sprintomatic/sounds/iykqic0/*', './sprintomatic/sounds/iykqic0'), ('./sprintomatic/sounds/johaynes/*', './sprintomatic/sounds/johaynes'),  ('./sprintomatic/sounds/nomiqbomi/*', './sprintomatic/sounds/nomiqbomi'), ('./sprintomatic/sounds/seth/*', './sprintomatic/sounds/seth'),  ('./sprintomatic/sounds/the_loner/*', './sprintomatic/sounds/the_loner') ],
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
