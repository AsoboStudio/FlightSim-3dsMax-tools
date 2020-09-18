import os
import sys

import MultiExporter.multiExporter as multiExporter
from maxsdk import menu as sdkmenu
from pymxs import runtime as rt


toolFolder = os.path.dirname(__file__)
if toolFolder not in sys.path:
    sys.path.append(toolFolder)
    


def installMenu():
    sdkmenu.createMacroScript(_func=multiExporter.run, category="FlightSim", name="MultiExporter", button_text="Multi Exporter")
    actionItem = rt.menuMan.createActionItem("MultiExporter", "FlightSim")
    FlightSimMenu = rt.menuman.findmenu("FlightSim")
    maxMenuBar = rt.menuMan.getMainMenuBar()
    if FlightSimMenu:
        sdkmenu.safeAddItem(FlightSimMenu, actionItem)
        sdkmenu.safeAddItem(maxMenuBar, rt.menuMan.createSubMenuItem("FlightSim", FlightSimMenu))
    else:
        print("Cannot find FlightSim menu")
    rt.menuMan.updateMenuBar()
