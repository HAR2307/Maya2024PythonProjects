import maya.cmds as cmds

from utils import parent_by_selection_order
from utils import unparent_by_selection_order
from utils import rigging_functions
from utils import rigging_functions_02
from utils import controller_curves
from utils import ribbon_setup


import importlib
importlib.reload(rigging_functions)
importlib.reload(rigging_functions_02)
importlib.reload(parent_by_selection_order)
importlib.reload(unparent_by_selection_order)
importlib.reload(controller_curves)
importlib.reload(ribbon_setup)

"""
copiar lo de abajo na mas pa usar el codigo

import maya.cmds as cmds

import importlib

from auto_rigger import leg_rig

importlib.reload(leg_rig)

left_side = 'lf'
right_side = 'rt'

left_leg_joints = leg_rig.create_leg_joints(left_side)[0]
right_leg_joints = leg_rig.create_leg_joints(right_side)[0]

left_fk_leg = leg_rig.create_fk_leg_rig(left_leg_joints)
right_fk_leg = leg_rig.create_fk_leg_rig(right_leg_joints)

"""
def create_leg_joints(side):

    leg_rig_joints = []
    leg_fk_rig_joints = []
    leg_ik_rig_joints = []
    foot_rig_joints = []

    leg_guides = []
    foot_guides = []

    all_leg_guides_list = sorted(cmds.listRelatives(side + '*leg_guide_grp',allDescendents=True,type='transform'))

    for eachGuide in all_leg_guides_list:
        if 'Foot' not in eachGuide:
            leg_guides.append(eachGuide)
        else:
            foot_guides.append(eachGuide)


    for eachGuide in leg_guides:

        leg_joint_name = eachGuide.replace('guide','jnt')
        leg_joint = cmds.joint(name = leg_joint_name)
        cmds.matchTransform(leg_joint,eachGuide)
        leg_rig_joints.append(leg_joint_name)

    cmds.select(clear=True)

    for eachGuide in foot_guides:

        foot_joint_name = eachGuide.replace('guide', 'jnt')
        foot_joint = cmds.joint(name = foot_joint_name)
        cmds.select(clear=True)
        cmds.matchTransform(foot_joint, eachGuide)
        foot_rig_joints.append(foot_joint_name)


    return [leg_rig_joints,foot_rig_joints]

def create_fk_leg_rig(leg_rig_joints):

    cmds.select(clear=True)

    controller_color = 0

    if 'lf' in leg_rig_joints[0]:
        controller_color = 6
    else:
        controller_color = 4

    rigging_functions_02.fk_setup(leg_rig_joints,controller_color)

    cmds.select(clear=True)

















