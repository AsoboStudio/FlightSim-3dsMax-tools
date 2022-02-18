from pymxs import runtime as rt

import os
from maxsdk.globals import *
from maxsdk.menu import * 

CATEGORY_MACRO = "FlightSim"

import lodtool
    
def installMenu():
    createMacroScript(_func=lodtool.run, category=CATEGORY_MACRO, name="FlightSimLODUtilities", button_text="LOD Utilities")

    actionItem = rt.menuMan.createActionItem("FlightSimLODUtilities",CATEGORY_MACRO)

    FlightSimMenu = rt.menuMan.findMenu(CATEGORY_MACRO)
    if not FlightSimMenu:
        FlightSimMenu = rt.menuMan.createMenu(CATEGORY_MACRO)

    maxMenuBar = rt.menuMan.getMainMenuBar()
    safeAddItem(FlightSimMenu, actionItem)
    safeAddItem(maxMenuBar, rt.menuMan.createSubMenuItem(CATEGORY_MACRO, FlightSimMenu))

    rt.menuMan.updateMenuBar()
 
try:
    installMenu()
    print("laoded Lodtool package")
except Exception as error: 
    print("LODsTool failed import because {}".format(error))