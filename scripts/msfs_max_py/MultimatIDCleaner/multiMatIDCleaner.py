
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

import MultimatIDCleaner.ui.mainwindow_ui as mainWindowUI
from maxsdk.globals import *
from maxsdk import qtUtils, sceneUtils, userprop, utility
import pymxs
from pymxs import runtime as rt

class MatListnBlank():
    MultimatList = []
    Blanks = []
    def __init__(self, _multimatList, _blanks):
        self.MultimatList = _multimatList
        self.Blanks = _blanks
    
    def get_MultimatList(self):
        return self.MultimatList
    def get_Blanks(self):
        return self.Blanks



class MainWindow(QWidget, mainWindowUI.Ui_MultimatCleaner):
    def __init__(self):
        QWidget.__init__(self)
        self.setupUi(self)
        self.retranslateUi(self)
        #button
        self.pushButton.pressed.connect(lambda: self._clickedFixedmatID())

    def _setNewFaceIDinObject(self,oldID, newID, Node):
        for f in range(1, Node.numfaces):
            if rt.classof(Node) == rt.Editable_mesh:
                curfaceID = rt.getFaceMatID(Node, f)
                if curfaceID == oldID:
                    rt.setFaceMatID(Node, f, newID)
            elif rt.classof(Node) == rt.Editable_poly:
                curfaceID = rt.polyop.getFaceMatID(Node, f)
                if curfaceID == oldID:
                    rt.polyop.setFaceMatID(Node, f, newID)
            else:
                print("Not a mesh or poly object")
                break
            

    def _clickedFixedmatID(self):
        #pymxs.redraw(False)
        selection = list(rt.selection)
        aTreatedMAt = []
        MTB = {}
        for s in selection:
            if rt.classof(s) == rt.Editable_mesh or rt.classof(s) == rt.Editable_poly:
                cmat = s.material
                if rt.classOf(cmat) == rt.Multimaterial and cmat not in aTreatedMAt:
                    blanks = []
                    offset = 0
                    #Extend multimat large enough to check for blanks
                    for i in range(len(cmat.materialList)):
                        if i < cmat.materialIDList[i - offset] :
                            offset += 1
                            if i != 0:
                                cmat.materialList.count += 1
                    offset = 0
                    for i in range(len(cmat.materialList)):
                        if i < cmat.materialIDList[i - offset] :
                            offset += 1
                            if i != 0:
                                blanks.append(i)
                                matlistcount = len(cmat.materialList)

                    aTreatedMAt.append(cmat)

                    print("First Matlist to ser : {0}".format(cmat.materialIDList))
                    x = [y for y in cmat.materialIDList]
                    MTB[cmat] = MatListnBlank(x, blanks)
                    print("First Fake matlB : {0}".format(MTB[cmat]))
                    if DEBUG_MODE():
                        print("First Blanks : {0}".format(blanks))
                        print("First Offsets : {0}".format(offset - 1))

#For the first mesh that is Mat ID recalculed
                    for j in range(len(blanks)):
                        repercute = False
                        if DEBUG_MODE():
                            print("First CurBlank : {0}".format(j))
                            print("_________________")
                        for i in range(len(cmat.materialList)):
                            if repercute:
                                if DEBUG_MODE():
                                    print("_______First_repercuteon________")
                                    print("First Pos in ID list to repercute : {0}, First prec value : {1}".format(i,cmat.materialIDList[i]))
                                    print("First New value to put : {0}".format(i + 1))                                
                                #self._setNewFaceIDinObject(oldID = cmat.materialIDList[i],newID = i + 1, Node = s)
                                cmat.materialIDList[i] = i + 1

                            if i == blanks[j] - 1 and repercute == False:
                                if DEBUG_MODE():
                                    print ("First Pos ID to Change : {0} ".format(blanks[j] - 1))
                                    print("First Value changed : {0}".format(blanks[j]) )
                                #self._setNewFaceIDinObject(oldID = cmat.materialIDList[i],newID = blanks[j],Node = s)
                                cmat.materialIDList[i] = blanks[j]
                                repercute = True
                    
#For other meshs that share the same multimat that are selected                    
                if rt.classOf(cmat) == rt.Multimaterial and cmat in MTB:
                    print("Current Fake matlB : {0}".format(MTB[cmat]))
                    print("Current Fake MTlMList : {0}".format(MTB[cmat].get_MultimatList()))
                    FakeMatList = list(MTB[cmat].get_MultimatList())

                    for j in range(len(MTB[cmat].get_Blanks())):
                        repercute = False
                        if DEBUG_MODE():
                            print("CurBlank : {0}".format(j))
                            print("_________________")

                        for i in range(len(FakeMatList)):
                            if repercute:
                                if DEBUG_MODE():
                                    print("_______repercuteon________")
                                    print("Pos in ID list to repercute : {0}, prec value : {1}".format(i, FakeMatList[i]))
                                    print("New value to put : {0}".format(i + 1))
                                self._setNewFaceIDinObject(oldID = FakeMatList[i],newID = i + 1, Node = s)
                                FakeMatList[i] = i + 1

                            if i == MTB[cmat].get_Blanks()[j] - 1 and repercute == False:
                                if DEBUG_MODE():
                                    print ("Pos ID to Change : {0} ".format(MTB[cmat].get_Blanks()[j] - 1))
                                    print("Value changed : {0}".format(MTB[cmat].get_Blanks()[j]) )
                                self._setNewFaceIDinObject(oldID = FakeMatList[i],newID = MTB[cmat].get_Blanks()[j],Node = s)
                                FakeMatList[i] = MTB[cmat].get_Blanks()[j]
                                repercute = True
            else:
                print("Not a EditableMesh or EditablePoly object, skipped")
        self.textBrowser.setText("Cleaned : {0}".format(aTreatedMAt))
        rt.holdMaxFile()
        rt.fetchMaxFile(quiet = True)




def run():

    MultimatCleaner = MainWindow()
    if MAXVERSION() <= MAX2020:
        import MaxPlus
        MaxPlus.AttachQWidgetToMax(MultimatCleaner)
    MultimatCleaner.show()
