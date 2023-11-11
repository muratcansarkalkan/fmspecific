import bpy

class ALPHA_TO_OPAQUE(bpy.types.Operator):

    bl_label = "alpha_to_opaque"
    bl_idname = "object.alphatoopaque"
    bl_description = "Changes blend mode of SELECTED objects from alpha blend to opaque"

    def execute(self, context):
        context = bpy.context

        for o in context.selected_objects:

            o.active_material.blend_method = 'OPAQUE'

        return {"FINISHED"}