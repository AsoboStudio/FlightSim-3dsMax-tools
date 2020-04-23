from pymxs import runtime as rt

import maxsdk.menu as sdkmenu
reload(sdkmenu)

import PBRViewportManager.setupMenu as pbrviewportmenu
reload(pbrviewportmenu)

import MultiExporter.setupMenu as multiExporterMenu
reload(multiExporterMenu)

import FlightSimManager.Constants
reload(FlightSimManager.Constants)

import Validations.setupMenu as validationsMenu
reload(validationsMenu)

import Utilities.setupMenu as utilitiesMenu
reload(utilitiesMenu)

if rt.maxversion()[0]>20000:
    import AnimationTool.setupMenu as animationToolMenu
    reload(animationToolMenu)

    import LODsTool.setupMenu as lodstool
    reload(lodstool)

    import AnimationExporter.setupMenu as animationExporterMenu
    reload(animationExporterMenu)

    import WiperTool.setupMenu as wiperMenu
    reload(wiperMenu)


def installCustomizations():
    """
    Install all customizations in viewport relatives to this package(menu,quadmenu,toolbar,mouse,colors)
    """
    ####
    #remove previouse quad menu handled with a category different from Constants.CUSTOM_VIEWPORT_CATEGORY,
    # we need to remove it manually, we can remove this after a "secure period" of 2-3 months
    layerQuadMenu = rt.menuMan.findQuadMenu("LayerExplorer Quad")
    for i in range(1, 4):
        lMenu = layerQuadMenu.getMenu(i)
        sdkmenu.deleteItemByName(lMenu, "FlightSim Airport Team")
        sdkmenu.deleteItemByName(lMenu, "FlightSim Environment")
    ####

    sdkmenu.deleteCategoryCustomizations(FlightSimManager.Constants.CUSTOM_VIEWPORT_CATEGORY)

    pbrviewportmenu.installMenu()
    validationsMenu.installMenu()
    multiExporterMenu.installMenu()

    utilitiesMenu.installMenu()
if rt.maxversion()[0]>20000:
    animationToolMenu.installMenu()
    lodstool.installMenu()
    animationExporterMenu.installMenu()
    wiperMenu.installMenu()