import bpy

#Texture Split
class TEXTURE_SPLIT(bpy.types.Operator):
    
    bl_label = "TextureSplit"
    bl_idname = "object.texturesplit"
    
    def execute(self, context):
        # Get the active object
        obj = bpy.context.active_object

        # Create a dictionary to store vertex groups based on their image texture
        image_to_vertex_groups = {}

        # Iterate through the object's polygons (faces)
        for poly in obj.data.polygons:
            material_index = poly.material_index
            material = obj.data.materials[material_index]

            # Iterate through the material's nodes to find the image texture
            for node in material.node_tree.nodes:
                if node.type == 'TEX_IMAGE':
                    image = node.image

                    # Check if the image is not None
                    if image is not None:
                        # Create a vertex group for each image texture
                        if image not in image_to_vertex_groups:
                            image_to_vertex_groups[image] = obj.vertex_groups.new(name=image.name)

                        # Assign the vertices of the face to the corresponding vertex group
                        for vert_index in poly.vertices:
                            image_to_vertex_groups[image].add([vert_index], 1.0, 'REPLACE')

        origin_name = bpy.context.active_object.name
        keys = bpy.context.object.vertex_groups.keys()
        real_keys = []
        for gr in keys:
            bpy.ops.object.mode_set(mode="EDIT")
            # Set the vertex group as active
            bpy.ops.object.vertex_group_set_active(group=gr)

            # Deselect all verts and select only current VG
            bpy.ops.mesh.select_all(action='DESELECT')
            bpy.ops.object.vertex_group_select()
            # bpy.ops.mesh.select_all(action='INVERT')
            try:
                bpy.ops.mesh.separate(type="SELECTED")
                real_keys.append(gr)
            except:
                pass
        for i in range(1, len(real_keys) + 1):
            bpy.data.objects['{}.{:03d}'.format(origin_name, i)].name = '{}.{}'.format(
                origin_name, real_keys[i - 1])

        return{"FINISHED"}
