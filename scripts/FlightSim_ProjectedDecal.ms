plugin Light ProjectedDecal
name:"Proj Decal"
classID:#(0x700f41e6, 0x536872c3)
extends:Directionallight
category:"ASOBO"
replaceUI:true
autoPromoteDelegateProps:false
(
	
	parameters main rollout:params
	(
		--delegate.coneShape = 2
		sizeX type:#float animatable:false default:100.0 ui:sizeX_UI
		sizeY type:#float animatable:false default:100.0 ui:sizeY_UI
		sizeZ type:#float animatable:false default:100.0 ui:sizeZ_UI
		FadeAngle type:#float animatable:false default:0.0 ui:FadeAngle_UI
		FadeDepth type:#float animatable:false default:0.0 ui:FadeDepth_UI
		
		on sizeX set val do
		(
			sizeX = val
			delegate.hotspot = sizeX * 0.5
			delegate.falloff = sizeX * 0.5
			delegate.aspect = ((Float)sizeX / (Float)sizeY)
		)
		
		on sizeY set val do
		(
			sizeY = val
			delegate.aspect = ((Float)sizeX / (Float)sizeY)
		)
		
		on sizeZ set val do
		(
			sizeZ = val
			delegate.farAttenStart = sizeZ
			delegate.farAttenEnd = sizeZ
		)
		
		on FadeAngle set val do
		(
			FadeAngle = val
		)
		
		on FadeDepth set val do
		(
			FadeDepth = val
		)
	)
	
	rollout params "Projected Decal Parameters"
	(
		spinner sizeX_UI "X size" range:[0.001, 10000000.0, 1.0] type:#worldunits
		spinner sizeY_UI "Y size" range:[0.001, 10000000.0, 1.0] type:#worldunits
		spinner sizeZ_UI "Z size" range:[0.001, 10000000.0, 1.0] type:#worldunits
		spinner FadeAngle_UI "Fade Angle" range:[0.0, 1.0, 0.0] type:#Float
		spinner FadeDepth_UI "Fade Depth" range:[0.0, 1.0, 0.0] type:#Float		
	)
	
	on useWireColor do false
	
	on attachedToNode node do
	(
		node.name = "Projected Decal"
		node.wirecolor = color 44 120 184
	)
	
	tool create
	(
		on mousePoint click do
		(
			delegate.coneShape = 2
			delegate.showCone = true
			delegate.hotspot = sizeX * 0.5
			delegate.falloff = sizeX * 0.5
			delegate.aspect = ((Float)sizeX / (Float)sizeY)
			delegate.useFarAtten = true
			delegate.farAttenStart = sizeZ
			delegate.farAttenEnd = sizeZ
			case click of
			(
				1: nodeTM.translation = gridPoint;
				2: #stop
			)
		)
		on mouseMove click do
		(
		)
	)
)