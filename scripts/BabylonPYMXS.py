'''
Wrapper to easaly run babylon form pymxs
'''
import os
import pymxs
import datetime
import time
rt = pymxs.runtime


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
    removeLodPrefix = None #True

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
    "babylonjs_animgroupexportnonanimated": True
}

def getPropertyDefaultValue(property):
    if (propertyToDefault.has_key(property)):
        return propertyToDefault[property]
    else:
        return None

def __overwriteIfSet(overwriteable, overwriter):
    return overwriteable if overwriter is None else overwriter

def runBabylonExporter(babylonParameters, log=False):
    if isinstance(babylonParameters, BabylonParameters):
        print "New Export started at " + str(datetime.datetime.now())
        rt.execute('Assembly = dotNetClass "System.Reflection.Assembly"')
        dllPath = os.path.join(rt.symbolicPaths.getPathValue(1),"bin\\assemblies\\Max2Babylon.dll")
        rt.execute('Assembly.loadfrom "{0}"'.format(dllPath))
        rt.execute('maxScriptManager = dotNetObject "Max2Babylon.MaxScriptManager"')
        rt.execute('param = maxScriptManager.InitParameters "c:\\default.gltf"')
        rt.param.outputPath = __overwriteIfSet(rt.param.outputPath,babylonParameters.outputPath)
        rt.param.outputFormat = __overwriteIfSet(rt.param.outputFormat,babylonParameters.outputFormat)
        rt.param.textureFolder = __overwriteIfSet(rt.param.textureFolder,babylonParameters.textureFolder)
        rt.param.scaleFactor = __overwriteIfSet(rt.param.scaleFactor,babylonParameters.scaleFactor)
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
        rt.param.removeLodPrefix = __overwriteIfSet(rt.param.removeLodPrefix,babylonParameters.removeLodPrefix)
        rt.maxScriptManager.Export(rt.param, log)
        print "exporting..."
        while isExporterProcessing():
            pass
        print "Exported Complete in {0}".format(babylonParameters.outputPath)


def isExporterProcessing():
    try:
        vGlobal = rt.globalVars.get(rt.name("BabylonExporterStatus"))
        if vGlobal == "Unavailable":
            return True
        return False
    except:
        return False
