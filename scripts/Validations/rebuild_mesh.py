from pymxs import runtime as rt
from maxsdk import sceneUtils

def box_trick(objects):
    parents = []
    animations = []
    layers = []
    result = []
    for objA in objects:
        if rt.classof(objA) == rt.Editable_Poly or rt.classof(objA) == rt.point:
            parent = objA.parent
            parentGuid = None
            if parent is not None:
                parentGuid = rt.getUserProp(parent, "babylonjs_GUID")
            parents.append(parentGuid)
            layers.append(objA.layer)
        
    for objA in objects:
        if rt.classof(objA) == rt.point:
            buffer = rt.getUserPropBuffer(objA)            
            b = rt.point()
            b.size = objA.size
            b.name = objA.name
            b.cross = objA.cross
            b.box = objA.box
            #b.controller = objA.controller
            b.controller.position = objA.controller.position
            b.rotation = objA.rotation
            b.position = objA.position
            b.pivot = objA.pivot
            b.layer = objA.layer
            rt.delete(objA)
            rt.setUserPropBuffer(b,buffer)
            result.append(b)
        elif rt.classof(objA) == rt.Editable_Poly:
            name = objA.name
            buffer = rt.getUserPropBuffer(objA)
            b = rt.box()
            b.position = objA.position
            b.rotation = objA.rotation
            b.backfaceCull = objA.backfaceCull
            lay = objA.layer
            pivot = objA.pivot
            a = rt.convertToPoly(b)
            rt.polyop.attach(a, objA)
            objB = rt.convertToPoly(a)
            startIndex = 1
            rt.polyop.deleteFaces(objB, [startIndex, startIndex + 1, startIndex + 2, startIndex + 3, startIndex + 4, startIndex + 5])
            rt.setUserPropBuffer(objB, buffer)
            objB.layer = lay
            objB.pivot = pivot
            objB.name = name
            result.append(objB)
    return zip(result,parents, layers)

def find_object_with_guid(guid):
    everything = sceneUtils.getAllObjects()
    for _, e in enumerate(everything):
        if (rt.getUserProp(e, "babylonjs_GUID") == guid):
            return e
    return None

def gather_parents_from_scene_using_guids(parentTable):
    """
    parentTable = tuple(MAXObj: object, string: parent guid)
    """
    guidToObj = {}
    for _, parentGuid,_ in parentTable:
        if parentGuid is None:
            continue
        parentObj = find_object_with_guid(parentGuid)
        if parentObj is not None:
            guidToObj[parentGuid] = parentObj
    return guidToObj

def run():
    sel = sceneUtils.getSelectedObjects()
    # we do the helper last because the mesh need to be cleansed first
    sel = sorted(sel, key=lambda x: rt.classof(x) == rt.point)

    parentTable = box_trick(sel)
    guidToObj = gather_parents_from_scene_using_guids(parentTable)

    for obj, parentGuid, layer in parentTable:
        if parentGuid is not None:
            obj.parent = guidToObj[parentGuid]      
        layer.addNode(obj)

if __name__ == "__main__":
    run()