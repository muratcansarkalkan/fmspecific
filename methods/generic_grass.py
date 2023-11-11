import bpy
import os
from shutil import copyfile

class GENERIC_GRASS(bpy.types.Operator):

    bl_label = "generic_grass"
    bl_idname = "object.genericgrass"
    bl_description = "Adds generic grass to the scene to avoid black holes"

    def execute(self, context):
        # Get the directory of the current blend file
        current_blend_dir = os.path.dirname(bpy.data.filepath)

        # Calculate the path to the blend file containing the "BackgroundGrass" object
        lights_blend_path = os.path.abspath(os.path.join(current_blend_dir, '..', '..', 'lights.blend'))

        # Name of the object to be appended
        object_to_append = "BackgroundGrass"

        # Name of the image texture in the appended object
        image_texture_name = "2439-4.png"  # Replace with the actual name

        # Append the object from the "lights.blend" file
        with bpy.data.libraries.load(lights_blend_path) as (data_from, data_to):
            data_to.objects = [name for name in data_from.objects if name == object_to_append]

        # Check if the object was appended
        if object_to_append in bpy.data.objects:
            # Link the object to the current scene
            bpy.context.collection.objects.link(bpy.data.objects[object_to_append])

            # Switch to Object mode
            bpy.ops.object.mode_set(mode='OBJECT')

            # Copy the image to the same path as "stadium_3.blend"
            image_path = os.path.join(current_blend_dir, '..', '..', '2439-4.png')
            new_image_path = os.path.join(current_blend_dir, '2439-4.png')
            
            try:
                copyfile(image_path, new_image_path)
                print(f"Image copied to: {new_image_path}")
            except FileNotFoundError:
                print(f"Image file not found at: {image_path}")
            
        else:
            print(f"Object '{object_to_append}' not found in the appended file.")

        return{"FINISHED"}