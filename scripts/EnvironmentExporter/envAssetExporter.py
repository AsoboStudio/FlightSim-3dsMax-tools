from PySide2.QtWidgets import *
from PySide2.QtCore import *
import EnvironmentExporter.ui.mainwindow_ui as mainwindow_ui

from pymxs import runtime as rt
import MaxPlus
import os

from maxsdk import userprop

reload(userprop)
from maxsdk import perforce as sdkperforce
from maxsdk import dialog as sdkdialog
import utils

reload(utils)
reload(sdkperforce)
reload(sdkdialog)


class MainWindow(QDialog):

    def __init__(self, mNode=None, parent=None):
        super(MainWindow, self).__init__(parent, Qt.Window)

        self.ui = mainwindow_ui.Ui_folderSelectorWidget()
        self.ui.setupUi(self)
        self.mNode = mNode
        self.nodePath = getNodePath(mNode)
        self.ui.exportPath.setText(self.nodePath)

        self.ui.browseExportBtn.clicked.connect(self.browseFolderExport)

    def browseFolderExport(self):
        fileDialog = QFileDialog(self)
        fileDialog.setFileMode(QFileDialog.DirectoryOnly)
        fileDialog.setAcceptMode(QFileDialog.AcceptOpen)
        storedPath = self.nodePath
        if not storedPath:
            storedPath = rt.pathConfig.getCurrentProjectFolder()
        folderPath = fileDialog.getExistingDirectory(self, "Chose Folder", storedPath, options=QFileDialog.ReadOnly)
        if folderPath:
            self.ui.exportPath.setText(folderPath)
            setNodePath(self.mNode, path=folderPath)


def getNodePath(mNode):
    nodePath = userprop.getUserProp(mNode, keyName="envAssetPath", defaultValue=None)
    if isinstance(nodePath, unicode) or isinstance(nodePath, str):
        return nodePath
    elif rt.maxFilePath:
        return os.path.join(rt.maxFilePath, "EXPORT")


def setNodePath(mNode, path):
    userprop.setUserProp(mNode, keyName="envAssetPath", value=path)


def run():
    explorer = rt.SceneExplorerManager.GetActiveExplorer()
    items = explorer.SelectedItems()
    condition = lambda x: rt.classOf(x) == rt.Editable_Poly or rt.classOf(x) == rt.Dummy
    validItems = [x for x in items if condition(x)]
    if validItems:
        if items.count == 1 and rt.keyboard.shiftPressed:
            window = MainWindow(mNode=items[0])
            MaxPlus.AttachQWidgetToMax(window)
            window.show()
        else:
            exportProgress = utils.QExportProgress(steps=len(validItems))
            MaxPlus.AttachQWidgetToMax(exportProgress)
            exportProgress.show()
            for i in items:
                if not i:
                    sdkdialog.showMessage("ERROR: No node Selected")
                    pass
                print "PROCESSING node {0}".format(i.name)
                exportPath = getNodePath(mNode=i)
                if exportPath:
                    utils.ExportEnvAsset(maxNode=i, exportProgress=exportProgress, flatten=True, exportPath=exportPath)
                else:
                    sdkdialog.showMessage("ERROR: no path selected for {0}\nShift + Click on export command to set folder path".format(i.name))

