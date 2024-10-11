import maya.cmds as cmds

from utils import parent_by_selection_order
from utils import unparent_by_selection_order
from utils import rigging_functions
from utils import controller_curves


from auto_rigger import spine_guides
from auto_rigger import head_guides
from auto_rigger import leg_guides
from auto_rigger import arm_guides
from auto_rigger import hand_guides

import importlib

importlib.reload(rigging_functions)
importlib.reload(parent_by_selection_order)
importlib.reload(unparent_by_selection_order)
importlib.reload(controller_curves)

importlib.reload(spine_guides)
importlib.reload(head_guides)
importlib.reload(leg_guides)
importlib.reload(arm_guides)
importlib.reload(hand_guides)

"""
copiar lo de abajo na mas pa usar el codigo

import maya.cmds as cmds

import importlib

from auto_rigger import biped_guides
from utils import rigging_functions

importlib.reload(biped_guides)
importlib.reload(rigging_functions)

letter = ''

asset_name = 'myAsset'

finger_count = 4

biped_guides.biped_spine_guides(letter)
biped_guides.biped_head_guides(letter)
biped_guides.biped_arm_guides(letter)
biped_guides.biped_leg_guides(letter)
biped_guides.biped_hand_guides(letter,finger_count)

rigging_functions.mirror_guides()

#After mirroring the desired guides run:

biped_guides.biped_hierarchy(asset_name)


"""

def biped_hierarchy(asset_name):

    master_guide_grp = cmds.group(em=True, name = asset_name + '_' + 'mainGuides_grp')

    guides_groups_list = cmds.ls('*guide_grp',type='transform')
    
    cmds.parent(guides_groups_list,master_guide_grp)



def biped_spine_guides(letter):

    side = 'cn'
    spine = spine_guides.create_spine_guides(side, letter)





def biped_head_guides(letter):

    side = 'cn'
    head = head_guides.create_head_guides(side,letter)



def  biped_arm_guides(letter):

    side = 'lf'
    arm = arm_guides.create_left_arm_guides(side,letter)




def biped_leg_guides(letter):

    side = 'lf'

    leg = leg_guides.create_left_leg_guides(side, letter)

def biped_hand_guides(letter,finger_count):

    side = 'lf'

    hand = hand_guides.create_left_hand_guides(side,letter,finger_count)







