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
importlib.reload(ribbon_setup)
importlib.reload(ik_fk_chain_rig_setup)

"""
copiar lo de abajo na mas pa usar el codigo

import maya.cmds as cmds

import importlib

from auto_rigger import neck_rig

importlib.reload(neck_rig)


neck_joints = neck_rig.create_neck_joints()
neck_rig_joints = neck_joints[0]
neck_skin_joints  = neck_joints[1]

neck_rig.create_neck_rig(neck_rig_joints,neck_skin_joints)

"""

def create_neck_joints():

    drive_neck_joint_list = []

    skin_neck_joint_list = []

    neck_guide_name = ''

    head_joint = ''

    if cmds.objExists('*neck_guide'):
        neck_guide_name = cmds.ls('*neck_guide', type='transform')[0]

    head_guide_name = ''

    if cmds.objExists('*head_guide'):
        head_guide_name = cmds.ls('*head_guide', type='transform')[0]

    joint_count = 3
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

        drive_neck_joint_list.append(joint)

    cmds.select(clear=True)

    for eachJoint in drive_neck_joint_list:

        skin_joint_name = eachJoint.replace('_jnt','_skin_jnt')
        skin_joint = cmds.joint(name=skin_joint_name)
        cmds.matchTransform(skin_joint,eachJoint)
        skin_neck_joint_list.append(skin_joint)

    cmds.select(clear=True)


    return [drive_neck_joint_list,skin_neck_joint_list]

def create_neck_rig(joint_list,skin_joint_list):

    master_TR_ctrl = cmds.ls('*TR_ctrl',type='transform')[0]
    print(master_TR_ctrl)
    master_TRS_ctrl = cmds.ls('*TRS_ctrl',type='transform')[0]
    print(master_TRS_ctrl)
    rig_main_group = cmds.ls('*_rigMain_grp')
    print(rig_main_group)
    skin_joints_group = cmds.ls('*_skinJoints_grp')
    print(skin_joints_group)

    start_joint = joint_list[0]
    end_joint = joint_list[len(joint_list) - 1]
    spline_spans = 4
    spline_handle_name = 'cn_neck_ik_splineHandle'
    controller_color = 30
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

    #neck_ik_fk_setup_group

    ribbon_joint = ribbon_setup.create_ribbon(start_joint, end_joint, joint_list, create_full_bind_hierarchy,
                                              rotate_in_x_axis,
                                              rotate_in_y_axis, rotate_in_z_axis)

    ribbon_joint_list = ribbon_joint[0]
    ribbon_setup_group = ribbon_joint[1]

    neck_ik_fk_setup_list = ik_fk_chain_rig_setup.ik_fk_chain_rig(ribbon_joint_list, spline_spans, spline_handle_name,
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
                                                                    master_TRS_ctrl,
                                                                    spline_axis)

    neck_ik_fk_setup_group = neck_ik_fk_setup_list[0]
    neck_ik_fk_setup_main_ctrl = neck_ik_fk_setup_list[1]
    neck_ik_setup_group = neck_ik_fk_setup_list[2]

    cmds.delete('cn_2_neck_ribbon_end_parentConstraint')

    head_drive_joint_name = end_joint.replace('neck','head')

    head_drive_joint = cmds.joint(name=head_drive_joint_name)

    cmds.matchTransform(head_drive_joint,end_joint)

    ribbon_end_joint = 'cn_2_neck_ribbon_end_jnt'

    ribbon_end_joint_parent_constraint = ribbon_end_joint.replace('jnt','pointConstraint')

    cmds.pointConstraint(head_drive_joint,ribbon_end_joint,maintainOffset=False)

    end_ik_ctrl = 'cn_2_neck_ribbon_end_ik_ctrl'

    head_drive_joint_constraint_name = head_drive_joint_name.replace('jnt','parentConstraint')

    cmds.parentConstraint(end_ik_ctrl,head_drive_joint,name = head_drive_joint_constraint_name)

    rotation_multiply_divide_node_name= 'neck_head_rotation_multiply_divide_node'

    rotation_multiply_divide_node = cmds.createNode('multiplyDivide', name=rotation_multiply_divide_node_name)

    cmds.connectAttr(head_drive_joint_name+'.rotate'+'.rotateY',rotation_multiply_divide_node_name+'.input1'+'.input1Y')
    cmds.connectAttr(rotation_multiply_divide_node_name+'.output'+'.outputY',ribbon_end_joint+'.rotate'+'.rotateY')

    head_children_locator_name = head_drive_joint_name.replace('jnt','loc')

    head_children_locator = cmds.spaceLocator(name=head_children_locator_name)[0]

    head_skin_joint_name = head_drive_joint_name.replace('jnt','skin_jnt')

    head_skin_joint = cmds.joint(name=head_skin_joint_name)

    cmds.matchTransform(head_skin_joint, end_joint)

    neck_end_skin_joint = skin_joint_list[len(joint_list) - 1]

    cmds.parent(head_skin_joint,neck_end_skin_joint)

    cmds.matchTransform(head_children_locator,neck_end_skin_joint)

    head_children_locator_constraint_name = head_children_locator_name.replace('loc','parentConstraint')

    cmds.parentConstraint(head_drive_joint,head_children_locator,name=head_children_locator_constraint_name,maintainOffset=False)

    create_jaw(head_children_locator,head_drive_joint,head_skin_joint)

   #cmds.parent(head_drive_joint,neck_ik_setup_group)
   #cmds.parent(ribbon_setup_group,neck_ik_fk_setup_group)
   #cmds.parent(neck_ik_fk_setup_group,rig_main_group)
   #cmds.parent(skin_joint_list[0],skin_joints_group)



def create_jaw(head_children_locator, head_drive_joint, head_skin_joint):

    jaw_joint_list = []
    jaw_skin_joint_list = []

    cmds.select(clear=True)

    head_end_guide = cmds.ls('*headEnd_guide', type='transform')[0]

    head_end_joint_name = head_end_guide.replace('_guide', '_skin_jnt')

    head_end_joint = cmds.joint(name=head_end_joint_name)

    cmds.matchTransform(head_end_joint, head_end_guide)

    cmds.select(clear=True)

    cmds.parent(head_end_joint, head_skin_joint)

    cmds.select(clear=True)

    jaw_guide = cmds.ls('*jaw_guide', type='transform')[0]

    jaw_joint_name = jaw_guide.replace('guide', 'jnt')

    jaw_joint = cmds.joint(name=jaw_joint_name)

    cmds.matchTransform(jaw_joint, jaw_guide)

    jaw_end_guide = cmds.ls('*jawEnd_guide', type='transform')[0]

    jaw_end_joint_name = jaw_end_guide.replace('guide', 'jnt')

    jaw_end_joint = cmds.joint(name=jaw_end_joint_name)

    cmds.matchTransform(jaw_end_joint, jaw_end_guide)


    jaw_group_name = jaw_joint_name.replace('jnt','grp')

    jaw_group = cmds.group(name=jaw_group_name,empty=True)

    cmds.matchTransform(jaw_group, jaw_joint)

    cmds.parent(jaw_joint,jaw_group)

    jaw_group_parent_constraint_name = jaw_group_name.replace('grp','parentConstraint')

    cmds.parentConstraint(head_children_locator,jaw_group,name= jaw_group_parent_constraint_name,maintainOffset=True)

    jaw_joint_list.append(jaw_joint_name)
    jaw_joint_list.append(jaw_end_joint_name)

    cmds.select(clear=True)

    for eachJoint in jaw_joint_list:
        skin_joint_name = eachJoint.replace('jnt','skin_jnt')
        skin_joint =cmds.joint(name=skin_joint_name)
        cmds.matchTransform(skin_joint,eachJoint)
        jaw_skin_joint_list.append(skin_joint_name)

    cmds.select(clear=True)

    cmds.parent(jaw_skin_joint_list[0],head_skin_joint)

    return [jaw_joint_list,jaw_skin_joint_list]















