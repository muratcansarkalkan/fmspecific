import bpy
import bmesh
import math
from mathutils import Vector


class WSP6_ADBOARDS(bpy.types.Operator):
    bl_idname = "object.wsp6adboards"
    bl_label = "Rotate Adboards"
    bl_description = "Apply UV transformations and geometry cleanup to selected faces"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # Ensure we are in Edit Mode
        bpy.ops.object.mode_set(mode='EDIT')

        obj = context.edit_object
        me = obj.data
        bm = bmesh.from_edit_mesh(me)

        # --- UV BOUNDING BOX CENTER ---
        uv_layer = bm.loops.layers.uv.verify()
        uvs = [l[uv_layer].uv for f in bm.faces for l in f.loops if f.select]

        if uvs:
            min_x = min(uv.x for uv in uvs)
            max_x = max(uv.x for uv in uvs)
            min_y = min(uv.y for uv in uvs)
            max_y = max(uv.y for uv in uvs)

            pivot = Vector(((min_x + max_x) / 2, (min_y + max_y) / 2))

            # --- UV TRANSFORMATIONS ---
            angle = math.radians(-90)  # 90 degrees Clockwise
            scale_x = 16.0
            scale_y = 0.0625

            for face in bm.faces:
                if face.select:
                    for loop in face.loops:
                        uv = loop[uv_layer].uv

                        temp_uv = uv - pivot

                        curr_x, curr_y = temp_uv.x, temp_uv.y
                        rotated_x = curr_x * math.cos(angle) - curr_y * math.sin(angle)
                        rotated_y = curr_x * math.sin(angle) + curr_y * math.cos(angle)

                        uv.x = (rotated_x * scale_x) + pivot.x
                        uv.y = (rotated_y * scale_y) + pivot.y

        bpy.ops.mesh.select_all(action='SELECT')

        # --- GEOMETRY CLEANUP ---
        bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=0.001)

        bpy.ops.mesh.select_all(action='SELECT')
        bmesh.update_edit_mesh(me)
        bpy.ops.mesh.tris_convert_to_quads()
        bm = bmesh.from_edit_mesh(me)

        bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
        for face in bm.faces:
            face.normal_flip()

        bmesh.update_edit_mesh(me)
        context.view_layer.update()

        self.report({'INFO'}, "Cleanup and UV Transform Complete.")
        return {'FINISHED'}
