from maxsdk.globals import *
if MAXVERSION() < MAX2017:
    import MaxPlus

from pymxs import runtime as rt

import itertools
import os
import maxsdk.userprop



def getAllNodes():
    return MaxPlus.Core.GetRootNode()if (MAXVERSION() < MAX2017) else getChildren(rt.rootNode)


def getFacesCount(nodes):
    total_faces = 0
    for n in nodes:
        total_faces += n.GetFaceCount()
    return total_faces

def get_node_by_name(name):
    if MAXVERSION() < MAX2017:
        return MaxPlus.INode.GetINodeByName(name)
    else:
        return rt.getNodeByName(name)


def getTrisCountMP(nodes):
    total_faces = 0
    for n in nodes:
        s = rt.getNodeByName(n.GetName())
        if s:
            c = rt.GetTriMeshFaceCount(s)[0]
            total_faces += c
    return total_faces

def getTrisCount(nodes):
    total_faces = 0
    for n in nodes:
        s = rt.getNodeByName(n.name)
        if s:
            c = rt.GetTriMeshFaceCount(s)[0]
            total_faces += c
    return total_faces


def removeAllModifiers(node):
    """Remove each modifier without applying them
    """
    if node.Modifiers:
        for m in list(node.Modifiers):
            if m:
                MaxPlus.ModifierPanel.Delete(node, m) if (MAXVERSION() < MAX2017) else rt.deletemodifier(node, m)


def collapseAllModifiers(node):
    """Collapses modifier stack.
    """
    rtNode = rt.getNodeByName(node.GetName())
    rt.collapseStack(rtNode)


def getChildren(node):
    """Recursive generator to get the descendants of a node
    """
    for c in node.Children:
        yield c
        for d in getChildren(c):
            yield d


def mirrorNode(node, mirrorAxis):
    original_parent = node.GetParent()
    if MAXVERSION() < MAX2017:
        temp_mesh = MaxPlus.Factory.CreateGeomObject(MaxPlus.ClassIds.Sphere)
        temp_parent = MaxPlus.Factory.CreateNode(temp_mesh)
    else:
        temp_parent = rt.sphere()

    node.SetParent(temp_parent)

    rtNode = rt.getNodeByName(temp_parent.GetName())
    p = rt.Point3(1, 1, 1)
    if mirrorAxis == "X":
        p = rt.Point3(-1, 1, 1)
    elif mirrorAxis == "Y":
        p = rt.Point3(1, -1, 1)
    elif mirrorAxis == "Z":
        p = rt.Point3(1, 1, -1)
    else:
        print("Error axis do not match")
    rt.scale(rtNode, p)

    node.SetParent(original_parent)
    MaxPlus.INode.Delete(temp_parent) if MAXVERSION() < MAX2017 else rt.delete(temp_parent)


def runMacroOnChildren(node, macro):
    for c in node.Children:
        macro(c)
        yield c
        for d in getChildren(c):
            macro(d)
            yield d


def compareOnHierachy(tree_root_A, tree_root_B, condition):
    for a, b in itertools.izip(tree_root_A.Children, tree_root_B.Children):
        if not condition(a, b):
            yield False
            break
        yield a, b
        for c, d in itertools.izip(getChildren(a), getChildren(b)):
            if not condition(c, d):
                yield False
                break
            yield c, d


def cloneHierarchy(root, parent, func, lambda_list):
    rt_old_node = rt.getNodeByName(root.GetName())
    rt_new_node = rt.copy(rt_old_node)
    # avoid copy with default 001 prefix
    rt_new_node.name = rt_old_node.name + "_temp"
    new_node = get_node_by_name(rt_new_node.name)
    func(new_node)
    new_node.SetParent(parent)
    for l in lambda_list:
        if l is not None:
            l(new_node)

    num_children = root.GetNumChildren()
    for i in range(0, num_children):
        child = root.GetChild(i)
        cloneHierarchy(child, new_node, func, lambda_list)


def getBaseNodes(nodeList):
    result = list()
    for node in nodeList:
        if node.GetParent() == (MaxPlus.Core.GetRootNode() if MAXVERSION() < MAX2017 else rt.rootNode):
            result.append(node)
    return result

def get_selected_nodes():
    if MAXVERSION() < MAX2017:
        return MaxPlus.SelectionManager.GetNodes()
    else:
        return rt.selection
        
def get_all_containers():
    objs = rt.objects
    cont = []
    for o in objs:
        if rt.classof(o) == rt.container:
            cont.append(o)
    return cont

def load_all_containers():
    cont = get_all_containers()
    for c in cont:
        c.LoadContainer()

def get_nodes_by_material(mat):
    nodes = getAllNodes()
    foundNodes = []
    for n in nodes:
        if n.material == mat:
            foundNodes.append(n)
    return foundNodes

class MatchnodeNunID():
    UniqueID = None
    Nodes = []
    def __init__(self, _uniqueID, _Nodes):
        self.UniqueID = _uniqueID
        self.Nodes = _Nodes


def is_double_unique_ID(nodes):
    UniqueIds = []
    result = False
    MatchnodeNunIDList = []
    for n in nodes:
        UnID = userprop.getUserProp(n, "flightsim_uniqueID")
        for n2 in nodes:
            UnID2 = userprop.getUserProp(n2, "flightsim_uniqueID")
            if UnID == UnID2 and n != n2:
                if UnID != None:
                    #print("FoundMatch on nodes ({0}/{1}) with Unique ID ({2})".format(n,n2,UnID))
                    a, pos = is_uniqueIDExist(MatchnodeNunIDList, UnID)
                    if a:
                        if not is_NodesExists(MatchnodeNunIDList, n.name):
                            MatchnodeNunIDList[pos].Nodes.append(n.name)
                        if not is_NodesExists(MatchnodeNunIDList, n2.name):
                            MatchnodeNunIDList[pos].Nodes.append(n2.name)
                    else:
                        temNodeList = []
                        temNodeList.append(n.name)
                        temNodeList.append(n2.name)
                        MatchnodeNunIDList.append(MatchnodeNunID(UnID,temNodeList))                    
                    result = True
    return result, MatchnodeNunIDList

def is_uniqueIDExist(_MatchnodeNunIDList, _cUID):
    for i in range(len(_MatchnodeNunIDList)):
        if _MatchnodeNunIDList[i].UniqueID == _cUID:
            return True, i
    return False, 0

def is_NodesExists(_MatchnodeNunIDList, _cNode):
    for MIL in _MatchnodeNunIDList:
        for n in MIL.Nodes:
            if n == _cNode:
                return True
    return False


