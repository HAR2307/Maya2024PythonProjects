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

from auto_rigger import chain_guides

importlib.reload(chain_guides)

guide_name = ''
side=''
letter=''
number_of_guides = 10

spine_guides.create_chain_guides(guide_name, side, letter, number_of_guides)


"""

def create_chain_guides(guide_name, side, letter, number_of_guides):


    counter = 0
    z_coordinate = 0
    end_range =  number_of_guides+1

    guide_list = []

    for i in range(0,end_range):

        if counter == end_range-1:

            guide = controller_curves.create_curve('cross',
                                                   controller_name=side + '_' + str(counter) + '_' +
                                                                   letter + '_' + guide_name + '_end_guide')
        else:
            guide = controller_curves.create_curve('cross',
                                                   controller_name=side + '_' + str(counter) + '_' +
                                                                   letter + '_' + guide_name + '_guide')

        cmds.setAttr(guide + '.tz', z_coordinate)
        guide_list.append(guide)

        counter +=1
        z_coordinate += 1

    parent_by_selection_order.parent_by_selection_list(guide_list)
    cmds.select(clear=True)


    return guide_list