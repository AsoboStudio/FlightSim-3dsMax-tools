import os

import sys

from pymxs import runtime as rt

from maxsdk import menu as sdkmenu


toolFolder = os.path.dirname(__file__)

if toolFolder not in sys.path:
    sys.path.append(toolFolder)

import AnimationTool.main as animtoolmain


def installMenu():

    animtoolPath = os.path.join(os.path.dirname(__file__), "main.py")
    macroscript = r'\
            macroScript FlightSimAnimationTool\
            category: "FlightSim"\
            tooltip: "Animation Tools"\
            (on execute do python.ExecuteFile "{0}")'.format(animtoolPath)

    rt.execute(macroscript)
    actionItem = rt.menuMan.createActionItem("FlightSimAnimationTool", "FlightSim")

    FlightSimMenu = rt.menuman.findmenu("FlightSim")
    maxMenuBar = rt.menuMan.getMainMenuBar()
    if FlightSimMenu:
        sdkmenu.safeAddItem(FlightSimMenu, actionItem)
        sdkmenu.safeAddItem(maxMenuBar, rt.menuMan.createSubMenuItem("FlightSim", FlightSimMenu))
    else:
        print("Cannot find FlightSim menu")

    rt.menuMan.updateMenuBar()
