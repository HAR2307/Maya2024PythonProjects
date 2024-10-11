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
from auto_rigger import hand_guides

importlib.reload(hand_guides)

side = 'lf'

letter = ''

finger_count = 4

hand_guides.create_left_hand_guides(side,letter,finger_count)


"""
def create_left_hand_guides(side,letter,finger_count):

    fingers_list = ['thumb','index','middle','ring','pinky']

    thumb_guide_list = []

    index_guide_list = []

    middle_guide_list = []

    ring_guide_list = []

    pinky_guide_list = []

    lf_hand_guide = controller_curves.create_curve('circle',controller_name=side + '_' + '0' + '_'+ letter + '_' + 'hand_guide')


    cmds.setAttr(lf_hand_guide + '.rz', -90)

    rigging_functions.freeze(lf_hand_guide)

    rigging_functions.set_colors(lf_hand_guide,6)

    for eachFinger in fingers_list:

        finger_guide = create_finger(side,eachFinger,letter)

        if 'thumb' in eachFinger:
            thumb_guide_list = finger_guide

        if 'index' in eachFinger:
            index_guide_list = finger_guide

        if 'middle' in eachFinger:
            middle_guide_list = finger_guide

        if 'ring' in eachFinger:
            ring_guide_list = finger_guide

        if 'pinky' in eachFinger:
            pinky_guide_list = finger_guide


    cmds.setAttr(thumb_guide_list[0] + '.ty', -1)
    cmds.setAttr(thumb_guide_list[0] + '.tz', 1.5)

    cmds.setAttr(index_guide_list[0] + '.tz', 0.75)

    cmds.setAttr(middle_guide_list[0] + '.tz', 0)

    cmds.setAttr(ring_guide_list[0] + '.tz', -1)

    cmds.setAttr(pinky_guide_list[0] + '.tz', -1.5)

    all_fingers_guide_list = [thumb_guide_list,index_guide_list,middle_guide_list,ring_guide_list,pinky_guide_list]

    for eachFingerGuide in all_fingers_guide_list:

        cmds.parent(eachFingerGuide[0],lf_hand_guide)

    cmds.setAttr(lf_hand_guide + '.ty', 15)
    cmds.setAttr(lf_hand_guide + '.tx', 8)

    left_hand_guide_group = cmds.group(em=True, name=side + '_' + letter + '_' + 'hand_guide_grp')

    cmds.matchTransform(left_hand_guide_group, lf_hand_guide)
    cmds.parent(lf_hand_guide, left_hand_guide_group)

    if finger_count == 3:
        cmds.delete(pinky_guide_list)
    if finger_count == 2:
        cmds.delete(pinky_guide_list)
        cmds.delete(ring_guide_list)
    if finger_count == 1:
        cmds.delete(pinky_guide_list)
        cmds.delete(ring_guide_list)
        cmds.delete(middle_guide_list)

    if finger_count > 4 and finger_count < 1:

        print('type a value between 4 and 1')





def create_finger(side,finger_name,letter):

    finger_list = []

    phalanges = 0

    x_coordinate = 0

    for eachGuide in range(0, 4):
        finger_guide = controller_curves.create_curve('cross', controller_name=side + '_' + str(
            phalanges) + '_' + letter + '_' + finger_name + '_guide')

        phalanges += 1

        x_coordinate += 1

        cmds.setAttr(finger_guide + '.tx', x_coordinate)

        rigging_functions.set_scales(finger_guide, .2)

        finger_list.append(finger_guide)

    parent_by_selection_order.parent_by_selection_list(finger_list)

    for eachGuide in finger_list:
        rigging_functions.set_colors(eachGuide, 6)



    return finger_list
























