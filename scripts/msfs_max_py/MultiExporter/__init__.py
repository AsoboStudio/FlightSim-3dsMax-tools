import os
import sys
from maxsdk.globals import *
from maxsdk.menu import * 
from pymxs import runtime as rt
    
CATEGORY_MACRO = "FlightSim"



import MultiExporter.multiExporter as ME
    
def installMenu():
    createMacroScriptQt(_module=ME, _widget=ME.MainWindow,_func=ME.MainWindow.show, category=CATEGORY_MACRO, name="MultiExporter", button_text="Multi Exporter")

    actionItem = rt.menuMan.createActionItem("MultiExporter", CATEGORY_MACRO)

    FlightSimMenu = rt.menuMan.findMenu(CATEGORY_MACRO)
    if not FlightSimMenu:
        FlightSimMenu = rt.menuMan.createMenu(CATEGORY_MACRO)

    safeAddItem(FlightSimMenu, actionItem)
    rt.menuMan.updateMenuBar()

try:
    installMenu()
    print("loaded MultiExporter")
except Exception as error: 
    print("MultiExporter failed import because {}".format(error))