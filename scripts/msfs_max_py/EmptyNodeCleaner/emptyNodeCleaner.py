from pymxs import runtime as rt
from maxsdk import node

def runEmptyNodeCleaner():
    sceneNodes = []
    sceneNodes = node.getAllNodes()
    NodesToRemove = []

    for sn in sceneNodes:
        cl = rt.classOf(sn)
        if cl == rt.Editable_Poly or cl == rt.Editable_Mesh:
            NF = sn.numfaces
            if NF <= 0:
                NodesToRemove.append(sn)

    for NTR in NodesToRemove:
        print("{0} was deleted because it was not containing any geometry".format(NTR))
        rt.delete(NTR)
