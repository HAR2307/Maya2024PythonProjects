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
from auto_rigger import leg_guides

importlib.reload(leg_guides)

leg_guides.create_left_leg_guides()

leg_guides.mirror_leg_guides()

"""


def create_left_leg_guides(side,letter):

    hips_guide = ''

    lf_hip_guide = controller_curves.create_curve('cross',controller_name=side + '_' + '0' + '_'+ letter + '_' + 'hip_guide')
    lf_upper_leg_guide = controller_curves.create_curve('cross',controller_name=side + '_' + '1' + '_'+ letter +  '_' + 'upperLeg_guide')
    lf_knee_guide = controller_curves.create_curve('cross',controller_name=side + '_' + '2' + '_'+ letter +  '_' + 'knee_guide')
    lf_ankle_guide = controller_curves.create_curve('cross',controller_name=side + '_' + '3' + '_'+ letter + '_' + 'ankle_guide')
    lf_ball_guide = controller_curves.create_curve('cross',controller_name=side + '_' + '4' + '_'+ letter + '_' + 'ball_guide')
    lf_leg_end_guide = controller_curves.create_curve('cross',controller_name=side + '_' + '5' + '_'+ letter + '_' + 'legEnd_guide')

    cmds.select(clear = True)

    cmds.setAttr(lf_hip_guide + '.tx', 1.5)
    cmds.setAttr(lf_hip_guide + '.ty', 8)

    cmds.setAttr(lf_upper_leg_guide + '.tx', 3)
    cmds.setAttr(lf_upper_leg_guide + '.ty', 8)

    cmds.setAttr(lf_knee_guide + '.tx', 3)
    cmds.setAttr(lf_knee_guide + '.ty', 4)

    cmds.setAttr(lf_ankle_guide + '.tx', 3)
    cmds.setAttr(lf_ankle_guide + '.ty', 1)

    cmds.setAttr(lf_ball_guide + '.tx', 3)
    cmds.setAttr(lf_ball_guide + '.tz', 1)

    cmds.setAttr(lf_leg_end_guide + '.tx', 3)
    cmds.setAttr(lf_leg_end_guide + '.tz', 2)


    left_leg_guides_list = [lf_hip_guide,lf_upper_leg_guide,lf_knee_guide,lf_ankle_guide,lf_ball_guide,lf_leg_end_guide]

    for eachGuide in left_leg_guides_list:
        rigging_functions.set_colors(eachGuide, 6)

    print(left_leg_guides_list)

    parent_by_selection_order.parent_by_selection_list(left_leg_guides_list)

    left_leg_guide_group = cmds.group(em=True, name =side + '_' + letter + '_' + 'leg_guide_grp' )

    cmds.matchTransform(left_leg_guide_group,lf_hip_guide)
    cmds.parent(lf_hip_guide,left_leg_guide_group)


    lf_heel_guide = controller_curves.create_curve('cross',
                                                  controller_name=side + '_' + '6' + '_' + letter + '_' + 'heelFoot_guide')
    lf_outer_foot_guide = controller_curves.create_curve('cross',
                                                        controller_name=side + '_' + '6' + '_' + letter + '_' + 'outerFoot_guide')
    lf_inner_foot_guide = controller_curves.create_curve('cross',
                                                   controller_name=side + '_' + '6' + '_' + letter + '_' + 'innerFoot_guide')

    foot_guides_list = [lf_heel_guide,lf_outer_foot_guide,lf_inner_foot_guide]

    for eachFootGuide in foot_guides_list:
        rigging_functions.set_scales(eachFootGuide,.2)


    cmds.setAttr(lf_heel_guide + '.tx', 3)
    cmds.setAttr(lf_heel_guide + '.tz', -1)

    cmds.setAttr(lf_outer_foot_guide + '.tx', 4)
    cmds.setAttr(lf_outer_foot_guide + '.tz', 1)

    cmds.setAttr(lf_inner_foot_guide + '.tx', 2)
    cmds.setAttr(lf_inner_foot_guide + '.tz', 1)

    foot_guides_list = [lf_heel_guide,lf_outer_foot_guide,lf_inner_foot_guide]

    for eachFootGuide in foot_guides_list:
        cmds.parent(eachFootGuide,lf_ankle_guide)

    lf_upperKnee_guide = controller_curves.create_curve('cross',
                                                   controller_name=side + '_' + '7' + '_' + letter + '_' + 'upperKnee_guide')
    rigging_functions.set_scales(lf_upperKnee_guide, .2)
    rigging_functions.set_colors(lf_upperKnee_guide, 6)

    lf_lowerKnee_guide = controller_curves.create_curve('cross',
                                                         controller_name=side + '_' + '7' + '_' + letter + '_' + 'lowerKnee_guide')
    rigging_functions.set_scales(lf_lowerKnee_guide, .2)
    rigging_functions.set_colors(lf_lowerKnee_guide, 6)

    cmds.setAttr(lf_upperKnee_guide + '.tx', 3)
    cmds.setAttr(lf_upperKnee_guide + '.ty', 4.1)

    cmds.setAttr(lf_lowerKnee_guide + '.tx', 3)
    cmds.setAttr(lf_lowerKnee_guide + '.ty', 3.9)

    cmds.parent(lf_upperKnee_guide,lf_knee_guide)
    cmds.parent(lf_lowerKnee_guide, lf_knee_guide)


   #if cmds.objExists('*hips_guide'):
   #
   #    hips_guide = cmds.ls('*hips_guide',type='transform')[0]
   #
   #    cmds.parent(left_leg_guide_group,hips_guide)


    return left_leg_guides_list,foot_guides_list



def mirror_leg_guides():

    rigging_functions.mirror_guides()












