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
def create_hierarchy(asset_name):

    num_items = [0,1,2]

    master_hierarchy_list = []

    master_TR_ctrl_name = asset_name + '_master_TR_' + 'ctrl'

    controller_curves.create_curve(shape_name='triangle', controller_name=master_TR_ctrl_name)

    rigging_functions.set_scales(master_TR_ctrl_name, 2)

    rigging_functions.freeze(master_TR_ctrl_name)

    scale_lists = ['.sx','.sy','.sz']

    for eachScale in scale_lists:

        rigging_functions.lock_and_hide_attributes(master_TR_ctrl_name,eachScale)

    master_TRS_ctrl_name = asset_name + '_master_TRS_' + 'ctrl'

    controller_curves.create_curve(shape_name='triangle', controller_name=master_TRS_ctrl_name)

    rigging_functions.set_scales(master_TRS_ctrl_name, 4)

    rigging_functions.freeze(master_TRS_ctrl_name)

    cmds.parent(master_TR_ctrl_name,master_TRS_ctrl_name)

    cmds.addAttr(master_TRS_ctrl_name, longName='skin_joints_visibility', at='bool', dv=0, k=True)

    skin_joint_group_name = asset_name + '_skinJoints_grp'
    skin_joint_group =  cmds.group(name= skin_joint_group_name, empty=True)

    cmds.parent(skin_joint_group_name,master_TR_ctrl_name)

    rigging_functions.set_colors(master_TR_ctrl_name,22)
    rigging_functions.set_colors(master_TRS_ctrl_name, 17)

    cmds.setAttr(skin_joint_group_name + '.inheritsTransform', 0)

    cmds.connectAttr(master_TRS_ctrl_name + '.skin_joints_visibility', skin_joint_group_name + '.visibility')

    if cmds.objExists('*mainGeometry_grp'):
        geo_group = cmds.ls('*mainGeometry_grp')
        cmds.parent(geo_group,master_TR_ctrl_name)
        cmds.setAttr(geo_group + '.inheritsTransform', 0)


    return [master_TRS_ctrl_name,master_TR_ctrl_name,skin_joint_group_name]






