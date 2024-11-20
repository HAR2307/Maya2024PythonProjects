import maya.cmds as cmds


from utils import parent_by_selection_order
from utils import unparent_by_selection_order
from utils import rigging_functions
from utils import controller_curves
from utils import ribbon_setup
from auto_rigger import chain_guides
from auto_rigger import ik_fk_chain_rig_setup
from utils import rigging_functions_02
from utils import create_master_controller
from utils import nurbs_ribbon_deformer_setup


import importlib
importlib.reload(rigging_functions)
importlib.reload(parent_by_selection_order)
importlib.reload(unparent_by_selection_order)
importlib.reload(controller_curves)
importlib.reload(ik_fk_chain_rig_setup)
importlib.reload(ribbon_setup)
importlib.reload(chain_guides)
importlib.reload(rigging_functions_02)
importlib.reload(create_master_controller)
importlib.reload(nurbs_ribbon_deformer_setup)

"""
copiar lo de abajo na mas pa usar el codigo

import maya.cmds as cmds

import importlib

from auto_rigger import ik_fk_chain_rig
from auto_rigger import chain_guides

importlib.reload(ik_fk_chain_rig)
importlib.reload(chain_guides)

guide_name = ''
side=''
letter=''
number_of_guides = 10

guide_list = chain_guides.create_chain_guides(guide_name, side, letter, number_of_guides)
joint_orientation = 'yzx:yup'

ik_fk_chain = ik_fk_chain_rig.create_ik_fk_chain(guide_list,joint_orientation)

"""

def create_ik_fk_chain(guide_list,joint_orientation):


    master_TR = ''

    master_TRS = ''

    chain_joints = rigging_functions_02.create_joints_from_guides(guide_list,joint_orientation)

    rig_joint_list = chain_joints[0]

    for eachJoint in rig_joint_list:
        rigging_functions.freeze(eachJoint)

    skin_joint_list = chain_joints[1]

    for eachJoint in skin_joint_list:
        rigging_functions.freeze(eachJoint)

    chain_orientation_data = chain_joints[2]

    print (chain_orientation_data)

    rig_group_name = rig_joint_list[0].replace('_jnt', '_rigMain_grp')

    rig_group = cmds.group(empty=True, name=rig_group_name)

    cmds.matchTransform(rig_group,rig_joint_list[0])

    if cmds.objExists('*_master_TRS_*'):

        master_TRS = cmds.ls('*_master_TRS_ctrl')
        master_TR = cmds.ls('*_master_TR_ctrl')
        skin_joints_group = cmds.ls('*_skinJoints_grp')

        cmds.parent(skin_joint_list[0], skin_joints_group)


    else:

        asset_name = rig_joint_list[0].replace('_jnt','_asset')
        master_ctrl_list = create_master_controller.create_hierarchy(asset_name)
        master_TRS = master_ctrl_list[0]
        master_TR = master_ctrl_list[1]
        skin_joints_group = master_ctrl_list[2]

        cmds.parent(skin_joint_list[0], skin_joints_group)


    start_joint = rig_joint_list[0]
    end_joint = rig_joint_list[len(rig_joint_list) - 1]
    spline_spans = 1
    spline_handle_name = rig_joint_list[0].replace('_jnt','_ik_splineHandle')
    controller_color = 30
    controller_shape = 'cube'
    controller_size = 3
    world_up_type = 4
    forward_axis = chain_orientation_data[0][4]
    world_up_axis =  chain_orientation_data[0][5]
    world_up_vector_x = chain_orientation_data[0][1]
    world_up_vector_y = chain_orientation_data[0][2]
    world_up_vector_z = chain_orientation_data[0][3]
    world_up_vector_end_x = chain_orientation_data[0][1]
    world_up_vector_end_y = chain_orientation_data[0][2]
    world_up_vector_end_z = chain_orientation_data[0][3]
    control_spans = 2
    root_at_world = False
    spline_axis = chain_orientation_data[0][0]

    rotate_in_x_axis = chain_orientation_data[1][0]
    rotate_in_y_axis = chain_orientation_data[1][1]
    rotate_in_z_axis = chain_orientation_data[1][2]




    create_full_bind_hierarchy = True

    ribbon_setup_list = ribbon_setup.create_ribbon(start_joint, end_joint, rig_joint_list,
                                              create_full_bind_hierarchy,rotate_in_x_axis,
                                              rotate_in_y_axis,rotate_in_z_axis)

    ribbon_joint_list = ribbon_setup_list[0]
    ribbon_setup_group = ribbon_setup_list[1]
    ribbon_surface_name = ribbon_setup_list[2]

    spline_ik_fk_setup_list = ik_fk_chain_rig_setup.ik_fk_chain_rig(ribbon_joint_list, spline_spans, spline_handle_name,
                                                                    controller_color,
                                                                    controller_shape,
                                                                    controller_size,
                                                                    world_up_type, forward_axis, world_up_axis,
                                                                    world_up_vector_x, world_up_vector_y,
                                                                    world_up_vector_z,
                                                                    world_up_vector_end_x, world_up_vector_end_y,
                                                                    world_up_vector_end_z,
                                                                    control_spans,
                                                                    root_at_world,
                                                                    master_TRS,
                                                                    spline_axis)

    cmds.select(clear=True)

    spline_ik_fk_ctrl_name = spline_ik_fk_setup_list[1]

    ribbon_sine_deformer_setup = nurbs_ribbon_deformer_setup.sine_wave_deformer_setup(ribbon_surface_name,spline_ik_fk_ctrl_name,rotate_in_y_axis,
                                                                                      rotate_in_x_axis,rotate_in_y_axis)

    cmds.parent(ribbon_setup_group, spline_ik_fk_setup_list[1])


    cmds.parent(spline_ik_fk_setup_list[0], rig_group)

    cmds.select(clear=True)

    all_joints = cmds.ls('*_jnt')

    for eachJoint in all_joints:
        cmds.setAttr(eachJoint+'.radius',0.1)

    cmds.parent(ribbon_sine_deformer_setup, master_TR)

    cmds.parent(rig_group_name,master_TR)

    cmds.setAttr(ribbon_sine_deformer_setup+'.visibility',0)
    cmds.setAttr(ribbon_setup_group + '.visibility', 0)

    rigging_functions_02.parent_constraint_between_joints(rig_joint_list,skin_joint_list)

    spline_ik_fk_ctrl_name = spline_ik_fk_setup_list[1]

    rigging_functions.set_colors(spline_ik_fk_ctrl_name,9)














