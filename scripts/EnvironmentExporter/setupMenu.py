import os
import sys
from pymxs import runtime as rt
from maxsdk import menu as sdkmenu
reload(sdkmenu)

toolFolder = os.path.dirname(__file__)
if toolFolder not in sys.path:
    sys.path.append(toolFolder)

import lodsExporter
import envAssetExporter
reload(lodsExporter)
reload(envAssetExporter)

LODS_EXP_MACRO = "ExportEnvironmentLODs"
ENV_EXP_MACRO = "ExportEnvironmentAsset"
CATEGORY_MACRO = "FlightSim"

def installQuadMenu():
    sdkmenu.createMacroScript(_func=lodsExporter.run, category=CATEGORY_MACRO, name=LODS_EXP_MACRO,button_text="Export LODs")
    sdkmenu.createMacroScript(_func=envAssetExporter.run, category=CATEGORY_MACRO, name=ENV_EXP_MACRO,button_text="Export Env Asset")

    actionItem0 = rt.menuMan.createActionItem(LODS_EXP_MACRO, CATEGORY_MACRO)
    actionItem1 = rt.menuMan.createActionItem(ENV_EXP_MACRO, CATEGORY_MACRO)


    layerQuadMenu = rt.menuMan.findQuadMenu("LayerExplorer Quad")
    layerMenu = layerQuadMenu.getMenu(1)
    FlightSimMenu = rt.menuMan.createMenu(CATEGORY_MACRO)
    FlightSimItem = rt.menuMan.createSubMenuItem(CATEGORY_MACRO,FlightSimMenu)

    sdkmenu.safeAddItem(FlightSimMenu, actionItem0)
    sdkmenu.safeAddItem(FlightSimMenu, actionItem1)
    sdkmenu.safeAddItem(layerMenu, FlightSimItem)
