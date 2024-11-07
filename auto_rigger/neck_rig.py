import maya.cmds as cmds

from utils import parent_by_selection_order
from utils import unparent_by_selection_order
from utils import rigging_functions
from utils import controller_curves
from auto_rigger import ik_fk_chain_rig_setup

import importlib
importlib.reload(rigging_functions)
importlib.reload(parent_by_selection_order)
importlib.reload(unparent_by_selection_order)
importlib.reload(controller_curves)
importlib.reload(ik_fk_chain_rig)

"""
copiar lo de abajo na mas pa usar el codigo

import maya.cmds as cmds

import importlib

from auto_rigger import neck_rig

importlib.reload(neck_rig)


neck_joint_list = neck_rig.create_neck_joints()
neck_rig.create_neck_rig(neck_joint_list)

"""

def create_neck_joints():

    neck_joint_list = []

    neck_guide_name = ''

    head_joint = ''

    if cmds.objExists('*neck_guide'):
        neck_guide_name = cmds.ls('*neck_guide', type='transform')[0]

    head_guide_name = ''

    if cmds.objExists('*head_guide'):
        head_guide_name = cmds.ls('*head_guide', type='transform')[0]

    joint_count = 4
    start = neck_guide_name
    end = head_guide_name

    steps = 1.0 / (joint_count - 1)
    perc = 0

    for jointNumber in range(joint_count):
        joint = cmds.joint(n='cn_' + str(jointNumber) + '_neck_jnt')
        cmds.setAttr(joint + '.displayLocalAxis', True)

        parent_constraint = cmds.parentConstraint(start, joint, weight=1.0 - perc)[0]
        cmds.parentConstraint(end, joint, weight=perc)
        cmds.delete(parent_constraint)

        perc += steps

        neck_joint_list.append(joint)

    cmds.select(clear=True)

    for eachJoint in neck_joint_list:


        if eachJoint == 'cn_3_neck_jnt':
            head_joint_name = eachJoint.replace('neck','head')
            head_joint = cmds.rename(eachJoint, head_joint_name)

    cmds.select(clear=True)

    cmds.select('cn_0_neck_jnt', hierarchy=True)

    result_neck_joint_list = cmds.ls(sl=True)

    cmds.select(clear=True)

   #head_end_guide = cmds.ls('*headEnd_guide',type='transform')[0]
   #
   #head_end_joint_name = head_end_guide.replace('guide','jnt')
   #
   #head_end_joint = cmds.joint(name=head_end_joint_name)
   #
   #cmds.matchTransform(head_end_joint, head_end_guide)
   #
   #cmds.parent(head_end_joint,head_joint)
    
   #jaw_guide = cmds.ls('*jaw_guide', type='transform')[0]
   #
   #jaw_joint_name = jaw_guide.replace('guide', 'jnt')
   #
   #jaw_joint = cmds.joint(name=jaw_joint_name)
   #
   #cmds.matchTransform(jaw_joint,jaw_guide)
   #
   #cmds.parent(jaw_joint, head_joint)
   #
   #jaw_end_guide = cmds.ls('*jawEnd_guide', type='transform')[0]
   #
   #jaw_end_joint_name = jaw_end_guide.replace('guide', 'jnt')
   #
   #jaw_end_joint = cmds.joint(name=jaw_end_joint_name)
   #
   #cmds.matchTransform(jaw_end_joint,jaw_end_guide)
   #
   #cmds.select(clear=True)
   #
   #print(result_neck_joint_list[0])
   #print(result_neck_joint_list[len(result_neck_joint_list) - 1])

    cmds.select(clear=True)


    return result_neck_joint_list

def create_neck_rig(joint_list):



    start_joint = joint_list[0]
    end_joint = joint_list[len(joint_list) - 1]
    spline_spans = 4
    spline_handle_name = 'cn_neck_ik_splineHandle'
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

    control_spans = 3

    root_at_world = False

    rig_main_grp_name = cmds.ls('*rigMain_grp', type='transform')[0]

    neck_ik_fk_setup_group = ik_fk_chain_rig.ik_fk_chain_rig(joint_list, spline_spans, spline_handle_name, controller_color,
                                    controller_shape,
                                    controller_size,
                                    world_up_type, forward_axis, world_up_axis,
                                    world_up_vector_x, world_up_vector_y, world_up_vector_z,
                                    world_up_vector_end_x, world_up_vector_end_y, world_up_vector_end_z,
                                    control_spans,
                                    root_at_world,
                                    rig_main_grp_name)

    cmds.parent(neck_ik_fk_setup_group,rig_main_grp_name)



    cmds.select(clear=True)








