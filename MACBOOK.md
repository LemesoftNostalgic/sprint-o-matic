### MacBook installation

This is my guess, but has not been tested. I don't have a MacBook to test with.

go to [Release folder](https://github.com/LemesoftNostalgic/sprint-o-matic/releases/latest), download and extract _Source code (tar.gz)_ to your machine.

If you don't yet have python3.10 or newer installed, then install it.
The instructions are in [python.org/Downloads](python.org/Downloads).

Then install the necessary python modules from the Terminal app:

```
   python -m pip install pygame
   python -m pip install requests
   python -m pip install argparse
   python -m pip install overpy
```

Then you can start the application from Terminal app.
Navigate to the correct folder and issue the following command:

```
   python main.py
```

You can also use the [command-line parameters](#command-line-usage) like this, for example if you want to provide the analysis as a file:

```
   python main.py --analysis yes
```
