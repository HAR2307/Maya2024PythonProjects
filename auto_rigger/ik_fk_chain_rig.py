import maya.cmds as cmds

from utils import parent_by_selection_order
from utils import unparent_by_selection_order
from utils import rigging_functions
from utils import controller_curves
from utils import ribbon_setup
from auto_rigger import chain_guides
from auto_rigger import ik_fk_chain_rig_setup
from utils import rigging_functions_02

import importlib
importlib.reload(rigging_functions)
importlib.reload(parent_by_selection_order)
importlib.reload(unparent_by_selection_order)
importlib.reload(controller_curves)
importlib.reload(ik_fk_chain_rig_setup)
importlib.reload(ribbon_setup)
importlib.reload(chain_guides)
importlib.reload(rigging_functions_02)

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

    chain_joints = rigging_functions_02.create_joints_from_guides(guide_list,joint_orientation)

    rig_joint_list = chain_joints[0]

    for eachJoint in rig_joint_list:
        rigging_functions.freeze(eachJoint)

    skin_joint_list = chain_joints[1]

    for eachJoint in skin_joint_list:
        rigging_functions.freeze(eachJoint)

    chain_orientation_data = chain_joints[2]

    print (chain_orientation_data)

    skin_joints_group_name = skin_joint_list[0].replace('_jnt', '_skinJoints_grp')

    skin_joints_group = cmds.group(empty=True, name=skin_joints_group_name)

    rig_group_name = rig_joint_list[0].replace('_jnt', '_rigMain_grp')

    rig_group = cmds.group(empty=True, name=rig_group_name)

    cmds.matchTransform(rig_group,rig_joint_list[0])

    start_joint = rig_joint_list[0]
    end_joint = rig_joint_list[len(rig_joint_list) - 1]
    spline_spans = 1
    spline_handle_name = rig_joint_list[0].replace('_jnt','_ik_splineHandle')
    controller_color = 22
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

    ribbon_joint = ribbon_setup.create_ribbon(start_joint, end_joint, rig_joint_list,
                                              create_full_bind_hierarchy,rotate_in_x_axis,
                                              rotate_in_y_axis,rotate_in_z_axis)

    ribbon_joint_list = ribbon_joint[0]
    ribbon_setup_group = ribbon_joint[1]

    spine_ik_fk_setup_group = ik_fk_chain_rig_setup.ik_fk_chain_rig(ribbon_joint_list, spline_spans, spline_handle_name,
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
                                                                    rig_group,
                                                                    spline_axis)

    cmds.select(clear=True)

    cmds.parent(ribbon_setup_group, spine_ik_fk_setup_group[1])

    cmds.parent(skin_joint_list[0],skin_joints_group )

    cmds.parent(skin_joints_group,rig_group)

    cmds.parent(spine_ik_fk_setup_group[0], rig_group)

    cmds.select(clear=True)

    all_joints = cmds.ls('*_jnt')

    for eachJoint in all_joints:
        cmds.setAttr(eachJoint+'.radius',0.1)








