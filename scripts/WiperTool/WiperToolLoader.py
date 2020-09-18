import uuid

from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
from pymxs import runtime as rt
from maxsdk import utility
from maxsdk import userprop as sdkprop
from maxsdk.globals import *
from WiperTool.WiperTool_Max import WiperTool_Max
import WiperTool.ui.mainwindow_ui as mainWindowUI
import WiperTool.ui.wiperConfigItem_ui as wiperConfigItemUI


import os


class WiperPointsDefinition(QWidget, wiperConfigItemUI.Ui_wiperPointsDefinition):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)
        self.setupUi(self)


class WipeMaskGenerator(QWidget,mainWindowUI.Ui_WiperMaskGenerator):
    wiperConfigsMap = None
    # tool parameters
    bakePath = None
    animInFrameStart = 0
    animInFrameEnd = 0
    animOutFrameStart = 0
    animOutFrameEnd = 0
    windshieldName = None

    def __init__(self):
        QWidget.__init__(self)
        self.setupUi(self)
        self.setContentsMargins(9, 9, 9, 9)
        self.__setSampleImage()
        intValidator = QIntValidator()
        self.bakePath = rt.maxFilePath if (rt.maxFilePath is not None) else rt.pathConfig.getCurrentProjectFolder()
        self.AnimInStart.setValidator(intValidator)
        self.AnimInEnd.setValidator(intValidator)
        self.AnimOutStart.setValidator(intValidator)
        self.AnimOutEnd.setValidator(intValidator)
        self.configGroupBoxlayout = QVBoxLayout()
        self.wiperConfigurationGroupBox.setLayout(self.configGroupBoxlayout)
        self.filePathButton.clicked.connect(lambda: self.__browseOutputFile(outputPath=self.bakePath))
        self.bakeTexture.clicked.connect(self.__bakeTexture)
        self.wiperConfigsMap = dict()
        self.__loadParams()
        self.outputPath.setText(self.bakePath)
        self.AnimInStart.setText(str(self.animInFrameStart))
        self.AnimInEnd.setText(str(self.animInFrameEnd))
        self.AnimOutStart.setText(str(self.animOutFrameStart))
        self.AnimOutEnd.setText(str(self.animOutFrameEnd))
        self.windshieldNodeName.setText(self.windshieldName)

        self.AnimInStart.textChanged.connect(lambda: self.__onParamChanged(0))
        self.AnimInEnd.textChanged.connect(lambda: self.__onParamChanged(1))
        self.AnimOutStart.textChanged.connect(lambda: self.__onParamChanged(2))
        self.AnimOutEnd.textChanged.connect(lambda: self.__onParamChanged(3))
        self.windshieldNodeName.textChanged.connect(lambda: self.__onParamChanged(4))
        self.outputPath.textChanged.connect(lambda: self.__onParamChanged(5))

    @Slot()
    def __onParamChanged(self, param):
        self.animInFrameStart = self.AnimInStart.text() if param == 0 else self.animInFrameStart
        self.animInFrameEnd = self.AnimInEnd.text() if param == 1 else self.animInFrameEnd
        self.animOutFrameStart = self.AnimOutStart.text() if param == 2 else self.animOutFrameStart
        self.animOutFrameEnd = self.AnimOutEnd.text() if param == 3 else self.animOutFrameEnd
        self.windshieldName = self.windshieldNodeName.text() if param == 4 else self.windshieldName
        self.bakePath = self.outputPath.text() if param == 5 else self.bakePath

    def __setSampleImage(self):
        imageDir = os.path.dirname(os.path.abspath(mainWindowUI.__file__))
        sampleImagePath = os.path.join(imageDir, "PlacementInfo.jpg")
        if os.path.exists(sampleImagePath):
            sampleImagePixmap = QPixmap(sampleImagePath)
            self.sampleImage.setPixmap(sampleImagePixmap)

    def __addConfiguration(self, ID,items = None):
        wiperPointsDefinition = WiperPointsDefinition()
        self.wiperConfigsMap.update({ID: wiperPointsDefinition})
        self.configGroupBoxlayout.addWidget(wiperPointsDefinition)
        wiperPointsDefinition.addConfig.clicked.connect(lambda: self.__addConfiguration(uuid.uuid4()))
        wiperPointsDefinition.removeConfig.clicked.connect(lambda: self.__removeConfiguration(ID))
        if items:
            wiperPointsDefinition.wiperPointA.setText(items[0])
            wiperPointsDefinition.wiperPointB.setText(items[1])


    @Slot()
    def __removeConfiguration(self, ID):
        if len(self.wiperConfigsMap) <= 1:
            return
        confItem = self.wiperConfigsMap[ID]
        confItem.hide()
        self.configGroupBoxlayout.removeWidget(confItem)
        del (confItem)
        self.wiperConifgsMap.pop(ID)

    def __browseOutputFile(self, outputPath):
        fileDialog = QFileDialog(self)
        # fileDialog.setAcceptMode(QFileDialog.AcceptOpen)
        bakePath = fileDialog.getSaveFileName(self, "Bake Texture in", outputPath, "Images (*.tga)")
        if bakePath:
            self.outputPath.setText(bakePath[0])

    def __bakeTexture(self):
        wipersItems = self.__getWiperPointsList()
        wt = WiperTool_Max(theGlass=self.windshieldName,animInStart=int(self.animInFrameStart), animInEnd=int(self.animInFrameEnd),animOutStart=int(self.animOutFrameStart),animOutEnd=int(self.animOutFrameEnd), dummySets=wipersItems,outputpath=self.bakePath)
        wt.run()

    def __getWiperPointsList(self):
        wipersItems = list()
        for id, widget in self.wiperConfigsMap.items():
            if isinstance(widget, WiperPointsDefinition):
                wiperPoitA = widget.wiperPointA.text()
                wiperPoitB = widget.wiperPointB.text()
                if wiperPoitA and wiperPoitB:
                    wiperPoints = [wiperPoitA, wiperPoitB]
                    wipersItems.append(wiperPoints)
        return wipersItems


    def __buildWiperItemsString(self, wipersItems):
        wiperArrayString = str()
        for i in range(len(wipersItems)):
            wiperPoints = wipersItems[i]
            wiperArrayString += "{0}&{1}".format(wiperPoints[0], wiperPoints[1])
            if i < len(wipersItems)-1:
                wiperArrayString += "|"
        return wiperArrayString

    def __parseWiperItemsString(self,wiperItemsString):
        wipersItems = list()
        if wiperItemsString:
            for item in wiperItemsString.split("|"):
                wiperPoints = item.split("&")
                wipersItems.append(wiperPoints)
        return wipersItems

    def __saveParams(self):
        wipersItems = self.__getWiperPointsList()
        wiperArrayString = self.__buildWiperItemsString(wipersItems)
        params = dict()
        params.update({"animInStartFrame": self.animInFrameStart})
        params.update({"animInEndFrame": self.animInFrameEnd})
        params.update({"animOutStartFrame": self.animOutFrameStart})
        params.update({"animOutEndFrame": self.animOutFrameEnd})
        params.update({"windshieldName": self.windshieldName})
        params.update({"bakePath": self.bakePath})
        params.update({"wiperItems": wiperArrayString})
        sdkprop.setUserPropDict(rt.rootNode, "WipeMaskGenerator", params)

    def __loadParams(self):
        params = sdkprop.getUserPropDict(rt.rootNode, "WipeMaskGenerator")

        if params:
            self.animInFrameStart = params["animInStartFrame"] if "animInStartFrame" in params.keys() else 0
            self.animInFrameEnd = params["animInEndFrame"] if "animInEndFrame" in params.keys() else 0 
            self.animOutFrameStart = params["animOutStartFrame"] if "animOutStartFrame" in params.keys() else 0
            self.animOutFrameEnd = params["animOutEndFrame"] if "animOutEndFrame" in params.keys() else 0
            self.windshieldName = params["windshieldName"] if "windshieldName" in params.keys() else None
            self.bakePath = params["bakePath"] if "bakePath" in params.keys() else None 
            wipersItems = self.__parseWiperItemsString(params["wiperItems"]) if "wiperItems" in params.keys() else None
            if not wipersItems:
                self.__addConfiguration(uuid.uuid4())
            else:
                for wItems in wipersItems:
                    self.__addConfiguration(uuid.uuid4(),wItems)
        else:
            self.__addConfiguration(uuid.uuid4())

    def closeEvent(self, *args, **kwargs):
        self.__saveParams()
wiperGenerator = None
def run():
    global wiperGenerator
    wiperGenerator = WipeMaskGenerator()
    wiperGenerator.show()
