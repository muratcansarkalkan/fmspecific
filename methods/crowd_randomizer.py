import bpy
import bmesh
import random

class CROWD_RANDOMIZER(bpy.types.Operator):

    bl_label = "crowd_randomizer"
    bl_idname = "object.crowdrandomizer"
    bl_description = "Function to randomly place UV maps of crowd meshes (select crowd in Object mode)"

    def execute(self, context):
        # Function to randomly place UV maps of crowd meshes

        # Set the number of divisions
        divisions = 12
        shift_unit = 1 / divisions

        # Get the active object
        obj = bpy.context.object
        if obj is None or obj.type != 'MESH':
            raise Exception("Please select a mesh object.")

        # Get the UV layer
        mesh = obj.data
        bm = bmesh.new()
        bm.from_mesh(mesh)
        uv_layer = bm.loops.layers.uv.verify()

        # Get all faces
        faces = list(bm.faces)
        total_faces = len(faces)
        faces_per_group = total_faces // divisions

        # Shuffle faces to randomize selection
        random.shuffle(faces)

        # Apply UV shifts
        for i in range(divisions - 1):  # Last 1/12 is not moved
            if not faces:
                break
            selected_faces = faces[:faces_per_group]
            del faces[:faces_per_group]

            shift_value = shift_unit * (i + 1)
            
            for face in selected_faces:
                for loop in face.loops:
                    uv = loop[uv_layer].uv
                    uv.x += shift_value  # Move in the U direction

        # Apply changes
        bm.to_mesh(mesh)
        bm.free()

        return {"FINISHED"}
