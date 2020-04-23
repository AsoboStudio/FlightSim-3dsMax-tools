global AsoboGraphicChartPos
if AsoboGraphicChart != undefined then destroydialog AsoboGraphicChart

rollout AsoboGraphicChart "Graphic Chart" width:180
(
	group "Diffuse"
	(
		label diff_lab "Valid range: 50-240"
		
		colorpicker Charcoal_diff "Charcoal" 			color:[50,50,50] alpha:false align:#right fieldWidth:80 height:15 modal:false title:"Charcoal"
		colorpicker Blackpaint_diff "Black paint"		color:[56,56,56] alpha:false align:#right fieldWidth:80 height:15 modal:false title:"Black Paint" offset:[0,-5]
		colorpicker Drydarkearth_diff "Dry dark earth"	color:[85,61,49] alpha:false align:#right fieldWidth:80 height:15 modal:false title:"Dry dark earth" offset:[0,-5]
		colorpicker Wornasphal_diff "Worn asphalt"		color:[91,91,91] alpha:false align:#right fieldWidth:80 height:15 modal:false title:"Worn asphalt" offset:[0,-5]
		colorpicker Africanskin_diff "African skin"		color:[116,94,81] alpha:false align:#right fieldWidth:80 height:15 modal:false title:"African skin" offset:[0,-5]
		colorpicker Dryclaysoil_diff "Dry clay soil"	color:[137,120,102] alpha:false align:#right fieldWidth:80 height:15 modal:false title:"Dry clay soil" offset:[0,-5]
		colorpicker Greengrass_diff "Green grass"		color:[123,130,78] alpha:false align:#right fieldWidth:80 height:15 modal:false title:"Green grass" offset:[0,-5]
		colorpicker Oldconcrete_diff "Old concrete"		color:[135,136,131] alpha:false align:#right fieldWidth:80 height:15 modal:false title:"Old concrete" offset:[0,-5]
		colorpicker Redclaytile_diff "Red clay tile"	color:[197,125,100] alpha:false align:#right fieldWidth:80 height:15 modal:false title:"Red clay tile" offset:[0,-5]
		colorpicker Drysand_diff "Dry sand"				color:[177,167,132] alpha:false align:#right fieldWidth:80 height:15 modal:false title:"Dry sand" offset:[0,-5]
		colorpicker Newconcrete_diff "New concrete"		color:[185,182,173] alpha:false align:#right fieldWidth:80 height:15 modal:false title:"New concrete" offset:[0,-5]
		colorpicker Cleancement_diff "Clean cement"		color:[192,191,187] alpha:false align:#right fieldWidth:80 height:15 modal:false title:"Clean cement" offset:[0,-5]
		colorpicker Whitecement_diff "White cement"		color:[219,218,216] alpha:false align:#right fieldWidth:80 height:15 modal:false title:"White cement" offset:[0,-5]
		colorpicker Whitepaint_diff "White paint"		color:[227,227,227] alpha:false align:#right fieldWidth:80 height:15 modal:false title:"White paint" offset:[0,-5]
		colorpicker Freshsnow_diff "Fresh snow"			color:[243,243,243] alpha:false align:#right fieldWidth:80 height:15 modal:false title:"Fresh snow" offset:[0,-5]
		
		colorpicker Metal_diff "Metal"			color:[0,0,0] alpha:false align:#right fieldWidth:80 height:15 modal:false title:"Metal" offset:[0,5]
		
		on Charcoal_diff changed c do Charcoal_diff.color = [50,50,50]
		on Blackpaint_diff changed c do Blackpaint_diff.color = [56,56,56]
		on Drydarkearth_diff changed c do Drydarkearth_diff.color = [85,61,49]
		on Wornasphal_diff changed c do Wornasphal_diff.color = [91,91,91]
		on Africanskin_diff changed c do Africanskin_diff.color = [116,94,81]
		on Dryclaysoil_diff changed c do Dryclaysoil_diff.color = [137,120,102]
		on Greengrass_diff changed c do Greengrass_diff.color = [123,130,78]
		on Oldconcrete_diff changed c do Oldconcrete_diff.color = [135,136,131]
		on Redclaytile_diff changed c do Redclaytile_diff.color = [197,125,100]
		on Drysand_diff changed c do Drysand_diff.color = [177,167,132]
		on Newconcrete_diff changed c do Newconcrete_diff.color = [185,182,173]
		on Cleancement_diff changed c do Cleancement_diff.color = [192,191,187]
		on Whitecement_diff changed c do Whitecement_diff.color = [219,218,216]
		on Whitepaint_diff changed c do Whitepaint_diff.color = [227,227,227]
		on Freshsnow_diff changed c do Freshsnow_diff.color = [243,243,243]
			
		on Metallic_diff changed c do Metallic_diff.color = [0,0,0]
	)
	
	group "Reflectance"
	(
		label ref_lab "Common range: 40-65"
		
		label dielectric_lab "Dielectric:" offset:[20,0]
		colorpicker Ice_ref "Ice"		color:[41,41,41] alpha:false align:#right fieldWidth:80 height:15 modal:false title:"Ice" offset:[0,-5]
		colorpicker Water_ref "Water"		color:[43,43,43] alpha:false align:#right fieldWidth:80 height:15 modal:false title:"Water" offset:[0,-5]
		colorpicker Skin_ref "Skin"			color:[50,50,50] alpha:false align:#right fieldWidth:80 height:15 modal:false title:"Skin" offset:[0,-5]
		colorpicker Plastic_ref "Plastic"	color:[59,59,59] alpha:false align:#right fieldWidth:80 height:15 modal:false title:"Plastic" offset:[0,-5]
		colorpicker Glass_ref "Glass"		color:[59,59,59] alpha:false align:#right fieldWidth:80 height:15 modal:false title:"Glass" offset:[0,-5]
		colorpicker Crystal_ref "Crystal"	color:[94,94,94] alpha:false align:#right fieldWidth:80 height:15 modal:false title:"Crystal" offset:[0,-5]
		colorpicker Diamond_ref "Diamond"	color:[115,115,115] alpha:false align:#right fieldWidth:80 height:15 modal:false title:"Diamond" offset:[0,-5]
		
		label metallic_lab "Metallic:" offset:[16,0]
		colorpicker Chromium_ref "Chromium" 	color:[194,195,195] alpha:false align:#right fieldWidth:80 height:15 modal:false title:"Chromium" offset:[0,-5]
		colorpicker Platinum_ref "Platinum" 	color:[213,208,200] alpha:false align:#right fieldWidth:80 height:15 modal:false title:"Platinum" offset:[0,-5]
		colorpicker Aluminium_ref "Aluminium"	color:[245,246,246] alpha:false align:#right fieldWidth:80 height:15 modal:false title:"Aluminium" offset:[0,-5]
		colorpicker Copper_ref "Copper" 		color:[250,208,192] alpha:false align:#right fieldWidth:80 height:15 modal:false title:"Copper" offset:[0,-5]
		colorpicker Silver_ref "Silver" 		color:[252,250,245] alpha:false align:#right fieldWidth:80 height:15 modal:false title:"Silver" offset:[0,-5]
		colorpicker Gold_ref "Gold" 			color:[255,226,155] alpha:false align:#right fieldWidth:80 height:15 modal:false title:"Gold" offset:[0,-5]
		
		label ior_lab "IOR and Reflectance:"
		spinner ior "ior:" range:[0.0,3.40E38,1.33] width:70 type:#float scale:0.01 across:2
		colorpicker ior_ref "" color:[0,0,0] alpha:false align:#right fieldWidth:50 height:16 modal:false title:"ior"
		
		on ior changed n do
		(
			local r = pow (n-1.0) 2.0 / pow (n+1.0) 2.0
			r = 255.0 * pow r (1.0/2.2)
			ior_ref.color = color r r r
		)
		
		on ior_ref changed c do
		(
			local r = (c.r+c.g+c.b)/3.0
			local n = pow (r/255.0) 2.2
			if n==1.0 then
				n = 3.40E38
			else
				n = -(n+1.0)/(n-1.0) - (2.0*sqrt(n))/((sqrt(n)-1.0)*(sqrt(n)+1.0))
			ior.value = n
		)
		
		on Ice_ref changed c do Ice_ref.color = [41,41,41]
		on Water_ref changed c do Water_ref.color = [43,43,43]
		on Skin_ref changed c do Skin_ref.color = [50,50,50]
		on Plastic_ref changed c do Plastic_ref.color = [59,59,59]
		on Glass_ref changed c do Glass_ref.color = [59,59,59]
		on Crystal_ref changed c do Crystal_ref.color = [94,94,94]
		on Diamond_ref changed c do Diamond_ref.color = [115,115,115]
			
		on Chromium_ref changed c do Chromium_ref.color = [194,195,195]
		on Platinum_ref changed c do Platinum_ref.color = [213,208,200]
		on Aluminium_ref changed c do Aluminium_ref.color = [245,246,246]
		on Copper_ref changed c do Copper_ref.color = [250,208,192]
		on Silver_ref changed c do Silver_ref.color = [252,250,245]
		on Gold_ref changed c do Gold_ref.color = [255,226,155]
	)
	
	on AsoboGraphicChart open do
	(
		ior.changed 1.33
	)
	
	on AsoboGraphicChart close do
	(
		deleteAllChangeHandlers id:#FurModeler
		AsoboGraphicChartPos = GetDialogPos AsoboGraphicChart
	)
)

if AsoboGraphicChartPos != undefined then
	createDialog AsoboGraphicChart pos:AsoboGraphicChartPos
else
	createDialog AsoboGraphicChart