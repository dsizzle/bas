

# # for RimRotateEmpty
# bpy.context.object.rotation_euler[2] = 2 * math.pi / num



#
# bas.py
#
#
bl_info = { "name": "Blender Rim Studio", 
            "description": "Makes rims",
            "version": (0, 1),
            "blender": (2, 79, 0),
            "category": "Object",
            "author": "Dale Cieslak"}

import bpy
import math
from bpy.props import *

# Store properties in the active scene
#
bpy.types.Scene.NumSpokes = IntProperty(
    name = "Spokes", 
    description = "Number of spokes",
    default = 5)

bpy.types.Scene.SpokeWidth = FloatProperty(
    name = "Spoke Width",
    description = "Width of spoke",
    default = 20.0)

bpy.types.Scene.WheelDiameter = FloatProperty(
    name = "Wheel Diameter", 
    description = "Diameter of wheel",
    default = 19)

bpy.types.Scene.WheelWidth = FloatProperty(
    name = "Wheel Width", 
    description = "Width of wheel",
    default = 6.5)

bpy.types.Scene.SpokeTaper = FloatProperty(
    name = "Spoke Taper",
    description = "Taper of spoke from inner to outer",
    default = 0)

bpy.types.Scene.ET = IntProperty(
    name = "Insertion Depth (ET)",
    description = "Insertion depth",
    default = 38)

bpy.types.Scene.CenterDiameter = FloatProperty(
    name = "Center Diameter",
    description = "Size of center hub",
    default = 15)
    
# Set up panel layout
class ToolPropsPanel(bpy.types.Panel):

    bl_label = "Blender Rim Studio"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    
    def draw(self, context):
        scene = context.scene
       
        self.layout.prop(scene, 'WheelDiameter')
        self.layout.prop(scene, 'WheelWidth')
        self.layout.prop(scene, 'NumSpokes')
        self.layout.prop(scene, 'SpokeWidth')
        self.layout.prop(scene, 'SpokeTaper')
        self.layout.prop(scene, 'CenterDiameter')
        self.layout.prop(scene, 'ET')

        self.layout.operator('execute.makerim')
    

class OBJECT_OT_ExecuteButton(bpy.types.Operator):
    bl_idname = "execute.makerim"
    bl_label = "Make Rim"

    def execute(self, context):
        scene = context.scene
        override = context.copy() # dictionary of context

        #bpy.ops.object.mode_set(mode='OBJECT', toggle=False)

        # load wheel
        #++bpy.ops.wm.append(filename="RimRotateEmpty", directory="D:/Projects/art/3d/vehicles/rim_model.blend\\Object\\")
        
        bpy.ops.wm.append(filename="base_rim", directory="D:/Projects/art/3d/vehicles/rim_model.blend\\Object\\")
        
        num_spokes = scene.NumSpokes
        wheel_diam = scene.WheelDiameter * .0254
        wheel_width_half = scene.WheelWidth * .0254 / 2.0
        center_diam = scene.CenterDiameter / 100.0
        mid_diam = ( (wheel_diam - center_diam) / 2.0 ) + center_diam

        print (wheel_diam, center_diam, mid_diam)
        et = scene.ET * .001 + .01

        one_deg = math.pi / 180.0
        rotation_angle = 2 * math.pi / num_spokes
        spoke_width = one_deg * scene.SpokeWidth
        space_width = (rotation_angle - spoke_width) / 2
        taper = scene.SpokeTaper

        outer_spoke_width = (.05 * spoke_width) / (wheel_diam / 2.0)
        outer_space_width = (rotation_angle - outer_spoke_width) / 2.0
        
        spoke_diff = outer_spoke_width - spoke_width / 2.0
        space_diff = outer_space_width - space_width / 2.0

        bpy.ops.object.select_all(action='DESELECT')
        bpy.data.objects['RimRotateEmpty'].select = True
        bpy.context.scene.objects.active = bpy.data.objects['RimRotateEmpty']
        bpy.ops.transform.rotate(value=-rotation_angle, axis=(0, 0, 1.0))

        bpy.ops.object.select_all(action='DESELECT')
        bpy.data.objects['base_rim'].select = True
        bpy.context.scene.objects.active = bpy.data.objects['base_rim']
        bpy.ops.view3d.snap_cursor_to_selected()
        bpy.context.space_data.pivot_point = 'CURSOR'
        bpy.context.object.modifiers["Array"].count = num_spokes

        bpy.ops.object.mode_set(mode='EDIT', toggle=False)
        bpy.ops.object.vertex_group_set_active(group='outer_edge')
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.vertex_group_select()
        bpy.ops.transform.rotate(value=-(rotation_angle - (6 * one_deg)), axis=(0, 0, 1.0))
        bpy.ops.mesh.select_all(action='DESELECT')

        bpy.ops.object.mode_set(mode='EDIT', toggle=False)
        bpy.ops.object.vertex_group_set_active(group='outer_mid')
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.vertex_group_select()
        bpy.ops.transform.rotate(value=-(rotation_angle - (outer_space_width / 2.0) - (5 * one_deg)), axis=(0, 0, 1.0))
        bpy.ops.mesh.select_all(action='DESELECT')
        
        bpy.ops.object.vertex_group_set_active(group='spoke_outer_edge')
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.vertex_group_select()
        bpy.ops.transform.rotate(value=-(rotation_angle - outer_space_width - (4 * one_deg)), axis=(0, 0, 1.0))
        bpy.ops.mesh.select_all(action='DESELECT')

        bpy.ops.object.vertex_group_set_active(group='spoke_center')
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.vertex_group_select()
        bpy.ops.transform.rotate(value=-((rotation_angle / 2.0) - (3 * one_deg)), axis=(0, 0, 1.0))
        bpy.ops.mesh.select_all(action='DESELECT')

        bpy.ops.object.vertex_group_set_active(group='spoke_inner_edge')
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.vertex_group_select()
        bpy.ops.transform.rotate(value=-(outer_space_width - (2 * one_deg)), axis=(0, 0, 1.0))
        bpy.ops.mesh.select_all(action='DESELECT')

        bpy.ops.object.vertex_group_set_active(group='inner_mid')
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.vertex_group_select()
        bpy.ops.transform.rotate(value=-((outer_space_width / 2.0) - (1 * one_deg)), axis=(0, 0, 1.0))
        bpy.ops.mesh.select_all(action='DESELECT')
        
        bpy.ops.object.vertex_group_set_active(group='spoke_outer_inner')
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.vertex_group_select()
        bpy.ops.transform.rotate(value=spoke_diff/2.0, axis=(0, 0, 1.0))
        bpy.ops.mesh.select_all(action='DESELECT')

        bpy.ops.object.vertex_group_set_active(group='spoke_inner_inner')
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.vertex_group_select()
        bpy.ops.transform.rotate(value=-spoke_diff/2.0, axis=(0, 0, 1.0))
        bpy.ops.mesh.select_all(action='DESELECT')

        bpy.ops.object.vertex_group_set_active(group='inner_inner_mid')
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.vertex_group_select()
        bpy.ops.transform.rotate(value=space_diff/4, axis=(0, 0, 1.0))
        bpy.ops.mesh.select_all(action='DESELECT')

        bpy.ops.object.vertex_group_set_active(group='inner_outer_mid')
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.vertex_group_select()
        bpy.ops.transform.rotate(value=-space_diff/4, axis=(0, 0, 1.0))
        bpy.ops.mesh.select_all(action='DESELECT')

        bpy.ops.object.vertex_group_set_active(group='wheel_circumference')
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.vertex_group_select()
        bpy.ops.transform.resize(value=(wheel_diam * 2.0, wheel_diam * 2.0, 1.0), constraint_axis=(True, True, False))
        bpy.ops.mesh.select_all(action='DESELECT')

        bpy.ops.object.vertex_group_set_active(group='inner_circumference')
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.vertex_group_select()
        bpy.ops.transform.resize(value=(center_diam * 10, center_diam * 10, 1.0), constraint_axis=(True, True, False))
        bpy.ops.mesh.select_all(action='DESELECT')

        # bpy.ops.object.vertex_group_set_active(group='spoke_midpoint')
        # bpy.ops.mesh.select_all(action='DESELECT')
        # bpy.ops.object.vertex_group_select()
        # bpy.ops.transform.resize(value=(mid_diam * 10. / 15., mid_diam * 10. / 15., 1.0), constraint_axis=(True, True, False))
        # bpy.ops.mesh.select_all(action='DESELECT')


        bpy.ops.object.vertex_group_set_active(group='outer_face')
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.vertex_group_select()
        bpy.ops.transform.translate(value=(0.0, 0.0, wheel_width_half - .25))
        bpy.ops.mesh.select_all(action='DESELECT')

        bpy.ops.object.vertex_group_set_active(group='inner_edge')
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.vertex_group_select()
        bpy.ops.transform.translate(value=(0.0, 0.0, -(wheel_width_half - .25)))
        bpy.ops.mesh.select_all(action='DESELECT')
        
        bpy.ops.object.vertex_group_set_active(group='center')
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.vertex_group_select()
        bpy.ops.transform.translate(value=(0.0, 0.0, -wheel_width_half + et))
        bpy.ops.mesh.select_all(action='DESELECT')
        

        bpy.ops.object.mode_set(mode='OBJECT', toggle=False)

        return{'FINISHED'}

def register():
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()

