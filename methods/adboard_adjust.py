import bpy
import bmesh

def execute_full_workflow(action):
    # --- PHASE 1: +X FACE MANIPULATION ---
    bpy.ops.object.mode_set(mode='EDIT')
    obj = bpy.context.edit_object
    me = obj.data
    bm = bmesh.from_edit_mesh(me)

    # Selection & initial count (n)
    bpy.ops.mesh.select_all(action='DESELECT')
    for f in bm.faces:
        if f.normal.dot((1, 0, 0)) > 0.9:
            f.select = True
    
    bm.select_flush(True)
    n = len([f for f in bm.faces if f.select])
    
    if n == 0: return

    # Edge Split and Move 1m in Z
    bpy.ops.mesh.edge_split()
    bpy.ops.transform.translate(value=(0, 0, 1))

    # Identify target face for Duplicate/Delete
    bm.faces.ensure_lookup_table()
    selected_faces = [f for f in bm.faces if f.select]
    target_face = max(selected_faces, key=lambda f: f.calc_center_median().y)

    # Perform Action & Set Scale Factor
    if action == 'DELETE':
        bpy.ops.mesh.select_all(action='DESELECT')
        target_face.select = True
        bpy.ops.mesh.delete(type='FACE')
        scale_factor = n / (n - 1) if n > 1 else 1.0
    
    elif action == 'DUPLICATE':
        verts_y = [v.co.y for v in target_face.verts]
        face_length_y = max(verts_y) - min(verts_y)
        bpy.ops.mesh.select_all(action='DESELECT')
        target_face.select = True
        bpy.ops.mesh.duplicate()
        bpy.ops.transform.translate(value=(0, face_length_y, 0))
        scale_factor = n / (n + 1)

    # Final selection of the group to Center and Scale
    bm.faces.ensure_lookup_table()
    final_selection = [f for f in bm.faces if f.normal.dot((1, 0, 0)) > 0.9]
    for f in final_selection: f.select = True

    if final_selection:
        median_y = sum((f.calc_center_median().y for f in final_selection)) / len(final_selection)
        bpy.ops.transform.translate(value=(0, -median_y, 0))
        bpy.ops.transform.resize(value=(1, scale_factor, 1))
        bpy.ops.transform.translate(value=(0, 0, -1))

    # --- PHASE 2: CENTER-MOST FACE SEPARATION ---
    bpy.ops.mesh.select_all(action='DESELECT')
    bm.faces.ensure_lookup_table()
    
    if len(bm.faces) >= 2:
        all_centers_y = [f.calc_center_median().y for f in bm.faces]
        overall_median_y = sum(all_centers_y) / len(all_centers_y)
        
        sorted_faces = sorted(bm.faces, key=lambda f: abs(f.calc_center_median().y - overall_median_y))
        sorted_faces[0].select = True
        sorted_faces[1].select = True

    # Duplicate and Separate
    bpy.ops.mesh.duplicate_move()
    bpy.ops.mesh.separate(type='SELECTED')
    
    # Update Mesh before switching modes
    bmesh.update_edit_mesh(me)
    bpy.ops.object.mode_set(mode='OBJECT')

    # Select the new object
    new_obj = [o for o in bpy.context.selected_objects if o != obj][0]
    bpy.ops.object.select_all(action='DESELECT')
    new_obj.select_set(True)
    bpy.context.view_layer.objects.active = new_obj

    # --- PHASE 3: VIEWPORT ALIGNMENT ---
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            for space in area.spaces:
                if space.type == 'VIEW_3D':
                    rv3d = space.region_3d
                    rv3d.view_rotation = (0.5, 0.5, 0.5, 0.5) # Right View
                    rv3d.view_perspective = 'ORTHO' # Perspective Mode
                    
    # --- PHASE 4: PRE-ATTACH ADJUSTMENT & ADBB ---
    # Ensure we are in Edit Mode for the new object
    bpy.ops.object.mode_set(mode='EDIT')
    
    # Select all geometry within the new object and move 0.01m in X
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.transform.translate(value=(0.01, 0, 0))
    
    # Switch back to Object Mode for the operator
    bpy.ops.object.mode_set(mode='OBJECT')     
    
    # --- PHASE 5: ADBB ATTACH ---
    bpy.ops.object.adbbattach()

# UI Operator
class UnifiedWorkflowOperator(bpy.types.Operator):
    bl_idname = "wm.unified_blender_task"
    bl_label = "Run Unified Workflow"
    
    action: bpy.props.EnumProperty(
        items=[('DUPLICATE', "Duplicate", "Scale n/(n+1)"),
               ('DELETE', "Delete", "Scale n/(n-1)")],
        name="Choose Method"
    )

    def execute(self, context):
        execute_full_workflow(self.action)
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

bpy.utils.register_class(UnifiedWorkflowOperator)
bpy.ops.wm.unified_blender_task('INVOKE_DEFAULT')

