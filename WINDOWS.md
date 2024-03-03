### Windows installation

**The easy way:**

go to [Release folder](https://github.com/LemesoftNostalgic/sprint-o-matic/releases/latest) and click the name of the Windows
executable _sprint-o-matic-notsigned.exe_. Then accept the browsers request to store the file. It should be downloaded to the "Downloads" folder.

Start the command prompt by writing "cmd" to the taskbar.
Google more instructions for using the command prompt if not familiar with
it. When at the command prompt, navigate to the correct folder and start
the application. Usually the commands are like this:

```
   cd Downloads
   sprint-o-matic-notsigned.exe
```

If you have downloaded multiple versions, Windows may have added extra text
to the newer versions. If the newest is _sprint-o-matic-notsigned(1).exe_
then start it like this:

```
   "sprint-o-matic-notsigned(1).exe"
```

You can also use the [command-line parameters](#command-line-usage) like this, for example if you want to provide the analysis as a file:

```
   sprint-o-matic-notsigned.exe --analysis yes
```

**The recommended and safer way:**

This may be a little different depending on your web browser. I used Mozilla
Firefox.

go to [Release folder](https://github.com/LemesoftNostalgic/sprint-o-matic/releases/latest) and click the name of the source code package _Source code (zip)_. The browser should download it to the "Downloads" folder. Navigate to the "Downloads" folder and click the source code package "sprint-o-matic-3.0.3" with the right mouse button and select "extract all" from the menu.

If you don't yet have python3.10 or newer installed, then install it.
The instructions are in [python.org/Downloads](python.org/Downloads).
There should be a button for the newest installation package. Follow the
instructions to store the installation package to your Dowloads folder.
Then navigate to the Downloads folder and double-click the python-3.10.2-amd64
icon and the python installer should start.
Now you see the installer window. **first tick the small box left of "Add python.exe" to the PATH. Only after that click "Install Now"**.
Wait for the installation to finish.

Start the command prompt by writing "cmd" to the taskbar.
Google more instructions for using the command prompt if not familiar with
it. When at the command prompt, install the necessary python modules with the
following commands:

```
   python -m pip install pygame
   python -m pip install requests
   python -m pip install argparse
   python -m pip install overpy
```

Start the command prompt by writing "cmd" to the taskbar.
Google more instructions for using the command prompt if not familiar with
it. When at the command prompt, navigate to the correct folder and start
the application. Usually the commands are like this:

```
   cd Downloads
   cd sprint-o-matic-3.0.3
   cd sprint-o-matic-3.0.3
   python main.py
```

You can also use the [command-line parameters](#command-line-usage) like this, for example if you want to provide the analysis as a file:

```
   python main.py --analysis yes
```

**Advanced:**

If you really want, you can re-build the executable
from sources using dopyinstaller.bat that is provided with the source code.
