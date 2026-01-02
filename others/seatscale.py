import bpy
import bmesh
import math

def snap_uv_x_to_grid(obj, grid_size=0.25):
    """ Snaps vertical UV edges (constant X, varying Y) to the nearest grid step on the X-axis. """
    
    if obj.type != 'MESH':
        print("Selected object is not a mesh.")
        return
    
    if not obj.data.uv_layers:
        print("No UV layers found on the object.")
        return
    
    mesh = obj.data
    bm = bmesh.new()
    bm.from_mesh(mesh)
    uv_layer = bm.loops.layers.uv.active

    if not uv_layer:
        print("No active UV layer found.")
        bm.free()
        return

    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.uv.select_all(action='SELECT')
    bpy.ops.object.mode_set(mode='OBJECT')

    moved = set()

    for face in bm.faces:
        loops = face.loops
        for i in range(len(loops)):
            loop1 = loops[i]
            loop2 = loops[(i + 1) % len(loops)]

            uv1 = loop1[uv_layer].uv
            uv2 = loop2[uv_layer].uv

            # Check if edge is vertical in UV space (X is roughly the same, Y differs)
            if math.isclose(uv1.x, uv2.x, abs_tol=1e-5) and not math.isclose(uv1.y, uv2.y, abs_tol=1e-5):

                snapped_x = round(uv1.x / grid_size) * grid_size

                for loop in (loop1, loop2):
                    key = (loop.vert.index, round(loop[uv_layer].uv.x, 5), round(loop[uv_layer].uv.y, 5))
                    if key not in moved:
                        loop[uv_layer].uv.x = snapped_x
                        moved.add(key)

    bm.to_mesh(mesh)
    bm.free()
    mesh.update()
    print(f"Snapped vertical UV edges to nearest {grid_size} unit.")

# Run it
selected_obj = bpy.context.object
if selected_obj:
    seat = 4
    grid_size = 1 / seat
    snap_uv_x_to_grid(selected_obj, grid_size)
