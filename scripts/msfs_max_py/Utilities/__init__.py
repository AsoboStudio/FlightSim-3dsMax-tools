import os

from maxsdk.globals import *
from maxsdk.menu import * 
from pymxs import runtime as rt

import Utilities.updateContainerID as updateContainerID
import Utilities.countMaterial as countMaterial
import Utilities.autoAddLODNodesToAnimGroup as autoAddLODNodesToAnimGroup 
import Utilities.splitScene as splitScene

CATEGORY_MACRO = "FlightSim"
SUB_MENU_NAME = "Utilities"



def installMenu():
    createMacroScript(_func=updateContainerID.run, category="FlightSim", name="UpdateContainerID", button_text= "Update Container ID")
    createMacroScript(_func=countMaterial.run, category="FlightSim", name="CountMaterialOnSelection", button_text="Count Materials")
    createMacroScript(_func=autoAddLODNodesToAnimGroup.run, category="FlightSim", name="AutoAddLODNodesToAnimGroup", button_text="Auto Add LOD Nodes To AnimGroup")
    createMacroScript(_func=splitScene.splitLayersToFiles, category="FlightSim", name="SplitLayersToFiles", button_text="Split Layers To Files")

    actionItem0 = rt.menuMan.createActionItem("UpdateContainerID", "FlightSim")
    actionItem1 = rt.menuMan.createActionItem("CountMaterialOnSelection", "FlightSim")
    actionItem2 = rt.menuMan.createActionItem("AutoAddLODNodesToAnimGroup", "FlightSim")
    actionItem3 = rt.menuMan.createActionItem("SplitLayersToFiles", "FlightSim")

    FlightSimMenu = rt.menuMan.findMenu(CATEGORY_MACRO)
    if not FlightSimMenu:
        FlightSimMenu = rt.menuMan.createMenu(CATEGORY_MACRO)

    AsoboUtilitiesMenu = rt.menuMan.findMenu(SUB_MENU_NAME)
    if not AsoboUtilitiesMenu:
        AsoboUtilitiesMenu = rt.menuMan.createMenu(SUB_MENU_NAME)

    AsoboUtilitiesItem = rt.menuMan.createSubMenuItem(SUB_MENU_NAME, AsoboUtilitiesMenu)

    safeAddItem(AsoboUtilitiesMenu, actionItem0)
    safeAddItem(AsoboUtilitiesMenu, actionItem1)
    safeAddItem(AsoboUtilitiesMenu, actionItem2)
    safeAddItem(AsoboUtilitiesMenu, actionItem3)
    safeAddItem(FlightSimMenu, AsoboUtilitiesItem)

    rt.menuMan.updateMenuBar()


try:
    installMenu()
except Exception as error: 
    print("utilitiesMenu failed to install because {}".format(error))