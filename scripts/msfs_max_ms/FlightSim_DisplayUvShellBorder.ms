(
 
	unRegisterRedrawViewsCallback cbDrawOpenEdges
 
	global RO_DISPLAY_UV_OE
	global cbDrawOpenEdges
	global cbSelectionChanged
 
	local vertexPos   = #()
	local uvChannel   = 1
	local edgesColor  = [0,255,0]
	local edgeOffset  = 0.03
	local forceRedraw = false
 
	fn cbDrawOpenEdges = (
		gw.setTransform (Matrix3 1)
		gw.setColor #line edgesColor
		for j in vertexPos do gw.polyLine j true
 
		-- Needed in some Max versions or used dirvers
		if forceRedraw do (
			gw.enlargeUpdateRect #whole
			gw.updateScreen()
		)
	)
 
	fn cbSelectionChanged mForce:false = (
 
		unRegisterRedrawViewsCallback cbDrawOpenEdges
 
		if ($ != undefined) do (
 
			setwaitcursor()
 
			st = timeStamp()
 
			obj = snapshotasmesh selection[1]
 
			allChannels = for j = 1 to meshop.getNumMaps obj where (meshop.getMapSupport obj j) collect j
 
			RO_DISPLAY_UV_OE.ddl_channel.items = for j in allChannels collect j as string
 
			if (mForce == false) do (
				uvChannel = allChannels[1]
				RO_DISPLAY_UV_OE.ddl_channel.selection = 1
			)
 
			numTFaces = meshop.getNumMapFaces obj uvChannel
			numTVerts = meshop.getNumMapVerts obj uvChannel
 
			facesTVertsIdx = for j = 1 to numTFaces collect (meshop.getMapFace obj uvChannel j)
 
			emesh = trimesh()
			setMesh emesh numverts:numTVerts numfaces:numTFaces
			setMesh emesh faces:facesTVertsIdx
 
			objOpenEdges = meshop.getOpenEdges obj
			meshOpenEdges = (meshop.getOpenEdges emesh) - objOpenEdges
 
			vertexPos = #()
 
			sharedFaces = meshop.getFacesUsingEdge emesh meshOpenEdges
			foundEdges = #()
 
			for j in sharedFaces do (
 
				objFaceVerts = getFace obj j
 
				edge1 = j*3 - 2
				edge2 = j*3 - 1
				edge3 = j*3
 
				n1 = (getFaceNormal obj j) * edgeOffset
 
				if (finditem meshOpenEdges edge1) > 0 do (
					v1Idx = objFaceVerts.x
					v2Idx = objFaceVerts.y
					if (findItem foundEdges [v1Idx, v2Idx] == 0) do (
						v1 = getVert obj v1Idx
						v2 = getVert obj v2Idx
						n3 = (normalize (cross n1 (v1-v2))) * edgeOffset
						append vertexPos #(v1+n1+n3, v2+n1+n3, v1-n1-n3, v2-n1-n3, v1-n1+n3, v2-n1+n3, v1+n1-n3, v2+n1-n3)
						append foundEdges [v2Idx, v1Idx]
					)
				)
				if (finditem meshOpenEdges edge2) > 0 do (
					v1Idx = objFaceVerts.y
					v2Idx = objFaceVerts.z
					if (findItem foundEdges [v1Idx, v2Idx] == 0) do (
						v1 = getVert obj v1Idx
						v2 = getVert obj v2Idx
						n3 = (normalize (cross n1 (v1-v2))) * edgeOffset
						append vertexPos #(v1+n1+n3, v2+n1+n3, v1-n1-n3, v2-n1-n3, v1-n1+n3, v2-n1+n3, v1+n1-n3, v2+n1-n3)
						append foundEdges [v2Idx, v1Idx]
					)
				)
				if (finditem meshOpenEdges edge3) > 0 do (
					v1Idx = objFaceVerts.z
					v2Idx = objFaceVerts.x
					if (findItem foundEdges [v1Idx, v2Idx] == 0) do (
						v1 = getVert obj v1Idx
						v2 = getVert obj v2Idx
						n3 = (normalize (cross n1 (v1-v2))) * edgeOffset
						append vertexPos #(v1+n1+n3, v2+n1+n3, v1-n1-n3, v2-n1-n3, v1-n1+n3, v2-n1+n3, v1+n1-n3, v2+n1-n3)
						append foundEdges [v2Idx, v1Idx]
					)
				)
 
			)
 
			sharedFaces = meshop.getFacesUsingEdge obj objOpenEdges
 
			for j in sharedFaces do (
 
				objFaceVerts = getFace obj j
 
				edge1 = j*3 - 2
				edge2 = j*3 - 1
				edge3 = j*3
 
				n1 = (getFaceNormal obj j) * edgeOffset
 
				if (finditem objOpenEdges edge1) > 0 do (
					v1Idx = objFaceVerts.x
					v2Idx = objFaceVerts.y
					v1 = getVert obj v1Idx
					v2 = getVert obj v2Idx
					n3 = (normalize (cross n1 (v1-v2))) * edgeOffset
					append vertexPos #(v1+n1+n3, v2+n1+n3, v1-n1-n3, v2-n1-n3, v1-n1+n3, v2-n1+n3, v1+n1-n3, v2+n1-n3)
				)
				if (finditem objOpenEdges edge2) > 0 do (
					v1Idx = objFaceVerts.y
					v2Idx = objFaceVerts.z
					v1 = getVert obj v1Idx
					v2 = getVert obj v2Idx
					n3 = (normalize (cross n1 (v1-v2))) * edgeOffset
					append vertexPos #(v1+n1+n3, v2+n1+n3, v1-n1-n3, v2-n1-n3, v1-n1+n3, v2-n1+n3, v1+n1-n3, v2+n1-n3)
				)
				if (finditem objOpenEdges edge3) > 0 do (
					v1Idx = objFaceVerts.z
					v2Idx = objFaceVerts.x
					v1 = getVert obj v1Idx
					v2 = getVert obj v2Idx
					n3 = (normalize (cross n1 (v1-v2))) * edgeOffset
					append vertexPos #(v1+n1+n3, v2+n1+n3, v1-n1-n3, v2-n1-n3, v1-n1+n3, v2-n1+n3, v1+n1-n3, v2+n1-n3)
				)
 
			)
 
			format "Found %\tUV Open Edges in %s\n" vertexPos.count ((timeStamp() - st) / 1000.0)
 
			registerRedrawViewsCallback cbDrawOpenEdges
 
			delete obj
			delete emesh
 
			gc light:true
 
			setArrowCursor()
 
		)
 
		forceCompleteRedraw()
 
	)
 
 
	try(destroyDialog RO_DISPLAY_UV_OE) catch()
	rollout RO_DISPLAY_UV_OE "UV Open Edges" width:160 height:198
	(
		checkbutton bt_enable "Display UV Open Edges" pos:[8,8] width:144 height:32
		dropdownList ddl_channel "UV Channel:" pos:[8,72] width:120 height:40 enabled:false
		colorPicker cp1 "" pos:[131,90] width:21 height:21 enabled:true color:edgesColor modal:false
		checkbox chk_redraw "Force Redraw" pos:[8,46] width:100 height:16 enabled:false
		spinner spn_width "Edge Width:" pos:[8,120] width:120 height:16 range:[1,100,4] type:#integer fieldwidth:50
		button bt_update "Update" pos:[8,160] width:144 height:28 enabled:false
 
		fn destroy = (
			callbacks.removeScripts #selectionSetChanged
			unRegisterRedrawViewsCallback cbDrawOpenEdges
			forceCompleteRedraw()
		)
 
		on RO_DISPLAY_UV_OE close do destroy()
 
		on bt_enable changed arg do
		(
			bt_update.enabled = arg
			ddl_channel.enabled = arg
			chk_redraw.enabled = arg
			destroy()
 
			if (arg == true) do (
				callbacks.addscript #selectionSetChanged "cbSelectionChanged()"
				cbSelectionChanged()
			)
		)
 
		on bt_update pressed do cbSelectionChanged()
 
		on ddl_channel selected arg do (
			uvChannel = (ddl_channel.selected as integer)
			cbSelectionChanged mForce:true
		)
 
		on cp1 changed arg do edgesColor = arg
 
		on spn_width changed arg do edgeOffset = (arg-1)/100.0
 
		on chk_redraw changed arg do forceRedraw = arg
 
	)
 
	createDialog RO_DISPLAY_UV_OE
 
)