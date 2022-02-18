from pymxs import runtime as rt
import maxsdk.node as node
import maxsdk.material as material

from maxsdk.globals import *

if MAXVERSION() < MAX2021:
    import collections


GLOBAL_IDENTICALS_MATS = []

class MatwDouble():
    OrigMat = None
    DoublesMats = []
    def __init__(self, _origMat, _doublesMats):
        self.OrigMat = _origMat
        self.DoublesMats = _doublesMats
    

def areSameOrdDicts(_dict1,_dic2, _skipGuID = False):
    for k, l in zip(_dict1,_dic2):
        if k != l:
            return False

    for k, l in zip(_dict1.items(),_dic2.items()):
        if k != l:
            if "guid" in str(k) and _skipGuID:
                continue
            else:
                return False
    return True

def isMatInOriginMat(_mat):
    global GLOBAL_IDENTICALS_MATS
    if GLOBAL_IDENTICALS_MATS != None:
        for i in range(len(GLOBAL_IDENTICALS_MATS)):
            if GLOBAL_IDENTICALS_MATS[i].OrigMat == _mat:
                return True, i
    return False, 0

def isMatInDoubles(_mat):
    global GLOBAL_IDENTICALS_MATS
    if GLOBAL_IDENTICALS_MATS != None:
        for i in range(len(GLOBAL_IDENTICALS_MATS)):
            for j in range(len(GLOBAL_IDENTICALS_MATS[i].DoublesMats)):
                if GLOBAL_IDENTICALS_MATS[i].DoublesMats[j] == _mat:
                    return True, i, j
    return False, 0, 0

def PropDicInallMapPropDic(CurMat, CurPropDic, AllPropDic):
    global GLOBAL_IDENTICALS_MATS
    for ALP in AllPropDic:
        if areSameOrdDicts(CurPropDic,AllPropDic[ALP], True):
            if CurMat.name != ALP.name:
                b, pos = isMatInOriginMat(ALP)
                c, pos1 = isMatInOriginMat(CurMat)
                d, pos2, pos3 = isMatInDoubles(ALP)
                e, pos4, pos4 = isMatInDoubles(CurMat)
                if b or c:
                    if b :
                        if c == False:
                            if e == False:
                                GLOBAL_IDENTICALS_MATS[pos].DoublesMats.append(CurMat)

                    if c :
                        if b == False:
                            if d == False:
                                GLOBAL_IDENTICALS_MATS[pos1].DoublesMats.append(ALP)
                        
                else:
                    if d == False and e == False:
                        doubleList = []
                        doubleList.append(ALP)
                        GLOBAL_IDENTICALS_MATS.append(MatwDouble(CurMat,doubleList))

def runMatSceneCleaner():
    global GLOBAL_IDENTICALS_MATS
    GLOBAL_IDENTICALS_MATS = []
    SceneMats = []
    UselessMats = []

    if MAXVERSION() < MAX2021:
        AllMatswProps = collections.OrderedDict([])
    else:
        AllMatswProps = {}

    originalsMats = []

    for matClass in rt.material.classes:
        for m in (rt.getclassinstances(matClass, processAllAnimatables=False, processChildren = True)):
            SceneMats.append(m)
        for mi in (rt.getclassinstances(matClass, processAllAnimatables=True, processChildren = True)):
            if mi not in SceneMats:
                UselessMats.append(mi)

    for i in range(len(SceneMats)):
        #if rt.classOf(SceneMats[i]) ==  rt.FlightSim:
        #if rt.classOf(SceneMats[i]) ==  rt.Physical_Material: //Uncomment if you wants to target specifics material types
        if MAXVERSION() < MAX2021:
            MatwProps = collections.OrderedDict([])
        else:
            MatwProps = {}
        propName = rt.getPropNames(SceneMats[i])
        for p in propName:
            param = rt.getProperty(SceneMats[i], p)
            MatwProps[p] = param
        AllMatswProps[SceneMats[i]] = MatwProps
            

    for mp in AllMatswProps:
        PropDicInallMapPropDic(mp, AllMatswProps[mp], AllMatswProps)


    for dbs in GLOBAL_IDENTICALS_MATS:
        MeshfromCopies = []
        DoublesMatswMultimatnID = []

        for dm in dbs.DoublesMats:
            print("[{0}] was a copy of [{1}], it has been removed and reassigned to [{1}]".format(dm,dbs.OrigMat))
            multMatsLinToCurDoublewID = material.getConnectedMultiMaterials(dm, True)
            if len(multMatsLinToCurDoublewID) != 0:
                DoublesMatswMultimatnID.append(multMatsLinToCurDoublewID)

            ndsfromMat = node.get_nodes_by_material(dm)
            for nfm in ndsfromMat:
                MeshfromCopies.append(nfm)

        for DMwM in DoublesMatswMultimatnID:
            for KeyMulToID in DMwM:
                material.assignMatToMutliMatFromID(KeyMulToID, dbs.OrigMat, DMwM[KeyMulToID])

        for mfc in MeshfromCopies:
            mfc.material = dbs.OrigMat

    rt.holdMaxFile()
    rt.fetchMaxFile(quiet = True)
    copyCounter = 0
    for dbs1 in GLOBAL_IDENTICALS_MATS:
        for dm1 in dbs.DoublesMats:
            copyCounter +=1
    rt.messageBox("Double Mat Scene Cleaner Tool finished. It has found and reasigned {0} materials duplicates".format(copyCounter))

