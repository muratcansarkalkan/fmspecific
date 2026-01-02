import bpy
import os

# --- Setup ---
class APPEND_LIGHTS(bpy.types.Operator):

    bl_label = "Append Lights"
    bl_idname = "object.appendlights"
    bl_description = "Append rain and sun"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        # --- Setup ---
        # Absolute path to the .blend file
        blend_path = r"C:\FIFA Manager Stadium Project\Bucket List Edit Convert\lights.blend"

        # Objects to append
        object_names = ["Rain", "Sun"]

        # Path inside the .blend file where objects live
        objects_dir = os.path.join(blend_path, "Object")

        # Append each object
        for obj_name in object_names:
            bpy.ops.wm.append(
                filepath=os.path.join(objects_dir, obj_name),
                directory=objects_dir,
                filename=obj_name
            )

        return{"FINISHED"}
