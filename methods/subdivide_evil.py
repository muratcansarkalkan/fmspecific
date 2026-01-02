import bpy
import bmesh
from mathutils import Vector

# --- Setup ---
class SUBDIVIDE_EVIL(bpy.types.Operator):

    bl_label = "SubdivideEvil"
    bl_idname = "mesh.subdivideevil"
    bl_description = "Subdivide edges (repeat script)"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        # --- Setup ---
        obj = bpy.context.edit_object
        me = obj.data
        bm = bmesh.from_edit_mesh(me)

        tolerance = 1
        selected_edges = [e for e in bm.edges if e.select]
        if not selected_edges:
            print("No edge selected.")
            raise SystemExit

        total_new_verts = 0

        for edge in selected_edges:
            v1, v2 = edge.verts
            edge_vec = v2.co - v1.co
            edge_len2 = edge_vec.length_squared
            if edge_len2 < 1e-12:
                continue  # degenerate edge

            aligned_vertices = []

            # --- Find vertices projected onto edge within tolerance ---
            for v in bm.verts:
                if v in edge.verts:
                    continue
                vec_to_vert = v.co - v1.co
                t = edge_vec.dot(vec_to_vert) / edge_len2
                if 0.0 < t < 1.0:  # projected point is on the edge segment
                    proj_point = v1.co + t * edge_vec
                    dist = (v.co - proj_point).length
                    if dist < tolerance:
                        aligned_vertices.append((t, v.co.copy()))

            if not aligned_vertices:
                continue

            # Sort by t along the edge (from v1 to v2)
            aligned_vertices.sort(key=lambda x: x[0])
            current_segments = [edge]

            # --- Subdivide edge at each t ---
            for t_value, vert_co in aligned_vertices:
                seg_found = None
                for seg in current_segments:
                    a, b = seg.verts
                    seg_vec = b.co - a.co
                    seg_len2 = seg_vec.length_squared
                    if seg_len2 < 1e-12:
                        continue
                    # Compute local t along this segment
                    local_t = seg_vec.dot(vert_co - a.co) / seg_len2
                    if 0.0 + 1e-6 < local_t < 1.0 - 1e-6:
                        seg_found = seg
                        break

                if seg_found is None:
                    continue

                # Compute final local factor along this segment
                a, b = seg_found.verts
                seg_vec = b.co - a.co
                seg_len2 = seg_vec.length_squared
                factor = seg_vec.dot(vert_co - a.co) / seg_len2

                res = bmesh.ops.bisect_edges(
                    bm,
                    edges=[seg_found],
                    edge_percents={seg_found: factor},
                    cuts=1
                )

                new_verts = [g for g in res.get("geom_split", []) if isinstance(g, bmesh.types.BMVert)]
                if not new_verts:
                    continue

                total_new_verts += len(new_verts)
                new_vert = new_verts[0]
                # Replace segment in current_segments
                new_edges = [ed for ed in new_vert.link_edges if ed != seg_found]
                try:
                    idx = current_segments.index(seg_found)
                    current_segments.pop(idx)
                    current_segments[idx:idx] = new_edges
                except ValueError:
                    current_segments.extend(new_edges)

        bmesh.update_edit_mesh(me)
        print(f"✅ Done. Split {len(selected_edges)} edge(s). Created {total_new_verts} new vertex/vertices.")

        return{"FINISHED"}
