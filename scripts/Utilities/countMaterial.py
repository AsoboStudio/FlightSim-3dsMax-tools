from pymxs import runtime as rt


def run():
    selection = rt.getCurrentSelection()
    allMats = []
    for _, sel in enumerate(selection):
        material = sel.mat
        matClass = rt.classof(material)
        objClass = rt.classof(sel)
        superMatClass = rt.superclassof(material)
        if objClass == rt.Editable_Poly or objClass == rt.Editable_mesh or objClass == rt.Editable_Patch:
            matCount = 0
            if matClass == rt.Multimaterial:
                mats = []
                facecount = rt.getNumFaces(sel)
                for i in range(1, facecount+1):
                    matId = sel.getFaceMaterial(i)
                    actualMaterial = rt.getSubMtl(material, matId)
                    
                    if actualMaterial not in mats:
                        mats.append(actualMaterial)

                    if actualMaterial not in allMats:
                        allMats.append(actualMaterial)

                    matCount = len(mats)
            elif superMatClass == rt.material:
                if material not in allMats:
                    allMats.append(material)
                matCount = 1
            print("{0} has {1} material(s)".format(sel.name, matCount))
        else:
            print("{0} is not of the right type to perform a material count".format(sel.name))
    print("{0} unique material found in the selection.".format(len(allMats)))
