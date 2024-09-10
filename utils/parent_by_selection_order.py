import maya.cmds as cmds

"""
copiar lo de abajo na mas pa usar el codigo

import importlib
from utils import parent_by_selection_order

importlib.reload(parent_by_selection_order)

selectionList = cmds.ls(selection=True)

parent_by_selection_order.parent_by_selection_list(selectionList)

"""

def parent_by_selection_list(selection_list):

    """parent by section order, the parameter is a list"""

    for eachObject in range(1, len(selection_list)):
        child = selection_list[eachObject]
        parent = selection_list[eachObject - 1]

        cmds.parent(child, parent)