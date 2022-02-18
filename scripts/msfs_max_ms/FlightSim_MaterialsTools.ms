if MaterialsTools != undefined then destroydialog MaterialsTools
rollout MaterialsTools "Materials Tools"
(
	group "CONVERT"
	(
		button std "FlightSim materials => Standard materials" toolTip:"Albedo layer only"
		button PM "PhysicalMaterial => FlightSim materials" toolTip:"Albedo and normal layer only"
		button StandardToFlightSim "StandardMaterial => FlightSim materials" toolTip:"Albedo and normal layer only"
	)

	group "SEARCH material by texture name"
	(
		edittext	txt_textureName "Texture Name" text:""
		button		btn_materialList		"print material list in listener"	width:180 toolTip:"Print material name using texture"
		button		btn_material_object	"put materials in Material editor"		width:180 	toolTip:"create multimaterial containing all material using Texture in material editor selected slot "
	)

	
	group "REASSIGN textures path"
	(
		button	btn_AutoFind	"AUTO retrieve texture" width:180 /*height:24 pos:[5,28]*/ tooltip:"- Start from the maxfile path and go to all parent folder to find the texture folder\n- If texture folder not found, then browse it manually\n- The script will replace textures path if they exist in subfolder"
		button	btn_browse		"MANUAL Browse texture folder"	width:180	/*height:24 pos:[5,56]*/ tooltip:"- Browse texture folder manually\n- The script will replace textures path if they exist in subfolder"
		progressbar pb_progress value:0 color:green
	)

	group "Material Renamer"
	(
		button btn_fn_AutoRenameFlightSimMat "Auto rename material with unique name" width:240
	)

	group "Shift standard material channels"
	(
		
		dropdownlist DdList_TextSource "You will put :" items:#("Diffuse","Normal","Specular Level", "Self Illumination") 
		dropdownlist DdList_Textarget "In the slot" items:#("Diffuse","Normal","Specular Level", "Self Illumination") 
		button btn_fn_Shift_Std_Mat_Chan "Shift channels with current config" width:240
	)
	
	
	local	TAB_Textures_Directory=#()
	local	T_materialRenamed=#()
	fn fn_ConverToStd mtl =
	(
		local std = standardMaterial \
		name:mtl.name \
		opacity:(mtl.baseColor.w*100) \
		diffuse:(mtl.baseColor as Color) \
		showInViewport:true
		
		if mtl.baseColorTex != undefined and mtl.baseColorTex != "" then
		(
			fullpath	=	(pathconfig.appendpath 	(pathConfig.getCurrentProjectFolder())	(mtl.baseColorTex))
			if doesfileexist fullpath then
			(
				btmap = Bitmaptexture filename:mtl.baseColorTex	 name:(getFilenameFile mtl.baseColorTex)
				if mtl.alphaMode != 1 then btmap.monoOutput = 1
				if mtl.alphaMode != 1 then btmap.RGBOutput = 1
				std.diffuseMap = btmap
				if mtl.alphaMode != 1 then
				(
					std.opacityMap = std.diffuseMap
				)
			)
		)

		if mtl.OcclusionRoughnessMetallicTex != undefined and mtl.OcclusionRoughnessMetallicTex != "" then
		(
			fullpath	=	(pathconfig.appendpath 	(pathConfig.getCurrentProjectFolder())	(mtl.OcclusionRoughnessMetallicTex))
			if doesfileexist fullpath then
			(
				std.SpecularLevelMap = Bitmaptexture filename:mtl.OcclusionRoughnessMetallicTex	 name:(getFilenameFile mtl.OcclusionRoughnessMetallicTex)

			)
		)

		if mtl.NormalTex != undefined and mtl.NormalTex != "" then
		(
			fullpath	=	(pathconfig.appendpath 	(pathConfig.getCurrentProjectFolder())	(mtl.NormalTex))
			if doesfileexist fullpath then
			(
				std.bumpMap = Bitmaptexture filename:mtl.NormalTex	 name:(getFilenameFile mtl.NormalTex)
			)
		)

		if mtl.EmissiveTex != undefined and mtl.EmissiveTex != "" then
		(
			fullpath	=	(pathconfig.appendpath 	(pathConfig.getCurrentProjectFolder())	(mtl.EmissiveTex))
			if doesfileexist fullpath then
			(
				std.SelfIllumMap = Bitmaptexture filename:mtl.EmissiveTex	 name:(getFilenameFile mtl.EmissiveTex)
			)
		)
		return std
	)

	fn fn_GetMaterialByTextureName _name	=
	(
		TAB_mat = #()
		_name="*"+tolower _name+"*"
		FlightSim_mat_list = (getClassInstances FlightSim )
		for i =1 to FlightSim_mat_list.count do			--pour tous les matos
		(
			mat= FlightSim_mat_list[i]

			for texName in mat.TexList do				--pour chaque texture de chaque material FlightSim
			(
				prop = 	(getProperty mat (texName+"Tex"))
				if prop!=undefined and prop!="" then		--si la texture est bien utilis?
				(
					if matchpattern (tolower prop)	pattern:(_name)	then appendifunique	TAB_mat	mat
				)
			)

		)
		return TAB_mat
	)

	fn fn_MaterialList	=
	(
		if txt_textureName.text!=""	then
		(
			List_materials = (fn_GetMaterialByTextureName txt_textureName.text	)
			if List_materials.count ==0 then messagebox "material with this texture not found !"
			else
			(

				format "-----------------------------------------------\nList_material using textures containing \"%\" :\n"	txt_textureName.text
				for i=1 to List_materials.count do
				(
					format "\t%\n"  List_materials[i].name
				)
				format "-----------------------------------------------\n"
				actionMan.executeAction 0 "40472"
			)
		)
		else	messagebox "Please enter texture name first"
	)

	fn fn_MaterialObject	=
	(
		if txt_textureName.text!=""	then
		(
			List_materials = (fn_GetMaterialByTextureName txt_textureName.text	)
			if List_materials.count ==0 then messagebox "material with this texture not found !"
			else
			(
				newmultimat_temp = multimaterial numsubs:List_materials.count	name:"Material Found"
				for i=1 to List_materials.count do
				(
					newmultimat_temp[i] = List_materials[i]
				)
				meditmaterials[activemeditslot] = newmultimat_temp
			)
		)
		else	messagebox "Please enter texture name first"
	)

	fn fn_DebugLog value = 
	(
		format(value + "\n")
	)

	fn fn_DebugWarning value = 
	(
		format(value + "\n")
	)
    
	fn fn_ConvertToPhysicalMaterial pMaterial = 
	(
		DebugLog("converting material " + pMaterial.name)
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
						DebugLog( "texture slot not supported")
					)
				)
			)
			
			if textureConverted then
			(
				DebugLog("texture  "+ textureSlotName +" converted")
			)
			else
			(
				DebugLog("texture  "+ textureSlotName +" NOT converted")
			)
		
		)
		return newMaterial
	)

	fn fn_ReplaceMaterialInstance sourceMat = 
	(
		if classOf(sourceMat) != FlightSim then
		(
			DebugLog("material " +  sourceMat.name + " is not supported" )
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
				DebugLog(" something went wrong converting material " +  sourceMat.name  )
			)
		)
	)

	fn fn_BakeTextureSlot pNode pSize = 
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

	fn fn_AutomaticUV =
	(
		for obj in selection do (
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

	fn fn_getDirectoryREC _Repertory _TAB_directory =
	(

		Repertory_Childs= getDirectories (_Repertory+"*")			--recup les sous repertoires du dossier
		for	RC	 in 	Repertory_Childs	do
		(
			append	_TAB_directory 	RC
			fn_getDirectoryREC 	RC  	_TAB_directory
		)
	)

	fn fn_ManualBrowseDirectory = --sert a corrigg? les paths des asobomat qui pointent encore vers perforce_asset
	(
		TAB_Textures_Directory=#()
		FilePath = getSavePath 	maxfilepath
		if FilePath!=undefined
			then	fn_getDirectoryREC		FilePath		TAB_Textures_Directory
		print "MANUEL : TAB_Textures_Directory"
		print TAB_Textures_Directory

	)

	fn fn_AutoFindDirectory = --sert a corrigg? les paths des asobomat qui pointent encore vers perforce_asset
	(
		TAB_Textures_Directory=#()
		notfound=true
		Current_Rep=maxfilepath
		while notfound	and	Current_Rep!=""	do
		(
			Current_Rep=pathconfig.removepathleaf Current_Rep
			if	Current_Rep==pathconfig.getCurrentProjectFolder()	then		--si on arrive a la racine du projet, on arrete de chercher
			(
				notfound=false
			)
			else
			(
				Repertory_Childs= getDirectories (Current_Rep+"\\*")
				if (Repertory_Childs.count >0) then 							--si il y a des sous repertoire
				(
					for rc in Repertory_Childs	 do
					(
						if  (matchpattern (pathconfig.stripPathToLeaf (tolower rc))	pattern:"*texture*")	then
						(

							notfound=false
							Current_Rep= pathconfig.appendpath Current_Rep	"texture"
							format "Texture folder path : %\n" Current_Rep
							fn_getDirectoryREC		Current_Rep		TAB_Textures_Directory

						)
					)
				)
			)
		)
		--print "AUTO : TAB_Textures_Directory"
		--print TAB_Textures_Directory
		if TAB_Textures_Directory.count==0	then		--si le repertoire n'a pas ?t? trouv? alors on va le chercher manuellement
		(
			messagebox	"Textures Directory not found\nPlease browse manually"
			fn_ManualBrowseDirectory()
		)
	)

	fn fn_Format2Params val1 val2 _longueur =
	(
			str=val1+"\t"
			for i=1 to (((_longueur-val1.count-(mod _longueur 4)+3) /	 4)+1) do str+="\t"
			str+=val2
			format "%\n" str

	)

	fn fn_ReassignTexturesPath =
	(
		ts=timestamp()
		local	TAB_textures_found=#()
		local	TAB_textures_failed=#()

		local	mat_name_lepluslong = 0
		if TAB_Textures_Directory!= undefined and TAB_Textures_Directory.count>0	then
		(
			FlightSim_mat_list = (getClassInstances FlightSim )
			for i =1 to FlightSim_mat_list.count do			--pour tous les matos
			(
				mat= FlightSim_mat_list[i]
				if mat_name_lepluslong<mat.name.count	then	mat_name_lepluslong=mat.name.count
				append	TAB_textures_found		#(mat.name,#())		--contient le nom du matos et 1er tableau contient les textures retrouv?, le 2eme les textures pas trouv?es)
				append	TAB_textures_failed		#(mat.name,#())		--contient le nom du matos et 1er tableau contient les textures retrouv?, le 2eme les textures pas trouv?es)

				for texName in mat.TexList do				--pour chaque texture de chaque material FlightSim
				(
					prop = 	(getProperty mat (texName+"Tex"))
					if prop!=undefined and prop!="" then		--si la texture est bien utilis?
					(
						--if not(doesfileexist (pathConfig.convertPathToAbsolute prop))	then		--si le fichier n'existe pas
						--(
							local	relative_path
							local	true_path
							local	Text_found=false
							for Directory in	TAB_Textures_Directory	do		--pour tous les repertoire de textures
							(
								true_path = pathconfig.appendpath 	Directory	(pathconfig.stripPathToLeaf prop)
								--format "true_path = %\n" true_path
								if	doesfileexist	true_path	then
								(
									relative_path	=	pathConfig.convertPathToRelativeTo  true_path  (pathConfig.getCurrentProjectFolder())
									--format "##  Texture recovered : %\n"  relative_path
									setProperty mat (texName+"Tex")	relative_path
									Text_found=true
									exit
								)
							)
							if Text_found 	then
							(
								append	(TAB_textures_found[TAB_textures_found.count][2]) (pathConfig.convertPathToRelativeTo  true_path  (pathConfig.getCurrentProjectFolder()))
							)
							else
							(
								append	(TAB_textures_failed[TAB_textures_failed.count][2]) (pathconfig.stripPathToLeaf true_path)
							)
						--)
					)
				)
				if pb_progress != undefined then pb_progress.value = 100.*i/FlightSim_mat_list.count
			)
		
			local	Tfound_count=0
			local	TMissed_count=0
			format "##################################\n#  v  # RECOVERED TEXTURES #  v  #\n"
			for T in TAB_textures_found do
			(
				if (T[2]).count>0	then
				(
					for f in (T[2])	do 
					(
						Tfound_count+=1
						fn_Format2Params		(T[1])	f	mat_name_lepluslong
			--format "(%)\t\t%\n"  (T[1])	f
					)
				)
			)
			format "###############################\n#  v  # MISSED TEXTURES #  v  #\n"
			for T in TAB_textures_failed do
			(
				if (T[2]).count>0	then
				(
					for f in (T[2])	do
					(
						TMissed_count+=1
						fn_Format2Params  (T[1])	f	mat_name_lepluslong
					)
				)
			)

			MB_str = Tfound_count as string	+" textures recovered\n" + TMissed_count as string	+" textures missed\n" + "View details on listener\n"  
			messagebox MB_str

		)
	)

	fn fn_AutoRenameFlightSimMat _suffixName =
	(
		T_allMatName = #()
		FlightSimMAtList = getclassinstances FlightSim
		for mat in FlightSimMAtList do
		(
			local	current_name = mat.name
			local	num = 1
			while ((finditem T_allMAtName (tolower current_name))!=0) and not (keyboard.controlpressed) do
			(
				current_name = _suffixName + formattedprint num format:"03d"
				num+=1
			)
			if	current_name!=mat.name	then
			(
				append	T_materialRenamed  (mat.name+"  ->  "+current_name)
				format "%\n" T_materialRenamed[T_materialRenamed.count]
			)
			mat.name = current_name
			appendifunique T_allMatName (tolower mat.name)
		)
	)

	fn fn_GetbitMapObjectByFileName _Fname =
	(
		for Bm in (getClassInstances Bitmaptexture) do			--pour tous les Bitmaps
		(
			if _Fname == bm.filename then
			(
				return Bm
			)
		)
		return undefined
	)

	

	on std pressed do
	(
		if (queryBox "Convert all FlightSim Materials to Standard ?\nNot undoable !" title:"Materials convertion" beep:false) then
		(
			for mtl in (getClassInstances FlightSim ) do
			(
				replaceInstances mtl (fn_ConverToStd mtl)
			)
		)
	)

	on PM pressed do
	(
		if (queryBox "Convert all Physical Materials to FlightSim Material ?\nNot undoable !" title:"Materials convertion" beep:false) then
		(
			for mat in (getClassInstances PhysicalMaterial) do			--pour tous les matos
			(
				new_FSmat = FlightSim()
				new_FSmat.basecolorTex = mat.mapM1.filename
				if mat.bumpmap != undefined then	new_FSmat.NormalTex = mat.bumpmap.normal_map.filename
				new_FSmat.name = mat.name
				replaceinstances mat new_FSmat
			)
		)
	)
	
	on StandardToFlightSim pressed do
	(
		if (queryBox "Convert all Standard Material to FlightSim Material ?\nNot undoable !" title:"Materials convertion" beep:false) then
		(
			for mat in (getClassInstances StandardMaterial) do			--pour tous les matos
			(
				new_FSmat = FlightSim()
				if mat.diffuseMap!= undefined then new_FSmat.basecolorTex = mat.diffuseMap.fileName
				if mat.bumpMap != undefined then	new_FSmat.NormalTex = mat.bumpMap.fileName

				if mat.SpecularLevelMap != undefined then	new_FSmat.OcclusionRoughnessMetallicTex = mat.SpecularLevelMap.fileName
				if mat.SelfIllumMap != undefined then	new_FSmat.EmissiveTex = mat.SelfIllumMap.fileName
				new_FSmat.name = mat.name
				replaceinstances mat new_FSmat
			)
		)
	)
	on btn_fn_Shift_Std_Mat_Chan pressed do
	(
		undo on
		(
			Map_Dic = #()
			Map_Dic[1] = "diffuseMap"
			Map_Dic[2] = "bumpMap"
			Map_Dic[3] = "SpecularLevelMap"
			Map_Dic[4] = "SelfIllumMap"

			for mat in (getClassInstances StandardMaterial) do			--pour tous les matos
			(
				Source_Input = DdList_TextSource.selection 
				Target_Input = DdList_Textarget.selection

				if getProperty mat Map_Dic[Source_Input] != undefined then 
				(
					Btext = fn_GetbitMapObjectByFileName((getProperty mat Map_Dic[Source_Input]).fileName)
					if Btext == undefined then
					( 
						BText = Bitmaptexture filename:(getProperty mat Map_Dic[Source_Input]).fileName name:(getFilenameFile (getProperty mat Map_Dic[Source_Input]).fileName)
					)
					setProperty mat Map_Dic[Target_Input] BText
				)
				else
				(
					--btmtarg = getProperty mat Map_Dic[Target_Input]
					setProperty mat Map_Dic[Target_Input] undefined
					setProperty mat (Map_Dic[Target_Input] + "Amount") 0
				)
			)			
		)
	)
	on btn_materialList pressed do fn_MaterialList()
	on btn_material_object pressed do fn_MaterialObject()
	on btn_flattenUV pressed do fn_AutomaticUV()

	on btn_AutoFind pressed do
	(
		fn_AutoFindDirectory()
		fn_ReassignTexturesPath()
	)

	on btn_browse pressed do
	(
		fn_ManualBrowseDirectory()
		fn_ReassignTexturesPath()
	)
	
	
	on btn_fn_AutoRenameFlightSimMat pressed do
	(
		if (querybox "operation can not be canceled\nAre you sure to continue?")	then
		(
			fn_AutoRenameFlightSimMat	"Mat_"
			messagebox (T_materialRenamed.count as string+" materials renamed (list in listener)")
		)
	)
)
createDialog MaterialsTools  260 500
