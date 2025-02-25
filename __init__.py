bl_info = {
    "name": "FM Specific Addons",
    "blender": (3, 10, 1),
    "category": "Object",
}

import bpy
import sys
# Your script code here
from . import main  # Replace with your script file name
from .methods.initial_import0 import INITIAL_IMPORT0
from .methods.initial_import1 import INITIAL_IMPORT1
from .methods.initial_import3 import INITIAL_IMPORT3
from .methods.vertex_tolightglow import VERTEX_TOLIGHTGLOW
from .methods.bake_trans import BAKE_TRANS
from .methods.texture_split import TEXTURE_SPLIT
from .methods.remove_vg import REMOVE_VG
from .methods.scale_empties import SCALE_EMPTIES
from .methods.adbb_attach import ADBB_ATTACH
from .methods.crowd_fifa16 import CROWD_FIFA16
from .methods.crowd_pes6 import CROWD_PES6
from .methods.crowd_split import CROWD_SPLIT
from .methods.generic_grass import GENERIC_GRASS
from .methods.alpha_to_opaque import ALPHA_TO_OPAQUE
from .methods.pes2020_matremove import PES2020_MATREMOVE
from .methods.remove_vcols import REMOVE_VCOLS
from .methods.vertex_brightness import VERTEX_BRIGHTNESS
from .methods.vertex_brightnight import VERTEX_BRIGHTNIGHT
from .methods.create_bakeimage import CREATE_BAKEIMAGE
from .methods.get_shadow import GET_SHADOW

def register():
    bpy.utils.register_class(main.PANEL_CUSTOM_UI)
    bpy.utils.register_class(INITIAL_IMPORT0)
    bpy.utils.register_class(INITIAL_IMPORT1)
    bpy.utils.register_class(INITIAL_IMPORT3)
    bpy.utils.register_class(BAKE_TRANS)
    bpy.utils.register_class(VERTEX_TOLIGHTGLOW)
    bpy.utils.register_class(TEXTURE_SPLIT)
    bpy.utils.register_class(REMOVE_VG)
    bpy.utils.register_class(SCALE_EMPTIES)
    bpy.utils.register_class(ADBB_ATTACH)
    bpy.utils.register_class(CROWD_FIFA16)
    bpy.utils.register_class(CROWD_PES6)
    bpy.utils.register_class(CROWD_SPLIT)
    bpy.utils.register_class(GENERIC_GRASS)
    bpy.utils.register_class(PES2020_MATREMOVE)
    bpy.utils.register_class(ALPHA_TO_OPAQUE)
    bpy.utils.register_class(REMOVE_VCOLS)
    bpy.utils.register_class(VERTEX_BRIGHTNESS)
    bpy.utils.register_class(VERTEX_BRIGHTNIGHT)
    bpy.utils.register_class(CREATE_BAKEIMAGE)
    bpy.utils.register_class(GET_SHADOW)

def unregister():
    bpy.utils.unregister_class(main.PANEL_CUSTOM_UI)
    bpy.utils.unregister_class(INITIAL_IMPORT0)
    bpy.utils.unregister_class(INITIAL_IMPORT1)
    bpy.utils.unregister_class(INITIAL_IMPORT3)
    bpy.utils.unregister_class(BAKE_TRANS)
    bpy.utils.unregister_class(VERTEX_TOLIGHTGLOW)
    bpy.utils.unregister_class(TEXTURE_SPLIT)
    bpy.utils.unregister_class(REMOVE_VG)
    bpy.utils.unregister_class(SCALE_EMPTIES)
    bpy.utils.unregister_class(ADBB_ATTACH)
    bpy.utils.unregister_class(CROWD_FIFA16)
    bpy.utils.unregister_class(CROWD_PES6)
    bpy.utils.unregister_class(CROWD_SPLIT)
    bpy.utils.unregister_class(GENERIC_GRASS)
    bpy.utils.unregister_class(PES2020_MATREMOVE)
    bpy.utils.unregister_class(ALPHA_TO_OPAQUE)
    bpy.utils.unregister_class(REMOVE_VCOLS)
    bpy.utils.unregister_class(VERTEX_BRIGHTNESS)
    bpy.utils.unregister_class(VERTEX_BRIGHTNIGHT)
    bpy.utils.unregister_class(CREATE_BAKEIMAGE)
    bpy.utils.unregister_class(GET_SHADOW)

if __name__ == "__main__":
    register()
