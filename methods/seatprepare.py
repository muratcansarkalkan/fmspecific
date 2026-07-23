import bpy
import bmesh

class SEAT_PREPARE(bpy.types.Operator):
    bl_label = "Seat Preparation"
    bl_idname = "object.seatprepare"
    bl_description = "Moves UV islands to 0,0 before latter 2 steps"

    def execute(self, context):

        obj = bpy.context.active_object
        if not obj or obj.type != 'MESH':
            raise Exception("Select a mesh object")

        me = obj.data
        bm = bmesh.from_edit_mesh(me)
        uv_layer = bm.loops.layers.uv.active

        if not uv_layer:
            raise Exception("No active UV layer")

        # ---------------------------
        # Build UV islands via face connectivity
        # ---------------------------

        face_uvs = {}

        for f in bm.faces:
            face_uvs[f] = tuple((loop[uv_layer].uv.x, loop[uv_layer].uv.y) for loop in f.loops)

        visited = set()
        islands = []

        def shares_uv(f1, f2):
            # crude but effective: shared UV coordinate check
            uvs1 = set(face_uvs[f1])
            uvs2 = set(face_uvs[f2])
            return len(uvs1.intersection(uvs2)) > 0

        for face in bm.faces:
            if face in visited:
                continue

            stack = [face]
            island = []

            while stack:
                f = stack.pop()
                if f in visited:
                    continue

                visited.add(f)
                island.append(f)

                for edge in f.edges:
                    for lf in edge.link_faces:
                        if lf not in visited:
                            stack.append(lf)

            islands.append(island)

        # ---------------------------
        # Process each island
        # ---------------------------

        for island in islands:
            # find min UV in this island
            min_u = 1e10
            min_v = 1e10

            loops = []

            for f in island:
                for loop in f.loops:
                    uv = loop[uv_layer].uv
                    loops.append(uv)
                    if uv.x < min_u: min_u = uv.x
                    if uv.y < min_v: min_v = uv.y

            # shift island
            for uv in loops:
                uv.x -= min_u
                uv.y -= min_v

        bmesh.update_edit_mesh(me)
        return {"FINISHED"}
