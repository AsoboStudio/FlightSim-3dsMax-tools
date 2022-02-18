import os

from maxsdk.globals import *
from maxsdk.menu import * 
from pymxs import runtime as rt

import EmptyNodeCleaner.emptyNodeCleaner as ENC

CATEGORY_MACRO = "FlightSim"
SUB_MENU_NAME = "Utilities"



def installMenu():
    createMacroScript(_func=ENC.runEmptyNodeCleaner, category="FlightSim", name="EmptyNodeCleaner", button_text="Empty Nodes Scene Cleaner")

    actionItem5 = rt.menuMan.createActionItem("EmptyNodeCleaner", "FlightSim")

    FlightSimMenu = rt.menuMan.findMenu(CATEGORY_MACRO)
    if not FlightSimMenu:
        FlightSimMenu = rt.menuMan.createMenu(CATEGORY_MACRO)

    AsoboUtilitiesMenu = rt.menuMan.findMenu(SUB_MENU_NAME)
    if not AsoboUtilitiesMenu:
        AsoboUtilitiesMenu = rt.menuMan.createMenu(SUB_MENU_NAME)

    AsoboUtilitiesItem = rt.menuMan.createSubMenuItem(SUB_MENU_NAME, AsoboUtilitiesMenu)

    safeAddItem(AsoboUtilitiesMenu, actionItem5)
    safeAddItem(FlightSimMenu, AsoboUtilitiesItem)

    rt.menuMan.updateMenuBar()


try:
    installMenu()
except Exception as error: 
    print("utilitiesMenu failed to install because {}".format(error))