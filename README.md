# FIFA Stadium Conversion Scripts

A collection of scripts for converting stadiums from FIFA16, PES6, and PES2020 to FIFA Manager 14 in Blender.

## Compatibility

These scripts are compatible with Blender 3.1.

## Installation

1. Download the repository as a ZIP file by clicking the "Code" button and selecting "Download ZIP."
2. Open Blender.
3. Go to `Edit` -> `Preferences`.
4. Click on the `Add-ons` tab.
5. Click the "Install" button at the top right.
6. Select the downloaded ZIP file and click "Install Add-on."
7. Enable the installed add-on by checking the checkbox next to its name.

## Prerequisites

Before using the custom PES6 to FIFA Manager conversion scripts, follow these additional steps:

1. **Add `stadium_3.blend` and `shad.png` to `Extra\fm_season` Directory:**
   - Copy the `stadium_3.blend` and `shad.png` from the `sample` folder inside the repository.
   - Paste `shad.png` into the `pes6_to_fifam` directory.
   - Move `stadium_3.blend` into the `Extra\fm_season` directory within the `pes6_to_fifam` directory.

2. **Place `lights.blend` and `2439-4.png` in the Parent Directory:**
   - Copy the `lights.blend` file and `2439-4.png` image from the `sample` folder inside the repository.
   - Paste them into the directory you specified as output path for pes6_to_fifam.

This is how the directory structure inside pes6_to_fifam should look:

├── pes6_to_fifam
│   ├── Extra
│   │   ├── fm_13
│   │   ├── fm_season
│   │   │   ├── stadium_3.blend
│   │   │   ├── ...
│   │   ├── shad.png
│   ├── pes6_to_fifam.bat
│   ├── pes6_to_fifam.exe
│   ├── README.txt (Please read this before doing anything)

Assuming you specified an output path as "D:\Convert" for pes6_to_fifam and imported a stadium named "ENG - Home Park", this is how the directory structure should look:

├── D:\
│   ├── Convert
│   │   ├── GEO - Boris Paichadze Dinamo Arena, Tblisi
│   │   │   ├── 0
│   │   │   │   ├── ...
│   │   │   │   ├── stadium_3.blend
│   │   │   ├── 1
│   │   │   │   ├── ...
│   │   │   │   ├── stadium_3.blend
│   │   │   ├── 3
│   │   │   │   ├── ...
│   │   │   │   ├── stadium_3.blend
│   │   ├── lights.blend
│   │   ├── 2439-4.png


## Usage

After installing the FIFA Stadium Conversion Scripts add-on, you can access it within Blender:

1. Open Blender.
2. Navigate to the 3D View.
3. Look for the "FM Specific" tab in the N-panel on the right side of the 3D View.

   ![FM Specific Tab](images/screenshot.png)

4. Within the "FM Specific" tab, you'll find various scripts categorized based on their functionality.

   - **Import GLTF and Scale**
      - Make sure you have the stadium GLTF files (`stadium_0.gltf`, `stadium_1.gltf`, `stadium_3.gltf`) available in the same blend file you've opened in Blender.
      - This function imports the gltf file, scales the stadium by 0.01 for easier editing, then moves whole stadium by 0.0125 meters to avoid flickering.
      - Import stad_0: Imports `stadium_0.gltf`
      - Import stad_1: Imports `stadium_1.gltf`
      - Import stad_3: Imports `stadium_3.gltf`

   - **Crowd Separation**
      - Crowd FIFA16: Separates crowds based on their texture for FIFA16 stadia.
      - Crowd PES6: Separates crowds based on their texture for PES6 stadia.

   - **Crowd Distribution**
      - Crowd Split: Equally and randomly distributes crowds for both away and home to 4 different materials (0,1,2,3)
      
   - **PES 2020**
      - Remove Unnecessary Materials: Removes every other material from the blend file unless the texture is a diffuse texture.
      - Alpha to Opaque: Switches blending type of Selected objects from alpha blend, to opaque.

   - **Others**
      - adbb Attach: Uses adbb
      - Add Generic Grass: `object.genericgrass`
      - Bake Transparent Objects: `object.baketrans`
      - Convert Vertex to Empties (Lights.001): `object.vertextolightglow`
      - Split Stadium by Textures (PES6): `object.texturesplit`
      - Clear Vertex Groups: `object.removevg`
      - Scale Empties: `object.scaleempties`

This tab provides easy access to the various functionalities offered by the FIFA Stadium Conversion Scripts.

## Warnings

- As the importing functions scale stadiums by 0.01, make sure you use "-scale 100" command at OTools while importing your output to an .o file.

## Addressing Flickering in Field Objects

In some cases, there might be flickering in the field objects. To mitigate this issue, you can follow these steps:

### Steps to Avoid Flickering

1. **Identify Field Objects:**
   - Open your blend file containing the stadium model.

2. **Edit Field Object:**
   - Locate the field object that is experiencing flickering.

3. **Enter Edit Mode:**
   - Select the field object.
   - Press `Tab` to enter Edit Mode.

4. **Select All Faces:**
   - Press `A` to select all faces of the field object.

5. **Move Faces in Z-Axis:**
   - Press `G` to enter the Grab mode.
   - Press `Z` to restrict movement to the Z-axis.
   - Move the faces slightly up or down by pressing `0.0025` and hitting `Enter`.

6. **Exit Edit Mode:**
   - Press `Tab` to exit Edit Mode.

### Notes

- This adjustment (moving faces up or down by 0.0025 m in the Z-axis) is a workaround to address flickering issues in the field objects.
- Experiment with the exact value based on your specific scene to find the most suitable adjustment.
- Save your blend file after making these adjustments.

Making this slight modification in the Z-axis for the affected field objects can help reduce or eliminate flickering during rendering.

## Technical Details

The scripts are written in Python and leverage Blender's Python API. They are designed to work seamlessly with Blender 3.1.

Feel free to explore the source code to understand the implementation details and make any necessary modifications to suit your needs.

## Contribution

If you'd like to contribute or report issues, feel free to open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).
