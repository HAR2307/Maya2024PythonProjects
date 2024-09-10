import maya.cmds as cmds

"""
copiar lo de abajo na mas pa usar el codigo

import importlib
from utils import unparent_by_selection_order

importlib.reload(unparent_by_selection_order)

selectionList = cmds.ls(selection=True)

unparent_by_selection_order.unparent_by_selection_list(selectionList)

"""

def unparent_by_selection_list(selection_list):

    """unparent by selection order, the parameter is a list"""

    relatives_List = cmds.listRelatives(selection_list,children=True,type='transform')

    for children in relatives_List:

        print(children)

        cmds.parent(children,world=True)