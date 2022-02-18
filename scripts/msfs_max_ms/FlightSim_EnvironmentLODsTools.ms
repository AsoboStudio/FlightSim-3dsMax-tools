if EnvironmentLODTools != undefined then destroydialog EnvironmentLODTools
rollout EnvironmentLODTools "Environment LODs Tools"
(
	fn fn_DebugLog value = 
	(
		--format(value + "\n")
	)

	fn fn_DebugWarning value = 
	(
		format(value + "\n")
	)
    
	fn fn_ConvertToPhysicalMaterial pMaterial = 
	(
		fn_DebugLog("converting material " + pMaterial.name)
		local newName = pMaterial.name + "_Physical"
		local newMaterial = PhysicalMaterial name:newName
		for textureSlot in getPropNames pMaterial do
		(   
			local textureConverted = false
			textureSlotName = textureSlot as string
			if hasProperty pMaterial (textureSlotName) then
			(
				local textureMapPath = (getProperty pMaterial (textureSlotName))
				if textureMapPath == undefined or textureMapPath == "" then continue
				case textureSlotName of (
					"BaseColorTex":(                
						local bm = Bitmaptexture filename:textureMapPath
						newMaterial.base_color_map = bm
						local textureConverted = true
					)
					"EmissiveTex":(
						local bm = Bitmaptexture filename:textureMapPath
						newMaterial.emission_map = bm 
						local textureConverted = true
					)
					"OpacityTex":(
						local bm = Bitmaptexture filename:textureMapPath
						newMaterial.transparency_map = bm
						local textureConverted = true
					)
					"OcclusionRoughnessMetallicTex":(
						local bm = Bitmaptexture filename:textureMapPath
						local occlusionTint = RGB_Tint map1:bm map1Enabled:true
						occlusionTint.red = (color 255 255 255)
						occlusionTint.green = (color 0 0 0)
						occlusionTint.blue = (color 0 0 0)
						local roughnessTint = RGB_Tint map1:bm map1Enabled:true
						roughnessTint.red = (color 0 0 0)
						roughnessTint.green = (color 255 255 255)
						roughnessTint.blue = (color 0 0 0)
						local metallicTint = RGB_Tint map1:bm map1Enabled:true
						metallicTint.red = (color 0 0 0)
						metallicTint.green = (color 0 0 0)
						metallicTint.blue = (color 255 255 255)
						newMaterial.roughness_map = roughnessTint
						newMaterial.metalness_map = metallicTint
						local textureConverted = true
					)
					default:(
						fn_DebugLog( "texture slot not supported")
					)
				)
			)
			
			if textureConverted then
			(
				fn_DebugLog("texture  "+ textureSlotName +" converted")
			)
			else
			(
				fn_DebugLog("texture  "+ textureSlotName +" NOT converted")
			)
		
		)
		return newMaterial
	)

	fn fn_ReplaceMaterialInstance sourceMat = 
	(
		if classOf(sourceMat) != FlightSim then
		(
			fn_DebugLog("material " +  sourceMat.name + " is not supported" )
		)
		else
		(
			local target = fn_ConvertToPhysicalMaterial sourceMat
			if target != undefined then
			(
				replaceInstances sourceMat target transferCAs:true
			)
			else
			(
				fn_DebugLog(" something went wrong converting material " +  sourceMat.name  )
			)
		)
	)

	fn fn_BakeTextureSlot pProjectionSources pNode pSize = 
	(
		--Clear all render elements 
		pNode.iNodeBakeProperties.removeAllBakeElements() 
		--Preparing the Bake Elements:
		be1 = diffusemap() --instance of the bake element class
		be1.outputSzX = be1.outputSzY = pSize --set the size of the baked map
		--specifythe full file path, name and type:
		be1.fileType = (getDir #image+"\\"+pNode.name+"_diffuse.png")
		be1.fileName = filenameFromPath be1.fileType
		be1.filterOn = true --enable filtering
		be1.shadowsOn = false --disable shadows
		be1.lightingOn = false --disable lighting
		be1.enabled = true --enable baking
		be1.targetMapSlotName = "Base Color Map"
		--Preparing theobjectfor baking:
		pNode.iNodeBakeProperties.addBakeElement be1 --add first element
		pNode.iNodeBakeProperties.bakeEnabled = true --enabling baking
		pNode.iNodeBakeProperties.bakeChannel = 1 --channel to bake
		pNode.iNodeBakeProperties.nDilations = 1 --expand the texturea bit
		select pNode --we are baking the selection, so we select the object
		--Call the renderer to bake both elements:
		render rendertype:#bakeSelected vfb:on progressBar:true outputSize:[pSize,pSize] outputfile:be1.fileType
		theMap1 =bitmaptexture filename:be1.fileType
		--Create a standard self-illum material using the Composite map
		bakedMat = standard diffusemap:theMap1 selfIllumAmount:100
		--Assign a Shell Material to the object,
		--keep the old material as original material,
		--set the new bakedMat as the baked material:
		pNode.material = Shell_Material originalMaterial:pNode.material\
		bakedMaterial:bakedMat viewportMtlIndex:1 renderMtlIndex:1
		--Show the textures of the baked material in the viewport
		showTextureMap pNode.material pNode.material.bakedMaterial true
	)

	fn fn_AddProjection pProjectionSources pNode =
	(
		mProjection = Projection()
		mProjection
	)

	fn fn_AutomaticUV =
	(
		for obj in selection do
		(
			my_unwrap = unwrap_UVW()
			my_unwrap.setAlwaysEdit false
			my_unwrap.setMapChannel 1
			my_unwrap.setFlattenAngle 45.0
			my_unwrap.setFlattenSpacing 0.02
			my_unwrap.setFlattenNormalize true
			my_unwrap.setFlattenRotate true
			my_unwrap.setFlattenFillHoles true
			my_unwrap.setApplyToWholeObject true
			my_unwrap.name = "Automatic Flatten"

			addModifier obj my_unwrap
			
			my_unwrap.flattenMapByMatID 45.0 0.02 true 2 true true
		)
		
	)

	fn fn_DetachObjects oPoly =
    (
		local pDummy= Dummy pos:oPoly.pos name:oPoly.name boxsize:[1,1,1]
		oPoly.parent = pDummy
        if (classOf oPoly != Editable_Poly) then
            throw "Wrong input in function: detachToNodes()"
        
        local iNumFacesLastElem = 0
        local baElemFaces = #{}
        local sName = ""
    
        while (true) do
        (
            baElemFaces = polyOp.getElementsUsingFace oPoly 1
            sName = uniqueName oPoly.name
			polyOp.detachFaces oPoly baElemFaces delete:true asNode:true name:sName
			local detached = getNodeByName(sName)
			detached.parent = pDummy
			detached.pivot = detached.center
            if ((polyOp.getNumFaces oPoly) == 0) then
            (
                delete oPoly
                exit
            )
    
            if (keyboard.escPressed == true) do
                throw "** escape key pressed **"
		)
    )

	group "LOD Generation"
	(
		button btn_DetachObjects "Detach Objects" width:240
		button 	btn_ConvertToInstances "Convert To Instances" width:240 toolTip:"Select objects to be replaced, and pick source objet"
		button btn_CloneAndConvertToPhysical "Clone And Convert To Physical"  width:240 toolTip:"Clone selection, and convert to Physical keeping Diffuse, Roughness, Metallic, Opacity, Emission"
		button btn_FlattenUV "Flatten UV" width:240
		button btn_SelectAllInstances "Select all Instances" width:240
		button btn_FilterSelectionByVisibleObjects "Filter selection by visible objects" width:240
	)
	
	on btn_SelectAllInstances pressed do 
	(
		mSel = selection as array
		result = #()
		for i=1 to mSel.count do 
		(
			InstanceMgr.GetInstances mSel[i] &instances
			if instances.count <=1 then continue
			for j in instances do 
			(
				appendIfUnique result j
			)
		)
		select result
	)
	
	on btn_FilterSelectionByVisibleObjects pressed do 
	(
		mSel = selection as array
		result = #()
		for i=1 to mSel.count do 
		(
			if not mSel[i].isHidden then
			(
				appendIfUnique result  mSel[i]
			)
		)
		select result
	)

	on btn_DetachObjects pressed do
	(
		for obj in selection do 
		(
			fn_DetachObjects(obj)
		)
	)

	on btn_ConvertToInstances pressed do
	(
		local sourceObj = selection[1]
		local obj_sel=for o in selection collect o
		if obj_sel.count>0 then
		(
			undo "ReplaceBy" on
			(
				replaceby obj_sel sourceObj
			)
		)
		for o in selection do
		(
			CenterObject o
		)
	)

	on btn_FlattenUV pressed do 
	(
		fn_AutomaticUV()
	)

	on btn_CloneAndConvertToPhysical pressed do
	(
		copiedSources = for obj in selection as array collect copy obj
		
		for copiedObj in copiedSources do 
		(
			sName = copiedObj.name + "_PhysicalMaterial"
			mainMat = copy copiedObj.material
			copiedObj.material = mainMat
			if classOf(mainMat) == Multimaterial then
			(
				for mat in mainMat.materialList do
				(
					fn_ReplaceMaterialInstance(mat) 
				)
			)
			else
			(
				fn_ReplaceMaterialInstance(mainMat) 
			)
		)
		
	)
)
createDialog EnvironmentLODTools  260 440
