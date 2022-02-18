from pymxs import runtime as rt
import os
from maxsdk.globals import *
from maxsdk.menu import * 
import sys
CATEGORY_MACRO = "FlightSim"
DEBUG_MODE_LOCAL = True

try:
    if rt.DEBUG_MODE != None:
        if rt.DEBUG_MODE:
            DEBUG_MODE_LOCAL = True  
        else:
            DEBUG_MODE_LOCAL = False
        print("Local DEBUG MODE : {0}".format(DEBUG_MODE_LOCAL))
except:
    print("No Custom Macro added")

import DeveloperTool.PythonScriptsReloader as ScrptRel
    
    

def installMenu():
    createMacroScript(_func=ScrptRel.ReloadPackages, category=CATEGORY_MACRO, name="PythonScriptsReloader", button_text="Python Scripts Reloader")
    actionItem = rt.menuMan.createActionItem("PythonScriptsReloader",CATEGORY_MACRO)
    FlightSimMenu = rt.menuman.findmenu(CATEGORY_MACRO)
    maxMenuBar = rt.menuMan.getMainMenuBar()


    FlightSimMenu = rt.menuMan.findMenu(CATEGORY_MACRO)
    if not FlightSimMenu:
        FlightSimMenu = rt.menuMan.createMenu(CATEGORY_MACRO)

    safeAddItem(FlightSimMenu, actionItem)
    safeAddItem(maxMenuBar, rt.menuMan.createSubMenuItem(CATEGORY_MACRO, FlightSimMenu))
    rt.menuMan.updateMenuBar()


if(DEBUG_MODE_LOCAL):
    try:
        installMenu()
    except Exception as error: 
        print("script failed to install because {}".format(error))