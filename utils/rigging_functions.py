import maya.cmds as cmds
import re
import importlib

from utils import controller_curves
from utils import parent_by_selection_order
from math import pow,sqrt


importlib.reload(controller_curves)
importlib.reload(parent_by_selection_order)

def set_scales(input_object,value):
    cmds.setAttr(input_object+ '.sx',value)
    cmds.setAttr(input_object + '.sy', value)
    cmds.setAttr(input_object + '.sz', value)


def set_colors(controller_shape,controller_color):
    shape = controller_shape + 'Shape'
    cmds.setAttr(controller_shape+'.overrideEnabled',1)
    cmds.setAttr(controller_shape+'.overrideColor',controller_color)

def get_scales(input_object,value):
    cmds.getAttr(input_object+ '.scaleX',value)
    cmds.getAttr(input_object + '.scaleY', value)
    cmds.getAttr(input_object + '.scaleZ', value)

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


def lock_and_hide_attributes(input_object,attribute_name):

    """attribute name must be str"""

    cmds.setAttr(input_object + attribute_name,lock=True,keyable=False,channelBox=False)
    cmds.setAttr(input_object + attribute_name, lock=True,keyable=False,channelBox=False)
    cmds.setAttr(input_object + attribute_name, lock=True,keyable=False,channelBox=False)

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

def create_controller(joint, controller_size,controller_color, controller_shape, prefix, constraint_type,
                      maintain_offset):

    """
    joint = str
    controller_size = float
    controller_color = int
    controller_shape = str
    prefix = str
    constraint_type = str
    maintain_offset = boolean


    """

    controller_name = joint.replace('_jnt', prefix)

    controller_shape = controller_curves.create_curve(shape_name=controller_shape,
                                                      controller_name=controller_name)

    set_scales(controller_shape,controller_size)

    freeze(controller_shape)

    cmds.matchTransform(controller_shape, joint)

    add_rotation_order_for_ctrls(controller_shape)

    set_colors(controller_shape, controller_color)

    ctrl_group_name = controller_shape + '_grp'

    ctrl_group_name = cmds.group(name=ctrl_group_name, empty=True)

    cmds.matchTransform(ctrl_group_name, controller_shape)

    cmds.parent(controller_shape, ctrl_group_name)

    if constraint_type == 'parent':

        constraint_name = joint.replace('_jnt','_parentConstraint')

        cmds.parentConstraint(controller_shape, joint, maintainOffset=maintain_offset, name = constraint_name)

    if constraint_type == 'point':

        constraint_name = joint.replace('_jnt','_pointConstraint')


        cmds.pointConstraint(controller_shape, joint, maintainOffset=maintain_offset, name =constraint_name)

    if constraint_type == 'orient':

        constraint_name = joint.replace('_jnt','_orientConstraint')


        cmds.orientConstraint(controller_shape, joint, maintainOffset=maintain_offset, name=constraint_name)

    if constraint_type == 'aim':

        constraint_name = joint.replace('_jnt','_aimConstraint')


        cmds.aimConstraint(controller_shape, joint, maintainOffset=maintain_offset, name=constraint_name)

    if constraint_type == 'none':

        cmds.matchTransform(ctrl_group_name, joint)

    return [controller_name,ctrl_group_name]







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


    def mirror_guides_process(side_1,side_2,top_guide_group):

        mirrored_guides_list = []

        foot_guide_list = []

        ankle_guide = ''

        mirrored_hand_group = ''

        mirrored_hand_list = []

        mirrored_thumb_list = []
        mirrored_index_list = []
        mirrored_middle_list = []
        mirrored_ring_list = []
        mirrored_pinky_list = []

        guide_hierarchy = cmds.listRelatives(top_guide_group,allDescendents=True,type='transform')

        print(guide_hierarchy)

        for eachGuide in guide_hierarchy:

            if 'constraint' not in eachGuide:

                if 'hand' in eachGuide:
                    mirrored_guide = controller_curves.create_curve('circle',
                                                                    controller_name=eachGuide.replace(side_1, side_2))
                    cmds.setAttr(mirrored_guide + '.rz', -90)
                    freeze(mirrored_guide)
                else:

                    mirrored_guide = controller_curves.create_curve('cross',controller_name=eachGuide.replace(side_1,side_2))




                cmds.matchTransform(mirrored_guide,eachGuide)
                mirrored_guides_list.append(mirrored_guide)

        print(mirrored_guides_list)

        reverse_order_list = sorted(mirrored_guides_list)

        parent_by_selection_order.parent_by_selection_list(reverse_order_list)

        guide_hierarchy_parent = reverse_order_list[0]

        mirrored_guides_parent_group = cmds.group(em=True, name = top_guide_group.replace(side_1,side_2))

        cmds.matchTransform(mirrored_guides_parent_group,top_guide_group)

        print(guide_hierarchy_parent)

        cmds.parent(guide_hierarchy_parent,mirrored_guides_parent_group)

        temporary_mirror_group=cmds.group(em=True,name='temporary_mirror_grp')

        cmds.parent(mirrored_guides_parent_group,temporary_mirror_group)

        cmds.setAttr(temporary_mirror_group + '.sx', -1)

        cmds.parent(mirrored_guides_parent_group,world=True)

        cmds.delete(temporary_mirror_group)

        if side_1 == 'lf':
            for eachGuide in reverse_order_list:
                set_colors(eachGuide, 13)
        if side_1 == 'rt':
            for eachGuide in reverse_order_list:
                set_colors(eachGuide, 6)

        for eachMirroredGuide in reverse_order_list:
            if 'ankle_guide' in eachMirroredGuide:
                ankle_guide = eachMirroredGuide
            if 'Foot' in eachMirroredGuide:
                foot_guide_list.append(eachMirroredGuide)

        for eachFootGuide in foot_guide_list:
            cmds.parent(eachFootGuide,world=True)

        for eachFootGuide in foot_guide_list:
            cmds.parent(eachFootGuide,ankle_guide)

        if 'hand' in mirrored_guides_parent_group:

            mirrored_hand_group = mirrored_guides_parent_group

            mirrored_hand_guide = ''

            mirrored_hand_list = cmds.listRelatives(mirrored_guides_parent_group,allDescendents=True,type = 'transform')

            for eachGuide in mirrored_hand_list:

                if 'hand' in eachGuide:
                    mirrored_hand_guide = eachGuide

            for eachGuide in mirrored_hand_list:

                if 'thumb' in eachGuide:
                    mirrored_thumb_list.append(eachGuide)
                if 'index' in eachGuide:
                    mirrored_index_list.append(eachGuide)
                if 'middle' in eachGuide:
                    mirrored_middle_list.append(eachGuide)
                if 'ring' in eachGuide:
                    mirrored_ring_list.append(eachGuide)
                if 'pinky' in eachGuide:
                    mirrored_pinky_list.append(eachGuide)

            for eachGuide in mirrored_hand_list:
                cmds.parent(eachGuide, world=True)


            reversed_thumb_list = sorted(mirrored_thumb_list)
            reversed_index_list = sorted(mirrored_index_list)
            reversed_middle_list = sorted(mirrored_middle_list)
            reversed_ring_list = sorted(mirrored_ring_list)
            reversed_pinky_list = sorted(mirrored_pinky_list)

            parent_by_selection_order.parent_by_selection_list(reversed_thumb_list)
            parent_by_selection_order.parent_by_selection_list(reversed_index_list)
            parent_by_selection_order.parent_by_selection_list(reversed_middle_list)
            parent_by_selection_order.parent_by_selection_list(reversed_ring_list)
            parent_by_selection_order.parent_by_selection_list(reversed_pinky_list)

            all_mirrored_fingers_guide_list = [reversed_thumb_list, reversed_index_list, reversed_middle_list, reversed_ring_list,
                                      reversed_pinky_list]

            for eachFingerGuide in all_mirrored_fingers_guide_list:
                cmds.parent(eachFingerGuide[0], mirrored_hand_guide)

            cmds.parent(mirrored_hand_guide, mirrored_hand_group)



            print('here are the mirrored hand guides:')
            print(mirrored_hand_list)

            print('here are the mirrored thumb guides:')
            print(mirrored_thumb_list)




    top_guide_group = get_top_parent_of_selected('transform')

    side_1 = ''
    side_2 = ''
    opposite_group = ''

    if 'grp' in top_guide_group:

        if 'lf' in top_guide_group:

            side_1= 'lf'
            side_2 = 'rt'
            opposite_group = top_guide_group.replace('lf','rt')

            if cmds.objExists(opposite_group):

                cmds.delete(opposite_group)

                mirrored_guides = mirror_guides_process(side_1, side_2,top_guide_group)

            else:
                mirrored_guides = mirror_guides_process(side_1, side_2,top_guide_group)



        if 'rt' in top_guide_group:

            side_1 = 'rt'
            side_2 = 'lf'

            opposite_group = top_guide_group.replace('rt', 'lf')

            if cmds.objExists(opposite_group):
                cmds.delete(opposite_group)

                mirrored_guides = mirror_guides_process(side_1, side_2,top_guide_group)
            else:
                mirrored_guides = mirror_guides_process(side_1, side_2,top_guide_group)

    else:
        print('no guide group found')








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

def spline_ik_setup(joint_list, spline_spans, spline_handle_name, controller_color, controller_shape,
                    controller_size,
                    world_up_type, forward_axis, world_up_axis,
                    world_up_vector_x, world_up_vector_y, world_up_vector_z,
                    world_up_vector_end_x, world_up_vector_end_y, world_up_vector_end_z,
                    spline_axis):

    """ setup for a ik spline module

    joint_list = list
    spline_spans = int
    spline_handle_name =str
    controller_color = int
    controller_shape = str
    world_up_type,forward_axis,world_up_axis = int
    world_up_vector_x,world_up_vector_y,world_up_vector_z = int
    world_up_vector_end_x,world_up_vector_end_y,world_up_vector_end_z = int
    spline axis =  str X,Y,Z

    Returns the name of the ik curve name

    """

    joint_list_len = len(joint_list)

    print(joint_list_len)

    middle_index = int(len(joint_list) / 2)  # = int(2.5) = 2

    start_joint = joint_list[0]
    mid_joint = joint_list[middle_index]
    end_joint = joint_list[joint_list_len-1]

    ik_spline_curve = ''
    ik_spline_effector = ''
    ik_ctrl_list = []

    curve_point_list = []

    start_joint_name = start_joint.replace('_jnt', '_start_jnt')

    start_bind_joint = cmds.joint(n=start_joint_name, radius=3)

    cmds.matchTransform(start_bind_joint, start_joint)
    cmds.select(clear=True)
    cmds.setAttr(start_bind_joint+'.visibility',0)

    mid_joint_name = mid_joint.replace('_jnt', '_mid_jnt')

    mid_bind_joint = cmds.joint(n=mid_joint_name, radius=3)

    cmds.matchTransform(mid_bind_joint, mid_joint)
    cmds.select(clear=True)
    cmds.setAttr(mid_bind_joint + '.visibility', 0)

    end_joint_name = end_joint.replace('_jnt', '_end_jnt')

    end_bind_joint = cmds.joint(n=end_joint_name, radius=3)

    cmds.matchTransform(end_bind_joint, end_joint)
    cmds.select(clear=True)
    cmds.setAttr(end_bind_joint + '.visibility', 0)

    start_joint_ctrl = create_controller(start_bind_joint, controller_size, controller_color, controller_shape,
                                         '_ik_ctrl',
                                         'parent', True)

    mid_joint_ctrl = create_controller(mid_bind_joint, controller_size, controller_color, controller_shape, '_ik_ctrl',
                                       'parent', True)

    end_joint_ctrl = create_controller(end_bind_joint, controller_size, controller_color, controller_shape, '_ik_ctrl',
                                       'parent', True)

    start_joint_ctrl_grp = start_joint_ctrl[1]

    mid_joint_ctrl_grp = mid_joint_ctrl[1]

    end_joint_ctrl_grp = end_joint_ctrl[1]

    start_joint_ctrl_name = start_joint_ctrl[0]

    mid_joint_ctrl_name = mid_joint_ctrl[0]

    end_joint_ctrl_name = end_joint_ctrl[0]


    spline_setup_ik_group = start_joint.replace('_jnt', '_setupSplineIK_grp')

    spline_setup_ik_group = cmds.group(empty=True, name=spline_setup_ik_group)

    cmds.matchTransform(spline_setup_ik_group, start_bind_joint)

    spline_ik_handle = cmds.ikHandle(solver='ikSplineSolver', startJoint=start_joint,
                                           endEffector=end_joint,
                  numSpans=spline_spans,
                  name=spline_handle_name)[0]

    if cmds.objExists('curve1'):

       #for eachJoint in joint_list:
       #
       #    coordinates = cmds.xform(eachJoint, query=True, translation=True, worldSpace=True)
       #    curve_point_list.append(coordinates)
       #
       #cmds.curve('curve1', r=True, p=curve_point_list)
        ik_spline_curve_name = spline_handle_name.replace('Handle','Curve')
        ik_spline_curve = cmds.rename('curve1',ik_spline_curve_name)

    if cmds.objExists('effector1'):
        ik_spline_effector_name = spline_handle_name.replace('Handle','Effector')
        ik_spline_effector = cmds.rename('effector1',ik_spline_effector_name)

    cmds.select(clear=True)

    cmds.select(start_bind_joint, add=True)
    cmds.select(mid_bind_joint, add=True)
    cmds.select(end_bind_joint, add=True)
    cmds.select(ik_spline_curve, add=True)

    cmds.skinCluster(bindMethod=0, maximumInfluences=3, name=ik_spline_curve + '_skinCluster')



    cmds.setAttr(spline_ik_handle + '.dTwistControlEnable', 1)
    cmds.setAttr(spline_ik_handle + '.dWorldUpType', world_up_type)
    cmds.setAttr(spline_ik_handle + '.dForwardAxis', forward_axis)
    cmds.setAttr(spline_ik_handle + '.dWorldUpAxis', world_up_axis)
    cmds.setAttr(spline_ik_handle + '.dWorldUpVectorX', world_up_vector_x)
    cmds.setAttr(spline_ik_handle + '.dWorldUpVectorY', world_up_vector_y)
    cmds.setAttr(spline_ik_handle + '.dWorldUpVectorZ', world_up_vector_z)
    cmds.setAttr(spline_ik_handle + '.dWorldUpVectorEndX', world_up_vector_end_x)
    cmds.setAttr(spline_ik_handle + '.dWorldUpVectorEndY',world_up_vector_end_y)
    cmds.setAttr(spline_ik_handle + '.dWorldUpVectorEndZ', world_up_vector_end_z)
    cmds.connectAttr(start_bind_joint + '.worldMatrix', spline_ik_handle + '.dWorldUpMatrix')
    cmds.connectAttr(end_bind_joint + '.worldMatrix', spline_ik_handle + '.dWorldUpMatrixEnd')

    cmds.select(clear=True)

    squash_stretch_setup_list = spline_ik_squash_stretch_setup(joint_list,ik_spline_curve,spline_axis)
    curve_info_node_name = squash_stretch_setup_list[0]
    spline_multiply_divide_node_name = squash_stretch_setup_list[1]


    cmds.parent(ik_spline_curve,spline_setup_ik_group)
    cmds.parent(start_bind_joint,spline_setup_ik_group)
    cmds.parent(mid_bind_joint, spline_setup_ik_group)
    cmds.parent(end_bind_joint, spline_setup_ik_group)
    cmds.parent(spline_ik_handle, spline_setup_ik_group)

    cmds.setAttr(spline_ik_handle+'.visibility',0)
    cmds.setAttr(ik_spline_curve + '.visibility', 0)


    return [spline_setup_ik_group,start_joint_ctrl_grp,end_joint_ctrl_grp,mid_joint_ctrl_grp,curve_info_node_name,spline_multiply_divide_node_name]



def fk_spline_setup(start_joint, divisor):

    """Function that does a FK setup based on the base joint of hierarchy

    start_joint =  str
    """

    fk_joint_list = []

    cmds.select(start_joint, hierarchy=True)

    joint_list = cmds.ls(sl=True,type = 'joint')

    cmds.select(clear=True)

    joint_counter = 0

    for eachJoint in joint_list:

        if joint_counter % divisor == 0:
            fk_joint_name = eachJoint.replace('_jnt', '_fk_jnt')

            fk_joint = cmds.joint(n=fk_joint_name, radius=2)

            cmds.matchTransform(fk_joint, eachJoint)

            cmds.setAttr(fk_joint + '.displayLocalAxis', True)

            fk_joint_list.append(fk_joint)

        joint_counter += 1

    print(joint_list)

    print(fk_joint_list)

    for eachJoint in fk_joint_list:
        freeze(eachJoint)


    fk_ctrl_list = []
    fk_ctrl_group_list = []

    for eachJoint in fk_joint_list:
        fk_ctrl = create_controller(eachJoint, 2,
                                                      18, 'circle', '_ctrl',
                                                      'parent', False)

        fk_ctrl_list.append(fk_ctrl[0])
        fk_ctrl_group_list.append(fk_ctrl[1])

    print(fk_ctrl_list)
    print(fk_ctrl_group_list)

    reverse_ctrl_list = fk_ctrl_list[::1]
    reverse_grp_list = fk_ctrl_group_list[::1]

    print(reverse_ctrl_list)
    print(reverse_grp_list)

    for group, ctrl in zip(reverse_grp_list[1:], reverse_ctrl_list):
        print(f'{group} -> {ctrl}')

        cmds.parent(group, ctrl)

    return fk_joint_list,fk_ctrl_list,fk_ctrl_group_list



def spline_ik_squash_stretch_setup(joint_list,spline_curve_name,spline_axis):

    """spline axis must be a str either, X,Y,Z"""

    curve_info_node = cmds.arclen(spline_curve_name, constructionHistory=True)
    curve_info_node_name = spline_curve_name + '_curveInfo'
    if cmds.objExists('curveInfo1'):
        cmds.rename('curveInfo1', curve_info_node_name)

    spline_multiply_divide_node_name = spline_curve_name + '_multiplyDivide'

    spline_multiply_divide_node = cmds.createNode('multiplyDivide', name=spline_multiply_divide_node_name)

    cmds.connectAttr(curve_info_node_name + '.arcLength',
                     spline_multiply_divide_node_name + '.input1' + '.input1'+spline_axis)

    spline_arclen = cmds.arclen(spline_curve_name)

    cmds.setAttr(spline_multiply_divide_node_name + '.input2' + '.input2'+spline_axis, spline_arclen)
    cmds.setAttr(spline_multiply_divide_node_name + '.operation', 2)

    spline_squash_stretch_pow_name = spline_curve_name + '_squashStretchPow'

    spline_squash_stretch_pow = cmds.createNode('multiplyDivide', name=spline_squash_stretch_pow_name)

    cmds.connectAttr(spline_multiply_divide_node_name + '.output' + '.output'+spline_axis,
                     spline_squash_stretch_pow_name + '.input1' + '.input1'+spline_axis)

    cmds.setAttr(spline_squash_stretch_pow_name + '.operation', 3)
    cmds.setAttr(spline_squash_stretch_pow_name + '.input2' + '.input2'+spline_axis, 0.5)

    spline_squash_stretch_invert_div_name = spline_curve_name + '_squashStretchInvertDiv'

    spline_squash_stretch_invert_div = cmds.createNode('multiplyDivide', name=spline_squash_stretch_invert_div_name)

    cmds.connectAttr(spline_squash_stretch_pow_name + '.output' + '.output'+spline_axis,
                     spline_squash_stretch_invert_div_name + '.input2' + '.input2'+spline_axis)

    cmds.setAttr(spline_squash_stretch_invert_div_name + '.operation', 2)
    cmds.setAttr(spline_squash_stretch_invert_div_name + '.input1' + '.input1'+spline_axis, 1)

    for eachJoint in joint_list:
        cmds.connectAttr(spline_multiply_divide_node_name + '.output' + '.output'+spline_axis,
                         eachJoint + '.scale' + '.scale'+spline_axis)

    for eachJoint in joint_list:

        if spline_axis == 'Y':

            cmds.connectAttr(spline_squash_stretch_invert_div_name + '.output' + '.output'+spline_axis,
                             eachJoint + '.scale' + '.scaleX')
            cmds.connectAttr(spline_squash_stretch_invert_div_name + '.output' + '.output'+spline_axis,
                             eachJoint + '.scale' + '.scaleZ')
        if spline_axis == 'X':

            cmds.connectAttr(spline_squash_stretch_invert_div_name + '.output' + '.output' + spline_axis,
                             eachJoint + '.scale' + '.scaleY')
            cmds.connectAttr(spline_squash_stretch_invert_div_name + '.output' + '.output' + spline_axis,
                             eachJoint + '.scale' + '.scaleZ')

        if spline_axis == 'Z':
            cmds.connectAttr(spline_squash_stretch_invert_div_name + '.output' + '.output' + spline_axis,
                             eachJoint + '.scale' + '.scaleY')
            cmds.connectAttr(spline_squash_stretch_invert_div_name + '.output' + '.output' + spline_axis,
                             eachJoint + '.scale' + '.scaleX')

    cmds.setAttr(spline_curve_name+'.inheritsTransform',0)

    return [curve_info_node_name,spline_multiply_divide_node_name]


def get_distance_between_two_objects(obj_a, obj_b):
    get_object_a_pos = cmds.xform(obj_a, q=True, t=True, ws=True)
    get_object_b_pos = cmds.xform(obj_b, q=True, t=True, ws=True)

    return sqrt(pow(get_object_a_pos[0] - get_object_b_pos[0], 2) + pow(get_object_a_pos[1] - get_object_b_pos[1], 2) + pow(get_object_a_pos[2] - get_object_b_pos[2], 2))









