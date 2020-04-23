

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


(
	local FlightSimMenu = menuMan.createMenu "FlightSim"

	local babylonUtilitiesSubMenu = menuMan.createMenu "Babylon Utilities"

	FlightSimMenu.addItem (menuMan.createActionItem "FlightSimMaterialsTools" "FlightSim") -1
	FlightSimMenu.addItem (menuMan.createActionItem "FlightSimObjectRenamer" "FlightSim") -1

	babylonUtilitiesSubMenu.addItem (menuMan.createActionItem "CreateAnimationGroupFromSelection" "FlightSim") -1


	FlightSimMenu.addItem (menuMan.createSubMenuItem "FlightSim" babylonUtilitiesSubMenu) -1

	
	local mainMenu = menuMan.getMainMenuBar()
	for i = mainMenu.numItems() to 1 by -1 do
		if (mainMenu.getItem i).getTitle() == "FlightSim" then
			mainMenu.removeItem (mainMenu.getItem i)
	mainMenu.addItem (menuMan.createSubMenuItem "FlightSim" FlightSimMenu) -1
	menuMan.updateMenuBar()
)