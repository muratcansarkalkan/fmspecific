import bpy

class SCALE_EMPTIES(bpy.types.Operator):

    bl_label = "ScaleEmpties"
    bl_idname = "object.scaleempties"
    
    def execute(self, context):
        def change_empty_size(empty, size_in_meters):
            empty.empty_display_size = size_in_meters

        # Change this value to set the desired size in meters
        new_size_in_meters = 1.0

        # Iterate through all empties in the scene
        for empty in bpy.context.scene.objects:
            if empty.type == 'EMPTY':
                change_empty_size(empty, new_size_in_meters)
                
        return{"FINISHED"}