import bpy

class BAKE_TRANS(bpy.types.Operator):

    bl_label = "BakeTrans"
    bl_idname = "object.baketrans"
    
    def execute(self, context):
        obj = bpy.context.active_object

        # Check if the active object is a mesh
        if obj.type == 'MESH':
            # Store the material name
            material_name = obj.active_material.name

            # Unlink the material from the object
            obj.active_material_index = 0
            bpy.ops.object.material_slot_remove()

            # Bake your desired settings (adjust as needed)
            bpy.ops.object.bake(type='SHADOW')

            # Re-link the material to the object
            new_material = bpy.data.materials.get(material_name)
            if new_material:
                obj.data.materials.append(new_material)
                obj.active_material = new_material
                
                print("Baking complete.")

            else:
                print("Active object is not a mesh.")
                
        return{"FINISHED"}