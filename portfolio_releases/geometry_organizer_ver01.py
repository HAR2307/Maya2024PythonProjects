import maya.cmds as cmds

"""A function that renames the selected geometry, renames it and group it
NOTE: Made for Maya 2024 and above """

def rename_geometry(name):
    """"parameter  name= str"""

    sel = cmds.ls(selection=True,long=True)
    count = 0
    geo_group = cmds.group(em=True,name=name)
    renamed_geometry = ""

    for eachGeometry in sel:

        count +=1

        print(eachGeometry)

        if count>=1 and count<10:

            renamed_geometry=cmds.rename(eachGeometry,name + '_'+'0'+str(count)+'_geo')
            cmds.parent(renamed_geometry, geo_group)
        else:
            renamed_geometry=cmds.rename(eachGeometry, name + '_' + str(count) + '_geo')
            cmds.parent(renamed_geometry, geo_group)




rename_geometry("desiredName")
