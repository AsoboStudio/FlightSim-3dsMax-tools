import sys
import os
import MaxPlus
import pymxs
rt = pymxs.runtime

import re

# to add module from parent folder
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

from maxsdk import layer as sdkLayer


def check_layers_names(silent = False):
    ##check layers name
    layers = sdkLayer.getAllLayers()
    layer_zero = rt.LayerManager.getLayer(0)
    shared = rt.LayerManager.getLayerFromName("SHARED")
    ignore_layers = []
    sdkLayer.getLayerChildren(layer_zero,ignore_layers)
    sdkLayer.getLayerChildren(shared, ignore_layers)
    wrong_layers = ""
    if(layers is not None):
        for l in layers:
            if l in ignore_layers:
                continue
            x = re.search("^(?!x).*$",l.name)
            if x is not None:
                wrong_layers  += l.name +"\n"

    if len(wrong_layers)>0:
        if not silent:
            rt.messageBox("WARNING!!!\n\n Followwing Objects DO NOT respect naming convention, layer LOD not specified,should be of type xN \n\n{0} ".format(wrong_layers))
        return False
    else:
        return True



def run():
    if check_layers_names():
        rt.messageBox("Layer's name validated")