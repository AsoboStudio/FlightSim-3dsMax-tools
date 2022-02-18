plugin Light FlightSimLight
name:"FlightSimLight"
classID:#(0x18a3b84e, 0x63ec33ad)
extends:Free_Light
category:"ASOBO"
replaceUI:true
autoPromoteDelegateProps:false
(
	fn clamp minVal maxVal val =
	(
		if val < minVal then val = minVal
		else if val > maxVal then val = maxVal
		return val
	)
    parameters main rollout:params
	(
	    Color type:#color default:white ui:Color_UI animatable:false
		Intensity type:#float animatable:false default:1.0 ui:Intensity_UI
	    ConeAngle type:#float animatable:false default:90.0 ui:ConeAngle_UI
		HasSimmetry type:#boolean animatable:false default:false ui:HasSimmetry_UI
		FlashFrequency type:#float default:0.0 animatable:false default:false ui:FlashFrequency_UI
		FlashDuration type:#float default:0.2 animatable:false default:false ui:FlashDuration_UI
		FlashPhase type:#float default:0.0 animatable:false default:false ui:FlashPhase_UI
		RotationSpeed type:#float default:0.0 animatable:false default:false ui:RotationSpeed_UI
		Kelvin type:#float default:3600.0 ui:Kelvin_UI
		ActivationMode type:#integer animatable:false default:1 ui:ActivationMode_UI


		on Intensity set val do(
			delegate.intensityType = 1
			delegate.intensity = val
		)
        on ConeAngle set val do
        (
			if val >= 359.99 then (
				delegate.distribution = 0
			)
			else (
				delegate.distribution = 1
			)

			if val != undefined then
			(
				delegate.falloff=val
				delegate.hotspot=val
			)
		)
	)

	rollout params "Parameters"
	(
		spinner Kelvin_UI "Kelvin" range:[1000, 20000, 3600.0] type:#Float align:#right scale:100
        colorpicker Color_UI "Color (K):" modal:false align:#right
	    spinner Intensity_UI "Intensity" range:[0.0, 10000000.0, 1.0] type:#Float align:#right\
			tooltip:"Flash per minutes"


		spinner ConeAngle_UI "Cone Angle" range:[0.0, 360, 90.0] type:#Float align:#right
		checkbox HasSimmetry_UI "Has Symmetry" type:#boolean
		group "Flash Settings" (
		spinner FlashFrequency_UI "Frequency (1/min)" range:[0.0, 1000.0, 1.0] align:#right type:#Float width:90 \
			tooltip:"Flash per minutes"
		spinner FlashDuration_UI "Duration (s)" range:[0.0, 1000.0, 0.2] align:#right type:#float width:90 \
			tooltip:"Flash duration in seconds"
		spinner FlashPhase_UI "Phase (s)" range:[0.0, 1000.0, 1.0] align:#right type:#float width:90 \
			tooltip:"Flash phase in seconds"
		spinner RotationSpeed_UI "Rotation (RPM)" range:[-1000.0, 1000.0, 0.0] align:#right type:#float width:90 \
			tooltip:"Rotation per minutes" )

		radiobuttons ActivationMode_UI "Activation Mode" columns:1 labels:#("Day/Night Cycle","Always On") 
		
		on Color_UI changed val do(
			delegate.useKelvin = false
		)
		on Kelvin_UI changed val do(
			delegate.usekelvin = true
			delegate.kelvin = val
			this.Color = delegate.color
			this.Color.r = clamp 0.0 255.0 this.Color.r
			this.Color.g = clamp 0.0 255.0 this.Color.g
			this.Color.b = clamp 0.0 255.0 this.Color.b
			delegate.usekelvin = true			
		)
		on params open do (
			if delegate.usekelvin == true then(
				Color_UI.color.r = clamp 0.0 255.0 delegate.color.r
				Color_UI.color.g = clamp 0.0 255.0 delegate.color.g
				Color_UI.color.b = clamp 0.0 255.0 delegate.color.b
				delegate.useKelvin = true
			)
		)
	)



)