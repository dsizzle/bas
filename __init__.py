bl_info = { "name": "Blender Auto Studio", 
            "description": "Makes cahs",
            "version": (0, 1),
            "blender": (2, 80, 0),
            "category": "Object",
            "author": "Dale Cieslak"}

import importlib

import bpy

from . import bas
from . import bas_ui
from . import properties
from . import mesh_utils

importlib.reload(bas)
importlib.reload(bas_ui)
importlib.reload(properties)
importlib.reload(mesh_utils)

classes = (
    bas_ui.WM_OT_HatchbackType,
    bas_ui.WM_OT_MidsizeSedanType,
    bas_ui.WM_OT_LuxurySedanType,
    bas_ui.WM_OT_SportsGTType,
    bas_ui.WM_OT_SportsMidEngineType,

    bas_ui.WM_OT_225_65R17Type,
    bas_ui.WM_OT_235_45R18Type,
    bas_ui.WM_OT_235_60R18Type,
    bas_ui.WM_OT_245_60R18Type,
    bas_ui.WM_OT_235_40R19Type,
    bas_ui.WM_OT_275_55R20Type,

    bas_ui.OBJECT_MT_TirePresetMenu,
    bas_ui.OBJECT_MT_PresetMenu,
    bas_ui.OBJECT_PT_ToolPropsPanel,
    bas_ui.OBJECT_OT_ExecuteButton
)

register, unregister = bpy.utils.register_classes_factory(classes)

if __name__ == "__main__":
    register()

