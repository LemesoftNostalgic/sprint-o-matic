## Adding new maps to Sprint-O-Matic

### Playing with your private maps

Using the [command line](#command-line-usage) parameters **--mapFileName** and **--lookupPngName** you can play with a map stored in your local filesystem. The map file is just an image of the map, preferably in png format, and the lookup file (i.e. terrain description) is an equally sized png image where the terrain characteristics are marked
with specific colors, see chapter [creating the terrain description](#creating-the-terrain-description).

### Make your map visible to Sprint-O-Matic users

Add a map to the Sprint-O-Matic's map listing, and everyone can play
with it. Some information regarding the map needs to be sent to the
sprint.o.matic at gmail.com to make the linkage happen:

- name, short one to fit it in the home screen
- url-link to an image of the map (png format is encouraged)
- license information for the map
- credit text for the owner/creator of the map
- url to a terrain description (equally sized png image as the map)
- license information for the terrain description
- credit text for the owner/creator of the terrain description
- meters-per-pixel factor
- default zoom factor

Here is an example of an entry in the [sprint-o-matic's current listing of external maps](https://github.com/LemesoftNostalgic/sprint-o-matic-external-map-links):

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
         "default-zoom": 1.0
    }
   ```

**Hint:** If you don't know how to publish files in the web to get an
URL of the map: an easy way to do that is to [open a free account and
repository in the GitHub](https://github.com/signup) and drag the files there.
Sprint.o.matic at gmail.com understands github repository names so you don't have
to give the precise URL in that case.

The two other things to pay attention is a) license of the map and b) creating the terrain description e.g "lookup-png".

a) Regarding the license, it is only possible to include map images
with relatively permissive license to the listing. In practice, the map
image will become visible to all the Sprint-O-Matic users when included.
The best way would be to license an
image of a candidate map with one of the creative commons license types.
This will probably limit the selection to older maps that have no more use
for live sprint orienteering events. For me, that sounds a good trade-off.

b) A bit more involved is the creation of the terrain description
e.g. "lookup-png". The following subchapter tells how to do that.

### Creating the terrain description

Basically, you have to create equally sized image as the map image.
One easy method is to make a copy of the original map image, re-paint
each terrain type with a correct color code and save the result as png.

The color codes are the following:

![Sprint-O-Matic lookup colors by Jyrki Leskelä](/doc/lookupcolors.png)

Please use an editor where you can choose the colors accurately.
I have used [GIMP](https://www.gimp.org) because I am familiar with it. The
terrain markings must represent exactly the color codes shown in the image
above. Then you need to review the edits. Pay attention to the black color of
sprint map notation: usually it marks an area that you cannot run through,
but some black features such as forest paths and fence symbol
slashes are actually runnable, so do not mark them forbidden.

See the [examples repository](https://github.com/LemesoftNostalgic/sprint-o-matic-map-image-example) for some examples of a map image and the
corresponding terrain description. I have also [a YouTube video showing
how to do the edits with GIMP](https://youtu.be/_n0IRG1GfLI).
The best working resolutions for map images and terrain descriptions are
between 1024-1280 pixels (width). The game engine is designed for
sprint map scales approximately from 1:3000 to 1:5000.

If you have an excellent map you wish to be included, but have no time or
skills to create the terrain description, please propose it via sprint.o.matic
at gmail.com anyway. I can create a couple of terrain images myself as a
pro-bono effort to get things rolling. A good map for Sprint-O-Matic is
one that has enough fences and other obstacles to pose a challenge.
Also slow green terrain is good but not mandatory.
