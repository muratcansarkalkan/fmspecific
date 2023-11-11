# Stadium Converting Tutorial (PES6 to FIFAM)

This tutorial will try to explain how to convert a stadium from PES6.

## Before reading

You can use direct download links to download required tools. You don't need to click inline links, as most of them forward to detailed descriptions. Also please read the FAQ section too.

## Required tools

**Blender 2.9+** 

The program we will use to edit stadiums. https://www.blender.org/download/ 

**Adobe Photoshop**

This is used for editing images. If you could find latest version of Photoshop, that's great. I use Photoshop 2020, latest version would be appreciated. For Photoshop, there's a trial 7-day version but also you can find a free CS2 version (it's old but still functional) on the internet.

https://www.adobe.com/uk/products/photoshop/free-trial-download.html 

**Latest OTools version**

OTools is a tool developed by Dmitri for importing/exporting EA Sports model format. **O** is a file extension in EA Sports games which is used for model and animation files.

https://bitbucket.org/fifam/otools/downloads/

**PES6 to FIFA Manager converter**

This tool is developed by Dmitri. It converts the PES6 stadia to .gltf files.

https://www.mediafire.com/file/wgbvkwnv8khedmb/pes6_to_fifam.7z/file

## File structure for PES6 stadia

For a custom PES6 stadium, make sure that the directory has at least 1_day_fine, 2_day_rain and 4_night_fine directories.

## File convention for stadiums

There are 21 files that are related to a stadium. 

| Files      | Description |
| :---        |    :----   |
| collision_0.bin, collision_1.bin, collision_3.bin      | Collision is used to define how ball will interact with stadium geometry.       |
| complete.txt | This has no meaning. It is a placeholder file by me to periodically batch upload stadiums. |
| covmap_1.fsh   | Covmap file is used to define the shadows reflecting over the players        |
| effects_0.txt, effects_3.txt      | Effect files are used to determine the brightness and color of lights.       |
| lights_0.loc, lights_3.loc   | Determines light locations and rotations.        |
| shadow_0.o, shadow_1.o, shadow_3.o      | Shadow model used on the field. This needs to be separate from stadium model       |
| sky_0.o, sky_1.o, sky_3.o   | Sky model        |
| stadium_0.o, stadium_1.o, stadium_3.o      | Stadium model       |
| template.xml | This XML file manages preview settings for stadiums to be presented in menus. |
| texture_0.fsh, texture_1.fsh, texture_3.fsh   | Every texture used for the stadium is packed in this file including shadow and sky        |

The suffix of files which are 0, 1, 3 are representing the weather condition. FIFAM supports 3 different weather conditions in 3D mode; ***rainy*** (0), ***day*** (1) and ***night*** (3). Rainy and day weather is used in weekend games depending on the weather, while night state is used in weekday games whether it's raining/snowing or not. Collision, light, shadow, sky, stadium and texture files are separately built for each weather.

## Starting

Coming soon

## Importing settings

Here are the settings you can use with descriptions.

| Command | Description |
| :---        |    :----   |
| -writefsh        |    Creates a .fsh file alongside the model.   |
| -stadium        |    Uses the stadium preset.   |
| -gentexnames        |    Generates texture names, if the texture names are larger than 4 characters.   |
| -fshLevels 5       |    Levels of [mipmaps](https://en.wikipedia.org/wiki/Mipmap).   |
| -srgb        |    Related to vertex colors. The vertex colors are displayed properly.   |
| -vColScale 0.5        |    Adjusts the brightness of vertex colors for the game.   |
| -fshFormat dxt        |    FSH format. DXT is preferred for stadiums for better compression and display.   |
| -sortByName        |    Sorting objects by their names. This is helpful especially for arranging the display of transparent objects.   |
| -fshForceAlphaCheck        |    This is for better alpha detecting. Many PNGs are saved with alpha channel even when there are no transparent pixels |

## FAQ

- There is an error displaying transparent parts. Fences look terrible. Why does that happen?
    - This is related to the rendering order of FIFA engine. EA’s game engine causes an ugly bug with transparent parts, if the objects are not ordered accordingly: Make sure that the more a mesh is in the front, the more backwards it should be in the part order of the stadium file.
    - For example, consider 4 parts; stand (opaque), seats (either opaque or transparent), fence (transparent) and net (transparent). From last to first; it should be net, then fence, then seats, then stands. PES6 models are not built according to this rule, so this is on your part. You can do this by naming the parts, then using `-sortByName` option while importing OTools. The name of net part will be last one, while stand part would be first (eg. Net part starts with Z, fence with Y, seats with X, stands with W). Rename the parts from Outliner, or press F2 while you are at Object Mode.
- The pitch looks weird as it changes color all the time. Why does that happen?
    - This is called [z-fighting](https://en.wikipedia.org/wiki/Z-fighting). Z-fighting is a phenomenon in rendering that occurs when two or more meshes have very similar distances to the camera. To avoid z-fighting, either elevate the pitch by at least 1 meters, or use `-translate 0,0,1.25` while importing the stadium to .o file.
    - You can avoid this problem if you use my plugin for Blender 3.1 [here](https://github.com/muratcansarkalkan/fmspecific) while importing stadiums.
- The shadow looks terrible on the field. Why does that happen?
    - The is related to the rendering order of FIFA once again. To avoid the weird view of shadow, you need to separate the part that needs to overlap the field and export to .gltf file as *shadow_\*.gltf*, then import with OTools. You can use the same settings with importing stadiums.
- Do you plan to create tutorials for stadiums made for other PES or FIFA games?
    - They are complex compared to PES6's models, so for now, no.