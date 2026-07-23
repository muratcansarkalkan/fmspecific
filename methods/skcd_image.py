import os
import bpy
import bpy.utils.previews

preview_collections = {}


def unregister_previews():
    for pcoll in list(preview_collections.values()):
        bpy.utils.previews.remove(pcoll)
    preview_collections.clear()


def register_previews():
    unregister_previews()

    pcoll = bpy.utils.previews.new()

    # Fallback path logic
    if bpy.data.is_saved:
        img_path = bpy.path.abspath("//skcd.png")
    else:
        img_path = os.path.abspath("skcd.png")

    if os.path.exists(img_path):
        pcoll.load("my_skcd_image", img_path, "IMAGE")
        print(f"[Panel Image] Loaded: {img_path}")
    else:
        print(f"[Panel Image] NOT FOUND at: {img_path}")

    preview_collections["main"] = pcoll


class OBJECT_OT_refresh_skcd_image(bpy.types.Operator):
    """Reload skcd.png from disk"""

    bl_idname = "object.refresh_skcd_image"
    bl_label = "Refresh Image"
    bl_options = {"REGISTER"}

    def execute(self, context):
        register_previews()
        for area in context.screen.areas:
            if area.type == "VIEW_3D":
                area.tag_redraw()

        self.report({"INFO"}, "Image refreshed successfully!")
        return {"FINISHED"}

if __name__ == "__main__":
    register()