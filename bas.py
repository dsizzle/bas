#
# bas.py
#
#
bl_info = { "name": "Blender Auto Studio", 
            "description": "Makes cahs",
            "version": (0, 1),
            "blender": (2, 79, 0),
            "category": "Object",
            "author": "Dale Cieslak"}

import bpy
import math
from bpy.props import *

# Store properties in the active scene
#
bpy.types.Scene.TireWidth = FloatProperty(
    name = "Tire Width", 
    description = "Width of tire",
    default = 215)

bpy.types.Scene.TireDiameter = FloatProperty(
    name = "Tire Outside Diameter", 
    description = "Diameter of tire",
    default = 24)
 
bpy.types.Scene.WheelDiameter = FloatProperty(
    name = "Wheel Size", 
    description = "Diameter of wheel",
    default = 19)
 
bpy.types.Scene.Wheelbase = FloatProperty(
    name = "Wheelbase",
    description = "Number of wheels between wheels",
    default = 3.0)

bpy.types.Scene.VehicleWidth = FloatProperty(
    name = "Vehicle Width",
    description = "Width of vehicle based on wheel size",
    default = 1.5)

bpy.types.Scene.RoofWidth = FloatProperty(
    name = "Roof Width",
    description = "Width of roof based on wheel size",
    default = 0.8)

bpy.types.Scene.FrontOverhang = FloatProperty(
    name = "Front Overhang",
    description = "Number of wheels in front of front wheel",
    default = 0.5,
    min = 0.25, max = 2.5)

bpy.types.Scene.RearOverhang = FloatProperty(
    name = "Rear Overhang",
    description = "Number of wheels to rear of rear wheel",
    default = 0.5,
    min = 0.25, max = 2.5)

bpy.types.Scene.WindshieldAngle = FloatProperty(
    name = "Windshield Angle",
    description = "Angle of windshield",
    default = 40.0,
    min = 20.0, max = 89.0)
    
bpy.types.Scene.MinSubd = IntProperty(
    name = "Min. SubD level",
    description = "minimum subd level for farthest object",
    default = 0)
    
bpy.types.Scene.AllObjects = BoolProperty(
    name="Affect All Objects",
    default = True)

    
# Set up panel layout
class ToolPropsPanel(bpy.types.Panel):

    bl_label = "Blender Auto Studio"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    
    def draw(self, context):
        scene = context.scene
       
        self.layout.prop(scene, 'TireWidth')
        self.layout.prop(scene, 'TireDiameter')
        self.layout.prop(scene, 'WheelDiameter')
        self.layout.separator()

        self.layout.prop(scene, 'Wheelbase')
        self.layout.prop(scene, 'FrontOverhang')
        self.layout.prop(scene, 'RearOverhang')
        self.layout.prop(scene, 'VehicleWidth')
        self.layout.prop(scene, 'RoofWidth')
        
        self.layout.prop(scene, 'WindshieldAngle')

        self.layout.separator()
        self.layout.prop(scene, 'AllObjects')
        self.layout.operator('execute.makecar')
    

class OBJECT_OT_ExecuteButton(bpy.types.Operator):
    bl_idname = "execute.makecar"
    bl_label = "Make Vehicle"

    def execute(self, context):
        scene = context.scene
        override = context.copy() # dictionary of context

        diam = scene.TireDiameter * .0254
        half_diam = diam / 2.0
        quarter_diam = diam / 4.0
        wheel_diam = scene.WheelDiameter * .0254
        sidewall_diam = ((diam / 2.) + wheel_diam) / 2.0
        width = scene.TireWidth / 1000.0
        dist_from_center_y = (diam * scene.Wheelbase) / 2. + (diam / 2.)
        dist_from_center_x = (diam * scene.VehicleWidth) - (width / 2.)
        front_overhang = (diam * scene.FrontOverhang) 
        rear_overhang = (diam * scene.RearOverhang) 
        overhang_diff = rear_overhang - front_overhang
        height = diam * 1.75
        shoulder_height = diam * 1.3
        shoulder_width = diam * 1.2
        roof_width = diam * scene.RoofWidth
        windshield_angle = scene.WindshieldAngle

        # load wheel
        bpy.ops.wm.append(filename="base_tire", directory="D:/Projects/art/3d/vehicles/wheel_model.blend\\Object\\")
        bpy.ops.wm.append(filename="base_vehicle", directory="D:/Projects/art/3d/vehicles/car_model.blend\\Object\\")
        
        #---------------- ??
        #wheel_mesh = bpy.context.object.data
        #bm = bmesh.from_edit_mesh(wheel_mesh)
        
        #bm.update_edit_mesh(wheel_mesh, True)
        #---------------- ??
        
        bpy.ops.object.select_all(action='DESELECT')
        bpy.data.objects['base_tire'].select = True
        bpy.context.scene.objects.active = bpy.data.objects['base_tire']
        bpy.ops.view3d.snap_cursor_to_selected()
        bpy.context.space_data.pivot_point = 'CURSOR'
        bpy.ops.object.mode_set(mode='EDIT', toggle=False)
        bpy.ops.object.vertex_group_set_active(group='tire_inner_vertices')
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.vertex_group_select()
        bpy.ops.transform.resize(value=(wheel_diam * 2.0, wheel_diam * 2.0, 1.0), constraint_axis=(True, True, False))
        bpy.ops.object.vertex_group_set_active(group='tire_outer_vertices')
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.vertex_group_select()
        bpy.ops.transform.resize(value=(diam, diam, 1.0), constraint_axis=(True, True, False))
        bpy.ops.object.vertex_group_set_active(group='tire_sidewall_vertices')
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.vertex_group_select()
        bpy.ops.transform.resize(value=(sidewall_diam, sidewall_diam, 1.0), constraint_axis=(True, True, False))        
        bpy.ops.object.vertex_group_set_active(group='tire_profile_vertices')
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.vertex_group_select()
        bpy.ops.transform.translate(value=(0.0, 0.0, -0.5+(width/2.)), constraint_axis=(False, False, True))        
        bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
        bpy.ops.object.modifier_apply(modifier='Array')
        bpy.ops.transform.rotate(value=1.5708, axis=(0.0, 1.0, 0.0))
        bpy.context.object.name="rear_left_wheel"
        bpy.ops.transform.translate(value=(dist_from_center_x, dist_from_center_y, half_diam))
        bpy.ops.object.duplicate()
        bpy.context.object.name="rear_right_wheel"
        bpy.ops.transform.translate(value=(-dist_from_center_x*2., 0, 0))
        bpy.ops.object.duplicate()
        bpy.context.object.name="front_right_wheel"
        bpy.ops.transform.translate(value=(0, -dist_from_center_y*2., 0))
        bpy.ops.object.duplicate()
        bpy.context.object.name="front_left_wheel"
        bpy.ops.transform.translate(value=(dist_from_center_x*2., 0, 0))
                        
        bpy.ops.object.empty_add(type='CUBE', location=(0, 0, 0))
        bpy.context.object.scale=(dist_from_center_x + width / 2., \
            ((dist_from_center_y * 2) + front_overhang + rear_overhang + diam) / 2., \
            height / 2.)
        bpy.context.object.location=(0, overhang_diff / 2., height/ 2.)
        bpy.context.object.name="vehicle_bounding_box"

        bpy.ops.object.select_all(action='DESELECT')
        bpy.data.objects['base_vehicle'].select = True
        bpy.context.scene.objects.active = bpy.data.objects['base_vehicle']
        bpy.ops.object.mode_set(mode='EDIT', toggle=False)
        bpy.ops.object.vertex_group_set_active(group='front_vertices')
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.vertex_group_select()
        bpy.ops.transform.translate(value=(0, 0-(dist_from_center_y + front_overhang + half_diam - 2.0), 0))
        
        bpy.ops.object.vertex_group_set_active(group='front_wheel_front_well_vertices')
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.vertex_group_select()
        bpy.ops.transform.translate(value=(0, diam * 1.1 - 0.5, 0))        
        bpy.ops.object.vertex_group_set_active(group='front_wheel_rear_well_vertices')
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.vertex_group_select()
        bpy.ops.transform.translate(value=(0, diam * 1.1 - 0.85, 0))
        bpy.ops.object.vertex_group_set_active(group='front_wheel_vertices')
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.vertex_group_select()
        bpy.ops.transform.translate(value=(0, 0-(dist_from_center_y - 1.0), 0))
        
        bpy.ops.object.vertex_group_set_active(group='rear_vertices')
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.vertex_group_select()
        bpy.ops.transform.translate(value=(0, dist_from_center_y + rear_overhang + half_diam - 2.0, 0))

        bpy.ops.object.vertex_group_set_active(group='rear_wheel_front_well_vertices')
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.vertex_group_select()
        bpy.ops.transform.translate(value=(0, diam * 1.1 - 0.5, 0))        
        bpy.ops.object.vertex_group_set_active(group='rear_wheel_rear_well_vertices')
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.vertex_group_select()
        bpy.ops.transform.translate(value=(0, diam * 1.1 - 0.85, 0))
        bpy.ops.object.vertex_group_set_active(group='rear_wheel_vertices')
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.vertex_group_select()
        bpy.ops.transform.translate(value=(0, dist_from_center_y - 1.0, 0))
        
        #rear_wheel_rear_well_vertices
        #rear_wheel_front_well_vertices

        bpy.ops.object.vertex_group_set_active(group='side_vertices')
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.vertex_group_select()
        bpy.ops.transform.translate(value=(dist_from_center_x + width / 2. - 1.0, 0, 0))

        bpy.ops.object.vertex_group_set_active(group='roof_side_vertices')
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.vertex_group_select()
        bpy.ops.transform.translate(value=(roof_width - 1.0, 0, 0))

        bpy.ops.object.vertex_group_set_active(group='hip_vertices')
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.vertex_group_select()
        bpy.ops.transform.translate(value=(0, 0, diam * 1.1 - .75))

        bpy.ops.object.vertex_group_set_active(group='skirt_vertices')
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.vertex_group_select()
        bpy.ops.transform.translate(value=(0, 0, quarter_diam))

        bpy.ops.object.vertex_group_set_active(group='midline_vertices')
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.vertex_group_select()
        bpy.ops.transform.translate(value=(0, 0, quarter_diam + half_diam - 0.5))

        bpy.ops.object.vertex_group_set_active(group='roof_vertices')
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.vertex_group_select()
        bpy.ops.transform.translate(value=(0, 0, height - 2.0))

        bpy.ops.object.vertex_group_set_active(group='shoulder_vertices')
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.vertex_group_select()
        bpy.ops.transform.translate(value=(0, 0, shoulder_height - 1.0))

        bpy.ops.object.vertex_group_set_active(group='centerline_vertices')
        bpy.ops.object.vertex_group_deselect()
        bpy.ops.transform.translate(value=(shoulder_width - 1.0, 0, 0))
 
        windshield_rads = math.radians(windshield_angle)
        base_y = (shoulder_height - half_diam) / math.tan(windshield_rads)
        print(math.tan(windshield_rads), base_y)
        top_y = (height - half_diam) / math.tan(windshield_rads)
        print(top_y)

        bpy.ops.object.vertex_group_set_active(group='windshield_base_vertices')
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.vertex_group_select()
        bpy.ops.transform.translate(value=(0, 0 - dist_from_center_y + base_y + 0.5, 0))

        bpy.ops.object.vertex_group_set_active(group='windshield_top_vertices')
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.vertex_group_select()
        bpy.ops.transform.translate(value=(0, 0 - dist_from_center_y + top_y + 0.5, 0))

        bpy.ops.object.vertex_group_set_active(group='front_back_midline_vertices')
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.vertex_group_select()
        bpy.ops.transform.translate(value=(0, 0 - dist_from_center_y + top_y + 0.75, 0))
        bpy.ops.mesh.select_all(action='DESELECT')

        bpy.ops.object.mode_set(mode='OBJECT', toggle=False)

        return{'FINISHED'}

def register():
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()

