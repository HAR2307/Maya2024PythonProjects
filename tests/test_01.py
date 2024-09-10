"""
copiar lo de abajo na mas pa usar el codigo

import importlib
from tests import test_01
importlib.reload(test_01)

test_01.test_function()
"""

import maya.cmds as cmds

def test_function():
    cmds.polyCube(name="pancho")