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

from auto_rigger import spine_guides

importlib.reload(spine_guides)

spine_guides.create_spine_guides()


"""

def create_spine_guides(side,letter):

    cog_guide = controller_curves.create_curve('cross',controller_name=side + '_' + '0' + '_'+ letter + '_' + 'cog_guide')
    hips_guide = controller_curves.create_curve('cross',controller_name=side + '_' + '1' + '_'+ letter + '_' + 'hips_guide')
    chest_guide = controller_curves.create_curve('cross',controller_name=side + '_' + '2' + '_'+ letter + '_' + 'chest_guide')

    spine_guide_list = [hips_guide,cog_guide,chest_guide]

    for eachGuide in spine_guide_list:
        rigging_functions.set_colors(eachGuide,22)

    cmds.select(clear=True)

    cmds.setAttr(cog_guide + '.ty', 5)
    cmds.setAttr(hips_guide + '.ty', 10)
    cmds.setAttr(chest_guide + '.ty', 15)

    cmds.parent(cog_guide,hips_guide)
    cmds.parent(chest_guide, hips_guide)

    spine_guide_group = cmds.group(em=True, name=side + '_' + letter + '_' + 'spine_guide_grp')

    cmds.matchTransform(spine_guide_group, hips_guide)
    cmds.parent(hips_guide, spine_guide_group)

    #main_guide_group = cmds.group(em=True, name='Guides_grp')

    #cmds.parent(spine_guide_group, main_guide_group)








