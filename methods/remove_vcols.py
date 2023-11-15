import bpy

class REMOVE_VCOLS(bpy.types.Operator):

    bl_label = "remove_vcols"
    bl_idname = "object.removevcols"
    bl_description = "Removes unnecessary vertex colors of selected objects from FIFA16 stadia"

    def execute(self, context):
        
        # Get the selected objects
        selected_objects = bpy.context.selected_objects

        # Iterate through the selected objects
        for obj in selected_objects:
            if obj.type == 'MESH':
                # Get the object's data (mesh)
                mesh = obj.data
                
                # Get a list of all the vertex color layers in the mesh
                vertex_color_layers = mesh.vertex_colors.keys()
                
                # Iterate through the vertex color layers
                for layer_name in vertex_color_layers:
                    # Check if the layer name is not "Col"
                    if layer_name != "Col":
                        # Remove the vertex color layer
                        mesh.vertex_colors.remove(mesh.vertex_colors[layer_name])

        return{"FINISHED"}