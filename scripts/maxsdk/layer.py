import pymxs
import MaxPlus

rt = pymxs.runtime


def getLayerChildren(root, result):
    if root is not None:
        num_children = root.getNumChildren()
        result.append(root)
        for i in range(1, num_children + 1):
            child = root.getChild(i)
            getLayerChildren(child, result)

def getLayerDescendants(roots):
    result = []
    for r in roots:
        res = []
        getLayerChildren(r,res)
        result += res
    return result

def getChildrenLayer(layer):   
    result = [] 
    if layer is not None:
        num_children = layer.getNumChildren()
        for i in range(1, num_children+1):
            child = layer.getChild(i)
            result.append(child)
    return result

def getParentLayer(layer):
    return layer.getParent()

def getRootLayer(layer):
    if(layer.getParent() != None):
        return getRootLayer(layer.getParent())
    else:
        return layer

def getAllRootLayer():
    result = []
    layers = getAllLayers()
    for l in layers:
        if(getParentLayer(l) == None):
            result.append(l)
    return result


def getAllLayers():
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

def getAllNodeInLayerHierarchy(rootLayer):
    """
    return all node contained in a layer hierarchy
    :param rootLayer: base layer
    :return: list of MaxPlus.INode
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

def getNodesInLayer(lay):
    result = []
    layerRT = lay.layerAsRefTarg
    lyr_nodes_children = rt.refs.dependents(layerRT)
    for n in lyr_nodes_children:
        cOf = rt.superClassOf(n)
        if( cOf != rt.ReferenceTarget and cOf != rt.Matrix3Controller ):
            result.append(n)
    return result



def getSelectedLayer():
    exp = rt.SceneExplorerManager.GetActiveExplorer()
    layer = exp.SelectedItems()
    count = rt.getProperty(layer, "count")
    if count <= 0:
        rt.messageBox("Please select a layer")
        return
    selectedLayerName = layer[0].name
    return MaxPlus.LayerManager.GetLayer(selectedLayerName)

def deleteAllEmptyLayerHierarchies():
    layers = getAllRootLayer()
    for lay in layers:
        rt.layerManager.deleteLayerHierarchy(lay.name)
