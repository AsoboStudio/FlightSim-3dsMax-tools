from pymxs import runtime as rt

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