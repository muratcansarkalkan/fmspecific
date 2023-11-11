import bpy
import os

class CROWD_SPLIT(bpy.types.Operator):

    bl_label = "crowd_split"
    bl_idname = "object.crowdsplit"
    bl_description = "Select another object and make sure nothing is selected in either of the crowds"

    def execute(self, context):
        # Set the name of the .gltf fileaimport bpy

        object_nameA = 'enable_crowdA'

        # Select the object with the faces you want to separate
        bpy.context.view_layer.objects.active = bpy.context.scene.objects[object_nameA]
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_mode(type='FACE')
        # Select 1/4 of original
        bpy.ops.mesh.select_random(ratio=0.25, seed=0, action='SELECT')
        # Separate the selected faces to a new object
        bpy.ops.mesh.separate(type='SELECTED')
        # Select 1/3 of remaining
        bpy.ops.mesh.select_random(ratio=0.33333, seed=0, action='SELECT')
        # Separate the selected faces to a new object
        bpy.ops.mesh.separate(type='SELECTED')
        # Select 1/2 of remaining
        bpy.ops.mesh.select_random(ratio=0.5, seed=0, action='SELECT')
        # Separate the selected faces to a new object
        bpy.ops.mesh.separate(type='SELECTED')
        bpy.ops.object.mode_set(mode='OBJECT')

        bpy.ops.object.select_all(action='DESELECT')

        object_nameH = 'enable_crowdH'

        # Select the object with the faces you want to separate
        bpy.context.view_layer.objects.active = bpy.context.scene.objects[object_nameH]
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_mode(type='FACE')
        # Select 1/4 of original
        bpy.ops.mesh.select_random(ratio=0.25, seed=0, action='SELECT')
        # Separate the selected faces to a new object
        bpy.ops.mesh.separate(type='SELECTED')
        # Select 1/3 of remaining
        bpy.ops.mesh.select_random(ratio=0.33333, seed=0, action='SELECT')
        # Separate the selected faces to a new object
        bpy.ops.mesh.separate(type='SELECTED')
        # Select 1/2 of remaining
        bpy.ops.mesh.select_random(ratio=0.5, seed=0, action='SELECT')
        # Separate the selected faces to a new object
        bpy.ops.mesh.separate(type='SELECTED')
        bpy.ops.object.mode_set(mode='OBJECT')


        material_assignment = {
            "enable_crowdA": "rwa0 [ClipTextureNoAlphaBlend]",
            "enable_crowdA.001": "rwa0.001 [ClipTextureNoAlphaBlend]",
            "enable_crowdA.002": "rwa0.002 [ClipTextureNoAlphaBlend]",
            "enable_crowdA.003": "rwa0.003 [ClipTextureNoAlphaBlend]",
            "enable_crowdH": "rwh0 [ClipTextureNoAlphaBlend]",
            "enable_crowdH.001": "rwh0.001 [ClipTextureNoAlphaBlend]",
            "enable_crowdH.002": "rwh0.002 [ClipTextureNoAlphaBlend]",
            "enable_crowdH.003": "rwh0.003 [ClipTextureNoAlphaBlend]"
        }

        # Iterate through the objects in the material dictionary
        for object_name, material_name in material_assignment.items():
            # Check if the object exists in the scene
            obj = bpy.data.objects.get(object_name)
            if obj:
                # Select the object and switch to Object Mode
                bpy.context.view_layer.objects.active = obj
                bpy.ops.object.mode_set(mode='OBJECT')

                # Clear existing materials on the object
                bpy.ops.object.material_slot_remove()

                # Check if the specified material exists in the scene
                material = bpy.data.materials.get(material_name)
                if material:
                    # Assign the specified material to the object
                    bpy.ops.object.material_slot_add()
                    bpy.context.object.material_slots[0].material = material
                    print(f"Material '{material_name}' assigned to object '{object_name}'.")
                else:
                    print(f"Material '{material_name}' not found.")
            else:
                print(f"Object '{object_name}' not found.")

        return{"FINISHED"}