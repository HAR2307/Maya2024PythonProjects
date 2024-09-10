import maya.cmds as cmds

"""
copiar lo de abajo na mas pa usar el codigo

import importlib
from auto_rigger import create_controller

importlib.reload(create_controller)

create_controller.create_controller('shape_name','joint_name',shape_size)

"""

def create_controller(shape,joint,size):

    """"receives: shape=str circle or square, joint=str joint name
    and size=int controller size"""

    ctrl_group = cmds.group(em=True,name=f'{joint}+ctrl_grp')

    controller=None

    if shape == 'circle':
        controller = cmds.circle(nr=(0, 0, size), c=(0, 0, 0), r=1, name=f'{joint}+ctrl')
    if shape == 'square':
        controller= cmds.curve(d=1, p=[(size, 0, size), (size, 0, -size), (-size, 0, -size), (-size, 0, size), (size, 0, size)],
                   name=f'{joint}+ctrl')

    cmds.parent(controller,ctrl_group)
    cmds.matchTransform(ctrl_group, joint)







