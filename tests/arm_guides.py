import maya.cmds as cmds
from utils import parent_by_selection_order
from utils import unparent_by_selection_order
from tests import mirror_guides
import importlib
importlib.reload(mirror_guides)
importlib.reload(parent_by_selection_order)
importlib.reload(unparent_by_selection_order)

"""
copiar lo de abajo na mas pa usar el codigo

import maya.cmds as cmds

import importlib
from auto_rigger import arm_guides

importlib.reload(arm_guides)

arm_guides.create_left_arm_guides()
arm_guides.create_right_arm_guides()
arm_guides.mirror_arm_guides()

"""


def create_left_arm_guides():
    shoulder_lf_locator = cmds.spaceLocator(n='shoulder_lf_guide')
    upper_arm_lf_locator = cmds.spaceLocator(n='upperArm_lf_guide')
    elbow_lf_locator = cmds.spaceLocator(n='elbow_lf_guide')
    wrist_lf_locator = cmds.spaceLocator(n='wrist_lf_guide')
    arm_end_lf_locator = cmds.spaceLocator(n='armEnd_lf_guide')

    cmds.move(1, 0, 0, shoulder_lf_locator)
    cmds.move(2, 0, 0, upper_arm_lf_locator)
    cmds.move(4, 0, 0, elbow_lf_locator)
    cmds.move(6, 0, 0, wrist_lf_locator)
    cmds.move(8, 0, 0, arm_end_lf_locator)

    left_arm_locators = [shoulder_lf_locator,upper_arm_lf_locator,elbow_lf_locator,wrist_lf_locator,arm_end_lf_locator]

    print(left_arm_locators)

    parent_by_selection_order.parent_by_selection_list(left_arm_locators)

    return left_arm_locators



def create_right_arm_guides():
    shoulder_rt_locator = cmds.spaceLocator(n='shoulder_rt_guide')
    upper_arm_rt_locator = cmds.spaceLocator(n='upperArm_rt_guide')
    elbow_rt_locator = cmds.spaceLocator(n='elbow_rt_guide')
    wrist_rt_locator = cmds.spaceLocator(n='wrist_rt_guide')
    arm_end_rt_locator = cmds.spaceLocator(n='armEnd_rt_guide')

    cmds.select(clear=True)

    cmds.move(-1, 0, 0, shoulder_rt_locator)
    cmds.move(-2, 0, 0, upper_arm_rt_locator)
    cmds.move(-4, 0, 0, elbow_rt_locator)
    cmds.move(-6, 0, 0, wrist_rt_locator)
    cmds.move(-8, 0, 0, arm_end_rt_locator)

   #cmds.rotate(-180, 0, 0, shoulder_rt_locator)
   #cmds.rotate(-180, 0, 0, upper_arm_rt_locator)
   #cmds.rotate(-180, 0, 0, elbow_rt_locator)
   #cmds.rotate(-180, 0, 0, wrist_rt_locator)
   #cmds.rotate(-180, 0, 0, arm_end_rt_locator)
   #
    right_arm_locators = [shoulder_rt_locator, upper_arm_rt_locator, elbow_rt_locator, wrist_rt_locator,
                         arm_end_rt_locator]

    print(right_arm_locators)

    parent_by_selection_order.parent_by_selection_list(right_arm_locators)

    return right_arm_locators

def mirror_arm_guides():

    mirror_guides.mirror_guides()







   #for armLocators, armTransformNodes in enumerate(
   #        left_arm_locators_transform_nodes):  ###i es la izquierda, l es la derecha, estamos usando un arreglo bidimensional para esto
   #    pos = cmds.xform(armTransformNodes, q=True, t=True, ws=True)
   #    cmds.move(-pos[0], pos[1], pos[2], right_arm_locators_transform_nodes[armLocators])