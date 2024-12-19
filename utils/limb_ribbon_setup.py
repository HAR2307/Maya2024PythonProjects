import maya.cmds as cmds

from utils import parent_by_selection_order
from utils import unparent_by_selection_order
from utils import rigging_functions
from utils import controller_curves
from utils import create_ribbon_plane
from utils import nurbs_ribbon_deformer_setup
from utils import plane_from_points_snap



import importlib
importlib.reload(rigging_functions)
importlib.reload(parent_by_selection_order)
importlib.reload(unparent_by_selection_order)
importlib.reload(controller_curves)
importlib.reload(create_ribbon_plane)
importlib.reload(nurbs_ribbon_deformer_setup)
importlib.reload(plane_from_points_snap)


def create_ribbon(start_object, end_object, joint_list):

    first_middle_index = joint_list[2]

    second_middle_index = joint_list[6]

    joints_to_bind_list = []

    mid_pos_locator = cmds.spaceLocator(name='mid_locator_temp')[0]

    cmds.delete(cmds.parentConstraint(start_object, end_object, mid_pos_locator))

    surface_name = joint_list[0].replace('_jnt', '_nurbs')

    first_joint = joint_list[0]

    distance_between_start_end = rigging_functions.get_distance_between_two_objects(start_object, end_object)

    nurbs_plane = plane_from_points_snap.create_plane(joint_list, surface_name)

    print(distance_between_start_end)

    follicle_group_name = joint_list[0].replace('_jnt', '_follicle_grp')

    follicle_group = cmds.group(em=True, name=follicle_group_name)

    cmds.select(nurbs_plane)

    follicle_node_list = []

    for i in range(len(joint_list)):
        follicle_node_name = joint_list[i].replace('_jnt', '_follicle_shape')
        follicle_node_list.append(follicle_node_name)

        y = str(i + 1)
        cmds.createNode('follicle', n=follicle_node_name)
        cmds.parent('follicle' + y, follicle_group, s=True)
        cmds.setAttr(follicle_node_name + '.simulationMethod', 0)
        cmds.makeIdentity(nurbs_plane, apply=True, t=1, r=1, s=1, n=0)

        cmds.connectAttr(follicle_node_name + '.outRotate', 'follicle' + y + '.rotate', f=True)
        cmds.connectAttr(follicle_node_name + '.outTranslate', 'follicle' + y + '.translate')
        cmds.connectAttr(nurbs_plane + '.worldMatrix', follicle_node_name + '.inputWorldMatrix')
        cmds.connectAttr(nurbs_plane + '.local', follicle_node_name + '.inputSurface')

        cmds.setAttr('follicle' + y + '.parameterV', 0.5)
        cmds.setAttr('follicle' + y + '.parameterU', float(i) / (len(joint_list) - 1))

    # cmds.delete(cmds.parentConstraint(mid_pos_locator, nurbs_plane))

    follicle_transform_list = cmds.listRelatives(follicle_group, allDescendents=True, type='transform')

    rename_follicle_dict = {follicle_node_list[i]: follicle_transform_list[i] for i in range(len(follicle_node_list))}

    for follicleNode, follicleTransform in rename_follicle_dict.items():
        follicle_transform_name = follicleNode.replace('_follicle_shape', '_follicle')
        cmds.rename(follicleTransform, follicle_transform_name)

    follicle_transform_list = cmds.listRelatives(follicle_group, allDescendents=True, type='transform')

    parent_joint_follicle_dict = {joint_list[i]: follicle_transform_list[i] for i in range(len(joint_list))}

    for eachItem in follicle_transform_list:
        cmds.parent(eachItem, world=True)

    for joint, follicleTransform in parent_joint_follicle_dict.items():
        cmds.parent(joint, follicleTransform)

    cmds.matchTransform(follicle_group, start_object)

    for eachFollicle in follicle_transform_list:
        cmds.setAttr(eachFollicle + '.inheritsTransform', 0)
        cmds.parent(eachFollicle, follicle_group)

    start_follicle_joint_name = joint_list[0].replace('_jnt', '_follicle_jnt')

    first_middle_follicle_joint_name = first_middle_index.replace('_jnt', '_follicle_jnt')

    second_middle_follicle_joint_name = second_middle_index.replace('_jnt', '_follicle_jnt')

    end_follicle_joint_name = joint_list[len(joint_list) - 1].replace('_jnt', '_follicle_jnt')

    follicle_bind_joints_list = []

    start_follicle_joint = cmds.joint(name=start_follicle_joint_name, radius=1.2)

    follicle_bind_joints_list.append(start_follicle_joint)

    first_middle_follicle_joint = cmds.joint(name=first_middle_follicle_joint_name, radius=1.2)

    follicle_bind_joints_list.append(first_middle_follicle_joint)

    second_middle_follicle_joint = cmds.joint(name=second_middle_follicle_joint_name, radius=1.2)

    follicle_bind_joints_list.append(second_middle_follicle_joint)

    end_follicle_joint = cmds.joint(name=end_follicle_joint_name, radius=1.2)

    follicle_bind_joints_list.append(end_follicle_joint)

    for eachJoint in follicle_bind_joints_list:
        cmds.parent(eachJoint, world=True)

    cmds.matchTransform(start_follicle_joint, joint_list[0])

    cmds.matchTransform(first_middle_follicle_joint, first_middle_index)

    cmds.matchTransform(second_middle_follicle_joint, second_middle_index)

    cmds.matchTransform(end_follicle_joint, joint_list[len(joint_list) - 1])

    for eachJoint in follicle_bind_joints_list:
        rigging_functions.freeze(eachJoint)
        cmds.setAttr(eachJoint + '.displayLocalAxis', True)

    ribbon_setup_group_name = joint_list[0].replace('_jnt', '_ribbonSetup_grp')
    ribbon_setup_group = cmds.group(name=ribbon_setup_group_name, empty=True)
    cmds.setAttr(ribbon_setup_group + '.inheritsTransform', 0)

    cmds.delete(mid_pos_locator)

    for eachJoint in follicle_bind_joints_list:
        cmds.select(eachJoint, add=True)

    cmds.select(nurbs_plane, add=True)

    cmds.skinCluster(bindMethod=0, maximumInfluences=5, name=surface_name + '_skinCluster')

    cmds.select(clear=True)

    for eachJoint in follicle_bind_joints_list:
        cmds.parent(eachJoint, ribbon_setup_group)
        cmds.setAttr(eachJoint + '.visibility', 0)

    cmds.parent(nurbs_plane, ribbon_setup_group)
    cmds.parent(follicle_group, ribbon_setup_group)

    cmds.select(clear=True)

    return [follicle_bind_joints_list, ribbon_setup_group, joint_list]

   