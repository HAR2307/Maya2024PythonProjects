import maya.cmds as cmds

"""
copiar lo de abajo na mas pa usar el codigo

import maya.cmds as cmds

import importlib

from utils import nurbs_ribbon_deformer_setup

importlib.reload(nurbs_ribbon_deformer_setup)

surface_name = '' 
controller_name = ''
rotate_handle_x = 90
rotate_handle_y = 0
rotate_handle_z = 90

nurbs_ribbon_deformer_setup.sine_wave_deformer_setup(surface_name,controller_name,rotate_handle_x,rotate_handle_y,rotate_handle_z)

"""

def sine_wave_deformer_setup(surface_name,controller_name,rotate_handle_x,rotate_handle_y,rotate_handle_z):

    cmds.addAttr(controller_name, longName='wave_toggle', at='bool', dv=0, k=True)
    cmds.addAttr(controller_name, longName='wave_amplitude', at='double', min=-5, max=5, dv=0, k=True)
    cmds.addAttr(controller_name, longName='wave_offset', at='double',dv=0, k=True)

    sine_wave_plane_name = surface_name + '_sine_wave'

    duplicate_surface = cmds.duplicate(surface_name)
    cmds.rename(duplicate_surface,sine_wave_plane_name)

    cmds.select(sine_wave_plane_name)

    sine_deformer_name = surface_name + '_sine_deformer'

    sine_deformer_list=  cmds.nonLinear(type='sine',name=sine_deformer_name)

    cmds.select(clear=True)

    print(sine_deformer_list)

    sine_deformer_handle =  sine_deformer_list[1]

    cmds.setAttr(sine_deformer_handle + '.rx', rotate_handle_x)
    cmds.setAttr(sine_deformer_handle + '.ry', rotate_handle_y)
    cmds.setAttr(sine_deformer_handle + '.rz', rotate_handle_z)

    cmds.connectAttr(controller_name+'.wave_amplitude',sine_deformer_name + '.amplitude')


    driver = controller_name+'.wave_offset'

    driven = sine_deformer_name + '.offset'

    cmds.setAttr(driver, 0)
    cmds.setAttr(driven, 0)
    cmds.setDrivenKeyframe(driven, currentDriver=driver,inTangentType = 'linear',outTangentType = 'linear')

    cmds.setAttr(driver, 10)
    cmds.setAttr(driven, 10)
    cmds.setDrivenKeyframe(driven, currentDriver=driver,inTangentType = 'linear',outTangentType = 'linear')

    cmds.setAttr(driver, 0)

    cmds.select(sine_deformer_name)

    cmds.setInfinity(pri='cycleRelative', poi='cycleRelative')

    cmds.select(clear=True)

    blendshape_name = surface_name+'_bShape'

    cmds.blendShape(sine_wave_plane_name,surface_name,name=blendshape_name)
    cmds.select(clear = True)

    cmds.reorderDeformers(surface_name+'_skinCluster',surface_name+'_bShape',surface_name)

    cmds.connectAttr(controller_name + '.wave_toggle', blendshape_name + '.'+ sine_wave_plane_name)

    deformer_group_name = surface_name + '_sine_deformer_grp'

    deformer_group = cmds.group(name=deformer_group_name, empty=True)

    cmds.parent(sine_wave_plane_name,deformer_group)
    cmds.parent(sine_deformer_handle, deformer_group)

    return deformer_group_name

















