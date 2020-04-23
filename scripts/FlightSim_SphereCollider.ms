plugin Helper AsoboSphereGizmo
name:"Sphere Gizmo"
classID:#(0x736e21e7, 0x45da3199)
extends:SphereGizmo
category:"ASOBO"
replaceUI:false
autoPromoteDelegateProps:false
(	
	parameters main rollout:params
	(
		IsCollider type:#boolean animatable:false default:true ui:IsCollider_UI
		IsRoad type:#boolean animatable:false default:false ui:IsRoad_UI
	)
	
	rollout params "Sphere Collider Parameters"
	(
		 checkbox IsCollider_UI "Is Collider" type:#boolean
		 checkbox IsRoad_UI "Is Road" type:#boolean
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