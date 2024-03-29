from pymxs import runtime as rt
from .globals import *

def deleteCategoryAndContentCustomizations(categoryName):
    maxMenuBar = rt.menuMan.getMainMenuBar()
    FlightSimMenu = rt.menuman.findmenu(categoryName)
    if(FlightSimMenu is not None):
        items = getAllItem(FlightSimMenu)
        for item in items:
            FlightSimMenu.removeItem(item)
            print("removed {}".format(item.getTitle()))
    deleteItemByName(maxMenuBar,categoryName)
    rt.menuMan.updateMenuBar()

    layerQuadMenu = rt.menuMan.findQuadMenu("LayerExplorer Quad")
    for i in range(1,4):
        lMenu = layerQuadMenu.getMenu(i)
        deleteItemByName(lMenu, categoryName)
        
def deleteCategoryCustomizations(categoryName):
    """
    Delete all custom macro added by given category(menu,quad menu,toolbar,mouse,colors)
    """
    maxMenuBar = rt.menuMan.getMainMenuBar()
    deleteItemByName(maxMenuBar,categoryName)
    rt.menuMan.updateMenuBar()

    layerQuadMenu = rt.menuMan.findQuadMenu("LayerExplorer Quad")
    for i in range(1,4):
        lMenu = layerQuadMenu.getMenu(i)
        deleteItemByName(lMenu,categoryName)

def getItemByName(maxMenu,name):
    for i in range(1, maxMenu.numItems() + 1):
        mItem = maxMenu.getItem(i)
        if mItem and mItem.getTitle() == name:
            return mItem
    return None

def getAllItem(maxMenu):
    result = []
    for i in range(1, maxMenu.numItems() + 1):
        mItem = maxMenu.getItem(i)
        result.append(mItem)
        try:
            subMenu = mItem.getSubMenu()
            if(subMenu and subMenu.numItems() > 0):             
                result += getAllItem(subMenu)
        except Exception as e:
            print(e)
    return result


def deleteItemByName(maxMenu, name):
    if not maxMenu:
        print("No menu found with name: {0}".format(name))
        return
    toRemove = []
    for i in range(1, maxMenu.numItems() + 1):
        mItem = maxMenu.getItem(i)
        if mItem and mItem.getTitle() == name:
            toRemove.append(i)
    for index in toRemove:
        maxMenu.removeItemByPosition(index)

def hasItem(maxMenu, itemTitle):
    for i in range(1, maxMenu.numItems() + 1):
        mItem = maxMenu.getItem(i)
        if mItem.getTitle() == itemTitle:
            return True
    return False


def getItemIndex(maxMenu, item):
    for i in range(1, maxMenu.numItems() + 1):
        mItem = maxMenu.getItem(i)
        if mItem.getTitle() == item.getTitle():
            return i
    return -1


def safeAddItem(maxMenu, item):
    if hasItem(maxMenu, item.getTitle()):
        itemIndex = getItemIndex(maxMenu, item)
        maxMenu.removeItemByPosition(itemIndex)
        maxMenu.addItem(item, itemIndex)
    else:
        maxMenu.addItem(item, -1)


def createMacroScript(_func, category="", name="", tool_tip="", button_text="", *args):
    """Creates a macroscript"""
    if tool_tip == "":
        tool_tip = name
    if button_text == "":
        button_text = name

    try:
        # gets the qualified name for bound methods
        # ex: data_types.general_types.GMesh.center_pivot
        func_name = "{0}.{1}.{2}".format(_func.__module__, args[0].__class__.__name__, _func.__name__)
    except (IndexError, AttributeError):
        # gets the qualified name for unbound methods
        # ex: data_types.general_types.get_selection
        func_name = "{0}.{1}".format(_func.__module__, _func.__name__)

    script = """
    (
        python.Execute "import {}"
        python.Execute "{}()"
    )
    """.format(_func.__module__, func_name)
    rt.macros.new(category, name, tool_tip, button_text, script)



def createMacroScriptQt(_module,_widget,_func, category="", name="", tool_tip="", button_text="", *args):
    """Creates a macroscript"""
    if tool_tip == "":
        tool_tip = name
    if button_text == "":
        button_text = name

    module_name = "{0}".format(_module.__name__)
    class_name = "{0}".format(_widget.__name__)
    func_name = "{0}".format(_func.__name__)

    script = ""

    if MAXVERSION() <= MAX2019:
        script = """
        (
            python.Execute "from {} import *"
            python.Execute "import MaxPlus"
            python.Execute "ui = {}()"
            python.Execute "MaxPlus.AttachQWidgetToMax(ui)"
            python.Execute "ui.{}()"
        )
        """.format(module_name,class_name, func_name)
    else:
        script = """
                (
                    python.Execute "from {} import *"
                    python.Execute "ui = {}()"
                    python.Execute "ui.{}()"
                )
                """.format(module_name,class_name, func_name)

    rt.macros.new(category, name, tool_tip, button_text, script)

