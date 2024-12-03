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

def ik_fk_chain_rig(joint_list, spline_spans, spline_handle_name, controller_color,
                                      controller_shape,
                                      controller_size,
                                      world_up_type, forward_axis, world_up_axis,
                                      world_up_vector_x, world_up_vector_y, world_up_vector_z,
                                      world_up_vector_end_x, world_up_vector_end_y, world_up_vector_end_z,
                                      control_spans,
                                      root_at_world,
                                      main_rig_grp,spline_axis):

    ik_spline_setup_list = rigging_functions.spline_ik_setup(joint_list, spline_spans, spline_handle_name, controller_color,
                                      controller_shape,
                                      controller_size,
                                      world_up_type, forward_axis, world_up_axis,
                                      world_up_vector_x, world_up_vector_y, world_up_vector_z,
                                      world_up_vector_end_x, world_up_vector_end_y, world_up_vector_end_z,spline_axis)

    ik_spline_setup_group = ik_spline_setup_list[0]

    print (ik_spline_setup_list)

    start_joint = joint_list[0]

    end_joint = joint_list[len(joint_list)-1]

    fk_setup_list = rigging_functions.fk_spline_setup(start_joint, control_spans)

    start_bind_group = ik_spline_setup_list[1]

    end_bind_group = ik_spline_setup_list[2]

    mid_bind_group = ik_spline_setup_list[3]

    start_constraint_name = start_bind_group.replace('_grp', '_parentConstraint')

    end_constraint_name = end_bind_group.replace('_grp', '_parentConstraint')

    start_fk_joint = fk_setup_list[0][0]
    end_fk_joint = fk_setup_list[0][(len(fk_setup_list[0])-1)]
    fk_setup_root_grp = fk_setup_list[2][0]
    fk_joint_list = fk_setup_list[0]


    cmds.parentConstraint(start_fk_joint, start_bind_group,
                          maintainOffset=True, name=start_constraint_name)

    cmds.parentConstraint(end_fk_joint, end_bind_group,
                          maintainOffset=True, name=end_constraint_name)

    main_ik_fk_ctrl = rigging_functions.create_controller(start_joint, 2, controller_color, 'square',
                                                           '_ctrl', 'none', False)
    main_ik_fk_ctrl_name = main_ik_fk_ctrl[0]

    print (main_ik_fk_ctrl_name)

    main_ik_fk_ctrl_grp = main_ik_fk_ctrl[1]

    ik_fk_setup_group_name = start_bind_group.replace('_grp', '_ikFkSetup_grp')

    ik_fk_setup_group = cmds.group(empty=True,name=ik_fk_setup_group_name)

    print(ik_fk_setup_group_name)

    cmds.matchTransform(ik_fk_setup_group,start_joint)

    cmds.parent(start_joint,ik_fk_setup_group)
    cmds.parent(ik_spline_setup_list, ik_fk_setup_group)
    cmds.parent(fk_setup_root_grp, ik_fk_setup_group)
    cmds.parent(start_fk_joint, ik_fk_setup_group)

    ik_fk_setup_root_group_name = start_bind_group.replace('_grp', '_ikFkSetupRoot_grp')
    ik_fk_setup_root_group = cmds.group(empty=True, name=ik_fk_setup_root_group_name)

    if root_at_world == True:
        cmds.parent(main_ik_fk_ctrl_grp,ik_fk_setup_root_group)
        cmds.parent(ik_fk_setup_group,ik_fk_setup_root_group)

    if root_at_world == False:

        cmds.matchTransform(ik_fk_setup_root_group,ik_fk_setup_group)
        cmds.parent(ik_fk_setup_group, ik_fk_setup_root_group)
        cmds.parent(main_ik_fk_ctrl_grp, ik_fk_setup_root_group)

    cmds.parent(ik_fk_setup_group, main_ik_fk_ctrl_name)

    curve_arclen = ik_spline_setup_list[4]
    spline_setup_multiply_divide = ik_spline_setup_list[5]

    ik_fk_setup_root_multiply_divide_node_name = ik_fk_setup_group_name.replace('_grp','_normalizeMultiplyDivide')

    ik_fk_setup_root_multiply_divide_node = cmds.createNode('multiplyDivide',
                                                            name= ik_fk_setup_root_multiply_divide_node_name)




    cmds.connectAttr(curve_arclen + '.arcLength',
                     ik_fk_setup_root_multiply_divide_node + '.input1' + '.input1'+spline_axis)

    cmds.connectAttr(main_rig_grp + '.scale'+'.scaleY',
                     ik_fk_setup_root_multiply_divide_node_name + '.input2' + '.input2'+spline_axis)

    cmds.setAttr(ik_fk_setup_root_multiply_divide_node_name + '.operation', 2)

    cmds.disconnectAttr(curve_arclen + '.arcLength',
                        spline_setup_multiply_divide+'.input1'+spline_axis)

    cmds.connectAttr(ik_fk_setup_root_multiply_divide_node_name + '.output' + '.output'+spline_axis,
                     spline_setup_multiply_divide + '.input1' + '.input1'+spline_axis)


    cmds.select(clear=True)

    for eachJoint in fk_joint_list:
        cmds.setAttr(eachJoint + '.visibility', 0)

    #mid ctrl space switching setup

    start_ctrl_ik_name = cmds.listRelatives(start_bind_group,allDescendents=True,type='transform')[0]
    mid_ctrl_ik_name = cmds.listRelatives(mid_bind_group,allDescendents=True,type='transform')[0]
    end_ctrl_ik_name = cmds.listRelatives(end_bind_group, allDescendents=True, type='transform')[0]

    cmds.addAttr(mid_ctrl_ik_name, longName='follow', at='enum', en=('world:both:top:bottom'), k=True)
    cmds.addAttr(mid_ctrl_ik_name, longName='startCtrl_parentConstraint_switch', at='bool', dv=0, k=True)
    cmds.addAttr(mid_ctrl_ik_name, longName='endCtrl_parentConstraint_switch', at='bool', dv=0, k=True)

    cmds.select(start_ctrl_ik_name,add=True)
    cmds.select(end_ctrl_ik_name,add=True)
    cmds.select(mid_bind_group,add=True)
    mid_ctrl_parent_constraint_name = mid_ctrl_ik_name.replace('ctrl','parentConstraint')
    mid_ctrl_parent_constraint = cmds.parentConstraint(name =mid_ctrl_parent_constraint_name, maintainOffset=True)
    weight_list = cmds.parentConstraint(mid_ctrl_parent_constraint_name, query=True, weightAliasList=True)
    start_weight_parent_constraint = weight_list[0]
    end_weight_parent_constraint = weight_list[1]

    cmds.connectAttr(mid_ctrl_ik_name+'.startCtrl_parentConstraint_switch',mid_ctrl_parent_constraint_name+'.'+ start_weight_parent_constraint)
    cmds.connectAttr(mid_ctrl_ik_name + '.endCtrl_parentConstraint_switch',mid_ctrl_parent_constraint_name + '.' + end_weight_parent_constraint)

    driver = mid_ctrl_ik_name + '.follow'

    driven_01 = mid_ctrl_ik_name+'.startCtrl_parentConstraint_switch'

    driven_02 = mid_ctrl_ik_name + '.endCtrl_parentConstraint_switch'

    cmds.setAttr(driver, 0)
    cmds.setAttr(driven_01, 0)
    cmds.setAttr(driven_02, 0)
    cmds.setDrivenKeyframe(driven_01, currentDriver=driver, inTangentType='linear', outTangentType='linear')
    cmds.setDrivenKeyframe(driven_02, currentDriver=driver, inTangentType='linear', outTangentType='linear')

    cmds.setAttr(driver, 1)
    cmds.setAttr(driven_01, 1)
    cmds.setAttr(driven_02, 1)
    cmds.setDrivenKeyframe(driven_01, currentDriver=driver, inTangentType='linear', outTangentType='linear')
    cmds.setDrivenKeyframe(driven_02, currentDriver=driver, inTangentType='linear', outTangentType='linear')

    cmds.setAttr(driver, 2)
    cmds.setAttr(driven_01, 0)
    cmds.setAttr(driven_02, 1)
    cmds.setDrivenKeyframe(driven_01, currentDriver=driver, inTangentType='linear', outTangentType='linear')
    cmds.setDrivenKeyframe(driven_02, currentDriver=driver, inTangentType='linear', outTangentType='linear')

    cmds.setAttr(driver, 3)
    cmds.setAttr(driven_01, 1)
    cmds.setAttr(driven_02, 0)
    cmds.setDrivenKeyframe(driven_01, currentDriver=driver, inTangentType='linear', outTangentType='linear')
    cmds.setDrivenKeyframe(driven_02, currentDriver=driver, inTangentType='linear', outTangentType='linear')

    cmds.setAttr(driver, 0)


    return [ik_fk_setup_root_group_name,main_ik_fk_ctrl_name,ik_spline_setup_group,start_bind_group,mid_bind_group,end_bind_group,start_ctrl_ik_name,mid_ctrl_ik_name,end_ctrl_ik_name]

