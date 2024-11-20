import maya.cmds as cmds
import maya.OpenMaya as om
import re
import importlib

from utils import controller_curves
from utils import parent_by_selection_order
from math import pow,sqrt
from utils import rigging_functions


importlib.reload(controller_curves)
importlib.reload(parent_by_selection_order)
importlib.reload(rigging_functions)

def get_object_orientation(my_object):

    world_matrix = cmds.xform(my_object, q=True, m=True, ws=True)

    x_axis = world_matrix[0:3]
    y_axis = world_matrix[4:7]
    z_axis = world_matrix[8:11]

    return [x_axis,y_axis,z_axis]

def orient_joint (joint,orient):


    if orient == 'yzx:yup':
        cmds.joint(joint,e=True,children=True,orientJoint='yzx',secondaryAxisOrient='yup',ch = True,
                   zeroScaleOrient=True)
        print('+y forward,+z up,-x, good_one')
        return [['Y',0,0,1,2,3],[0,-90,90]]

    if orient == 'zxy:yup':
        cmds.joint(joint,e=True,children=True,orientJoint='zxy',secondaryAxisOrient='yup',ch = True,
                   zeroScaleOrient=True)
        print('+z forward,+x up')
        return [['Z', 1, 0, 0, 4, 6],[0,-90,90]]

    if orient == 'xyz:yup':
        cmds.joint(joint,e=True,children=True,orientJoint='xyz',secondaryAxisOrient='yup',ch = True,
                   zeroScaleOrient=True)
        print('+x forward,+y up')
        return [['X', 0, 1, 0, 0, 0],[0,90,90]]

    if orient == 'zyx:yup':
        cmds.joint(joint,e=True,children=True,orientJoint='zyx',secondaryAxisOrient='yup',ch = True,
                   zeroScaleOrient=True)
        print('+z forward,+y up, +x, default')
        return [['Z', 0, 1, 0, 4, 0],[0,-90,90]]

    if orient == 'yxz:zup':
        cmds.joint(joint,e=True,children=True,orientJoint='yxz',secondaryAxisOrient='zup',ch = True,
                   zeroScaleOrient=True)
        print('+y forward,-z down, x, another good one')
        return [['Y', 0, 0, -1, 2, 4],[0,90,90]]

    if orient == 'xzy:zup':
        cmds.joint(joint,e=True,children=True,orientJoint='xzy',secondaryAxisOrient='zup',ch = True,
                   zeroScaleOrient=True)
        print('+x forward,y up, -z')
        return [['X', 0, 1, 0, 0, 0],[0,90,90]]

    if orient == 'zxy:zup':
        cmds.joint(joint,e=True,children=True,orientJoint='zxy',secondaryAxisOrient='zup',ch = True,
                   zeroScaleOrient=True)
        print('+z forward,Y up, +x')
        return [['Z', 0, 1, 0, 4, 0],[0,-90,90]]

    if orient == 'yzx:zup':
        cmds.joint(joint,e=True,children=True,orientJoint='yzx',secondaryAxisOrient='zup',ch = True,
                   zeroScaleOrient=True)
        print('+y forward,-z down, +x')
        return [['Y', 0, 0, -1, 2, 4],[0,90,90]]

    if orient == 'yzx:xup':
        cmds.joint(joint,e=True,children=True,orientJoint='yzx',secondaryAxisOrient='xup',ch = True,
                   zeroScaleOrient=True)
        print('+y forward,+x up, +z')
        return [['Y', 1, 0, 0, 2, 6],[0,0,0]]

    if orient == 'zyx:xup':
        cmds.joint(joint,e=True,children=True,orientJoint='zyx',secondaryAxisOrient='xup',ch = True,
                   zeroScaleOrient=True)
        print('+z forward,-x down, +y')
        return [['Z', -1, 0, 0, 4, 7],[0,-90,90]]

    if orient == 'xzy:xup':
        cmds.joint(joint,e=True,children=True,orientJoint='xzy',secondaryAxisOrient='xup',ch = True,
                   zeroScaleOrient=True)
        print('+x forward,-y down, +z')
        return [['X', 0, -1, 0, 0, 1],[0,-90,90]]


    if orient == 'zxy:xup':
        cmds.joint(joint,e=True,children=True,orientJoint='zxy',secondaryAxisOrient='xup',ch = True,
                   zeroScaleOrient=True)
        print('+Z forward,+Y up,+x')
        return [['Z', 0, 1, 0, 4, 0],[0,-90,90]]


def create_joints_from_guides(guide_list,joint_orientation):

    rig_joints_list = []
    skin_joints_list = []

    for eachGuide in guide_list:

        joint_name = eachGuide.replace('_guide', '_jnt')

        joint = cmds.joint(name=joint_name,radius=0.1)

        cmds.setAttr(joint + '.displayLocalAxis', True)

        cmds.matchTransform(joint, eachGuide)

        rigging_functions.freeze(joint)

        rig_joints_list.append(joint)

    cmds.select(clear=True)

    for eachGuide in guide_list:

        skin_joint_name = eachGuide.replace('_guide', '_skin_jnt')

        skin_joint = cmds.joint(name=skin_joint_name,radius=0.1)

        cmds.setAttr(skin_joint + '.displayLocalAxis', True)

        cmds.matchTransform(skin_joint, eachGuide)

        rigging_functions.freeze(skin_joint)

        skin_joints_list.append(skin_joint)

    orient_joint(rig_joints_list[0], joint_orientation)
    cmds.select(clear=True)
    chain_orientation = orient_joint(skin_joints_list[0], joint_orientation)
    cmds.select(clear=True)
    cmds.delete(rig_joints_list[len(rig_joints_list)-1])
    cmds.delete(skin_joints_list[len(skin_joints_list) - 1])

    cmds.select(rig_joints_list[0],hierarchy=True)
    rig_joints_list = cmds.ls(sl=True)
    cmds.select(clear=True)
    cmds.select(skin_joints_list[0], hierarchy=True)
    skin_joints_list = cmds.ls(sl=True)
    cmds.select(clear=True)

    return [rig_joints_list,skin_joints_list,chain_orientation]

def connect_objects_trs(drive_joint_list,skin_joint_list):

    connect_dict = {drive_joint_list[i]: skin_joint_list[i] for i in range(len(drive_joint_list))}

    for driveJoint, skinJoint in connect_dict.items():

        cmds.connectAttr(driveJoint+'.scale.scaleX',skinJoint+'.scale.scaleX')
        cmds.connectAttr(driveJoint + '.scale.scaleY', skinJoint + '.scale.scaleY')
        cmds.connectAttr(driveJoint + '.scale.scaleZ', skinJoint + '.scale.scaleZ')

        cmds.connectAttr(driveJoint + '.translate.translateX', skinJoint + '.translate.translateX')
        cmds.connectAttr(driveJoint + '.translate.translateY', skinJoint + '.translate.translateY')
        cmds.connectAttr(driveJoint + '.translate.translateZ', skinJoint + '.translate.translateZ')

        cmds.connectAttr(driveJoint + '.rotate.rotateX', skinJoint + '.rotate.rotateX')
        cmds.connectAttr(driveJoint + '.rotate.rotateY', skinJoint + '.rotate.rotateY')
        cmds.connectAttr(driveJoint + '.rotate.rotateZ', skinJoint + '.rotate.rotateZ')

def parent_constraint_between_joints(drive_joint_list,skin_joint_list):

    connect_dict = {drive_joint_list[i]: skin_joint_list[i] for i in range(len(drive_joint_list))}

    for driveJoint, skinJoint in connect_dict.items():

        cmds.parentConstraint(driveJoint,skinJoint,maintainOffset=True)











