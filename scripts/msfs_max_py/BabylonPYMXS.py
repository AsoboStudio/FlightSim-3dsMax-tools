'''
Wrapper to easily run babylon form pymxs
'''
import os
from pymxs import runtime as rt
import datetime
import time
import warnings
import logging
from maxsdk.logger import SignalHandler
from maxsdk.globals import *
from maxsdk import qtUtils

handler = SignalHandler()
babylonLogger = logging.getLogger("BabylonLogger")
babylonLogger.setLevel(level=logging.INFO)
babylonLogger.addHandler(handler)

class BabylonParameters:
    exportNode = None
    exportLayers = None
    outputPath = None
    outputFormat = None
    textureFolder = None
    scaleFactor = None #1
    writeTextures = None #False
    animationExportType = None #rt.execute('(dotnetclass "BabylonExport.Entities.AnimationExportType").Export')
    enableASBAnimationRetargeting = None  #True
    enableASBUniqueID = None #True
    overwriteTextures = None #False
    exportHiddenObjects = None #False
    exportMaterials = None #False
    exportOnlySelected = None #False
    usePreExportProcess = None #False
    applyPreprocessToScene = None #False
    mergeContainersAndXRef = None #False
    flattenGroups = None #False
    #flattenScene = None #False
    bakeAnimationType = None # rt.execute('(dotnetclass "Max2Babylon.BakeAnimationType").DoNotBakeAnimation')
    removeNamespaces = None #True
    removeLodPrefix = None  #True
    keepInstances = None  #False
    tangentSpaceConvention = None  #0

    exportAsSubmodel = None #False


    mergeAOWithMR = None #False



    def __init__(self, outputPath, outputFormat):
        self.outputPath = outputPath
        self.outputFormat = outputFormat

propertyToDefault = {
    "babylonjs_txtCompression" : 100,
    "babylonjs_txtScaleFactor" : 1,
    "flightsim_tangent_space_convention": 0,
    "babylonjs_export_animations_type": "Export",
    "babylonjs_export_materials": True,
    "flightsim_removelodprefix": True,
    "flightsim_removenamespaces": True,
    "babylonjs_animgroupexportnonanimated": True,
    "babylonjs_bakeAnimationsType": 0,  # after this the values are just usual type default
    "babylonjs_autosave": False,
    "babylonjs_exporthidden" : False,
    "babylonjs_preproces": False,
    "babylonjs_mergecontainersandxref" : False,
    "babylonjs_overwritetextures": False,    
    "babylonjs_applyPreprocess": False,
    "flightsim_flattenGroups": False,    
    "babylonjs_writetextures": False,
    "babylonjs_mergeAOwithMR": False,

    "flightsim_keepInstances": False,    
    #"babylonjs_flattenScene": False,
    "babylonjs_asb_animation_retargeting": True,
    "flightsim_asb_unique_id": True,
    "babylonjs_onlySelected": False,

    "flightsim_exportAsSubmodel": False
}

babylonParameters = [
    "babylonjs_autosave",   
    "babylonjs_exporthidden",
    "flightsim_removelodprefix",
    "flightsim_removenamespaces",
    #"babylonjs_flattenScene",
    "babylonjs_export_materials",
    "flightsim_tangent_space_convention",
    "babylonjs_animgroupexportnonanimated",
    "babylonjs_preproces",
    "babylonjs_mergecontainersandxref",
    "babylonjs_applyPreprocess",
    "flightsim_flattenGroups",
    "babylonjs_bakeAnimationsType",
    "babylonjs_asb_animation_retargeting",
    "flightsim_asb_unique_id",
    "babylonjs_txtCompression",
    "babylonjs_writetextures",
    "babylonjs_overwritetextures",
    "babylonjs_mergeAOwithMR",

    "flightsim_keepInstances",
    "babylonjs_export_animations_type",
    "babylonjs_txtScaleFactor",
    "textureFolderPathProperty",
    "babylonjs_onlySelected",
    "flightsim_exportAsSubmodel"
]
  
def applyOptionPresetToBabylonParam(optionPreset, babylonParam):
    """
    Apply the parameters of an OptionPresetObject onto a BabylonParam

    \nin: 
    optionPreset : OptionPresetObject 
    babylonParam : BabylonParameters
    \nout: 
    BabylonParameters (modified)
    """
    options = optionPreset.get()
    properties = options[1]
    babylonParam.writeTextures = getBabylonParamFromDict(properties,"babylonjs_writetextures")
    babylonParam.overwriteTextures =  getBabylonParamFromDict(properties,"babylonjs_overwritetextures")
    babylonParam.animationExportType = castStrToDotNetEnum("BabylonExport.Entities.AnimationExportType",getBabylonParamFromDict(properties,"babylonjs_export_animations_type"))
    babylonParam.enableASBAnimationRetargeting = getBabylonParamFromDict(properties,"babylonjs_asb_animation_retargeting")
    babylonParam.enableASBUniqueID = getBabylonParamFromDict(properties,"flightsim_asb_unique_id")
    babylonParam.exportHiddenObjects = getBabylonParamFromDict(properties,"babylonjs_exporthidden")
    babylonParam.exportMaterials = getBabylonParamFromDict(properties,"babylonjs_export_materials")
    babylonParam.usePreExportProcess = getBabylonParamFromDict(properties,"babylonjs_preproces") 
    babylonParam.applyPreprocessToScene = getBabylonParamFromDict(properties,"babylonjs_applyPreprocess") 
    babylonParam.mergeContainersAndXRef = getBabylonParamFromDict(properties,"babylonjs_mergecontainersandxref") 
    #babylonParam.flattenScene = getBabylonParamFromDict(properties,"babylonjs_flattenScene") 
    babylonParam.bakeAnimationType = castIntToDotNetEnum("Max2Babylon.BakeAnimationType",getBabylonParamFromDict(properties,"babylonjs_bakeAnimationsType")) # rt.execute('(dotnetclass "Max2Babylon.BakeAnimationType").DoNotBakeAnimation')
    babylonParam.removeNamespaces = getBabylonParamFromDict(properties,"flightsim_removenamespaces")
    babylonParam.removeLodPrefix = getBabylonParamFromDict(properties,"flightsim_removelodprefix")
    babylonParam.keepInstances = getBabylonParamFromDict(properties,"flightsim_keepInstances")
    babylonParam.tangentSpaceConvention = getBabylonParamFromDict(properties,"flightsim_tangent_space_convention")
    babylonParam.mergeAOWithMR = getBabylonParamFromDict(properties,"babylonjs_mergeAOwithMR")

    babylonParam.textureFolder = getBabylonParamFromDict(properties,"textureFolderPathProperty")
    babylonParam.flattenGroups = getBabylonParamFromDict(properties,"flightsim_flattenGroups")
    babylonParam.exportOnlySelected = getBabylonParamFromDict(properties,"babylonjs_onlySelected")
    babylonParam.exportAsSubmodel = getBabylonParamFromDict(properties, "flightsim_exportAsSubmodel")

    return babylonParam

def getBabylonParamFromDict(_dict, _prop):
    if (_prop in _dict):
        return _dict[_prop]
    else:
        if _prop in propertyToDefault:
            return propertyToDefault[_prop]
    return None
    

def castStrToDotNetEnum(dotnetenum, string):
    '''
    Find enum value of key string and returns it
    \nin : 
    dotnetenum= str("dotnetenum") 
    string= str  
    \nout : 
    rt.dotNetObject 
    '''
    arg = string.replace(" ","")
    command = '(dotnetclass "{0}").{1}'.format(dotnetenum,arg)
    return rt.execute(command)


def castIntToDotNetEnum(dotnetenum, index):
    '''
    Cast python int to dotnetobject enum
    \nin : 
    dotnetenum= str("dotnetenum") 
    index= int 
    \nout : 
    rt.dotNetObject 
    '''
    animExpType = rt.getPropNames(rt.execute('(dotnetclass "{0}")'.format(dotnetenum)))
    prop = rt.name(animExpType[index])
    command = '(dotnetclass "{0}").{1}'.format(dotnetenum, prop)
    return rt.execute(command)


def getPropertyDefaultValue(property):
    if ( property in propertyToDefault ):
        return propertyToDefault[property]
    else:
        return None

def __overwriteIfSet(overwriteable, overwriter):    
    """
    Returns overwriteable if overwriter is set, overwriteable otherwise
    \nin: 
    overwriteable=object 
    overwriter=object
    \nout: 
    overwriter if not None else overwriteable
    """    
    return overwriteable if overwriter is None else overwriter
    

def initializeBabylonExport():
    rt.execute('Assembly = dotNetClass "System.Reflection.Assembly"')
    dllPath = os.path.join(rt.symbolicPaths.getPathValue(1),"bin\\assemblies\\Max2Babylon.dll")
    rt.execute('Assembly.loadfrom "{0}"'.format(dllPath))
    rt.execute('maxScriptManager = dotNetObject "Max2Babylon.MaxScriptManager"')   
    rt.execute('param = maxScriptManager.InitParameters "c:\\default.gltf"')
    rt.execute('param.logLevel = (dotNetClass "Max2Babylon.LogLevel").WARNING')
    rt.maxScriptManager.InitializeGuidTable()

def setRTParameters(babylonParameters):
    if isinstance(babylonParameters, BabylonParameters):
        rt.execute('param = maxScriptManager.InitParameters "c:\\default.gltf"')
        rt.execute('param.logLevel = (dotNetClass "Max2Babylon.LogLevel").WARNING')
        rt.execute('logger = dotNetObject "Max2Babylon.MaxScriptLogger" false')
        rt.execute('logger.logLevel = (dotNetClass "Max2Babylon.LogLevel").WARNING')
        if (babylonParameters.exportNode):
            rt.param.exportNode =  rt.param.GetNodeByHandle(babylonParameters.exportNode.inode.handle)
        if(babylonParameters.exportLayers):
            rt.param.exportLayers = rt.param.NameToIILayer(babylonParameters.exportLayers)      
        rt.param.outputPath = __overwriteIfSet(rt.param.outputPath, babylonParameters.outputPath)        
        rt.param.outputFormat = __overwriteIfSet(rt.param.outputFormat, babylonParameters.outputFormat)        
        rt.param.textureFolder = __overwriteIfSet(rt.param.textureFolder, babylonParameters.textureFolder)        
        rt.param.scaleFactor = __overwriteIfSet(rt.param.scaleFactor, babylonParameters.scaleFactor)        
        rt.param.writeTextures = __overwriteIfSet(rt.param.writeTextures,babylonParameters.writeTextures)
        rt.param.animationExportType = __overwriteIfSet(rt.param.animationExportType,babylonParameters.animationExportType)
        rt.param.enableASBAnimationRetargeting = __overwriteIfSet(rt.param.enableASBAnimationRetargeting, babylonParameters.enableASBAnimationRetargeting)
        rt.param.enableASBUniqueID = __overwriteIfSet(rt.param.enableASBUniqueID,babylonParameters.enableASBUniqueID)
        rt.param.overwriteTextures = __overwriteIfSet(rt.param.overwriteTextures,babylonParameters.overwriteTextures)
        rt.param.exportHiddenObjects = __overwriteIfSet(rt.param.exportHiddenObjects,babylonParameters.exportHiddenObjects)
        rt.param.exportMaterials = __overwriteIfSet(rt.param.exportMaterials, babylonParameters.exportMaterials)
        rt.param.exportOnlySelected = __overwriteIfSet(rt.param.exportOnlySelected,babylonParameters.exportOnlySelected)
        rt.param.usePreExportProcess = __overwriteIfSet(rt.param.usePreExportProcess,babylonParameters.usePreExportProcess)
        rt.param.applyPreprocessToScene = __overwriteIfSet(rt.param.applyPreprocessToScene,babylonParameters.applyPreprocessToScene)
        rt.param.flattenGroups = __overwriteIfSet(rt.param.flattenGroups,babylonParameters.flattenGroups)
        rt.param.mergeContainersAndXRef = __overwriteIfSet(rt.param.mergeContainersAndXRef,babylonParameters.mergeContainersAndXRef)
        #rt.param.flattenScene = __overwriteIfSet(rt.param.flattenScene,babylonParameters.flattenScene)
        rt.param.bakeAnimationType = __overwriteIfSet(rt.param.bakeAnimationType,babylonParameters.bakeAnimationType)
        rt.param.removeNamespaces = __overwriteIfSet(rt.param.removeNamespaces,babylonParameters.removeNamespaces)
        rt.param.removeLodPrefix = __overwriteIfSet(rt.param.removeLodPrefix, babylonParameters.removeLodPrefix)
        rt.param.keepInstances = __overwriteIfSet(rt.param.keepInstances, babylonParameters.keepInstances)
        rt.param.tangentSpaceConvention = __overwriteIfSet(rt.param.tangentSpaceConvention, babylonParameters.tangentSpaceConvention)
        rt.param.exportOnlySelected = __overwriteIfSet(rt.param.exportOnlySelected, babylonParameters.exportOnlySelected)
        rt.param.exportAsSubmodel = __overwriteIfSet(rt.param.exportAsSubmodel, babylonParameters.exportAsSubmodel)

        rt.param.mergeAOWithMR = __overwriteIfSet(rt.param.mergeAOWithMR, babylonParameters.mergeAOWithMR)



def _runBabylonAction(action, successMsg):
    timeStart = time.time()
    criticalError = None
    try:
        action()
        for msg in rt.logger.GetLogEntries():
            if msg.progress: 
                continue
            if msg.level.toString() == "ERROR":
                babylonLogger.error ("{0}\n".format(msg.message))
            if msg.level.toString() == "WARNING":
                babylonLogger.warning("{0}\n".format(msg.message))
            if msg.level.toString() == "MESSAGE":
                babylonLogger.info("{0}\n".format(msg.message))
    except Exception as criticalError:
        babylonLogger.critical("{0}\n".format(criticalError))
        qtUtils.popup(text=str(criticalError), title="An error as occured during the export process")
        return False

    delta = round(time.time() - timeStart,3)
    babylonLogger.info("Opertation complete in {0}".format(delta))
    babylonLogger.info(successMsg)
    return True
       
        


def runBabylonExporter(babylonParameters):
    babylonLogger.info("New Export started at " + str(datetime.datetime.now()))
    setRTParameters(babylonParameters)
    action = lambda : rt.maxScriptManager.Export(rt.param, rt.logger)
    successMsg = "Export path is {0}".format(babylonParameters.outputPath)
    return _runBabylonAction(action,successMsg)
        
def runPreExportProcess():
    babylonLogger.info("New Pre-Export started at " + str(datetime.datetime.now()))
    rt.execute('logger = dotNetObject "Max2Babylon.MaxScriptLogger" false')
    rt.execute('logger.logLevel = (dotNetClass "Max2Babylon.LogLevel").WARNING')
    rt.execute('preExportProcess = dotNetObject "Max2Babylon.PreExport.PreExportProcess" param logger')
    action = lambda: rt.preExportProcess.ApplyPreExport()
    successMsg = "Pre Export completed"
    return _runBabylonAction(action,successMsg)

def isExporterProcessing():
    try:
        vGlobal = rt.globalVars.get(rt.name("BabylonExporterStatus"))
        if vGlobal == "Unavailable":
            return True
        return False
    except:
        return False

