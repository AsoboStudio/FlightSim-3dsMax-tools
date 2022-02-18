from pymxs import runtime as rt
import os
from maxsdk.globals import *
from maxsdk.menu import * 
import sys


CATEGORY_MACRO = "FlightSim"

import PBRViewportManager.PBRviewport as  PBRviewport


def installMenu():
    createMacroScript(_func=PBRviewport.UseStudioIBL, category="FlightSim", name="SetStudioIBL")
    createMacroScript(_func=PBRviewport.UseExteriorIBL, category="FlightSim", name="SetExteriorIBL")
    createMacroScript(_func=PBRviewport.UseInteriorIBL, category="FlightSim", name="SetInteriorIBL")
    createMacroScript(_func=PBRviewport.UseLegacyShader, category="FlightSim", name="UseLegacyShader")

    actionItem0 = rt.menuMan.createActionItem("SetStudioIBL", "FlightSim")
    actionItem1 = rt.menuMan.createActionItem("SetExteriorIBL", "FlightSim")
    actionItem2 = rt.menuMan.createActionItem("SetInteriorIBL", "FlightSim")
    actionItem3 = rt.menuMan.createActionItem("UseLegacyShader", "FlightSim")

    generalLabelMenu = rt.menuman.findmenu("Views - General Viewport Label Menu")
    FlightSimIBLMenu = rt.menuMan.createMenu("FlightSim IBL")
    FlightSimIBLItem = rt.menuMan.createSubMenuItem("FlightSim IBL", FlightSimIBLMenu)

    safeAddItem(FlightSimIBLMenu, actionItem0)
    safeAddItem(FlightSimIBLMenu, actionItem1)
    safeAddItem(FlightSimIBLMenu, actionItem2)
    safeAddItem(FlightSimIBLMenu, actionItem3)
    safeAddItem(generalLabelMenu, FlightSimIBLItem)

try:
    installMenu()
except Exception as error: 
    print("PBRViewportManager failed to install because {}".format(error))