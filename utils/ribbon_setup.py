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


"""
copiar lo de abajo na mas pa usar el codigo

import maya.cmds as cmds

import importlib

from utils import ribbon_setup
from auto_rigger import spine_rig

importlib.reload(ribbon_setup)
importlib.reload(spine_rig)

start = ''

end = ''

rotate_in_Z = True

joint_list = spine_rig.create_spine_joints()[0]

create_full_bind_hierarchy = False

ribbon_setup.create_ribbon(start,end,rotate_in_Z,joint_list,create_full_bind_hierarchy)

"""

def create_ribbon(start_object,end_object,joint_list,create_full_bind_hierarchy):

    joints_to_bind_list = []

    mid_pos_locator = cmds.spaceLocator(name='mid_locator_temp')[0]

    cmds.delete(cmds.parentConstraint(start_object,end_object,mid_pos_locator))

    surface_name = joint_list[0].replace('_jnt', '_nurbs')

    first_joint = joint_list[0]


    distance_between_start_end = rigging_functions.get_distance_between_two_objects(start_object,end_object)

    nurbs_plane = plane_from_points_snap.create_plane(joint_list,surface_name)

    print(distance_between_start_end)

    follicle_group_name = joint_list[0].replace('_jnt','_follicle_grp')

    follicle_group = cmds.group(em=True, name = follicle_group_name)

    cmds.select(nurbs_plane)

    follicle_node_list = []

    for i in range(len(joint_list)):

        follicle_node_name = joint_list[i].replace('_jnt','_follicle_shape')
        follicle_node_list.append(follicle_node_name)

        y = str(i + 1)
        cmds.createNode('follicle', n=follicle_node_name)
        cmds.parent('follicle' + y, follicle_group, s=True)
        cmds.setAttr(follicle_node_name + '.simulationMethod', 0)
        cmds.makeIdentity(nurbs_plane, apply=True, t=1, r=1, s=1, n=0)

        cmds.connectAttr(follicle_node_name + '.outRotate', 'follicle' + y + '.rotate', f=True)
        cmds.connectAttr(follicle_node_name + '.outTranslate', 'follicle' + y + '.translate')
        cmds.connectAttr(nurbs_plane + '.worldMatrix', follicle_node_name + '.inputWorldMatrix')
        cmds.connectAttr(nurbs_plane +'.local', follicle_node_name + '.inputSurface')

        cmds.setAttr('follicle' + y + '.parameterV', 0.5)
        cmds.setAttr('follicle' + y + '.parameterU', float(i) / (len(joint_list) - 1))

    #cmds.delete(cmds.parentConstraint(mid_pos_locator, nurbs_plane))

    follicle_transform_list = cmds.listRelatives(follicle_group,allDescendents=True,type = 'transform')

    rename_follicle_dict = {follicle_node_list[i]: follicle_transform_list[i] for i in range(len(follicle_node_list))}

    for follicleNode, follicleTransform in rename_follicle_dict.items():
        follicle_transform_name =  follicleNode.replace('_follicle_shape','_follicle')
        cmds.rename(follicleTransform,follicle_transform_name)

    follicle_transform_list = cmds.listRelatives(follicle_group, allDescendents=True, type='transform')

    parent_joint_follicle_dict = {joint_list[i]: follicle_transform_list[i] for i in range(len(joint_list))}

    for eachItem in follicle_transform_list:
        cmds.parent(eachItem, world=True)

    for joint, follicleTransform in parent_joint_follicle_dict.items():
    
        cmds.parent(joint,follicleTransform)

    cmds.matchTransform(follicle_group,start_object)

    for eachFollicle in follicle_transform_list:
        cmds.setAttr(eachFollicle+'.inheritsTransform',0)
        cmds.parent(eachFollicle,follicle_group)

    start_follicle_joint_name=joint_list[0].replace('_jnt','_follicle_jnt')

    middle_index = int(len(joint_list) / 2)  # = int(2.5) = 2

    middle_follicle_joint_name = joint_list[middle_index].replace('_jnt','_follicle_jnt')

    end_follicle_joint_name = joint_list[len(joint_list)-1].replace('_jnt', '_follicle_jnt')

    follicle_bind_joints_list = []

    start_follicle_joint = cmds.joint(name=start_follicle_joint_name,radius=1.2)

    follicle_bind_joints_list.append(start_follicle_joint)

    middle_follicle_joint = cmds.joint(name=middle_follicle_joint_name,radius=1.2)

    follicle_bind_joints_list.append(middle_follicle_joint)

    end_follicle_joint = cmds.joint(name=end_follicle_joint_name,radius=1.2)

    follicle_bind_joints_list.append(end_follicle_joint)

    for eachJoint in follicle_bind_joints_list:
        cmds.parent(eachJoint,world = True)

    cmds.matchTransform(start_follicle_joint,joint_list[0])

    cmds.matchTransform(middle_follicle_joint, joint_list[middle_index])

    cmds.matchTransform(end_follicle_joint,joint_list[len(joint_list)-1])


    for eachJoint in follicle_bind_joints_list:
        rigging_functions.freeze(eachJoint)
        cmds.setAttr(eachJoint + '.displayLocalAxis', True)


    ribbon_setup_group_name = joint_list[0].replace('_jnt','_ribbonSetup_grp')
    ribbon_setup_group = cmds.group(name=ribbon_setup_group_name,empty=True)
    cmds.setAttr(ribbon_setup_group + '.inheritsTransform', 0)

    cmds.delete(mid_pos_locator)

    if not create_full_bind_hierarchy:

        for eachJoint in follicle_bind_joints_list:
            cmds.select(eachJoint, add=True)

        cmds.select(nurbs_plane,add=True)

        cmds.skinCluster(bindMethod=0, maximumInfluences=3, name=surface_name + '_skinCluster')

        cmds.select(clear=True)

        for eachJoint in follicle_bind_joints_list:
            cmds.parent(eachJoint,ribbon_setup_group)
            cmds.setAttr(eachJoint + '.visibility', 0)


        cmds.parent(nurbs_plane,ribbon_setup_group)
        cmds.parent(follicle_group, ribbon_setup_group)

        cmds.select(clear=True)

        return [follicle_bind_joints_list,ribbon_setup_group]

    else:

        cmds.delete(start_follicle_joint)
        cmds.delete(middle_follicle_joint)
        cmds.delete(end_follicle_joint)

        for eachJoint in joint_list:

            joint_to_bind_name = eachJoint.replace('_jnt','_ribbon_jnt')

            joint_to_bind = cmds.joint(name=joint_to_bind_name,radius=1.3)

            cmds.setAttr(joint_to_bind + '.displayLocalAxis', True)

            cmds.setAttr(joint_to_bind + '.visibility', 0)

            cmds.matchTransform(joint_to_bind, eachJoint)

            joints_to_bind_list.append(joint_to_bind)


        cmds.select(joints_to_bind_list[0],hierarchy=True,add=True)

        cmds.select(nurbs_plane,add=True)

        cmds.skinCluster(bindMethod=1, maximumInfluences=5, name=surface_name + '_skinCluster')

        cmds.select(clear=True)

        ribbon_driver_group_name = joints_to_bind_list[0].replace('_jnt','_grp')

        ribbon_driver_group = cmds.group(name=ribbon_driver_group_name,empty=True)

        cmds.parent(joints_to_bind_list[0],ribbon_driver_group)
        cmds.setAttr(ribbon_driver_group + '.inheritsTransform', 0)

        cmds.parent(ribbon_driver_group, ribbon_setup_group)
        cmds.parent(nurbs_plane, ribbon_setup_group)
        cmds.parent(follicle_group, ribbon_setup_group)



        return [joints_to_bind_list,ribbon_setup_group,surface_name]





















