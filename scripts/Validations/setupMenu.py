import os
import sys
from pymxs import runtime as rt
from maxsdk import menu as sdkmenu

toolFolder = os.path.dirname(__file__)
if toolFolder not in sys.path:
    sys.path.append(toolFolder)

import fix_node_names
import layer_validation
import lods_hierachy
import unique_names
import node_validation
import rebuild_mesh

CATEGORY_MACRO = "FlightSim"
SUB_MENU_NAME = "Plane Validation"

def installMenu():

    sdkmenu.createMacroScript(_func=fix_node_names.run, category=CATEGORY_MACRO, name="FixEndLines", button_text="Fix End Lines")
    sdkmenu.createMacroScript(_func=layer_validation.run, category=CATEGORY_MACRO, name="Layers")
    sdkmenu.createMacroScript(_func=lods_hierachy.run, category=CATEGORY_MACRO, name="LODsHierarchy", button_text="LODs Hierarchy")
    sdkmenu.createMacroScript(_func=unique_names.run, category=CATEGORY_MACRO, name="UniqueNames", button_text= "Unique Names")
    sdkmenu.createMacroScript(_func=node_validation.run, category=CATEGORY_MACRO, name="Nodes")
    sdkmenu.createMacroScript(_func=rebuild_mesh.run, category=CATEGORY_MACRO, name="RebuildNodes", button_text="Rebuild Nodes (risky)")

    actionItem0 = rt.menuMan.createActionItem("FixEndLines", CATEGORY_MACRO)
    actionItem1 = rt.menuMan.createActionItem("Layers", CATEGORY_MACRO)
    actionItem2 = rt.menuMan.createActionItem("LODsHierarchy", CATEGORY_MACRO)
    actionItem3 = rt.menuMan.createActionItem("Nodes", CATEGORY_MACRO)
    actionItem4 = rt.menuMan.createActionItem("UniqueNames", CATEGORY_MACRO)
    actionItem5 = rt.menuMan.createActionItem("RebuildNodes", CATEGORY_MACRO)

    FlightSimMenu = rt.menuMan.findMenu(CATEGORY_MACRO)
    if not FlightSimMenu:
        FlightSimMenu = rt.menuMan.createMenu(CATEGORY_MACRO)

    PlaneValidationMenu = rt.menuMan.findMenu(SUB_MENU_NAME)
    if not PlaneValidationMenu:
        PlaneValidationMenu = rt.menuMan.createMenu(SUB_MENU_NAME)

    PlaneValidationItem = rt.menuMan.createSubMenuItem(SUB_MENU_NAME, PlaneValidationMenu)

    sdkmenu.safeAddItem(PlaneValidationMenu, actionItem0)
    sdkmenu.safeAddItem(PlaneValidationMenu, actionItem1)
    sdkmenu.safeAddItem(PlaneValidationMenu, actionItem2)
    sdkmenu.safeAddItem(PlaneValidationMenu, actionItem3)
    sdkmenu.safeAddItem(PlaneValidationMenu, actionItem4)
    sdkmenu.safeAddItem(PlaneValidationMenu, actionItem5)
    sdkmenu.safeAddItem(FlightSimMenu, PlaneValidationItem)

    rt.menuMan.updateMenuBar()