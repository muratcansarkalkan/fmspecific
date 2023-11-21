import bpy

class REMOVE_VG(bpy.types.Operator):
    
    bl_label = "RemoveVG"
    bl_idname = "object.removevg"
    
    def execute(self, context):
        # Get all objects in the scene
        objects = bpy.context.scene.objects

        # Loop through each object
        for obj in objects:
            if obj.type == 'MESH':
                # Access the object's vertex groups and clear them
                obj_vertex_groups = obj.vertex_groups
                for group in obj_vertex_groups:
                    obj_vertex_groups.remove(group)
            
        return{"FINISHED"}
