plugin Light MacroLightSpot
name:"MacroLight"
classID:#(0x451a77a6, 0x232b0194)
extends:Freespot
category:"ASOBO"
replaceUI:true
autoPromoteDelegateProps:false
(

    parameters main rollout:params
	(
	    Color type:#point4 default:white ui:Color_UI animatable:false
	    Intensity type:#float animatable:false default:1.0 ui:Intensity_UI
	    ConeAngle type:#float animatable:false default:90.0 ui:ConeAngle_UI
		HasSimmetry type:#boolean animatable:false default:false ui:HasSimmetry_UI
		IsBeacon type:#boolean animatable:false default:false ui:IsBeacon_UI

        on ConeAngle set val do
        (
            if val != undefined then
            (
                this.Freespot.falloff=val
                this.Freespot.hotspot=val
            )
        )
	)

	rollout params "Parameers"
	(
        colorpicker Color_UI "Light Color:" modal:false align:#right
	    spinner Intensity_UI "Light Intensity" range:[0.0, 100, 1.0] type:#Float align:#right
	    spinner ConeAngle_UI "Cone Angle" range:[0.0, 180, 90.0] type:#Float align:#right
		checkbox HasSimmetry_UI "Has Simmetry" type:#boolean
		checkbox IsBeacon_UI "Is Beacon" type:#boolean
	)

)