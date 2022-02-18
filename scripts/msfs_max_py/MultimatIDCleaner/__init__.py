from pymxs import runtime as rt
from maxsdk.globals import *
from maxsdk.menu import * 

CATEGORY_MACRO = "FlightSim"
SUB_MENU_NAME = "Utilities"
import MultimatIDCleaner.multiMatIDCleaner as multiMatIDCleaner

def installMenu():
    createMacroScript(_func=multiMatIDCleaner.run, category="FlightSim", name="MultimatIDCleaner", button_text="Multimat ID Cleaner")

    actionItem = rt.menuMan.createActionItem("MultimatIDCleaner", "FlightSim")

    FlightSimMenu = rt.menuMan.findMenu(CATEGORY_MACRO)
    if not FlightSimMenu:
        FlightSimMenu = rt.menuMan.createMenu(CATEGORY_MACRO)

    AsoboUtilitiesMenu = rt.menuMan.findMenu(SUB_MENU_NAME)
    if not AsoboUtilitiesMenu:
        AsoboUtilitiesMenu = rt.menuMan.createMenu(SUB_MENU_NAME)

    AsoboUtilitiesItem = rt.menuMan.createSubMenuItem(SUB_MENU_NAME, AsoboUtilitiesMenu)

    safeAddItem(AsoboUtilitiesMenu, actionItem)
    safeAddItem(FlightSimMenu, AsoboUtilitiesItem)

    rt.menuMan.updateMenuBar()
 
try:
    installMenu()
except Exception as error: 
    print("MultimatIDCleaner failed import because {}".format(error))