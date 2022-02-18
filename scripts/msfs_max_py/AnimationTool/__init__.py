import os

from maxsdk.globals import *
from maxsdk.menu import * 
from pymxs import runtime as rt
    
CATEGORY_MACRO = "FlightSim"



import mainWindow as MW

def installMenu():
    createMacroScriptQt(_module=MW, _widget=MW.MainView,_func=MW.MainView.show, category=CATEGORY_MACRO, name="AnimationTools", button_text="Animation Tools")

    actionItem = rt.menuMan.createActionItem("AnimationTools", CATEGORY_MACRO)

    FlightSimMenu = rt.menuMan.findMenu(CATEGORY_MACRO)
    if not FlightSimMenu:
        FlightSimMenu = rt.menuMan.createMenu(CATEGORY_MACRO)

    safeAddItem(FlightSimMenu, actionItem)
    rt.menuMan.updateMenuBar()

try:
    installMenu()
    print("loaded AnimationTools")
except Exception as error: 
    print("AnimationTools failed import because {}".format(error))