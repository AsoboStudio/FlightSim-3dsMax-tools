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
		Kelvin type:#float default:3600.0 ui:Kelvin_UI

		on Kelvin set val do(
			delegate.usekelvin = true
			delegate.kelvin = val
			this.Color = delegate.color
			this.Color.r = clamp 0.0 255.0 this.Color.r
			this.Color.g = clamp 0.0 255.0 this.Color.g
			this.Color.b = clamp 0.0 255.0 this.Color.b
		)
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
        colorpicker Color_UI "Light Color:" modal:false align:#right
	    spinner Intensity_UI "Intensity" range:[0.0, 10000000.0, 1.0] type:#Float align:#right

		spinner ConeAngle_UI "Cone Angle" range:[0.0, 360, 90.0] type:#Float align:#right
		checkbox HasSimmetry_UI "Has Simmetry" type:#boolean
		spinner FlashFrequency_UI "Flash Frequency" range:[0.0, 1000.0, 1.0] align:#right type:#Float

	)




)