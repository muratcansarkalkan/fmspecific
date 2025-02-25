import bpy
import os

class GET_SHADOW(bpy.types.Operator):

    bl_label = "get_shadow"
    bl_idname = "object.getshadow"
    bl_description = "Loads shadow image and connects nodes"

    def execute(self, context):
        
        def connect_texture_to_principled_bsdf(obj, texture_node_name="bake"):
            if not obj or obj.type != 'MESH' or not obj.active_material:
                return
            
            mat = obj.active_material
            nodes = mat.node_tree.nodes
            links = mat.node_tree.links
            
            # Find the Principled BSDF node
            principled_node = next((node for node in nodes if node.type == 'BSDF_PRINCIPLED'), None)
            if not principled_node:
                return
            
            # Find the texture node
            texture_node = nodes.get(texture_node_name)
            if not texture_node or texture_node.type != 'TEX_IMAGE':
                return
            
            # Change image to shad.tga from working directory
            working_dir = os.getcwd()
            image_path = os.path.join(working_dir, "shad.tga")
            texture_node.image = bpy.data.images.load(image_path)
            
            # Connect Color to Base Color
            links.new(texture_node.outputs['Color'], principled_node.inputs['Base Color'])
            
            # Connect Alpha to Alpha
            links.new(texture_node.outputs['Alpha'], principled_node.inputs['Alpha'])
            
            # Set blend mode to Alpha Blend
            mat.blend_method = 'BLEND'
            mat.use_backface_culling = False
            
        # Apply to selected object
        if bpy.context.object:
            connect_texture_to_principled_bsdf(bpy.context.object)
            
        return{"FINISHED"}