import os

import pymxs
import re
from pymxs import runtime as rt
from maxsdk import layer

def getAllObjects():
    return rt.objects

def getSelectedObjects():
    return rt.getCurrentSelection()

def getSceneRootNode():
    rootScene = rt.rootScene
    worldSubAnim = rootScene[rt.Name('world')]
    return worldSubAnim.object

# returns each root of a collection of object
def getAllRoots(objects):
    allRoots = []
    for o in objects:
        root = getRoot(o)
        if(root not in allRoots):
            allRoots.append(root)
    return allRoots    

# returns the root of the object hierarchy.
def getRoot(obj):
    if(obj.parent == rt.undefined):
        return obj
    else:
        return getRoot(obj.parent)

def getChildren(obj):
    return obj.children

# returns all the descending hierarchy. Call getRoot() before to get the full hierarchy
def getDescendants(obj):    
    hierarchy = []
    hierarchy.append(obj)
    for m in obj.children:
        hierarchy += getDescendants(m)
    return hierarchy

def getDescendantsOfMultiple(objects):
    hierarchies = []
    for o in objects:
        hierarchies += getDescendants(o)
    return hierarchies

def getLODLevel(obj):    
    w = re.match(".+_LOD[0-9]+$", obj.name)
    if(w):
        d = re.findall("[0-9]+$", w.string)
        return int(d[0])
    else:
        return None

def getLODValue(obj):
    try:
        return float(rt.getUserProp(obj,"flightsim_lod_value"))
    except:
        return None
    
defaultLODValues = [70.0, 40.0, 20.0, 10.0]

def getDefaultLODValue(lodLevel):
    defaultCount = len(defaultLODValues)
    if(lodLevel >= defaultCount):
        return defaultLODValues[defaultCount-1]
    if(lodLevel < 0):
        return defaultLODValues[0]
    return defaultLODValues[lodLevel]
    

# Collapse and expand foldout in the hierarchy        
def collapseAllAndExpandSelected():
    explorer = rt.SceneExplorerManager.GetActiveExplorer()
    if explorer is not None :
        explorer.CollapseAll()
        explorer.ExpandSelected()
        rt.macros.run("Scene Explorer","SEFindSelected")
        rt.macros.run("Scene Explorer","SEFindSelected") # we run it twice to make sure it focuses on the hierarchy correctly


def sortObjectsByLODLevels(objects):
    newList = sorted(objects, key=lambda x: getLODLevel(x) , reverse=False)
    return newList

def selectLayers(layers):
    obj = []
    for lay in layers:
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
    gizmos = []
    for o in getDescendantsOfMultiple(roots):
        if rt.classOf(o) in gizmoClasses:
            gizmos.append(o)
    return gizmos 


def convertToBoxCollider(gizmo):
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
    newGizmo = rt.AsoboSphereGizmo()
    newGizmo.parent = gizmo.parent
    newGizmo.transform = gizmo.transform
    newGizmo.sphereGizmo.radius = gizmo.radius
    newGizmo.name = gizmo.name
    gizmo.layer.addnode(newGizmo)
    rt.delete(gizmo)
    return newGizmo

def convertToCylinderCollider(gizmo):
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
    g = gizmo.cylGizmo
    if g.radius <= 0 :
        g.radius *= -1
    if g.height <= 0:
        g.height *= -1    
        rt.toolMode.coordsys(rt.Name("local"))
        rt.rotate(gizmo, (rt.EulerAngles(180, 0, 0)))
    
def cleanupSphereCollider(gizmo):
    if gizmo.sphereGizmo.radius <= 0:
        gizmo.sphereGizmo.radius *= -1

# create conversion table by binding the convert function to a dict key
gizmoConversion = {
    "BoxGizmo" : convertToBoxCollider,
    "SphereGizmo" : convertToSphereCollider,
    "CylGizmo" : convertToCylinderCollider
}

gizmoCleanup = {
    "AsoboBoxGizmo" : cleanupBoxCollider,
    "AsoboSphereGizmo" : cleanupSphereCollider,
    "AsoboCylinderGizmo" : cleanupCylinderCollider
}

# finds cleanup function and runs it.
def cleanupGizmosValues(gizmos):
    for g in gizmos:
        gClass = str(rt.classOf(g))
        if(gClass in gizmoCleanup.keys()):
            gizmoCleanup[str(rt.classOf(g))](g)

# finds conversion function and runs it. 
# Returns new gizmo array
def convertGizmosToAsoboGizmos(gizmos):
    newGizmos = []
    for g in gizmos:
        gClass = str(rt.classOf(g))
        if(gClass in gizmoConversion.keys()):
            g = gizmoConversion[str(rt.classOf(g))](g)

        newGizmos.append(g)
    return newGizmos

######################
####### Filter #######
######################
def filterLODLevel(objects, lodLevel = "[0-9]+"):
    newObjects = []
    for o in objects:
        if(re.match(".+_LOD" + str(lodLevel) + "$",o.name)):
            newObjects.append(o)
    return newObjects

# only returns object USING the property
def filterObjectsWithUserProperty(objects, property):
    newObjects = [o for o in objects if rt.getUserProp(o, property) != None]
    return newObjects

# only returns object NOT USING the property
def filterObjectsWithoutUserProperty(objects, property):
    newObjects = [o for o in objects if rt.getUserProp(o, property) == None]
    return newObjects

# only returns visible objects
def filterObjectsVisible(objects):
    return [o for o in objects if o.isHidden == False]                

# filters out gizmos 
def filterOutGizmos(objects):
    gizmos = []
    for o in objects:
        if str(rt.classOf(o)) not in gizmoClasses:
            gizmos.append(o)
    return gizmos

# only returns gizmos 
def filterGizmos(objects):
    gizmos = []
    for o in objects:
        if str(rt.classOf(o)) in gizmoClasses:
            gizmos.append(o)
    return gizmos

# create a flattened copy of the hierarchy
# Keep the gizmos
# returns root of the newly flattened hierarchy
def flattenMesh(rootNode):
    hierarchy = getDescendants(rootNode)
    objsToFlatten = []
    toKeep = []
    for node in hierarchy:
        cls = rt.classOf(node)
        if cls == rt.Editable_Poly or cls == rt.Editable_Mesh or cls == rt.PolyMeshObject:
            objsToFlatten.append(node)
        else:
            toKeep.append(node)

    flattened = rt.createMesh(objsToFlatten, name=rootNode.name, transform=rootNode.transform)
    for node in toKeep:
        snapNode = rt.snapshot(node)
        snapNode.parent = flattened
        snapNode.name = node.name

    flattened.name = rootNode.name
    return flattened

# recursive function to copy the hierarchy
# create a copy of a hierarchy and returns the root
def copyHierarchy(rootNode):
    current = rt.snapshot(rootNode)
    current.name = rootNode.name
    children = getChildren(rootNode)
    for child in children:
        copyChild = copyHierarchy(child)
        copyChild.parent = current
    return current

getSceneRootNode()




