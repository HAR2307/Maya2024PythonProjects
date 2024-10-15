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

    rigging_functions.spline_ik_setup(start_joint, end_joint, spline_spans, spline_handle_name, controller_color,
                                      controller_shape,
                                      controller_size,
                                      world_up_type, forward_axis, world_up_axis,
                                      world_up_vector_x, world_up_vector_y, world_up_vector_z,
                                      world_up_vector_end_x, world_up_vector_end_y, world_up_vector_end_z)


    fk_joint_list = []

    cmds.select(start_joint,hierarchy=True)

    joint_list = cmds.ls(sl=True)

    cmds.select(clear=True)

    joint_counter = 0

    for eachJoint in joint_list:


        if joint_counter %  2 ==0:

            fk_joint_name = eachJoint.replace('_jnt', '_fk_jnt')

            fk_joint = cmds.joint(n=fk_joint_name, radius=2)

            cmds.matchTransform(fk_joint,eachJoint)

            cmds.setAttr(fk_joint + '.displayLocalAxis', True)

            fk_joint_list.append(fk_joint)

        joint_counter += 1

    start_bind_group = cmds.ls('*_start*_grp',type = 'transform')[0]

    end_bind_group = cmds.ls('*_end*_grp',type = 'transform')[0]

    start_constraint_name = start_bind_group.replace('_grp', '_parentConstraint')

    end_constraint_name = end_bind_group.replace('_grp', '_parentConstraint')

    cmds.parentConstraint('cn_0_hips_fk_jnt','cn_0_hips_start_ik_ctrl_grp',
                          maintainOffset=False,name=start_constraint_name)

    cmds.parentConstraint('cn_6_chest_fk_jnt', 'cn_6_chest_end_ik_ctrl_grp',
                          maintainOffset=False,name = end_constraint_name)

    fk_ctrl_list = []


    for eachJoint in range(1,len(fk_joint_list)-1):

        fk_ctrl= rigging_functions.create_controller(fk_joint_list[eachJoint],2,
                                                     18,'circle','_ctrl',
                                                'parent',False)

        fk_ctrl_list.append(fk_ctrl)

    fk_ctrl_group_list = cmds.ls('*_fk_ctrl_grp',type='transform')

    reverse_ctrl_list =sorted(fk_ctrl_list)
    reverse_grp_list = sorted(fk_ctrl_group_list)

    print(reverse_ctrl_list)
    print(reverse_grp_list)


    for group, ctrl in zip(reverse_grp_list[1:], reverse_ctrl_list):

        print(f'{group} -> {ctrl}')

        cmds.parent(group,ctrl)

    ##create stretch setup

    spline_curve_name = cmds.ls('*ik_splineCurve')[0]
    curve_info_node = cmds.arclen( spline_curve_name,constructionHistory =True )
    curve_info_node_name = spline_curve_name + '_curveInfo'
    if cmds.objExists('curveInfo1'):
        cmds.rename('curveInfo1',curve_info_node_name)

    spline_multiply_divide_node_name = spline_curve_name + '_multiplyDivide'

    spline_multiply_divide_node = cmds.createNode('multiplyDivide',name=spline_multiply_divide_node_name)

    cmds.connectAttr(curve_info_node_name+'.arcLength',
                     spline_multiply_divide_node_name+'.input1'+'.input1Y')

    spline_arclen =  cmds.arclen(spline_curve_name)

    cmds.setAttr(spline_multiply_divide_node_name+'.input2'+'.input2Y',spline_arclen)
    cmds.setAttr(spline_multiply_divide_node_name+'.operation',2)

    spline_squash_stretch_pow_name = spline_curve_name + '_squashStretchPow'

    spline_squash_stretch_pow = cmds.createNode('multiplyDivide',name=spline_squash_stretch_pow_name)

    cmds.connectAttr(spline_multiply_divide_node_name+'.output'+'.outputY',
                     spline_squash_stretch_pow_name + '.input1' + '.input1Y')

    cmds.setAttr(spline_squash_stretch_pow_name + '.operation', 3)
    cmds.setAttr(spline_squash_stretch_pow_name + '.input2' + '.input2Y', 0.5)

    spline_squash_stretch_invert_div_name = spline_curve_name + '_squashStretchInvertDiv'

    spline_squash_stretch_invert_div = cmds.createNode('multiplyDivide', name=spline_squash_stretch_invert_div_name)

    cmds.connectAttr(spline_squash_stretch_pow_name + '.output' + '.outputY',
                     spline_squash_stretch_invert_div_name + '.input2' + '.input2Y')

    cmds.setAttr(spline_squash_stretch_invert_div_name + '.operation', 2)
    cmds.setAttr(spline_squash_stretch_invert_div_name + '.input1' + '.input1Y', 1)

    for eachJoint in joint_list:
        cmds.connectAttr(spline_multiply_divide_node_name + '.output' + '.outputY',
                         eachJoint + '.scale' + '.scaleY')

    for eachJoint in joint_list:
        cmds.connectAttr(spline_squash_stretch_invert_div_name + '.output' + '.outputY',
                         eachJoint + '.scale' + '.scaleX')
        cmds.connectAttr(spline_squash_stretch_invert_div_name + '.output' + '.outputY',
                         eachJoint + '.scale' + '.scaleZ')










































































