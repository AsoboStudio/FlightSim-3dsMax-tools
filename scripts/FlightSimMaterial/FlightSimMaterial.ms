if not NitrousGraphicsManager.IsEnabled() then
	messageBox "Flight Simulator Material works in Direct3D 11 mode only, please switch viewport display driver.\n*Customize/Preferences/Viewports/Choose Driver...*" title:"Flight Simulator" beep:true



rcmenu FlightSimMaterialRCMenuTex
(
	menuItem rc_display "Display" enabled:false
	menuItem rc_open "Open" enabled:false
	menuItem rc_explore "Explore" enabled:false
	separator sep1
	subMenu "Flags"
	(
		menuItem rc_tAlphaPreservation "Alpha Preservation" enabled:false checked:false
		menuItem rc_tNoReduce "No Reduction" enabled:false checked:false
		separator sep2
		menuItem rc_tEdit "Edit Flags File" enabled:false
		menuItem rc_tDelete "Delete Flags File" enabled:false
	)
	separator sep3
	menuItem rc_copy "Copy" enabled:false
	menuItem rc_paste "Paste" enabled:false
	menuItem rc_reload "Reload" enabled:false
	menuItem rc_remove "Remove" enabled:false
	
	local mtl
	local clipboardClass
	local basename
	local filename
	local TFlagsFile
	
	fn updateTooltipFlags =
	(
		mtl.texturesUI.updateUiFlags basename
	)
	
	fn createTFlagsFile =
	(
		if doesFileExist TFlagsFile then
		(
			return true
		)
		else
		(
			local newFile = createFile TFlagsFile
			if newFile == undefined do return false
			close newFile
			return true
		)
	)
	
	fn getFlag flagStr =
	(
		local file = openFile TFlagsFile mode:"rtS"
		local content = readDelimitedString file #eof
		close file
		
		local pos = (findString content flagStr)
		if pos != undefined then
			return true
		else
			return false
	)
	
	fn setFlag flagStr =
	(
		local file = openFile TFlagsFile mode:"rtS"
		local content = readDelimitedString file #eof
		close file
		
		if (findString content "_DEFAULT=") == undefined then content = "_DEFAULT="
		
		local pos = (findString content flagStr)
		if pos != undefined then
		(
			content = substituteString content ("+"+flagStr) ""
			content = substituteString content flagStr ""
		)
		else
			append content ("+"+flagStr)
			
		file = openFile TFlagsFile mode:"wtSc"
		format content to:file
		flush file
		close file
		updateTooltipFlags()
	)
	
	fn deleteTFlags =
	(
		if doesFileExist TFlagsFile then
		(
			if queryBox ("Suprimer le fichier .TFlags ?\n"+TFlagsFile) title:"TFlags" beep:false then
			(
				deleteFile TFlagsFile
			)
		)
		else print "Fichier TFlags inexistant"
		updateTooltipFlags()
	)
	
	on FlightSimMaterialRCMenuTex open do
	(
		mtl = undefined
		if MatEditor.mode == #basic then --TODO get slate editor mtl, only possible in 3ds >= 2017 SP3
			mtl = medit.GetCurMtl()
		else if MatEditor.mode == #advanced then
			mtl = sme.GetMtlInParamEditor()
		
		if mtl != undefined then
		(
			clipboardClass = dotNetClass "System.Windows.Forms.Clipboard"
			basename = mtl.texturesUI.activeTex
			filename = mapPaths.getFullFilePath (getProperty mtl (basename + "Tex"))
			
			if filename != "" then
			(
				rc_reload.enabled = rc_explore.enabled = rc_remove.enabled = true
				if doesFileExist filename then
				(
					rc_copy.enabled = rc_display.enabled = rc_open.enabled = true
					
					rc_tAlphaPreservation.enabled = true
					rc_tNoReduce.enabled = true
					rc_tEdit.enabled = true
					
					TFlagsFile = filename + ".FLAGS"
					if doesFileExist TFlagsFile then
					(
						rc_tDelete.enabled = true
						
						rc_tAlphaPreservation.checked = getFlag "ALPHAPRESERVATION"
						rc_tNoReduce.checked = getFlag "NOREDUCE"
					)
				)
			)
			else if getProperty mtl (basename + "Tex") != "" then --tex not found
			(
				filename = getProperty mtl (basename + "Tex")
				rc_reload.enabled = rc_explore.enabled = rc_remove.enabled = true
			)
			
			if clipboardClass.ContainsText() then
			(
				rc_paste.enabled = case tolower (getFilenameType (clipboardClass.GetText())) of
				(
					(".tif"): true
					(".dds"): true
					(".jpg"): true
					(".tga"): true 
					(".png"): true
					(".bmp"): true
					(".hdr"): true
					default: false
				)
			)
		)
	)

	on rc_display picked do
	(
		display ( openBitMap filename )
	)
	on rc_open picked do
	(
		HiddenDOSCommand filename donotwait:true
	)
	on rc_explore picked do
	(
		HiddenDOSCommand ("start \"\" \"explorer.exe\" /select," + filename)
	)
	
	on rc_tAlphaPreservation picked do if createTFlagsFile() then setFlag "ALPHAPRESERVATION"
	on rc_tNoReduce picked do if createTFlagsFile() then setFlag "NOREDUCE"
	on rc_tEdit picked do if createTFlagsFile() then shellLaunch TFlagsFile ""
	on rc_tDelete picked do deleteTFlags()
	
	on rc_copy picked do
	(
		clipboardClass.SetText filename
	)
	on rc_paste picked do
	(
		mtl.texturesUI.loadTex (clipboardClass.GetText()) basename
	)
	on rc_reload picked do
	(
		mtl.texturesUI.loadTex filename basename
	)
	on rc_remove picked do
	(
		mtl.texturesUI.clearTex basename
	)
)

global FlightSim_paramsRolledUp = true
global FlightSim_texturesRolledUp = true

plugin material FlightSim
name:"Flight Simulator"
classID:#(0x5ac74889, 0x27e705cd)
extends:DirectX_9_Shader replaceUI:true autoPromoteDelegateProps:false
version:0.1
(
	local TexList = #(
		"BaseColor",
		"OcclusionRoughnessMetallic",
		"Normal",
		"BlendMask",
		"Emissive",
		"WetnessAO",
		"Opacity",
		"Dirt",
		"HeightMap",
		"DetailColor",
		"DetailOcclusionRoughnessMetallic",
		"DetailNormal"
	)

    local matList = #(
        #Standard, --1
        #Decal, --2
        #Windshield, --3
        #PortHole, --4
        #Glass, --5
        #GeoDecalFrosted, --6
        #ClearCoat, --7
        #ParallaxWindow, --8
        #Anisotropic, --9
        #Hair, --10
        #SSS, --11
        #Invisible, --12
        #FakeTerrain, --13
        #FresnelFade, --14
        #EnvironmentOccluder --15
    )
	
	local curPath = getFilenamePath (getSourceFileName())
	
	fn openBitmapGamma assetId gamma: =
	(
		local bm
		if gamma == unsupplied or (maxversion())[1] < 16000 then
			bm = openbitmap assetId
		else
			bm = openbitmap assetId gamma:gamma
		if bm != undefined then
			bm.filename = AssetManager.GetFileName assetId -- openbitmap return absolute path, set back to relative
		return bm
	)
	
	local TexBlack = openbitmap (pathConfig.appendPath curPath "FlightSimMaterial_Black.bmp") 
	local TexWhite = openbitmap (pathConfig.appendPath curPath "FlightSimMaterial_White.bmp") 
	local TexFlat = openbitmap (pathConfig.appendPath curPath "FlightSimMaterial_Flat.bmp") gamma:1.0
	local TexGrey = openbitmap (pathConfig.appendPath curPath "FlightSimMaterial_Grey.bmp") gamma:1.0
	local TexRadiance = openBitMap (pathConfig.appendPath curPath @"IBLmap\\Studio_Radiance.dds") gamma:1.0
	local TexIrradiance = openBitMap (pathConfig.appendPath curPath @"IBLmap\\Studio_Irradiance.dds") gamma:1.0
	local TexBRDFLUT = openBitMap (pathConfig.appendPath curPath "FlighSim_BRDFLUT.png") gamma:1.0
	
	local filesTypes = "*.tif,*.dds,*.jpg,*.tga,*.png,*.bmp,*.hdr|*.tif;*.dds;*.jpg;*.tga;*.png;*.bmp;*.hdr"

	local clipboardClass = dotNetClass "System.Windows.Forms.Clipboard"
	
	fn mxs2dotBmp bm &dotbm =
	(
		local data = if clipboardClass.ContainsText() then clipboardClass.GetText() else ""
		local tempBm = bitmap 300 (300*bm.height/bm.width)
		copy bm tempBm
		setClipboardBitmap tempBm
		free tempBm
		if dotbm != undefined then dotbm.dispose()
		dotbm = clipboardClass.GetImage()
		try (clipboardClass.SetText data) catch()
	)
	
	fn updateGlobalUI =
	(
		if ((MatEditor.mode == #basic and this==medit.GetCurMtl()) or
			(MatEditor.mode == #advanced and this==sme.GetMtlInParamEditor()))
		do
		(
			if loading == false and
				MatEditor.isOpen() and
				this.delegate != undefined then
			(			
				this.texturesUI.updateUI()
				this.paramsUI.updateUI()
			)
		)		
	)
	
	-- support paths relatifs
	fn getFullFilePath &filePath assetType:#Bitmap = FileResolutionManager.getFullFilePath filePath assetType
	
	-- get the name of the texture param from the delegate
	fn getDelTexPName basename =(
		"p_" + basename + "Tex"

	)
	
	--technique
	fn isFlag flag = findItem this.Flags flag > 0

	fn setShaderTechniqueByName techName= 
	(	
		/* 3dsmax strange bahviour : getTechniqueName and technique have indices starting from 1 and 0 respectivily*/
		
		local numTech = delegate.getNumberOfTechniques()
		-- format "number of technique is %\n" numTech
		for i=0 to (numTech-1) do
		(
			if delegate.getTechniqueName (i+1) == techName then
			(
				delegate.technique = i
				--format "set shader tech to %\n" (delegate.getTechniqueName i)
			)
			else
			(
				--format "cannot find technique from value %\n" i
			)
		)
	)
	
	fn loadShader =
	(
	    --format "loading shader % for % \n" matList[this.materialType] delegate.effectFile
		case (matList[this.materialType]) of
		(
            #Standard:
            (
                --format "SETTING STANDARD\n"
                delegate.effectFile = pathConfig.appendPath curPath @"Fx/FlightSimMaterial_Standard.fx"
				
                if this.doubleSided then
                (
                    setShaderTechniqueByName("Tech_Base")
                )
                else
                (
                    setShaderTechniqueByName("Tech_TwoSide")
                )
            )
			#Decal:
            (
                --format "SETTING DECAL \n"
                delegate.effectFile = pathConfig.appendPath curPath @"Fx/FlightSimMaterial_Decal.fx"
				
                if this.doubleSided then
                (
                    setShaderTechniqueByName("Tech_Decal")
                )
                else
                (
                    setShaderTechniqueByName("Tech_DecalTwoSide")
                )
            )
            #Windshield:
            (
                delegate.effectFile = pathConfig.appendPath curPath @"Fx/FlightSimMaterial_Standard.fx"
                if this.doubleSided then
                (
                    setShaderTechniqueByName("Tech_Base")
                )
                else
                (
                    setShaderTechniqueByName("Tech_TwoSide")
                )
            )
            #PortHole:
            (
                delegate.effectFile = pathConfig.appendPath curPath @"Fx/FlightSimMaterial_Standard.fx"
                if this.doubleSided then
                (
                    setShaderTechniqueByName("Tech_Base")
                )
                else
                (
                    setShaderTechniqueByName("Tech_TwoSide")
                )
            )
            #Glass:
            (
                delegate.effectFile = pathConfig.appendPath curPath @"Fx/FlightSimMaterial_Standard.fx"
                if this.doubleSided then
                (
                    setShaderTechniqueByName("Tech_Base")
                )
                else
                (
                    setShaderTechniqueByName("Tech_TwoSide")
                )
            )
            #GeoDecalFrosted:
            (
                delegate.effectFile = pathConfig.appendPath curPath @"Fx/FlightSimMaterial_Standard.fx"
                if this.doubleSided then
                (
                    setShaderTechniqueByName("Tech_Base")
                )
                else
                (
                    setShaderTechniqueByName("Tech_TwoSide")
                )
            )
            #ClearCoat:
            (
                delegate.effectFile = pathConfig.appendPath curPath @"Fx/FlightSimMaterial_Standard.fx"
                if this.doubleSided then
                (
                    setShaderTechniqueByName("Tech_Base")
                )
                else
                (
                    setShaderTechniqueByName("Tech_TwoSide")
                )
            )
            #ParallaxWindow:
            (
                delegate.effectFile = pathConfig.appendPath curPath @"Fx/FlightSimMaterial_ParallaxWindow.fx"
                if this.doubleSided then
                (
                    setShaderTechniqueByName("Tech_Parallax")
                )
                else
                (
                    setShaderTechniqueByName("Tech_Parallax_TwoSide")
                )
            )
            #Anisotropic:
            (
                delegate.effectFile = pathConfig.appendPath curPath @"Fx/FlightSimMaterial_Standard.fx"
                if this.doubleSided then
                (
                    setShaderTechniqueByName("Tech_Base")
                )
                else
                (
                    setShaderTechniqueByName("Tech_TwoSide")
                )
            )
            #Invisible:
            (
                delegate.effectFile = pathConfig.appendPath curPath @"Fx/FlightSimMaterial_Flat.fx"
                setShaderTechniqueByName("Tech_Invisible")
            )
            #FakeTerrain:
            (
                delegate.effectFile = pathConfig.appendPath curPath @"Fx/FlightSimMaterial_Standard.fx"
                if this.doubleSided then
                (
                    setShaderTechniqueByName("Tech_Base")
                )
                else
                (
                    setShaderTechniqueByName("Tech_TwoSide")
                )
            )
            #FresnelFade:
            (
                delegate.effectFile = pathConfig.appendPath curPath @"Fx/FlightSimMaterial_Standard.fx"
               if this.doubleSided then
                (
                    setShaderTechniqueByName("Tech_Base")
                )
                else
                (
                    setShaderTechniqueByName("Tech_TwoSide")
                )
            )
            #EnvironmentOccluder:
            (
                delegate.effectFile = pathConfig.appendPath curPath @"Fx/FlightSimMaterial_Flat.fx"
                setShaderTechniqueByName("Tech_EnvOccluder")
            )

            default:
            (
                format "fallback in default status"
                delegate.effectFile = pathConfig.appendPath curPath @"Fx/FlightSimMaterial_Standard.fx"
            )
		)

		delegate.p_irradianceTex = TexIrradiance
		delegate.p_radianceTex = TexRadiance
		delegate.p_specularBRDF_LUT = TexBRDFLUT

		for i in TexList do
			if (getProperty this (i + "Tex")) == undefined then setProperty this (i + "Tex") ""
	)
	
	parameters params rollout:paramsUI
	(		
		radianceMap  type:#filename assettype:#Bitmap
		irradianceMap type:#filename assettype:#Bitmap
	    uniqueInContainer type:#boolean default:false ui:uniqueInContainer animatable:false

		materialType type:#integer default:1 ui:materialType animatable:false
		
		baseColor type:#point4 default:white ui:BaseColor animatable:false
		emissive type:#point4 default:black ui:Emissive animatable:true
		
		roughness type:#float default:1.0 ui:Roughness animatable:false
		metallic type:#float default:1.0 ui:metallic animatable:false
		normalScale type:#float default:1.0 ui:normalScale animatable:false
		
		alphaMode type:#integer default:1 ui:alphaMode animatable:false
		drawOrder type:#integer default:0 ui:drawOrder animatable:false
		alphaCutoff type:#float default:0.5 ui:alphaCutoff animatable:false
		detailUVScale type:#float default:2.0 ui:detailUVScale animatable:false
		detailUVOffsetX type:#float default:0.0 ui:detailUVOffsetX animatable:false
		detailUVOffsetY type:#float default:0.0 ui:detailUVOffsetY animatable:false
		detailNormalScale type:#float default:1.0 ui:detailNormalScale animatable:false
		blendThreshold type:#float default:0.1 ui:blendThreshold animatable:false
		doubleSided type:#boolean default:false ui:doubleSided animatable:false
		
		decalColorFactor type:#float default:1.0 ui:decalColorFactor animatable:false
		decalRoughnessFactor type:#float default:1.0 ui:decalRoughnessFactor animatable:false
		decalMetalFactor type:#float default:1.0 ui:decalMetalFactor animatable:false
		decalOcclusionFactor type:#float default:1.0 ui:decalOcclusionFactor animatable:false
		decalNormalFactor type:#float default:1.0 ui:decalNormalFactor animatable:false
		decalEmissiveFactor type:#float default:1.0 ui:decalEmissiveFactor animatable:false
		
		parallaxScale type:#float default:0.0 ui:parallaxScale animatable:false
		roomSizeXScale type:#float default:0.5 ui:roomSizeXScale animatable:false
		roomSizeYScale type:#float default:0.5 ui:roomSizeYScale animatable:false
		roomNumberXY type:#float default:1.0 ui:roomNumberXY animatable:false
		corridor type:#boolean default:false ui:corridor animatable:false
		
		glassReflectionMaskFactor type:#float default:1.0 ui:glassReflectionMaskFactor animatable:false
		glassDeformationFactor type:#float default:0.0 ui:glassDeformationFactor animatable:false
		
		fresnelFactor type:#float default:1.0 ui:fresnelFactor animatable:false
		fresnelOpacityOffset type:#float default:0.0 ui:fresnelOpacityOffset animatable:false
		
		SSSColor type:#point4 default:white ui:SSSColor animatable:false

		collisionMaterial type:#boolean default:false ui:collisionMaterial animatable:false
		roadMaterial type:#boolean default:false ui:roadMaterial animatable:false
		noCastShadow type:#boolean default:false ui:noCastShadow animatable:false
		AOUseUV2 type:#boolean default:false ui:AOUseUV2 animatable:false
		clampUVX type:#boolean default:false ui:clampUVX animatable:false
		clampUVY type:#boolean default:false ui:clampUVY animatable:false
		clampUVZ type:#boolean default:false ui:clampUVZ animatable:false

		responsiveAA type:#boolean default:false ui:responsiveAA animatable:false

		guid type:#string default:"00000000-0000-0000-0000-000000000000" ui:guid animatable:false

		on irradianceMap set val do
		(
			if val != undefined and getFullFilePath &val then
				delegate.p_irradianceTex = openBitmapGamma val gamma:1.0
			else
				delegate.p_irradianceTex = TexRadiance
		)

		on radianceMap set val do
		(
		    if val != undefined and getFullFilePath &val then
				delegate.p_radianceTex = openBitmapGamma val gamma:1.0
			else
				delegate.p_radianceTex = TexRadiance
		)

		on baseColor set val do
		(
			animate off delegate.p_baseColorFactor = val
		)

		on roughness set val do
		(
			animate off delegate.p_roughnessFactor = val
		)

		on metallic set val do
		(
			animate off delegate.p_metallicFactor = val
		)
		
		on emissive set val do
		(
			animate off delegate.p_emissiveFactor = val
		)
		
		on normalScale set val do
		(
			animate off delegate.p_normalScale = val
		)
		
		on alphaMode set val do
		(
			animate off delegate.p_alphaMode = this.alphaMode - 1
		)
		
		on drawOrder set val do
		(
			animate off delegate.p_drawOrder = val
		)
		
		on alphaCutoff set val do
		(
			animate off delegate.p_alphaCutoff = val
		)
		
		on detailUVScale set val do
		(
			animate off delegate.p_detailUVScale = val
		)
		
		on detailUVOffsetX set val do
		(
			animate off delegate.p_detailUVOffsetX = val
		)
		
		on detailUVOffsetY set val do
		(
			animate off delegate.p_detailUVOffsetY = val
		)
		
		on detailNormalScale set val do
		(
			animate off delegate.p_detailNormalScale = val
		)
		
		on blendThreshold set val do
		(
			animate off delegate.p_blendThreshold = val
		)
		
		on glassReflectionMaskFactor set val do
		(
			animate off delegate.p_glassReflectionMaskFactor = val
		)
		
		on glassDeformationFactor set val do
		(
			animate off delegate.p_glassDeformationFactor = val
		)
		
		on fresnelFactor set val do
		(
			animate off delegate.p_fresnelFactor = val
		)
		
		on fresnelOpacityOffset set val do
		(
			animate off delegate.p_fresnelOpacityOffset = val
		)
		
		on parallaxScale set val do
		(
			animate off delegate.p_parallaxScale = val
		)
		
		on roomSizeXScale set val do
		(
			animate off delegate.p_roomSizeXScale = val
		)
		
		on roomSizeYScale set val do
		(
			animate off delegate.p_roomSizeYScale = val
		)
		
		on roomNumberXY set val do
		(
			animate off delegate.p_roomNumberXY = val
		)

		on corridor set val do
		(
			animate off delegate.p_corridorEnabled = val
		)
		
		on SSSColor set val do
		(
			animate off delegate.p_SSSColorFactor = val
		)
		
		on doubleSided set val do
		(	
			--print "setting double sided funct"
			--format "this.doubleSided = % \n" this.
			---todo: optimize this changing just the techquinques
			loadShader()
		)
	)
	
	parameters textures rollout:texturesUI
	(
		BaseColorTex type:#filename assettype:#Bitmap
		OcclusionRoughnessMetallicTex type:#filename assettype:#Bitmap
		NormalTex type:#filename assettype:#Bitmap
		WetnessAOTex type:#filename assettype:#Bitmap --named like the sampler in engine side (for anisotropic)
		OpacityTex type:#filename assettype:#Bitmap --named like the sampler in engine side (for SSS)
		DirtTex type:#filename assettype:#Bitmap --named like the sampler in engine side (for clearCoat)
		HeightMapTex type:#filename assettype:#Bitmap --named like the sampler in engine side (for parallax Window)
		EmissiveTex type:#filename assettype:#Bitmap
		DetailColorTex type:#filename assettype:#Bitmap
		DetailOcclusionRoughnessMetallicTex type:#filename assettype:#Bitmap
		DetailNormalTex type:#filename assettype:#Bitmap
		BlendMaskTex type:#filename assettype:#Bitmap
		
		-- filenames
		on BaseColorTex set val do
		(
			if val != undefined and getFullFilePath &val then
				delegate.p_baseColorTex = openBitmapGamma val gamma:2.2
			else
				delegate.p_baseColorTex = TexWhite
		)

		on OcclusionRoughnessMetallicTex set val do
		(
			if val != undefined and getFullFilePath &val then
				delegate.p_occlusionRoughnessMetallicTex = openBitmapGamma val gamma:1.0
			else
				delegate.p_occlusionRoughnessMetallicTex = TexWhite
		)
		
		on NormalTex set val do
		(
			if val != undefined and getFullFilePath &val then
				delegate.p_normalTex = openBitmapGamma val gamma:1.0
			else
				delegate.p_normalTex = TexFlat
		)
		
		on WetnessAOTex set val do
		(
			if val != undefined and getFullFilePath &val then
				delegate.p_wetnessAOTex = openBitmapGamma val gamma:1.0
			else
				delegate.p_wetnessAOTex = TexFlat
		)
		
		on DirtTex set val do
		(
			if val != undefined and getFullFilePath &val then
				delegate.p_dirtTex = openBitmapGamma val gamma:1.0
			else
				delegate.p_dirtTex = TexGrey
		)
		
		on OpacityTex set val do
		(
			if val != undefined and getFullFilePath &val then
				delegate.p_opacityTex = openBitmapGamma val gamma:1.0
			else
				delegate.p_opacityTex = TexFlat
		)
		
		on EmissiveTex set val do
		(
			if val != undefined and getFullFilePath &val then
				delegate.p_emissiveTex = openBitmapGamma val gamma:2.2
			else
				delegate.p_emissiveTex = TexBlack
		)
		
		on DetailColorTex set val do
		(
			if val != undefined and getFullFilePath &val then
			(
				delegate.p_detailColorTex = openBitmapGamma val gamma:1.0
				delegate.p_detailColorEnabled = true
			)
			else
			(
				delegate.p_detailColorTex = TexGrey
				delegate.p_detailColorEnabled = false
			)
		)
		
		on DetailOcclusionRoughnessMetallicTex set val do
		(
			if val != undefined and getFullFilePath &val then
			(
				delegate.p_detailOcclusionRoughnessMetallicTex = openBitmapGamma val gamma:1.0
				delegate.p_detailOccRoughMetalEnabled = true
			)
			else
			(
				delegate.p_detailOcclusionRoughnessMetallicTex = TexWhite
				delegate.p_detailOccRoughMetalEnabled = false
			)
		)
		
		on DetailNormalTex set val do
		(
			if val != undefined and getFullFilePath &val then
			(
				delegate.p_detailNormalTex = openBitmapGamma val gamma:1.0
				delegate.p_detailNormalEnabled = true
			)
			else
			(
				delegate.p_detailNormalTex = TexFlat
				delegate.p_detailNormalEnabled = false
			)
		)
		
		on BlendMaskTex set val do
		(
			if val != undefined and getFullFilePath &val then
			(
				delegate.p_blendMaskTex = openBitmapGamma val gamma:1.0
				delegate.p_blendmaskEnabled = true
			)
			else
			(
				delegate.p_blendMaskTex = TexBlack
				delegate.p_blendmaskEnabled = false
			)
		)
	)
	
	rollout paramsUI "Parameters"
	(
		local maxWidth = paramsUI.width
		local halfMaxWidth = maxWidth * 0.4
		editText guid offset:[0, 0] align:#left enabled:false  width:maxWidth
		
        checkbox uniqueInContainer "Unique In Container Inheritance"  offset:[0,0] align:#left \
			tooltip:"Only in presence of duplicated container, and need a unique name"

		label materialTypeLab "Material Type:" across:2 offset:[0,3] align:#left
		dropdownlist materialType "" items:#("Standard","Decal","WindShield","PortHole","Glass","GeoDecalFrosted","ClearCoat","ParallaxWindow","Anisotropic","Hair","SSS","Invisible","FakeTerrain","FresnelFade","EnvironmentOccluder") offset:[-75,0]
		button chart "CHART" border:true offset:[0,-27] align:#right

		colorpicker baseColor "Base Color:" modal:false fieldWidth:30 height:20 align:#left across:2 \
			tooltip:"The RGBA components of the base color of the material. The fourth component (A) is the alpha coverage of the material. The alphaMode property specifies how alpha is interpreted. These values are linear. If a baseColorTexture is specified, this value is multiplied with the texel values."
		colorpicker emissive " Emissive:" modal:false fieldWidth:60 height:20 align:#left offset:[8,0] \
			tooltip:"The RGB components of the emissive color of the material. These values are linear. If an emissiveTexture is specified, this value is multiplied with the texel values."

		groupBox alphaModeBox "Alpha Mode:" height:90 width:halfMaxWidth
		radioButtons alphaMode "" labels:#("OPAQUE","MASK","BLEND","DITHER") columns:1 align:#left offset:[10,-80] \
			tooltip:#(
				"OPAQUE - The rendered output is fully opaque and any alpha value is ignored.",
				"MASK - The rendered output is either fully opaque or fully transparent depending on the alpha value and the specified alpha cutoff value. This mode is used to simulate geometry such as tree leaves or wire fences.",
				"BLEND - The rendered output is combined with the background using the normal painting operation (i.e. the Porter and Duff over operator). This mode is used to simulate geometry such as guaze cloth or animal fur.",
				"DITHER - The rendered output is blend with dithering dot patern"
				)

		groupBox renderFlagBox "Render Param:" height:110 width:halfMaxWidth offset:[0,10]
		spinner drawOrder "Draw Order:" type:#integer range:[-999,999,0] fieldWidth:30 offset:[10,-98] align:#left\
			tooltip:"Draw Order Offset, to manually sort decals draw order for example"
		checkbox noCastShadow "no Cast Shadow" offset:[10,0] align:#left \
			tooltip:"no Cast Shadow"
		checkbox doubleSided "Double Sided" offset:[10,0] align:#left \
			tooltip:"The doubleSided property specifies whether the material is double sided. When this value is false, back-face culling is enabled. When this value is true, back-face culling is disabled and double sided lighting is enabled. The back-face must have its normals reversed before the lighting equation is evaluated."
		checkbox responsiveAA "Responsive AA" offset:[10,0] align:#left \
			tooltip:"The responsiveAA property specifies the behaviour of material regarding temporal Anti Aliasing. When this value is false, temporal AA is enabled. When this value is true, temporal AA is disabled ."

		groupBox gameplayBox "Gameplay param:" height:58 width:halfMaxWidth offset:[0,20]
		checkbox collisionMaterial "Collision Material" offset:[10,-46] align:#left tooltip:"Collision Material"
		checkbox roadMaterial "Road Material" offset:[10,0] align:#left \
		tooltip:"Road Material"

		groupBox UVParams "UVs options:" height:80 width:halfMaxWidth offset:[0,5]
		groupBox UVClampParams "UV Clamp:" height:40 width:(halfMaxWidth-10) offset:[4,-50]
		checkbox AOUseUV2 "AO Use UV2" offset:[10,-63] align:#left \
			tooltip:"AO use UV2"
		checkbox ClampUVX "X" offset:[10,15] align:#left \
		checkbox ClampUVY "Y" offset:[40,-19] across:2 align:#left \
		checkbox ClampUVZ "Z" offset:[-80,-19] align:#left \

		--groupBox usualMaterialBox "material param:" height:250 width:200
		local usualMaterialOffsetY = -272
		spinner roughness "Roughness:" range:[0,1,1] scale:0.01 fieldWidth:40 align:#right offset:[0,usualMaterialOffsetY] \
			tooltip:"The roughness of the material. A value of 1.0 means the material is completely rough. A value of 0.0 means the material is completely smooth. This value is linear. If a metallicRoughnessTexture is specified, this value is multiplied with the roughness texel values."
		spinner metallic "Metallic:" range:[0,1,1] scale:0.01 fieldWidth:40 align:#right \
			tooltip:"The metalness of the material. A value of 1.0 means the material is a metal. A value of 0.0 means the material is a dielectric. Values in between are for blending between metals and dielectrics such as dirty metallic surfaces. This value is linear. If a metallicRoughnessTexture is specified, this value is multiplied with the metallic texel values."
		spinner normalScale "Normal Scale:" range:[0,1,1] scale:0.01 fieldWidth:40 align:#right \
			tooltip:"The scalar multiplier applied to each normal vector of the texture. This value is ignored if normalTexture is not specified."
		spinner alphaCutoff "Alpha Cutoff:" range:[0,1,1] scale:0.01 fieldWidth:40 align:#right \
			tooltip:"When alphaMode is set to MASK the alphaCutoff property specifies the cutoff threshold. If the alpha value is greater than or equal to the alphaCutoff value then it is rendered as fully opaque, otherwise, it is rendered as fully transparent. alphaCutoff value is ignored for other modes."
		spinner detailUVScale "Detail UV Scale:" range:[0.01,100,2] scale:0.01 fieldWidth:40 align:#right \
			tooltip:"Detail UV Scale"
		spinner detailUVOffsetX "Detail UV Offset X:" range:[-10.00,10.00,0.0] scale:0.01 fieldWidth:40 align:#right \
			tooltip:"Detail UV Offset X"
		spinner detailUVOffsetY "Detail UV Offset Y:" range:[-10.00,10.00,0.0] scale:0.01 fieldWidth:40 align:#right \
			tooltip:"Detail UV Offset Y"
		spinner detailNormalScale "Detail Normal Scale:" range:[0.00,1.00,1.0] scale:0.01 fieldWidth:40 align:#bottomright \
			tooltip:"Detail Normal Scale"
		spinner blendThreshold "Blend Threshold:" range:[0.001,1.000,0.100] scale:0.01 fieldWidth:40 align:#right \
			tooltip:"Blend Threshold need blendMask Tex"

		local decalOffsetY = 90
		groupBox decalBox "Decal per component blend factors:" height:85 width:maxWidth offset:[0, decalOffsetY]
		spinner decalColorFactor "Color:" 					range:[0,1,1] scale:0.01 fieldWidth:40 align:#right offset:[-50,-70] across:2
		spinner decalRoughnessFactor "Roughness:" 	range:[0,1,1] scale:0.01 fieldWidth:40 align:#right offset:[-80,-70]
		spinner decalMetalFactor "Metal:" 					range:[0,1,1] scale:0.01 fieldWidth:40 align:#right offset:[-50,0] across:2
		spinner decalOcclusionFactor "Occlusion:" 		range:[0,1,1] scale:0.01 fieldWidth:40 align:#right offset:[-80,0]
		spinner decalNormalFactor "Normal:" 				range:[0,1,1] scale:0.01 fieldWidth:40 align:#right offset:[-50,0] across:2
		spinner decalEmissiveFactor "Emissive:" 			range:[0,1,1] scale:0.01 fieldWidth:40 align:#right offset:[-80,0]

		local SSSBoxOffsetY = -80.0
		groupBox SSSbox "SSS parameters:" height:50 width:maxWidth offset:[0, SSSBoxOffsetY]
		colorpicker SSSColor "SSS Color" modal:false fieldWidth:30 height:20 align:#right offset:[-50,SSSBoxOffsetY+45] across:2 \
			tooltip:"The RGBA components of the SSS color of the material. These values are linear. If a SSSTexture is specified, this value is multiplied with the texel values."

		local GlassBoxOffsetY = -80
		groupBox GlassBox "Glass parameters:" height:64 width:maxWidth offset:[-160, GlassBoxOffsetY]
		spinner glassReflectionMaskFactor "Glass Reflection Mask Factor:" range:[0.000,1.000,0.000] scale:0.01 fieldWidth:40 offset:[-80, -52] align:#right \
			tooltip:"Glass Reflection Mask Factor"
		spinner glassDeformationFactor "Glass Deformation Factor:" range:[0.000,1.000,0.000] scale:0.01 fieldWidth:40 offset:[-80, 0] align:#right \
			tooltip:"Glass Deformation Factor"

		local ParallaxBoxOffsetY = -50
		groupBox ParallaxBox "Parallax parameters:" height:130 width:maxWidth offset:[0, ParallaxBoxOffsetY]
		spinner parallaxScale "Parallax scale:" range:[0.000,1.000,0.500] scale:0.01 fieldWidth:40 offset:[-150, -115] align:#right \
			tooltip:"Parallax scale"
		spinner roomSizeXScale "room SizeX Scale:" range:[0.01,10.000,0.500] scale:0.01 fieldWidth:40 offset:[-150, 0] align:#right \
			tooltip:"room SizeX Scale"
		spinner roomSizeYScale "room SizeY Scale:" range:[0.01,10.000,0.500] scale:0.01 fieldWidth:40 offset:[-150, 0] align:#right \
			tooltip:"room SizeY Scale"
		spinner roomNumberXY "room number XY:" range:[1,16,2] scale:1 fieldWidth:40 offset:[-150, 0] align:#right \
			tooltip:"room Number XY"
		checkbox corridor "Corridor" offset:[20, 0] align:#left tooltip:"Use as a corridor"

		local fresnelBoxOffsetY = -90
		groupBox fresnelBox "Fresnel parameters:" height:70 width:maxWidth offset:[0, fresnelBoxOffsetY]
		spinner fresnelFactor "Fresnel Factor:" range:[0.001,100.000,1.000] scale:0.01 fieldWidth:40 offset:[-80,-55] align:#right \
			tooltip:"Fresnel Factor"
		spinner fresnelOpacityOffset "Fresnel Opacity Offset:" range:[-1.0,1.0,0.000] scale:0.01 fieldWidth:40 offset:[-80, 0] align:#right \
			tooltip:"Fresnel Opacity Offset"		
			
		
		

		fn updateUI =
		(
			emissive.enabled = not(matList[materialType.selection] == #Invisible or matList[materialType.selection] == #EnvironmentOccluder)
			roughness.enabled = not(matList[materialType.selection] == #Invisible or matList[materialType.selection] == #EnvironmentOccluder)
			metallic.enabled = not(matList[materialType.selection] == #Invisible or matList[materialType.selection] == #EnvironmentOccluder)
			normalScale.enabled = not(matList[materialType.selection] == #Invisible or matList[materialType.selection] == #EnvironmentOccluder)
			blendThreshold.enabled = not(matList[materialType.selection] == #Invisible or matList[materialType.selection] ==#FresnelFade or matList[materialType.selection] == #EnvironmentOccluder)
			doubleSided.enabled = not(matList[materialType.selection] == #Invisible or matList[materialType.selection] == #EnvironmentOccluder)
			responsiveAA.enabled = not(matList[materialType.selection] == #Invisible or matList[materialType.selection] == #EnvironmentOccluder)

			UVParams.enabled = not(matList[materialType.selection] == #Invisible or matList[materialType.selection] == #EnvironmentOccluder)
			AOUseUV2.enabled = not(matList[materialType.selection] == #Invisible or matList[materialType.selection] == #EnvironmentOccluder)
			renderFlagBox.enabled = not(matList[materialType.selection] == #Invisible or matList[materialType.selection] == #EnvironmentOccluder)
			drawOrder.enabled = not(matList[materialType.selection] == #Invisible or matList[materialType.selection] == #EnvironmentOccluder)
			noCastShadow.enabled = not(matList[materialType.selection] == #Invisible or matList[materialType.selection] == #EnvironmentOccluder)

			alphaMode.enabled = alphaModeBox.enabled = (matList[materialType.selection] == #Standard or ( materialType.selection >= 7 and  materialType.selection <= 11) or matList[materialType.selection] == #FresnelFade)
			alphaCutoff.enabled = alphaMode.enabled and alphaMode.state == 2

			decalBox.visible = (matList[materialType.selection] == #Decal or matList[materialType.selection] == #GeoDecalFrosted)
			decalColorFactor.visible = (matList[materialType.selection] == #Decal or matList[materialType.selection] == #GeoDecalFrosted)
			decalRoughnessFactor.visible = (matList[materialType.selection] == #Decal or matList[materialType.selection] == #GeoDecalFrosted)
			decalMetalFactor.visible = (matList[materialType.selection] == #Decal or matList[materialType.selection] == #GeoDecalFrosted)
			decalOcclusionFactor.visible = (matList[materialType.selection] == #Decal or matList[materialType.selection] == #GeoDecalFrosted)
			decalNormalFactor.visible = (matList[materialType.selection] == #Decal or matList[materialType.selection] == #GeoDecalFrosted)
			decalEmissiveFactor.visible = (matList[materialType.selection] == #Decal or matList[materialType.selection] == #GeoDecalFrosted)

			SSSbox.visible = (matList[materialType.selection] == #SSS or matList[materialType.selection] == #Hair)
			SSSColor.visible = (matList[materialType.selection] == #SSS or matList[materialType.selection] == #Hair)
			SSSColor.enabled =(matList[materialType.selection] == #SSS or matList[materialType.selection] == #Hair)

			GlassBox.visible = (matList[materialType.selection] == #Glass)
			GlassBox.enabled = (matList[materialType.selection] == #Glass)
			glassReflectionMaskFactor.visible = (matList[materialType.selection] == #Glass)
			glassReflectionMaskFactor.enabled = (matList[materialType.selection] == #Glass)
			glassDeformationFactor.visible = (matList[materialType.selection] == #Glass)
			glassDeformationFactor.enabled = (matList[materialType.selection] == #Glass)

			fresnelBox.visible = (matList[materialType.selection] == #FresnelFade)
			fresnelBox.enabled = (matList[materialType.selection] == #FresnelFade)
			fresnelFactor.visible = (matList[materialType.selection] == #FresnelFade)
			fresnelFactor.enabled = (matList[materialType.selection] == #FresnelFade)
			fresnelOpacityOffset.visible = (matList[materialType.selection] == #FresnelFade)
			fresnelOpacityOffset.enabled = (matList[materialType.selection] == #FresnelFade)

			--if parallax, we don't have a detail map.
			detailUVScale.enabled = not(matList[materialType.selection] == #ParallaxWindow or matList[materialType.selection] == #Invisible or matList[materialType.selection] == #FresnelFade or matList[materialType.selection] == #EnvironmentOccluder)
			detailUVOffsetX.enabled = not(matList[materialType.selection] == #ParallaxWindow or matList[materialType.selection] == #Invisible or matList[materialType.selection] == #FresnelFade or matList[materialType.selection] == #EnvironmentOccluder)
			detailUVOffsetY.enabled = not(matList[materialType.selection] == #ParallaxWindow or matList[materialType.selection] == #Invisible or matList[materialType.selection] == #FresnelFade or matList[materialType.selection] == #EnvironmentOccluder)
			detailNormalScale.enabled = not(matList[materialType.selection] == #ParallaxWindow or matList[materialType.selection] == #Invisible or matList[materialType.selection] == #FresnelFade or matList[materialType.selection] == #EnvironmentOccluder)
			ParallaxBox.visible = (matList[materialType.selection] == #ParallaxWindow)
			parallaxScale.visible = (matList[materialType.selection] == #ParallaxWindow)
			parallaxScale.enabled = (matList[materialType.selection] == #ParallaxWindow)
			roomSizeXScale.visible =  (matList[materialType.selection] == #ParallaxWindow)
			roomSizeXScale.enabled =  (matList[materialType.selection] == #ParallaxWindow)
			roomSizeYScale.visible =  (matList[materialType.selection] == #ParallaxWindow)
			roomSizeYScale.enabled =  (matList[materialType.selection] == #ParallaxWindow)
			roomNumberXY.visible =  (matList[materialType.selection] == #ParallaxWindow)
			roomNumberXY.enabled =  (matList[materialType.selection] == #ParallaxWindow)
			corridor.visible =  (matList[materialType.selection] == #ParallaxWindow)
			corridor.enabled = (matList[materialType.selection] == #ParallaxWindow)

            UVClampParams.enabled = not(matList[materialType.selection] == #EnvironmentOccluder)
			clampUVX.enabled = not(matList[materialType.selection] == #EnvironmentOccluder)
			clampUVY.enabled = not(matList[materialType.selection] == #EnvironmentOccluder)
			clampUVZ.enabled = not(matList[materialType.selection] == #EnvironmentOccluder)

			gameplayBox.enabled = not(matList[materialType.selection] == #EnvironmentOccluder)


			collisionMaterial.enabled = not(matList[materialType.selection] == #EnvironmentOccluder)
			roadMaterial.enabled = not(matList[materialType.selection] == #EnvironmentOccluder)

            if(paramsUI.guid.text == "00000000-0000-0000-0000-000000000000") then
            (
                guid.visible = false
            )
            else
            (
                guid.visible = true
            )
			if (matList[materialType.selection] == #GeoDecalFrosted) then
			(
				decalEmissiveFactor.text = "Melt Sys:"
				decalOcclusionFactor.text = "Blast Sys:"
			)
			else
			(
				decalEmissiveFactor.text = "Emissive:"
				decalOcclusionFactor.text = "Occlusion:"
			)

			--if (matList[materialType.selection] == #Decal or matList[materialType.selection] == #GeoDecalFrosted) then
			--(
			--	paramsUI.height = 650
			--)
			--else if(matList[materialType.selection] == #Glass) then -- glass
			--(
			--	paramsUI.height = 600
			--)
			--else if(matList[materialType.selection] == #ParallaxWindow) then --parallax
			--(
			--	paramsUI.height = 650
			--)
			--else if(matList[materialType.selection] == #Hair or matList[materialType.selection] == #SSS) then --SSS ou Hair
			--(
			--	paramsUI.height = 650
			--)
			--else if(matList[materialType.selection] == #FresnelFade) then --fresnel fade
			--(
			--	paramsUI.height = 650
			--)
			--else
			--(
			--	paramsUI.height  = 650
			--)
		)

		on materialType selected val do
		(
			updateGlobalUI()
			loadShader()
			completeRedraw()
		)

		on alphaMode changed val do
		(
			updateUI()
		)

		on paramsUI open do
		(
			paramsUI.open = FlightSim_paramsRolledUp
			updateUI()
		)

		on paramsUI rolledUp state do
		(
			FlightSim_paramsRolledUp = state
		)

		on chart pressed do filein "FlightSim_Chart.ms"
	)

	rollout texturesUI "Textures"
	(
		local maxWidth = texturesUI.width
		local btnStyle = (dotNetClass "System.Windows.Forms.FlatStyle").flat -- Flat / Popup / Standard / System
		local btnColor = (dotnetclass "system.drawing.color").FromArgb 68 68 68
		local btnFont = dotNetObject "System.Drawing.Font" "Microsoft Sans Serif" 9 (dotNetClass "System.Drawing.FontStyle").bold
		local btnTooltip = dotnetobject "System.Windows.Forms.ToolTip"

		dotnetcontrol	BaseColorTexBtn "system.windows.forms.button" \
			AllowDrop:true FlatStyle:btnStyle backColor:btnColor font:btnFont \
			width:maxWidth height:32

		dotnetcontrol	OcclusionRoughnessMetallicTexBtn "system.windows.forms.button" \
			AllowDrop:true FlatStyle:btnStyle backColor:btnColor font:btnFont \
			width:maxWidth height:32

		dotnetcontrol	NormalTexBtn "system.windows.forms.button" \
			AllowDrop:true FlatStyle:btnStyle backColor:btnColor font:btnFont \
			width:maxWidth height:32

		dotnetcontrol	EmissiveTexBtn "system.windows.forms.button" \
			AllowDrop:true FlatStyle:btnStyle backColor:btnColor font:btnFont \
			width:maxWidth height:32

		dotnetcontrol	DetailColorTexBtn "system.windows.forms.button" \
			AllowDrop:true FlatStyle:btnStyle backColor:btnColor font:btnFont \
			width:maxWidth height:32

		dotnetcontrol	DetailOcclusionRoughnessMetallicTexBtn "system.windows.forms.button" \
			AllowDrop:true FlatStyle:btnStyle backColor:btnColor font:btnFont \
			width:maxWidth height:32

		dotnetcontrol	DetailNormalTexBtn "system.windows.forms.button" \
			AllowDrop:true FlatStyle:btnStyle backColor:btnColor font:btnFont \
			width:maxWidth height:32

		dotnetcontrol	BlendMaskTexBtn "system.windows.forms.button" \
			AllowDrop:true FlatStyle:btnStyle backColor:btnColor font:btnFont \
			width:maxWidth height:32

		dotnetcontrol	WetnessAOTexBtn "system.windows.forms.button" \
			AllowDrop:true FlatStyle:btnStyle backColor:btnColor font:btnFont \
			width:maxWidth height:32

		dotnetcontrol	DirtTexBtn "system.windows.forms.button" \
			AllowDrop:true FlatStyle:btnStyle backColor:btnColor font:btnFont \
			width:maxWidth height:32

		dotnetcontrol	HeightMapTexBtn "system.windows.forms.button" \
			AllowDrop:true FlatStyle:btnStyle backColor:btnColor font:btnFont \
			width:maxWidth height:32

		dotnetcontrol	OpacityTexBtn "system.windows.forms.button" \
			AllowDrop:true FlatStyle:btnStyle backColor:btnColor font:btnFont \
			width:maxWidth height:32


		-- variable contenant le nom de la texture cibl�e lors du clic droit
		local activeTex

		-- disabled all texture slot
		fn disabledAllTextureSlot =
		(
			this.texturesUI.BaseColorTexBtn.text = "disabled"
			this.texturesUI.OcclusionRoughnessMetallicTexBtn.text = "disabled"
			this.texturesUI.NormalTexBtn.text = "disabled"
			this.texturesUI.EmissiveTexBtn.text = "disabled"
			this.texturesUI.DetailColorTexBtn.text = "disabled"
			this.texturesUI.DetailNormalTexBtn.text = "disabled"
			this.texturesUI.DetailOcclusionRoughnessMetallicTexBtn.text = "disabled"
			this.texturesUI.BlendMaskTexBtn.text = "disabled"
			this.texturesUI.WetnessAOTexBtn.text = "disabled"
			this.texturesUI.DirtTexBtn.text = "disabled"
			this.texturesUI.HeightMapTexBtn.text = "disabled"
			---
			this.texturesUI.BaseColorTexBtn.enabled = false
			this.texturesUI.OcclusionRoughnessMetallicTexBtn.enabled = false
			this.texturesUI.NormalTexBtn.enabled = false
			this.texturesUI.EmissiveTexBtn.enabled = false
			this.texturesUI.DetailColorTexBtn.enabled = false
			this.texturesUI.DetailNormalTexBtn.enabled = false
			this.texturesUI.DetailOcclusionRoughnessMetallicTexBtn.enabled = false
			this.texturesUI.BlendMaskTexBtn.enabled = false
			this.texturesUI.WetnessAOTexBtn.enabled = false
			this.texturesUI.DirtTexBtn.enabled = false
			this.texturesUI.HeightMapTexBtn.enabled = false
		)

		-- slot name update
		fn updateUiNames =
		(
			for texName in TexList do
				(getProperty this.texturesUI (texName+"TexBtn")).Font = btnFont

			--init
			(
				this.texturesUI.BaseColorTexBtn.enabled = true
				this.texturesUI.OcclusionRoughnessMetallicTexBtn.enabled = true
				this.texturesUI.NormalTexBtn.enabled = true
				this.texturesUI.EmissiveTexBtn.enabled = true
				this.texturesUI.BaseColorTexBtn.text = "Base Color"
				this.texturesUI.OcclusionRoughnessMetallicTexBtn.text = "Occlusion (R), Roughness (G), Metallic (B)"
				this.texturesUI.NormalTexBtn.text = "Normal"
				this.texturesUI.EmissiveTexBtn.text = "Emissive"

				this.texturesUI.BlendMaskTexBtn.enabled = true
				this.texturesUI.BlendMaskTexBtn.text = "Blend Mask"

				this.texturesUI.DetailColorTexBtn.enabled = true
				this.texturesUI.DetailNormalTexBtn.enabled = true
				this.texturesUI.DetailOcclusionRoughnessMetallicTexBtn.enabled = true

				if(BlendMaskTex == "") then
				(
					this.texturesUI.DetailColorTexBtn.text = "Detail Color (RGB), Alpha (A)"
					this.texturesUI.DetailNormalTexBtn.text = "Detail Normal"
					this.texturesUI.DetailOcclusionRoughnessMetallicTexBtn.text = "Detail Occlusion (R), Roughness (G), Metallic (B)"
					delegate.p_blendmaskEnabled = false
				)
				else
				(
					this.texturesUI.DetailColorTexBtn.text = "Secondary Color (RGB), Alpha (A)"
					this.texturesUI.DetailNormalTexBtn.text = "Secondary Normal"
					this.texturesUI.DetailOcclusionRoughnessMetallicTexBtn.text = "Secondary Occ (R), Rough (G), Metal (B)"
					delegate.p_blendmaskEnabled = true
				)

				this.texturesUI.HeightMapTexBtn.enabled = false
				this.texturesUI.HeightMapTexBtn.text = "disabled"
				this.texturesUI.DirtTexBtn.enabled = false
				this.texturesUI.DirtTexBtn.text = "disabled"
				this.texturesUI.WetnessAOTexBtn.enabled = false
				this.texturesUI.WetnessAOTexBtn.text = "disabled"
			)


			case matList[this.materialType] of
			(
				#Windshield: --WindShield
				(
					this.texturesUI.WetnessAOTexBtn.enabled = true
					this.texturesUI.WetnessAOTexBtn.text = "Wiper Mask (RG)"
				)
				#GeoDecalFrosted: --GeoDecalFrosted
				(
					this.texturesUI.BlendMaskTexBtn.enabled = false
					this.texturesUI.BlendMaskTexBtn.text = "disabled"
					this.texturesUI.DetailOcclusionRoughnessMetallicTexBtn.text = "Melt patern (R), Roughness (G), Metallic (B)"
					delegate.p_blendmaskEnabled = false
				)
				#ClearCoat:
				(
					this.texturesUI.DirtTexBtn.enabled = true
					this.texturesUI.DirtTexBtn.text = "Clearcoat amount (R), Clearcoat rough (G)"
				)
				#ParallaxWindow:
				(
					this.texturesUI.BaseColorTexBtn.text = "Front Glass Color"
					this.texturesUI.OcclusionRoughnessMetallicTexBtn.text = "Occlusion (R), Roughness (G), Metallic (B)"
					this.texturesUI.NormalTexBtn.text = "Front Glass Normal"
					this.texturesUI.DetailColorTexBtn.enabled = true
					this.texturesUI.DetailColorTexBtn.text = "Behind Glass Color (RGB), Alpha (A)"
					this.texturesUI.EmissiveTexBtn.enabled = true
					this.texturesUI.EmissiveTexBtn.text = "Emissive Ins Window (RGB), offset Time (A)"
					this.texturesUI.DetailNormalTexBtn.enabled = false
					this.texturesUI.DetailNormalTexBtn.text = "disabled"
					this.texturesUI.DetailOcclusionRoughnessMetallicTexBtn.enabled = false
					this.texturesUI.DetailOcclusionRoughnessMetallicTexBtn.text = "disabled"
					this.texturesUI.BlendMaskTexBtn.enabled = false
					this.texturesUI.BlendMaskTexBtn.text = "disabled"
					this.texturesUI.HeightMapTexBtn.enabled = false
					this.texturesUI.HeightMapTexBtn.text = "disabled"
				)
				#Anisotropic:
				(
					this.texturesUI.WetnessAOTexBtn.enabled = true
					this.texturesUI.WetnessAOTexBtn.text = "anisotropic direction (RG)"
				)
				#Hair:
				(
					this.texturesUI.WetnessAOTexBtn.enabled = true
					this.texturesUI.WetnessAOTexBtn.text = "anisotropic direction (RG)"
					 this.texturesUI.DetailColorTexBtn.enabled = false
					this.texturesUI.DetailColorTexBtn.text = "disabled"
					this.texturesUI.DetailNormalTexBtn.enabled = false
					this.texturesUI.DetailNormalTexBtn.text = "disabled"
					this.texturesUI.DetailOcclusionRoughnessMetallicTexBtn.enabled = false
					this.texturesUI.DetailOcclusionRoughnessMetallicTexBtn.text = "disabled"
					this.texturesUI.BlendMaskTexBtn.enabled = false
					this.texturesUI.BlendMaskTexBtn.text = "disabled"
				)
				#SSS:
				(
					 this.texturesUI.DetailColorTexBtn.enabled = false
					this.texturesUI.DetailColorTexBtn.text = "disabled"
					this.texturesUI.DetailNormalTexBtn.enabled = false
					this.texturesUI.DetailNormalTexBtn.text = "disabled"
					this.texturesUI.DetailOcclusionRoughnessMetallicTexBtn.enabled = false
					this.texturesUI.DetailOcclusionRoughnessMetallicTexBtn.text = "disabled"
					this.texturesUI.BlendMaskTexBtn.enabled = false
					this.texturesUI.BlendMaskTexBtn.text = "disabled"
				)
				#Invisible:
				(
					disabledAllTextureSlot()
				)
				#FresnelFade:
				(
					this.texturesUI.BlendMaskTexBtn.enabled = false
					this.texturesUI.BlendMaskTexBtn.text = "disabled"
					this.texturesUI.DetailColorTexBtn.enabled = false
					this.texturesUI.DetailColorTexBtn.text = "disabled"
					this.texturesUI.DetailNormalTexBtn.enabled = false
					this.texturesUI.DetailNormalTexBtn.text = "disabled"
					this.texturesUI.DetailOcclusionRoughnessMetallicTexBtn.enabled = false
					this.texturesUI.DetailOcclusionRoughnessMetallicTexBtn.text = "disabled"
				)
				#EnvironmentOccluder:
				(
				    disabledAllTextureSlot()
				)

			)
		)

		-- function update the display of texture (UI only) and tooltip
		fn updateUiBm basename =
		(
			local filename = getProperty this (basename + "Tex")
			local btn = getProperty this.texturesUI (basename + "TexBtn")
			if filename != "" and filename != undefined then
			(
				if getFullFilePath &filename then
				(
					-- Image
					local tex
					try( tex	= getProperty delegate (getDelTexPName basename) )
					catch( tex = undefined )
					if tex == undefined then tex = openBitMap filename
					mxs2dotBmp tex &btn.Image
					
					-- TFlags
					local TFlagsFile = getFilenamePath filename + (filenameFromPath filename) + ".FLAGS"
					local TFlags = ""
					local stream = openFile TFlagsFile
					if stream != undefined then
					(
						TFlags = "TFlags:\n"
						TFlags += readDelimitedString stream #eof
						close stream
					)
					
					-- Tooltip
					local bminfo = getBitmapInfo tex
					
					local txt = btn.text + "\n" \
						+ filename + "\n" \
						+ bminfo[3] as string + "*"+ bminfo[4] as string + " Alpha:" + bminfo[9] as string + " Bits:" + bminfo[5] as string + "\n" \
						+ TFlags
					
					btnTooltip.SetToolTip btn txt
					
					gc light:true
				)
				else
				(
					mxs2dotBmp (bitmap 210 4 color:red) &btn.Image
					btnTooltip.SetToolTip btn ("FILE NOT FOUND\n" + filename)
				)
			)
			else
			(
				btn.Image = undefined
				btnTooltip.SetToolTip btn ""
			)
		)

		fn updateUiBmAll =
		(
			for texName in TexList do
				updateUiBm texName
		)

		-- update tooltips base name
		fn updateUiTooltip basename =
		(
			local btn = getProperty this.texturesUI (basename + "TexBtn")
			local txt = btnTooltip.GetToolTip btn
			if txt != "" then
			(
				txt = replace txt 1 ((findString txt "\n")-1) btn.text
				btnTooltip.SetToolTip btn txt
			)
		)
		
		-- update tooltips flags
		fn updateUiFlags basename =
		(
			local filename = getProperty this (basename + "Tex")
			local btn = getProperty this.texturesUI (basename + "TexBtn")
			if filename != "" then
			(
				if getFullFilePath &filename then
				(
					local TFlagsFile = getFilenamePath filename + (filenameFromPath filename) + ".FLAGS"
					local TFlags = ""
					local stream = openFile TFlagsFile
					if stream != undefined then
					(
						TFlags = "TFlags:\n"
						TFlags += readDelimitedString stream #eof
						close stream
					)
					
					local txt = btnTooltip.GetToolTip btn
					local pos = findString txt "TFlags"
					if pos != undefined then
					(
						txt = (substring txt 1 (pos-1)) + TFlags
						btnTooltip.SetToolTip btn txt
					)
				)
			)
		)

		fn updateUI =
		(
			updateUiNames()
			updateUiBmAll()
		)

		on texturesUI open do
		(
			texturesUI.open = FlightSim_texturesRolledUp
			if not loading and this.delegate != undefined then --"loading" send true before that the delegate is defined
				updateUI()
		)

		on texturesUI rolledUp state do
		(
			FlightSim_texturesRolledUp = state
		)

		on texturesUI reload do
		(
			if this.delegate != undefined then  --"loading" send true before that the delegate is defined
			(
				updateUiBmAll()
			)
		)

		-- bitmaps loading
		fn loadTex filename basename =
		(
			local localHolding = false
			if (theHold.holding() == false) do
			(
				theHold.begin()
				localHolding = true
			)

			try
			(
				animate off
				(
					filename = pathConfig.convertPathToRelativeTo filename (pathConfig.getCurrentProjectFolder())
					setProperty this (basename + "Tex") filename
					updateUiBm basename

					if (theHold.holding() == true and localHolding) do
						theHold.accept ("Mtl : Load Texture" + " (" + basename + ")")
				)
			)
			catch
			(
				if (theHold.holding() == true and localHolding) do
					theHold.Cancel()
			)
		)

		-- bitmaps deleting
		fn clearTex basename =
		(
			local localHolding = false
			if (theHold.holding() == false) do
			(
				theHold.begin()
				localHolding = true
			)

			try
			(
				animate off
				(
					local tex = (basename + "Tex") as name
					setProperty this tex ""
					updateUiBm basename

					if (theHold.holding() == true and localHolding) do
						theHold.accept ("Mtl : Clear Texture" + " (" + basename + ")")
				)
			)
			catch
			(
				if (theHold.holding() == true and localHolding) do
					theHold.Cancel()
			)

			if(basename == "BlendMask") do
			(
				updateUiNames()
				delegate.p_blendmaskEnabled = false
			)

			if(basename == "DetailColor") do
			(
				updateUiNames()
				delegate.p_detailColorEnabled = false
			)

			if(basename == "DetailNormal") do
			(
				updateUiNames()
				delegate.p_detailNormalEnabled = false
			)

			if(basename == "DetailOcclusionRoughnessMetallic") do
			(
				updateUiNames()
				delegate.p_detailOccRoughMetalEnabled = false
			)


		)

		fn loadLinked filename basename =
		(			
			if basename == "BaseColor"  and filename!=undefined	then
			(				
				-- filename	=	(pathconfig.convertPathToAbsolute 	(pathconfig.appendpath 	(pathConfig.getCurrentProjectFolder())	filename	)	)
				local cpath = getFilenamePath filename
				local cname = getFilenameFile filename
				local	ctype = getFilenameType	filename
				local offset = findString (tolower  cname) "albedo"


				if offset != undefined then		--		nommenclature 1 (airport)
				(
					cname = substring cname 1 (offset-1)
					local comp = pathConfig.appendPath cpath (cname + "COMP"+ctype)
					local nmap = pathConfig.appendPath cpath (cname + "Normal"+ctype)
					local	emiss = pathConfig.appendPath cpath (cname + "Emissive"+ctype)
					if this.NormalTex == "" and doesFileExist nmap then
						loadTex (pathConfig.convertPathToRelativeTo  nmap (pathConfig.getCurrentProjectFolder())) "Normal"
					if this.OcclusionRoughnessMetallicTex == "" and doesFileExist comp then
						loadTex (pathConfig.convertPathToRelativeTo  comp (pathConfig.getCurrentProjectFolder())) "OcclusionRoughnessMetallic"
					if this.EmissiveTex == "" and doesFileExist emiss then
						loadTex (pathConfig.convertPathToRelativeTo  emiss (pathConfig.getCurrentProjectFolder())) "Emissive"
				)
				else										--		nommenclature 2 (planes)
				(
					offset = findString (tolower  cname) "_albd"
					if offset != undefined then
					(
						cname = substring cname 1 (offset-1)
						local comp = pathConfig.appendPath cpath (cname + "_comp"+ctype)
						local nmap = pathConfig.appendPath cpath (cname + "_norm"+ctype)
						local	emiss = pathConfig.appendPath cpath (cname + "_emis"+ctype)
						if this.NormalTex == "" and doesFileExist nmap then
							loadTex (pathConfig.convertPathToRelativeTo  nmap (pathConfig.getCurrentProjectFolder())) "Normal"
						if this.OcclusionRoughnessMetallicTex == "" and doesFileExist comp then
							loadTex (pathConfig.convertPathToRelativeTo  comp (pathConfig.getCurrentProjectFolder())) "OcclusionRoughnessMetallic"
						if this.EmissiveTex == "" and doesFileExist emiss then
							loadTex (pathConfig.convertPathToRelativeTo  emiss (pathConfig.getCurrentProjectFolder())) "Emissive"
					)
				)
			)

			if(basename == "BlendMask") do
			(
				updateUiNames()
			)

			if(basename == "DetailColor") do
			(
				updateUiNames()
				delegate.p_detailColorEnabled = true
			)

			if(basename == "DetailNormal") do
			(
				updateUiNames()
				delegate.p_detailNormalEnabled = true
			)

			if(basename == "DetailOcclusionRoughnessMetallic") do
			(
				updateUiNames()
				delegate.p_detailOccRoughMetalEnabled = true
			)
		)

		fn browseTex basename =
		(
			local curPath = getProperty this (basename + "Tex")
			local filename = getOpenFileName caption:basename filename:(pathConfig.convertPathToAbsolute	curPath) historyCategory:"FlightSimHistory" types:filesTypes
			if filename != undefined then
				loadTex 		filename basename
				loadLinked	filename basename

			if(basename == "BlendMask") do
			(
				updateUiNames()
			)

			if(basename == "DetailColor") do
			(
				updateUiNames()
				delegate.p_detailColorEnabled = true
			)

			if(basename == "DetailNormal") do
			(
				updateUiNames()
				delegate.p_detailNormalEnabled = true
			)

			if(basename == "DetailOcclusionRoughnessMetallic") do
			(
				updateUiNames()
				delegate.p_detailOccRoughMetalEnabled = true
			)
		)

		-- right clic menu
		fn rightclickMenu basename =
		(
			ActiveTex = basename --couldn't send that to the popupmenu ?
			popUpMenu FlightSimMaterialRCMenuTex
		)

		on BaseColorTexBtn MouseClick sender arg do browseTex "BaseColor"
		on OcclusionRoughnessMetallicTexBtn MouseClick sender arg do browseTex "OcclusionRoughnessMetallic"
		on NormalTexBtn MouseClick sender arg do browseTex "Normal"
		on BlendMaskTexBtn MouseClick sender arg do browseTex "BlendMask"
		on DirtTexBtn MouseClick sender arg do browseTex "Dirt"
		on WetnessAOTexBtn MouseClick sender arg do browseTex "WetnessAO"
		on OpacityTexBtn MouseClick sender arg do browseTex "Opacity"
		on EmissiveTexBtn MouseClick sender arg do browseTex "Emissive"
		on DetailColorTexBtn MouseClick sender arg do browseTex "DetailColor"
		on DetailOcclusionRoughnessMetallicTexBtn MouseClick sender arg do browseTex "DetailOcclusionRoughnessMetallic"
		on DetailNormalTexBtn MouseClick sender arg do browseTex "DetailNormal"

		local mdist = 0.0
		local oldPos = [0.0, 0.0]
		fn btnDragMove sender arg basename =
		(
			local pos = [arg.location.x, arg.location.y]
			if arg.button==arg.button.left then
			(
				mdist += distance pos oldPos
				if mdist>10.0 do
				(
					local filename = getProperty this (basename + "Tex")
					if filename != undefined and filename != "" do
						sender.DoDragDrop #("FlightSimMaterialDnD",basename,filename) (dotNetClass "System.Windows.Forms.DragDropEffects").Move
				)
			)
			else
			(
				mdist = 0.0
			)
			oldPos = pos
		)

		fn btnDragOver sender arg =
		(
			arg.Effect = arg.Effect.Move
		)

		fn btnDragDrop arg basename =
		(
			--print (arg.data.GetFormats())
			local data = arg.data.GetData "FileNameW"
			if data != undefined then
			(
				local filename = data[1]
				if filename!=undefined then
				(
					local ext = "*" + getFilenameType filename + "*"
					if matchPattern filesTypes pattern:ext ignoreCase:true and ext!="**" then
					(
						loadTex 		filename basename
						loadLinked	filename basename
					)
				)
			)
			else
			(
				data = arg.data.GetData "System.Object[]"
				if data != undefined and data[1]=="FlightSimMaterialDnD" do --swap
				(
					local localHolding = false
					if (theHold.holding() == false) do
					(
						theHold.begin()
						localHolding = true
					)

					try
					(
						local filename = getProperty this (basename + "Tex")
						local srcBasename = data[2]
						local srcFilename = data[3]

						if filename != "" then
							loadTex filename srcBasename
						else
							clearTex srcBasename

						loadTex srcFilename basename

						if (theHold.holding() == true and localHolding) do
							theHold.accept ("Mtl : Swap Textures " + "(" + srcBasename + " / " + basename + ")")
					)
					catch
					(
						if (theHold.holding() == true and localHolding) do
							theHold.Cancel()
					)
				)
			)
		)

		on BaseColorTexBtn MouseMove sender arg do btnDragMove sender arg "BaseColor"
		on OcclusionRoughnessMetallicTexBtn MouseMove sender arg do btnDragMove sender arg "OcclusionRoughnessMetallic"
		on NormalTexBtn MouseMove sender arg do btnDragMove sender arg "Normal"
		on BlendMaskTexBtn MouseMove sender arg do btnDragMove sender arg "BlendMask"
		on WetnessAOTexBtn MouseMove sender arg do btnDragMove sender arg "WetnessAO"
		on DirtTexBtn MouseMove sender arg do btnDragMove sender arg "Dirt"
		on OpacityTexBtn MouseMove sender arg do btnDragMove sender arg "Opacity"
		on EmissiveTexBtn MouseMove sender arg do btnDragMove sender arg "Emissive"
		on DetailColorTexBtn MouseMove sender arg do btnDragMove sender arg "DetailColor"
		on DetailOcclusionRoughnessMetallicTexBtn MouseMove sender arg do btnDragMove sender arg "DetailOcclusionRoughnessMetallic"
		on DetailNormalTexBtn MouseMove sender arg do btnDragMove sender arg "DetailNormal"

		on BaseColorTexBtn DragOver sender arg do btnDragOver sender arg
		on OcclusionRoughnessMetallicTexBtn DragOver sender arg do btnDragOver sender arg
		on NormalTexBtn DragOver sender arg do btnDragOver sender arg
		on BlendMaskTexBtn DragOver sender arg do btnDragOver sender arg
		on DirtTexBtn sender arg do btnDragOver sender arg
		on WetnessAOTexBtn DragOver sender arg do btnDragOver sender arg
		on OpacityTexBtn DragOver sender arg do btnDragOver sender arg
		on EmissiveTexBtn DragOver sender arg do btnDragOver sender arg
		on DetailColorTexBtn DragOver sender arg do btnDragOver sender arg
		on DetailOcclusionRoughnessMetallicTexBtn DragOver sender arg do btnDragOver sender arg
		on DetailNormalTexBtn DragOver sender arg do btnDragOver sender arg

		on BaseColorTexBtn DragDrop sender arg do btnDragDrop arg "BaseColor"
		on OcclusionRoughnessMetallicTexBtn DragDrop sender arg do btnDragDrop arg "OcclusionRoughnessMetallic"
		on NormalTexBtn DragDrop sender arg do btnDragDrop arg "Normal"
		on BlendMaskTexBtn DragDrop sender arg do btnDragDrop arg "BlendMask"
		on DirtTexBtn DragDrop sender arg do btnDragDrop arg "Dirt"
		on WetnessAOTexBtn DragDrop sender arg do btnDragDrop arg "WetnessAO"
		on OpacityTexBtn DragDrop sender arg do btnDragDrop arg "Opacity"
		on EmissiveTexBtn DragDrop sender arg do btnDragDrop arg "Emissive"
		on DetailColorTexBtn DragDrop sender arg do btnDragDrop arg "DetailColor"
		on DetailOcclusionRoughnessMetallicTexBtn DragDrop sender arg do btnDragDrop arg "DetailOcclusionRoughnessMetallic"
		on DetailNormalTexBtn DragDrop sender arg do btnDragDrop arg "DetailNormal"

		on BaseColorTexBtn mouseUp sender arg do if arg.button==arg.button.right do rightclickMenu("BaseColor")
		on OcclusionRoughnessMetallicTexBtn mouseUp sender arg do if arg.button==arg.button.right do rightclickMenu ("OcclusionRoughnessMetallic")
		on NormalTexBtn mouseUp sender arg do if arg.button==arg.button.right do rightclickMenu ("Normal")
		on BlendMaskTexBtn mouseUp sender arg do if arg.button==arg.button.right do rightclickMenu ("BlendMask")
		on DirtTexBtn mouseUp sender arg do if arg.button==arg.button.right do rightclickMenu ("Dirt")
		on WetnessAOTexBtn mouseUp sender arg do if arg.button==arg.button.right do rightclickMenu ("WetnessAO")
		on OpacityTexBtn mouseUp sender arg do if arg.button==arg.button.right do rightclickMenu ("Opacity")
		on EmissiveTexBtn mouseUp sender arg do if arg.button==arg.button.right do rightclickMenu ("Emissive")
		on DetailColorTexBtn mouseUp sender arg do if arg.button==arg.button.right do rightclickMenu ("DetailColor")
		on DetailOcclusionRoughnessMetallicTexBtn mouseUp sender arg do if arg.button==arg.button.right do rightclickMenu ("DetailOcclusionRoughnessMetallic")
		on DetailNormalTexBtn mouseUp sender arg do if arg.button==arg.button.right do rightclickMenu ("DetailNormal")
	)
	
	on create do
	(
		loadShader()
		delegate.renderMaterial = undefined
	)

	on postCreate do
	(

	)

	on clone original do
	(
	)

	on load do	(
		loadShader()
	)

	on postLoad do(
	)

	on update do
	(
		MatEditor.close()
	)
)



--callbacks.removeScripts id:#FlightSimMaterialAdded
callbacks.removeScripts id:#FlightSimMaterialCallback

callbacks.addScript #sceneUndo \
"local undoStr = callbacks.notificationParam()
if MatEditor.isOpen() then
(
	local mat = medit.GetCurMtl()
	if classof mat == FlightSimMaterial then
		mat.updateGlobalUI()
)
" id:#FlightSimMaterialCallback

callbacks.addScript #sceneRedo \
"local undoStr = callbacks.notificationParam()
if MatEditor.isOpen() then
(
	local mat = medit.GetCurMtl()
	if classof mat == FlightSimMaterial then
		mat.updateGlobalUI()
)
" id:#FlightSimMaterialCallback

--callbacks.addScript #mtlRefAdded "local mat = callbacks.notificationParam() mat.paramsUI.initGUID()" id:#FlightSimMaterialAdded