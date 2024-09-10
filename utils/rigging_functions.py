import maya.cmds as cmds
import re
import importlib

from utils import controller_curves
from utils import parent_by_selection_order


importlib.reload(controller_curves)
importlib.reload(parent_by_selection_order)


def set_colors(controller_shape,controller_color):
    shape = controller_shape + 'Shape'
    cmds.setAttr(controller_shape+'.overrideEnabled',1)
    cmds.setAttr(controller_shape+'.overrideColor',controller_color)

def set_scales(input_object,value):
    cmds.setAttr(input_object+ '.sx',value)
    cmds.setAttr(input_object + '.sy', value)
    cmds.setAttr(input_object + '.sz', value)

def set_rotations(input_object,value):
    cmds.setAttr(input_object + '.rx',value)
    cmds.setAttr(input_object + '.ry', value)
    cmds.setAttr(input_object + '.rz', value)

def set_translations(input_object,value):
    cmds.setAttr(input_object + '.tx',value)
    cmds.setAttr(input_object + '.ty', value)
    cmds.setAttr(input_object + '.tz', value)

def lock_translations(input_object):
    cmds.setAttr(input_object + '.tx',lock=True)
    cmds.setAttr(input_object + '.ty', lock=True)
    cmds.setAttr(input_object + '.tz', lock=True)

def lock_rotations(input_object):
    cmds.setAttr(input_object + '.rx',lock=True)
    cmds.setAttr(input_object + '.ry', lock=True)
    cmds.setAttr(input_object + '.rz', lock=True)

def lock_scales(input_object):
    cmds.setAttr(input_object + '.sx',lock=True)
    cmds.setAttr(input_object + '.sy', lock=True)
    cmds.setAttr(input_object + '.sz', lock=True)

def toggle_visibility(input_object):
    visibility_state =  cmds.getAttr(input_object + '.v')
    if visibility_state == 0:
        cmds.setAttr(input_object+'.v',1)
    else:
        cmds.setAttr(input_object + '.v', 0)

def template_mode(input_object):
    template_state=cmds.getAttr(input_object+'.template')
    if template_state == 0:
        cmds.setAttr(input_object+'.template',1)
    else:
        cmds.setAttr(input_object + '.template', 0)

def label_joints(input_joint,label_name,rig_side):
    cmds.setAttr(input_joint+'.side',rig_side)
    cmds.setAttr(input_joint + '.type', 18)
    cmds.setAttr(input_joint + '.otherType',label_name,type='string')

def freeze(target_object):
    cmds.makeIdentity(target_object,apply=True, t = True, r = True, s = True, n = False)

def add_rotation_order_for_ctrls(object):
    cmds.addAttr(object, longName='Extra', at='enum', en=('____'), k=True)
    cmds.setAttr(object + '.Extra', lock=True)
    cmds.addAttr(object, longName='RotationOrder', at='enum', en=('xyz:yzx:zxy:xzy:yxz:zyx'), k=True)
    cmds.connectAttr(object + '.RotationOrder', object + '.rotateOrder')


def get_top_parent_of_selected(nodeType):
    """
    Parameter is string
    Returns the top parent node of the currently selected object in Maya.
    If no object is selected or if the selection is empty, returns None.
    """
    # Get the currently selected objects
    selected_objects = cmds.ls(selection=True)

    if not selected_objects:
        print("No object is selected.")
        return None

    # Take the first selected object
    selected_object = selected_objects[0]

    # Initialize with the selected object
    current_node = selected_object

    # Traverse up the hierarchy to find the top parent
    while True:
        parent = cmds.listRelatives(current_node, parent=True ,type=nodeType)
        if parent:
            current_node = parent[0]
        else:
            # We've reached the top parent
            break

    return current_node

def mirror_guides():

    mirrored_guides_list = []

    top_guide_group = get_top_parent_of_selected('transform')

    guide_hierarchy = cmds.listRelatives(top_guide_group,allDescendents=True,type='transform')

    print(guide_hierarchy)

    for eachGuide in guide_hierarchy:

        mirrored_guide = controller_curves.create_curve('cross',controller_name=eachGuide.replace('lf','rt'))
        cmds.matchTransform(mirrored_guide,eachGuide)
        mirrored_guides_list.append(mirrored_guide)

    print(mirrored_guides_list)

    reverse_order_list = sorted(mirrored_guides_list)

    parent_by_selection_order.parent_by_selection_list(reverse_order_list)

    guide_hierarchy_parent = reverse_order_list[0]

    mirrored_guides_parent_group = cmds.group(em=True, name = top_guide_group.replace('lf','rt'))

    cmds.matchTransform(mirrored_guides_parent_group,top_guide_group)

    print(guide_hierarchy_parent)

    cmds.parent(guide_hierarchy_parent,mirrored_guides_parent_group)

    temporary_mirror_group=cmds.group(em=True,name='temporary_mirror_grp')

    cmds.parent(mirrored_guides_parent_group,temporary_mirror_group)

    cmds.setAttr(temporary_mirror_group + '.sx', -1)

    cmds.parent(mirrored_guides_parent_group,world=True)

    cmds.delete(temporary_mirror_group)



def replace_substring_in_names(old_substring, new_substring,object_list):
    """
    Replaces the old_substring with the new_substring in the names of all selected objects in Maya.

    Args:
    old_substring (str): The substring to be replaced.
    new_substring (str): The new substring to replace the old one.
    """


    if not object_list:
        print("No objects selected.")
        return

    for obj in object_list:
        # Check if the object name contains the old substring
        if old_substring in obj:
            # Create the new name by replacing the substring
            new_name = obj.replace(old_substring, new_substring)
            try:
                # Rename the object
                cmds.rename(obj, new_name)
                print(f"Renamed '{obj}' to '{new_name}'")
            except Exception as e:
                print(f"Failed to rename '{obj}': {e}")






