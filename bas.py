#
# bas.py
#
#

import bpy
import bmesh
import math

from .mesh_utils import *

def make_wheel(tire_obj, tire_diam, tire_width, wheel_diam):
    sidewall_diam = tire_diam * 3. / 4.
    
    bpy.ops.object.select_all(action='DESELECT')
    tire_obj.select_set(True)
    bpy.context.view_layer.objects.active = tire_obj
    bpy.ops.view3d.snap_cursor_to_selected()
    bpy.context.scene.tool_settings.transform_pivot_point = 'CURSOR'
    bpy.ops.object.mode_set(mode='EDIT', toggle=False)
    bpy.ops.object.vertex_group_set_active(group='tire_inner_vertices')
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.vertex_group_select()
    bpy.ops.transform.resize(value=(wheel_diam * 2.0, wheel_diam * 2.0, 1.0), constraint_axis=(True, True, False))
    bpy.ops.object.vertex_group_set_active(group='tire_outer_vertices')
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.vertex_group_select()
    bpy.ops.transform.resize(value=(tire_diam, tire_diam, 1.0), constraint_axis=(True, True, False))
    bpy.ops.object.vertex_group_set_active(group='tire_sidewall_vertices')
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.vertex_group_select()
    bpy.ops.transform.resize(value=(sidewall_diam, sidewall_diam, 1.0), constraint_axis=(True, True, False))        
    bpy.ops.object.vertex_group_set_active(group='tire_profile_vertices')
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.vertex_group_select()
    bpy.ops.transform.translate(value=(0.0, 0.0, -0.5+(tire_width/2.)))#, constraint_axis=(False, False, True))        
    
    bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
    bpy.ops.object.modifier_apply(modifier='Array')
    bpy.ops.transform.rotate(value=1.5708, orient_axis='Y')
    bpy.ops.transform.translate(value=(0.0, 0.0, tire_diam/2.))

def place_wheels(tire_obj, dist_from_center_x, dist_from_center_y):
    bpy.ops.object.select_all(action='DESELECT')
    tire_obj.select_set(True)
    bpy.context.view_layer.objects.active = tire_obj
    bpy.context.object.name="rear_left_wheel"
    bpy.ops.transform.translate(value=(dist_from_center_x, dist_from_center_y, 0))
    bpy.ops.object.duplicate()
    bpy.context.object.name="rear_right_wheel"
    bpy.ops.transform.translate(value=(-dist_from_center_x*2., 0, 0))
    bpy.ops.object.duplicate()
    bpy.context.object.name="front_right_wheel"
    bpy.ops.transform.translate(value=(0, -dist_from_center_y*2., 0))
    bpy.ops.object.duplicate()
    bpy.context.object.name="front_left_wheel"
    bpy.ops.transform.translate(value=(dist_from_center_x*2., 0, 0))

def make_vehicle(context):
    scene = context.scene
    override = context.copy() # dictionary of context

    diam = (scene.TireWidth * scene.TireSidewall / 2540. * 2 ) + scene.WheelDiameter
    diam = diam * .0254
    half_diam = diam / 2.0
    quarter_diam = diam / 4.0
    wheel_diam = scene.WheelDiameter * .0254
    tire_width = scene.TireWidth / 1000.0
    dist_from_center_y = (diam * scene.Wheelbase) / 2. + (half_diam)
    dist_from_center_y_in = (diam * scene.Wheelbase) / 2.
    dist_from_center_x = (diam * scene.VehicleWidth) - (tire_width / 2.)
    front_overhang = (diam * scene.FrontOverhang) 
    rear_overhang = (diam * scene.RearOverhang) 
    overhang_diff = rear_overhang - front_overhang
    height = diam * scene.VehicleHeight
    top_line_height = diam * scene.WaistLine
    top_line_width = diam * scene.WaistWidth
    roof_width = diam * scene.RoofWidth
    wheel_gap = 0.05
    shoulder_line_height = diam * (1+(wheel_gap*2))
    wheel_arch_width = 0.1
    wedge_rads = scene.WedgeAngle * math.pi / 180.

    # save selection first?
    bpy.ops.object.select_all(action='DESELECT')
    
    vehicle_collection = bpy.data.collections.new("vehicle")
    bpy.context.scene.collection.children.link(vehicle_collection)
    vehicle_root=bpy.context.view_layer.layer_collection.children[vehicle_collection.name]

    bpy.context.view_layer.active_layer_collection=vehicle_root

    # load wheel
    bpy.ops.wm.append(filename="base_tire", directory="D:/Projects/art/3d/vehicles/wheel_model.blend\\Object\\")
    tire_obj = bpy.context.selected_objects[0]

    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.wm.append(filename="base_vehicle", directory="D:/Projects/art/3d/vehicles/car_model.blend\\Object\\")
    body_obj = bpy.context.selected_objects[0]
    
    make_wheel(tire_obj, diam, tire_width, wheel_diam)

    place_wheels(tire_obj, dist_from_center_x, dist_from_center_y)
                    
    bpy.ops.object.empty_add(type='CUBE', location=(0, 0, 0))
    bpy.context.object.scale=(dist_from_center_x + tire_width / 2., \
        ((dist_from_center_y * 2) + front_overhang + rear_overhang + diam) / 2., \
        height / 2.)
    bpy.context.object.location=(0, overhang_diff / 2., height/ 2.)
    bpy.context.object.name="vehicle_bounding_box"

    bpy.ops.object.select_all(action='DESELECT')
    body_obj.select_set(True)
    bpy.context.view_layer.objects.active = body_obj 
    bpy.ops.object.mode_set(mode='EDIT', toggle=False)
    
    vehicle_bmesh = bmesh.from_edit_mesh(body_obj.data)
    
    vertex_multiselect(['front'])
    vertex_transform(vehicle_bmesh, y=0-(dist_from_center_y + front_overhang + half_diam))
    
    vertex_multiselect(['front_wheel'])

    y_max = -1000
    y_min = 0
    for v in vehicle_bmesh.verts:
        if v.select:
            if v.co.y > y_max:
                y_max = v.co.y
            if v.co.y < y_min:
                y_min = v.co.y

    y_mid = (y_max+y_min)/2.+dist_from_center_y

    vertex_transform(vehicle_bmesh, y=-y_mid, relative=True)
    
    front_front_well_location = 0-dist_from_center_y-half_diam-(diam*wheel_gap)
    front_rear_well_location = 0-dist_from_center_y+half_diam+(diam*wheel_gap)

    vertex_multiselect(['front_wheel_front_well'])
    vertex_transform(vehicle_bmesh, y=front_front_well_location)
    
    vertex_multiselect(['front_wheel_arch_front'])
    vertex_transform(vehicle_bmesh, y=front_front_well_location-wheel_arch_width)
    
    vertex_multiselect(['front_wheel_rear_well'])
    vertex_transform(vehicle_bmesh, y=front_rear_well_location)
         
    vertex_multiselect(['front_wheel_arch_rear'])
    vertex_transform(vehicle_bmesh, y=front_rear_well_location+wheel_arch_width)
    
    vertex_multiselect(['rear'])
    vertex_transform(vehicle_bmesh, y=(dist_from_center_y + rear_overhang + half_diam))
    
    vertex_multiselect(['rear_wheel'])
    vertex_transform(vehicle_bmesh, y=y_mid, relative=True)
    
    rear_front_well_location = dist_from_center_y-half_diam-(diam*wheel_gap)
    rear_rear_well_location = dist_from_center_y+half_diam+(diam*wheel_gap)

    vertex_multiselect(['rear_wheel_front_well'])
    vertex_transform(vehicle_bmesh, y=rear_front_well_location)

    vertex_multiselect(['rear_wheel_arch_front'])
    vertex_transform(vehicle_bmesh, y=rear_front_well_location-wheel_arch_width)

    vertex_multiselect(['rear_wheel_rear_well'])
    vertex_transform(vehicle_bmesh, y=rear_rear_well_location)

    vertex_multiselect(['rear_wheel_arch_rear'])
    vertex_transform(vehicle_bmesh, y=rear_rear_well_location+wheel_arch_width)
   
    offset = math.sin(math.radians(45)) * half_diam * 1.2
    
    vertex_multiselect(['front_well_detail','rear_well_detail'])
    vertex_transform(vehicle_bmesh, z=offset+half_diam)
    
    shoulder_x = scene.VehicleWidth * diam
    
    vertex_multiselect(['side'])
    vertex_transform(vehicle_bmesh, x=shoulder_x)

    vertex_multiselect(['roof_side'])
    vertex_transform(vehicle_bmesh, x=roof_width)

    vertex_multiselect(['shoulder_line'])
    vertex_transform(vehicle_bmesh, z=shoulder_line_height)

    vertex_multiselect(['skirt'])
    vertex_transform(vehicle_bmesh, z=quarter_diam)

    vertex_multiselect(['mid_line'])
    vertex_transform(vehicle_bmesh, z=half_diam)

    vertex_multiselect(['roof'])
    vertex_transform(vehicle_bmesh, z=height)

    vertex_multiselect(['top_line'])
    vertex_transform(vehicle_bmesh, z=top_line_height)

    vertex_multiselect([],['centerline','mid_centerline'], False)
    vertex_transform(vehicle_bmesh, x=top_line_width)

    mid_centerline_width = roof_width/2

    vertex_multiselect(['mid_centerline'])
    vertex_transform(vehicle_bmesh, x=mid_centerline_width)

    vertex_multiselect([],['greenhouse'], False)
    vertex_multiselect(['windshield_base','rearwindow_base'],['centerline','side'], False)
    vertex_transform(vehicle_bmesh, x=top_line_width/2)

    hip_line_height = (shoulder_line_height+top_line_height) / 2.

    vertex_multiselect(['hip_line'])
    vertex_transform(vehicle_bmesh, z=hip_line_height)

    windshield_rads = math.radians(scene.WindshieldAngle)
    base_y = (top_line_height - half_diam) / math.tan(windshield_rads)
    top_y = (height - half_diam) / math.tan(windshield_rads)
    
    vertex_multiselect(['windshield_base'])
    vertex_transform(vehicle_bmesh, y=0-dist_from_center_y+base_y)
    
    vertex_multiselect(['windshield_top'])
    vertex_transform(vehicle_bmesh, y=0-dist_from_center_y+top_y)

    front_of_rear_wheel_well = dist_from_center_y - half_diam - (diam * wheel_gap)
    top_roof_line = 0 - dist_from_center_y + top_y

    mid_line = ((top_roof_line) + (front_of_rear_wheel_well)) / 2.

    vertex_multiselect(['front_back_midline'])
    vertex_transform(vehicle_bmesh, y=mid_line)

    top_line_corner_base = (shoulder_x-top_line_width)
    top_line_front = top_line_corner_base*(1-scene.FrontCurve)
    top_line_rear = top_line_corner_base*(1-scene.RearCurve)
        
    vertex_multiselect(['front_corner'],['top_line'])
    vertex_transform(vehicle_bmesh, x=top_line_front+top_line_width)

    vertex_multiselect(['rear_corner'],['top_line'])
    vertex_transform(vehicle_bmesh, x=top_line_rear+top_line_width)

    rear_wheel_delta = (dist_from_center_y)-(half_diam-diam*wheel_gap)
    rear_wheel_half_delta = (rear_wheel_delta+mid_line)/2.

    vertex_multiselect(['rear_roof'],['rear_wheel_rear_well'])
    vertex_transform(vehicle_bmesh, y=rear_wheel_half_delta)

    for v in vehicle_bmesh.verts:
        if v.select:
            v.co.y = rear_wheel_half_delta

    vertex_multiselect(['rear_roof'],['rear_wheel_front_well'])
    vertex_transform(vehicle_bmesh, y=rear_wheel_delta)
    
    vertex_multiselect(['front_corner'])
    vertex_transform(vehicle_bmesh, y=front_overhang*(1./2.)*(scene.FrontCurve), relative=True)

    vertex_multiselect(['front'],['centerline','side'])
    vertex_transform(vehicle_bmesh, y=front_overhang*(1./8.)*(scene.FrontCurve), relative=True)

    vertex_multiselect(['rear_corner'])
    vertex_transform(vehicle_bmesh, y=-(rear_overhang*(1./2.)*(scene.RearCurve)), relative=True)

    vertex_multiselect(['rear'],['centerline','side'])
    vertex_transform(vehicle_bmesh, y=-(rear_overhang*(1./8.)*(scene.RearCurve)), relative=True)

    vertex_multiselect(['front_back_midline'],['hip_line','shoulder_line','bottom','mid_line','roof'])

    vertex_multiselect(['greenhouse'])
    
    if scene.CabPlacement == 'FWD':
        adjusted_base_y = top_line_height / math.tan(windshield_rads)
        vertex_transform(vehicle_bmesh, y=base_y-adjusted_base_y, relative=True)
    elif scene.CabPlacement == 'MID':
        adjusted_base_y = ((top_line_height / math.tan(windshield_rads))+half_diam)
        vertex_transform(vehicle_bmesh, y=base_y-adjusted_base_y, relative=True)    

    bpy.ops.view3d.snap_cursor_to_selected()
    bpy.context.scene.tool_settings.transform_pivot_point = 'CURSOR'

    vertex_multiselect(['top_line','front'], ['bottom','mid_line'])

    bpy.ops.transform.rotate(value=wedge_rads, orient_axis='X')

    vertex_multiselect(['centerline','mid_centerline'],['bottom','front','rear_bumper'])
    vertex_transform(vehicle_bmesh, z=0.05, relative=True)

    front_slope_base = (shoulder_line_height-half_diam)*scene.FrontSlope
    vertex_multiselect(['front'],['bottom','mid_line'])
    vertex_transform(vehicle_bmesh, z=-(front_slope_base)*(2./3.), relative=True)

    vertex_multiselect(['front_wheel_front_well'],['front_wheel_arch','bottom','mid_line','shoulder_line'])
    vertex_transform(vehicle_bmesh, z=-(front_slope_base)*(1./3.), relative=True)

    vertex_multiselect(['front_wheel'],['front_wheel_arch','front_wheel_rear_well','front_wheel_front_well','shoulder_line','front_well_detail','rear_well_detail'])
    vertex_transform(vehicle_bmesh, z=-(front_slope_base)*(1./6.), relative=True)

    bmesh.update_edit_mesh(body_obj.data)

    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='OBJECT', toggle=False)







