from PySide2.QtWidgets import *
from PySide2.QtCore import *
import EnvironmentExporter.ui.mainwindow_ui as mainwindow_ui
import pymxs
from pymxs import runtime as rt
import re
import MaxPlus
import os
from maxsdk import userprop
from maxsdk import perforce as sdkperforce
from maxsdk import dialog as sdkdialog
import utils
import xml.etree.ElementTree as ET
from xml.dom import minidom


class MainWindow(QDialog):

    def __init__(self, layerName=None, parent=None):
        super(MainWindow, self).__init__(parent, Qt.Window)

        self.ui = mainwindow_ui.Ui_folderSelectorWidget()
        self.ui.setupUi(self)
        self.layerName = layerName
        self.layerPath = getLayerPath(layerName)
        self.ui.exportPath.setText(self.layerPath)

        self.ui.browseExportBtn.clicked.connect(self.browseFolderExport)

    def browseFolderExport(self):
        fileDialog = QFileDialog(self)
        fileDialog.setFileMode(QFileDialog.DirectoryOnly)
        fileDialog.setAcceptMode(QFileDialog.AcceptOpen)
        storedPath = self.layerPath
        if not storedPath:
            storedPath = rt.pathConfig.getCurrentProjectFolder()
        folderPath = fileDialog.getExistingDirectory(self, "Chose Folder", storedPath, options=QFileDialog.ReadOnly)
        if folderPath:
            self.ui.exportPath.setText(folderPath)
            setLayerPath(layerName=self.layerName, path=folderPath)


def getLayerPath(layerName):
    layerPath = userprop.getUserPropDict(rt.rootNode, propName="envLODsPath", keyName=layerName)
    if isinstance(layerPath, unicode) or isinstance(layerPath, str):
        return layerPath
    elif rt.maxFilePath:
        return os.path.join(rt.maxFilePath, "EXPORT")


def setLayerPath(layerName, path):
    envLODsPath = userprop.getUserPropDict(rt.rootNode, propName="envLODsPath")
    envLODsPath.update({layerName: path})
    userprop.setUserPropDict(rt.rootNode, propName="envLODsPath", dictObj=envLODsPath)


def isValidaFormat(nodeName):
    match = re.search("_LOD[0-9]$", nodeName)
    if match:
        return True
    else:
        return False


def deleteInvalidGLTF(flatName):
    targetGLTFFileName = flatName + ".gltf"
    targetBINFileName = flatName + ".bin"
    if os.path.exists(targetGLTFFileName) or os.path.exists(targetBINFileName):
        print("found {0} to remove".format(flatName))
        sdkperforce.P4delete(targetGLTFFileName)
        sdkperforce.P4delete(targetBINFileName)


def isDefaultLODsValue(LODsValue):
    for lodValue in LODsValue:
        if lodValue != 0:
            return False
    return True


def modifyXML(xmlFilePath, LODsValue=None):
    if LODsValue is None:
        LODsValue = [70, 40, 15]
    elif isDefaultLODsValue(LODsValue):
        LODsValue = [70, 40, 15]
    LODsValue = reversed(sorted(LODsValue))
    if os.path.exists(xmlFilePath):
        file = open(xmlFilePath, "r")
        root = ET.fromstring(file.read())
        if root.tag == "ModelInfo":
            lodsElement = root.find("LODS")
            if lodsElement is not None:
                root.remove(lodsElement)
            lodsElement = ET.Element("LODS")
            for v in LODsValue:
                lodElement = ET.Element("LOD")
                lodElement.set("minSize", str(v))
                lodsElement.append(lodElement)
            root.append(lodsElement)
        sdkperforce.P4edit(xmlFilePath)
        xmlstr = minidom.parseString(ET.tostring(root)).toprettyxml(encoding='UTF-8', indent="   ")
        dom_string = os.linesep.join([s for s in xmlstr.splitlines() if s.strip()])
        with open(xmlFilePath, "w") as f:
            f.write(dom_string)


def setLayerVisibility(root, visibility):
    if root is not None:
        num_children = root.getNumChildren()
        root.ishidden = not visibility
        for i in range(1, num_children + 1):
            child = root.getChild(i)
            setLayerVisibility(child, visibility)


def ExportLODinstance(exportPath, n, exportProgress):
    lodValue = float(userprop.getUserProp(n, "flightsim_lod_value", 0))
    if lodValue is None:
        print("Missing Lod Value in node {0}".format(n.name))
        return None
    utils.ExportEnvAsset(exportPath=exportPath, maxNode=n, exportProgress=exportProgress, flatten=True)
    return lodValue


def exportLODsLayer(item, exportProgress):
    if not item and rt.classOf(item) != rt.Base_LayerBase_Layer:
        exportProgress.close()
        sdkdialog.showMessage("ERROR: No Layer Selected")
        return
    if isValidaFormat(item.name):
        exportProgress.close()
        sdkdialog.showMessage("ERRORs: LODs export run on wrong layer")
        return

    layerName = item.name
    print("PROCESSING layer {0}".format(layerName))
    layer = rt.LayerManager.getLayerFromName(layerName)
    layer.current = True
    setLayerVisibility(layer,True)
    layerChilds = rt.refs.dependents(layer.layerAsRefTarg)
    for i in range(1, layer.getNumChildren() + 1):
        rt.append(layerChilds, layer.getChild(i))
    exportPath = getLayerPath(layerName)
    if not exportPath:
        exportProgress.close()
        sdkdialog.showMessage("ERROR: no path selected for {0}\nShift + Click on export command to set folder path".format(layerName))
        return
    lodsValue = []
    for n in layerChilds:
        cls = rt.classOf(n)
        if cls == rt.MixinInterface and isValidaFormat(n.name):
            layerNodes = []
            n.nodes(pymxs.mxsreference(layerNodes))
            for lNode in layerNodes:
                if isValidaFormat(lNode.name):
                    lodsValue.append(ExportLODinstance(exportPath, lNode, exportProgress))
        elif (cls == rt.Editable_Poly or cls == rt.Dummy) and isValidaFormat(n.name):
            lodsValue.append(ExportLODinstance(exportPath, n, exportProgress))
    flatFilePath = os.path.join(exportPath, layerName)
    deleteInvalidGLTF(flatFilePath)
    xmlFilePath = flatFilePath + ".xml"

    if os.path.exists(xmlFilePath) and lodsValue:
        modifyXML(xmlFilePath, lodsValue)

def run():
    explorer = rt.SceneExplorerManager.GetActiveExplorer()
    items = explorer.SelectedItems()
    condition = lambda x: rt.classOf(x) == rt.Base_LayerBase_Layer
    validItems = [x for x in items if condition(x)]
    if validItems:
        if items.count == 1 and rt.keyboard.shiftPressed:
            layerName = items[0].name
            window = MainWindow(layerName=layerName)
            MaxPlus.AttachQWidgetToMax(window)
            window.show()
        else:
            exportProgress = utils.QExportProgress(steps=len(validItems))
            MaxPlus.AttachQWidgetToMax(exportProgress)
            exportProgress.show()
            for i in items:
                exportLODsLayer(i, exportProgress)