import bpy
import bmesh

class SEAT_SUBDIVIDER(bpy.types.Operator):
    bl_label = "Seat Subdivider"
    bl_idname = "object.seatsubdivider"
    bl_description = "Subdivides seats based on provided multiplier"

    multiplier: bpy.props.IntProperty(
        name="Multiplier",
        description="Subdivision multiplier (converted to float internally)",
        default=4,
        min=1,
        max=100
    )

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        # --- SETTINGS ---
        MULTIPLIER = float(self.multiplier)
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

            for edge in bm.edges:
                if edge.select:
                    if not edge.link_loops:
                        continue

                    loop = edge.link_loops[0]
                    uv1 = loop[uv_layer].uv
                    uv2 = loop.link_loop_next[uv_layer].uv if loop.edge == edge else loop.link_loop_prev[uv_layer].uv

                    uv_dist = abs(uv1.x - uv2.x)
                    uv_dist_y = abs(uv1.y - uv2.y)

                    if uv_dist > uv_dist_y and uv_dist > 0.01:
                        num_cuts = int(round((uv_dist * MULTIPLIER) + OFFSET))

                        if num_cuts > 0:
                            bmesh.ops.subdivide_edges(bm,
                                                      edges=[edge],
                                                      cuts=num_cuts,
                                                      use_grid_fill=True)

            bmesh.update_edit_mesh(obj.data)
            print(f"Subdivision complete. Multiplier used: {MULTIPLIER}")

        subdivide_by_uv_length()
        return {"FINISHED"}
