import maya.cmds as cmds

"""
copiar lo de abajo na mas pa usar el codigo

import maya.cmds as cmds

import importlib
from utils import geometry_renamer
importlib.reload(geometry_renamer)

name = ''

geometry_renamer.rename_geometry(name)

"""

def rename_geometry(name):
    """"parameter  name= str"""

    sel = cmds.ls(selection=True,long=True)
    count = 0
    renamed_geometry = ""

    for eachGeometry in sel:

        count +=1

        print(eachGeometry)

        if count>=1 and count<10:

            renamed_geometry=cmds.rename(eachGeometry,name + '_'+'0'+str(count)+'_geo')

        else:
            renamed_geometry=cmds.rename(eachGeometry, name + '_' + str(count) + '_geo')
