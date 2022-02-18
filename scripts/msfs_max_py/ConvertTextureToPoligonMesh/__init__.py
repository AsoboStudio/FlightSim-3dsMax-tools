import os

from maxsdk.globals import *
from maxsdk.menu import * 
from pymxs import runtime as rt

import ConvertTextureToPoligonMesh.convertTextureToMesh as CTM

CATEGORY_MACRO = "FlightSim"
SUB_MENU_NAME = "Utilities"



def installMenu():
    createMacroScriptQt(_module=CTM,_widget=CTM.ConvertTextureToMeshWindow,_func=CTM.ConvertTextureToMeshWindow.show, category=CATEGORY_MACRO, name="ConvertTextureToMesh", button_text="Convert Texture To Mesh")

    actionItem7 = rt.menuMan.createActionItem("ConvertTextureToMesh", CATEGORY_MACRO)

    FlightSimMenu = rt.menuMan.findMenu(CATEGORY_MACRO)
    if not FlightSimMenu:
        FlightSimMenu = rt.menuMan.createMenu(CATEGORY_MACRO)

    AsoboUtilitiesMenu = rt.menuMan.findMenu(SUB_MENU_NAME)
    if not AsoboUtilitiesMenu:
        AsoboUtilitiesMenu = rt.menuMan.createMenu(SUB_MENU_NAME)

    AsoboUtilitiesItem = rt.menuMan.createSubMenuItem(SUB_MENU_NAME, AsoboUtilitiesMenu)

    safeAddItem(AsoboUtilitiesMenu, actionItem7)
    safeAddItem(FlightSimMenu, AsoboUtilitiesItem)

    rt.menuMan.updateMenuBar()


try:
    installMenu()
except Exception as error: 
    print("utilitiesMenu failed to install because {}".format(error))