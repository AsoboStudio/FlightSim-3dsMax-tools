from pymxs import runtime as rt
import node

def GetSceneMatByName(matName):
    SceneMats = []
    for matClass in rt.material.classes:
        for m in (rt.getclassinstances(matClass, processAllAnimatables=False, processChildren = True)):
            SceneMats.append(m)
    for SM in SceneMats:
        if SM.name == matName:
            return SM
    print("No mat match with this name found")

def getMaterialByFaceID(multiMat, ID):
    if rt.classOf(multiMat) == rt.MultiMaterial:
        matIdList = list(multiMat.materialIDList)
        for i in range(len(matIdList)):
            if multiMat.materialIDList[i] == ID:
                return multiMat.materialList[i]
    return None


def isMatInMultiMat(multiMat, mat):
    if rt.classOf(multiMat) == rt.MultiMaterial:
        if multiMat.material1 is None:
            return False
        for m in multiMat.materialList:
            if m.name == mat.name:
                return True
    return False


def getIDFromMaterial(multiMat, mat):
    if rt.classOf(multiMat) == rt.MultiMaterial:
        matList = list(multiMat.materialList)
        for i in range(len(matList)):
            if multiMat.materialList[i].name == mat.name:
                return multiMat.materialIDList[i]
    return -1


def assignMatToMutliMat(multiMat, mat):
    if rt.classOf(multiMat) == rt.MultiMaterial:
        if multiMat.material1 is None:
            multiMat.material1 = mat
        else:
            multiMat.numsubs = multiMat.numsubs + 1
            multiMat.materialList[multiMat.numsubs - 1] = mat

def assignMatToMutliMatFromID(multiMat, mat, ID):
    if rt.classOf(multiMat) == rt.MultiMaterial:
        multiMat.materialList[ID-1] = mat

def getConnectedMultiMaterials(mat, withID = False):
    nodes = node.getAllNodes()
    foundMats = []
    foundMatswID = {}
    for n in nodes:
        cmat = n.material
        if rt.classof(cmat) == rt.MultiMaterial:
            if cmat.numsubs > 0:
                for i in range(len(cmat.materialList)):
                    if cmat.materialList[i] == mat:
                        foundMats.append(cmat)
                        if withID:
                            foundMatswID[cmat] = i+1
    if withID:                    
        return foundMatswID
    else:
        return foundMats