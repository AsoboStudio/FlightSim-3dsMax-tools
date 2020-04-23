import MaxPlus

def get_children(node):
    for c in node.Children:
        yield c
        for d in get_children(c):
            yield d

def printRootPropBuffer():
    print "root prop"
    rootNode = MaxPlus.Core.GetRootNode()
    buffer = MaxPlus.WStr()
    MaxPlus.INode.GetUserPropBuffer(rootNode,buffer)
    bufferString = buffer.Contents()
    bufferString = bufferString.replace(";","\n")
    print bufferString

def cleanRootPropBuffer():
    rootNode = MaxPlus.Core.GetRootNode()
    buffer = MaxPlus.WStr()
    MaxPlus.INode.SetUserPropBuffer(rootNode, buffer)


# cleanRootPropBuffer()
printRootPropBuffer()
# nodeinScne = list(getChildren(rootNode))
# for node in nodeinScne:
#     print node.GetHandle()