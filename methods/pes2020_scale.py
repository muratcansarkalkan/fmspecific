import bpy
from math import radians
from mathutils import Vector, Matrix

class PES2020_SCALE(bpy.types.Operator):

    bl_label = "PES2020_scale"
    bl_idname = "object.pes2020scale"
    bl_description = "Removes empties and scales PES 2020 stadiums to FIFAM"

    def execute(self, context):
        
        # Remove empties only if they are visible in an active collection
        for obj in list(bpy.data.objects):
            if obj.type == 'EMPTY' and obj.visible_get():
                bpy.data.objects.remove(obj, do_unlink=True)
        
        # CONFIG
        # -----------------------------
        scale_yz = 32.25 / 52.5
        scale_x  = 21.5 / 34
        rotation_deg = 90  # around Z
        # -----------------------------

        # Save original pivot
        orig_pivot = context.scene.transform_orientation_slots[0].type
        orig_pivot_point = context.scene.tool_settings.transform_pivot_point

        # Get 3D cursor location
        cursor_loc = context.scene.cursor.location.copy()

        # Get selected objects, or all if none selected
        objs = context.selected_objects if context.selected_objects else bpy.data.objects

        # Build rotation matrix around cursor
        rot_mat = Matrix.Translation(cursor_loc) @ \
                  Matrix.Rotation(radians(rotation_deg), 4, 'Z') @ \
                  Matrix.Translation(-cursor_loc)

        # Build scale matrix around cursor
        scale_mat = Matrix.Translation(cursor_loc) @ \
                    Matrix.Scale(scale_x, 4, Vector((1,0,0))) @ \
                    Matrix.Scale(scale_yz, 4, Vector((0,1,0))) @ \
                    Matrix.Scale(scale_yz, 4, Vector((0,0,1))) @ \
                    Matrix.Translation(-cursor_loc)

        # Apply to visible objects in active collections
        for obj in objs:
            if not obj.visible_get():  # skips if hidden individually or via collection
                continue
                
            # apply rotation
            obj.matrix_world = rot_mat @ obj.matrix_world

            # apply non-uniform scale
            obj.matrix_world = scale_mat @ obj.matrix_world

        # Restore pivot
        context.scene.tool_settings.transform_pivot_point = orig_pivot_point
        context.scene.transform_orientation_slots[0].type = orig_pivot

        return {"FINISHED"}