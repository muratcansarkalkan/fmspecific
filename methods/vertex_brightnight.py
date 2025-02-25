import bpy

class VERTEX_BRIGHTNIGHT(bpy.types.Operator):

    bl_label = "vertex_brightnight"
    bl_idname = "object.vertexbrightnight"
    bl_description = "Adjust brightness of selected objects by negative %60 to adjust for night setting"

    def execute(self, context):
        # Function to adjust vertex colors brightness by a factor
        def adjust_vertex_color_brightnight(obj, adjustment=-0.6):
            if obj.type != 'MESH' or not obj.data.vertex_colors:
                return
            
            vertex_color_layer = obj.data.vertex_colors.active.data
            
            for v_color in vertex_color_layer:
                v_color.color[0] = max(0, v_color.color[0] + adjustment)  # Adjust Red
                v_color.color[1] = max(0, v_color.color[1] + adjustment)  # Adjust Green
                v_color.color[2] = max(0, v_color.color[2] + adjustment)  # Adjust Blue

        # Process all selected objects
        for obj in bpy.context.selected_objects:
            adjust_vertex_color_brightnight(obj)

        return {"FINISHED"}
