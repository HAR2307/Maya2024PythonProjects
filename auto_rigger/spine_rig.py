import maya.cmds as cmds

from utils import parent_by_selection_order
from utils import unparent_by_selection_order
from utils import rigging_functions
from utils import controller_curves

import importlib
importlib.reload(rigging_functions)
importlib.reload(parent_by_selection_order)
importlib.reload(unparent_by_selection_order)
importlib.reload(controller_curves)

"""
copiar lo de abajo na mas pa usar el codigo

import maya.cmds as cmds

import importlib

from auto_rigger import spine_rig

importlib.reload(spine_rig)


spine_rig.create_spine_joints()
spine_rig.create_spine_rig()

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

    result_spine_joint_list = cmds.ls(sl=True)

    cmds.select(clear=True)

    return result_spine_joint_list

def create_spine_rig ():

    start_joint =  'cn_0_hips_jnt'
    end_joint = 'cn_6_chest_jnt'
    spline_spans = 1
    spline_handle_name = 'cn_spine_ik_splineHandle'
    controller_color = 22
    controller_shape = 'cube'
    world_up_type = 4
    forward_axis = 2
    world_up_axis = 3
    world_up_vector_x = 0
    world_up_vector_y = 0
    world_up_vector_z = 1
    world_up_vector_end_x = 0
    world_up_vector_end_y = 0
    world_up_vector_end_z = 1

    rigging_functions.spline_ik_setup(start_joint, end_joint, spline_spans, spline_handle_name, controller_color,
                                      controller_shape,
                                      world_up_type, forward_axis, world_up_axis,
                                      world_up_vector_x, world_up_vector_y, world_up_vector_z,
                                      world_up_vector_end_x, world_up_vector_end_y, world_up_vector_end_z)

    cmds.select(start_joint,hierarchy=True)

    spine_joint_list = cmds.ls(sl=True)

    cmds.select(clear=True)

    counter = 0

    for eachJoint in spine_joint_list:


        if counter %  2 ==0:

            fk_joint_name = eachJoint.replace('_jnt', '_fk_jnt')

            fk_joint = cmds.joint(n=fk_joint_name, radius=2)

            cmds.matchTransform(fk_joint,eachJoint)

            cmds.setAttr(fk_joint + '.displayLocalAxis', True)

        counter += 1

    start_bind_group = cmds.ls('*_start*_grp',type = 'transform')[0]

    end_bind_group = cmds.ls('*_end*_grp',type = 'transform')[0]

    start_constraint_name = start_bind_group.replace('_grp', '_parentConstraint')

    end_constraint_name = end_bind_group.replace('_grp', '_parentConstraint')

    cmds.parentConstraint('cn_0_hips_fk_jnt','cn_0_hips_start_ik_ctrl_grp',
                          maintainOffset=False,name=start_constraint_name)

    cmds.parentConstraint('cn_6_chest_fk_jnt', 'cn_6_chest_end_ik_ctrl_grp',
                          maintainOffset=False,name = end_constraint_name)









































