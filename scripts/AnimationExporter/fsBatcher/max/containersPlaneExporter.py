import sys
import os
import logging

home = os.path.expanduser("~")
logFilePath = os.path.join(home, "cockpitBatcher.log")

#to create log file
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

logging.basicConfig(level=logging.DEBUG, filename=logFilePath, filemode="a+",
                    format="%(asctime)-15s %(levelname)-8s %(message)s")

# to debug in max listener
logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

modulePath = os.path.dirname(__file__)
sdk = None

pathIndex = modulePath.rfind("scripts")
if pathIndex != -1:
    sdk = os.path.join(modulePath[0:pathIndex], "scripts")
if modulePath not in sys.path:
    sys.path.append(modulePath)
if sdk not in sys.path:
    sys.path.append(sdk)

import pymxs
import xml.etree.ElementTree as ET
import babylonExporter

reload(babylonExporter)
import re

rt = pymxs.runtime

reportFile = r"OBJECT/PLANES/report.xml"
reportFile = os.path.join(rt.pathConfig.getCurrentProjectFolder(), reportFile)


class MaxProject():
    filePath = None
    exportItemList = None

    def __init__(self):
        self.filePath = None
        self.exportItemList = []


class ExportItem():
    gltfPath = None
    texturePath = None
    layers = None

    def __init__(self):
        self.gltfPath = None
        self.texturePath = None
        self.layers = []


def setParentVisibility(layer, visible):
    parent = layer.getParent()
    if parent:
        parent.ishidden = not visible
        setParentVisibility(parent, visible)


def setLayerVisibility(layer, visible, includeChild=True):
    layer.ishidden = not visible
    if includeChild:
        for i in range(1, layer.getNumChildren()+1):
            child = layer.getChild(i)
            setLayerVisibility(child, visible, includeChild)


def hideAllLayers():
    count = rt.LayerManager.count
    for i in range(0, count):
        layer = rt.LayerManager.GetLayer(i)
        setLayerVisibility(layer, False, True)


def showLayers(layers):
    for l in layers:
        maxLayer = rt.LayerManager.getLayerFromName(l)
        if maxLayer:
            setParentVisibility(maxLayer, True)
            setLayerVisibility(maxLayer, True, True)
        else:
            logging.info("cannot find a layer named {0}".format(l))


def getMaxFileWithContainersFromReport():
    projectFolderPath = rt.pathConfig.getCurrentProjectFolder()
    containersFiles = []
    if projectFolderPath and os.path.exists(reportFile):
        tree = ET.parse(reportFile)
        root = tree.getroot()
        for child in root.getchildren():
            containersFiles.append(str(child.text).replace("[KITTYHAWK_DATA]", projectFolderPath))
    return containersFiles


def updateContainerID():
    for o in rt.objects:
        if rt.Containers.IsContainerNode(o):
            match = re.search(r"_\d+", o.name)
            if not match:
                rt.setUserProp(o, "babylonjs_ContainerID", 1)
                o.name = o.name + "_ID_1"

def updateContainerID2():
    for o in rt.objects:
        if rt.Containers.IsContainerNode(o):
            match = re.search(r"_ID_\d+", o.name)
            if match:
                o.name = str(o.name).replace("_ID_","_")


def mergeXref():
    records = []
    for k in range(1, rt.objXRefMgr.recordCount + 1):
        rec = rt.objXRefMgr.GetRecord(k)
        records.append(rec)
    for rec in records:
        rt.objXRefMgr.MergeRecordIntoScene(rec)


def mergeContainer():
    containers = []
    for o in rt.objects:
        if rt.Containers.IsContainerNode(o):
            containers.append(o)
    for c in containers:
        c.MakeUnique()


def batchUpdateID():
    for cFile in getMaxFileWithContainersFromReport():
        os.system('cmd /c "p4 edit -c default {0}"'.format(cFile))
        rt.loadMaxFile(cFile, quiet=True)
        logging.info("Opening ... {0}".format(cFile))
        updateContainerID()
        updateContainerID2()
        rt.saveMaxFile(cFile, quiet=True)


def batchExport():
    for cFile in getMaxFileWithContainersFromReport():
        os.system('cmd /c "p4 edit -c default {0}"'.format(cFile))
        rt.loadMaxFile(cFile, quiet=True)
        logging.info("_______________________________")
        logging.info("Opening ... {0}".format(cFile))
        exportItemsString = rt.getUserProp(rt.rootNode, "babylonjs_ExportItemList")
        if not exportItemsString:
            logging.info("Multi Export items not found")
            continue

        maxProject = MaxProject()
        maxProject.filePath = cFile
        exportItems = exportItemsString.split(";")

        for i in range(len(exportItems)):
            exportItem = ExportItem()
            itemString = rt.getUserProp(rt.rootNode, exportItems[i])
            if not itemString:
                logging.info("No properties valid for {0}".format(exportItems[i]))
                continue
            itemProps = itemString.split(";")
            gltfPath = itemProps[1]
            if not os.path.isabs(gltfPath):
                fileDir = os.path.dirname(cFile)
                gltfPath = os.path.join(fileDir, gltfPath)
            exportItem.gltfPath = gltfPath
            exportItem.texturePath = itemProps[2]
            layersString = itemProps[3]
            if not layersString:
                logging.info("No layer found for export item {0}".format(itemString))
                continue
            exportItem.layers = layersString.split("~")
            maxProject.exportItemList.append(exportItem)

        logging.info("found {0} items to export".format(str(len(maxProject.exportItemList))))
        for item in maxProject.exportItemList:
            if isinstance(item, ExportItem):
                logging.info("exporting {0}".format(str(item.layers)))
                hideAllLayers()
                showLayers(layers=item.layers)
                params = babylonExporter.BabylonParameters(item.gltfPath, outputFormat="gltf")
                params.removeLodPrefix = True
                params.removeNamespaces = True
                params.textureFolder = item.texturePath
                params.animgroupExportNonAnimated = True
                params.optimizeAnimations = False
                params.exportMaterials = True
                params.usePreExportProcess = True
                params.mergeContainersAndXRef = True
                params.applyPreprocessToScene = True
                babylonExporter.runBabylonExporter(params, False)
                head, tail = os.path.split(item.gltfPath)
                changelistName = "default"
                if tail:
                    changelistName = os.path.splitext(tail)[0]
                os.system('cmd /c "p4 add -c default {0}"'.format(item.gltfPath))
                os.system('cmd /c "p4 edit -c default {0}"'.format(item.gltfPath))
    logging.info("Operation Complete")


# import maxsdk.debug
# batchUpdateID()
batchExport()
