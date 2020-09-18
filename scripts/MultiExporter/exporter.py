"""
This module contains the function to setup and export groups of object and preset ( as defined in presetUtils )
"""

import os
import time
import uuid
import xml.etree.ElementTree as ET
from io import BytesIO
from xml.dom import minidom

import BabylonPYMXS
import MultiExporter.constants as const
import MultiExporter.presetUtils
from maxsdk import layer
from maxsdk import perforce as sdkperforce
from maxsdk import qtUtils, sceneUtils, userprop, utility
from pymxs import runtime as rt

log = ""

def addExportPathToObjects(objects):
    selected = objects
    print(len(selected))
    maxPath = rt.maxFilePath
    initialDir = os.path.join((maxPath), "Export")
    if (not os.path.exists(initialDir)):
        initialDir = maxPath
    # open dialog to get path
    expPath = rt.getSavePath(caption="Export Path", initialDir=initialDir)
    selected = sceneUtils.getAllRoots(selected)
    passAll = False
    if(expPath != None):
        for s in selected:
            exportPath = os.path.join(expPath, s.name + ".gltf")
            exportPath = rt.pathConfig.convertPathToRelativeTo(
                exportPath, rt.pathConfig.getCurrentProjectFolder())
            print(exportPath)
            oldPath = rt.getUserProp(s, const.PROP_EXPORT_PATH)
            if(oldPath == None or passAll == True):
                userprop.setUserProp(s, const.PROP_EXPORT_PATH, exportPath)
            else:
                popup = qtUtils.popup_Yes_YesToAll_No_NoToAll(
                    title="Add export path to {0}".format(s.name),
                    text="{0} already has an export path. Do you want to override it ?"
                    " \nChange path from :\n  {1} \n to :\n  {2}".format(
                        s.name, oldPath, exportPath)
                )
                if(popup == 0):
                    break
                if(popup == 2):
                    passAll = True
                if(popup >= 2):
                    userprop.setUserProp(s, const.PROP_EXPORT_PATH, exportPath)


def removeExportPathToObjects(objects):
    selected = sceneUtils.getAllRoots(objects)
    passAll = False
    for s in selected:
        oldPath = rt.getUserProp(s, const.PROP_EXPORT_PATH)
        if(oldPath == None) or (passAll == True):
            userprop.removeUserProp(s, const.PROP_EXPORT_PATH)
        else:
            popup = qtUtils.popup_Yes_YesToAll_No_NoToAll(
                title="Remove export path from {0}".format(s.name),
                text="Are you sure you want to remove the export path of {0} ?"
                "\nCurrent path is :\n{1}".format(s.name, oldPath)
            )
            if(popup == 0):
                break
            if(popup == 2):
                passAll = True
            if(popup >= 2):
                userprop.removeUserProp(s, const.PROP_EXPORT_PATH)


def collectObjectBundlesForExport(objects, optionPreset=None):
    bundles = []
    global log

    for obj in objects:
        # create log string to return after export in case something goes wrong
        # get export path from user property
        exportPath = getExportPath(obj)
        if(exportPath == None or exportPath == ""):
            log += "\nERROR : Couldn't export {0}. No export path found.".format(obj.name)
            continue
        assetFilePath = utility.convertRelativePathToAbsolute(
            exportPath, rt.pathConfig.getCurrentProjectFolder())
        # find all gizmos
        gizmos = sceneUtils.getDescendants(obj)
        gizmos = sceneUtils.filterGizmos(gizmos)

        # convert them to AsoboGizmos if needed
        try:
            gizmos = sceneUtils.convertGizmosToAsoboGizmos(gizmos)
        except Exception as error:
            lineLog = "{0}, {1} will not export".format(error, obj.name)
            log += "\n"
            log += lineLog
            print(lineLog)
            continue
        # remove negative values
        sceneUtils.cleanupGizmosValues(gizmos)
        # copy hierarchy or flatten hierarchy to export
        if(getFlattenFlag(obj)):
            toExport = sceneUtils.flattenMesh(obj)
        else:
            toExport = sceneUtils.copyHierarchy(obj)
        # reset matrix
        toExport.transform = rt.matrix3(1)
        # find object lod param
        lodLevel = sceneUtils.getLODLevel(obj)
        lodValue = sceneUtils.getLODValue(obj)
        if(lodLevel != None):  # if we have lods we can update the xml file
            metaPath = fromLODPathToMetadataPath(assetFilePath)
            lodLog = updateSingleMetadataLODValue(metaPath, lodLevel, lodValue)
            if(lodLog != ""):
                log += "\nSomething went wrong while updating the XML file of {0}, the XML will not be updated but the export will still be performed : {1}\n".format(
                    obj.name, lodLog)
                print(log)
        # find hierarchy and select it in the scene
        hierarchyToExport = sceneUtils.getDescendants(toExport)

        # run babylon exporter
        param = BabylonPYMXS.BabylonParameters(assetFilePath, "gltf")

        if optionPreset is not None:
            param = BabylonPYMXS.applyOptionPresetToBabylonParam(optionPreset, param)
            print("Overwritten param")


        param.exportOnlySelected = True
        param.exportHiddenObjects = True

        bundle = (assetFilePath, hierarchyToExport, param)
        bundles.append(bundle)
    return bundles

def exportObjects(objects, optionPreset=None):
    global log
    log = ""
    bundles = collectObjectBundlesForExport(objects, optionPreset)
    for bundle in bundles:
        try:
            exportBundleObjects(bundle)
        except Exception as error:
            log += str(error)     
            continue

    for bundle in bundles:
        try:
            objects = bundle[1]
            rt.delete(bundle[1])
            del objects
        except Exception as error:
            log += str(error)
            continue

    if log != "":
        qtUtils.popup(title="Some export failed", text=log)
    

def exportBundleObjects(exportBundles):
    """bundle(assetFilePath, objects, babylonParam)
    """
        # perforce
    assetFilePath = exportBundles[0]
    objects = exportBundles[1]
    babylonParam = exportBundles[2]
    rt.clearSelection()
    rt.select(objects)
    BabylonPYMXS.runBabylonExporter(babylonParam)
    # perforce
    extensionLessPath = os.path.splitext(assetFilePath)[0]
    sdkperforce.P4edit(extensionLessPath + ".bin")
    sdkperforce.P4edit(extensionLessPath + ".gltf")

def exportPreset(preset, optionPreset=None):
    log = ""
    layers = []
    for lay in preset.layerNames:
        layers.append(rt.layerManager.getLayerFromName(lay))

    layer.disableAll()
    layer.enableThese(layers)

    exportPath = preset.path
    assetFilePath = utility.convertRelativePathToAbsolute(
        exportPath, rt.pathConfig.getCurrentProjectFolder())
    if not os.path.isdir(os.path.split(assetFilePath)[0]):
        log += "\n\"{}\" export folder cannot be found or is invalid.\n".format(
            preset.name)
    else:
        param = BabylonPYMXS.BabylonParameters(assetFilePath, "gltf")
        if optionPreset is not None:
            param = BabylonPYMXS.applyOptionPresetToBabylonParam(optionPreset,param)
        param.exportOnlySelected = False
        param.scaleFactor = 1
        
        BabylonPYMXS.runBabylonExporter(param)
        # perforce
        extensionLessPath = os.path.splitext(assetFilePath)[0]
        sdkperforce.P4edit(extensionLessPath + ".bin")
        sdkperforce.P4edit(extensionLessPath + ".gltf")
    return log


def collectBundlesForExport(presetsAndOptions):
    bundles = []
    for preset, optionPreset in presetsAndOptions:
        layers = []
        for lay in preset.layerNames:
            layers.append(rt.layerManager.getLayerFromName(lay))
        
        exportPath = preset.path
        assetFilePath = utility.convertRelativePathToAbsolute(exportPath, rt.pathConfig.getCurrentProjectFolder())

        param = BabylonPYMXS.BabylonParameters(assetFilePath, "gltf")
        if optionPreset is not None:
            param = BabylonPYMXS.applyOptionPresetToBabylonParam(optionPreset,param)
        param.exportOnlySelected = False
        param.scaleFactor = 1
        
        bundle = (assetFilePath, layers, param)
        bundles.append(bundle)
    return bundles

def exportPresetsAndOptions(presetsAndOptions):
    global log
    log = ""
    bundles = collectBundlesForExport(presetsAndOptions)
    noProcessBundles = [x for x in bundles if not x[2].usePreExportProcess]
    preProcessBundles = [x for x in bundles if x[2].usePreExportProcess]
    hasPreProcess = len(preProcessBundles) > 0
    if hasPreProcess:
        if qtUtils.popup_Yes_No(title="Your Max File needs to be saved.",
                            text="Your max file needs to be saved before exporting. Do you want to continue the export and save your scene ?"
                            ) :
            rt.saveMaxFile(rt.maxFileName)
        else:
            qtUtils.popup(title="Export has been canceled",
                        text="The export has been canceled")
            return
        
    for bundle in noProcessBundles:
        try:
            exportBundleLayers(bundle)
        except Exception as error:
            log += str(error)
            continue
    
    if hasPreProcess:        
        BabylonPYMXS.runPreExportProcess()
        for bundle in preProcessBundles:
            try:
                exportBundleLayers(bundle)
            except Exception as error:
                log += str(error)
                continue
        BabylonPYMXS.revertScene()
    
    if log != "":
        qtUtils.popup(title="Some export failed", text=log)

    
def exportBundleLayers(exportBundles):
    """
    bundle(assetFilePath, layers, babylonParam)
    """
    assetFilePath = exportBundles[0]
    layers = exportBundles[1]
    babylonParam = exportBundles[2]
    layer.disableAll()
    layer.enableThese(layers)

    BabylonPYMXS.runBabylonExporter(babylonParam)
    # perforce
    extensionLessPath = os.path.splitext(assetFilePath)[0]
    sdkperforce.P4edit(extensionLessPath + ".bin")
    sdkperforce.P4edit(extensionLessPath + ".gltf")

def getFlattenFlag(obj):
    flag = rt.getUserProp(obj, const.PROP_FLATTEN)
    return flag


def getExportPath(obj):
    path = userprop.getUserProp(obj, const.PROP_EXPORT_PATH)
    return path


def markForDeleteObsoleteGLTF(flatName):
    targetGLTFFileName = flatName + ".gltf"
    targetBINFileName = flatName + ".bin"
    if os.path.exists(targetGLTFFileName) or os.path.exists(targetBINFileName):
        print("found {0} to remove".format(flatName))
        sdkperforce.P4revert(targetBINFileName)
        sdkperforce.P4revert(targetGLTFFileName)
        sdkperforce.P4delete(targetGLTFFileName)
        sdkperforce.P4delete(targetBINFileName)

        
# given a "..._LOD[0-9].gltf" or .bin path returns the xml path
def fromLODPathToMetadataPath(path):
    flatPath = os.path.splitext(path)[0]
    flatPath = utility.removeLODSuffix(flatPath)
    return flatPath + ".xml"


def getAbsoluteExportPath(obj):
    exportPath = getExportPath(obj)
    if(exportPath == None):
        return None
    assetFilePath = utility.convertRelativePathToAbsolute(
        exportPath, rt.pathConfig.getCurrentProjectFolder())
    return assetFilePath
# given a "..._LOD[0-9].gltf" or .bin path returns the xml path


def getMetadataPath(obj):
    exportPath = getAbsoluteExportPath(obj)
    if (exportPath == None):
        return None
    flatPath = os.path.splitext(exportPath)[0]
    flatPath = utility.removeLODSuffix(flatPath)
    return flatPath + ".xml"
# for a given set of objects setup as LODs, sort them by lodLevels _LOD0 1 2
# write a single xml file representing the aformentionned set of LODs
# keep the guid if the xml already exist, create a new one otherwise


def createLODMetadata(xmlPath, objects):
    log = ""
    if (not os.path.isdir(os.path.split(xmlPath)[0])):
        return "\nERROR : The output path for the xml is invalid, you probably need to save your max file and redo the export path."
    if(not xmlPath):
        return "\nERROR : Can't create metadata path for {0} Check your object's export path".format(objects[0].name)
    if(os.path.exists(xmlPath)):  # if xml already exist parse it
        xml = open(xmlPath, "r")
        modelInfo = ET.fromstring(xml.read())
        methodUsed = "updated"
    else:  # otherwise create it
        modelInfo = ET.Element("ModelInfo")
        # assigned new guid
        modelInfo.set("guid", "{" + str(uuid.uuid4()) + "}")
        modelInfo.set("version", "1.1")
        methodUsed = "created"
    lods = modelInfo.find("LODS")  # find the registered LODs
    if(lods is not None):  # if found delete them
        modelInfo.remove(lods)
    objectToSort = sceneUtils.filterLODLevel(objects, "[0-9]+")
    sortedObjects = sceneUtils.sortObjectsByLODLevels(
        objectToSort)  # sort object by lod levels
    lodCount = len(objectToSort)
    flatName = os.path.splitext(xmlPath)[0]
    categoryName = os.path.split(flatName)[1]
    if (len(sortedObjects) != 0):  # if we found LODs register them
        if (sceneUtils.getLODLevel(sortedObjects[0]) != 0):
            log += "\nERROR : Can't create metadata if {0} doesn't have a LOD0.".format(
                sortedObjects[0].name)
            return log
        lodsElement = ET.SubElement(modelInfo, "LODS")
        for obj in sortedObjects:
            lod = ET.SubElement(lodsElement, "LOD")
            lodValue = sceneUtils.getLODValue(obj)
            if(lodValue == None):  # if no valid LOD Value found pick a default value
                lodValue = sceneUtils.getDefaultLODValue(
                    sceneUtils.getLODLevel(obj))
                log += "\nWARNING : Couldn't find lod value on {0} it will use the default value {1}".format(
                    obj.name, lodValue)
            lod.set("minSize", str(lodValue))
        # if we have LODs in the file we check if there is an old object before the lods and delete it
        markForDeleteObsoleteGLTF(flatName)
    xmlLog = writeXML(xmlPath, modelInfo)
    successLog = "\nSuccesfully {0} XML file for {1}. It contains {2} LODs".format(methodUsed, categoryName, lodCount)
    log += successLog if xmlLog == "" else xmlLog
    return log


def updateSingleMetadataLODValue(xmlPath, lodLevel, lodValue):
    log = ""
    if(not os.path.exists(xmlPath)):
        return "\nERROR : This file doesn't exist. can't update it"
    xml = open(xmlPath, "r")
    root = ET.fromstring(xml.read())
    lods = root.find("LODS")
    # if no LODS in the xml or the current lodLevel is beyond what's already setup
    if (lods is None) or (len(lods) < lodLevel + 1):
        return "\nERROR : XML file is missing data. Please regenerate it from the LOD View."
    if(lodValue == None):  # if no valid LOD Value found pick a default value
        lodValue = sceneUtils.getDefaultLODValue(lodLevel)
        log += "\nWARNING : Couldn't find lod value for LOD{0}. The default value {1} will be used".format(
            lodLevel, lodValue)
    lods[lodLevel].set("minSize", str(lodValue))
    log += writeXML(xmlPath, root)
    return log


def writeXML(xmlPath, root):
    output = ET.tostring(root)
    xmlstr = minidom.parseString(output).toprettyxml(
        encoding='utf-8', indent="   ")
    dom_string = os.linesep.join([s for s in xmlstr.splitlines() if s.strip()])
    exists = os.path.exists(xmlPath)
    sdkperforce.P4edit(xmlPath)
    try:
        myfile = open(xmlPath, "w+")
        myfile.write(dom_string)
        if(not exists):
            sdkperforce.P4edit(xmlPath)
        return ""
    except IOError:       
        return "\nPermission denied. The XML file is not writable. Please make sure your perforce environment is the same as your 3dsMax Project.\nIf you're not using perforce, make the xml file writable."


def executeMaxScriptDependencies():
    flattenFile = os.path.join(os.path.dirname(__file__), "flatten.ms")
    flattenFunction = open(flattenFile, "r").read()
    rt.execute(flattenFunction)


# add createMesh() function in Max. TODO needs to be done in python
executeMaxScriptDependencies()

