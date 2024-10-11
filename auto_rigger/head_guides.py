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

from auto_rigger import head_guides

importlib.reload(head_guides)

head_guides.create_head_guides()

"""

def create_head_guides(side,letter):

    chest_guide = ''

    neck_guide = controller_curves.create_curve('cross',controller_name=side + '_' + '0' + '_'+ letter + '_' + 'neck_guide')
    head_guide = controller_curves.create_curve('cross',controller_name=side + '_' + '1' + '_'+ letter + '_' + 'head_guide')
    head_end_guide = controller_curves.create_curve('cross',controller_name=side + '_' + '2' + '_'+ letter + '_' + 'headEnd_guide')

    head_guide_list = [head_guide,neck_guide,head_end_guide]

    for eachGuide in head_guide_list:
        rigging_functions.set_colors(eachGuide,22)

    cmds.select(clear=True)

    cmds.setAttr(neck_guide + '.ty', 20)

    cmds.setAttr(head_guide + '.ty', 25)

    cmds.setAttr(head_end_guide + '.ty', 30)

    jaw_guide = controller_curves.create_curve('cross',controller_name=side + '_' + '0' + '_'+ letter + '_' + 'jaw_guide')
    jaw_end_guide = controller_curves.create_curve('cross',controller_name=side + '_' + '1' + '_'+ letter + '_' + 'jawEnd_guide')

    cmds.setAttr(jaw_guide + '.ty', 27.5)

    cmds.setAttr(jaw_end_guide + '.ty', 27.5)
    cmds.setAttr(jaw_end_guide + '.tz', 5)

    cmds.parent(head_guide, neck_guide)
    cmds.parent(jaw_end_guide,jaw_guide)
    cmds.parent(jaw_guide,head_guide)
    cmds.parent(head_end_guide, head_guide)

    head_guide_group = cmds.group(em=True, name=side + '_' + letter + '_' + 'head_guide_grp')

    cmds.matchTransform(head_guide_group, neck_guide)

    cmds.parent(neck_guide, head_guide_group)






