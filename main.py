# Libraries
from mtoa.cmds.arnoldRender import arnoldRender
import os
import maya.cmds as cmds
import UI as ui
import helper

reload(ui)
reload(helper)

def init():
    """
    Script initialization
    """

    # Create the UI
    toolUI = ui.AutomaticRenderingUI()
    toolUI.createUI()
    toolUI.launchButton.clicked.connect(lambda: render(toolUI))

def render (ui):
    """
    Trigger the render
    :param ui: The UI created in UI.py
    """

    # Store the selected polymesh
    selected = cmds.ls(sl = True, dag = True, type = "mesh", long = True)

    if not selected:
        cmds.confirmDialog(title = 'Error', message = 'No polymesh selected!', button = ['Dismiss'])

        return False
    else:
        resolution = getCurrentResolution()
        cameras = getCameras()

        # Get the input values
        texturePath = ui.texturePath.text()

        # Get all the textures in the folder
        textures = helper.listTextures(ui, os.listdir(texturePath))

        for texture in textures:

            # Get texture name
            textureName = texture['textureName'] + '_file.outColor'

            # Get shader name
            shadingEngine = cmds.listConnections(selected , type = 'shadingEngine')
            materials = cmds.ls(cmds.listConnections(shadingEngine ), materials = True)

            # Create file node and 2dPlacer
            helper.createFileNode(texture, False)

            # Link texture to the selected object
            cmds.connectAttr(textureName, (materials[0] + '.baseColor'), f = True)

            # for camera in cameras:
            for camera in cameras:

                # Change output names and directories
                helper.setFileNameAndOutputDirectory(ui, texture['textureName'])
                arnoldRender(resolution['w'], resolution['h'], True, True, camera, ' -layer defaultRenderLayer')

def getCameras():
    """
    Return all the non-default (i.e.: persp top front side) cameras in the scene
    """

    # Get all cameras first
    cameras = cmds.ls(type = 'camera', l = True)

    # Let's filter all startup / default cameras
    startup_cameras = [camera for camera in cameras if cmds.camera(cmds.listRelatives(camera, parent = True)[0], startupCamera = True, q = True)]

    # non-default cameras are easy to find now.
    non_startup_cameras = list(set(cameras) - set(startup_cameras))

    # Let's get their respective transform names, just in-case
    non_startup_cameras_transforms = map(lambda x: cmds.listRelatives(x, parent = True)[0], non_startup_cameras)

    return non_startup_cameras_transforms

# Get current resolution
def getCurrentResolution():
    """
    Return the current renderLayer resolution used in the render settings
    """

    renderlayers = cmds.ls(type = "renderLayer")

    for layer in renderlayers:
        resolution = {
            'w': None,
            'h': None
        }

        if layer == 'defaultRenderLayer':
            resolution['w'] = cmds.getAttr("defaultResolution.width")
            resolution['h'] = cmds.getAttr("defaultResolution.height")

        return resolution