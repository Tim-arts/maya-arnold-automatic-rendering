from PySide2 import QtCore
from PySide2 import QtWidgets
from shiboken2 import wrapInstance
from maya import OpenMayaUI as omui
import maya.cmds as cmds
import os
import config as config

reload(config)

class AutomaticRenderingUI:
    
    def __init__(self):

        self.actualWorkspace = cmds.workspace(fullName = True)
        self.PLUGIN_NAME = self.PLUGIN_VERSION = self.TEXTURE_FOLDER = ''
        self.PLUGIN_NAME = config.PLUGIN_NAME
        self.PLUGIN_VERSION = config.PLUGIN_VERSION
        self.TEXTURE_FOLDER = config.TEXTURE_FOLDER
        self.IMAGE_EXTENSIONS = config.IMAGE_EXTENSIONS
        self.OUTPUT_FOLDER = config.OUTPUT_FOLDER
        self.DEFAULT_OUTPUT_FILENAME = config.DEFAULT_OUTPUT_FILENAME
        self.OUTPUT_FILENAME = config.OUTPUT_FILENAME
        self.DEFAULT_OUTPUT_EXTENSIONTYPE = config.DEFAULT_OUTPUT_EXTENSIONTYPE
        self.OUTPUT_EXTENSIONTYPE = config.OUTPUT_EXTENSIONTYPE
        self.INFOS = config.INFOS
        self.DELIMITERS = config.DELIMITERS

        print('\n\n' + self.PLUGIN_NAME + ' version ' + self.PLUGIN_VERSION + '\n')

    def createUI(self):
        """
        Creates the UI
        :return: None
        """

        mayaMainWindowPtr = omui.MQtUtil.mainWindow()
        mayaMainWindow = wrapInstance(long(mayaMainWindowPtr), QtWidgets.QWidget)

        # Create our main window
        self.mainWindow = QtWidgets.QDialog()
        self.mainWindow.setParent(mayaMainWindow)
        self.mainWindow.setWindowTitle(self.PLUGIN_NAME + ' version ' + self.PLUGIN_VERSION)
        # self.mainWindow.setFixedSize(220,450)
        self.mainWindow.setWindowFlags(QtCore.Qt.Window)

        # Create vertical layout
        self.layVMainWindowMain = QtWidgets.QVBoxLayout()
        self.mainWindow.setLayout(self.layVMainWindowMain)

        # Create horizontal layout
        self.layHMainWindowMain = QtWidgets.QHBoxLayout()
        self.layVMainWindowMain.insertLayout(0, self.layHMainWindowMain, stretch = 1)

        # Create two vertical layouts
        self.layVMainWindow01 = QtWidgets.QVBoxLayout()
        self.layHMainWindowMain.insertLayout(0, self.layVMainWindow01, stretch = 1)
        self.layVMainWindow02 = QtWidgets.QVBoxLayout()
        self.layHMainWindowMain.insertLayout(1, self.layVMainWindow02, stretch = 3)

        # Texture Folder
        self.grpBrowseForDirectory = QtWidgets.QGroupBox('Textures Folder')
        self.layVMainWindow01.addWidget(self.grpBrowseForDirectory)

        self.textureFolderLayout = QtWidgets.QHBoxLayout()
        self.grpBrowseForDirectory.setLayout(self.textureFolderLayout)

        # Add Texture folder widgets
        sourceImagesFolder = self.actualWorkspace + '/' + self.TEXTURE_FOLDER
        self.texturePath = QtWidgets.QLineEdit(sourceImagesFolder)
        self.texturePath.setToolTip('Set the path of your texture folder')
        self.textureFolderLayout.addWidget(self.texturePath)

        self.getButton = QtWidgets.QPushButton('Get')
        self.getButton.clicked.connect(lambda: self.getTextureFolder())
        self.textureFolderLayout.addWidget(self.getButton)
        self.getButton.setToolTip('Get your texture folder using a dialog window')
        self.getButton.setToolTipDuration(2000)

        # Output
        self.groupOutput = QtWidgets.QGroupBox('Output')
        self.layVMainWindow01.addWidget(self.groupOutput)

        self.outputLayout = QtWidgets.QVBoxLayout()
        self.groupOutput.setLayout(self.outputLayout)

        self.outputInfo = QtWidgets.QLabel(
            'Enter the name and the extension type of the files output'
        )
        self.outputLayout.addWidget(self.outputInfo)

        self.outputSubLayout = QtWidgets.QHBoxLayout()
        self.outputLayout.insertLayout(-1, self.outputSubLayout, stretch = 0)

        self.outputLayoutLabel = QtWidgets.QVBoxLayout()
        self.outputSubLayout.insertLayout(1, self.outputLayoutLabel, stretch = 0)

        self.outputSubLayoutValue = QtWidgets.QVBoxLayout()
        self.outputSubLayout.insertLayout(2, self.outputSubLayoutValue, stretch = 0)

        # Add Output widgets
        self.fileNameLabel = QtWidgets.QLabel('Name')
        self.outputLayoutLabel.addWidget(self.fileNameLabel)

        self.fileName = QtWidgets.QLineEdit(self.DEFAULT_OUTPUT_FILENAME)
        self.outputSubLayoutValue.addWidget(self.fileName)

        self.extensionTypeLabel = QtWidgets.QLabel('Extension')
        self.extensionTypeLabel.setToolTip(', '.join(self.IMAGE_EXTENSIONS))
        self.outputLayoutLabel.addWidget(self.extensionTypeLabel)
        self.extensionTypeLabel.resize(200,200)

        self.extensionType = QtWidgets.QLineEdit(self.DEFAULT_OUTPUT_EXTENSIONTYPE)
        self.outputSubLayoutValue.addWidget(self.extensionType)

        # Launch button
        self.grpLaunch = QtWidgets.QGroupBox('Launch renders')
        self.layVMainWindowMain.addWidget(self.grpLaunch)

        self.launchLayout = QtWidgets.QHBoxLayout()
        self.grpLaunch.setLayout(self.launchLayout)

        # Add Launch widgets
        self.launchButton = QtWidgets.QPushButton('Launch')
        self.launchLayout.addWidget(self.launchButton)

        global window

        try:
            window.close()
            window.deleteLater()
        except:
            pass

        window = self.mainWindow
        self.mainWindow.show()

    def getTextureFolder(self):
        """
        Get the base texture path in the interface, the file dialog start in the base texture path of the project
        :return: The texture directory
        """

        startingDirectory = self.texturePath.text()

        # Get project
        projectDirectory = cmds.workspace(rootDirectory = True, query = True)

        # Set base texture folder
        textureFolder = projectDirectory + '/' + self.TEXTURE_FOLDER

        if os.path.isdir(textureFolder):
            sourceImages = textureFolder
        else:
            sourceImages = projectDirectory

        # Open a file dialog
        result = cmds.fileDialog2(startingDirectory = startingDirectory, fileMode = 2, okCaption = 'Select')

        if result is None:
            return

        workDirectory = result[0]

        # Update the texture path in the interface
        self.texturePath.setText(workDirectory)

        return workDirectory