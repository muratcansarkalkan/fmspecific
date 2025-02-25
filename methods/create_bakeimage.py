import bpy

class CREATE_BAKEIMAGE(bpy.types.Operator):

    bl_label = "create_bakeimage"
    bl_idname = "object.createbakeimage"
    bl_description = "Creates image to be baked in 512x512 and creates a material"

    def execute(self, context):

        def create_material_with_texture(obj, material_name="shad", texture_name="bake", texture_size=(512, 512)):
            # Create a new material
            mat = bpy.data.materials.get(material_name) or bpy.data.materials.new(name=material_name)
            mat.use_nodes = True
            
            # Get the material's node tree
            nodes = mat.node_tree.nodes
            links = mat.node_tree.links
            
            # Remove existing texture nodes if they exist
            for node in nodes:
                if node.type == 'TEX_IMAGE' and node.name == texture_name:
                    nodes.remove(node)
            
            # Create a new image texture node
            tex_node = nodes.new(type='ShaderNodeTexImage')
            tex_node.name = texture_name
            tex_node.label = texture_name
            tex_node.image = bpy.data.images.new(texture_name, width=texture_size[0], height=texture_size[1])
            
            # Assign material to object
            if obj.data.materials:
                obj.data.materials[0] = mat
            else:
                obj.data.materials.append(mat)
            
        # Apply to selected object
        if bpy.context.object:
            create_material_with_texture(bpy.context.object)

        return {"FINISHED"}
