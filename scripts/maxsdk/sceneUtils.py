"""Module to interact with a 3dsMax scene.
"""

import os
import re

import maxsdk.layer as layer
import pymxs

rt = pymxs.runtime


def getAllObjects():
    """Returns all the object in the scene
    """
    return rt.objects


def getSelectedObjects():
    """Returns all the selected object in the scene
    """
    return rt.getCurrentSelection()


def getSceneRootNode():
    """Returns the unique Root Node of the scene, this is where we can store scene wide user properties. 
    """
    rootScene = rt.rootScene
    worldSubAnim = rootScene[rt.Name('world')]
    return worldSubAnim.object


def getAllRoots(objects):
    """Returns each root of a collection of object
    """
    allRoots = []
    for o in objects:
        root = getRoot(o)
        if(root not in allRoots):
            allRoots.append(root)
    return allRoots
# returns the root of the object hierarchy.


def getRoot(obj):
    """Recursive function to get the root of an object
    """
    if(obj.parent == rt.undefined):
        return obj
    else:
        return getRoot(obj.parent)


def getChildren(obj):
    """Returns all direct children of an object
    """
    return obj.children

def getDescendants(obj):
    """Returns all the descending hierarchy. Call getRoot() before to get the full hierarchy
    """
    hierarchy = []
    hierarchy.append(obj)
    for m in obj.children:
        hierarchy += getDescendants(m)

    return hierarchy


def getDescendantsOfMultiple(objects):
    """Returns all the descending hierarchies of a collection of objects.
    """
    objType = type(objects)
    if objType != pymxs.MXSWrapperObjectSet and objType != list:
        return getDescendants(objects)
        
    hierarchies = []
    for o in objects:
        hierarchies += getDescendants(o)

    result = []
    for h in hierarchies:
        if h not in result:
            result.append(h)
    return result


def getLODLevel(obj):
    """Returns the LOD level of an object as an int, 
    returns None if the object is not a LOD
    """
    w = re.match(".+_LOD[0-9]+$", obj.name)    
    if(w):
        d = re.findall("[0-9]+$", w.string)
        return int(d[0])
    else:
        w = re.match("x[0-9]+_", obj.name)
        if (w):
            d = re.findall("[0-9]+", w.group(0))
            return int(d[0])
        else:
            return None


def getLODValue(obj):
    """Returns the value of the LOD ( minSize ), returns None if the user property is not set
    """
    try:
        return float(rt.getUserProp(obj, "flightsim_lod_value"))
    except:
        return None

def setLODValue(obj, lodValue):
    """Set the lod Value of an object.

    \nin:
          obj= pymxs.MXSWrapperBase
          lodValue= int
    """
    rt.setUserProp(obj, "flightsim_lod_value", lodValue)

defaultLODValues = [70.0, 40.0, 20.0, 10.0] 


def getDefaultLODValue(lodLevel):
    """Given a LOD level as an int, returns the default LOD Value that the object should probably use
    
    \nin:
        lodLevel= int
    
    \out:
        lodValue= float
    """
    defaultCount = len(defaultLODValues)
    if(lodLevel >= defaultCount):
        return defaultLODValues[defaultCount-1]
    if(lodLevel < 0):
        return defaultLODValues[0]
    return defaultLODValues[lodLevel]

def getSharedOptimizeValue(objects):
    """Check every object in the list for the babylon optimize vertice user property we only optimize if all of them do 
    """
    firstState = None
    for obj in objects:
        state = rt.getUserProp(obj, "babylonjs_optimizevertices")
        if state is None:
            state = True
        if firstState is None:
            firstState = state
        if firstState != state:
            return False
    return firstState

def collapseAllAndExpandSelected():
    """Collapse all the Scene Explorer items and expand the selected ones.
    """
    explorer = rt.SceneExplorerManager.GetActiveExplorer()
    if explorer is not None:
        explorer.CollapseAll()
        explorer.ExpandSelected()
        rt.macros.run("Scene Explorer", "SEFindSelected")
        # we run it twice to make sure it focuses on the hierarchy correctly
        rt.macros.run("Scene Explorer", "SEFindSelected")


def sortObjectsByLODLevels(objects):
    """Returns a sorted version of the array in the order LOD0 to LODn
    """
    newList = sorted(objects, key=lambda x: getLODLevel(x), reverse=False)
    return newList


def selectLayers(layers):
    """Select nodes in the layers
    """
    obj = []
    for lay in layers:
        if(rt.classof(lay) == rt.MixinInterface):
            obj += layer.getNodesInLayer(lay)
    rt.select(obj)

######################
####### Gizmo ########
######################
gizmoClasses = [
    "BoxGizmo",
    "SphereGizmo",
    "CylGizmo",
    "LodSphere",
    "SphereFade",
    "CylinderCollider",
    "SphereCollider",
    "BoxCollider",
    "AsoboCylinderGizmo",
    "AsoboBoxGizmo",
    "AsoboSphereGizmo"
]


def getGizmosInDescendants(roots):
    """Returns all the legal gizmos in the hierachies of all the given roots.

    Legal gizmos are declared by class name in the gizmoClasses list
    """
    gizmos = []
    for o in getDescendantsOfMultiple(roots):
        if (str(rt.classOf(o)) in gizmoClasses):
            gizmos.append(o)
    return gizmos


def convertToBoxCollider(gizmo):
    """Convert a box gizmo to a AsoboBoxGizmo
    """
    newGizmo = rt.AsoboBoxGizmo()
    newGizmo.parent = gizmo.parent
    newGizmo.transform = gizmo.transform
    newGizmo.boxGizmo.width = gizmo.width
    newGizmo.boxGizmo.height = gizmo.height
    newGizmo.boxGizmo.length = gizmo.length
    newGizmo.name = gizmo.name
    gizmo.layer.addnode(newGizmo)
    rt.delete(gizmo)
    return newGizmo


def convertToSphereCollider(gizmo):
    """Convert a sphere gizmo to a AsoboSphereGizmo
    """
    newGizmo = rt.AsoboSphereGizmo()
    newGizmo.parent = gizmo.parent
    newGizmo.transform = gizmo.transform
    newGizmo.sphereGizmo.radius = gizmo.radius
    newGizmo.name = gizmo.name
    gizmo.layer.addnode(newGizmo)
    rt.delete(gizmo)
    return newGizmo


def convertToCylinderCollider(gizmo):
    """Convert a cylinder gizmo to a AsoboCylinderGizmo
    """
    newGizmo = rt.AsoboCylinderGizmo()
    newGizmo.parent = gizmo.parent
    newGizmo.transform = gizmo.transform
    newGizmo.cylGizmo.radius = gizmo.radius
    newGizmo.cylGizmo.height = gizmo.height
    newGizmo.name = gizmo.name
    gizmo.layer.addnode(newGizmo)
    rt.delete(gizmo)
    return newGizmo


def cleanupBoxCollider(gizmo):
    """Remove negative sizes of a box gizmo
    """
    g = gizmo.boxGizmo
    if(g.width <= 0):
        g.width *= -1
    if(g.length <= 0):
        g.length *= -1
    if(g.height <= 0):
        g.height *= -1
        rt.toolMode.coordsys(rt.Name("local"))
        rt.rotate(gizmo, (rt.EulerAngles(180, 0, 0)))


def cleanupCylinderCollider(gizmo):
    """Remove negative sizes of a Cylinder Gizmos
    """
    g = gizmo.cylGizmo
    if g.radius <= 0:
        g.radius *= -1
    if g.height <= 0:
        g.height *= -1
        rt.toolMode.coordsys(rt.Name("local"))
        rt.rotate(gizmo, (rt.EulerAngles(180, 0, 0)))


def cleanupSphereCollider(gizmo):
    """Make sure the radius of a sphere gizmo is positive
    """
    if gizmo.sphereGizmo.radius <= 0:
        gizmo.sphereGizmo.radius *= -1


# create conversion table by binding the convert function to a dict key
gizmoConversion = {
    "BoxGizmo": convertToBoxCollider,
    "SphereGizmo": convertToSphereCollider,
    "CylGizmo": convertToCylinderCollider
}
gizmoCleanup = {
    "AsoboBoxGizmo": cleanupBoxCollider,
    "AsoboSphereGizmo": cleanupSphereCollider,
    "AsoboCylinderGizmo": cleanupCylinderCollider
}
# finds cleanup function and runs it.


def cleanupGizmosValues(gizmos):
    """Wrapper to cleanup a group of gizmos based on the gizmoCleanup dictionary defined in sceneUtils
    """
    for g in gizmos:
        gClass = str(rt.classOf(g))
        if(gClass in gizmoCleanup.keys()):
            gizmoCleanup[str(rt.classOf(g))](g)
# finds conversion function and runs it.
# Returns new gizmo array


def convertGizmosToAsoboGizmos(gizmos):
    """Wrapper to convert a group of gizmos to their Asobo equivalent based on the gizmoConversion dictionary defined in sceneUtils
    returns a list with the new gizmos converted or not.
    """
    newGizmos = []
    for g in gizmos:
        gRoot = getRoot(g)
        gClass = str(rt.classOf(g))
        if gRoot is g:
            raise Exception('\nERROR : {0} used as top parent'.format(gClass))
        if(gClass in gizmoConversion.keys()):
            g = gizmoConversion[str(rt.classOf(g))](g)
        newGizmos.append(g)
    return newGizmos

######################
####### Filter #######
######################


def filterLODLevel(objects, lodLevel="[0-9]+"):
    """Only returns objects of the given lodLevel, lodLevel can either be an integer or a regular expression
    """
    newObjects = []
    for o in objects:
        if(re.match(".+_LOD" + str(lodLevel) + "$", o.name)):
            newObjects.append(o)    
        elif (re.match("x" + str(lodLevel) + "_", o.name)):
            newObjects.append(o)
    return newObjects


def filterObjectsWithUserProperty(objects, property):
    """Only returns object USING the property
    """
    newObjects = [o for o in objects if rt.getUserProp(o, property) != None]
    return newObjects
# only returns object NOT USING the property


def filterObjectsWithoutUserProperty(objects, property):
    """Only returns object NOT USING the property
    """
    newObjects = [o for o in objects if rt.getUserProp(o, property) == None]
    return newObjects
# only returns visible objects


def filterObjectsVisible(objects):
    """Only returns visible objects
    """
    return [o for o in objects if o.isHidden == False]
# filters out gizmos


def filterOutGizmos(objects):
    """Only returns non gizmo object
    """
    gizmos = []
    for o in objects:
        if str(rt.classOf(o)) not in gizmoClasses:
            gizmos.append(o)
    return gizmos
# only returns gizmos


def filterGizmos(objects):
    """Only returns the gizmos
    """
    gizmos = []
    for o in objects:
        if str(rt.classOf(o)) in gizmoClasses:
            gizmos.append(o)
    return gizmos
# create a flattened copy of the hierarchy
# Keep the gizmos
# returns root of the newly flattened hierarchy


def conformSceneLayersToTemplate(template):
    """Conform your scene layers and their children nodes to a template dictionary. 
    Keys : baseName 
    Values : list of root node
    A parent layer is created for each baseName
    A child layer is created for each rootNode in the corresponding baseName layer
    The hierarchy of the rootNode is then stored in its layer

    \nin:
    template = dict(key=str, value=list(node))
    """
    layerManager = rt.layerManager
    defaultLayer = layerManager.getLayer(0)
    allObjects = getAllObjects()
    for x in allObjects:
        defaultLayer.addNode(x)
    for baseName in template.keys():
        currentCategory = layerManager.getLayerFromName(baseName)
        if(currentCategory is None):
            currentCategory = layerManager.newLayerFromName(baseName)
        for o in template[baseName]:
            currentLayer = layerManager.getLayerFromName(o.name)
            if(currentLayer is None):
                currentLayer = layerManager.newLayerFromName(o.name)
            hierarchy = getDescendants(o)
            for oo in hierarchy:
                currentLayer.addNode(oo)
            currentLayer.setParent(currentCategory)
    layer.deleteAllEmptyLayerHierarchies()

def flattenMesh(rootNode):
    """Returns a flattened version of the descendants of the given object, keeping gizmos intact
    """
    hierarchy = getDescendants(rootNode)
    objsToFlatten = []
    toKeep = []
    for node in hierarchy:
        cls = rt.classOf(node)
        if cls == rt.Editable_Poly or cls == rt.Editable_Mesh or cls == rt.PolyMeshObject:
            objsToFlatten.append(node)
        else:
            toKeep.append(node)
    flattened = rt.createMesh(
        objsToFlatten, name=rootNode.name, transform=rootNode.transform)
    for node in toKeep:
        snapNode = rt.snapshot(node)
        snapNode.parent = flattened
        snapNode.name = node.name
    flattened.name = rootNode.name
    del objsToFlatten
    del toKeep
    return flattened
# recursive function to copy the hierarchy
# create a copy of a hierarchy and returns the root


def copyHierarchy(rootNode):
    """Recursive function that copy a hierarchy and returns you a reference to the root of the copy
    """
    current = rt.snapshot(rootNode)
    current.name = rootNode.name
    children = getChildren(rootNode)
    for child in children:
        copyChild = copyHierarchy(child)
        copyChild.parent = current
    return current
