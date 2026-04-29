import bpy
import bmesh
import random
import math

def get_loose_parts(obj):
    """Get all loose parts as sets of vertex indices."""
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    
    # Find connected components
    visited = set()
    parts = []
    
    for v in bm.verts:
        if v.index in visited:
            continue
        
        # BFS to find all connected vertices
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
        print("No active UV layer found!")
        return
    
    # Build a set of loop indices that belong to our vertices
    vert_set = set(vert_indices)
    
    for poly in mesh.polygons:
        for loop_idx in poly.loop_indices:
            loop = mesh.loops[loop_idx]
            if loop.vertex_index in vert_set:
                uv = uv_layer.data[loop_idx].uv
                uv.x += offset_x
                uv.y += offset_y


def distribute_parts_to_groups(parts, num_groups):
    """
    Distribute parts into num_groups as equally as possible.
    Extra parts go to earlier groups.
    e.g. 41 parts, 12 groups -> 4,4,4,4,4,3,3,3,3,3,3,3
    """
    total = len(parts)
    base_size = total // num_groups
    remainder = total % num_groups  # first 'remainder' groups get one extra
    
    groups = []
    idx = 0
    for i in range(num_groups):
        size = base_size + (1 if i < remainder else 0)
        groups.append(parts[idx:idx + size])
        idx += size
    
    return groups


def compute_uv_offset(group_index, columns, step):
    """
    Compute UV offset for a group index.
    Layout fills left-to-right, then moves down a row.
    """
    col = group_index % columns
    row = group_index // columns
    offset_x = col * step
    offset_y = -row * step
    return offset_x, offset_y


# ─── CONFIG ───────────────────────────────────────────────────────────────────

NUM_GROUPS   = 12      # How many UV slots to divide into
UV_STEP      = 0.25    # Step size per slot (1 / tiles per row)
COLUMNS      = 4       # How many groups per row  (1/UV_STEP)
RANDOM_SEED  = 42      # Set to None for a different shuffle each run

# ──────────────────────────────────────────────────────────────────────────────

obj = bpy.context.active_object

if obj is None or obj.type != 'MESH':
    raise RuntimeError("Please select a mesh object first.")

print(f"\n=== UV Loose-Part Distributor ===")
print(f"Object: {obj.name}")

# 1. Find all loose parts
parts = get_loose_parts(obj)
print(f"Loose parts found: {len(parts)}")

# 2. Shuffle randomly
if RANDOM_SEED is not None:
    random.seed(RANDOM_SEED)
random.shuffle(parts)

# 3. Distribute into groups
groups = distribute_parts_to_groups(parts, NUM_GROUPS)
for i, g in enumerate(groups):
    ox, oy = compute_uv_offset(i, COLUMNS, UV_STEP)
    print(f"  Group {i+1:>2}: {len(g):>2} part(s)  →  UV offset ({ox:+.4f}, {oy:+.4f})")

# 4. Apply UV offsets
for group_index, group_parts in enumerate(groups):
    ox, oy = compute_uv_offset(group_index, COLUMNS, UV_STEP)
    for part_verts in group_parts:
        move_uv_for_part(obj, part_verts, ox, oy)

# 5. Refresh
obj.data.update()
print("\nDone! UVs updated.")