import maya.cmds as cmds

"""Functions"""

def controllers_colors(controller_shape,controller_color):
    shape = controller_shape + 'Shape'
    cmds.setAttr(controller_shape+'.overrideEnabled',1)
    cmds.setAttr(controller_shape+'.overrideColor',controller_color)



"""Guide Mode"""

def guide_base(unique_name):

    if cmds.objExists(unique_name+'Guide_grp'):
        cmds.setAttr(unique_name+'Guide_grp.v',1)
        cmds.delete(unique_name+'Rig_grp')

    else:

        main = cmds.curve(d=1,p=[[5.0, 0.0, 0.0], [3.536, 0.0, -3.536], [0.0, 0.0, -5.0], [-3.536, 0.0, -3.536], [-5.0, 0.0, -0.0], [-3.536, 0.0, 3.536], [-0.0, 0.0, 5.0], [3.536, 0.0, 3.536], [5.0, 0.0, 0.0]]
                          ,n='c_'+unique_name+'Main_ctrl_guide')
        sub = cmds.curve(d=1,p=[[5.0, 0.0, 0.0], [3.536, 0.0, -3.536], [0.0, 0.0, -5.0], [-3.536, 0.0, -3.536], [-5.0, 0.0, -0.0], [-3.536, 0.0, 3.536], [-0.0, 0.0, 5.0], [3.536, 0.0, 3.536], [5.0, 0.0, 0.0]]
                          ,n='c_'+unique_name+'SubMain_ctrl_guide')
        cmds.scale(.7,.7,.7,sub+'.cv[0:8]')

        cmds.parent(sub,main)

        guide_grp = cmds.group(main,n=unique_name+'Guide_grp')

        controllers_colors(main,17)
        controllers_colors(sub,17)

        return main, sub, guide_grp


"""Rig mode"""

def rig_base(unique_name):

    main = cmds.duplicate('c_'+unique_name+'Main_ctrl_guide',n ='c_'+unique_name+'Main_ctrl',rc=True )[0]
    sub = cmds.rename(cmds.listRelatives(main,c=True)[-1],'c_'+unique_name+'SubMain_ctrl')
    cmds.makeIdentity(main,apply=True, t=1,r=1,s=1,n=0,pn=1)
    cmds.parent(main,w=True)
    main_grp =  cmds.group(main,n = unique_name + 'Rig_grp')
    cmds.setAttr(unique_name + 'Guide_grp.v', 0)

name = ''

guide_base(name)
rig_base(name)
