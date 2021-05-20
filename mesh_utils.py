import bpy

def vertex_multiselect(select_list, deselect_list=[], deselect=True):
    if deselect:
        bpy.ops.mesh.select_all(action='DESELECT')

    for group_name in select_list:
        bpy.ops.object.vertex_group_set_active(group=group_name)
        bpy.ops.object.vertex_group_select()

    for group_name in deselect_list:
        bpy.ops.object.vertex_group_set_active(group=group_name)
        bpy.ops.object.vertex_group_deselect()

def vertex_transform(mesh, x=None, y=None, z=None, relative=False):
    for v in mesh.verts:
        if v.select:
            if x:
                if relative:
                    v.co.x += x
                else:
                    v.co.x = x
            if y:
                if relative:
                    v.co.y += y
                else:
                    v.co.y = y
            if z:
                if relative:
                    v.co.z += z
                else:
                    v.co.z = z
