import bpy
import os

# Operator
class QUICK_OT_export_gltf(bpy.types.Operator):
    bl_idname = "export_scene.quick_gltf"
    bl_label = "Export Visible to GLTF"
    bl_description = "Export all visible objects with transforms applied to chosen GLTF file name"

    def execute(self, context):
        scene = context.scene
        filename = scene.quick_gltf_export_name

        # Deselect all
        bpy.ops.object.select_all(action='DESELECT')

        # Select all visible objects
        for obj in context.view_layer.objects:
            if not obj.hide_get():
                obj.select_set(True)

        # Apply rotation + scale
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)

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
