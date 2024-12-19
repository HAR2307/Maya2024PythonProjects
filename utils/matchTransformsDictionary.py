import maya.cmds as cmds

"""
copiar lo de abajo na mas pa usar el codigo

import maya.cmds as cmds

import importlib
from utils import matchTransformsDictionary

importlib.reload(matchTransformsDictionary)

list1 = '' 

list2 = ''

matchTransformsDictionary.match_transforms_from_two_lists(list1,list2)



"""

def match_transforms_from_two_lists(first_list, second_list):

    #first_list = cmds.listRelatives(list_1,allDescendents=True,type='transform')

    print(first_list)

    #second_list = cmds.listRelatives(list_2, allDescendents=True, type='transform')

    print(second_list)

    setup_dict = {first_list[i]: second_list[i] for i in range(len(first_list))}

    for objectFromList1, objectFromList2 in setup_dict.items():

        cmds.matchTransform(objectFromList2,objectFromList1)