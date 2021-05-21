import bpy
import bpy.props

bpy.types.Scene.TireWidth = bpy.props.FloatProperty(
    name = "Tire Width", 
    description = "Width of tire (mm)",
    default = 225)

bpy.types.Scene.TireSidewall = bpy.props.FloatProperty(
    name = "Tire Sidewall", 
    description = "Sidewall width (in)",
    default = 50)
 
bpy.types.Scene.WheelDiameter = bpy.props.FloatProperty(
    name = "Wheel Size", 
    description = "Diameter of wheel",
    default = 17)
 
bpy.types.Scene.Wheelbase = bpy.props.FloatProperty(
    name = "Wheelbase",
    description = "Number of wheels between wheels",
    default = 3.25)

bpy.types.Scene.VehicleHeight = bpy.props.FloatProperty(
    name = "Vehicle Height",
    description = "Height of vehicle based on wheel size",
    default = 2.33)

# rename to belt line?
bpy.types.Scene.WaistLine = bpy.props.FloatProperty(
    name = "Waist Line",
    description = "Waist Line of vehicle based on wheel size",
    default = 1.66)

bpy.types.Scene.VehicleWidth = bpy.props.FloatProperty(
    name = "Vehicle Width",
    description = "Width of vehicle based on wheel size",
    default = 1.45)

# rename to belt line?
bpy.types.Scene.WaistWidth = bpy.props.FloatProperty(
    name = "Waist Width",
    description = "Width of vehicle at waistline based on wheel size",
    default = 1.17)

bpy.types.Scene.RoofWidth = bpy.props.FloatProperty(
    name = "Roof Width",
    description = "Width of roof based on wheel size",
    default = 0.8)

bpy.types.Scene.FrontOverhang = bpy.props.FloatProperty(
    name = "Front Overhang",
    description = "Number of wheels in front of front wheel",
    default = 1.0,
    min = 0.25, max = 1.5)

bpy.types.Scene.RearOverhang = bpy.props.FloatProperty(
    name = "Rear Overhang",
    description = "Number of wheels to rear of rear wheel",
    default = 0.5,
    min = 0.25, max = 1.5)

bpy.types.Scene.WindshieldAngle = bpy.props.FloatProperty(
    name = "Windshield Angle",
    description = "Angle of windshield",
    default = 45.0,
    min = 20.0, max = 89.0)

bpy.types.Scene.WedgeAngle = bpy.props.FloatProperty(
    name = "Wedge Angle",
    description = "Angle of lines from front to back",
    default = 2.0,
    min = 0, max = 3)

bpy.types.Scene.CabPlacement = bpy.props.EnumProperty(
    name="Cab Placement",
    description = "Where the cab sits",
    default='FWD',
    items=[
        ('FWD', "Front-wheel drive", ""),
        ('RWD', "Rear-wheel drive", ""),
        ('MID', "Mid-Engine", ""), 
    ]) 

bpy.types.Scene.FrontCurve = bpy.props.FloatProperty(
    name = "Front Curvature",
    description = "Curvature of front end",
    default = 1.0,
    min = 0, max = 1
    )

bpy.types.Scene.RearCurve = bpy.props.FloatProperty(
    name = "Rear Curvature",
    description = "Curvature of rear end",
    default = 1.0,
    min = 0, max = 1
    )

bpy.types.Scene.FrontSlope = bpy.props.FloatProperty(
    name = "Front Slope",
    description = "Slope of front end",
    default = 1.0,
    min = 0, max = 1 
    )

bpy.types.Scene.WindshieldCurve = bpy.props.FloatProperty(
    name = "Windshield Curvature",
    description = "Curve of the windshield base",
    default = 0.5,
    min = 0, max = 1
    )