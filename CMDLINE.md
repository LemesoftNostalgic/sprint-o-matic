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
