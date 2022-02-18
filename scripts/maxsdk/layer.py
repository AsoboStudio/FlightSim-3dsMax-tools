"""
This module contains functions to handle layers in 3dsMax
"""

import pymxs
from maxsdk.globals import *
if MAXVERSION() < MAX2017:
    import MaxPlus

rt = pymxs.runtime

def getLayerChildren(root, result):
    """
    Recursively get all the descendant layers (including self) of a layer
    
    \nin: 
    root=(MixinInterface.LayerProperties)
    \nin-out:
    result=list(MixinInterface.LayerProperties)
    """
    if root:
        try:
            num_children = root.getNumChildren()
            result.append(root)
            for i in range(1, num_children + 1):
                child = root.getChild(i)
                getLayerChildren(child, result)
        except:
            print("impossible to getLayerChildren of {}".format(root))



def getLayerDescendants(roots):
    """
    Returns all the descendant layers (including self) of all the layers specified.
    
    \nin: 
    list(MixinInterface.LayerProperties)
    \nout:
    list(MixinInterface.LayerProperties)
    """
    result = []
    for r in roots:
        res = []
        getLayerChildren(r,res)
        result += res
    return result

def getChildrenLayer(layer):
    """
    Get the children layers. All the children of children recursively.
    
    \nin: 
    MixinInterface.LayerProperties
    \nout:
    MixinInterface.LayerProperties
    """
    result = [] 
    if layer is not None:
        num_children = layer.getNumChildren()
        for i in range(1, num_children+1):
            child = layer.getChild(i)
            result.append(child)
    return result

def getParentLayer(layer):
    """
    Get the parent layer

    \nin: 
    MixinInterface.LayerProperties
    \nout:
    MixinInterface.LayerProperties
    """
    return layer.getParent()

def getRootLayer(layer):
    """
    Find the root of the layer by going up the parent chain.

    \nin: 
    MixinInterface.LayerProperties
    \nout:
    MixinInterface.LayerProperties
    """
    if(layer.getParent() != None):
        return getRootLayer(layer.getParent())
    else:
        return layer

 
def getAllRootLayer():
    """
    Returns all the root layer in the scene. A root layer is a layer without any parent.

    \nout:
    list(MixinInterface.LayerProperties)
    """
    result = []
    layers = getAllLayers()
    for l in layers:
        if(getParentLayer(l) == None):
            result.append(l)
    return result


def getAllLayers():
    """
    Returns all layers in the scene
    
    \nout:
    list(MixinInterface.LayerProperties)
    """
    result = []
    count = rt.LayerManager.count
    for i in range(count):
        layer = rt.LayerManager.GetLayer(i)
        result.append(layer)
    return result

def getAllLayersMP():
    result = []
    count = MaxPlus.LayerManager.GetNumLayers()
    for i in range(count):
        layer = MaxPlus.LayerManager.GetLayer(i)
        result.append(layer)
    return result

def get_layer(name):
    if MAXVERSION() < MAX2017:
        return MaxPlus.LayerManager.GetLayer(name)
    else:
        return rt.layermanager.getLayerFromName(name) #Pythonysation de maxscript

def getAllNodeInLayerTree(layer):
    result = []
    descendants = []
    getLayerChildren(layer,descendants)
    for l in descendants:
        for n in getDependentsOfLayer(l):
            result.append(n)
    return result

def getAllNodeInLayerHierarchyMP(rootLayer):
    """
    Returns all node contained in a layer hierarchy.

    \nin: 
    rootLayer= MaxPlus base layer
    \nout:
    list of MaxPlus.INode
    """
    result_list = []
    lyrList = []
    getLayerChildren(rootLayer, lyrList)
    for l in lyrList:
        mp_layer = MaxPlus.LayerManager.GetLayer(l.name)
        lyr_nodes_children = mp_layer.GetNodes()
        for n in lyr_nodes_children:
            result_list.append(n)
    return result_list

def getAllNodeInLayerTree(layer):
    result = []
    descendants = []
    getLayerChildren(layer,descendants)
    for l in descendants:
        for n in getDependentsOfLayer(l):
            result.append(n)
    return result


def getDependentsOfLayer(lay):
    """
    Get every valid node dependent on the specified layer.

    \nin:
    lay=MixinInterface.LayerProperties

    \nout: 
    list(node)
    """
    result = []
    layerRT = lay.layerAsRefTarg
    lyr_nodes_children = rt.refs.dependents(layerRT)
    for n in lyr_nodes_children:
        if(rt.isvalidnode(n) and n not in result):
            result.append(n)
    return result

def getNodesInLayer(lay):
    """
    Returns all the nodes in a layer

    \nin:
    lay= MixinInterface.LayerProperties

    \nout:
    pymxs.MXSWrapperBase
    """
    result = []
    lay.nodes(pymxs.mxsreference(result))
    return result

def getSelectedLayer():
    """
    Returns the first selected layer in the scene. Check first if an explorer is open, if so it will get these selected items. 

    \nout: 
    MaxPlus.Layer
    """
    explorer = rt.SceneExplorerManager.GetActiveExplorer()
    if (explorer == None):
        layer = rt.getCurrentSelection()
    else:
        layer = explorer.SelectedItems()
    count = rt.getProperty(layer, "count")
    if count <= 0:
        rt.messageBox("Please select a layer")
        return
    selectedLayerName = layer[0].name

    return (MaxPlus.LayerManager.GetLayer(selectedLayerName)) if (MAXVERSION() < MAX2017) else rt.layermanager.getLayerFromName(selectedLayerName)

def getSelectedLayerMP():
    """
    Returns the first selected layer in the scene. Check first if an explorer is open, if so it will get these selected items. 

    \nout: 
    MaxPlus.Layer
    """
    explorer = rt.SceneExplorerManager.GetActiveExplorer()
    if (explorer == None):
        layer = rt.getCurrentSelection()
    else:
        layer = explorer.SelectedItems()
    count = rt.getProperty(layer, "count")
    if count <= 0:
        rt.messageBox("Please select a layer")
        return
    selectedLayerName = layer[0].name

    return MaxPlus.LayerManager.GetLayer(selectedLayerName)

def deleteAllEmptyLayerHierarchies():
    """
    Attempts to delete all layers. Non empty ones are kept by 3dsMax automatically
    """
    layers = getAllRootLayer()
    for lay in layers:
        rt.layerManager.deleteLayerHierarchy(lay.name)


def disableAll():
    """
    Disable every layer in the scene
    """
    layers = getAllLayers()
    disableThese(layers)

def _visibilityInHierarchy(layer, state):
    """
    Recursive Function to enable every direct parents of a layer.

    \nin: 
    layer = pymxs.runtime.MixinInterface.LayerProperties
    state = bool
    """
    layer.on = state
    parent = layer.getParent()
    if parent is not None:
        _visibilityInHierarchy(parent, state)


def enableThese(layers):
    """
    Enables a list of layer. This will also enable the parents of the layer.

    \nin:
    layers = list(MixinInterface.LayerProperties)
    """
    for layer in layers:
        _visibilityInHierarchy(layer, True)

def enableTheseAndTheirDescendant(layers):
    getLayerDescendants(layers)

def disableThese(layers):
    """
    Disable a list of layer.

    \nin:
    layers = list(MixinInterface.LayerProperties)
    """
    for layer in layers:
        layer.on = False

def getLayerFromNode(node):
    node.layer.name
