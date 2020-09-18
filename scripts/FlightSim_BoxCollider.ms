plugin Helper AsoboBoxGizmo
name:"Box Gizmo"
classID:#(0x231f3b1a, 0x5a974704)
extends:BoxGizmo
category:"ASOBO"
replaceUI:false
autoPromoteDelegateProps:false
(
	parameters main rollout:params
	(
	    IsCollider type:#boolean animatable:false default:true ui:IsCollider_UI
		IsRoad type:#boolean animatable:false default:false ui:IsRoad_UI
	)
	
	rollout params "Box Collider Parameters"
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