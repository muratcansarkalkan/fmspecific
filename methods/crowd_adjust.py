import bpy

# ─── Input Dialog ─────────────────────────────────────────────────────────────

class CROWD_ADJUST(bpy.types.Operator):
    bl_idname = "object.crowdadjust"
    bl_label = "Crowd Scale Factor"
    bl_description = "Crowd AIO tool"

    mode: bpy.props.EnumProperty(
        name="Game",
        items=[
            ('FIFA16', "FIFA 16 (11/12)", "Scale factor 11/12"),
            ('PES6',   "PES 6 (20/12)",   "Scale factor 20/12"),
            ('CUSTOM', "Custom Value",     "Enter a custom scale factor"),
        ],
        default='FIFA16'
    )

    custom_value: bpy.props.FloatProperty(
        name="Custom Scale Factor",
        default=1.0,
        min=0.01,
        max=10.0
    )

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "mode")
        if self.mode == 'CUSTOM':
            layout.prop(self, "custom_value")

    def execute(self, context):
        if self.mode == 'FIFA16':
            scale_factor = 11 / 12
        elif self.mode == 'PES6':
            scale_factor = 20 / 12
        else:
            scale_factor = self.custom_value

        run_crowd_script(scale_factor)
        return {'FINISHED'}


def run_crowd_script(scale_factor):

    # ─── Step 1: Scale UV maps on X axis only for enable_crowd ───────────────

    enable_crowd = bpy.data.objects.get("enable_crowd")
    if enable_crowd is None:
        raise RuntimeError("Object 'enable_crowd' not found in the scene.")

    me = enable_crowd.data
    for uv_layer in me.uv_layers:
        for loop in me.loops:
            uv = uv_layer.data[loop.index].uv
            uv.x *= scale_factor

    # ─── Step 2: Run crowd operators ─────────────────────────────────────────

    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.view_layer.objects.active = enable_crowd
    enable_crowd.select_set(True)

    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='OBJECT')

    bpy.ops.object.crowdrandomizer()

    bpy.ops.object.select_all(action='DESELECT')

    bpy.ops.object.crowdpes6()

    # ─── Step 3: Remove materials from enable_crowdA then enable_crowdH ──────

    for obj_name in ["enable_crowdA", "enable_crowdH"]:
        obj = bpy.data.objects.get(obj_name)
        if obj is None:
            print(f"Warning: '{obj_name}' not found, skipping material removal.")
            continue

        obj.data.materials.clear()
        print(f"Cleared all materials from '{obj_name}'.")

    # ─── Step 4: Run crowd split ──────────────────────────────────────────────

    bpy.ops.object.crowdsplit()

    # ─── Step 5: Merge all objects starting with "enable_crowd" ──────────────

    bpy.ops.object.select_all(action='DESELECT')

    crowd_objects = [
        obj for obj in bpy.data.objects
        if obj.name.lower().startswith("enable_crowd")
    ]

    if not crowd_objects:
        raise RuntimeError("No objects starting with 'enable_crowd' found to merge.")

    for obj in crowd_objects:
        obj.select_set(True)

    active_obj = bpy.data.objects.get("enable_crowd") or crowd_objects[0]
    bpy.context.view_layer.objects.active = active_obj

    bpy.ops.object.join()

    bpy.context.active_object.name = "Enable_crowd"

    print(f"Done. Scale factor used: {scale_factor:.4f}. Merged object renamed to 'Enable_crowd'.")
    
    return{"FINISHED"}