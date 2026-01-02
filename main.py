import bpy

class PANEL_CUSTOM_UI(bpy.types.Panel):
    
    bl_label = 'FM Specific'
    bl_idname = 'OBJECT_PT_Panel'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "FM Specific"
    
    def draw(self, context):
        # Variables
        layout = self.layout
        scene = context.scene

        # Create simple rows
        # Create simple row
        row = layout.row()
        row.label(text = "Import GLTF and Scale")
        row = layout.row(align=True)
        row.operator("object.initialimport0", text = "stad_0")
        row.operator("object.initialimport1", text = "stad_1")
        row.operator("object.initialimport3", text = "stad_3")
        row = layout.row()
        row.operator("object.scaleempties", text = "Scale empties")
        # Create simple row
        row = layout.row()
        row.label(text = "Crowd separation")
        row = layout.row(align=True)
        row.operator("object.crowdfifa16", text = "Crowd FIFA16")
        row.operator("object.crowdpes6", text = "Crowd PES6")
        row = layout.row()
        row.label(text = "Crowd distribution")
        row = layout.row(align=True)
        row.operator("object.crowdsplit", text = "Split")
        row.operator("object.crowdrandomizer", text = "Randomizer")
        # Create simple row
        row = layout.row()
        row.label(text = "PES 2020")
        row = layout.row()
        row.operator("object.pes2020matremove", text = "Remove unnecessary materials")
        row = layout.row()
        row.operator("object.pes2020scale", text = "Remove empties and scale stadium")
        row = layout.row()
        row.operator("object.alphatoopaque", text = "Alpha to opaque")
        # Create simple row
        row = layout.row()
        row.label(text = "Others")
        row = layout.row()
        row.operator("object.adbbattach", text = "adbb Attach")
        row = layout.row()
        row.operator("object.genericgrass", text = "Add generic grass")
        row = layout.row()
        row.operator("object.baketrans", text = "Bake transparent objects")
        row = layout.row()
        row.operator("object.vertextolightglow", text = "Convert vertex to empties, name your object as Lights.001")
        row = layout.row()
        row.operator("object.texturesplit", text = "Split stadium by textures (PES6)")
        row = layout.row()
        row.operator("object.removevg", text = "Clear vertex groups")
        row = layout.row()
        row.operator("object.removevcols", text = "Remove vertex colors (FIFA16)")
        row = layout.row()
        row.operator("object.vertexbrightness", text = "Adjust brightness")
        row = layout.row()
        row.operator("object.vertexbrightnight", text = "Adjust brightness for night, selected objects")
        row = layout.row()
        row.operator("object.createbakeimage", text = "Create bake image")
        row = layout.row()
        row.operator("object.getshadow", text = "Load shadow image")
        row = layout.row()
        row.operator("object.appendlights", text = "Append lights")
        row = layout.row()
        row.operator("mesh.subdivideevil", text = "Subdivide edge (repeat use)")
        
        layout.label(text="Choose Export Target:")
        layout.prop(scene, "quick_gltf_export_name", text="")
        layout.operator("export_scene.quick_gltf", icon="EXPORT")

