import bpy

class BAKE_TRANS(bpy.types.Operator):
    bl_label = "BakeTrans"
    bl_idname = "object.baketrans"
    
    def execute(self, context):
        selected_objects = [obj for obj in bpy.context.selected_objects if obj.type == 'MESH']
        
        if not selected_objects:
            self.report({'WARNING'}, "No mesh objects selected.")
            return {'CANCELLED'}
        
        # Deselect all first
        bpy.ops.object.select_all(action='DESELECT')
        
        for obj in selected_objects:
            # Select only this object and make it active
            obj.select_set(True)
            bpy.context.view_layer.objects.active = obj
            
            if not obj.active_material:
                self.report({'WARNING'}, f"Object '{obj.name}' has no material, skipping.")
                obj.select_set(False)
                continue
            
            # Store the material name
            material_name = obj.active_material.name
            
            # Unlink the material
            obj.active_material_index = 0
            bpy.ops.object.material_slot_remove()
            
            # Bake this single object
            bpy.ops.object.bake(type='SHADOW')
            
            # Re-link the material back
            new_material = bpy.data.materials.get(material_name)
            if new_material:
                obj.data.materials.append(new_material)
                obj.active_material = new_material
                self.report({'INFO'}, f"Baking complete for '{obj.name}'.")
            else:
                self.report({'WARNING'}, f"Could not re-link material for '{obj.name}'.")
            
            # Deselect before moving to the next
            obj.select_set(False)
        
        bpy.ops.object.select_all(action='DESELECT')

        # Reselect stored mesh objects
        for obj in selected_objects:
            obj.select_set(True)

        # Optional: set one as active
        if selected_objects:
            bpy.context.view_layer.objects.active = selected_objects[0]
            
        return {"FINISHED"}