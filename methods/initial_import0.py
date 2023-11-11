import bpy
import os

class INITIAL_IMPORT0(bpy.types.Operator):

    bl_label = "initial_import0"
    bl_idname = "object.initialimport0"
    bl_description = "Adds generic grass to the scene to avoid black holes"

    def execute(self, context):
        # Set the name of the .gltf file
        gltf_filename = "stadium_0.gltf"
        # Get the absolute path of the current .blend file
        blend_file_path = bpy.path.abspath("//")

        # Construct the full path to the .gltf file
        gltf_path = os.path.join(blend_file_path, gltf_filename)

        # Clear existing mesh objects in the scene
        bpy.ops.object.select_all(action='DESELECT')
        bpy.ops.object.select_by_type(type='MESH')
        bpy.ops.object.delete()

        # Import the .gltf file with pack images feature disabled
        bpy.ops.import_scene.gltf(filepath=gltf_path, import_pack_images=False)

        # Select all imported objects
        bpy.ops.object.select_all(action='SELECT')

        # Scale all selected objects by 0.01
        bpy.ops.transform.resize(value=(0.01, 0.01, 0.01))

        # Apply Rotation and Scale transforms
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)

        # Function to get empty display size
        def change_empty_size(empty, size_in_meters):
            empty.empty_display_size = size_in_meters

        # Change this value to set the desired size in meters
        new_size_in_meters = 1.0

        # Iterate through all empties in the scene
        for empty in bpy.context.scene.objects:
            if empty.type == 'EMPTY':
                change_empty_size(empty, new_size_in_meters)
                
        # Switch to Edit mode for all selected objects
        bpy.ops.object.mode_set(mode='EDIT')

        # Convert Tris to Quads with specific angle settings and "Compare UVs" option enabled
        bpy.ops.mesh.select_all(action='SELECT')
        #bpy.ops.mesh.tris_convert_to_quads()
        # Tris to quads with options didn't work.
        bpy.ops.mesh.tris_convert_to_quads(face_threshold=1.30899, shape_threshold=1.30899, uvs=True)

        # Move all vertices in the positive Z-axis direction by 0.0125 meters
        bpy.ops.transform.translate(value=(0, 0, 0.0125), constraint_axis=(False, False, True))

        # Switch back to Object mode
        bpy.ops.object.mode_set(mode='OBJECT')

        return{"FINISHED"}