"""
Generic Python MaxPlus library
"""
import os
import re

import MaxPlus as MaxPlus
import pymxs
from pymxs import runtime as rt


def get_selection():
    return MaxPlus.SelectionManager.GetNodes()

def evaluate_max_script_file(_filePath):
    f = open(_filePath, "r")
    s = f.read()
    x = MaxPlus.Core.EvalMAXScript(s)
    

def get_parent_layer(layer_name):
    l = rt.LayerManager.getLayerFromName(layer_name)
    p = l.getParent()
    if p is None:
        print "Layer {0} is a root".format(layer_name)
    else:
        return MaxPlus.LayerManager.GetLayer(p.name)


def set_parent_layer(mp_layer_source, mp_layer_target):
    src_lyr_name = mp_layer_source.GetName()
    trgt_lyr_name = mp_layer_target.GetName()
    lyr_src = rt.LayerManager.getLayerFromName(src_lyr_name)
    trgt_lyr = rt.LayerManager.getLayerFromName(trgt_lyr_name)
    lyr_src.setParent(trgt_lyr)


def getAllNodes():
    return GetChildren(MaxPlus.Core.GetRootNode())


def GetChildren(node):
    for c in node.Children:
        yield c
        for d in GetChildren(c):
            yield d


def GetObjectByName(name):
    nodeList = getAllNodes()
    for n in nodeList:
        if (n.Name == name):
            return n
    return None


def GetObjectWithName(name):
    """
    Return the first object in hierarchy that contains the given name
    :param name: name of the object to search
    :return: INode
    """
    nodeList = getAllNodes()
    for n in nodeList:
        if name in n.Name:
            return n
    return None


def IsLeaf(node):
    if node.GetNumChildren() == 0:
        return True
    else:
        return False


def DeleteHierarchy(node):
    children = GetChildren(node)
    tab = MaxPlus.INodeTab()
    for i in children:
        tab.Append(i)
    MaxPlus.INode.DeleteNodes(tab)
    node.Delete()


def CopyAnimationControl(originalNode, dummyNode):
    """
    Copy Transform Controller from source to target
    :param originalNode: Source INode
    :param dummyNode: Target INode
    :return:
    """
    originalTransformControl = GetTransformControl(originalNode)
    dummyTransformControl = GetTransformControl(dummyNode)
    dummyTransformControl.Copy(originalTransformControl)

def createDummyHierachy(source, parent):
    p = create_dummy(source, parent)
    for c in source.Children:
        createDummyHierachy(c, p)
    return p

def create_dummy(node,parent):


    rtNode = rt.getNodeByHandle(node.Handle)
    MaxPlus.Core.EvalMAXScript("myType = #instance")
    rt.maxOps.cloneNodes(rtNode, cloneType=rt.myType)
    dummyNode = MaxPlus.INode.GetINodeByHandle(rt.handle)

    dummyNode.Name = node.Name + "_dummy"
    dummyNode.SetParent(parent)

    CopyAnimationControl(node, dummyNode)
    return dummyNode

def CreateDummyHierarchy(root, dummyParent, prefix):
    if root is None:
        nodes = MaxPlus.Core.GetRootNode().Children
        dummyParent = MaxPlus.Core.GetRootNode()
    else:
        numChildren = root.GetNumChildren()
        nodes = []
        if dummyParent == MaxPlus.Core.GetRootNode():
            nodes.append(root)

        for i in range(0, numChildren):
            child = root.GetChild(i)
            if (prefix in child.Name):
                nodes.append(child)
    for n in nodes:
        dummy = MaxPlus.Factory.CreateGeomObject(MaxPlus.ClassIds.Sphere)
        dummy.ParameterBlock.Radius.Value = 0.05
        dummyNode = MaxPlus.Factory.CreateNode(dummy)
        dummyNode.Position = n.Position
        dummyNode.Rotation = n.Rotation

        dummyNode.Name = n.Name + "_dummy"
        dummyNode.SetParent(dummyParent)

        CopyAnimationControl(n, dummyNode)
        CreateDummyHierarchy(n, dummyNode, prefix)


def replace_node_prefix(n, prefix, new_prefix):
    name = str(n.GetName())
    name = name[:-5]
    name = name.replace(prefix, new_prefix)
    # existent_node = MaxPlus.INode.GetINodeByName(name)
    # if existent_node is not None:
    #     print "{0} already exist,previous one ha been removed".format(name)
    #     #MaxPlus.INode.Delete(existent_node)
    n.Name = name


def replace_layer_prefix(l, prefix, new_prefix):
    name = l.name
    name = name.replace(prefix, new_prefix)
    name = name[:-5]
    ex = rt.LayerManager.getLayerFromName(name)
    if ex is not None:
        rt.LayerManager.deleteLayerHierarchy(name, forceDelete = True)
    l.setname(name)



def clone_hierarchy(root, parent, func, lambda_list):
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
        clone_hierarchy(child, new_node, func, lambda_list)


def GetTransformControl(node):
    for i in range(node.GetNumSubAnims()):
        subAnim = node.GetSubAnim(i)
        if str(subAnim) == "Animatable(Position/Rotation/Scale)":
            genericController = MaxPlus.Control__CastFrom(subAnim)
            return genericController


def ResetXForm(root, includeChild, scaleOnly):
    if (includeChild == False):
        root.ResetTransform(0, scaleOnly)
    else:
        root.ResetTransform(0, scaleOnly)
        numChildren = root.GetNumChildren()
        nodes = []
        for i in range(0, numChildren):
            nodes.append(root.GetChild(i))
        for n in nodes:
            ResetXForm(n, includeChild, scaleOnly)


def Mirror(node, mirrorAxis):
    scale = None
    if mirrorAxis == "X":
        scale = MaxPlus.Point3(-1, 1, 1)
    elif mirrorAxis == "Y":
        scale = MaxPlus.Point3(1, -1, 1)
    elif mirrorAxis == "Z":
        scale = MaxPlus.Point3(1, 1, -1)
    else:
        print "Error axis do not match"
    node.Scaling = scale


def AddPositionListAndConstraint(node):
    """this method store the original PositionXYZ controller
    and add it into the new listControl
    to be safe this should be done for every child control"""
    positionList = MaxPlus.Factory.CreatePositionController(MaxPlus.ClassIds.position_list)
    positionConstraint = MaxPlus.Factory.CreatePositionController(MaxPlus.ClassIds.Position_Constraint)
    transformControl = GetTransformControl(node)
    positionXYZ = transformControl.GetPositionController()
    positionList.AssignController(positionXYZ, 0)
    positionList.AssignController(positionConstraint, 1)
    transformControl.AssignController(positionList, 0)
    return positionConstraint


def AddRotationListAndConstraint(node):
    """this method stopre the original PositionXYZ controller
    and add it into the new listControl
    to be safe this should be done for every child control"""
    rotationList = MaxPlus.Factory.CreateRotationController(MaxPlus.ClassIds.rotation_list)
    rotationConstraint = MaxPlus.Factory.CreateRotationController(MaxPlus.ClassIds.Orientation_Constraint)
    transformControl = GetTransformControl(node)
    rotationXYZ = transformControl.GetRotationController()
    rotationList.AssignController(rotationXYZ, 0)
    rotationList.AssignController(rotationConstraint, 1)
    transformControl.AssignController(rotationList, 1)
    return rotationConstraint


def FindAnimatedObject(node):
    children = list(GetChildren(node))
    children.append(node)
    animated = []
    for c in children:
        # print c
        if c.IsAnimated():
            animated.append(c)
    return animated


def FindObjectByPrefix(node, prefix):
    children = GetChildren(node)
    resultList = []
    for c in children:
        if prefix in c.Name:
            resultList.append(c)
    return resultList


def findObjectBySuffix(suffix, nodeList):
    result_list = []
    for c in nodeList:
        if suffix in c.Name:
            result_list.append(c)
    return result_list

def removeLODSuffix(name):
    w = re.findall("_LOD[0-9]+$", name) # find the lod part
    if(w):
        name = name.replace(w[0],"") # and remove it
    return name

def CreateSphereAt(radius, pos, name):
    # pos is Point3
    sphere = MaxPlus.Factory.CreateGeomObject(MaxPlus.ClassIds.Sphere)
    sphere.ParameterBlock.Radius.Value = radius
    node = MaxPlus.Factory.CreateNode(sphere, name)
    pt = pos
    node.Move(pt)
    return MaxPlus.INode(sphere)


def printList(a):
    for i in a:
        print i


def RemoveScaleKeys(node):
    transform_controller = GetTransformControl(node)
    c = transform_controller.GetScaleController()
    c.DeleteKeys(MaxPlus.Constants.TrackDoall)


def remove_position_keys(node):
    transform_controller = GetTransformControl(node)
    c = transform_controller.GetPositionController()
    c.DeleteKeys(MaxPlus.Constants.TrackDoall)


def remove_rotation_keys(node):
    transform_controller = GetTransformControl(node)
    c = transform_controller.GetRotationController()
    c.DeleteKeys(MaxPlus.Constants.TrackDoall)


def remove_transform_keys(node):
    remove_position_keys(node)
    remove_rotation_keys(node)
    RemoveScaleKeys(node)


def get_layer_children(root, result):
    """
    return given layer and their children
    :param root: root layer
    :param result: result layer list
    :return: layer list
    """
    # print root.name
    num_children = root.getNumChildren()
    if num_children == 0:
        result.append(root)
    else:
        for i in range(1, num_children + 1):
            child = root.getChild(i)
            # print "step" + str(i) + " " + child.name
            get_layer_children(child, result)
    return result


def get_layer_by_prefix(prefix):
    """
    return first layer with the given prefix in name
    :param prefix: prefix to search
    :return: MaxPlus.Layer
    """
    num_layers = MaxPlus.LayerManager.GetNumLayers()
    for i in range(num_layers):
        lyr = MaxPlus.LayerManager.GetLayer(i)
        name = lyr.GetName()
        if prefix in name:
            return lyr


def get_layer_by_name(name):
    """
    return layer ,looking for the passed name
    :param name: searched name
    :return: MaxPlus.Layer
    """
    n = MaxPlus.LayerManager.GetLayer(name)
    return n



def get_unparent_nodes_in_layer_hierarchy(root_layer):
    """
    return all node directly child of the World , contained in a layer hierarchy
    :param root_layer: base layer
    :return: list of MaxPlus.INode
    """
    result_list = []
    lyr_list = [root_layer]
    lyr_list = get_layer_children(root_layer, lyr_list)

    for l in lyr_list:
        print l.name
        mp_layer = MaxPlus.LayerManager.GetLayer(l.name)
        lyr_nodes_children = mp_layer.GetNodes()
        for n in lyr_nodes_children:
            #print n.GetName()
            if n.GetParent() == MaxPlus.Core.GetRootNode():
                result_list.append(n)
    return result_list


def copy_transform_from_controller(controller, source_name, target_name):
    num_keys = controller.GetNumKeys()
    # print num_keys
    MaxPlus.Animation.SetAnimateButtonState(True)
    for i in range(num_keys):
        key_time = controller.GetKeyTime(i)
        # print "key " + str(i) + " is at: " + str(key_time / 160)

        # print "move to the selected time"
        MaxPlus.Animation.SetTime(key_time, False)
        # print "copy transform"
        rt_source = rt.getNodeByName(source_name)
        rt_target = rt.getNodeByName(target_name)
        t = rt_source.getmxsprop("transform")
        rt_target.setmxsprop("transform", t)
    MaxPlus.Animation.SetAnimateButtonState(False)


def get_key_times(controller):
    num_keys = controller.GetNumKeys()
    result = []
    for i in range(num_keys):
        result.append(controller.GetKeyTime(i))
    return result


def remove_unused_key(source, target):
    """
    tcb controller make some strange stuff adding unused key,
    this method remove the key if it has been added on all controllers,pos rot,scale and you want to clean up
    """
    src_transform = GetTransformControl(source)
    src_pos_controller = src_transform.GetPositionController()
    src_rot_controller = src_transform.GetRotationController()
    src_scale_controller = src_transform.GetScaleController()
    src_controller_list = [src_pos_controller, src_rot_controller, src_scale_controller]

    target_transform = GetTransformControl(target)
    target_pos_controller = target_transform.GetPositionController()
    target_rot_controller = target_transform.GetRotationController()
    target_scale_controller = target_transform.GetScaleController()
    target_controller_list = [target_pos_controller, target_rot_controller, target_scale_controller]


    for i in range(len(src_controller_list)):
    # for i in range(1):
        # print "controller" + str(i)
        src_keys = get_key_times(src_controller_list[i])
        # print "src keys"
        # printList(src_keys)
        target_keys = get_key_times(target_controller_list[i])
        match_key = list()
        for k_source in src_keys:
            # print "examin key: " + str(k_source)
            for k_target in target_keys:
                r = range(k_source -80, k_source +80)
                if k_target in r:
                    match_key.append(k_target)
                # else:
                    # print str(k_target) + "do not  match"
        # print "match keys"
        # printList(match_key)
        remove_keys = list(set(target_keys) - set(match_key))
        for j in remove_keys:
            # print "key:" + str(j)
            target_controller_list[i].DeleteKeyAtTime(j)

def clone_layer_hierarchy(root, parent, func):
    new_lyr = rt.LayerManager.newLayer()
    new_lyr.setName(root.name + "_temp")
    func(new_lyr) #rename layer
    if parent is not None:
        new_lyr.setParent(parent)

    num_children = root.getNumChildren()
    for i in range(1, num_children + 1):
        child = root.getChild(i)
        clone_layer_hierarchy(child, new_lyr, func)

def convert_to_editable_mesh(node):
    node.Convert(MaxPlus.ClassIds.TriMeshGeometry)
    obj = node.GetBaseObject()
    return obj

def convert_to_editable_poly(node):
    node.Convert(MaxPlus.ClassIds.PolyMeshObject)
    obj = node.GetBaseObject()
    return obj

def get_asobo_folder():
    home = os.path.expanduser("~")
    asobo = os.path.join(home, ".asobo")
    if not os.path.exists(asobo):
        os.makedirs(asobo)
    return asobo

def attachToMax(widget):
    MaxPlus.AttachQWidgetToMax(widget)
