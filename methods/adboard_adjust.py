import bpy
import bmesh


def execute_full_workflow(context, action):
    # --- PHASE 1: +X FACE MANIPULATION ---
    bpy.ops.object.mode_set(mode='EDIT')
    obj = context.edit_object
    me = obj.data
    bm = bmesh.from_edit_mesh(me)

    bpy.ops.mesh.select_all(action='DESELECT')
    for f in bm.faces:
        if f.normal.dot((1, 0, 0)) > 0.9:
            f.select = True

    bm.select_flush(True)
    n = len([f for f in bm.faces if f.select])

    if n == 0:
        return False

    bpy.ops.mesh.edge_split()
    bpy.ops.transform.translate(value=(0, 0, 1))

    bm.faces.ensure_lookup_table()
    selected_faces = [f for f in bm.faces if f.select]
    target_face = max(selected_faces, key=lambda f: f.calc_center_median().y)

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

    bm.faces.ensure_lookup_table()
    final_selection = [f for f in bm.faces if f.normal.dot((1, 0, 0)) > 0.9]
    for f in final_selection:
        f.select = True

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

    bpy.ops.mesh.duplicate_move()
    bpy.ops.mesh.separate(type='SELECTED')

    bmesh.update_edit_mesh(me)
    bpy.ops.object.mode_set(mode='OBJECT')

    new_obj = [o for o in context.selected_objects if o != obj][0]
    bpy.ops.object.select_all(action='DESELECT')
    new_obj.select_set(True)
    context.view_layer.objects.active = new_obj

    # --- PHASE 3: VIEWPORT ALIGNMENT ---
    for area in context.screen.areas:
        if area.type == 'VIEW_3D':
            for space in area.spaces:
                if space.type == 'VIEW_3D':
                    rv3d = space.region_3d
                    rv3d.view_rotation = (0.5, 0.5, 0.5, 0.5)
                    rv3d.view_perspective = 'ORTHO'

    # --- PHASE 4: PRE-ATTACH ADJUSTMENT ---
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.transform.translate(value=(0.01, 0, 0))
    bpy.ops.object.mode_set(mode='OBJECT')

    # --- PHASE 5: ADBB ATTACH ---
    bpy.ops.object.adbbattach()

    return True


class ADBOARD_ADJUST(bpy.types.Operator):
    bl_idname = "object.adboardadjust"
    bl_label = "Modify Adboards for ADBB"
    bl_description = "Adjust adboard faces and attach via ADBB"
    bl_options = {'REGISTER', 'UNDO'}

    action: bpy.props.EnumProperty(
        name="Method",
        items=[
            ('DUPLICATE', "Duplicate", "Add a face and scale n/(n+1)"),
            ('DELETE',    "Delete",    "Remove a face and scale n/(n-1)"),
        ],
        default='DUPLICATE'
    )

    def execute(self, context):
        ok = execute_full_workflow(context, self.action)
        if not ok:
            self.report({'WARNING'}, "No +X faces found on the active object.")
            return {'CANCELLED'}
        self.report({'INFO'}, f"Adboard adjust complete ({self.action}).")
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
