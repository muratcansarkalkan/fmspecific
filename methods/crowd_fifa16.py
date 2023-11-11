import bpy

class CROWD_FIFA16(bpy.types.Operator):

    bl_label = "crowd_fifa16"
    bl_idname = "object.crowdfifa16"
    bl_description = "Separates crowd properly for FIFA16"

    def execute(self, context):
        # Set the object name to select
        object_name = "enable_crowd"

        # Deselect all objects
        bpy.ops.object.select_all(action='DESELECT')

        # Select the object by name
        if bpy.data.objects.get(object_name):
            bpy.data.objects[object_name].select_set(True)
            bpy.context.view_layer.objects.active = bpy.data.objects[object_name]

        # Create a dictionary to store vertex groups based on their image texture
        image_to_vertex_groups = {}
        obj = bpy.context.view_layer.objects.active
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
            
        bpy.ops.object.mode_set(mode='OBJECT')

        # Remove the original object
        if bpy.data.objects.get(object_name):
            bpy.ops.object.select_all(action='DESELECT')
            bpy.data.objects[object_name].select_set(True)
            bpy.ops.object.delete()

        # Set the mapping of old texture names to new names
        texture_name_mapping = {".rwa0": "A", ".rwh0": "H"}

        # Deselect all objects
        bpy.ops.object.select_all(action='DESELECT')

        # Select the objects by name
        for texture_name, new_suffix in texture_name_mapping.items():
            object_name_with_texture = f"{object_name}{texture_name}"
            if bpy.data.objects.get(object_name_with_texture):
                bpy.data.objects[object_name_with_texture].select_set(True)

        # Rename the selected objects
        for obj in bpy.context.selected_objects:
            original_name = obj.name
            for texture_name, new_suffix in texture_name_mapping.items():
                if texture_name in original_name:
                    new_name = original_name.replace(texture_name, new_suffix)
                    obj.name = new_name
                    break

        # Set the object names to select
        object_name_A = "enable_crowdA"
        object_name_H = "enable_crowdH"

        # Deselect all objects
        bpy.ops.object.select_all(action='DESELECT')

        # Select objects by name
        if bpy.data.objects.get(object_name_A):
            bpy.data.objects[object_name_A].select_set(True)

        if bpy.data.objects.get(object_name_H):
            bpy.data.objects[object_name_H].select_set(True)

        # Remove vertex groups from the selected objects
        for obj in bpy.context.selected_objects:
            bpy.context.view_layer.objects.active = obj
            bpy.ops.object.vertex_group_remove(all=True)

        return{"FINISHED"}
