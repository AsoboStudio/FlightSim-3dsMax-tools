from pymxs import runtime as rt
from maxsdk import sceneUtils,utility,qtUtils,layer
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *

def splitLayersToFiles():
    if(not qtUtils.popup_Yes_No("This operation could take some time....Are you sure?","Confirm")):
        return
    rootLayer = layer.getAllRootLayer()
    for l in rootLayer:
        nodes = layer.getAllNodeInLayerTree(l)
        rt.select(nodes)
        newFilePath =  rt.maxFilePath + l.name
        rt.saveNodes(nodes,newFilePath,quiet=True)

