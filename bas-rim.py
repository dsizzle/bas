

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
    default = 50.0)

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
    default = 0, min=-0.9, max=0.9)

bpy.types.Scene.ET = IntProperty(
    name = "Insertion Depth (ET)",
    description = "Insertion depth",
    default = 38)

bpy.types.Scene.CenterDiameter = FloatProperty(
    name = "Center Diameter",
    description = "Size of center hub",
    default = 15)
    
bpy.types.Scene.SpokeCurveDepth = FloatProperty(
    name = "Spoke Curve Depth",
    description = "How much the spokes bulge outward or inward",
    default = 0)

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
        self.layout.prop(scene, 'SpokeCurveDepth')
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
        bpy.ops.wm.append(filename="base_rim", directory="D:/Projects/art/3d/vehicles/rim_model4.blend\\Object\\")
        bpy.ops.wm.append(filename="base_spokes", directory="D:/Projects/art/3d/vehicles/rim_model4.blend\\Object\\")
        
        num_spokes = scene.NumSpokes
        wheel_diam = scene.WheelDiameter * .0254 / .5  # divide by 25cm radius 

        wheel_width_half = scene.WheelWidth * .0254 / 2.0  
        center_diam = ( scene.CenterDiameter / 100. ) / .1   # .1 = 10cm (2 * radius of 5cm)
        mid_diam = ( (wheel_diam + (center_diam * .1)) / 2.0 ) / .55  

        et = scene.ET * .001 + .01

        one_deg = math.pi / 180.0
        rotation_angle = 2 * math.pi / num_spokes
        spoke_width = 2.5 * one_deg * scene.SpokeWidth
        
        taper = scene.SpokeTaper

        inner_taper = -.01
        outer_taper = .01

        if taper < 0:
            inner_taper = taper
        elif taper > 0:
            outer_taper = taper
            
        spoke_width_taper = spoke_width / (1.00 + taper)
        
        outer_spoke_width = (.05 * spoke_width) / (wheel_diam / 2.0)
        outer_spoke_width_taper = outer_spoke_width / (1.00 - taper)
        
        space_width = (rotation_angle - spoke_width_taper) / 2.

        mid_spoke_width = (.05 * spoke_width) / (mid_diam / 2.0)

        outer_space_width = (rotation_angle - outer_spoke_width_taper) / 2.0
        outer_space_width2 = rotation_angle / 2.0

        print ("------")
        print (rotation_angle, outer_spoke_width_taper, outer_space_width)
        print ("-=-=-")
        print (wheel_diam, mid_diam, center_diam)
        print (outer_spoke_width, mid_spoke_width, spoke_width)

        spoke_diff = (spoke_width_taper - outer_spoke_width_taper) / 2.0
        space_diff = (space_width - outer_space_width) / 2.0

        print (spoke_diff)

        spoke_curve_depth = scene.SpokeCurveDepth / 100

#15.766
#14.294

       

        # bpy.ops.object.select_all(action='DESELECT')
        # bpy.data.objects['RimRotateEmpty.001'].select = True
        # bpy.context.scene.objects.active = bpy.data.objects['RimRotateEmpty.001']
        # bpy.ops.transform.rotate(value=-rotation_angle, axis=(0, 0, 1.0))

        # bpy.ops.object.select_all(action='DESELECT')
        # bpy.data.objects['base_rim'].select = True
        # bpy.context.scene.objects.active = bpy.data.objects['base_rim']
        # bpy.ops.view3d.snap_cursor_to_selected()
        # bpy.context.space_data.pivot_point = 'CURSOR'
        # bpy.context.object.modifiers["Array"].count = num_spokes

        # bpy.ops.object.mode_set(mode='EDIT', toggle=False)
        # bpy.ops.object.vertex_group_set_active(group='outer_edge')
        # bpy.ops.mesh.select_all(action='DESELECT')
        # bpy.ops.object.vertex_group_select()
        # bpy.ops.transform.rotate(value=-(rotation_angle - (7 * one_deg)), axis=(0, 0, 1.0))
        # bpy.ops.mesh.select_all(action='DESELECT')

        # bpy.ops.object.vertex_group_set_active(group='spoke_center')
        # bpy.ops.mesh.select_all(action='DESELECT')
        # bpy.ops.object.vertex_group_select()
        # bpy.ops.transform.rotate(value=-((rotation_angle / 2.0) - (3.5 * one_deg)), axis=(0, 0, 1.0))
        # bpy.ops.mesh.select_all(action='DESELECT')

        # bpy.ops.object.mode_set(mode='EDIT', toggle=False)
        # bpy.ops.object.vertex_group_set_active(group='outer_mid')
        # bpy.ops.mesh.select_all(action='DESELECT')
        # bpy.ops.object.vertex_group_select()
        # bpy.ops.transform.rotate(value=-(rotation_angle - (outer_space_width2 / 2.0) - (6 * one_deg)), axis=(0, 0, 1.0))
        # bpy.ops.mesh.select_all(action='DESELECT')

        # bpy.ops.object.vertex_group_set_active(group='inner_mid')
        # bpy.ops.mesh.select_all(action='DESELECT')
        # bpy.ops.object.vertex_group_select()
        # bpy.ops.transform.rotate(value=-((outer_space_width2 / 2.0) - (1 * one_deg)), axis=(0, 0, 1.0))
        # bpy.ops.mesh.select_all(action='DESELECT')

        # bpy.ops.object.vertex_group_set_active(group='wheel_circumference')
        # bpy.ops.mesh.select_all(action='DESELECT')
        # bpy.ops.object.vertex_group_select()
        # bpy.ops.transform.resize(value=(wheel_diam, wheel_diam, 1.0), constraint_axis=(True, True, False))
        # bpy.ops.mesh.select_all(action='DESELECT')

        # bpy.ops.object.vertex_group_set_active(group='inner_circumference')
        # bpy.ops.mesh.select_all(action='DESELECT')
        # bpy.ops.object.vertex_group_select()
        # bpy.ops.transform.resize(value=(center_diam, center_diam, 1.0), constraint_axis=(True, True, False))
        # bpy.ops.mesh.select_all(action='DESELECT')

        # bpy.ops.object.vertex_group_set_active(group='outer_face')
        # bpy.ops.mesh.select_all(action='DESELECT')
        # bpy.ops.object.vertex_group_select()
        # bpy.ops.transform.translate(value=(0.0, 0.0, wheel_width_half - .25))
        # bpy.ops.mesh.select_all(action='DESELECT')

        # bpy.ops.object.vertex_group_set_active(group='inner_edge')
        # bpy.ops.mesh.select_all(action='DESELECT')
        # bpy.ops.object.vertex_group_select()
        # bpy.ops.transform.translate(value=(0.0, 0.0, -(wheel_width_half - .25)))
        # bpy.ops.mesh.select_all(action='DESELECT')
        
        # bpy.ops.object.vertex_group_set_active(group='center')
        # bpy.ops.mesh.select_all(action='DESELECT')
        # bpy.ops.object.vertex_group_select()
        # bpy.ops.transform.translate(value=(0.0, 0.0, -wheel_width_half + et))
        # bpy.ops.mesh.select_all(action='DESELECT')
        
        # bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
        #---

        bpy.ops.object.select_all(action='DESELECT')
        bpy.data.objects['spoke_rotate_empty'].select_set(True)
        bpy.context.view_layer.objects.active = bpy.data.objects['spoke_rotate_empty']
        bpy.ops.transform.rotate(value=-rotation_angle, orient_axis='Z') #(0, 0, 1.0))

        bpy.data.objects['base_rim'].select_set(False)
        bpy.data.objects['base_spokes'].select_set(True)
        bpy.context.view_layer.objects.active = bpy.data.objects['base_spokes']
        bpy.ops.view3d.snap_cursor_to_selected()
        # 2.7 # bpy.context.space_data.pivot_point = 'CURSOR'
        bpy.context.scene.tool_settings.transform_pivot_point = 'CURSOR'
        bpy.context.object.modifiers["Array"].count = num_spokes
        bpy.ops.object.mode_set(mode='EDIT', toggle=False)
        

        #---

        # outer_rotation = (rotation_angle - outer_space_width)
        # mid_rotation = ((rotation_angle / 2.0) )
        # inner_rotation = (rotation_angle - space_width)
        # outer_diff = ((outer_rotation + mid_rotation) / 2.0) - (rotation_angle / 2.0)
        # inner_diff = spoke_width / 4.0
        # mid_diff = (outer_diff + inner_diff) / 2.0

        # print(outer_rotation, mid_rotation, inner_rotation)

        # bpy.ops.object.vertex_group_set_active(group='spoke_outer_circ')
        # bpy.ops.mesh.select_all(action='DESELECT')
        # bpy.ops.object.vertex_group_select()
        # bpy.ops.transform.rotate(value=-(rotation_angle - outer_space_width - (4.0 * one_deg)), axis=(0, 0, 1.0))
        # bpy.ops.mesh.select_all(action='DESELECT')

        # bpy.ops.object.vertex_group_set_active(group='spoke_center')
        # bpy.ops.mesh.select_all(action='DESELECT')
        # bpy.ops.object.vertex_group_select()
        # bpy.ops.transform.rotate(value=-((rotation_angle / 2.0) - (2.0 * one_deg)), axis=(0, 0, 1.0))
        # bpy.ops.mesh.select_all(action='DESELECT')

        # bpy.ops.object.vertex_group_set_active(group='spoke_inner_circ')
        # bpy.ops.mesh.select_all(action='DESELECT')
        # bpy.ops.object.vertex_group_select()
        # bpy.ops.transform.rotate(value=-(outer_space_width - (0 * one_deg)), axis=(0, 0, 1.0))
        # bpy.ops.mesh.select_all(action='DESELECT')

        # bpy.ops.object.vertex_group_set_active(group='spoke_center_outer')
        # bpy.ops.mesh.select_all(action='DESELECT')
        # bpy.ops.object.vertex_group_select()
        # bpy.ops.transform.rotate(value=-((inner_diff / 2.0) - (3 * one_deg)), axis=(0, 0, 1.0))
        # bpy.ops.mesh.select_all(action='DESELECT')

        # bpy.ops.object.vertex_group_set_active(group='spoke_center_inner')
        # bpy.ops.mesh.select_all(action='DESELECT')
        # bpy.ops.object.vertex_group_select()
        # bpy.ops.transform.rotate(value=((inner_diff / 2.0) - (2 * one_deg)), axis=(0, 0, 1.0))
        # bpy.ops.mesh.select_all(action='DESELECT')

        # bpy.ops.object.vertex_group_set_active(group='spoke_midpoint')
        # bpy.ops.mesh.select_all(action='DESELECT')
        # bpy.ops.object.vertex_group_select()
        # bpy.ops.transform.resize(value=(mid_diam, mid_diam, 1.0), constraint_axis=(True, True, False))
        # bpy.ops.transform.translate(value=(0, 0, spoke_curve_depth))
        # bpy.ops.mesh.select_all(action='DESELECT')

        # bpy.ops.object.vertex_group_set_active(group='spoke_midpoint_inner')
        # bpy.ops.mesh.select_all(action='DESELECT')
        # bpy.ops.object.vertex_group_select()
        # bpy.ops.transform.rotate(value=((spoke_diff / 2.0)), axis=(0, 0, 1.0))
        # bpy.ops.mesh.select_all(action='DESELECT')

        # bpy.ops.object.vertex_group_set_active(group='spoke_midpoint_outer')
        # bpy.ops.mesh.select_all(action='DESELECT')
        # bpy.ops.object.vertex_group_select()
        # bpy.ops.transform.rotate(value=-((rotation_angle / 2.0) + (spoke_diff / 2.0)), axis=(0, 0, 1.0))
        # bpy.ops.mesh.select_all(action='DESELECT')

        # bpy.ops.object.vertex_group_set_active(group='spoke_outer_inner')
        # bpy.ops.mesh.select_all(action='DESELECT')
        # bpy.ops.object.vertex_group_select()
        # bpy.ops.transform.rotate(value=-((rotation_angle) - (spoke_width / 2.0)), axis=(0, 0, 1.0))
        # bpy.ops.mesh.select_all(action='DESELECT')

        # bpy.ops.object.vertex_group_set_active(group='spoke_inner_inner')
        # bpy.ops.mesh.select_all(action='DESELECT')
        # bpy.ops.object.vertex_group_select()
        # bpy.ops.transform.rotate(value=-( spoke_diff), axis=(0, 0, 1.0))
        # bpy.ops.mesh.select_all(action='DESELECT')

        # bpy.ops.object.vertex_group_set_active(group='spoke_circ_outer')
        # bpy.ops.mesh.select_all(action='DESELECT')
        # bpy.ops.object.vertex_group_select()
        # bpy.ops.transform.rotate(value=-(outer_diff - (3 * one_deg)), axis=(0, 0, 1.0))
        # bpy.ops.mesh.select_all(action='DESELECT')

        # bpy.ops.object.vertex_group_set_active(group='spoke_circ_inner')
        # bpy.ops.mesh.select_all(action='DESELECT')
        # bpy.ops.object.vertex_group_select()
        # bpy.ops.transform.rotate(value=(outer_diff - (3 * one_deg)), axis=(0, 0, 1.0))
        # bpy.ops.mesh.select_all(action='DESELECT')

        # bpy.ops.object.vertex_group_set_active(group='spoke_mid_outer')
        # bpy.ops.mesh.select_all(action='DESELECT')
        # bpy.ops.object.vertex_group_select()
        # bpy.ops.transform.rotate(value=-((mid_diff / 2.0) - (3 * one_deg)), axis=(0, 0, 1.0))
        # bpy.ops.mesh.select_all(action='DESELECT')

        # bpy.ops.object.vertex_group_set_active(group='spoke_mid_inner')
        # bpy.ops.mesh.select_all(action='DESELECT')
        # bpy.ops.object.vertex_group_select()
        # bpy.ops.transform.rotate(value=((mid_diff / 2.0) - (3 * one_deg)), axis=(0, 0, 1.0))
        # bpy.ops.mesh.select_all(action='DESELECT')
        # --- 

        bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
        bpy.ops.object.select_all(action='DESELECT')
        bpy.data.objects['base_rim'].select_set(True)
        bpy.context.view_layer.objects.active = bpy.data.objects['base_rim']
        bpy.ops.view3d.snap_cursor_to_selected()
        #bpy.context.space_data.pivot_point = 'CURSOR'
        bpy.context.scene.tool_settings.transform_pivot_point = 'CURSOR'
        #bpy.context.object.modifiers["Array"].count = num_spokes
        bpy.ops.object.mode_set(mode='EDIT', toggle=False)

        bpy.ops.object.vertex_group_set_active(group='rim_outer')
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.vertex_group_select()
        bpy.ops.transform.resize(value=(wheel_diam, wheel_diam, 1.0), constraint_axis=(True, True, False))
        bpy.ops.mesh.select_all(action='DESELECT')

        bpy.ops.object.vertex_group_set_active(group='rim_inner')
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.vertex_group_select()
        bpy.ops.transform.resize(value=(wheel_diam, wheel_diam, 1.0), constraint_axis=(True, True, False))
        bpy.ops.mesh.select_all(action='DESELECT')

        bpy.ops.object.vertex_group_set_active(group='rim_profile')
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.vertex_group_select()
        bpy.ops.transform.translate(value=(0.0, 0.0, wheel_width_half - .5))
        bpy.ops.mesh.select_all(action='DESELECT')

        bpy.ops.object.vertex_group_set_active(group='rim_inside')
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.vertex_group_select()
        bpy.ops.transform.translate(value=(0.0, 0.0, -(wheel_width_half - .5)))
        bpy.ops.mesh.select_all(action='DESELECT')        

        bpy.ops.object.mode_set(mode='OBJECT', toggle=False)

        return{'FINISHED'}

__classes__ = (
    ToolPropsPanel,
    OBJECT_OT_ExecuteButton
)

def register():
    for c in __classes__:
        bpy.utils.register_class(c)
    #bpy.utils.register_module(__name__)

def unregister():
    for c in __classes__:
        bpy.utils.unregister_class(c)
    #bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()

