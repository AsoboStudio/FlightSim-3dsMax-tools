

macroScript FlightSimMaterialsTools category:"FlightSim" buttontext:"Materials Tools" tooltip:"Materials Tools" Icon:#("Material_Modifiers",2)
(
	filein (pathConfig.appendPath FlightSimPluginPath @"FlightSim_MaterialsTools.ms")
)

macroScript FlightSimObjectRenamer category:"FlightSim" buttontext:"Objects Renamer" tooltip:"Objects Renamer"
(
	filein	(pathConfig.appendPath FlightSimPluginPath @"FlightSim_ObjectRenamer.ms")
)

macroScript CreateAnimationGroupFromSelection category:"FlightSim" buttontext:"Create AnimationGroup From Selection" tooltip:"Create AnimationGroup From Selection"
(
    filein	(pathConfig.appendPath FlightSimPluginPath @"Utilities\\create_animation_group_from_selection.ms")
)

macroScript FlightSimEnvironmentLODsTools category:"FlightSim" buttontext:"Environment LODs Tools" tooltip:"Generic utilities to generate LODs"
(
    filein	(pathConfig.appendPath FlightSimPluginPath @"FlightSim_EnvironmentLODsTools.ms")
)

macroScript FlightSim_DisplayUvShellBorder category:"FlightSim" buttontext:"Display Uv Shell Border" tooltip:"Display Uv Shell Border"
(
    filein	(pathConfig.appendPath FlightSimPluginPath @"FlightSim_DisplayUvShellBorder.ms")
)


(
	local FlightSimMenu = menuMan.findMenu "FlightSim"
	while True do (
		local FlightSimMenu = menuMan.findMenu "FlightSim"

		if FlightSimMenu != undefined then
		(		
			menuMan.unRegisterMenu(FlightSimMenu)
		)
		else
		(
			exit
		)
	)
	FlightSimMenu = menuMan.createMenu "FlightSim"

	local babylonUtilitiesSubMenu = menuMan.createMenu "Babylon Utilities"

	FlightSimMenu.addItem (menuMan.createActionItem "FlightSimEnvironmentLODsTools" "FlightSim") -1
	FlightSimMenu.addItem (menuMan.createActionItem "FlightSimMaterialsTools" "FlightSim") -1
	FlightSimMenu.addItem (menuMan.createActionItem "FlightSimObjectRenamer" "FlightSim") -1
	FlightSimMenu.addItem (menuMan.createActionItem "FlightSim_DisplayUvShellBorder" "FlightSim") -1

	babylonUtilitiesSubMenu.addItem (menuMan.createActionItem "CreateAnimationGroupFromSelection" "FlightSim") -1


	FlightSimMenu.addItem (menuMan.createSubMenuItem "FlightSim" babylonUtilitiesSubMenu) -1

	local mainMenu = menuMan.getMainMenuBar()

	mainMenu.addItem (menuMan.createSubMenuItem "FlightSim" FlightSimMenu) -1
	menuMan.updateMenuBar()
)
