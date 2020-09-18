import os
import sys
from pymxs import runtime as rt
from maxsdk import menu as sdkmenu

from WiperTool import WiperToolLoader
toolFolder = os.path.dirname(__file__)
if toolFolder not in sys.path:
    sys.path.append(toolFolder)

def installMenu():

    sdkmenu.createMacroScript(_func=WiperToolLoader.run, category="FlightSim", name="WiperMaskGenerator", button_text="Wiper Mask Generator")

    actionItem = rt.menuMan.createActionItem("WiperMaskGenerator", "FlightSim")
    FlightSimMenu = rt.menuman.findmenu("FlightSim")
    maxMenuBar = rt.menuMan.getMainMenuBar()
    if FlightSimMenu:
        sdkmenu.safeAddItem(FlightSimMenu, actionItem)
        sdkmenu.safeAddItem(maxMenuBar, rt.menuMan.createSubMenuItem("FlightSim", FlightSimMenu))
    else:
        print("Cannot find FlightSim menu")

    rt.menuMan.updateMenuBar()
