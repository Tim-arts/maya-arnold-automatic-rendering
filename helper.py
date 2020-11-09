import maya.cmds as cmds
import os
import re

def getDelimiter(string, array):
    """
    Return the delimiter contained inside a string
    :param string: The name of the texture
    :param array: An array of delimiters
    :return The delimiter
    """

    for delimiter in array:

        if delimiter in string:

            return delimiter

def listTextures(ui, textures):
    """
    Return an array of images names contained inside the texturePath folder
    :param ui: The name of the material
    :param textures: An array of unfiltered textures
    :return: Array of texture names
    """

    foundTextures = []

    # Get the texture path
    texturePath = ui.texturePath.text()

    for texture in textures:

        file = {}

        # Create the texture path
        filePath = os.path.join(texturePath, texture)

        # If item is a file
        if os.path.isfile(filePath):
            # Get item's extension
            extension = texture.split('.')[-1]

            # If its a valid texture file
            if extension in ui.IMAGE_EXTENSIONS:

                delimiter = getDelimiter(filePath, ui.DELIMITERS)
                textureName = re.split(ui.DELIMITERS, texture)

                # Delete the last item in array
                del textureName[-1]

                textureName = delimiter.join(textureName)

                # file['materialName'] = ''
                file['textureName'] = textureName
                file['filePath'] = filePath
                file['extension'] = extension

                foundTextures.append(file)

    return foundTextures

def createFileNode(texture, UDIMS):
    """
    Creates a file node and a place2d node, set the texture of the file node and connect both of them
    :param texture: The texture as object
    :param UDIMS: If texture has UDIMs
    :return: Name of the file node
    """

    # materialName = texture['materialName']
    textureName = texture['textureName']
    filePath = texture['filePath']

    # Create a file node
    # fileNode = cmds.shadingNode('file', asTexture = True, isColorManaged = True, name = (materialName + '_' + textureName + '_file'))
    fileNode = cmds.shadingNode('file', asTexture = True, isColorManaged = True, name = (textureName + '_file'))

    # Create a place2d node
    # place2d = cmds.shadingNode('place2dTexture', asUtility = True, name = (materialName + '_' + textureName + '_place2d'))
    place2d = cmds.shadingNode('place2dTexture', asUtility = True, name = (textureName + '_place2d'))

    # Set the file path of the file node
    cmds.setAttr(fileNode + '.fileTextureName', filePath, type = 'string')

    if UDIMS:
        cmds.setAttr(fileNode + '.uvTilingMode', 3)

    # Connect the file and the place2d nodes
    connectPlace2dTexture(place2d, fileNode)

    return fileNode

def connectPlace2dTexture(place2d, fileNode):
    """
    Connect the place2d to the file node
    :param place2d: The name of the place2d node
    :param fileNode: The name of the file node
    :return: None
    """

    # Connections to make
    connections = ['rotateUV', 'offset', 'noiseUV', 'vertexCameraOne', 'vertexUvThree', 'vertexUvTwo',
                   'vertexUvOne', 'repeatUV', 'wrapV', 'wrapU', 'stagger', 'mirrorU', 'mirrorV', 'rotateFrame',
                   'translateFrame', 'coverage']

    # Basic connections
    cmds.connectAttr(place2d + '.outUV', fileNode + '.uvCoord', f = True)
    cmds.connectAttr(place2d + '.outUvFilterSize', fileNode + '.uvFilterSize', f = True)

    # Other connections
    for attribute in connections:
        cmds.connectAttr(place2d + '.' + attribute, fileNode + '.' + attribute)

def setFileNameAndOutputDirectory(ui, textureName):
    """
    Set filenames and output directory before rendering
    :param ui: The name of the material
    :param textureName: An array of textures that will be rendered
    """

    if ui.fileName.text() == ui.DEFAULT_OUTPUT_FILENAME or ui.fileName.text() == '':
        fileName = ui.OUTPUT_FILENAME + '_' + textureName
    else:
        fileName = ui.OUTPUT_FOLDER + ui.fileName.text() + '_' + textureName

    if ui.extensionType.text() == ui.DEFAULT_OUTPUT_EXTENSIONTYPE or ui.extensionType.text() == '':
        extensionType = ui.OUTPUT_EXTENSIONTYPE
    else:
        extensionType = ui.extensionType.text()

    # Set output fileName and extensionType
    cmds.setAttr('defaultRenderGlobals.imageFilePrefix', fileName, type = 'string')
    cmds.setAttr("defaultArnoldDriver.ai_translator", extensionType, type = "string")