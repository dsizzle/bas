import bpy
import bmesh

def vertex_multiselect(select_list, deselect_list=[], deselect=True):
	if deselect:
		bpy.ops.mesh.select_all(action='DESELECT')

	for group_name in select_list:
		bpy.ops.object.vertex_group_set_active(group=group_name)
        bpy.ops.object.vertex_group_select()

    for group_name in deselect_list:
    	bpy.ops.object.vertex_group_set_active(group=group_name)
        bpy.ops.object.vertex_group_deselect()
