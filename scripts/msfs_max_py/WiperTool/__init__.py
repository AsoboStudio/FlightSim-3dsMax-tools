from pymxs import runtime as rt

import os
from maxsdk.globals import *
from maxsdk.menu import * 

import WiperToolLoader
CATEGORY_MACRO = "FlightSim"

def installMenu():

    createMacroScript(_func=WiperToolLoader.run, category=CATEGORY_MACRO, name="WiperMaskGenerator", button_text="Wiper Mask Generator")

    actionItem = rt.menuMan.createActionItem("WiperMaskGenerator", CATEGORY_MACRO)
    FlightSimMenu = rt.menuman.findmenu(CATEGORY_MACRO)
    maxMenuBar = rt.menuMan.getMainMenuBar()

    FlightSimMenu = rt.menuMan.findMenu(CATEGORY_MACRO)
    if not FlightSimMenu:
        FlightSimMenu = rt.menuMan.createMenu(CATEGORY_MACRO)

    safeAddItem(FlightSimMenu, actionItem)
    safeAddItem(maxMenuBar, rt.menuMan.createSubMenuItem(CATEGORY_MACRO, FlightSimMenu))

    rt.menuMan.updateMenuBar()

try:
    installMenu()
except Exception as error: 
    print("WiperMaskGenerator failed import because {}".format(error))