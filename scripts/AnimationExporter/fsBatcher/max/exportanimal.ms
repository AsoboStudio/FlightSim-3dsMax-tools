print "------------------------------------------------------------------------------------"

print localtime
exportType="###exportType###"
exportPaths=#(###exportPaths###)
gltfAnimationName=###gltfAnimationName###
bakeAnimation=###bakeAnimations###
-- exportType="Model"
-- exportPaths=#("C:\Users\mgrillon\Desktop\Test")
-- exportFiles=#("D:/Workspace_mgrillon/ASSETS/KittyHawk_Data/ART/fs/object/Global/Asobo_Animals/Bears/Shared/Bear_Adult_Exporter.max")
-- gltfAnimationName="Bears"
-- bakeAnimation=false

format "Export type %\n" exportType

Assembly = dotNetClass "System.Reflection.Assembly"
Assembly.loadfrom "C:\\Program Files\\Autodesk\\3ds Max 2019\\bin\\assemblies\\Max2Babylon.dll"
maxScriptManager = dotNetObject "Max2Babylon.MaxScriptManager"

fn exportLodPreset exportPath mName lod gltfAnimationName =
(
     print "New Export instance"
     format "exporting % at lod %\n" mName lod

     exportName = trimleft mName "pr_"
     exportFolder = exportPath + "\\"
     modelFolder = exportFolder+"model."+exportName
     animationFolder = exportFolder+"animation"
     param = maxScriptManager.InitParameters "c:\\default.gltf"
     case exportType of
     (
        "Animation":
        (
            outputPath = animationFolder
			makedir outputPath all:true
			outputPath = outputPath+"\\"+gltfAnimationName+".gltf"
            param.animationExportType = (dotnetclass "BabylonExport.Entities.AnimationExportType").ExportOnly
            param.outputPath = outputPath
            param.exportMaterials = false
        )
        "Model":
        (
            outputPath = modelFolder
			makedir outputPath all:true
			outputPath = outputPath+"\\"+exportName+"_LOD0"+lod+".gltf"
            param.animationExportType = (dotnetclass "BabylonExport.Entities.AnimationExportType").NotExport
			param.outputPath = outputPath
			param.exportMaterials = true
		)
        "All":
        (
            outputPath = modelFolder
			makedir outputPath all:true
			outputPath = outputPath+"\\"+exportName+"_LOD0"+lod+".gltf"
            param.animationExportType = (dotnetclass "BabylonExport.Entities.AnimationExportType").Export
			param.outputPath = outputPath
			param.exportMaterials = true
		)
        default:
        (
            param.animationExportType = 0
        )
     )
     param.mergeContainersAndXRef = false
     param.writeTextures = false
     param.overwriteTextures = false
     param.usePreExportProcess = true
	 if (bakeAnimation==true) then
	(
		param.bakeAnimationType = (dotnetclass "Max2Babylon.BakeAnimationType").BakeAllAnimations
	)
	else
	(
		param.bakeAnimationType = (dotnetclass "Max2Babylon.BakeAnimationType").DoNotBakeAnimation
	)
     param.optimizeAnimations = true
     param.animgroupExportNonAnimated = true
     param.enableASBAnimationRetargeting = true

     maxScriptManager.Export param false
)

fn hideNodes nodes=
(
	for n in nodes do
	(
		n.ishidden = true
	)
)

fn showLodInLayer layerObject lodValue=
(
	layerObject.nodes &layerNodes
    for n in layerNodes do
    (
		n.ishidden = true
        if(n.name[2] == lodValue) then
        (
            n.ishidden = false
        )        
    )
)

fn exportScene exportPath=
(
    presetLayer = #()

    for i = 0 to layerManager.count-1 do
    (
        mLayer = layerManager.getLayer i
        patternMatch = matchPattern mLayer.name pattern:"pr_*"
        if(patternMatch) then
        (
          mLayer.on = false
          append presetLayer mLayer
        )
    )

    for pLayer in presetLayer do
    (
        format "evaluating preset layer %\n" pLayer.name
        local lodNodes = #()
        pLayer.nodes &theNodes
        for n in theNodes do
        (
            pattern =@"^(?i)x[0-9]_"
            rgx = dotnetObject "System.Text.RegularExpressions.Regex" pattern
            patternMatch = rgx.Match n.name
            if patternMatch.success then
            (
                append lodNodes n
            )
        )

        pLayer.on = true
        --evaluate lods value in layer
        local lodsInScene=#()
        for lodNode in lodNodes do
        (
            lodValue = lodNode.name[2]
            appendIfUnique lodsInScene lodValue
        )

        format "found those lods % in preset %\n" lodsInScene pLayer.name
        for lodValue in lodsInScene do
        (
			print ("_____")
            format "exporting lod % \n" lodValue
            showLodInLayer pLayer lodValue					
            exportLodPreset exportPath pLayer.name lodValue gltfAnimationName			
        )
        pLayer.on = false
    )
)

exportPath = exportPaths[1]
format "Export folder %\n" exportPath


format "found % xref object\n" objXRefMgr.recordCount
for k=1 to objXRefMgr.recordCount do
(
    rec = objXRefMgr.GetRecord k
    objXRefMgr.MergeRecordIntoScene rec
)

exportScene exportPath
print "Batch Complete"




