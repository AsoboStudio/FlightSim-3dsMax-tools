from pymxs import runtime as rt
import maxsdk.node as node
import maxsdk.userprop as userprop
from maxsdk.globals import *
from maxsdk import qtUtils,utility
from PySide2 import QtCore, QtGui, QtWidgets
import ConvertTextureToPoligonMesh.ui.convertTextureToMesh_ui as convertTextureToMeshUI
import os

class ConvertTextureToMeshWindow(QtWidgets.QWidget, convertTextureToMeshUI.Ui_ConvertTextureToMesh):

    texturePath = ""
    defaultMsg = ""
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setupUi(self)
        self.retranslateUi(self)
        self.defaultMsg = self.info_lbl.text()
        self.texturePath = userprop.getUserProp(rt.rootNode,"FlightSim_ConvertTextureToMesh")
        state = userprop.getUserProp(rt.rootNode,"FlightSim_ConvertTextureToMesh_useMaterialAlpha")
        self.useAlpha_chb.setChecked(True if state == None else state)
        self.path_lbl.setText(self.texturePath)
        self.browse_btn.clicked.connect(self.loadTexture)
        self.convertToMesh_btn.clicked.connect(self.convertToMesh)
        self.useAlpha_chb.stateChanged.connect(self.onUseAlphaStateChanged)

    def isValidTexture(self, texturePath):
        if not self.texturePath or self.texturePath == "":
                    return False
        if not os.path.exists(self.texturePath):
                return False
        self.infoLbl = self.defaultMsg	
        return True
        
    def convertToMesh(self):
        if not self.useAlpha_chb.isChecked() and not self.isValidTexture(self.texturePath):
            self.info_lbl = "Specified texture is missing or not found"
            return
        
        subdivideMod = rt.subdivide()
        volSel = rt.Vol__Select ()
        for o in rt.selection:
            texturePath = self.texturePath
            if self.useAlpha_chb.isChecked():
                mat = o.material
                if rt.classOf(mat) == rt.FlightSim:
                    texturePath = mat.BaseColorTex
                elif rt.classOf(mat) == rt.Standardmaterial:
                    texturePath = mat.opacityMap.filename
                else:
                    self.info_lbl = "Currently only FlightSim material are supported"
                    continue

                if not os.path.isabs(texturePath):
                    texturePath = os.path.join( rt.pathConfig.getCurrentProjectFolder(),texturePath)
                if not self.isValidTexture(texturePath):
                    continue
                    
                        
                    
            p = rt.convertToPoly(o)
            rt.addModifier(o, subdivideMod)
            subdivideMod.size = 0.001
            rt.convertTo(o, rt.editable_poly)
            #hack adding the modifier only one time do not work for first object in iteration WTF?
            rt.addModifier(o, subdivideMod)
            subdivideMod.size = 0.001
            rt.convertTo(o, rt.editable_poly)
            rt.addModifier(p, volSel)
            volSel.level = 1
            volSel.invert = True
            bitmap = rt.Bitmaptexture(filename=texturePath)
            volSel.texture = bitmap
            volSel.method = 0
            volSel.volume = 4
            p= rt.convertToPoly(o)
            rt.subObjectLevel = 1
            p.delete(pymxs.runtime.Name("Vertex"))
            rt.convertTo(o, rt.editable_poly)
        
    def loadTexture(self):
        if self.texturePath and self.texturePath != "":
            self.texturePath = os.path.basename(self.texturePath)
        else:
            self.texturePath  = rt.maxFilePath
            
        self.texturePath, _ = QtWidgets.QFileDialog.getOpenFileName(self, self.tr("Load Image"), self.tr( self.texturePath ))
        if self.texturePath and self.texturePath != "":
            userprop.setUserProp(rt.rootNode,"FlightSim_ConvertTextureToMesh",self.texturePath)
        self.path_lbl.setText(self.texturePath)
        
    def onUseAlphaStateChanged(self):
        state = int(self.useAlpha_chb.isChecked())
        userprop.setUserProp(rt.rootNode,"FlightSim_ConvertTextureToMesh_useMaterialAlpha",state)


#~ w = ConvertTextureToMeshWindow()
#~ w.show()