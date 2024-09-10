import maya.cmds as cmds
import importlib
from utils import parent_by_selection_order
from utils import unparent_by_selection_order
importlib.reload(parent_by_selection_order)
importlib.reload(unparent_by_selection_order)


def mirror_guides():
    all_left_guides = cmds.ls("*lf_guide")  ##lista de locators izquierdos
    print(all_left_guides)
    left_Locators = cmds.listRelatives(all_left_guides, p=True, f=True,type='transform')



    all_right_guides = cmds.ls("*rt_guide")  ##lista de locators izquierdos
    print(all_right_guides)
    right_Locators = cmds.listRelatives(all_right_guides, p=True, f=True)

    for i, l in enumerate(left_Locators):  # for loop that checks the left locators position and mirrors that translation to the right locators
        pos = cmds.xform(l, q=True, t=True, ws=True)
        cmds.move(-pos[0], pos[1], pos[2], right_Locators[i])
        print(i)






