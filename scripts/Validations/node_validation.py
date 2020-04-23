import sys
import os
import MaxPlus
import pymxs
import re
rt = pymxs.runtime

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path)

import layer_validation
reload(layer_validation)

sys.path.append(os.path.join(os.path.dirname(dir_path), os.pardir))

from maxsdk import utility as sdk_utility
reload(sdk_utility)

from maxsdk import layer as sdkLayer
reload(sdkLayer)



def check_node_validation(silent = False):
    ##check node name
    nodes = sdk_utility.getAllNodes()
    layer_zero = rt.LayerManager.getLayer(0)
    shared_layer = rt.LayerManager.getLayerFromName("SHARED")
    shared_nodes = sdkLayer.getAllNodeInLayerHierarchy(shared_layer)
    ignore_nodes = sdkLayer.getAllNodeInLayerHierarchy(layer_zero)
    wrong_nodes = ""
    if(nodes is not None):
        for n in nodes:
            if n in ignore_nodes:
                continue
            if n == MaxPlus.Core.GetRootNode():
                continue

            originalName = n.GetName()
            noNamespace = re.sub("^.*:","",originalName)
            x = re.search("^(?!x).*$",noNamespace)
            y = re.search(r"\w*(_left|_right|_center)\b",noNamespace)
            if n in shared_nodes:
                if y is None:
                    wrong_nodes += n.GetName() + "\n"
            else:
                if x is not None:
                    wrong_nodes += n.GetName() + "\n"
                if y is None:
                    wrong_nodes += n.GetName() + "\n"

    if not silent:
        if len(wrong_nodes)>0:
                rt.messageBox("WARNING!!!\n\n Following Objects DO NOT not respect naming convention, LOD not specified,should be of type xN_whatever_left/right/center: \n\n{0}".format(wrong_nodes))
            #return
        else:
                rt.messageBox("Node's name validated")

    #check node relative to layer
    nodes = sdk_utility.getAllNodes()
    wrong_nodes_in_layer = ""
    wrong_nodes = ""
    if nodes is not None:
        for n in nodes:
            if n in ignore_nodes:
                continue
            if n == MaxPlus.Core.GetRootNode():
                continue
            layer_name = n.GetLayer().GetName()
            if (layer_name == str(0)):
                continue
            layer_lod_value = layer_name[1]
            originalName = n.GetName()
            noNamespace = re.sub("^.*:", "", originalName)
            y = re.search(r"\w*(_left|_right|_center)\b", noNamespace)
            nod_lod_value = noNamespace[1]
            if layer_lod_value != nod_lod_value:
                wrong_nodes_in_layer  += n.GetName() + "is in layer "+layer_name+" with different LOD value" +"\n"
            if y is None:
                wrong_nodes  += n.GetName() +"\n"

    if(wrong_nodes != ""):
        return
    if not silent:
        if len(wrong_nodes_in_layer)>0:
                rt.messageBox("WARNING!!!\n\n Following Objects are children of a wrong layer \n\n{0}".format(wrong_nodes_in_layer))
        else:
            rt.messageBox("Node's and Layer's name validated!!! BRAVO!!!")

def run():
    if layer_validation.check_layers_names():
        check_node_validation()


