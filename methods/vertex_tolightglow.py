import bpy

class VERTEX_TOLIGHTGLOW(bpy.types.Operator):

    bl_label = "VertexLightGlow"
    bl_idname = "object.vertextolightglow"
    
    def execute(self, context):
        # Set the name of the object you want to work with
        object_name = "Lights.001"
        suffix = " [dir]"
        # Get the object by name
        obj = bpy.data.objects.get(object_name)

        if obj is not None:
            bpy.context.view_layer.objects.active = obj
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.select_all(action='DESELECT')
            
            # Select unconnected vertices
            bpy.ops.mesh.select_non_manifold()

            bpy.ops.object.mode_set(mode='OBJECT')

            # Create empties for each selected vertex
            for v in obj.data.vertices:
                if v.select:
                    empty = bpy.data.objects.new("LightGlowA.001", None)
                    empty.location = obj.matrix_world @ v.co
                    bpy.context.collection.objects.link(empty)
            
            bpy.ops.object.select_all(action='DESELECT')
            obj.select_set(True)
            bpy.context.view_layer.objects.active = obj
            bpy.ops.object.delete()
        else:
            print("Object not found.")

        for obj in bpy.context.collection.objects:
            if obj.name.startswith("LightGlowA"):
                # Check if the object's name starts with "LightGlowA"
                obj.name += suffix
                
        return{"FINISHED"}
