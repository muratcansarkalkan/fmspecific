import bpy
import os
import subprocess

# Operator
class QUICK_OT_export_gltf(bpy.types.Operator):
    bl_idname = "export_scene.quick_gltf"
    bl_label = "Export Visible to GLTF"
    bl_description = "Export all visible objects with transforms applied to chosen GLTF file name"

    def execute(self, context):
        scene = context.scene
        selected = scene.quick_gltf_export_name

        # "sky_3_fifa16.gltf" is a UI-only choice: it exports to the real
        # sky_3.gltf file, but uses a different vColScale on import below.
        if selected == "sky_3_fifa16.gltf":
            filename = "sky_3.gltf"
        else:
            filename = selected

        # Deselect all
        bpy.ops.object.select_all(action='DESELECT')

        # Gather visible objects, split lights from the rest
        light_objs = []
        other_objs = []
        for obj in context.view_layer.objects:
            if not obj.hide_get():
                if obj.type == 'LIGHT':
                    light_objs.append(obj)
                else:
                    other_objs.append(obj)

        # Apply rotation + scale to everything except lights
        if other_objs:
            bpy.ops.object.select_all(action='DESELECT')
            for obj in other_objs:
                obj.select_set(True)
            context.view_layer.objects.active = other_objs[0]
            bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)

        # Reselect everything visible for export
        bpy.ops.object.select_all(action='DESELECT')
        for obj in other_objs + light_objs:
            obj.select_set(True)

        # Output directory
        if bpy.data.filepath:
            out_dir = os.path.dirname(bpy.data.filepath)
        else:
            out_dir = os.path.expanduser("~")
        filepath = os.path.join(out_dir, filename)

        # Export to glTF
        bpy.ops.export_scene.gltf(
            filepath=filepath,
            export_format='GLTF_SEPARATE',
            use_selection=True,
            export_yup=True,
            export_apply=True,
            export_texcoords=True,
            export_normals=True,
            export_colors=True,
            export_materials='EXPORT',
            export_image_format='AUTO',
            export_texture_dir="",
            export_keep_originals=False,
            export_extras=False,
            export_animations=False,
            export_cameras=False,
            export_lights=False,
            check_existing=False
        )
        self.report({'INFO'}, f"Exported {filename}")
        print(f"✅ Export finished: {filepath}")

        # --- Post-process with otools ---
        vcol_scale = '0.75' if selected == "sky_3_fifa16.gltf" else '0.5'

        cmd = [
            'otools', 'import',
            '-i', filename,
            '-game', 'fm13',
            '-writefsh',
            '-stadium',
            '-gentexnames',
            '-fshLevels', '5',
            '-srgb',
            '-vColScale', vcol_scale,
            '-scale', '100',
            '-sortByName',
            '-mergeVCols',
            '-fshForceAlphaCheck',
            '-fshAddTextures', 'shad',
            '-fshFormat', 'dxt'
        ]

        subprocess.call(cmd, cwd=out_dir)
        self.report({'INFO'}, f"otools import finished for {filename}")
        print(f"✅ otools import finished: {filename} (vColScale={vcol_scale})")

        return {'FINISHED'}


# UI Panel
class QUICK_PT_gltf_panel(bpy.types.Panel):
    bl_label = "GLTF Quick Export"
    bl_idname = "VIEW3D_PT_quick_gltf_export"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "GLTF Export"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        layout.label(text="Choose Export Target:")
        layout.prop(scene, "quick_gltf_export_name", text="")
        layout.operator("export_scene.quick_gltf", icon="EXPORT")


# Register
def register():
    bpy.utils.register_class(QUICK_OT_export_gltf)
    bpy.utils.register_class(QUICK_PT_gltf_panel)
    bpy.types.Scene.quick_gltf_export_name = bpy.props.EnumProperty(
        name="GLTF Name",
        description="Choose a target export filename",
        items=[
            ("shadow_1.gltf", "shadow_1.gltf", ""),
            ("sky_3.gltf", "sky_3.gltf", ""),
            ("sky_3_fifa16.gltf", "sky_3.gltf (FIFA16)", ""),
            ("stadium_0.gltf", "stadium_0.gltf", ""),
            ("stadium_1.gltf", "stadium_1.gltf", ""),
            ("stadium_3.gltf", "stadium_3.gltf", ""),
        ],
        default="stadium_3.gltf"
    )


def unregister():
    del bpy.types.Scene.quick_gltf_export_name
    bpy.utils.unregister_class(QUICK_PT_gltf_panel)
    bpy.utils.unregister_class(QUICK_OT_export_gltf)


if __name__ == "__main__":
    register()