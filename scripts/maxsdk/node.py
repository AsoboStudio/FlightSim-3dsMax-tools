import MaxPlus
import pymxs
import itertools
import os
rt = pymxs.runtime


def getAllNodes():
    return getChildren(MaxPlus.Core.GetRootNode())


def getFacesCount(nodes):
    total_faces = 0
    for n in nodes:
        total_faces += n.GetFaceCount()
    return total_faces


def getTrisCount(nodes):
    total_faces = 0
    for n in nodes:
        s = rt.getNodeByName(n.GetName())
        if s:
            c = rt.GetTriMeshFaceCount(s)[0]
            total_faces += c
    return total_faces


def removeAllModifiers(node):
    if node.Modifiers:
        for m in list(node.Modifiers):
            if m:
                MaxPlus.ModifierPanel.Delete(node, m)


def collapseAllModifiers(node):
    rtNode = rt.getNodeByName(node.GetName())
    rt.collapseStack(rtNode)


def getChildren(node):
    for c in node.Children:
        yield c
        for d in getChildren(c):
            yield d


def mirrorNode(node, mirrorAxis):
    original_parent = node.GetParent()
    temp_mesh = MaxPlus.Factory.CreateGeomObject(MaxPlus.ClassIds.Sphere)
    temp_parent = MaxPlus.Factory.CreateNode(temp_mesh)
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
        print "Error axis do not match"
    rt.scale(rtNode, p)

    node.SetParent(original_parent)
    MaxPlus.INode.Delete(temp_parent)


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
    new_node = MaxPlus.INode.GetINodeByName(rt_new_node.name)
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
        if node.GetParent() == MaxPlus.Core.GetRootNode():
            result.append(node)
    return result

