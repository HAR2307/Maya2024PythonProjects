import maya.cmds as cmds

from utils import parent_by_selection_order
from utils import unparent_by_selection_order
from utils import rigging_functions
from utils import rigging_functions_02
from utils import controller_curves
from utils import ribbon_setup
from utils import limb_ribbon_setup


import importlib
importlib.reload(rigging_functions)
importlib.reload(rigging_functions_02)
importlib.reload(parent_by_selection_order)
importlib.reload(unparent_by_selection_order)
importlib.reload(controller_curves)
importlib.reload(ribbon_setup)
importlib.reload(limb_ribbon_setup)


"""
copiar lo de abajo na mas pa usar el codigo

import maya.cmds as cmds

import importlib

from auto_rigger import leg_rig

importlib.reload(leg_rig)

leg_joints = leg_rig.create_leg_joints()

left_leg_rig_joints = leg_joints[0]
right_leg_rig_joints = leg_joints[2]


left_fk_leg = leg_rig.create_fk_leg_rig(left_leg_rig_joints)
right_fk_leg = leg_rig.create_fk_leg_rig(right_leg_rig_joints)

"""
def create_leg_joints():


    left_leg_rig_joints = []
    left_foot_rig_joints = []


    left_leg_guides = []
    left_foot_guides = []
    right_leg_guides = []
    right_foot_guides = []

    left_leg_skin_joints = []
    right_leg_skin_joints = []


    all_left_guides = sorted(cmds.listRelatives('lf' + '*leg_guide_grp',allDescendents=True,type='transform'))
    all_right_guides = sorted(cmds.listRelatives('rt' + '*leg_guide_grp', allDescendents=True, type='transform'))

    for eachGuide in all_left_guides:
        if 'Foot' not in eachGuide:
            left_leg_guides.append(eachGuide)
        else:
            left_foot_guides.append(eachGuide)


    for eachGuide in left_leg_guides:

        leg_joint_name = eachGuide.replace('guide','jnt')
        leg_joint = cmds.joint(name = leg_joint_name)
        cmds.matchTransform(leg_joint,eachGuide)
        left_leg_rig_joints.append(leg_joint_name)
        cmds.setAttr(leg_joint + '.displayLocalAxis', True)

    cmds.select(clear=True)

    for eachGuide in all_right_guides:
        if 'Foot' not in eachGuide:
            right_leg_guides.append(eachGuide)
        else:
            right_foot_guides.append(eachGuide)


    cmds.select(clear=True)

    for eachGuide in left_foot_guides:

        foot_joint_name = eachGuide.replace('guide', 'jnt')
        foot_joint = cmds.joint(name = foot_joint_name)
        cmds.select(clear=True)
        cmds.matchTransform(foot_joint, eachGuide)
        left_foot_rig_joints.append(foot_joint_name)
        cmds.setAttr(foot_joint + '.displayLocalAxis', True)

    cmds.select(clear=True)

    right_leg_rig_joints = cmds.mirrorJoint(left_leg_rig_joints[0],mirrorYZ=True,mirrorBehavior = True,searchReplace=['lf','rt'])

    cmds.select(clear=True)

    right_foot_rig_joints = []

    for eachJoint in left_foot_rig_joints:
        right_foot_joint = cmds.mirrorJoint(eachJoint, mirrorYZ=True, mirrorBehavior = True, searchReplace=['lf', 'rt'])
        cmds.select(clear=True)
        right_foot_rig_joints.append(right_foot_joint[0])

    cmds.select(clear=True)

    match_transform_dict = {right_leg_guides[i]: right_leg_rig_joints[i] for i in range(len(right_leg_guides))}

    for guide, joint in match_transform_dict.items():

        guide_translations = cmds.xform(guide, query=True, translation=True,worldSpace=True)
        #joint_rotations = cmds.xform(joint, query=True, rotation=True,worldSpace=True)

        cmds.xform(joint,translation=guide_translations,worldSpace=True)

    cmds.select(clear=True)

    left_leg_upper_leg_start = left_leg_rig_joints[1]
    left_knee = left_leg_rig_joints[2]
    left_ankle = left_leg_rig_joints[3]


    left_upper_leg_rig_chain = rigging_functions_02.create_joints_from_two_points(left_leg_upper_leg_start,
                                                                                  left_knee, 6, 'lf_',
                                                                                  '_upperLeg_jnt')
    cmds.select(clear=True)


    left_lower_leg_rig_chain = rigging_functions_02.create_joints_from_two_points(left_knee,
                                                                                  left_ankle, 6, 'lf_',
                                                                                  '_lowerLeg_jnt')
    cmds.select(clear=True)

    right_upper_leg_rig_chain = cmds.mirrorJoint(left_upper_leg_rig_chain[0], mirrorYZ=True, mirrorBehavior=True,
                                                 searchReplace=['lf', 'rt'])

    right_lower_leg_rig_chain = cmds.mirrorJoint(left_lower_leg_rig_chain[0], mirrorYZ=True, mirrorBehavior=True,
                                                 searchReplace=['lf', 'rt'])

    cmds.select(clear=True)

    left_leg_joint_chain = left_upper_leg_rig_chain + left_lower_leg_rig_chain

    right_leg_joint_chain = right_upper_leg_rig_chain + right_lower_leg_rig_chain

    print(left_leg_joint_chain)

    print(right_leg_joint_chain)

    left_leg_joint_chain_start = left_leg_joint_chain[0]
    left_leg_joint_chain_end = left_leg_joint_chain[len(left_leg_joint_chain) - 1]

    #left_leg_ribbon_setup = limb_ribbon_setup.create_ribbon(left_leg_joint_chain_start,left_leg_joint_chain_end,left_leg_joint_chain)









    return [left_leg_rig_joints,left_foot_rig_joints,right_leg_rig_joints,right_foot_rig_joints,left_leg_skin_joints,right_leg_skin_joints]

def add_ribbon_to_legs(joint_list):

    upper_leg_start = joint_list[0]
    upper_leg_end = joint_list[2]
    lower_leg_end = joint_list[3]






def create_fk_leg_rig(leg_rig_joints):

    cmds.select(clear=True)

    controller_color = 0

    if 'lf' in leg_rig_joints[0]:
        controller_color = 6
    else:
        controller_color = 4

    fk_setup_list = rigging_functions_02.fk_setup(leg_rig_joints,controller_color)

    cmds.select(clear=True)

    fk_joint_list = fk_setup_list[0]
    fk_ctrl_list  = fk_setup_list[1]
    fk_ctrl_group_list = fk_setup_list[2]




    return [fk_joint_list,fk_ctrl_list,fk_ctrl_group_list]

















