import bpy
import bmesh

# --- SETTINGS ---
# The formula used is: cuts = (uv_length * multiplier) + offset
# Based on your examples: 2.0 -> 7 and 1.0 -> 3
MULTIPLIER = 4.0
OFFSET = -1
# ----------------

def subdivide_by_uv_length():
    obj = bpy.context.edit_object
    if not obj or obj.type != 'MESH':
        print("Please enter Edit Mode with a mesh object.")
        return

    bm = bmesh.from_edit_mesh(obj.data)
    uv_layer = bm.loops.layers.uv.active

    if not uv_layer:
        print("No active UV map found.")
        return

    # We process edges one by one because each might need a different number of cuts
    for edge in bm.edges:
        if edge.select:
            # Calculate UV length of the edge
            # (Taking the first loop/face that uses this edge)
            if not edge.link_loops:
                continue
                
            loop = edge.link_loops[0]
            uv1 = loop[uv_layer].uv
            uv2 = loop.link_loop_next[uv_layer].uv if loop.edge == edge else loop.link_loop_prev[uv_layer].uv
            
            # Calculate horizontal (U) distance in UV space
            uv_dist = abs(uv1.x - uv2.x)
            uv_dist_y = abs(uv1.y - uv2.y)
            
            # Only process if it's primarily horizontal in UV space
            if uv_dist > uv_dist_y and uv_dist > 0.01:
                # Calculate number of cuts based on your increments
                num_cuts = int(round((uv_dist * MULTIPLIER) + OFFSET))
                
                if num_cuts > 0:
                    # Perform subdivision on this specific edge
                    bmesh.ops.subdivide_edges(bm, 
                                              edges=[edge], 
                                              cuts=num_cuts, 
                                              use_grid_fill=True)

    bmesh.update_edit_mesh(obj.data)
    print("Subdivision complete based on UV length.")

subdivide_by_uv_length()