plugin Helper SphereFade
name:"Sphere Fade"
classID:#(0x794b56ca, 0x172623ba)
extends:SphereGizmo
category:"ASOBO"
replaceUI:false
autoPromoteDelegateProps:false
(	
	parameters main rollout:params
	(
		
	)
	
	rollout params "Sphere Fade Parameters"
	(
		
	)

	fn setAsDoNotExport nodeVar =
	(
		setUserProp nodeVar "babylonjs_noexport" True
	)

	on attachedToNode n do
	(
		setAsDoNotExport(n)
	)
)