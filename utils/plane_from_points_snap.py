import maya.cmds as cmds

from utils import parent_by_selection_order
from utils import unparent_by_selection_order
from utils import rigging_functions
from utils import rigging_functions_02
from utils import controller_curves
from utils import ribbon_setup
from auto_rigger import ik_fk_chain_rig_setup
from utils import create_master_controller

import importlib
importlib.reload(rigging_functions)
importlib.reload(rigging_functions_02)
importlib.reload(parent_by_selection_order)
importlib.reload(unparent_by_selection_order)
importlib.reload(controller_curves)
importlib.reload(ik_fk_chain_rig_setup)
importlib.reload(ribbon_setup)
importlib.reload(create_master_controller)

"""
copiar lo de abajo na mas pa usar el codigo

import maya.cmds as cmds

import importlib

from utils import plane_from_points_snap

importlib.reload(plane_from_points_snap)

object_list = cmds.ls(selection=True)
surface_name = 'test_plane'

plane_from_points_snap.create_plane(object_list,surface_name)
"""

def create_plane(object_list,surface_name):

    point_list = []

    first_object_in_list = object_list[0]

    for eachObject in object_list:
        print(eachObject)
        coordinates  = cmds.xform(eachObject,query=True, translation=True, worldSpace=True)
        point_list.append(coordinates)
        print(coordinates)

    points = point_list

    first_curve = 'curve_01'

    cmds.curve(ep=points, d=3,name = first_curve)

    second_curve = 'curve_02'

    cmds.curve(ep=points, d=3, name=second_curve)

    width = (cmds.arclen(first_curve))/8

    first_curve_group = 'curve_01_grp'
    cmds.group(empty=True,name=first_curve_group)
    second_curve_group = 'curve_02_grp'
    cmds.group(empty=True, name=second_curve_group)

    cmds.matchTransform(first_curve_group,first_object_in_list)
    cmds.matchTransform(second_curve_group, first_object_in_list)

    cmds.parent(first_curve,first_curve_group)
    cmds.parent(second_curve, second_curve_group)

    cmds.move( width, 0, 0, first_curve_group,relative=True,objectSpace=True)
    cmds.move(-width, 0, 0, second_curve_group, relative=True, objectSpace=True)

    surface = cmds.loft(first_curve,second_curve,name = surface_name,constructionHistory=False,reverseSurfaceNormals = True)

    cmds.delete(first_curve_group)
    cmds.delete(second_curve_group)

    return surface_name



