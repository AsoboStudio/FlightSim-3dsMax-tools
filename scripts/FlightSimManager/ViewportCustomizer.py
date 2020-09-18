from pymxs import runtime as rt
from maxsdk.globals import *
import os
import maxsdk.menu as sdkmenu


import FlightSimManager.Constants

def isMax2019v3orSuperior():
    if rt.maxversion()[0] > 21000:
        return True
    elif rt.maxversion()[0] == 21000 and len(rt.maxversion())==9 and rt.maxversion()[8] == ".3 Update"  :
        return True
    else:
        return False

try:
    import ModeldefConverter.setupMenu as modeldefConverterMenu
except Exception as error: 
    print("ModeldefConverter failed import because {}".format(error))

if(isMax2019v3orSuperior()):
    try:
        import MultiExporter.setupMenu as multiExporterMenu
    except Exception as error: 
        print("MultiExporter failed import because {}".format(error))
    try:
        import WiperTool.setupMenu as wiperMenu
    except Exception as error: 
        print("WiperTool failed import because {}".format(error))
    try:
        import PBRViewportManager.setupMenu as pbrviewportmenu
    except Exception as error:
        print("PBRViewportManager failed import because{}".format(error))
    try:
        import Validations.setupMenu as validationsMenu
    except Exception as error: 
        print("Validations failed import because {}".format(error))
    try:
        import Utilities.setupMenu as utilitiesMenu
    except Exception as error: 
        print("Utilities failed import because {}".format(error))
    try:
        import AnimationTool.setupMenu as animationToolMenu
    except Exception as error: 
        print("AnimationTool failed import because {}".format(error))
    try:
        import LODsTool.setupMenu as lodstool
    except Exception as error: 
        print("LODsTool failed import because {}".format(error))



def installCustomizations():
    """
    Install all customizations in viewport relatives to this package(menu,quadmenu,toolbar,mouse,colors)
    """
    flightSimMenu = rt.menuMan.findMenu(FlightSimManager.Constants.CUSTOM_VIEWPORT_CATEGORY)
    if flightSimMenu is not None:
        rt.menuMan.unRegisterMenu(flightSimMenu)
        
    c = os.path.dirname(__file__)

    cmd = 'filein @"{0}\\..\\FlightSim_EntryPoint.ms"'.format(c)
    rt.execute(cmd)

    try:
        modeldefConverterMenu.installMenu()
    except Exception as error: 
        print("modeldefConverterMenu failed to install because {}".format(error))

    
    if(isMax2019v3orSuperior()):
        try:
            wiperMenu.installMenu()
        except Exception as error: 
            print("PBRViewportManager failed to install because {}".format(error))
        try:
            multiExporterMenu.installMenu()
        except Exception as error: 
            print("multiExporterMenu failed to install because {}".format(error))
        try:
            pbrviewportmenu.installMenu()
        except Exception as error: 
            print("PBRViewportManager failed to install because {}".format(error))
        try:
            validationsMenu.installMenu()
        except Exception as error: 
            print("validationsMenu failed to install because {}".format(error))
        try:
            utilitiesMenu.installMenu()
        except Exception as error: 
            print("utilitiesMenu failed to install because {}".format(error))
        try:
            animationToolMenu.installMenu()
        except Exception as error: 
            print("animationToolMenu failed to install because {}".format(error))
        try:
            lodstool.installMenu()
        except Exception as error: 
            print("lodstool failed to install because {}".format(error))
        