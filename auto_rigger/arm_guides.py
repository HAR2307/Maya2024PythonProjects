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
from auto_rigger import arm_guides

importlib.reload(arm_guides)

arm_guides.create_left_arm_guides()

arm_guides.mirror_arm_guides()

"""


def create_left_arm_guides(side,letter):

    chest_guide = ''

    lf_shoulder_guide = controller_curves.create_curve('cross',controller_name=side + '_' + '0' + '_'+ letter + '_' + 'shoulder_guide')
    lf_upper_arm_guide = controller_curves.create_curve('cross',controller_name=side + '_' + '1' + '_'+ letter +  '_' + 'upperArm_guide')
    lf_elbow_guide = controller_curves.create_curve('cross',controller_name=side + '_' + '2' + '_'+ letter +  '_' + 'elbow_guide')
    lf_wrist_guide = controller_curves.create_curve('cross',controller_name=side + '_' + '3' + '_'+ letter + '_' + 'wrist_guide')
    lf_arm_end_guide = controller_curves.create_curve('cross',controller_name=side + '_' + '4' + '_'+ letter + '_' + 'armEnd_guide')

    left_arm_guides_list = [lf_shoulder_guide, lf_upper_arm_guide, lf_elbow_guide, lf_wrist_guide,
                            lf_arm_end_guide]

    for eachGuide in left_arm_guides_list:
        rigging_functions.set_colors(eachGuide,6)

    print(left_arm_guides_list)

    cmds.select(clear = True)

    cmds.setAttr(lf_shoulder_guide + '.tx', 2)
    cmds.setAttr(lf_shoulder_guide + '.ty', 15)

    cmds.setAttr(lf_upper_arm_guide + '.tx', 4)
    cmds.setAttr(lf_upper_arm_guide + '.ty', 15)


    cmds.setAttr(lf_elbow_guide + '.tx', 6)
    cmds.setAttr(lf_elbow_guide + '.ty', 15)


    cmds.setAttr(lf_wrist_guide + '.tx', 8)
    cmds.setAttr(lf_wrist_guide + '.ty', 15)

    cmds.setAttr(lf_arm_end_guide + '.tx', 10)
    cmds.setAttr(lf_arm_end_guide + '.ty', 15)


    left_arm_guides_list = [lf_shoulder_guide,lf_upper_arm_guide,lf_elbow_guide,lf_wrist_guide,lf_arm_end_guide]

    print(left_arm_guides_list)

    parent_by_selection_order.parent_by_selection_list(left_arm_guides_list)

    left_arm_guide_group = cmds.group(em=True, name =side + '_' + letter + '_' + 'arm_guide_grp' )

    cmds.matchTransform(left_arm_guide_group,lf_shoulder_guide)
    cmds.parent(lf_shoulder_guide,left_arm_guide_group)

    #if cmds.objExists('*chest_guide'):
    #
    #    chest_guide = cmds.ls('*chest_guide',type='transform')[0]
    #
    #    cmds.parent(left_arm_guide_group,chest_guide)

    return left_arm_guides_list


def mirror_arm_guides():

    rigging_functions.mirror_guides()
























