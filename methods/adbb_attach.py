import bpy
import os
from mathutils import Vector

class ADBB_ATTACH(bpy.types.Operator):

    bl_label = "ADBBAttach"
    bl_idname = "object.adbbattach"
    bl_description = "Switch to Right Ortographic View before execution"

    def execute(self, context):
        area_type = 'VIEW_3D' # change this to use the correct Area Type context you want to process in
        areas  = [area for area in bpy.context.window.screen.areas if area.type == area_type]

        if len(areas) <= 0:
            raise Exception(f"Make sure an Area of type {area_type} is open or visible in your screen!")

        override = {
            'window': bpy.context.window,
            'screen': bpy.context.window.screen,
            'area': areas[0],
            'region': [region for region in areas[0].regions if region.type == 'WINDOW'][0],
        }

        # Remember the active object and mode
        active_object = bpy.context.active_object
        prev_mode = bpy.context.object.mode

        # Set the 2D cursor position (you may need to adjust these coordinates)
        cursor_location = (0.0, 0.0)

        # Switch to Right Orthographic view
        bpy.ops.view3d.view_axis(override, type='RIGHT')

        # Switch to Edit Mode
        bpy.ops.object.mode_set(mode='EDIT')

        # Select all faces
        bpy.ops.mesh.select_all(action='SELECT')

        # UV Mapping: Project View from Bounds
        bpy.ops.uv.unwrap(method='CONFORMAL', margin=0)

        # Switch back to Object Mode
        bpy.ops.object.mode_set(mode='OBJECT')

        # Set the 2D cursor position
        bpy.context.scene.cursor.location = (cursor_location[0], cursor_location[1], 0)

        # Scale UVs by 0.75 along the X-axis with 2D cursor as the pivot
        #bpy.ops.transform.resize(value=(0.75, 1, 1), orient_type='CURSOR', orient_matrix_type='CURSOR', mirror=True)

        for obj in bpy.context.selected_objects:
            bpy.ops.object.mode_set(mode = 'EDIT')
            bpy.ops.mesh.select_all(action= 'SELECT')
            for area in bpy.context.screen.areas:
                if area.type == 'VIEW_3D':
                    for region in area.regions:
                        if region.type == 'WINDOW':
                            override = {'area': area, 'region': region, 'edit_object': bpy.context.edit_object}
                            bpy.ops.uv.project_from_view(override , camera_bounds=False, correct_aspect=True, scale_to_bounds=True)
            bpy.ops.object.mode_set(mode = 'OBJECT')

        if bpy.context.active_object:
            selected_object_name = bpy.context.active_object.name
            print(f"The selected object is: {selected_object_name}")

        #Get object and UV map given their names
        def GetObjectAndUVMap( objName, uvMapName ):
            try:
                obj = bpy.data.objects[objName]

                if obj.type == 'MESH':
                    uvMap = obj.data.uv_layers[uvMapName]
                    return obj, uvMap
            except:
                pass

            return None, None

        #Scale a 2D vector v, considering a scale s and a pivot point p
        def Scale2D( v, s, p ):
            return ( p[0] + s[0]*(v[0] - p[0]), p[1] + s[1]*(v[1] - p[1]) )     

        #Scale a UV map iterating over its coordinates to a given scale and with a pivot point
        def ScaleUV( uvMap, scale, pivot ):
            for uvIndex in range( len(uvMap.data) ):
                uvMap.data[uvIndex].uv = Scale2D( uvMap.data[uvIndex].uv, scale, pivot )

        #UV data are not accessible in edit mode
        bpy.ops.object.mode_set(mode='OBJECT')

        #The names of the object and map
        uvMapName = 'UVMap'

        #Defines the pivot and scale
        pivot = Vector( (0.0, 0.0) )
        scale = Vector( (0.75, 1) )

        #Get the object from names
        obj, uvMap = GetObjectAndUVMap( selected_object_name, uvMapName )

        #If the object is found, scale its UV map
        if obj is not None:
            ScaleUV( uvMap, scale, pivot )

        # Switch back to the previous mode
        bpy.ops.object.mode_set(mode=prev_mode)

        # Restore the active object
        bpy.context.view_layer.objects.active = active_object

        # Name of the material
        material_name = "adbb [Texture2x]"

        # Create a new material
        material = bpy.data.materials.new(name=material_name)

        # Add the material to the active object
        if bpy.context.active_object:
            # Remove existing materials from the active object
            bpy.context.active_object.data.materials.clear()

            # Add the new material
            bpy.context.active_object.data.materials.append(material)
        else:
            print("No active object to assign the material.")

        # Switch to the Shader Editor
        for area in bpy.context.screen.areas:
            if area.type == 'IMAGE_EDITOR':
                area.type = 'NODE_EDITOR'

        # Create a new shader node tree for the material
        material.use_nodes = True
        nodes = material.node_tree.nodes

        # Clear default nodes
        for node in nodes:
            nodes.remove(node)

        # Create an Image Texture node
        image_texture_node = nodes.new(type='ShaderNodeTexImage')
        image_texture_node.location = (0, 0)

        # Set the image path
        image_path = "//adbb.png"
        image_texture_node.image = bpy.data.images.load(image_path)

        # Create a Principled BSDF shader node
        principled_bsdf_node = nodes.new(type='ShaderNodeBsdfPrincipled')
        principled_bsdf_node.location = (300, 0)

        # Connect the Image Texture node to the Base Color of Principled BSDF
        material.node_tree.links.new(image_texture_node.outputs["Color"], principled_bsdf_node.inputs["Base Color"])

        # Create a Material Output node
        material_output_node = nodes.new(type='ShaderNodeOutputMaterial')
        material_output_node.location = (600, 0)

        # Connect the Principled BSDF to the Material Output
        material.node_tree.links.new(principled_bsdf_node.outputs["BSDF"], material_output_node.inputs["Surface"])

        print(f"Material '{material_name}' created and nodes connected.")

        return{"FINISHED"}
