'''
Wrapper to easily run babylon form pymxs
'''
import os
from pymxs import runtime as rt
import datetime
import time

class BabylonParameters:
    outputPath = None
    outputFormat = None
    textureFolder = None
    scaleFactor = None #1
    writeTextures = None #False
    animationExportType = None #rt.execute('(dotnetclass "BabylonExport.Entities.AnimationExportType").Export')
    enableASBAnimationRetargeting = None #False
    overwriteTextures = None #False
    exportHiddenObjects = None #False
    exportMaterials = None #False
    exportOnlySelected = None #False
    optimizeAnimations = None #False
    animgroupExportNonAnimated = None #True
    usePreExportProcess = None #False
    applyPreprocessToScene = None #False
    mergeContainersAndXRef = None #False
    flattenScene = None #False
    bakeAnimationType = None # rt.execute('(dotnetclass "Max2Babylon.BakeAnimationType").DoNotBakeAnimation')
    removeNamespaces = None #True
    removeLodPrefix = None  #True
    keepInstances = None  #False
    tangentSpaceConvention = None  #0
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
    "babylonjs_donotoptimizeanimations": True,
    "babylonjs_animgroupexportnonanimated": True,
    "babylonjs_bakeAnimationsType": 0,  # after this the values are just usual type default
    "babylonjs_autosave": False,
    "babylonjs_exporthidden" : False,
    "babylonjs_preproces": False,
    "babylonjs_mergecontainersandxref" : False,
    "babylonjs_overwritetextures": False,    
    "babylonjs_applyPreprocess": False,    
    "babylonjs_writetextures": False,
    "babylonjs_mergeAOwithMR": False,
    "flightsim_keepInstances": False,    
    "babylonjs_flattenScene": False,
    "babylonjs_asb_animation_retargeting": False
}

babylonParameters = [
    "babylonjs_autosave",   
    "babylonjs_exporthidden",
    "flightsim_removelodprefix",
    "flightsim_removenamespaces",
    "babylonjs_flattenScene",
    "babylonjs_export_materials",
    "flightsim_tangent_space_convention",
    "babylonjs_donotoptimizeanimations",
    "babylonjs_animgroupexportnonanimated",
    "babylonjs_preproces",
    "babylonjs_mergecontainersandxref",
    "babylonjs_applyPreprocess",
    "babylonjs_bakeAnimationsType",
    "babylonjs_asb_animation_retargeting",
    "babylonjs_txtCompression",
    "babylonjs_writetextures",
    "babylonjs_overwritetextures",
    "babylonjs_mergeAOwithMR",
    "flightsim_keepInstances",
    "babylonjs_export_animations_type",
    "babylonjs_txtScaleFactor"
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
    babylonParam.writeTextures = properties["babylonjs_writetextures"]
    babylonParam.overwriteTextures =  properties["babylonjs_overwritetextures"]
    babylonParam.animationExportType = castStrToDotNetEnum("BabylonExport.Entities.AnimationExportType",properties["babylonjs_export_animations_type"])
    babylonParam.enableASBAnimationRetargeting = properties["babylonjs_asb_animation_retargeting"]
    babylonParam.exportHiddenObjects = properties["babylonjs_exporthidden"]
    babylonParam.exportMaterials = properties["babylonjs_export_materials"]
    babylonParam.optimizeAnimations = properties["babylonjs_donotoptimizeanimations"]
    babylonParam.animgroupExportNonAnimated = properties["babylonjs_animgroupexportnonanimated"]
    babylonParam.usePreExportProcess = properties["babylonjs_preproces"] 
    babylonParam.applyPreprocessToScene = properties["babylonjs_applyPreprocess"] 
    babylonParam.mergeContainersAndXRef = properties["babylonjs_mergecontainersandxref"] 
    babylonParam.flattenScene = properties["babylonjs_flattenScene"] 
    babylonParam.bakeAnimationType = castIntToDotNetEnum("Max2Babylon.BakeAnimationType",properties["babylonjs_bakeAnimationsType"]) # rt.execute('(dotnetclass "Max2Babylon.BakeAnimationType").DoNotBakeAnimation')
    babylonParam.removeNamespaces = properties["flightsim_removenamespaces"]
    babylonParam.removeLodPrefix = properties["flightsim_removelodprefix"]
    babylonParam.keepInstances = properties["flightsim_keepInstances"]
    babylonParam.tangentSpaceConvention = properties["flightsim_tangent_space_convention"]
    babylonParam.mergeAOWithMR = properties["babylonjs_mergeAOwithMR"]
    return babylonParam

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
    if (propertyToDefault.has_key(property)):
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
    rt.execute('logger = dotNetObject "Max2Babylon.MaxScriptLogger" false')
    rt.execute('param = maxScriptManager.InitParameters "c:\\default.gltf"')
    rt.maxScriptManager.InitializeGuidTable()


def runBabylonExporter(babylonParameters, log=False):
    if isinstance(babylonParameters, BabylonParameters):
        print("New Export started at " + str(datetime.datetime.now()))
        rt.execute('param = maxScriptManager.InitParameters "c:\\default.gltf"')
        rt.execute('logger = dotNetObject "Max2Babylon.MaxScriptLogger" false')
        rt.execute('logger.logLevel = (dotNetClass "Max2Babylon.LogLevel").WARNING')
        rt.param.outputPath = __overwriteIfSet(rt.param.outputPath, babylonParameters.outputPath)        
        rt.param.outputFormat = __overwriteIfSet(rt.param.outputFormat, babylonParameters.outputFormat)        
        rt.param.textureFolder = __overwriteIfSet(rt.param.textureFolder, babylonParameters.textureFolder)        
        rt.param.scaleFactor = __overwriteIfSet(rt.param.scaleFactor, babylonParameters.scaleFactor)        
        rt.param.writeTextures = __overwriteIfSet(rt.param.writeTextures,babylonParameters.writeTextures)
        rt.param.animationExportType = __overwriteIfSet(rt.param.animationExportType,babylonParameters.animationExportType)
        rt.param.enableASBAnimationRetargeting = __overwriteIfSet(rt.param.enableASBAnimationRetargeting,babylonParameters.enableASBAnimationRetargeting)
        rt.param.overwriteTextures = __overwriteIfSet(rt.param.overwriteTextures,babylonParameters.overwriteTextures)
        rt.param.exportHiddenObjects = __overwriteIfSet(rt.param.exportHiddenObjects,babylonParameters.exportHiddenObjects)
        rt.param.exportMaterials = __overwriteIfSet(rt.param.exportMaterials, babylonParameters.exportMaterials)
        rt.param.exportOnlySelected = __overwriteIfSet(rt.param.exportOnlySelected,babylonParameters.exportOnlySelected)
        rt.param.optimizeAnimations = __overwriteIfSet(rt.param.optimizeAnimations,babylonParameters.optimizeAnimations)
        rt.param.animgroupExportNonAnimated = __overwriteIfSet(rt.param.animgroupExportNonAnimated,babylonParameters.animgroupExportNonAnimated)
        rt.param.usePreExportProcess = __overwriteIfSet(rt.param.usePreExportProcess,babylonParameters.usePreExportProcess)
        rt.param.applyPreprocessToScene = __overwriteIfSet(rt.param.applyPreprocessToScene,babylonParameters.applyPreprocessToScene)
        rt.param.mergeContainersAndXRef = __overwriteIfSet(rt.param.mergeContainersAndXRef,babylonParameters.mergeContainersAndXRef)
        rt.param.flattenScene = __overwriteIfSet(rt.param.flattenScene,babylonParameters.flattenScene)
        rt.param.bakeAnimationType = __overwriteIfSet(rt.param.bakeAnimationType,babylonParameters.bakeAnimationType)
        rt.param.removeNamespaces = __overwriteIfSet(rt.param.removeNamespaces,babylonParameters.removeNamespaces)
        rt.param.removeLodPrefix = __overwriteIfSet(rt.param.removeLodPrefix, babylonParameters.removeLodPrefix)
        rt.param.keepInstances = __overwriteIfSet(rt.param.keepInstances, babylonParameters.keepInstances)
        rt.param.tangentSpaceConvention = __overwriteIfSet(rt.param.tangentSpaceConvention, babylonParameters.tangentSpaceConvention)
        rt.param.mergeAOWithMR = __overwriteIfSet(rt.param.mergeAOWithMR, babylonParameters.mergeAOWithMR)

        timeStart = time.time()
        rt.maxScriptManager.Export(rt.param, rt.logger)
               
        for msg in rt.logger.GetLogEntries():
            if msg.progress == False:
                print(msg.message)

        delta = round(time.time() - timeStart,3)
        print("Exported Complete in {0}s at {1}".format(delta,babylonParameters.outputPath))

def runPreExportProcess():
    rt.execute('preExportProcess = dotNetObject "Max2Babylon.PreExport.PreExportProcess" param')
    rt.preExportProcess.ApplyPreExport()


def revertScene():
    rt.preExportProcess.RevertScene()


def isExporterProcessing():
    try:
        vGlobal = rt.globalVars.get(rt.name("BabylonExporterStatus"))
        if vGlobal == "Unavailable":
            return True
        return False
    except:
        return False
