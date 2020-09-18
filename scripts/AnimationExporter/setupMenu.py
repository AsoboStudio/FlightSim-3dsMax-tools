import os

import sys

from pymxs import runtime as rt

from maxsdk import menu as sdkmenu


toolFolder = os.path.dirname(__file__)

if toolFolder not in sys.path:
    sys.path.append(toolFolder)


def installMenu():

    animExportPath = os.path.join(os.path.dirname(__file__), "animexporter.py")
    macroscript = r'\
        macroScript FlightSimAnimationExporter\
        category: "FlightSim"\
        tooltip: "Animation Exporter"\
        (on execute do python.ExecuteFile "{0}")'.format(animExportPath)

    rt.execute(macroscript)


    actionItem = rt.menuMan.createActionItem("FlightSimAnimationExporter", "FlightSim")

    FlightSimMenu = rt.menuman.findmenu("FlightSim")
    maxMenuBar = rt.menuMan.getMainMenuBar()
    if FlightSimMenu:
        sdkmenu.safeAddItem(FlightSimMenu, actionItem)
        sdkmenu.safeAddItem(maxMenuBar, rt.menuMan.createSubMenuItem("FlightSim", FlightSimMenu))
    else:
        print "Cannot find FlightSim menu"

    rt.menuMan.updateMenuBar()
