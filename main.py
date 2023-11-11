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
        # Create simple rows
        # Create simple row
        row = layout.row()
        row.label(text = "Import GLTF and scale")
        row = layout.row()
        row.operator("object.initialimport0", text = "Import stad_0")
        row = layout.row()
        row.operator("object.initialimport1", text = "Import stad_1")
        row = layout.row()
        row.operator("object.initialimport3", text = "Import stad_3")
        # Create simple row
        row = layout.row()
        row.label(text = "Crowd modification")
        row = layout.row()
        row.operator("object.crowdsplit", text = "Crowd Split")
        row = layout.row()
        row.operator("object.crowdfifa16", text = "Crowd FIFA16")
        row = layout.row()
        row.operator("object.crowdpes6", text = "Crowd PES6")
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
        row.operator("object.scaleempties", text = "Scale empties")