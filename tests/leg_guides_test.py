import maya.cmds as cmds

def create_left_leg_guides():
    hipLfLocator = cmds.spaceLocator(n='Lf_leg_hip_locator')
    upperLegLfLocator = cmds.spaceLocator(n='Lf_leg_upperLeg_locator')
    kneeLfLocator = cmds.spaceLocator(n='Lf_leg_knee_locator')
    ankleLfLocator = cmds.spaceLocator(n='Lf_leg_ankle_locator')
    ballLfLocator = cmds.spaceLocator(n='Lf_leg_ball_locator')
    toeLfLocator = cmds.spaceLocator(n='Lf_leg_toe_locator')

    cmds.move(1, 0, 0, hipLfLocator)
    cmds.move(2, 0, 0, upperLegLfLocator)
    cmds.move(2, -2, 0, kneeLfLocator)
    cmds.move(2, -3, 0, ankleLfLocator)
    cmds.move(2, -3, 1, ballLfLocator)
    cmds.move(2, -3, 2, toeLfLocator)

    cmds.select(clear=True)

def create_right_leg_guides():
    hipRtLocator = cmds.spaceLocator(n='Rt_leg_hip_locator')
    upperLegRtLocator = cmds.spaceLocator(n='Rt_leg_upperLeg_locator')
    kneeRtLocator = cmds.spaceLocator(n='Rt_leg_knee_locator')
    ankleRtLocator = cmds.spaceLocator(n='Rt_leg_ankle_locator')
    ballRtLocator = cmds.spaceLocator(n='Rt_leg_ball_locator')
    toeRtLocator = cmds.spaceLocator(n='Rt_leg_toe_locator')

    cmds.move(-1, 0, 0, hipRtLocator)
    cmds.move(-2, 0, 0, upperLegRtLocator)
    cmds.move(-2, -2, 0, kneeRtLocator)
    cmds.move(-2, -3, 0, ankleRtLocator)
    cmds.move(-2, -3, 1, ballRtLocator)
    cmds.move(-2, -3, 2, toeRtLocator)

    cmds.select(clear=True)

def mirror_leg_guides():
    allLeftLegLocators = cmds.ls("Lf_leg_*")  ##lista de locators izquierdos
    leftLegLocatorsTransformNodes = cmds.listRelatives(*allLeftLegLocators, p=True,
                                                       f=True)  ##buscas solo los parents, evitando los shapes nodes, aqui buscamos los transforms

    allRightLegLocators = cmds.ls("Rt_leg_*")  ##lista de locators derechos
    rightRightLocatorsTransformNodes = cmds.listRelatives(*allRightLegLocators, p=True, f=True)

    print(allLeftLegLocators)
    print(allRightLegLocators)

    for legLocators, legTransformNodes in enumerate(
            leftLegLocatorsTransformNodes):  ###i es la izquierda, l es la derecha, estamos usando un arreglo bidimensional para esto
        pos = cmds.xform(legTransformNodes, q=True, t=True, ws=True)
        cmds.move(-pos[0], pos[1], pos[2], rightRightLocatorsTransformNodes[legLocators])
