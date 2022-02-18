from globals import *
if MAXVERSION() < MAX2017:
    import MaxPlus
else:
    from pymxs import runtime as rt
import os
import json_utility

import utility as sdk_utility

import json

class INodeEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, MaxPlus.INode):
            node = {}

            node["name"] = obj.GetName()
            source_transform_control = sdk_utility.GetTransformControl(obj)
            posController = source_transform_control.GetPositionController()
            rotController = source_transform_control.GetRotationController()
            scaleController = source_transform_control.GetScaleController()

            if posController is not None and posController.GetNumKeys()>0:
                node["positionController"] = json_utility.encodePositionController(posController)
            if rotController is not None and rotController.GetNumKeys()>0:
                node["rotationController"] = json_utility.encodeRotationController(rotController)
            # if scaleController is not None and scaleController.GetNumKeys()>0:
            #     node["scaleController"] = JSONUtility.encodeScaleController(scaleController)
            return node
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)

    @staticmethod
    def decodeNode(data):
        name = data["name"]
        node = rt.getNodeByName(name) if (MAXVERSION() >= MAX2017) else MaxPlus.INode.GetINodeByName(name)
        if not node:
            print("Node: {0} not found".format(data["name"]))
            return

        source_transform_control = sdk_utility.GetTransformControl(node)
        posController = source_transform_control.GetPositionController()
        rotController = source_transform_control.GetRotationController()
        if "positionController" in data:
            json_utility.decodePositionController(posController, data["positionController"])
        if "rotationController" in data:
            json_utility.decodeRotationController(rotController, data["rotationController"])
        # JSONUtility.encodeController(scaleController, obj.GetName())
