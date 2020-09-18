import os
import sys
from pymxs import runtime as rt
from maxsdk import menu as sdkmenu
from maxsdk.globals import *

toolFolder = os.path.dirname(__file__)
if toolFolder not in sys.path:
    sys.path.append(toolFolder)

import PBRviewport


def installMenu():

    sdkmenu.createMacroScript(_func=PBRviewport.UseStudioIBL, category="FlightSim", name="SetStudioIBL")
    sdkmenu.createMacroScript(_func=PBRviewport.UseExteriorIBL, category="FlightSim", name="SetExteriorIBL")
    sdkmenu.createMacroScript(_func=PBRviewport.UseInteriorIBL, category="FlightSim", name="SetInteriorIBL")
    sdkmenu.createMacroScript(_func=PBRviewport.UseLegacyShader, category="FlightSim", name="UseLegacyShader")

    actionItem0 = rt.menuMan.createActionItem("SetStudioIBL", "FlightSim")
    actionItem1 = rt.menuMan.createActionItem("SetExteriorIBL", "FlightSim")
    actionItem2 = rt.menuMan.createActionItem("SetInteriorIBL", "FlightSim")
    actionItem3 = rt.menuMan.createActionItem("UseLegacyShader", "FlightSim")

    generalLabelMenu = rt.menuman.findmenu("Views - General Viewport Label Menu")
    FlightSimIBLMenu = rt.menuMan.createMenu("FlightSim IBL")
    FlightSimIBLItem = rt.menuMan.createSubMenuItem("FlightSim IBL", FlightSimIBLMenu)

    sdkmenu.safeAddItem(FlightSimIBLMenu, actionItem0)
    sdkmenu.safeAddItem(FlightSimIBLMenu, actionItem1)
    sdkmenu.safeAddItem(FlightSimIBLMenu, actionItem2)
    sdkmenu.safeAddItem(FlightSimIBLMenu, actionItem3)
    sdkmenu.safeAddItem(generalLabelMenu, FlightSimIBLItem)

