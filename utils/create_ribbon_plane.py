import maya.cmds as cmds
import re
import importlib


from utils import parent_by_selection_order
from utils import unparent_by_selection_order
from utils import rigging_functions
from utils import controller_curves
from auto_rigger import ik_fk_chain_rig_setup
from auto_rigger import spine_rig

import importlib
importlib.reload(rigging_functions)
importlib.reload(parent_by_selection_order)
importlib.reload(unparent_by_selection_order)
importlib.reload(controller_curves)
importlib.reload(ik_fk_chain_rig_setup)
importlib.reload(spine_rig)

def create_surface(surface_name, plane_width,plane_length,u_patches,v_patches,rotate_x,rotate_y,rotate_z):

    nurbs_plane = cmds.nurbsPlane(width=plane_width, lengthRatio=plane_length,
                                  axis=[0, 0, 0],
                                  patchesU=u_patches, patchesV=v_patches, pivot=[0, 0, 0], degree=3,
                                  name=surface_name)[0]

    cmds.setAttr(nurbs_plane + '.rx', rotate_x)
    cmds.setAttr(nurbs_plane + '.ry', rotate_y)
    cmds.setAttr(nurbs_plane + '.rz', rotate_z)

    rigging_functions.freeze(nurbs_plane)

    cmds.delete(nurbs_plane, constructionHistory=True)

    return surface_name