import bpy
import bmesh
import os

class MODIFY_FLAGS(bpy.types.Operator):
    bl_label = "Modify Flags"
    bl_idname = "object.modifyflags"
    bl_description = "Modifies acrs and hcrs to afla and hfla"

    def execute(self, context):
        
        def stretch_uvs_for_mesh(obj):
            """Stretches the active UV map of a mesh to fill the 0-1 texture space."""
            bpy.context.view_layer.objects.active = obj
            bpy.ops.object.mode_set(mode='EDIT')
            
            bm = bmesh.from_edit_mesh(obj.data)
            uv_layer = bm.loops.layers.uv.active
            
            if not uv_layer:
                bpy.ops.object.mode_set(mode='OBJECT')
                return False

            uvs = [loop[uv_layer].uv for face in bm.faces for loop in face.loops]
            if not uvs:
                bpy.ops.object.mode_set(mode='OBJECT')
                return False

            min_x = min(uv.x for uv in uvs)
            max_x = max(uv.x for uv in uvs)
            min_y = min(uv.y for uv in uvs)
            max_y = max(uv.y for uv in uvs)

            width = max_x - min_x
            height = max_y - min_y

            if width == 0 or height == 0:
                bpy.ops.object.mode_set(mode='OBJECT')
                return False

            scale_x = 1.0 / width
            scale_y = 1.0 / height

            for uv in uvs:
                uv.x = (uv.x - min_x) * scale_x
                uv.y = (uv.y - min_y) * scale_y

            bmesh.update_edit_mesh(obj.data)
            bpy.ops.object.mode_set(mode='OBJECT')
            return True

        # Main script logic within the operator's execute method
        initial_active = context.active_object
        initial_mode = context.mode
        
        if initial_mode != 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')

        for obj in context.scene.objects:
            if obj.type != 'MESH' or not obj.data.materials:
                continue
                
            should_process_obj = False
            
            for mat in obj.data.materials:
                if not mat or not mat.use_nodes:
                    continue
                    
                mat_updated = False
                
                for node in mat.node_tree.nodes:
                    if node.type == 'TEX_IMAGE' and node.image:
                        filepath = node.image.filepath
                        filename = os.path.basename(filepath).lower()
                        
                        target = None
                        replacement = None
                        if "hcrs" in filename:
                            target, replacement = "hcrs", "hfla"
                        elif "acrs" in filename:
                            target, replacement = "acrs", "afla"
                            
                        if target and replacement:
                            new_filename = filename.replace(target, replacement)
                            dir_path = os.path.dirname(filepath)
                            node.image.filepath = os.path.join(dir_path, new_filename)
                            node.image.name = node.image.name.lower().replace(target, replacement)
                            
                            mat_updated = True
                            should_process_obj = True
                
                if mat_updated:
                    mat.blend_method = 'OPAQUE'
            
            if should_process_obj:
                self.report({'INFO'}, f"Processing UVs and Materials for: {obj.name}")
                stretch_uvs_for_mesh(obj)

        if initial_active and initial_active.name in context.scene.objects:
            context.view_layer.objects.active = initial_active
            
        self.report({'INFO'}, "Texture Swap and UV Fit Operation Complete")
        return {'FINISHED'}