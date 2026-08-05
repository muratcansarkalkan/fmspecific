import bpy

class OPAQUE_TO_ALPHA(bpy.types.Operator):

    bl_label = "opaque_to_alpha"
    bl_idname = "object.opaquetoalpha"
    bl_description = ("Connects the Base Color texture's Alpha output to the Principled BSDF's "
                       "Alpha input (if not already connected), sets blend mode to Alpha Blend, "
                       "and enables Show Backface")

    def execute(self, context):
        context = bpy.context

        for o in context.selected_objects:

            mat = o.active_material
            if mat is None or mat.node_tree is None:
                continue

            node_tree = mat.node_tree
            nodes = node_tree.nodes
            links = node_tree.links

            # Find the Principled BSDF node
            bsdf = None
            for n in nodes:
                if n.type == 'BSDF_PRINCIPLED':
                    bsdf = n
                    break

            if bsdf is None:
                continue

            base_color_input = bsdf.inputs.get("Base Color")
            alpha_input = bsdf.inputs.get("Alpha")

            if base_color_input is None or alpha_input is None:
                continue

            if not base_color_input.is_linked:
                continue

            # Get the node feeding Base Color
            tex_node = base_color_input.links[0].from_node
            tex_alpha_output = tex_node.outputs.get("Alpha")

            if tex_alpha_output is None:
                continue

            # Check if Alpha input is already connected to that texture node's Alpha output
            already_connected = False
            if alpha_input.is_linked:
                for link in alpha_input.links:
                    if link.from_node == tex_node and link.from_socket == tex_alpha_output:
                        already_connected = True
                        break

            if not already_connected:
                links.new(tex_alpha_output, alpha_input)

            # Set blend mode to Alpha Blend and enable Show Backface
            mat.blend_method = 'BLEND'
            mat.show_transparent_back = True

        return {"FINISHED"}