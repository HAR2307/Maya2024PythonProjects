import maya.cmds as cmds

from utils import parent_by_selection_order
from utils import unparent_by_selection_order
from utils import rigging_functions
from utils import rigging_functions_02
from utils import controller_curves
from utils import ribbon_setup
from auto_rigger import ik_fk_chain_rig_setup
from utils import create_master_controller

import importlib
importlib.reload(rigging_functions)
importlib.reload(rigging_functions_02)
importlib.reload(parent_by_selection_order)
importlib.reload(unparent_by_selection_order)
importlib.reload(controller_curves)
importlib.reload(ik_fk_chain_rig_setup)
importlib.reload(ribbon_setup)
importlib.reload(create_master_controller)

"""
copiar lo de abajo na mas pa usar el codigo

import maya.cmds as cmds

import importlib

from auto_rigger import spine_rig

importlib.reload(spine_rig)


spine_joints = spine_rig.create_spine_joints()
spine_rig_joints = spine_joints[0]
spine_skin_joints  = spine_joints[1]
cog_drive_joint = spine_joints[2]
cog_skin_joint = spine_joints[3]

spine_rig.create_spine_rig(spine_rig_joints,spine_skin_joints,cog_drive_joint,cog_skin_joint)

"""

def create_spine_joints():

    spine_joints_list = []

    hips_guide_name =  ''

    cog_guide_name = ''

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

    cmds.select(clear=True)


    if cmds.objExists('*cog_guide'):
        cog_guide_name = cmds.ls('*cog_guide', type='transform')[0]

    cog_drive_joint_name = cog_guide_name.replace('guide', 'jnt').replace('__','_')
    cog_skin_joint_name = cog_guide_name.replace('guide', 'skin_jnt').replace('__','_')

    cog_drive_joint = cmds.joint(name = cog_drive_joint_name)
    cmds.matchTransform(cog_drive_joint,cog_guide_name)

    cmds.select(clear=True)


    cog_skin_joint = cmds.joint(name= cog_skin_joint_name)
    cmds.matchTransform(cog_skin_joint, cog_guide_name)

    cmds.select(clear=True)




    return [drive_spine_joint_list,skin_joint_list,cog_drive_joint,cog_skin_joint]

def create_spine_rig (rig_joints,skin_joints,cog_drive_joint,cog_skin_joint):


    guide_root_group_name = cmds.ls('*_mainGuides_grp',type='transform')[0]

    rig_main_group_name = guide_root_group_name.replace('_mainGuides_grp','_rigMain_grp')

    rig_main_group = cmds.group(empty=True,name=rig_main_group_name)

    asset_name = guide_root_group_name.replace('_mainGuides_grp','')

    master_ctrl_list = create_master_controller.create_hierarchy(asset_name)

    master_TRS = master_ctrl_list[0]
    master_TR = master_ctrl_list[1]
    skin_joints_group = master_ctrl_list[2]
    root_orient_loc = master_ctrl_list[3]


    start_joint =  rig_joints[0]
    end_joint =  rig_joints[len(rig_joints) - 1]
    spline_spans = 4
    spline_handle_name = 'cn_spine_ik_splineHandle'
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


    ribbon_joint = ribbon_setup.create_ribbon(start_joint, end_joint, rig_joints, create_full_bind_hierarchy)

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
                                      master_TRS,
                                      spline_axis)


    cmds.select(clear=True)

    cog_controller_size = 1
    cog_controller_color = 9
    controller_shape = 'square'
    prefix = '_ctrl'
    constraint_type = 'parent'
    maintain_offset = False

    cog_ctrl = rigging_functions.create_controller(cog_drive_joint, cog_controller_size, cog_controller_color, controller_shape, prefix, constraint_type,maintain_offset)

    cog_ctrl_name = cog_ctrl[0]
    cog_group_ctrl_name = cog_ctrl[1]

    cmds.parent(ribbon_setup_group,spine_ik_fk_setup_group[1])

    cmds.parent(spine_ik_fk_setup_group[0],rig_main_group)

    cmds.parent(cog_group_ctrl_name,rig_main_group)
    cmds.parent(cog_drive_joint, cog_ctrl_name)

    cmds.parent(spine_ik_fk_setup_group[0], cog_ctrl_name)

    cmds.parent(skin_joints[0],skin_joints_group)

    cmds.parent(cog_skin_joint,skin_joints_group)

    cmds.parent(skin_joints[0],cog_skin_joint)

    cmds.parent(rig_main_group, master_TR)

    cmds.select(clear=True)

    chest_joint = end_joint

    spline_ik_fk_ctrl_name = spine_ik_fk_setup_group[1]

    rigging_functions.set_colors(spline_ik_fk_ctrl_name, 9)

    cmds.select(clear=True)

    rig_joints.append(cog_drive_joint)
    skin_joints.append(cog_skin_joint)

    rigging_functions_02.parent_constraint_between_joints(rig_joints,skin_joints)

    ik_fk_setup_root_group_name  = spine_ik_fk_setup_group[0]

    cmds.parentConstraint(cog_drive_joint,cog_skin_joint)

    chest_children_locator_name = end_joint.replace('jnt', 'loc')

    chest_children_locator = cmds.spaceLocator(name=chest_children_locator_name)[0]

    cmds.matchTransform(chest_children_locator,end_joint)

    cmds.parent(chest_children_locator_name,end_joint)


    return [ik_fk_setup_root_group_name,chest_joint,master_ctrl_list,rig_main_group_name,cog_drive_joint,cog_ctrl_name,cog_group_ctrl_name,chest_children_locator_name,root_orient_loc]








   










































































