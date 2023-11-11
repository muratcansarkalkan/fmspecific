import bpy

class REMOVE_VG(bpy.types.Operator):
    
    bl_label = "RemoveVG"
    bl_idname = "object.removevg"
    
    def execute(self, context):

        # Ensure there's an active object
        if bpy.context.active_object:
            obj = bpy.context.active_object
            
            # Remove all vertex groups from the active object
            for group in obj.vertex_groups:
                obj.vertex_groups.remove(group)
            
            print("All vertex groups have been removed from the active object.")
        else:
            print("No active object found.")
            
        return{"FINISHED"}
