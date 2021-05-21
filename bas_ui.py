import bpy
from . import bas

class WM_OT_HatchbackType(bpy.types.Operator):
    bl_label = "Hatchback"
    bl_idname = "wm.hatchback_type"

    def execute(self, context):
        scene = context.scene

        scene.TireWidth = 215
        scene.TireSidewall = 50
        scene.WheelDiameter = 17

        scene.Wheelbase = 3.25
        scene.FrontOverhang = 1
        scene.RearOverhang = 0.5
        scene.VehicleHeight = 2.33
        scene.WaistLine = 1.66
        scene.WindshieldAngle = 45
        scene.VehicleWidth = 1.45
        scene.WaistWidth = 1.17
        scene.RoofWidth = 0.8
        scene.CabPlacement = 'FWD'

        return {'FINISHED'}


class WM_OT_MidsizeSedanType(bpy.types.Operator):
    bl_label = "Midsize Sedan"
    bl_idname = "wm.midsize_sedan_type"

    def execute(self, context):
        scene = context.scene

        scene.TireWidth = 225
        scene.TireSidewall = 50
        scene.WheelDiameter = 17

        scene.Wheelbase = 3.5
        scene.FrontOverhang = 0.75
        scene.RearOverhang = 1
        scene.VehicleHeight = 2.25
        scene.WaistLine = 1.5
        scene.WindshieldAngle = 40
        scene.VehicleWidth = 1.5
        scene.WaistWidth = 1.17
        scene.RoofWidth = 0.8
        scene.CabPlacement = 'FWD'

        return {'FINISHED'}


class WM_OT_LuxurySedanType(bpy.types.Operator):
    bl_label = "Luxury Sedan"
    bl_idname = "wm.luxury_sedan_type"

    def execute(self, context):
        scene = context.scene

        scene.TireWidth = 245
        scene.TireSidewall = 50
        scene.WheelDiameter = 19

        scene.Wheelbase = 3.75
        scene.FrontOverhang = 0.75
        scene.RearOverhang = 1
        scene.VehicleHeight = 2.25
        scene.WaistLine = 1.5
        scene.WindshieldAngle = 35
        scene.VehicleWidth = 1.5
        scene.WaistWidth = 1.17
        scene.RoofWidth = 0.8
        scene.CabPlacement = 'RWD'

        return {'FINISHED'}


class WM_OT_SportsGTType(bpy.types.Operator):
    bl_label = "Sports GT"
    bl_idname = "wm.sports_gt_type"

    def execute(self, context):
        scene = context.scene

        scene.TireWidth = 235
        scene.TireSidewall = 50
        scene.WheelDiameter = 18

        scene.Wheelbase = 2.8
        scene.FrontOverhang = 0.5
        scene.RearOverhang = 0.5
        scene.VehicleHeight = 1.8
        scene.WaistLine = 1.33
        scene.WindshieldAngle = 30
        scene.VehicleWidth = 1.5
        scene.WaistWidth = 1.2
        scene.RoofWidth = 0.8
        scene.CabPlacement = 'RWD'

        return {'FINISHED'}


class WM_OT_SportsMidEngineType(bpy.types.Operator):
    bl_label = "Sports Mid-engine"
    bl_idname = "wm.sports_mid_engine_type"

    def execute(self, context):
        scene = context.scene

        scene.TireWidth = 245
        scene.TireSidewall = 35
        scene.WheelDiameter = 19

        scene.Wheelbase = 2.75
        scene.FrontOverhang = 0.75
        scene.RearOverhang = 0.5
        scene.VehicleHeight = 1.75
        scene.WaistLine = 1.33
        scene.WindshieldAngle = 25
        scene.VehicleWidth = 1.55
        scene.WaistWidth = 1.25
        scene.RoofWidth = 0.75
        scene.CabPlacement = 'MID'

        return {'FINISHED'}


class WM_OT_225_65R17Type(bpy.types.Operator):
    bl_label = "225/65R17"
    bl_idname = "wm.225_65r17_type"

    def execute(self, context):
        scene = context.scene

        scene.TireWidth = 225
        scene.TireSidewall = 65
        scene.WheelDiameter = 17

        return {'FINISHED'}


class WM_OT_235_45R18Type(bpy.types.Operator):
    bl_label = "235/45R18"
    bl_idname = "wm.235_45r18_type"

    def execute(self, context):
        scene = context.scene

        scene.TireWidth = 235
        scene.TireSidewall = 45
        scene.WheelDiameter = 18

        return {'FINISHED'}


class WM_OT_235_60R18Type(bpy.types.Operator):
    bl_label = "235/60R18"
    bl_idname = "wm.235_60r18_type"

    def execute(self, context):
        scene = context.scene

        scene.TireWidth = 235
        scene.TireSidewall = 60
        scene.WheelDiameter = 18

        return {'FINISHED'}


class WM_OT_245_60R18Type(bpy.types.Operator):
    bl_label = "245/60R18"
    bl_idname = "wm.245_60r18_type"

    def execute(self, context):
        scene = context.scene

        scene.TireWidth = 245
        scene.TireSidewall = 60
        scene.WheelDiameter = 18

        return {'FINISHED'}


class WM_OT_235_40R19Type(bpy.types.Operator):
    bl_label = "235/40R19"
    bl_idname = "wm.235_40r19_type"

    def execute(self, context):
        scene = context.scene

        scene.TireWidth = 235
        scene.TireSidewall = 40
        scene.WheelDiameter = 19

        return {'FINISHED'}


class WM_OT_275_55R20Type(bpy.types.Operator):
    bl_label = "275/55R20"
    bl_idname = "wm.275_55r20_type"

    def execute(self, context):
        scene = context.scene

        scene.TireWidth = 275
        scene.TireSidewall = 55
        scene.WheelDiameter = 20

        return {'FINISHED'}

class OBJECT_MT_PresetMenu(bpy.types.Menu):
    bl_label = "Vehicle Preset"
    bl_idname = "mt.preset_menu"

    def draw(self, context):
        layout = self.layout

        layout.operator(WM_OT_HatchbackType.bl_idname, text=WM_OT_HatchbackType.bl_label)
        #layout.operator(WM_OT_CompactSedanType.bl_idname, text=WM_OT_CompactSedanType.bl_label)
        layout.operator(WM_OT_MidsizeSedanType.bl_idname, text=WM_OT_MidsizeSedanType.bl_label)
        layout.operator(WM_OT_LuxurySedanType.bl_idname, text=WM_OT_LuxurySedanType.bl_label)
        layout.operator(WM_OT_SportsGTType.bl_idname, text=WM_OT_SportsGTType.bl_label)
        layout.operator(WM_OT_SportsMidEngineType.bl_idname, text=WM_OT_SportsMidEngineType.bl_label)


class OBJECT_MT_TirePresetMenu(bpy.types.Menu):
    bl_label = "Tire Preset"
    bl_idname = "mt.tire_preset_menu"

    def draw(self, context):
        layout = self.layout

        layout.operator(WM_OT_225_65R17Type.bl_idname, text=WM_OT_225_65R17Type.bl_label)
        layout.operator(WM_OT_235_45R18Type.bl_idname, text=WM_OT_235_45R18Type.bl_label)
        layout.operator(WM_OT_235_60R18Type.bl_idname, text=WM_OT_235_60R18Type.bl_label)
        layout.operator(WM_OT_245_60R18Type.bl_idname, text=WM_OT_245_60R18Type.bl_label)
        layout.operator(WM_OT_235_40R19Type.bl_idname, text=WM_OT_235_60R18Type.bl_label)
        layout.operator(WM_OT_275_55R20Type.bl_idname, text=WM_OT_235_60R18Type.bl_label)


# Set up panel layout
class OBJECT_PT_ToolPropsPanel(bpy.types.Panel):
    bl_label = "Blender Auto Studio"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    
    def draw(self, context):
        scene = context.scene
        layout = self.layout

        layout.menu(OBJECT_MT_TirePresetMenu.bl_idname, text=OBJECT_MT_TirePresetMenu.bl_label)
        
        layout.prop(scene, 'TireWidth')
        layout.prop(scene, 'TireSidewall')
        layout.prop(scene, 'WheelDiameter')
        layout.separator()

        layout.menu(OBJECT_MT_PresetMenu.bl_idname, text=OBJECT_MT_PresetMenu.bl_label)
        
        layout.prop(scene, 'Wheelbase')
        layout.prop(scene, 'FrontOverhang')
        layout.prop(scene, 'FrontCurve', slider=True)
        layout.prop(scene, 'FrontSlope', slider=True)
        layout.prop(scene, 'RearOverhang')
        layout.prop(scene, 'RearCurve', slider=True)
        layout.prop(scene, 'VehicleHeight')
        layout.prop(scene, 'WaistLine')
        layout.prop(scene, 'VehicleWidth')
        layout.prop(scene, 'WaistWidth')
        layout.prop(scene, 'RoofWidth')
        layout.prop(scene, 'WindshieldAngle')
        layout.prop(scene, 'WedgeAngle')
        layout.prop(scene, 'CabPlacement')

        layout.separator()
        #layout.prop(scene, 'AllObjects')
        layout.operator('execute.makecar')
    

class OBJECT_OT_ExecuteButton(bpy.types.Operator):
    bl_idname = "execute.makecar"
    bl_label = "Make Vehicle"

    def execute(self, context):
        bas.make_vehicle(context)

        return{'FINISHED'}