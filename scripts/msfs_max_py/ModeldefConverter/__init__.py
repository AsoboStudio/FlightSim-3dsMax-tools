from pymxs import runtime as rt
from maxsdk.globals import *
from maxsdk.menu import * 
import sys
CATEGORY_MACRO = "FlightSim"

import ModeldefConverter.xml2jsonAnimationGroup as xml2json

def installMenu():
    createMacroScript(_func=xml2json.run, category="FlightSim", name="ConvertModelDefToJson", button_text="Legacy modeldef Converter")

    actionItem = rt.menuMan.createActionItem("ConvertModelDefToJson", "FlightSim")

    FlightSimMenu = rt.menuMan.findMenu(CATEGORY_MACRO)
    if not FlightSimMenu:
        FlightSimMenu = rt.menuMan.createMenu(CATEGORY_MACRO)

    maxMenuBar = rt.menuMan.getMainMenuBar()
    safeAddItem(FlightSimMenu, actionItem)
    safeAddItem(maxMenuBar, rt.menuMan.createSubMenuItem(CATEGORY_MACRO, FlightSimMenu))

    rt.menuMan.updateMenuBar()
 
try:
    installMenu()
except Exception as error: 
    print("ConvertModelDefToJson failed import because {}".format(error))