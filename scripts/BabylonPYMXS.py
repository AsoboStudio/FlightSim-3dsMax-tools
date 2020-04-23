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
    scaleFactor = 1
    writeTextures = False
    rt.execute('Assembly = dotNetClass "System.Reflection.Assembly"')
    dllPath = os.path.join(rt.symbolicPaths.getPathValue(1),"bin\\assemblies\\Max2Babylon.dll")
    rt.execute('Assembly.loadfrom "{0}"'.format(dllPath))
    animationExportType = rt.execute('(dotnetclass "BabylonExport.Entities.AnimationExportType").Export')
    enableASBAnimationRetargeting = False
    overwriteTextures = False
    exportHiddenObjects = False
    exportMaterials = False
    exportOnlySelected = False
    optimizeAnimations = False
    animgroupExportNonAnimated = True
    usePreExportProcess = False
    applyPreprocessToScene = False
    mergeContainersAndXRef = False
    flattenScene = False
    bakeAnimationType = rt.execute('(dotnetclass "Max2Babylon.BakeAnimationType").DoNotBakeAnimation')
    removeNamespaces = True
    removeLodPrefix = True

    def __init__(self, outputPath, outputFormat):
        self.outputPath = outputPath
        self.outputFormat = outputFormat


def runBabylonExporter(babylonParameters, log=False):
    if isinstance(babylonParameters, BabylonParameters):
        print "New Export started at " + str(datetime.datetime.now())
        rt.execute('Assembly = dotNetClass "System.Reflection.Assembly"')
        dllPath = os.path.join(rt.symbolicPaths.getPathValue(1),"bin\\assemblies\\Max2Babylon.dll")
        rt.execute('Assembly.loadfrom "{0}"'.format(dllPath))
        rt.execute('maxScriptManager = dotNetObject "Max2Babylon.MaxScriptManager"')
        rt.execute('param = maxScriptManager.InitParameters "c:\\default.gltf"')
        rt.param.outputPath = babylonParameters.outputPath
        rt.param.outputFormat = babylonParameters.outputFormat
        rt.param.textureFolder = babylonParameters.textureFolder
        rt.param.scaleFactor = babylonParameters.scaleFactor
        rt.param.writeTextures = babylonParameters.writeTextures
        rt.param.animationExportType = babylonParameters.animationExportType
        rt.param.enableASBAnimationRetargeting = babylonParameters.enableASBAnimationRetargeting
        rt.param.overwriteTextures = babylonParameters.overwriteTextures
        rt.param.exportHiddenObjects = babylonParameters.exportHiddenObjects
        rt.param.exportMaterials = babylonParameters.exportMaterials
        rt.param.exportOnlySelected = babylonParameters.exportOnlySelected
        rt.param.optimizeAnimations = babylonParameters.optimizeAnimations
        rt.param.animgroupExportNonAnimated = babylonParameters.animgroupExportNonAnimated
        rt.param.usePreExportProcess = babylonParameters.usePreExportProcess
        rt.param.applyPreprocessToScene = babylonParameters.applyPreprocessToScene
        rt.param.mergeContainersAndXRef = babylonParameters.mergeContainersAndXRef
        rt.param.flattenScene = babylonParameters.flattenScene
        rt.param.bakeAnimationType = babylonParameters.bakeAnimationType
        rt.param.removeNamespaces = babylonParameters.removeNamespaces
        rt.param.removeLodPrefix = babylonParameters.removeLodPrefix
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
