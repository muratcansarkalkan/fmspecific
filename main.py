import bpy
from .methods import skcd_image

class PANEL_CUSTOM_UI(bpy.types.Panel):
    
    bl_label = 'FM Specific'
    bl_idname = 'OBJECT_PT_Panel'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "FM Specific"
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        # --- Import & Scale ---
        layout.label(text="Import GLTF and Scale")
        row = layout.row(align=True)
        row.operator("object.initialimport0", text="stad_0")
        row.operator("object.initialimport1", text="stad_1")
        row.operator("object.initialimport3", text="stad_3")
        layout.operator("object.scaleempties", text="Scale empties")

        # --- Crowd ---
        layout.separator(factor=0.5)
        layout.label(text="Crowd Separation")
        layout.operator("object.crowdadjust", text="Crowd all in one tool")
        row = layout.row(align=True)
        row.operator("object.crowdfifa16", text="Crowd FIFA16")
        row.operator("object.crowdpes6", text="Crowd PES6")

        layout.label(text="Crowd Distribution")
        row = layout.row(align=True)
        row.operator("object.crowdsplit", text="Split")
        row.operator("object.crowdrandomizer", text="Randomizer")

        # --- PES 6 ---
        layout.separator(factor=0.5)
        layout.label(text="PES 6")
        row = layout.row(align=True)
        row.operator("object.wsp6adboards", text="Rotate adba")
        row.operator("object.bannersadjustpes6", text="Banners")
        row.operator("object.modifyflags", text="Flags")

        # --- PES 2020 ---
        layout.separator(factor=0.5)
        layout.label(text="PES 2020")
        layout.operator("object.pes2020matremove", text="Remove unnecessary materials")
        row = layout.row(align=True)
        row.operator("object.pes2020scale", text="Remove empties & scale")
        row = layout.row(align=True)
        row.operator("object.alphatoopaque", text="Alpha to opaque")
        row.operator("object.opaquetoalpha", text="Opaque to alpha")

        # --- Seats ---
        layout.separator(factor=0.5)
        layout.label(text="Seats")
        row = layout.row(align=True)
        row.operator("object.seatprepare", text="UV prepare")
        row.operator("object.seatscale", text="Scale")
        row.operator("object.seatsubdivider", text="Subdivide")

        # --- Others ---
        layout.separator(factor=0.5)
        layout.label(text="Others")
        row = layout.row(align=True)
        row.operator("object.adbbattach", text="adbb Attach")
        row.operator("object.adboardadjust", text="Modify adboards")
        row = layout.row(align=True)
        row.operator("object.genericgrass", text="Generic grass")
        row.operator("object.baketrans", text="Bake transparent")
        row = layout.row(align=True)
        row.operator("object.removevg", text="Clear vertex groups")
        row.operator("object.removevcols", text="Remove vtx colors")
        row = layout.row(align=True)
        row.operator("object.vertexbrightness", text="Brightness")
        row.operator("object.vertexbrightnight", text="Brightness (night)")
        row = layout.row(align=True)
        row.operator("object.createbakeimage", text="Bake image")
        row.operator("object.getshadow", text="Load shadow")
        row = layout.row(align=True)
        row.operator("object.appendlights", text="Append lights")
        row.operator("object.covmapscene", text="Covmap scene")
        row = layout.row(align=True)
        row.operator("object.vertextolightglow", text="Vertex → empties (Lights.001)")
        row = layout.row(align=True)
        row.operator("object.texturesplit", text="Split by textures (PES6)")
        row.operator("mesh.subdivideevil", text="Subdivide edge")

        # --- Display Image & Refresh ---
        box = layout.box()
        header_row = box.row(align=True)
        header_row.label(text="Image Preview:", icon="IMAGE_DATA")
        header_row.operator("object.refresh_skcd_image", text="", icon="FILE_REFRESH")

        pcoll = skcd_image.preview_collections.get("main")
        if pcoll and "my_skcd_image" in pcoll:
            icon_id = pcoll["my_skcd_image"].icon_id

            img_row = box.row()
            img_row.scale_y = 0.8
            img_row.alignment = "CENTER"
            img_row.template_icon(icon_value=icon_id, scale=10.0)
        else:
            row = box.row(align=True)
            row.label(text="skcd.png not found", icon="ERROR")
            row.operator("object.refresh_skcd_image", text="", icon="FILE_REFRESH")

        layout.separator(factor=0.5)

        # --- Export ---
        layout.separator(factor=0.5)
        layout.label(text="Export Target:")
        layout.prop(scene, "quick_gltf_export_name", text="")
        layout.operator("export_scene.quick_gltf", icon="EXPORT")