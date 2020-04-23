import MaxPlus
import pymxs

rt = pymxs.runtime


def copyTransformFromController(controller, sourceName, targetName):
    # type: (MaxPlus.Control, str, str) -> None
    """
    Copy animation key from the source node to target on the specified controller
    :param controller: Source controller (rotation, position, ..)
    :param sourceName: Source node name
    :param targetName: Target node name
    :return: None
    """
    keyNumber = controller.GetNumKeys()
    MaxPlus.Animation.SetAnimateButtonState(True)
    for i in range(keyNumber):
        key_time = controller.GetKeyTime(i)
        MaxPlus.Animation.SetTime(key_time, False)
        rt_source = rt.getNodeByName(sourceName)
        rt_target = rt.getNodeByName(targetName)
        t = rt_source.getmxsprop("transform")
        rt_target.setmxsprop("transform", t)
    MaxPlus.Animation.SetAnimateButtonState(False)


def copyAnimation(source, target):
    # type: (MaxPlus.INode, MaxPlus.INode) -> None
    """
    Copy all animation keys on Position, Rotation, Scale controllers
    :param source: Source node
    :param target: Target node
    :return: None
    """
    if source.IsAnimated():
        sourceTransformControl = getTransformControl(source)

        posController = sourceTransformControl.GetPositionController()
        rotController = sourceTransformControl.GetRotationController()
        scaleController = sourceTransformControl.GetScaleController()

        copyTransformFromController(posController, source.GetName(), target.GetName())
        copyTransformFromController(rotController, source.GetName(), target.GetName())
        copyTransformFromController(scaleController, source.GetName(), target.GetName())


def getTransformControl(node):
    # type: (MaxPlus.INode) -> MaxPlus.Control
    """
    Get the Transform Control of the specified Node
    :param node: Node to query
    :return: Transform Control
    """
    for i in range(node.GetNumSubAnims()):
        subAnim = node.GetSubAnim(i)
        if str(subAnim) == "Animatable(Position/Rotation/Scale)":
            genericController = MaxPlus.Control__CastFrom(subAnim)
            return genericController


def plotAnimation(nodeList):
    """
    Plot animation for the entire Viewport TimeRange on passed node
    :param nodeList:
    :return:
    """
    try:
        MaxPlus.ViewportManager.DisableSceneRedraw()
        timeRange = MaxPlus.Animation.GetAnimRange()
        viewportFrame = timeRange.End() / 160
        MaxPlus.Animation.SetAnimateButtonState(True)

        for n in nodeList:
            tmp = MaxPlus.Factory.CreateHelperObject(MaxPlus.ClassIds.Point)
            tmp.ParameterBlock.Size.Value = 1.0
            tmpNode = MaxPlus.Factory.CreateNode(tmp)
            rt_target = rt.getNodeByName(tmpNode.Name)
            rt_source = rt.getNodeByName(n.Name)
            for i in range(viewportFrame):
                MaxPlus.Animation.SetTime(i * 160, False)
                t = rt_source.getmxsprop("transform")
                rt_target.setmxsprop("transform", t)
            command = '(getnodebyname "{0}").transform.controller = (getnodebyname "{1}").transform.controller'.format(
                n.Name, tmpNode.Name)
            print command
            MaxPlus.Core.EvalMAXScript(command)
    finally:
        MaxPlus.Animation.SetAnimateButtonState(False)
        MaxPlus.ViewportManager.EnableSceneRedraw()
        MaxPlus.Animation.SetTime(0, True)


def setKeyPRS(node):
    """
    Set key base on the curreent TrnaformController
    :param node:
    :return: None
    """
    transformController = getTransformControl(node)
    posController = transformController.GetPositionController()
    rotController = transformController.GetRotationController()
    scaleController = transformController.GetScaleController()
    posController.AddNewKey(MaxPlus.Now(), MaxPlus.Constants.AddkeyFlagged)
    rotController.AddNewKey(MaxPlus.Now(), MaxPlus.Constants.AddkeyFlagged)
    scaleController.AddNewKey(MaxPlus.Now(), MaxPlus.Constants.AddkeyFlagged)


def removeScaleKeys(node):
    transform_controller = getTransformControl(node)
    c = transform_controller.GetScaleController()
    c.DeleteKeys(MaxPlus.Constants.TrackDoall)


def removePositionKeys(node):
    transform_controller = getTransformControl(node)
    c = transform_controller.GetPositionController()
    c.DeleteKeys(MaxPlus.Constants.TrackDoall)


def removeRotationKeys(node):
    transform_controller = getTransformControl(node)
    c = transform_controller.GetRotationController()
    c.DeleteKeys(MaxPlus.Constants.TrackDoall)


def removeTransformKeys(node):
    removePositionKeys(node)
    removeRotationKeys(node)
    removeScaleKeys(node)
