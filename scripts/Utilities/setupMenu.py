import os

import sys

from pymxs import runtime as rt

from maxsdk import menu as sdkmenu


toolFolder = os.path.dirname(__file__)

if toolFolder not in sys.path:
    sys.path.append(toolFolder)

import Utilities.updateContainerID as updateContainerID
import Utilities.countMaterial as countMaterial
import Utilities.xml2jsonAnimationGroup as xml2json

CATEGORY_MACRO = "FlightSim"
SUB_MENU_NAME = "Babylon Utilities"

def installMenu():
    sdkmenu.createMacroScript(_func=updateContainerID.run, category="FlightSim", name="UpdateContainerID", button_text= "Update Container ID")
    sdkmenu.createMacroScript(_func=countMaterial.run, category="FlightSim", name="CountMaterialOnSelection", button_text="Count Materials")
    sdkmenu.createMacroScript(_func=xml2json.run, category="FlightSim", name="ConvertModelDefToJson", button_text="Legacy modeldef Converter")

    actionItem0 = rt.menuMan.createActionItem("UpdateContainerID", "FlightSim")
    actionItem1 = rt.menuMan.createActionItem("CountMaterialOnSelection", "FlightSim")
    actionItem2 = rt.menuMan.createActionItem("ConvertModelDefToJson", "FlightSim")

    FlightSimMenu = rt.menuMan.findMenu(CATEGORY_MACRO)
    if not FlightSimMenu:
        FlightSimMenu = rt.menuMan.createMenu(CATEGORY_MACRO)

    BabylonUtilitesMenu = rt.menuMan.findMenu(SUB_MENU_NAME)
    if not BabylonUtilitesMenu:
        BabylonUtilitesMenu = rt.menuMan.createMenu(SUB_MENU_NAME)

    BabylonUtilitesItem = rt.menuMan.createSubMenuItem(SUB_MENU_NAME, BabylonUtilitesMenu)

    sdkmenu.safeAddItem(BabylonUtilitesMenu, actionItem0)
    sdkmenu.safeAddItem(FlightSimMenu, BabylonUtilitesItem)
    sdkmenu.safeAddItem(FlightSimMenu, actionItem1)
    sdkmenu.safeAddItem(FlightSimMenu, actionItem2)

    rt.menuMan.updateMenuBar()