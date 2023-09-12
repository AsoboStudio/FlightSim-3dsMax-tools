"""
This module contains the function to setup and export groups of object and preset ( as defined in presetUtils )
"""
import sys
import os
import time
import uuid
import xml.etree.ElementTree as ET
from io import BytesIO
from xml.dom import minidom
from maxsdk.globals import *
from BabylonPYMXS import *


import MultiExporter.constants as const
import MultiExporter.presetUtils as presetUtils

from maxsdk import layer
from maxsdk import perforce as sdkperforce
from maxsdk import qtUtils, sceneUtils, userprop, utility
from pymxs import runtime as rt


log = ""

def addExportPathToObjects(objects, forcedPath=None, prompt=True):
    """Find the root of each object and ask the user for a path. Store this path in the user property of the roots

    \nin: list(pymxs.MXSWrapperBase)
    """
    selected = objects
    maxPath = rt.maxFilePath
    initialDir = os.path.join((maxPath), "Export")
    if (not os.path.exists(initialDir)):
        initialDir = maxPath
    # open dialog to get path
    if forcedPath == None:
        expPath = rt.getSavePath(caption="Export Path", initialDir=initialDir)
    else:
        expPath = forcedPath
    selected = sceneUtils.getAllRoots(selected)
    passAll = False
    if prompt == False:
        passAll = True
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


def removeExportPathToObjects(objects, prompt=True):
    """Remove the export path stored in the user property of the objects. If prompt is false, automatically accepts everything and don't open any message box.

    \nin: 
    list(pymxs.MXSWrapperBase)
    prompt = boolean 
    """
    selected = sceneUtils.getAllRoots(objects)
    passAll = False
    if prompt == False:
        passAll = True
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
    """Transform a selection of object into a collection of bundle ready to be exported.

    \nin: 
          objects= list(pymxs.MXSWrapperBase)
          optionPreset= presetUtils.OptionPresetObjects
    """
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
        originalHierarchy = sceneUtils.getDescendants(obj)
        gizmos = sceneUtils.filterGizmos(originalHierarchy)

        # convert them to AsoboGizmos if needed
        try:
            gizmos = sceneUtils.convertGizmosToAsoboGizmos(gizmos)
        except Exception as error:
            lineLog = "{0}, {1} will not export".format(error, obj.name)
            log += "\n"
            log += lineLog
            print(lineLog)
            continue

        sceneUtils.cleanupGizmosValues(gizmos)
        toExport = obj
        lodLevel = sceneUtils.getLODLevel(obj)
        lodValue = sceneUtils.getLODValue(obj)
        
        if(lodLevel != None):  # if we have lods we can update the xml file
            metaPath = fromLODPathToMetadataPath(assetFilePath)
            lodLog = updateSingleMetadataLODValue(metaPath, lodLevel, lodValue)
            if(lodLog != ""):
                log += "\nSomething went wrong while updating the XML file of {0}, the XML will not be updated but the export will still be performed : {1}\n".format(
                    obj.name, lodLog)
                print(log)



        # run babylon exporter
        param = BabylonParameters(assetFilePath, "gltf")

        if optionPreset is not None:
            param = applyOptionPresetToBabylonParam(optionPreset, param)
            print("Overwritten param")
        

        # param.exportOnlySelected = True
        param.exportHiddenObjects = True

        try:
            relativeTextureFolder = param.textureFolder[1:] if (param.textureFolder[:1] == "\\") else param.textureFolder
            param.textureFolder = utility.convertRelativePathToAbsolute(relativeTextureFolder, rt.pathConfig.getCurrentProjectFolder())
        except Exception as error:
            print ("Error resolving texturePath")
            print( error )

        bundle = (assetFilePath, toExport, param)
        bundles.append(bundle)
    return bundles

def exportObjects(objects, optionPreset=None,prompt=True):
    """Export the objects using the option preset if specified.

    \nin: 
          objects= list(pymxs.MXSWrapperBase)
          optionPreset= presetUtils.OptionPresetObject
    """
    global log
    log = ""
    bundles = collectObjectBundlesForExport(objects, optionPreset)

    noProcessBundles = [x for x in bundles if not x[2].usePreExportProcess]
    preProcessBundles = [x for x in bundles if x[2].usePreExportProcess]

    hasPreProcess = len(preProcessBundles) > 0
    if hasPreProcess:
        if(prompt):
            if qtUtils.popup_Yes_No(title="Your Max File needs to be saved.",
                                text="Your max file needs to be saved before exporting. Do you want to continue the export and save your scene ?"
                                ) :
                rt.saveMaxFile(os.path.join(rt.maxFilePath,rt.maxFileName))
            else:
                qtUtils.popup(title="Export has been canceled",
                            text="The export has been canceled")
                return
        else:
            rt.saveMaxFile(os.path.join(rt.maxFilePath,rt.maxFileName))

    for bundle in noProcessBundles:
        try:
            # objects = sceneUtils.getDescendants(bundle[1])
            # bundle = (bundle[0],objects,bundle[2])
            
            exportBundleObjects(bundle)
        except Exception as error:
            log += "{0} :\n".format(os.path.split(bundle[0])[1])
            log += str(error)
            continue
    
    if hasPreProcess:
        applyPreprScene = False
        rt.holdMaxFile()
        success = runPreExportProcess()
        if success:
            for sec in bundles:
                applyPreprScene = applyPreprScene or sec[2].applyPreprocessToScene

            for bundle in preProcessBundles:
                try:
                    exportBundleObjects(bundle)
                except Exception as error:
                    log += "{0} :\n".format(os.path.split(bundle[0])[1])
                    log += str(error)
                    continue
            if not applyPreprScene:
                rt.fetchMaxFile(quiet = True)
        else:
            rt.fetchMaxFile(quiet = True)
    
    if log != "" and prompt == True:
        qtUtils.popup_scroll(title="Some export failed", text=log)

    # for bundle in bundles:
    #     try:
    #         objects = bundle[1]
    #         rt.delete(bundle[1])
    #         del objects
    #     except Exception as error:
    #         log += "{0} :\n".format(os.path.split(bundle[0])[1])
    #         log += str(error)
    #         continue

    if log != "" and prompt == True:
        qtUtils.popup_scroll(title="Some export failed", text=log)
    

def exportBundleObjects(exportBundles):
    """Export a bundle.
    
    \nin:
          exportBundles= tuple(assetFilePath, list(pymxs.MXSWrapperBase), babylonParam)
    """
        # perforce
    assetFilePath = exportBundles[0]
    objects = exportBundles[1]
    babylonParam = exportBundles[2]
    babylonParam.exportNode = objects
    runBabylonExporter(babylonParam)
    # perforce
    extensionLessPath = os.path.splitext(assetFilePath)[0]
    sdkperforce.P4edit(extensionLessPath + ".bin")
    sdkperforce.P4edit(extensionLessPath + ".gltf")



def getExportPath(obj):
    path = userprop.getUserProp(obj, const.PROP_EXPORT_PATH)
    return path


def markForDeleteObsoleteGLTF(flatName):
    """Given the path of an exported LOD without the LOD suffix, revert or delete the obsolete gltf.     
    When creating example_LOD0.gtlf you need to delete example.gltf that use to be the exported asset

    \nin: flatName= str
    """
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
    """Given the path of an exported LOD returns the path to the XML

    \nin: path= str
    """
    flatPath = os.path.splitext(path)[0]
    flatPath = utility.removeLODSuffix(flatPath)
    return flatPath + ".xml"


def getAbsoluteExportPath(obj):
    """Returns the absolute export path stored in the object user property.

    \nin: obj= pymxs.MXSWrapperBase
    """
    exportPath = getExportPath(obj)
    if(exportPath == None):
        return None
    assetFilePath = utility.convertRelativePathToAbsolute(
        exportPath, rt.pathConfig.getCurrentProjectFolder())
    return assetFilePath
# given a "..._LOD[0-9].gltf" or .bin path returns the xml path


def getMetadataPath(obj):
    """Returns the XML path extrapolated from the export path stored in the object user property.

    \nin: 
          obj= pymxs.MXSWrapperBase
    \nout:
          xmlPath= str
    """
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
    """Create a single xml file for the list of objects. Objects are sorted based on their LOD level and their values are written in the xmlFile

    \nin: 
          xmlPath= str
          objects= list(pymxs.MXSWrapperBase)
    \nout:
          log= str
    """
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

def createLODMetadataForSimObject(xmlPath, objects):
    """Create a single xml file for the list of objects. Objects are sorted based on their LOD level and their values are written in the xmlFile

    \nin: 
          xmlPath= str
          objects= list(pymxs.MXSWrapperBase)
    \nout:
          log= str
    """
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
            lod.set("MinSize", str(lodValue))
            lod.set("ModelFile", str(obj.name))
        # if we have LODs in the file we check if there is an old object before the lods and delete it
        markForDeleteObsoleteGLTF(flatName)
    xmlLog = writeXML(xmlPath, modelInfo)
    successLog = "\nSuccesfully {0} XML file for {1}. It contains {2} LODs".format(methodUsed, categoryName, lodCount)
    log += successLog if xmlLog == "" else xmlLog
    return log


def updateSingleMetadataLODValue(xmlPath, lodLevel, lodValue):
    """Update a single value in the xml file depending on the LodLevel. If the lodLevel is above the number of LODs already in the XML the update will fail.

    \nin: 
          xmlPath= str
          lodLevel= int
          lodValue= int
    \nout:
          log= str
    """
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
    lods[lodLevel].set("MinSize", str(lodValue))
    log += writeXML(xmlPath, root)
    return log


def writeXML(xmlPath, root):
    """Write a xml.etree.ElementTree to a xml file.

    \nin:
          xmlPath= str
          root= xml.etree.ElementTree.Element
    \nout:
          log= str
    """
    output = ET.tostring(root)
    xmlstr = minidom.parseString(output).toprettyxml(
        encoding='utf-8', indent="   ").decode("utf-8")
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


