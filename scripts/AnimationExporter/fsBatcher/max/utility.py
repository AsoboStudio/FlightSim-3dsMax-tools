import pymxs
import xml.etree.ElementTree as ET
import os
import re
import json
import glob
import datetime
rt = pymxs.runtime


class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, MaxProject):
            return {
                "items": obj.exportItemList,
                "filePath": obj.filePath
            }
        if isinstance(obj, ExportItem):
            return {
                "gltfPath": obj.gltfPath,
                "texturePath": obj.texturePath,
                "layers": obj.layers
            }
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)


class MaxProject():
    filePath = None
    exportItemList = []


class ExportItem():
    gltfPath = None
    texturePath = None
    layers = []


def sceneHasContainer():
    for node in rt.rootNode.children:
        if rt.Containers.IsContainerNode(node):
            return True
    return False


def report(maxFiles):
    REPORTFOLDER = ""
    data = []
    for m in maxFiles:
        print "loading ..." + m
        rt.loadMaxFile(m, quiet=True)
        if not sceneHasContainer():
            continue
        else:
            print m + " has container"
        exportItemsString = rt.getUserProp(rt.rootNode, "babylonjs_ExportItemList")
        if not exportItemsString:
            continue

        maxProject = MaxProject()
        maxProject.filePath = m
        exportItems = exportItemsString.split(";")

        for i in range(len(exportItems)):
            exportItem = ExportItem()
            itemString = rt.getUserProp(rt.rootNode, exportItems[i])
            if not itemString:
                continue
            itemProps = itemString.split(";")
            exportItem.gltfPath = itemProps[1]
            exportItem.texturePath = itemProps[2]
            layersString = itemProps[3]
            if not layersString:
                continue
            exportItem.layers = layersString.split("~")
            maxProject.exportItemList.append(exportItem)

        data.append(maxProject)

    reportFile = os.path.join(REPORTFOLDER, "layersReport.json")
    with open(reportFile, 'w') as outfile:
        json.dump(data, outfile, indent=4, cls=CustomEncoder)

    print "report done"


def getMaxFiles(folder):
    maxFiles = []
    for x in os.walk(folder):
        if "_OLD" in x[0]:
            continue
        if "_LIBRARY" in x[0]:
            continue
        for y in glob.glob(os.path.join(x[0], '*.max')):
            maxFiles.append(y)
    return maxFiles


def getSceneWithContainer():
    for m in getMaxFiles():
        rt.loadMaxFile(m, quiet=True)
        if sceneHasContainer():
            print m

    print "evaluation done"


def getMaxFileWithContainersFromReport():
    reportFile = r"d:/KittyHawk/ASSETS/KittyHawk_Data/OBJECT/PLANES/report.xml"
    projectFolderPath = rt.pathConfig.getCurrentProjectFolder()
    containersFiles = []
    if projectFolderPath and os.path.exists(reportFile):
        tree = ET.parse(reportFile)
        root = tree.getroot()
        for child in root.getchildren():
            containersFiles.append(str(child.text).replace("[KITTYHAWK_DATA]", projectFolderPath))
    return containersFiles

def updateIDAndExport():
    for cFile in getMaxFileWithContainersFromReport():
        os.system('cmd /c "p4 edit -c default {0}"'.format(cFile))
        rt.loadMaxFile(cFile, quiet=True)
        for o in rt.objects:
            if rt.Containers.IsContainerNode(o):
                match = re.search(r"_ID_\d+", o.name)
                if not match:
                    rt.setUserProp(o, "babylonjs_ContainerID", 1)
                    o.name = o.name + "_ID_1"
        rt.saveMaxFile(cFile, quiet=True)
