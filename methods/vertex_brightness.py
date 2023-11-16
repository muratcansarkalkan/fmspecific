import bpy

class VERTEX_BRIGHTNESS(bpy.types.Operator):

    bl_label = "vertex_brightness"
    bl_idname = "object.vertexbrightness"
    bl_description = "Adjust brightness of all objects by %25"

    def execute(self, context):
        # Function to adjust vertex colors brightness by a factor
        def adjust_vertex_colors_brightness(obj, factor):
            if obj.type == 'MESH':
                mesh = obj.data
                if mesh.vertex_colors:
                    for layer_name, vcol_layer in mesh.vertex_colors.items():
                        for poly in mesh.polygons:
                            for loop_index in range(poly.loop_start, poly.loop_start + poly.loop_total):
                                color = vcol_layer.data[loop_index].color
                                vcol_layer.data[loop_index].color = (color[0] + factor, color[1] + factor, color[2] + factor, color[3])

        # Set the brightness adjustment factor
        brightness_factor = 0.25  # Adjust this value as needed

        # Get all objects in the scene
        objects = bpy.context.scene.objects

        # Adjust brightness for each object
        for obj in objects:
            adjust_vertex_colors_brightness(obj, brightness_factor)

        return {"FINISHED"}
