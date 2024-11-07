import maya.cmds as cmds

from utils import parent_by_selection_order
from utils import unparent_by_selection_order
from utils import rigging_functions
from utils import controller_curves
from utils import ribbon_setup
from auto_rigger import ik_fk_chain_rig_setup

import importlib
importlib.reload(rigging_functions)
importlib.reload(parent_by_selection_order)
importlib.reload(unparent_by_selection_order)
importlib.reload(controller_curves)
importlib.reload(ik_fk_chain_rig_setup)
importlib.reload(ribbon_setup)

"""
copiar lo de abajo na mas pa usar el codigo

import maya.cmds as cmds

import importlib

from auto_rigger import spine_rig

importlib.reload(spine_rig)


spine_joint_list = spine_rig.create_spine_joints()[0]
spine_rig.create_spine_rig(spine_joint_list)

"""

def create_spine_joints():

    spine_joints_list = []

    hips_guide_name =  ''

    if cmds.objExists('*hips_guide'):
        hips_guide_name = cmds.ls('*hips_guide', type='transform')[0]


    chest_guide_name = ''

    if cmds.objExists('*chest_guide'):
        chest_guide_name = cmds.ls('*chest_guide', type='transform')[0]


    joint_count = 7
    start = hips_guide_name
    end = chest_guide_name

    steps = 1.0 / (joint_count - 1)
    perc = 0

    for jointNumber in range(joint_count):

        joint = cmds.joint(n='cn_' + str(jointNumber)+'_spine_jnt')
        cmds.setAttr(joint + '.displayLocalAxis', True)

        parent_constraint = cmds.parentConstraint(start, joint, weight=1.0 - perc)[0]
        cmds.parentConstraint(end, joint, weight=perc)
        cmds.delete(parent_constraint)

        perc += steps

        spine_joints_list.append(joint)

    cmds.select(clear=True)

    for eachJoint in spine_joints_list:

        if eachJoint == 'cn_0_spine_jnt':
            cmds.rename(eachJoint,'cn_0_hips_jnt')

        if eachJoint == 'cn_6_spine_jnt':
            cmds.rename(eachJoint, 'cn_6_chest_jnt')

    cmds.select('cn_0_hips_jnt',hierarchy=True)

    drive_spine_joint_list = cmds.ls(sl=True)

    cmds.select(clear=True)

    skin_joint_list = []

    for eachJoint in drive_spine_joint_list:
        skin_joint_name = eachJoint.replace('_jnt','_skin_jnt')
        skin_joint = cmds.joint(name=skin_joint_name)
        cmds.matchTransform(skin_joint,eachJoint)
        skin_joint_list.append(skin_joint)


    return [drive_spine_joint_list,skin_joint_list]

def create_spine_rig (joint_list):

    guide_root_group_name = cmds.ls('*_mainGuides_grp',type='transform')[0]

    rig_main_group_name = guide_root_group_name.replace('_mainGuides_grp','_rigMain_grp')

    rig_main_group = cmds.group(empty=True,name=rig_main_group_name)


    start_joint =  joint_list[0]
    end_joint =  joint_list[len(joint_list)-1]
    spline_spans = 1
    spline_handle_name = 'cn_spine_ik_splineHandle'
    controller_color = 22
    controller_shape = 'cube'
    controller_size = 3
    world_up_type = 4
    forward_axis = 2
    world_up_axis = 3
    world_up_vector_x = 0
    world_up_vector_y = 0
    world_up_vector_z = 1
    world_up_vector_end_x = 0
    world_up_vector_end_y = 0
    world_up_vector_end_z = 1
    control_spans = 2
    root_at_world = False
    spline_axis = 'Y'

    create_full_bind_hierarchy = True

    rotate_in_x_axis = 0
    rotate_in_y_axis = 0
    rotate_in_z_axis = 90


    ribbon_joint = ribbon_setup.create_ribbon(start_joint, end_joint, joint_list, create_full_bind_hierarchy,rotate_in_x_axis,
                                              rotate_in_y_axis,rotate_in_z_axis)

    ribbon_joint_list = ribbon_joint[0]
    ribbon_setup_group = ribbon_joint[1]

    spine_ik_fk_setup_group = ik_fk_chain_rig_setup.ik_fk_chain_rig(ribbon_joint_list, spline_spans, spline_handle_name, controller_color,
                                      controller_shape,
                                      controller_size,
                                      world_up_type, forward_axis, world_up_axis,
                                      world_up_vector_x, world_up_vector_y, world_up_vector_z,
                                      world_up_vector_end_x, world_up_vector_end_y, world_up_vector_end_z,
                                      control_spans,
                                      root_at_world,
                                      rig_main_group,
                                      spline_axis)


    cmds.select(clear=True)

    cmds.parent(ribbon_setup_group,spine_ik_fk_setup_group[1])

    cmds.parent(spine_ik_fk_setup_group[0],rig_main_group)

    cmds.select(clear=True)






   










































































