import os
import uuid
from xml.dom import minidom
import xml.etree.ElementTree as ET
from io import BytesIO

import BabylonPYMXS
from maxsdk import perforce as sdkperforce
from maxsdk import sceneUtils, userprop, utility
import qtUtils
from pymxs import runtime as rt

reload(userprop)
reload(utility)
reload(sceneUtils)
reload(qtUtils)

def addExportPathToObjects(objects):
    selected = objects
    maxPath = rt.maxFilePath
    initialDir = os.path.join((maxPath), "Export")
    expPath = rt.getSavePath(caption="Export Path", initialDir=initialDir) # open dialog to get path
    selected = sceneUtils.getAllRoots(selected)
    passAll = False
    if(expPath != None):
        for s in selected:   
            exportPath = os.path.join(expPath,s.name + ".gltf")
            exportPath = rt.pathConfig.convertPathToRelativeTo(exportPath,rt.maxFilePath)
            oldPath = rt.getUserProp(s,"Exp")
            if(oldPath == None or passAll == True):        
                userprop.setUserProp(s,"Exp", exportPath)
            else:  
                popup = qtUtils.popup_Yes_YesToAll_No_NoToAll(
                    title="Add export path to {0}".format(s.name),
                    text="{0} already has an export path. Do you want to override it ?"
                " \nChange path from :\n  {1} \n to :\n  {2}".format(s.name,oldPath,exportPath)
                )        
                if(popup == 0):
                    break
                if(popup == 2):
                    passAll = True 
                if(popup >= 2):
                    userprop.setUserProp(s,"Exp", exportPath)            
                        

def removeExportPathToObjects(objects):
    selected = sceneUtils.getAllRoots(objects)
    passAll = False
    for s in selected:        
        oldPath = rt.getUserProp(s,"Exp")
        if(oldPath == None) or (passAll == True):        
            userprop.removeUserProp(s, "Exp")
        else: 
            popup = qtUtils.popup_Yes_YesToAll_No_NoToAll(
                title="Remove export path from {0}".format(s.name), 
                text="Are you sure you want to remove the export path of {0} ?"
            "\nCurrent path is :\n{1}".format(s.name,oldPath)
            )
            if(popup == 0):
                break
            if(popup == 2):
                passAll = True 
            if(popup >= 2):
                userprop.removeUserProp(s, "Exp")        


def exportObjects(objects):
    log = ""
    for o in objects:      
        log += exportObject(o) # export and get the log back and add it to queue of errors

def exportObject(obj):
    # create log string to return after export in case something goes wrong
    log = "" 
    # get export path from user property
    exportPath = getExportPath(obj)
    if(exportPath == None or exportPath == ""):
        log = "Can't export {0}. No export path found.".format(obj.name)
        return log
    assetFilePath = rt.pathConfig.removePathTopParent(exportPath)
    assetFilePath = os.path.join(rt.maxFilePath, assetFilePath)
    # find all gizmos
    gizmos = sceneUtils.getDescendants(obj)
    gizmos = sceneUtils.filterGizmos(gizmos)
    # convert them to AsoboGizmos if needed
    gizmos = sceneUtils.convertGizmosToAsoboGizmos(gizmos)    
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
    if(lodLevel != None): # if we have lods we can update the xml file
        metaPath = fromLODPathToMetadataPath(assetFilePath)
        if(not updateSingleMetadataLODValue(metaPath,lodLevel,lodValue)):
            log += "Can't update XML file of {0} please regenerate it.\n".format(obj.name)

    # find hierarchy and select it in the scene
    hierarchyToExport = sceneUtils.getDescendants(toExport)
    rt.select(hierarchyToExport)
    # run babylon exporter
    param = BabylonPYMXS.BabylonParameters(assetFilePath, "gltf")
    param.exportOnlySelected = True
    param.exportMaterials = True
    param.scaleFactor = 1
    BabylonPYMXS.runBabylonExporter(param)
    # perforce
    sdkperforce.P4edit(assetFilePath + ".bin")
    sdkperforce.P4edit(assetFilePath + ".gltf")
    # delete copy after export
    rt.delete(hierarchyToExport)
    return log

def getFlattenFlag(obj):
    flag = rt.getUserProp(obj,"flightsim_flatten")
    return flag

def getExportPath(obj):
    path = userprop.getUserProp(obj,"Exp")
    return path

def markForDeleteObsoleteGLTF(flatName):
    targetGLTFFileName = flatName + ".gltf"
    targetBINFileName = flatName + ".bin"
    if os.path.exists(targetGLTFFileName) or os.path.exists(targetBINFileName):
        print "found {0} to remove".format(flatName)
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
    assetFilePath = rt.pathConfig.removePathTopParent(exportPath)
    assetFilePath = os.path.join(rt.maxFilePath, assetFilePath)
    return assetFilePath

# given a "..._LOD[0-9].gltf" or .bin path returns the xml path
def getMetadataPath(obj):
    exportPath = getExportPath(obj)
    if(exportPath == None):
        return None
    assetFilePath = rt.pathConfig.removePathTopParent(exportPath)
    assetFilePath = os.path.join(rt.maxFilePath, assetFilePath)
    flatPath = os.path.splitext(assetFilePath)[0]
    flatPath = utility.removeLODSuffix(flatPath)
    return flatPath + ".xml"

def createLODMetadata(xmlPath, objects):
    if(not xmlPath):
        print "Can't create metadata path. Check your object's export path"
        return False
    if(os.path.exists(xmlPath)):
        print xmlPath + " already exists. Clearing and rewriting LOD Values"        
        return updateLODMetadata(xmlPath, objects)
    objectToSort = sceneUtils.filterLODLevel(objects,"[0-9]+")
    modelInfo = ET.Element("ModelInfo")    
    modelInfo.set("guid", "{" + str(uuid.uuid4()) + "}")
    modelInfo.set("version", "1.1")
    lodsElement = ET.SubElement(modelInfo,"LODS")
    sortedObjects = sceneUtils.sortObjectsByLODLevels(objectToSort)
    for obj in sortedObjects:
        lod = ET.SubElement(lodsElement,"LOD")
        lod.set("minSize", str(sceneUtils.getLODValue(obj)))
    if(len(objectToSort) != 0):
        flatName = os.path.splitext(xmlPath)[0]
        print flatName
        markForDeleteObsoleteGLTF(flatName)
    writeXML(xmlPath,modelInfo)
    return True

# TODO : NEEDS TO BE MERGE WITH CREATE LOD METADATA ABOVE

def updateLODMetadata(xmlPath, objects):
    if(not os.path.exists(xmlPath)):
        print "This file doesn't exist. can't update it : " + xmlPath
        return False
    xml = open(xmlPath, "r")
    root = ET.fromstring(xml.read())
    lods = root.find("LODS")
    if(lods is not None):
        root.remove(lods)
    lodObjects = sceneUtils.filterLODLevel(objects,"[0-9]+")
    sortedObjects = sceneUtils.sortObjectsByLODLevels(lodObjects)
    if(len(sortedObjects) != 0):
        lods = ET.SubElement(root,"LODS")
        lods.clear()
        for obj in sortedObjects:
            lod = ET.SubElement(lods,"LOD")
            lod.set("minSize", str(sceneUtils.getLODValue(obj)))  
    
    writeXML(xmlPath,root)
    if(len(sortedObjects) != 0): # if there is LODs in this metadata then check for flatname.gltf .bin and mark them for delete
        flatName = os.path.splitext(xmlPath)[0]
        markForDeleteObsoleteGLTF(flatName)
    return True
    

def updateSingleMetadataLODValue(xmlPath,lodLevel,lodValue):
    if(not os.path.exists(xmlPath)):
        print "This file doesn't exist. can't update it : " + xmlPath
        return False
    xml = open(xmlPath, "r")
    root = ET.fromstring(xml.read())
    lods = root.find("LODS")
    if (lods is None) or (len(lods) < lodLevel + 1): # if no LODS in the xml or current lodLevel is beyond what's already setup
        print xmlPath + " file is missing data. Please regenerate it."
        return False
    lods[lodLevel].set("minSize", str(lodValue))    
    writeXML(xmlPath,root)
    return True

def writeXML(xmlPath, root):    
    output = ET.tostring(root) 
    sdkperforce.P4edit(xmlPath)    
    xmlstr = minidom.parseString(output).toprettyxml( encoding='utf-8',indent="   ")
    dom_string = os.linesep.join([s for s in xmlstr.splitlines() if s.strip()])
    myfile = open(xmlPath , "w+")
    myfile.write(dom_string)

def executeMaxScriptDependencies():
    flattenFile = os.path.join(os.path.dirname(__file__), "flatten.ms")
    flattenFunction = open(flattenFile, "r").read()
    rt.execute(flattenFunction)

# add createMesh() function in Max. TODO needs to be done in python
executeMaxScriptDependencies()