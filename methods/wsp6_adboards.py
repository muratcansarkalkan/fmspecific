import bpy
import bmesh
import math
from mathutils import Vector

# Ensure we are in Edit Mode
bpy.ops.object.mode_set(mode='EDIT')

# Get the mesh data
obj = bpy.context.edit_object
me = obj.data
bm = bmesh.from_edit_mesh(me)

# --- 2. FIND UV BOUNDING BOX CENTER ---
uv_layer = bm.loops.layers.uv.verify()
uvs = [l[uv_layer].uv for f in bm.faces for l in f.loops if f.select]

if uvs:
    min_x = min(uv.x for uv in uvs)
    max_x = max(uv.x for uv in uvs)
    min_y = min(uv.y for uv in uvs)
    max_y = max(uv.y for uv in uvs)
    
    pivot = Vector(((min_x + max_x) / 2, (min_y + max_y) / 2))

    # --- 3. APPLY UV TRANSFORMATIONS ---
    angle = math.radians(-90) # 90 degrees Clockwise
    scale_x = 16.0
    scale_y = 0.0625

    for face in bm.faces:
        if face.select:
            for loop in face.loops:
                uv = loop[uv_layer].uv
                
                # Move to origin relative to pivot
                temp_uv = uv - pivot
                
                # Rotate
                curr_x, curr_y = temp_uv.x, temp_uv.y
                rotated_x = curr_x * math.cos(angle) - curr_y * math.sin(angle)
                rotated_y = curr_x * math.sin(angle) + curr_y * math.cos(angle)
                
                # Scale and Move back to pivot
                uv.x = (rotated_x * scale_x) + pivot.x
                uv.y = (rotated_y * scale_y) + pivot.y

bpy.ops.mesh.select_all(action='SELECT')

# --- 1. GEOMETRY CLEANUP ---
# Merge by Distance (0.001m)
bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=0.001)

bpy.ops.mesh.select_all(action='SELECT')
# Tris to Quads (Triangles to Faces)
# This operator is better handled via bpy.ops for standard behavior
bmesh.update_edit_mesh(me) # Sync bmesh back to mesh for bpy.ops
bpy.ops.mesh.tris_convert_to_quads()
bm = bmesh.from_edit_mesh(me) # Re-sync bmesh

# Recalculate Normals Inside
# Use bmesh.ops.recalc_face_normals with 'inside' set to True
bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
for face in bm.faces:
    face.normal_flip() # Explicitly ensure they point inward

# Update the mesh and viewport
bmesh.update_edit_mesh(me)
bpy.context.view_layer.update()
print("Cleanup and UV Transform Complete.")