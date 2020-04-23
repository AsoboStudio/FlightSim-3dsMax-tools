if MaterialsTools != undefined then destroydialog MaterialsTools
rollout MaterialsTools "Materials Tools"
(
	fn Convert_std mtl =
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
				std.diffuseMap = Bitmaptexture filename:mtl.baseColorTex	 name:(getFilenameFile mtl.baseColorTex)
				if mtl.alphaMode != 1 then
				(
					std.opacityMap = std.diffuseMap
				)
			)
		)
		
		return std
	)
	
	group "CONVERT"
	(
		button std "FlightSim materials => Standard materials" toolTip:"Albedo layer only"
		button PM "PhysicalMaterial => FlightSim materials" toolTip:"Albedo and normal layer only"
		
		on std pressed do
		(
			if (queryBox "Convert all FlightSim Materials to Standard ?\nNot undoable !" title:"Materials convertion" beep:false) then
			(
				for mtl in (getClassInstances FlightSim ) do
				(
					replaceInstances mtl (Convert_std mtl)
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

	)






	group "SEARCH material by texture name"
	(
		edittext	txt_textureName "Texture Name" text:""
		button		btn_materialList		"print material list in listener"	width:180 toolTip:"Print material name using texture"
		button		btn_material_object	"put materials in Material editor"		width:180 	toolTip:"create multimaterial containing all material using Texture in material editor selected slot "
	)


	fn KH_getMaterial_ByTextureName _name	=
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

	fn		fn_materialList	=
	(
		if txt_textureName.text!=""	then
		(
			List_materials = (KH_getMaterial_ByTextureName txt_textureName.text	)
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

	fn		fn_material_object	=
	(
		if txt_textureName.text!=""	then
		(
			List_materials = (KH_getMaterial_ByTextureName txt_textureName.text	)
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

	on btn_materialList pressed do fn_materialList()
	on btn_material_object pressed do fn_material_object()



	local	TAB_Textures_Directory=#()
	group "REASSIGN textures path"
	(
		button	btn_AutoFind	"AUTO retrieve texture"			width:180	/*height:24 pos:[5,28]*/ \
												tooltip:"- Start from the maxfile path and go to all parent folder to find the texture folder\n- If texture folder not found, then browse it manually\n- The script will replace textures path if they exist in subfolder"
		button	btn_browse		"MANUAL Browse texture folder"	width:180	/*height:24 pos:[5,56]*/ \
												tooltip:"- Browse texture folder manually\n- The script will replace textures path if they exist in subfolder"
		progressBar pb_progress value:0 color:green
	)

	fn get_directory_REC 	_Repertory  	_TAB_directory	=
	(

		Repertory_Childs= getDirectories (_Repertory+"*")			--recup les sous repertoires du dossier
		for	RC	 in 	Repertory_Childs	do
		(
			append	_TAB_directory 	RC
			get_directory_REC 	RC  	_TAB_directory
		)
	)

	fn ManualBrowse_Directory	=			--sert a corrigg? les paths des asobomat qui pointent encore vers perforce_asset
	(
		TAB_Textures_Directory=#()
		FilePath = getSavePath 	maxfilepath
		if FilePath!=undefined
			then	get_directory_REC		FilePath		TAB_Textures_Directory
		print "MANUEL : TAB_Textures_Directory"
		print TAB_Textures_Directory

	)

	fn AutoFind_Directory	=			--sert a corrigg? les paths des asobomat qui pointent encore vers perforce_asset
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
							get_directory_REC		Current_Rep		TAB_Textures_Directory

						)
					)
				)
			)
		)
-- 		print "AUTO : TAB_Textures_Directory"
-- 		print TAB_Textures_Directory
		if TAB_Textures_Directory.count==0	then		--si le repertoire n'a pas ?t? trouv? alors on va le chercher manuellement
		(
			messagebox	"Textures Directory not found\nPlease browse manually"
			ManualBrowse_Directory()
		)
	)

	fn	format_2_params  	val1	val2	_longueur	=
	(
			str=val1+"\t"
			for i=1 to (((_longueur-val1.count-(mod _longueur 4)+3) /	 4)+1) do str+="\t"
			str+=val2
			format "%\n" str

	)

	fn	Reassign_Textures_Path =
	(
		ts=timestamp()
		local	TAB_textures_found=#()
		local	TAB_textures_failed=#()

		local	mat_name_lepluslong = 0
		if TAB_Textures_Directory.count>0	then
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
-- 						if not(doesfileexist (pathConfig.convertPathToAbsolute prop))	then		--si le fichier n'existe pas
-- 						(
							local	relative_path
							local	true_path
							local	Text_found=false
							for Directory in	TAB_Textures_Directory	do		--pour tous les repertoire de textures
							(
								true_path = pathconfig.appendpath 	Directory	(pathconfig.stripPathToLeaf prop)
-- 								format "true_path = %\n" true_path
								if	doesfileexist	true_path	then
								(
									relative_path	=	pathConfig.convertPathToRelativeTo  true_path  (pathConfig.getCurrentProjectFolder())
-- 									format "##  Texture recovered : %\n"  relative_path
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
-- 						)
					)
				)
				pb_progress.value = 100.*i/FlightSim_mat_list.count
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
						format_2_params		(T[1])	f	mat_name_lepluslong
-- 						format "(%)\t\t%\n"  (T[1])	f
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
						format_2_params  (T[1])	f	mat_name_lepluslong
					)
				)
			)

			MB_str = Tfound_count as string	+" textures recovered\n" + TMissed_count as string	+" textures missed\n" + "View details on listener\n"  
			messagebox MB_str

		)
	)

	
	on btn_AutoFind pressed do
	(
		AutoFind_Directory()
		Reassign_Textures_Path()
	)
	on btn_browse pressed do
	(
		ManualBrowse_Directory()
		Reassign_Textures_Path()
	)
	
	group "Material Renamer"
	(
		button btn_autoRenameFlightSimMat "Auto rename material with unique name" width:240
	)
	local	T_materialRenamed=#()
	fn	AutoRenameFlightSimMAt _suffixName =
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
	
	on btn_autoRenameFlightSimMat pressed do
	(
		if (querybox "operation can not be canceled\nAre you sure to continue?")	then
		(
			AutoRenameFlightSimMAt	"Mat_"
			messagebox (T_materialRenamed.count as string+" materials renamed (list in listener)")
		)

	)
)
createDialog MaterialsTools  260 340
