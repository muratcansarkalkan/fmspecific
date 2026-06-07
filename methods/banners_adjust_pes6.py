import bpy
import bmesh
import random


def get_loose_parts(obj):
    """Get all loose parts as sets of vertex indices."""
    bm = bmesh.new()
    bm.from_mesh(obj.data)

    visited = set()
    parts = []

    for v in bm.verts:
        if v.index in visited:
            continue

        component = set()
        queue = [v]
        while queue:
            current = queue.pop()
            if current.index in visited:
                continue
            visited.add(current.index)
            component.add(current.index)
            for edge in current.link_edges:
                other = edge.other_vert(current)
                if other.index not in visited:
                    queue.append(other)

        parts.append(component)

    bm.free()
    return parts


def move_uv_for_part(obj, vert_indices, offset_x, offset_y):
    """Move UV coordinates for a specific set of vertices."""
    mesh = obj.data
    uv_layer = mesh.uv_layers.active

    if not uv_layer:
        return

    vert_set = set(vert_indices)

    for poly in mesh.polygons:
        for loop_idx in poly.loop_indices:
            loop = mesh.loops[loop_idx]
            if loop.vertex_index in vert_set:
                uv = uv_layer.data[loop_idx].uv
                uv.x += offset_x
                uv.y += offset_y


def distribute_parts_to_groups(parts, num_groups):
    """Distribute parts into num_groups as equally as possible."""
    total = len(parts)
    base_size = total // num_groups
    remainder = total % num_groups

    groups = []
    idx = 0
    for i in range(num_groups):
        size = base_size + (1 if i < remainder else 0)
        groups.append(parts[idx:idx + size])
        idx += size

    return groups


def compute_uv_offset(group_index, columns, step):
    """Compute UV offset for a group index."""
    col = group_index % columns
    row = group_index // columns
    offset_x = col * step
    offset_y = -row * step
    return offset_x, offset_y


class BANNERS_ADJUST_PES6(bpy.types.Operator):
    bl_idname = "object.bannersadjustpes6"
    bl_label = "Adjust Banners"
    bl_description = "Distribute loose UV parts into slots across the UV grid"
    bl_options = {'REGISTER', 'UNDO'}

    num_groups: bpy.props.IntProperty(
        name="UV Slots",
        description="How many UV slots to divide into",
        default=12,
        min=1,
        max=64
    )
    uv_step: bpy.props.FloatProperty(
        name="UV Step",
        description="Step size per slot (1 / tiles per row)",
        default=0.25,
        min=0.01,
        max=1.0
    )
    columns: bpy.props.IntProperty(
        name="Columns",
        description="How many groups per row",
        default=4,
        min=1,
        max=32
    )
    random_seed: bpy.props.IntProperty(
        name="Random Seed",
        description="Seed for shuffling parts",
        default=42
    )

    def execute(self, context):
        obj = context.active_object

        if obj is None or obj.type != 'MESH':
            self.report({'ERROR'}, "Please select a mesh object first.")
            return {'CANCELLED'}

        parts = get_loose_parts(obj)
        self.report({'INFO'}, f"Loose parts found: {len(parts)}")

        random.seed(self.random_seed)
        random.shuffle(parts)

        groups = distribute_parts_to_groups(parts, self.num_groups)

        for group_index, group_parts in enumerate(groups):
            ox, oy = compute_uv_offset(group_index, self.columns, self.uv_step)
            for part_verts in group_parts:
                move_uv_for_part(obj, part_verts, ox, oy)

        obj.data.update()
        self.report({'INFO'}, "Done! UVs updated.")
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
