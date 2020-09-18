import pymxs
import re
rt = pymxs.runtime

def run():

    for o in rt.objects:
        if rt.Containers.IsContainerNode(o):
            match = re.search(r"_ID_\d+", o.name)
            if not match:
                rt.setUserProp(o, "babylonjs_ContainerID", 1)
                o.name = o.name + "_ID_1"
