import bpy

class PES2020_MATREMOVE(bpy.types.Operator):

    bl_label = "PES2020_matremove"
    bl_idname = "object.pes2020matremove"
    bl_description = "Removes unnecessary materials for PES2020 stadia"

    def execute(self, context):
        #Get the material you want (replace the name below)
        mats = bpy.data.materials

        for mat in mats:
            mat.use_nodes = True
            
            for i in mat.node_tree.nodes:
                if type(i) == bpy.types.ShaderNodeGroup:
                    mat.node_tree.nodes.remove(i)
                elif i.name == 'NormalMap_Tex_NRM':
                    mat.node_tree.nodes.remove(i)
                elif i.name == 'SpecularMap_Tex_LIN':
                    mat.node_tree.nodes.remove(i)
                elif i.name == 'MetalnessMap_Tex_LIN':
                    mat.node_tree.nodes.remove(i)

        return {"FINISHED"}
        
