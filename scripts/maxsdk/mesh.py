import MaxPlus


def getObjectMesh(node):
    # type: (MaxPlus.INode) -> MaxPlus.TriMeshGeometry
    """
    Convert specified Node in a EditableMesh
    :param node: Node to query
    :return: editableMesh of Node
    """
    node.Convert(MaxPlus.ClassIds.TriMeshGeometry)
    objectState = node.EvalWorldState()
    objectOriginal = objectState.Getobj()
    triObj = MaxPlus.TriObject._CastFrom(objectOriginal)
    triMesh = triObj.GetMesh()
    return triMesh
