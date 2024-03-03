### Linux installation

**The easy way:**

go to [Release folder](https://github.com/LemesoftNostalgic/sprint-o-matic/releases/latest) and click the name of the Linux
executable _sprint-o-matic_. Navigate to the "Downloads" folder with
Terminal and start the application with:

```
     ./sprint-o-matic
```

You can also use the command-line parameters like this, for example if you want to provide the analysis as a file:

```
     ./sprint-o-matic --analysis yes
```

**The recommended and safer way:**

This may be a little different depending on your web browser. I used Mozilla
Firefox.

go to [Release folder](https://github.com/LemesoftNostalgic/sprint-o-matic/releases/latest) and click the name of the source code package _Source code (zip)_. The browser should download it to the "Downloads" folder. Navigate to the "Downloads" folder and click the source code package "sprint-o-matic-3.0.3" with the right mouse button and select "extract all" from the menu.

If you don't yet have python3.10 or newer installed, then install it.
The instructions are in [python.org/Downloads](python.org/Downloads).
With Ubuntu and Debian, open the Terminal and issue the following commands:

```
 sudo apt update
 sudo apt install python3
 sudo apt install python3-pip
```

Then install the necessary python modules:

```
   python3 -m pip install pygame
   python3 -m pip install requests
   python3 -m pip install argparse
   python3 -m pip install overpy
```

Then you can start the application.
Navigate to the correct folder and issue the following command:

```
   python3 main.py
```

You can also use the command-line parameters like this, for example if you want to provide the analysis as a file:

```
   python3 main.py --analysis yes
```

**Advanced:**

If you really want, you can re-build the executable
from sources using dopyinstaller.sh.
