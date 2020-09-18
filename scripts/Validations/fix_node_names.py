import MaxPlus
import re
import pymxs
rt = pymxs.runtime

def get_children(node):
    for c in node.Children:
        yield c
        for d in get_children(c):
            yield d

def run():
    root = MaxPlus.Core.GetRootNode()
    scene_nodes = list(get_children(root))
    for node in scene_nodes:
        name = node.GetName()
        name = name.replace("\n","")
        node.SetName(name)
    rt.messageBox("Operation Complete")

