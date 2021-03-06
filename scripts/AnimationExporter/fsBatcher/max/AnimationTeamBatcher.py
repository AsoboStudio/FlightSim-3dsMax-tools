import pymxs
from pymxs import runtime as rt
import BabylonPYMXS
import re
import maxsdk.perforce as sdkperforce
import os

exportedType = None
bakeAnimation = None


def exportLodPreset(exportPath, mName, lod):
    exportName = rt.trimleft(mName, "pr_")
    exportFolder = exportPath + "\\"
    modelFolder = exportFolder + "model." + exportName
    animationFolder = exportFolder + "animation"
    param = BabylonPYMXS.BabylonParameters(r"c:\\default", r"gltf")

    if exportedType == "Animation":
        outputPath = animationFolder
        rt.makedir(outputPath, all=True)
        param.outputPath = outputPath + "\\" + exportName + ".gltf"
        param.animationExportType = rt.execute('(dotnetclass "BabylonExport.Entities.AnimationExportType").ExportOnly')
        param.outputPath = outputPath
        param.exportMaterials = False
    elif exportedType == "Model":
        outputPath = modelFolder
        rt.makedir(outputPath, all=True)
        outputPath = outputPath + "\\" + exportName + "_LOD0" + lod + ".gltf"
        param.animationExportType = rt.execute('(dotnetclass "BabylonExport.Entities.AnimationExportType").NotExport')
        param.outputPath = outputPath
        param.exportMaterials = True
    elif exportedType == "All":
        outputPath = modelFolder
        rt.makedir(outputPath, all=True)
        outputPath = outputPath + "\\" + exportName + "_LOD0" + lod + ".gltf"
        param.animationExportType = rt.execute('(dotnetclass "BabylonExport.Entities.AnimationExportType").Export')
        param.outputPath = outputPath
        param.exportMaterials = True
    param.mergeContainersAndXRef = False
    param.writeTextures = False
    param.overwriteTextures = False
    param.usePreExportProcess = False

    if bakeAnimation:
        param.bakeAnimationType = rt.execute('(dotnetclass "Max2Babylon.BakeAnimationType").BakeAllAnimations')
    else:
        param.bakeAnimationType = rt.execute('(dotnetclass "Max2Babylon.BakeAnimationType").DoNotBakeAnimation')
    param.optimizeAnimations = True
    param.animgroupExportNonAnimated = True
    param.enableASBAnimationRetargeting = True
    param.removeNamespaces = True
    param.removeLodPrefix = True
    # param.keepInstance = True
    try:
        BabylonPYMXS.runBabylonExporter(param, False)

    except:
        print("ERROR exporting lod {1} of {0}".format(lod, mName))


def hideNodes(nodes):
    for n in nodes:
        n.ishidden = True


def showLodInLayer(layerObject, lodValue):
    layerNodes = []
    layerObject.nodes(pymxs.mxsreference(layerNodes))
    for n in layerNodes:
        n.ishidden = True
        if n.name[1] == lodValue:
            n.ishidden = False


def exportScene(exportPath, bakeAnim, exportType):
    for k in range(1, rt.objXRefMgr.recordCount):
        rec = rt.objXRefMgr.GetRecord(k)
        rt.objXRefMgr.MergeRecordIntoScene(rec)

    global bakeAnimation
    bakeAnimation = bakeAnim
    global exportedType
    exportedType = exportType

    presetLayer = rt.Array()

    for i in range(0, rt.layerManager.count):
        mLayer = rt.layerManager.getLayer(i)
        patternMatch = rt.matchPattern(mLayer.name, pattern="pr_*")
        if patternMatch:
            mLayer.on = False
            rt.append(presetLayer, mLayer)

    for pLayer in presetLayer:
        print("evaluating preset layer {0}".format(pLayer.name))
        lodNodes = rt.Array()
        theNodes = []
        pLayer.nodes(pymxs.mxsreference(theNodes))
        for n in theNodes:
            pattern = r"^(?i)x[0-9]_"
            patternMatch = re.match(pattern, n.name)
            if patternMatch:
                rt.append(lodNodes, n)

        pLayer.on = True
        lodsInScene = rt.Array()
        for lodNode in lodNodes:
            lodValue = lodNode.name[1]
            rt.appendIfUnique(lodsInScene, lodValue)

        for lodValue in lodsInScene:
            showLodInLayer(pLayer, lodValue)
            exportLodPreset(exportPath, pLayer.name, lodValue)

        pLayer.on = False
    print("OPERATION COMPLETE")
