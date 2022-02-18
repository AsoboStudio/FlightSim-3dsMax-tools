import os

from maxsdk.globals import *
from maxsdk.menu import * 
from pymxs import runtime as rt

import SameNameNodeChecker.sameNameNodeChecker as SNC

CATEGORY_MACRO = "FlightSim"
SUB_MENU_NAME = "Utilities"



def installMenu():
    createMacroScript(_func=SNC.run, category="FlightSim", name="SameNameNodeChecker", button_text="Dupl node's name tool")

    actionItem6 = rt.menuMan.createActionItem("SameNameNodeChecker", "FlightSim")

    FlightSimMenu = rt.menuMan.findMenu(CATEGORY_MACRO)
    if not FlightSimMenu:
        FlightSimMenu = rt.menuMan.createMenu(CATEGORY_MACRO)

    AsoboUtilitiesMenu = rt.menuMan.findMenu(SUB_MENU_NAME)
    if not AsoboUtilitiesMenu:
        AsoboUtilitiesMenu = rt.menuMan.createMenu(SUB_MENU_NAME)

    AsoboUtilitiesItem = rt.menuMan.createSubMenuItem(SUB_MENU_NAME, AsoboUtilitiesMenu)

    safeAddItem(AsoboUtilitiesMenu, actionItem6)
    safeAddItem(FlightSimMenu, AsoboUtilitiesItem)

    rt.menuMan.updateMenuBar()


try:
    installMenu()
except Exception as error: 
    print("utilitiesMenu failed to install because {}".format(error))