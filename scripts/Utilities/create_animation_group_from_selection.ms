Assembly = dotNetClass "System.Reflection.Assembly"
dllPath = pathConfig.appendPath (symbolicPaths.getPathValue(1)) "bin\\assemblies\\Max2Babylon.dll"
Assembly.loadfrom dllPath
maxScriptManager = dotNetObject "Max2Babylon.MaxScriptManager"



fn getAnimGroupName mNode =
(
	animGroupName = trimLeft mNode.name ":"
	pattern =@"(?i)x[0-9]_"
	rgx = dotnetObject "System.Text.RegularExpressions.Regex" pattern
	result = rgx.Replace animGroupName ""
	return result
)

fn getLodOfName mName = 
(
    result = #()
    for obj in rootScene.world.children do (
        pattern =@"(?i)x[0-9]_"+ mName
        rgx = dotnetObject "System.Text.RegularExpressions.Regex" pattern
        match = rgx.Match obj.name pattern

        if match.Success then
        (
            append result obj
        )
    )
	return result
)

fn getNodeFromOtherLod mNode =
(
	patternLod =@"(?i)x[0-9]_"
	rgx = dotnetObject "System.Text.RegularExpressions.Regex" patternLod
	match = rgx.Match mNode.Name patternLod
	if not match.Success then
	(
		print("no lod found this node")
		return undefined
	)
	else
	(		
		nodeList = #()
		simpleName = trimLeft mNode.name ":"
		if simpleName != mNode.Name then
		(
			nameSpaceLen = simpleName.count
			for i=0 to 6 do
			(
				newName = mNode.Name
				newName[nameSpaceLen + 2] = i
				lodNode= getnodebyname newname
				append nodelist lodNode
			)
		)
		else
		(
			for i=0 to 7 do
			(
				newName = mNode.Name
				newName[2] = i as string
				lodNode= getnodebyname newname
				if lodNode == undefined then 
					continue
				append nodelist lodNode
			)
		)
	)

	return nodeList
)

fn ReplaceWords mStream mFromStr mToStr mIgnoreCase:false =
(
	regex = dotnetclass "system.text.regularexpressions.regex"
	pattern = mFromStr + "\b"	
	result = regex.replace mStream pattern mToStr
	return result 
)

fn hasAnimation mNode =
(
    return mNode.position.isAnimated or mNode.rotation.isAnimated or mNode.scale.isAnimated
)

if $ != undefined then
(
	for n in (selection as array) do
	(
		if hasAnimation n then
		(
			animGroup = maxScriptManager.CreateAnimationGroup()
            nodeList = #()
			cl = superclassof n
			if cl == Helper then
			(
				noLodNoHelper = ReplaceWords n.Name "_helper" "" mIgnoreCase:true
				nodeList = getLodOfName noLodNoHelper
				if nodeList !=undefined then
				(
					for lodNode in nodeList do
					(
						maxScriptManager.AddNodeInAnimationGroup animGroup lodNode.handle
					)
					maxScriptManager.AddNodeInAnimationGroup animGroup n.handle
					endFrame = maxScriptManager.GetTimeRange animGroup
					maxScriptManager.SetAnimationGroupTimeRange animGroup 0 endframe
					maxScriptManager.RenameAnimationGroup animGroup noLodNoHelper
				)
				else
				(
					print("added without lod pattern: " + n.name)
					maxScriptManager.AddNodeInAnimationGroup animGroup n.handle
					endFrame = maxScriptManager.GetTimeRange animGroup
					maxScriptManager.SetAnimationGroupTimeRange animGroup 0 endframe
					animGroupName = getAnimGroupName n
					maxScriptManager.RenameAnimationGroup animGroup animGroupName
				)
				
			)				
			if cl==GeometryClass then
			(
				nodeList = getNodeFromOtherLod n
				
				if nodeList !=undefined then
				(
					for lodNode in nodeList do
					(
						maxScriptManager.AddNodeInAnimationGroup animGroup lodNode.handle
					)
					endFrame = maxScriptManager.GetTimeRange animGroup
					maxScriptManager.SetAnimationGroupTimeRange animGroup 0 endframe
					animGroupName = getAnimGroupName n
					maxScriptManager.RenameAnimationGroup animGroup animGroupName
				)
				else
				(
					print("added without lod pattern: " + n.name)
					maxScriptManager.AddNodeInAnimationGroup animGroup n.handle
					endFrame = maxScriptManager.GetTimeRange animGroup
					maxScriptManager.SetAnimationGroupTimeRange animGroup 0 endframe
					animGroupName = getAnimGroupName n
					maxScriptManager.RenameAnimationGroup animGroup animGroupName
				)
			)		
			
		)	
	)
)
else
(
	messagebox "Nothing selected"
)
