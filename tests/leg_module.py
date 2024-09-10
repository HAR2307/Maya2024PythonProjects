import maya.cmds as cmds

import importlib

from utils import controller_curves

importlib.reload(controller_curves)





"""Functions"""
def controllers_colors(controller_shape,controller_color):
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


def fk_setup(controller, joint, distance):
    """Function that make joints into controller shapes leaving the transforms empty """
    temp_name = controller
    cmds.scale(distance/12,distance/12,distance/12, controller)
    freeze(controller)
    controller = cmds.rename(controller,'tempItem')
    temp_controller = cmds.rename(cmds.listRelatives(controller, c = True)[0], temp_name)
    cmds.parent(temp_controller,joint, r=True, s = True) #sustituye el shape node por un joint  parent -r -s
    cmds.delete(controller)



"""Leg guide"""
def leg_guide_setup(rig_side, character_name):

    leg_parts = ['upperLeg', 'knee', 'ankle', 'ball', 'toe', 'upperLegBend', 'lowerLegBend']

    cmds.select(d=True)
    if cmds.objExists('c_'+character_name+'pelvis_skinjnt'):
        skin_joints_list =  cmds.ls('*skinjnt')
        print(skin_joints_list)
        skin_joints_group= cmds.group(skin_joints_list, n=character_name + 'skinJnts_grp')
        cmds.parent(skin_joints_group,'lf_'+ character_name + 'LegGuideRig_grp')
        toggle_visibility(skin_joints_group)
        cmds.delete('c_'+character_name+'pelvisFkCtrl_grp')
        try:
            cmds.delete('lf_'+character_name+'heelTwistReverse_multiplyDivide','rt_'+character_name+'heelTwistReverse_multiplyDivide')
        except:
            pass

    if cmds.objExists('lf_'+ character_name + 'LegGuideRig_grp'):
        toggle_visibility('lf_'+ character_name + 'LegGuideRig_grp')

    else:

        cmds.select(d=True)
        pelvis= cmds.joint(n='c_' + character_name + 'pelvis_bnd_jnt_guide')
        cmds.setAttr(pelvis + '.radius', 2)
        cmds.select(d = True)

        upper_leg = cmds.joint(name =rig_side + '_' + character_name + 'upperLeg_bnd_ctrl_guide')
        knee = cmds.joint(name =rig_side + '_' + character_name + 'knee_bnd_ctrl_guide')
        ankle = cmds.joint(name =rig_side + '_' + character_name + 'ankle_bnd_ctrl_guide')
        ball = cmds.joint(name =rig_side + '_' + character_name + 'ball_bnd_ctrl_guide')
        toe = cmds.joint(name =rig_side + '_' + character_name + 'toe_bnd_ctrl_guide')

        bank_left = cmds.joint(name =rig_side + '_' + character_name + 'left_footRoll_jnt_guide')
        bank_right = cmds.joint(name =rig_side + '_' + character_name + 'right_footRoll_jnt_guide')

        heel = cmds.joint(name =rig_side + '_' + character_name + 'heel_bnd_ctrl_guide')

        cmds.parent(heel,ankle)

        cmds.parent(bank_right,bank_left,ball)

        cmds.setAttr(pelvis+'.ty',12)

        cmds.setAttr(upper_leg+'.ty',11)
        cmds.setAttr(upper_leg+'.tx',1)

        cmds.setAttr(knee+'.ty',-5)
        cmds.setAttr(knee+'.tz',1)

        cmds.setAttr(ankle+'.ty',-5)
        cmds.setAttr(ankle+'.tz',-1)

        cmds.setAttr(ball+'.ty',-1)
        cmds.setAttr(ball+'.tz',1)

        cmds.setAttr(toe+'.tz',1)

        cmds.setAttr(bank_left+'.tx',.3)
        cmds.setAttr(bank_right+'.tx',-.3)

        cmds.setAttr(heel+'.ty',-1)

        "create main leg joints"
        joints = cmds.ls(upper_leg,knee,ankle)
        "pole vector visualization"
        mid_locator = cmds.spaceLocator(n=rig_side + '_' + character_name + '_legMidPoint_loc')[0]
        aim_locator = cmds.spaceLocator(n=rig_side + '_' + character_name + '_legAimPoint_loc')[0]
        target_locator = cmds.spaceLocator(n=rig_side + '_' + character_name + '_legTargetPoint_loc')[0]
        poleVector_placement_locator = cmds.spaceLocator(n=rig_side + '_' + character_name + '_pvPlacement_loc')[0]
        poleVector_placement_locator_group = cmds.group(poleVector_placement_locator, n=rig_side + '_' + character_name + '_pvPlacement_offset')
        poleVector_direction_ctrl = controller_curves.create_curve('doubleArrowSemiCircle', character_name + 'PvLegDirection_ctrl')

        cmds.xform(poleVector_direction_ctrl,cp = True)
        cmds.rotate(-90,0,0,poleVector_direction_ctrl)
        freeze(poleVector_direction_ctrl) #cmds.makeIdentity(poleVector_direction_ctrl,apply=True,t=True,r=True,s=True,n=False)
        cmds.setAttr(poleVector_direction_ctrl+'.rx',l=True)
        cmds.setAttr(poleVector_direction_ctrl+'.ry',l=True)

        lock_translations(poleVector_direction_ctrl)
        lock_scales(poleVector_direction_ctrl)

        poleVector_direction_ctrl_grp = cmds.group(poleVector_direction_ctrl, n=rig_side + '_' + character_name + 'PvlegDirectionCtrl_grp')

        cmds.parent(poleVector_placement_locator_group,poleVector_direction_ctrl,r=True)

        cmds.setAttr(poleVector_placement_locator+'.ty',l=True)
        cmds.setAttr(poleVector_placement_locator+'.tz',l=True)

        lock_rotations(poleVector_placement_locator)
        lock_scales(poleVector_placement_locator)

        cmds.pointConstraint(knee,poleVector_direction_ctrl_grp)
        cmds.orientConstraint(aim_locator,poleVector_direction_ctrl_grp)

        cmds.setAttr(mid_locator + '.localScaleX',0)
        cmds.setAttr(mid_locator + '.localScaleY',0)
        cmds.setAttr(mid_locator + '.localScaleZ',0)

        cmds.setAttr(aim_locator + '.localScaleX',0)
        cmds.setAttr(aim_locator + '.localScaleY',0)
        cmds.setAttr(aim_locator + '.localScaleZ',0)

        cmds.setAttr(target_locator + '.localScaleX',0.5)
        cmds.setAttr(target_locator + '.localScaleY',0.5)
        cmds.setAttr(target_locator + '.localScaleZ',0.5)

        #adelantamos el locator target 4.5

        cmds.setAttr(target_locator + '.tx',4.5)

        cmds.parent(aim_locator,mid_locator)
        cmds.parent(target_locator,aim_locator)

        cmds.parentConstraint(upper_leg,ankle,mid_locator)
        cmds.aimConstraint(knee,aim_locator,worldUpType='object',worldUpObject = upper_leg,
                           worldUpVector=(0,1,0))

        aim_curve=cmds.curve(d=1, p=[(1,0,0),(0,0,0)], name=rig_side + '_' + character_name + 'legAimVectorCurve')
        aim_cluster_a = cmds.cluster(aim_curve +'.cv[0]', name=rig_side + '_' + character_name + 'legAimVectorCurveClusterA')[1]
        aim_cluster_b = cmds.cluster(aim_curve +'.cv[1]', name=rig_side + '_' + character_name + 'legAimVectorCurveClusterB')[1]

        cmds.parentConstraint(knee,aim_cluster_a)
        cmds.parentConstraint(target_locator,aim_cluster_b)

        cmds.delete(cmds.parentConstraint(target_locator,poleVector_placement_locator_group))

        #CleanUp

        legGuide_group = cmds.group(poleVector_direction_ctrl_grp, mid_locator, aim_cluster_a, aim_cluster_b, aim_curve, name=rig_side + '_' + character_name + 'LegGuideRig_grp')
        legGuide_master_curve = cmds.circle(r = 6, nr=(0,1,0), n='legGuides_ctrl',constructionHistory=False)[0]
        controllers_colors(pelvis,22)
        controllers_colors(upper_leg,22)
        controllers_colors(upper_leg,22)

        toggle_visibility(aim_cluster_a),toggle_visibility(aim_cluster_b)
        template_mode(mid_locator),template_mode(aim_curve)

        cmds.delete(cmds.parentConstraint(knee,legGuide_master_curve))
        cmds.parent(legGuide_group,pelvis,upper_leg,legGuide_master_curve)

        no_transform_group = cmds.group(aim_curve, n = 'legNoTransform_grp')
        cmds.setAttr(no_transform_group + '.inheritsTransform',0)

        legGuide_group = cmds.group(legGuide_master_curve, n =rig_side + '_' + character_name + 'LegGuide_grp')
        toggle_visibility(target_locator)

        if cmds.objExists(character_name + 'LegGuide_grp'):
            cmds.parent(legGuide_group, character_name + 'LegGuide_grp')


"""leg rig"""

def leg_rig_setup(rig_side, character_name):


    leg_parts = ['upperLeg', 'knee', 'ankle', 'ball', 'upperLegBend', 'lowerLegBend'] #toe abd tip ommited because is an end joint

    left_skin_joints_list = []
    right_skin_joints_list = []

    if rig_side == 'lf':
        cmds.select(d = True)
        pelvis_joint = cmds.joint(n='c_' + character_name + 'pelvis_bnd_jnt')
        cmds.setAttr(pelvis_joint + '.radius',2)
        toggle_visibility('lf_' + character_name + 'LegGuide_grp')
        cmds.delete(cmds.parentConstraint(pelvis_joint+ '_guide',pelvis_joint))
    cmds.select(d = True)

    upper_leg = cmds.joint(name =rig_side + '_' + character_name + 'upperLeg_bnd_ctrl')
    knee = cmds.joint(name =rig_side + '_' + character_name + 'knee_bnd_ctrl')
    ankle = cmds.joint(name =rig_side + '_' + character_name + 'ankle_bnd_ctrl')
    ball = cmds.joint(name =rig_side + '_' + character_name + 'ball_bnd_ctrl')
    toe = cmds.joint(name =rig_side + '_' + character_name + 'toe_bnd_ctrl')

    leg_bnd_controllers_list = [upper_leg, knee, ankle, ball, toe]


    ##upper_leg = lf_upperLeg_jnt_guide, upper_leg[2:] = _upperLeg_jnt_guide

    for eachJoint in leg_bnd_controllers_list:
        cmds.delete(cmds.parentConstraint('lf'+eachJoint[2:]+'_guide',eachJoint))


    #create offset groups
    upper_leg_offset = cmds.group(em = True, name =rig_side + '_' + character_name + 'upperLegOffset_grp')
    knee_offset = cmds.group(em = True, name =rig_side + '_' + character_name + 'kneeOffset_grp')
    ankle_offset = cmds.group(em = True, name =rig_side + '_' + character_name + 'ankleOffset_grp')
    ball_offset = cmds.group(em = True, name =rig_side + '_' + character_name + 'ballOffset_grp')
    toe_offset = cmds.group(em = True, name =rig_side + '_' + character_name + 'toeOffset_grp')

    leg_offset_groups_list = [upper_leg_offset,knee_offset,ankle_offset,ball_offset,toe_offset]


    #constraint offset groups to joints, parent joints tgo offset groups

    constraint_offset_groups_to_joints_dict = {leg_bnd_controllers_list[i]: leg_offset_groups_list[i] for i in range(len(leg_bnd_controllers_list))}

    for eachJoint, eachGroup in constraint_offset_groups_to_joints_dict.items():
        cmds.delete(cmds.parentConstraint(eachJoint, eachGroup))
        cmds.parent(eachJoint,eachGroup)
        cmds.setAttr(eachJoint+'.jointOrientX',0)
        cmds.setAttr(eachJoint+'.jointOrientY',0)
        cmds.setAttr(eachJoint+'.jointOrientZ',0)
        set_rotations(eachJoint,0)

    #parent in hierarchy
    cmds.parent(knee_offset, upper_leg)
    cmds.parent(ankle_offset, knee)
    cmds.parent(ball_offset, ankle)
    cmds.parent(toe_offset, ball)

    if rig_side == 'rt':
        delete_constraint_offset_groups_to_joints_dict = {leg_bnd_controllers_list[i]: leg_offset_groups_list[i] for i in range(len(leg_bnd_controllers_list))}

        for eachJoint, eachGroup in delete_constraint_offset_groups_to_joints_dict.items():

            cmds.delete(cmds.parentConstraint('lf_' + eachJoint[3:] , eachGroup))

    ##Get scale of the leg

    leg_start =  cmds.xform(upper_leg,q=True, worldSpace=True,rotatePivot=True)
    leg_end =  cmds.xform(ankle,q=True, worldSpace=True,rotatePivot=True)

    distance_shape =  cmds.createNode('distanceDimShape',n='deleteMe_distance')
    cmds.setAttr(distance_shape+'.endPoint',*(leg_end))
    cmds.setAttr(distance_shape+'.startPoint',*(leg_start))
    distance_value = cmds.getAttr(distance_shape+'.distance')
    cmds.delete(cmds.listRelatives(distance_shape,p=True))

    #FK Setup

    upper_leg_fk_ctrl = controller_curves.create_curve('sphere', rig_side + '_' + character_name + 'upperLeg_fk_ctrl')
    knee_fk_ctrl = controller_curves.create_curve('sphere', rig_side + '_' + character_name + 'knee_fk_ctrl')
    ankle_fk_ctrl = controller_curves.create_curve('sphere', rig_side + '_' + character_name + 'ankle_fk_ctrl')
    ball_fk_ctrl = controller_curves.create_curve('sphere', rig_side + '_' + character_name + 'ball_fk_ctrl')
    toe_fk_ctrl= controller_curves.create_curve('sphere', rig_side + '_' + character_name + 'toe_fk_ctrl')

    fk_ctrls_list = [upper_leg_fk_ctrl,knee_fk_ctrl,ankle_fk_ctrl,ball_fk_ctrl,toe_fk_ctrl]

    fk_setup_dict = {fk_ctrls_list[i]: leg_bnd_controllers_list[i] for i in range(len(leg_bnd_controllers_list))}

    for eachController, eachJoint in fk_setup_dict.items():
        fk_setup(eachController, eachJoint, distance_value)


    #IK Setup
    ik_leg_ctrl = controller_curves.create_curve('cube', rig_side + '_' + character_name + 'leg_ik_ctrl')
    cmds.rename(cmds.listRelatives(ik_leg_ctrl,c = True)[0], rig_side + '_' + character_name + 'ik_leg_shape')
    cmds.scale(distance_value/9,distance_value/9,distance_value/9,ik_leg_ctrl)
    freeze(ik_leg_ctrl)

    foot_control_group = cmds.group(ik_leg_ctrl, name =rig_side + '_' + character_name + 'ikFootCtrl_grp')
    cmds.delete(cmds.parentConstraint(ankle,foot_control_group))

    leg_ik_handle= cmds.ikHandle(startJoint=upper_leg, endEffector=ankle, name=rig_side + '_' + character_name + 'legIkrpSolver_ikHandle', solver='ikRPsolver')[0]
    cmds.setAttr(leg_ik_handle+'.ikFkManipulation',1)

    poleVector_ctrl = controller_curves.create_curve('cube', rig_side + '_' + character_name + 'leg_poleVector_ctrl')
    cmds.rename(cmds.listRelatives(ik_leg_ctrl,c = True)[0], rig_side + '_' + character_name + 'leg_poleVector_Shape')
    cmds.scale(distance_value / 10, distance_value / 10, distance_value / 10, poleVector_ctrl)
    freeze(poleVector_ctrl)

    poleVector_controller_group = cmds.group(poleVector_ctrl, name =rig_side + '_' + character_name + 'legPoleVectorCtrl_grp')
    cmds.delete(cmds.parentConstraint('lf' + '_' + character_name + '_pvPlacement_loc', poleVector_controller_group))

    neutralWorld_locator = cmds.spaceLocator(n=rig_side + '_' + character_name + 'legNeutralWorldPv_loc')[0]
    cmds.delete(cmds.pointConstraint(poleVector_ctrl,neutralWorld_locator))

    localFoot_locator = cmds.spaceLocator(n=rig_side + '_' + character_name + 'legLocalFootPv_loc')[0]
    cmds.delete(cmds.pointConstraint(poleVector_ctrl,localFoot_locator))
    cmds.parent(localFoot_locator,ik_leg_ctrl)

    poleVector_constraint = cmds.parentConstraint(neutralWorld_locator,localFoot_locator,poleVector_controller_group,mo=True)[0]
    cmds.poleVectorConstraint(poleVector_ctrl,leg_ik_handle)
    cmds.parent(leg_ik_handle,ik_leg_ctrl)

    #add shared attribuutes for ik fk and space switching
    leg_attrs_controller = controller_curves.create_curve('point', rig_side + '_' + character_name + 'legAttributes_ctrl')
    leg_attrs_shape = cmds.rename(cmds.listRelatives(leg_attrs_controller, c=True)[0], rig_side + '_' + character_name + 'legAttributes_shape')

    cmds.addAttr(leg_attrs_shape,longName='IK_FK_SWITCHES',attributeType='enum',enumName=('____'),keyable=True)
    cmds.addAttr(leg_attrs_shape,longName='FK_IK_leg',attributeType='float',max=1,min=0,keyable=True)
    cmds.addAttr(leg_attrs_shape,longName='FK_IK_poleVector',attributeType='float',max=1,min=0,keyable=True)
    cmds.addAttr(leg_attrs_shape, longName = 'bendyLeg', attributeType = 'float', max = 1, min = 0, keyable = True)
    cmds.addAttr(leg_attrs_shape,longName='stretchLegScale',attributeType='float',max=1,min=0,keyable=True)

    cmds.setAttr(leg_attrs_shape+'.IK_FK_SWITCHES',l=True)
    cmds.setAttr(leg_attrs_shape+'.FK_IK_leg',1)
    cmds.setAttr(leg_attrs_shape+'.bendyLeg',1)
    cmds.setAttr(leg_attrs_shape+'.stretchLegScale',1)

    reverse_IKFK_switch =  cmds.createNode('reverse',n = 'ikLegSwitch_reverse')
    cmds.connectAttr(leg_attrs_shape+'.FK_IK_poleVector',reverse_IKFK_switch+'.ix') #input X = .ix
    cmds.connectAttr(leg_attrs_shape+'.FK_IK_leg',reverse_IKFK_switch+'.iz')

    #connect pole Vector

    cmds.connectAttr(reverse_IKFK_switch + '.ox',poleVector_constraint+'.'+neutralWorld_locator+'W0') #output X = .ox
    cmds.connectAttr(leg_attrs_shape + '.FK_IK_poleVector', poleVector_constraint + '.' + localFoot_locator + 'W1')

    #create pointers for pole vector

    cmds.select(d=True)
    pole_vector_joint = cmds.joint(name =rig_side + '_' + character_name + 'poleVectorLeg_jnt')
    cmds.setAttr(pole_vector_joint+'.v',0)
    cmds.parent(pole_vector_joint,poleVector_ctrl,r=True)
    pole_vector_curve= cmds.curve(d = 1, p = [(0,0,0),(0,0,1)], n =rig_side + '_' + character_name + 'poleVectorPointer_curve')
    pole_vector_curve_cluster01 = cmds.cluster(pole_vector_curve + '.cv[0]')
    pole_vector_curve_cluster02 = cmds.cluster(pole_vector_curve + '.cv[1]')
    cmds.delete(cmds.parentConstraint(pole_vector_joint,pole_vector_curve_cluster01))
    cmds.delete(cmds.parentConstraint(knee,pole_vector_curve_cluster02))
    cmds.delete(pole_vector_curve,constructionHistory=True)
    cmds.skinCluster(pole_vector_joint,knee,pole_vector_curve)
    cmds.parent(pole_vector_curve,poleVector_ctrl)
    cmds.setAttr(pole_vector_curve + '.inheritsTransform',0) #avoiding double transforms

    #stretch Legs
    cmds.connectAttr(leg_attrs_shape+'.stretchLegScale',upper_leg+'.sy')
    cmds.connectAttr(leg_attrs_shape+'.stretchLegScale',knee+'.sy')

    #parent attribute shape on controllers

    leg_ctrls_parent_to_attrs_shape = [ik_leg_ctrl,upper_leg,knee,ankle,ball,toe,poleVector_ctrl]

    for eachCtrl in leg_ctrls_parent_to_attrs_shape:
        cmds.parent(leg_attrs_shape, eachCtrl, shape=True, add=True)


    leg_ik_group = cmds.group(foot_control_group, poleVector_controller_group, n =rig_side + '_' + character_name + 'poleVectorPointerIk_grp')

    #make Main Leg _ctrl
    if cmds.objExists('c_' + character_name + 'pelvis_fk_ctrl'):
        pelvis_fk_ctrl = 'c_' + character_name + 'pelvis_fk_ctrl'
        pelvis_fk_ctrl_group = 'c_' + character_name + 'pelvisFkCtrl_grp'
        pelvis_ik_ctrl = 'c_' + character_name + 'pelvis_ik_ctrl'
        pelvis_ik_ctrl_group = 'c_' + character_name + 'pelvisIkCtrl_grp'
    else:
        pelvis_fk_ctrl = controller_curves.create_curve('circle','c_' + character_name + 'pelvis_fk_ctrl')
        cmds.scale(distance_value/3.5,distance_value/3.5,distance_value/3.5,pelvis_fk_ctrl)
        freeze(pelvis_fk_ctrl)
        pelvis_fk_ctrl_group = cmds.group(pelvis_fk_ctrl, n ='c_' + character_name + 'pelvisFkCtrl_grp')

        pelvis_ik_ctrl = controller_curves.create_curve('square','c_' + character_name + 'pelvis_ik_ctrl')
        cmds.scale(distance_value / 4.5, distance_value / 4.5, distance_value / 4.5, pelvis_ik_ctrl)
        freeze(pelvis_ik_ctrl)
        pelvis_ik_ctrl_group = cmds.group(pelvis_ik_ctrl, n='c_' + character_name + 'pelvisIKCtrl_grp')

        cmds.parent(pelvis_ik_ctrl_group,pelvis_fk_ctrl)
        cmds.delete((cmds.pointConstraint(pelvis_joint,pelvis_fk_ctrl_group)))

    #Foot Setup

    cmds.addAttr(ik_leg_ctrl, longName = 'Foot_functions', at = 'enum', en = ('____'), k = True)
    cmds.addAttr(ik_leg_ctrl, longName = 'Foot_roll', at = 'float', k = True)
    cmds.addAttr(ik_leg_ctrl, longName = 'Foot_bank', at = 'float', k = True)
    cmds.addAttr(ik_leg_ctrl, longName = 'Tip_roll', at = 'float', k = True)
    cmds.addAttr(ik_leg_ctrl, longName = 'Tip_twist', at = 'float', k = True)
    cmds.addAttr(ik_leg_ctrl, longName = 'Heel_roll', at = 'float', k = True)
    cmds.addAttr(ik_leg_ctrl, longName = 'Heel_twist', at = 'float', k = True)
    cmds.addAttr(ik_leg_ctrl, longName = 'Heel_tilt', at = 'float', k = True)
    cmds.setAttr(ik_leg_ctrl + '.Foot_functions', l = True)
    cmds.select(d = True)

    heel_roll_jnt=cmds.joint(name =rig_side + '_' + character_name + 'heelFootRoll_jnt')
    foot_tip_jnt = cmds.joint(name =rig_side + '_' + character_name + 'footTipFootRoll_jnt')
    ball_roll_jnt = cmds.joint(name =rig_side + '_' + character_name + 'ballFootRoll_jnt')
    foot_ankle_jnt = cmds.joint(name =rig_side + '_' + character_name + 'footAnkleTipFootRoll_jnt')
    heel_group = cmds.group(heel_roll_jnt, name =rig_side + '_' + character_name + 'heelFootRollJnt_grp')
    cmds.delete((cmds.pointConstraint('lf' + '_' + character_name + 'heel_bnd_ctrl_guide', heel_group)))
    cmds.delete(cmds.aimConstraint(toe, heel_group, aimVector = (0, 0, 1), upVector = (0, 1, 0), worldUpObject = ankle))
    cmds.delete((cmds.pointConstraint(toe, foot_tip_jnt)))
    cmds.delete((cmds.pointConstraint(ball, ball_roll_jnt)))
    cmds.delete((cmds.pointConstraint(ankle, foot_ankle_jnt)))
    cmds.parent(leg_ik_handle,foot_ankle_jnt)
    set_rotations(ball,0)

    ik_foot_handle =  cmds.ikHandle(startJoint=ankle, endEffector=ball, name=rig_side + '_' + character_name + 'footIKSCsolver', solver ='ikSCsolver')[0]
    ik_toe_handle =  cmds.ikHandle(startJoint=ball, endEffector=toe, name=rig_side + '_' + character_name + 'toeIKSCsolver', solver ='ikSCsolver')[0]

    ball_roll_ctrl = controller_curves.create_curve('doubleArrowSemiCircle', rig_side + '_' + character_name + 'ball_ik_ctrl')
    cmds.setAttr(ball_roll_ctrl+'.rz',-90)
    cmds.scale(distance_value/20, distance_value/20, distance_value/20, ball_roll_ctrl)
    freeze(ball_roll_ctrl)
    ball_ik_ctrl_grp = cmds.group(ball_roll_ctrl, n =rig_side + '_' + character_name + 'ballIkCtrl_grp')
    cmds.connectAttr(leg_attrs_shape +'.FK_IK_leg', ball_ik_ctrl_grp+'.v')
    cmds.delete(cmds.parentConstraint(ball_roll_jnt, ball_ik_ctrl_grp))
    cmds.parentConstraint(foot_tip_jnt, ball_ik_ctrl_grp, mo = True)
    #Add toe rotation
    toe_rotation_locator = cmds.spaceLocator(n =rig_side + '_' + character_name + 'iKtoeRotate_loc')[0]
    cmds.delete(cmds.pointConstraint(toe, toe_rotation_locator))
    cmds.parent(toe_rotation_locator, ball_roll_ctrl)
    cmds.setAttr(toe_rotation_locator+'.v',0)
    cmds.parent(ik_foot_handle,ball_roll_jnt)
    cmds.parent(ik_toe_handle,toe_rotation_locator)

    foot_roll_condition_forward= cmds.createNode('condition', n =rig_side + '_' + character_name + 'footRollForward_cnd')
    foot_roll_condition_back = cmds.createNode('condition', n =rig_side + '_' + character_name + 'footRollBack_cnd')
    toeTip_add_double_linear = cmds.createNode('addDoubleLinear', n =rig_side + '_' + character_name + 'rollToeTipRotValue_addDLinear')
    toeRoot_add_double_linear = cmds.createNode('addDoubleLinear', n =rig_side + '_' + character_name + 'rollToeRootRotValue_addDLinear')
    foot_roll_reverse_multiply_divide = cmds.createNode('multiplyDivide', n =rig_side + '_' + character_name + 'footRollReverse_multiplyDivide')

    #connect foot roll attributes to nodes

    cmds.connectAttr(ik_leg_ctrl + '.Foot_roll', foot_roll_condition_forward + '.firstTerm')
    cmds.connectAttr(ik_leg_ctrl + '.Foot_roll', toeTip_add_double_linear + '.input1')
    cmds.connectAttr(toeTip_add_double_linear + '.output', foot_roll_condition_forward + '.colorIfTrueR')
    cmds.connectAttr(foot_roll_condition_forward + '.outColorR', foot_tip_jnt + '.rx')

    #set foot roll attributes

    cmds.setAttr(foot_roll_condition_forward + '.secondTerm', 30)
    cmds.setAttr(foot_roll_condition_forward + '.operation', 3) # caching 3 = greater or equal to
    cmds.setAttr(toeTip_add_double_linear + '.input2', -30)
    cmds.setAttr(foot_roll_condition_forward + '.colorIfFalseR', 0)
    cmds.setAttr(foot_roll_condition_back + '.secondTerm', 30)
    cmds.setAttr(foot_roll_condition_back + '.operation', 3)
    cmds.setAttr(toeRoot_add_double_linear + '.input2', -60)
    cmds.setAttr(foot_roll_reverse_multiply_divide + '.input2X', -1)

    cmds.connectAttr(toeRoot_add_double_linear + '.o', foot_roll_reverse_multiply_divide + '.input1X')
    cmds.connectAttr(ik_leg_ctrl + '.Foot_roll', toeRoot_add_double_linear + '.input1')
    cmds.connectAttr(ik_leg_ctrl + '.Foot_roll', foot_roll_condition_back + '.colorIfFalseR')
    cmds.connectAttr(ik_leg_ctrl + '.Foot_roll', foot_roll_condition_back + '.firstTerm')
    cmds.connectAttr(ik_leg_ctrl + '.Heel_roll', heel_roll_jnt + '.rx')

    heel_twist_multiply_divide = cmds.createNode('multiplyDivide', n =rig_side + '_' + character_name + 'heelTwistReverse_multiplyDivide')
    cmds.setAttr(heel_twist_multiply_divide + '.i2x', -1)
    cmds.setAttr(heel_twist_multiply_divide + '.i2y', -1)
    cmds.connectAttr(ik_leg_ctrl + '.Heel_twist', heel_roll_jnt + '.ry')
    cmds.connectAttr(foot_roll_reverse_multiply_divide + '.ox', foot_roll_condition_back + '.colorIfTrueR')
    cmds.connectAttr(foot_roll_condition_back + '.outColorR', ball_roll_jnt + '.rx')

    toe_roll_locator = cmds.spaceLocator(n =rig_side + '_' + character_name + 'iKtoeRoll_loc')[0]
    toe_roll_locator_grp = cmds.group(toe_roll_locator, n =rig_side + '_' + character_name + 'iKtoeRollLoc_grp')
    cmds.delete(cmds.parentConstraint(foot_tip_jnt,toe_roll_locator_grp))
    cmds.parent(heel_group,toe_roll_locator)
    cmds.connectAttr(ik_leg_ctrl+'.Tip_roll',toe_roll_locator+'.rx')
    lock_scales(ball_roll_ctrl)
    lock_translations(ball_roll_ctrl)

    tip_roll_ctrl = controller_curves.create_curve('doubleArrowSemiCircle', rig_side + '_' + character_name + 'tip_ik_ctrl')
    cmds.setAttr(tip_roll_ctrl + '.ry', 90)
    cmds.scale(distance_value/20, distance_value/20, distance_value/20, tip_roll_ctrl)
    freeze(tip_roll_ctrl)
    tip_roll_ctrl_offset_grp = cmds.group(tip_roll_ctrl, n =rig_side + '_' + character_name + 'tipRollCtrlOffset_grp')
    tip_roll_ctrl_grp = cmds.group(tip_roll_ctrl_offset_grp, n =rig_side + '_' + character_name + 'tipIkCtrl_grp')
    cmds.delete(cmds.parentConstraint(toe, tip_roll_ctrl_grp))
    cmds.connectAttr(ik_leg_ctrl + '.Tip_twist', tip_roll_ctrl_offset_grp + '.ry')
    cmds.connectAttr(ik_leg_ctrl + '.Heel_tilt', heel_roll_jnt + '.rz')

    #connect foot rolls for ik and fk
    cmds.parent(toe_roll_locator_grp,tip_roll_ctrl)
    cmds.parent(tip_roll_ctrl_grp,ball_ik_ctrl_grp,ik_leg_ctrl)

    #connect IK leg blend

    cmds.connectAttr(leg_attrs_shape + '.FK_IK_leg', leg_ik_handle + '.ikBlend')
    cmds.connectAttr(leg_attrs_shape + '.FK_IK_leg', ik_toe_handle + '.ikBlend')
    cmds.connectAttr(leg_attrs_shape + '.FK_IK_leg', ik_foot_handle + '.ikBlend')
    cmds.connectAttr(leg_attrs_shape + '.FK_IK_leg', ik_leg_ctrl + '.v')
    cmds.connectAttr(leg_attrs_shape + '.FK_IK_leg', poleVector_ctrl + '.v')

    for eachFKCtrl in fk_ctrls_list:
        cmds.connectAttr(reverse_IKFK_switch + '.oz', eachFKCtrl + '.v')

    #basic bendy leg
    cmds.select(d = True)
    upper_leg_bend_jnt = cmds.joint(n =rig_side + '_' + character_name + 'upperLegBend_jnt')
    lower_leg_bend_jnt = cmds.joint(n =rig_side + '_' + character_name + 'lowerLegBend_jnt')
    upper_leg_bend_ctrl = controller_curves.create_curve('circle', rig_side + '_' + character_name + 'upperLegBend_ctrl')
    cmds.scale(distance_value/20, distance_value/20, distance_value/20, upper_leg_bend_ctrl)
    lower_leg_bend_ctrl = controller_curves.create_curve('circle', rig_side + '_' + character_name + 'lowerLegBend_ctrl')
    cmds.scale(distance_value/20, distance_value/20, distance_value/20, lower_leg_bend_ctrl)
    upper_leg_bend_ctrl_grp = cmds.group(upper_leg_bend_ctrl, n =rig_side + '_' + character_name + 'upperLegBendCtrl_grp')
    lower_leg_bend_ctrl_grp = cmds.group(lower_leg_bend_ctrl, n =rig_side + '_' + character_name + 'lowerLegBendCtrl_grp')
    cmds.parent(upper_leg_bend_jnt, upper_leg_bend_ctrl)
    cmds.parent(lower_leg_bend_jnt, lower_leg_bend_ctrl)
    cmds.delete(cmds.parentConstraint(upper_leg, knee, upper_leg_bend_ctrl_grp))
    cmds.delete(cmds.parentConstraint(ankle, knee, lower_leg_bend_ctrl_grp))
    cmds.delete(cmds.aimConstraint(knee, upper_leg_bend_ctrl_grp, aim = (0, 1, 0)))
    cmds.delete(cmds.aimConstraint(knee, lower_leg_bend_ctrl_grp, aim = (0, -1, 0)))
    cmds.parent(upper_leg_bend_ctrl_grp, upper_leg)
    cmds.parent(lower_leg_bend_ctrl_grp, knee)

    #foot banking
    bank_inside_loc = cmds.spaceLocator(n =rig_side + '_' + character_name + 'bankInside_loc')[0]
    bank_outside_loc = cmds.spaceLocator(n =rig_side + '_' + character_name + 'bankOutside_loc')[0]
    cmds.delete(cmds.parentConstraint('lf_' + character_name + 'right_footRoll_jnt_guide', bank_inside_loc))
    cmds.delete(cmds.parentConstraint('lf_' + character_name + 'left_footRoll_jnt_guide', bank_outside_loc))
    cmds.parent(bank_outside_loc, bank_inside_loc)
    cmds.parent(toe_roll_locator_grp, bank_outside_loc)
    cmds.parent(bank_inside_loc, tip_roll_ctrl)
    bank_inside_condition = cmds.createNode('condition', n =rig_side + '_' + character_name + 'footBankinside_cnd')
    cmds.connectAttr(ik_leg_ctrl + '.Foot_bank', bank_inside_condition + '.firstTerm')
    cmds.connectAttr(ik_leg_ctrl + '.Foot_bank', bank_inside_condition + '.colorIfTrueR')
    cmds.setAttr(bank_inside_condition + '.operation', 3)
    cmds.connectAttr(bank_inside_condition + '.outColorR', bank_inside_loc + '.rz')
    bank_outside_condition = cmds.createNode('condition', n =rig_side + '_' + character_name + 'footBankOutside_cnd')
    cmds.connectAttr(ik_leg_ctrl + '.Foot_bank', bank_outside_condition + '.firstTerm')
    cmds.connectAttr(ik_leg_ctrl + '.Foot_bank', bank_outside_condition + '.colorIfTrueR')
    cmds.setAttr(bank_outside_condition + '.operation', 5)
    cmds.connectAttr(bank_outside_condition + '.outColorR', bank_outside_loc + '.rz')
    toggle_visibility(bank_inside_loc)

    # parent pelvis under pelvis control

    if rig_side == 'lf':
        cmds.parent(pelvis_joint, pelvis_ik_ctrl)
        # add limitations
    lock_translations(ankle)
    lock_scales(poleVector_ctrl)
    lock_rotations(poleVector_ctrl)
    lock_scales(ik_leg_ctrl)

    # cleanup

    controllers_colors(upper_leg, 23)
    if rig_side == 'lf':
        controllers_colors(poleVector_ctrl, 6)
        controllers_colors(upper_leg, 6)
        controllers_colors(ik_leg_ctrl, 6)
        controllers_colors(tip_roll_ctrl, 6)
        controllers_colors(ball_roll_ctrl, 6)
        controllers_colors(upper_leg_bend_ctrl, 6)
        controllers_colors(lower_leg_bend_ctrl, 6)
    else:
        controllers_colors(poleVector_ctrl, 13)
        controllers_colors(upper_leg, 13)
        controllers_colors(ik_leg_ctrl, 13)
        controllers_colors(tip_roll_ctrl, 13)
        controllers_colors(ball_roll_ctrl, 13)
        controllers_colors(upper_leg_bend_ctrl, 13)
        controllers_colors(lower_leg_bend_ctrl, 13)
    controllers_colors(pelvis_fk_ctrl, 17)
    toggle_visibility(leg_ik_handle)
    toggle_visibility(neutralWorld_locator)
    toggle_visibility(localFoot_locator)
    toggle_visibility(leg_attrs_shape)
    cmds.delete(cmds.parentConstraint(neutralWorld_locator, localFoot_locator)) # to prevent pv from rotation when switching

    #add bind joints

    skinCluster_list = cmds.ls(typ = 'skinCluster')


    for skin in skinCluster_list:
        try:
            cmds.skinCluster(skin, e=True, moveJointsMode=True)
        except:
            pass
    if rig_side == 'rt':
        if cmds.objExists('c_' + character_name + 'pelvis_skinjnt'):

            pelvis_skinjnt = 'c_' + character_name + 'pelvis_skinjnt'

            for eachLegPart in leg_parts:
                left_bind_joint = 'lf_' + character_name + eachLegPart + '_skinjnt'
                left_skin_joints_list.append(left_bind_joint)

            for eachLegPart in leg_parts:
                right_bind_joint = 'rt_' + character_name + eachLegPart + '_skinjnt'
                right_skin_joints_list.append(right_bind_joint)
        else:
            cmds.select(d=True)
            if cmds.objExists('c_' + character_name + 'pelvis_skinjnt'):
                pelvis_skinjnt = 'c_' + character_name + 'pelvis_skinjnt'

            else:
                pelvis_skinjnt = cmds.joint(n= 'c_' + character_name + 'pelvis_skinjnt')
                cmds.setAttr(pelvis_skinjnt + '.radius', 3)
                controllers_colors(pelvis_skinjnt, 1)

            for eachLegPart in leg_parts:
                left_bind_joint = cmds.joint(n='lf_' + character_name + eachLegPart + '_skinjnt')
                left_skin_joints_list.append(left_bind_joint)

            for eachLegPart in leg_parts:
                right_bind_joint = cmds.joint(n='rt_' + character_name + eachLegPart + '_skinjnt')
                right_skin_joints_list.append(right_bind_joint)


            for eachJoint in left_skin_joints_list:
                controllers_colors(eachJoint,1)
                cmds.setAttr(eachJoint + '.radius', 3)

            for eachJoint in right_skin_joints_list:
                controllers_colors(eachJoint, 1)
                cmds.setAttr(eachJoint + '.radius', 3)

            label_joints(pelvis_skinjnt, pelvis_skinjnt[2:], 0)

            for eachJoint in left_skin_joints_list:
                label_joints(eachJoint,eachJoint[3:],1) #joint = lf_upperLeg_skinjnt [2:]joint = upperLeg_skinjnt

            for eachJoint in right_skin_joints_list:
                label_joints(eachJoint,eachJoint[3:],2)


        # parent binds under corresponding joints
        for leftLegParts in leg_parts:
            if leftLegParts !='upperLegBend' and leftLegParts !='lowerLegBend':
                cmds.parent('lf_' + character_name + leftLegParts + '_skinjnt', 'lf_' + character_name + leftLegParts + '_bnd_ctrl')
            else:
                cmds.parent('lf_' + character_name + leftLegParts + '_skinjnt', 'lf_' + character_name + leftLegParts + '_jnt')

        for rightLegParts in leg_parts:
            if rightLegParts !='upperLegBend' and rightLegParts !='lowerLegBend':
                cmds.parent('rt_' + character_name + rightLegParts + '_skinjnt', 'rt_' + character_name + rightLegParts + '_bnd_ctrl')
            else:
                cmds.parent('rt_' + character_name + rightLegParts + '_skinjnt', 'rt_' + character_name + rightLegParts + '_jnt')



        bind_skinjnts_list= [value for joint in (left_skin_joints_list,right_skin_joints_list) for value in joint]
        cmds.parent(pelvis_skinjnt, 'c_' + character_name + 'pelvis_bnd_jnt')
        bind_skinjnts_list.append(pelvis_skinjnt)

        for eachBindJoint in bind_skinjnts_list:
            set_translations(eachBindJoint,0)
            cmds.setAttr(eachBindJoint + '.jointOrientX', 0)
            cmds.setAttr(eachBindJoint + '.jointOrientY', 0)
            cmds.setAttr(eachBindJoint + '.jointOrientZ', 0)

        # create set
        if cmds.objExists('c_' + character_name + 'legsBind_set'):
            pass
        else:
            cmds.sets(bind_skinjnts_list, n='c_' + character_name + 'legsBind_set')

    #skin cluster manager

    for skinCluster in skinCluster_list:
        try:
            cmds.skinCluster(skinCluster, e = True, moveJointsMode = False) #Turn skin cluster again
        except:
            pass

    cmds.select(d=True)

    legs_group = cmds.group(leg_ik_group, leg_attrs_controller, neutralWorld_locator, upper_leg_offset, n=rig_side + '_' + character_name + 'Leg_grp')

    #mirror leg

    if rig_side == 'lf':
        rig_side = 'rt'
        leg_rig_setup(rig_side, character_name)
    else:
        mirrored_group = cmds.group(em=True, n=rig_side + '_' + character_name + 'mirroredLeg_grp')
        cmds.parent(legs_group, mirrored_group)
        cmds.setAttr(mirrored_group + '.sx', -1)
        cmds.parent('lf_' + character_name + 'Leg_grp', legs_group, 'c_' + character_name + 'pelvisFkCtrl_grp')
        cmds.delete(mirrored_group)
        if cmds.objExists(character_name + 'skinJnts_grp'):
            cmds.delete(character_name + 'skinJnts_grp')
        rig_side = 'lf'
    cmds.parentConstraint(pelvis_ik_ctrl, upper_leg_offset, mo=True)



chr_name = ''
side = 'lf'

leg_guide_setup(side,chr_name)
leg_rig_setup(side,chr_name)



