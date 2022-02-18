import MaxPlus
import maxsdk.utility as sdkutility

import maxsdk.node as sdknode

import maxsdk.skin as sdkskin

import maxsdk.animation as sdkanim

import re
import os
import pymxs

rt = pymxs.runtime


def DeletePositionKey(obj, time):
    objsel = "$" + obj.Name
    command = "selectKeys {0}.position.controller {1}".format(objsel, time)
    MaxPlus.Core.EvalMAXScript(command)
    command = "deleteKeys {0}.position.controller #selection".format(obj)
    MaxPlus.Core.EvalMAXScript(command)


def SetPositionConstraintTarget(source, target):
    sourceMS = """(getNodeByName "{0}")""".format(source.Name)
    targetMS = """(getNodeByName "{0}")""".format(target.Name)
    command = targetMS + ".position.controller.Position_Constraint.appendtarget " + sourceMS + " 100"
    MaxPlus.Core.EvalMAXScript(command)


def SetOrientationConstraintTarget(source, target):
    sourceMS = """(getNodeByName "{0}")""".format(source.Name)
    targetMS = """(getNodeByName "{0}")""".format(target.Name)
    command = targetMS + ".rotation.controller.Orientation_Constraint.appendtarget " + sourceMS + " 100"
    MaxPlus.Core.EvalMAXScript(command)
    # command = targetMS + ".rotation.controller.Orientation_Constraint.controller.relative = on"
    # MaxPlus.Core.EvalMAXScript(command)


def findBakeSource(bakeTarget, bakeSources, suffix, dummySuffix):
    for n in bakeSources:
        objCoreName = bakeTarget.Name.replace(suffix, "")
        dummyCoreName = n.Name.replace("_dummy", "")
        dummyCoreName = dummyCoreName.replace(dummySuffix, "")
        if (objCoreName == dummyCoreName):
            return n


def findObjectAndBake(target, dummyroot, suffix, oppositeSuffix, copyDirection):
    bakeSources = list(sdknode.getChildren(dummyroot))
    targetChildrens = list(sdknode.getChildren(target))
    targetChildrens.append(target)
    bakeTargets = sdkutility.findObjectBySuffix(oppositeSuffix, targetChildrens)

    for bakeTarget in bakeTargets:
        bakeSource = findBakeSource(bakeTarget, bakeSources, oppositeSuffix, suffix)
        if bakeSource is not None:
            sdkutility.RemoveScaleKeys(bakeTarget)
            sdkutility.AddPositionListAndConstraint(bakeTarget)
            SetPositionConstraintTarget(bakeSource, bakeTarget)
            sdkutility.AddRotationListAndConstraint(bakeTarget)
            SetOrientationConstraintTarget(bakeSource, bakeTarget)

    selectionTab = MaxPlus.INodeTab()
    for n in bakeTargets:
        selectionTab.Append(n)
    MaxPlus.SelectionManager.SelectNodes(selectionTab)
    plotFile = os.path.join(os.path.dirname(os.path.abspath(__file__)), "plot.ms")
    plot = open(plotFile, "r")
    MaxPlus.Core.EvalMAXScript(plot.read())


def mirror_animation(source, target, src_suffix, target_suffix, copyDirection):
    # mirror from parent of selection
    # todo: if no parent add a node on center
    dummyRoot = MaxPlus.INode.CreateTreeInstance(source)
    dummyHierarchy = list(sdknode.getChildren(dummyRoot))
    dummyHierarchy.append(dummyRoot)
    for n in dummyHierarchy:
        n.SetName(n.GetName()[:-3] + "_dummy")
        setDummy(n)
    MaxPlus.SelectionManager.SelectNode(dummyRoot)
    MaxPlus.Core_EvalMAXScript("tm = $.transform\ntm.row1 = tm.row1 * [-1,1,1]\n$.transform  =tm")
    try:
        findObjectAndBake(target, dummyRoot, src_suffix, target_suffix, copyDirection)
    finally:
        cleanUp(src_suffix, target_suffix, copyDirection)


def remove_unused_key(target_anim_root, source_suffix, target_suffix):
    # children_list = [target_anim_root]
    # children_list += list(sdkutility.GetChildren(target_anim_root))
    # for target_node in children_list:
    # find the binomial node and copy
    source_node = find_binomial(target_anim_root, source_suffix, target_suffix)
    if source_node:
        sdkutility.remove_unused_key(source_node, target_anim_root)


def find_binomial(node, src_suffix, target_suffix):
    src_name = node.GetName()
    binomial_name = re.sub(r'{0}$'.format(src_suffix), target_suffix, src_name)
    if src_name != binomial_name:
        return MaxPlus.INode.GetINodeByName(binomial_name)
    else:
        return None


def mirror_skin(src, target, src_suffix, target_suffix, mirror_axis):
    MaxPlus.Animation.SetTime(0, False)
    sdknode.collapseAllModifiers(target)
    target_skinmodifier = sdkskin.add_skin_modifier(target)
    MaxPlus.SelectionManager.SelectNode(target)
    MaxPlus.Core.EvalMAXScript("max modify mode")
    src_skinmodifier = sdkskin.get_skin_modifier(src)
    boneslist = sdkskin.get_bones_list_from_skin_modifier(src_skinmodifier)
    MaxPlus.SelectionManager.SelectNode(target)
    if boneslist:
        for bone in boneslist:
            binomial_bone = find_binomial(bone, src_suffix, target_suffix)
            if binomial_bone:
                sdkskin.add_bone_to_skin_modifier_of_selected_node(binomial_bone)
            else:
                sdkskin.add_bone_to_skin_modifier_of_selected_node(bone)
    else:
        return

    MaxPlus.SelectionManager.SelectNode(src)
    MaxPlus.Core_EvalMAXScript("skinUtils.ExtractSkinData $")
    skin_data = MaxPlus.INode.GetINodeByName("SkinData_" + src.GetName())
    sdknode.mirrorNode(skin_data, mirror_axis)
    target_bone_list = sdkskin.get_bones_list_from_skin_modifier(target_skinmodifier)
    for target_bone in target_bone_list:
        name = target_bone.GetName()
        new_name = re.sub(r'{0}$'.format(target_suffix), src_suffix, name)
        target_bone.SetName(new_name)
    MaxPlus.SelectionManager.ClearNodeSelection()
    selection = MaxPlus.INodeTab()
    selection.Append(target)
    selection.Append(skin_data)
    MaxPlus.SelectionManager.SelectNodes(selection)
    MaxPlus.Core.EvalMAXScript("skinUtils.ImportSkinDataNoDialog true false false false false 1 0")
    target_bone_list = sdkskin.get_bones_list_from_skin_modifier(target_skinmodifier)
    for target_bone in target_bone_list:
        name = target_bone.GetName()
        new_name = re.sub(r'{0}$'.format(src_suffix), target_suffix, name)
        target_bone.SetName(new_name)
    MaxPlus.SelectionManager.ClearNodeSelection()
    MaxPlus.INode.Delete(skin_data)


def convertToAnimationHelper(node, parent, includeChildren, keepExistent,deleteKeysOnSource):
    regex = r"^x[0-9]_"
    if node.IsAnimated():
        helperName = node.GetName() + "_helper"
        helperName = re.sub(regex, "", helperName)
        helperNode = MaxPlus.INode.GetINodeByName(helperName)
        sceneNodes = sdknode.getAllNodes()
        if not helperNode:
            helperNode = createHelper(node, parent, helperName)
        else:
            if not keepExistent:
                MaxPlus.INode.Delete(helperNode)
                helperNode = createHelper(node, parent, helperName)
        if deleteKeysOnSource:
            name = re.sub(regex, "", node.GetName())
            for n in sceneNodes:
                if n.GetName().endswith(name):
                    sdkanim.removeTransformKeys(n)

    if includeChildren:
        for c in node.Children:
            convertToAnimationHelper(c, helperNode, includeChildren, keepExistent,deleteKeysOnSource)


def createHelper(node, parent, helperName):
    helper = MaxPlus.Factory.CreateHelperObject(MaxPlus.ClassIds.Point)
    helper.ParameterBlock.DrawOnTop.Value = True
    helper.ParameterBlock.AxisTripod.Value = True
    helper.ParameterBlock.Box.Value = True
    helper.ParameterBlock.Size.Value = 0.020
    helperNode = MaxPlus.Factory.CreateNode(helper)
    helperNode.SetName(helperName)
    helperNode.SetParent(parent)
    sdkanim.copyAnimation(node, helperNode)
    return helperNode


def is_top_node(node, node_list):
    if (node.GetParent() in node_list):
        return False
    else:
        return True


def mirrorUnskinned(leftSuffix, rightSuffix, copyDirection):
    MaxPlus.Animation.SetTime(0, False)
    src_node = MaxPlus.SelectionManager.GetNodes()
    mirroredTopNode = MaxPlus.INode.CreateTreeInstance(src_node[0])
    MaxPlus.SelectionManager.SelectNode(mirroredTopNode)
    MaxPlus.Core_EvalMAXScript("tm = $.transform\ntm.row1 = tm.row1 * [-1,1,1]\n$.transform  =tm")
    mirroredHierarchy = list(sdknode.getChildren(mirroredTopNode))
    mirroredHierarchy.append(mirroredTopNode)
    for n in mirroredHierarchy:
        n.SetName(n.GetName()[:-7] + "right")
        sdkutility.ResetXForm(n, True, True)
        sdkutility.remove_transform_keys(n)

    mirror_animation(src_node[0], mirroredTopNode, leftSuffix, rightSuffix, copyDirection)


def cleanUp(leftSuffix, rightSuffix, copyDirection):
    sceneRoot = MaxPlus.Core.GetRootNode()
    children = list(sdknode.getChildren(sceneRoot))
    for n in children:
        if isDummy(n):
            n.SetParent(MaxPlus.Core.GetRootNode())
            MaxPlus.INode.Delete(n)

    selection = MaxPlus.SelectionManager.GetNodes()
    for selected in selection:
        if copyDirection == 0:
            remove_unused_key(selected, rightSuffix, leftSuffix)
        elif copyDirection == 1:
            remove_unused_key(selected, leftSuffix, rightSuffix)


def setDummy(node):
    mxs_node = rt.maxOps.getNodeByHandle(node.GetHandle())
    rt.setUserProp(mxs_node, "PlotDummy", True)


def isDummy(node):
    mxs_node = rt.maxOps.getNodeByHandle(node.GetHandle())
    value = rt.getUserProp(mxs_node, "PlotDummy")
    return value
