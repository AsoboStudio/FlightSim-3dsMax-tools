import WiperTool.ui.mainwindow_ui as mainWindowUI
import WiperTool.ui.wiperConfigItem_ui as wiperConfigItemUI
import uuid

reload(wiperConfigItemUI)
reload(mainWindowUI)
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
from pymxs import runtime as rt
from maxsdk import utility
from maxsdk import userprop as sdkprop
import WiperTool_Max

reload(WiperTool_Max)
from WiperTool_Max import WiperTool_Max
import os


class WiperPointsDefinition(QWidget, wiperConfigItemUI.Ui_wiperPointsDefinition):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)
        self.setupUi(self)


class WipeMaskGenerator(QWidget, mainWindowUI.Ui_WiperMaskGenerator):
    wiperConfigsMap = None

    # tool parameters
    bakePath = None
    initFrame = 0
    midFrame = 0
    finalFrame = 0
    windshieldName = None

    def __init__(self):
        QWidget.__init__(self)
        self.setupUi(self)
        self.setContentsMargins(9, 9, 9, 9)
        self.__setSampleImage()
        intValidator = QIntValidator()
        self.bakePath = rt.maxFilePath if (rt.maxFilePath is not None) else rt.pathConfig.getCurrentProjectFolder()
        self.initalAnimFrame.setValidator(intValidator)
        self.finalAnimFrame.setValidator(intValidator)
        self.configGroupBoxlayout = QVBoxLayout()
        self.wiperConfigurationGroupBox.setLayout(self.configGroupBoxlayout)
        self.filePathButton.clicked.connect(lambda: self.__browseOutputFile(outputPath=self.bakePath))
        self.bakeTexture.clicked.connect(self.__bakeTexture)
        self.wiperConfigsMap = dict()
        self.__loadParams()
        self.outputPath.setText(self.bakePath)
        self.initalAnimFrame.setText(str(self.initFrame))
        self.midlleAnimationFrame.setText(str(self.midFrame))
        self.finalAnimFrame.setText(str(self.finalFrame))
        self.windshieldNodeName.setText(self.windshieldName)

        self.initalAnimFrame.textChanged.connect(lambda: self.__onParamChanged(0))
        self.midlleAnimationFrame.textChanged.connect(lambda: self.__onParamChanged(1))
        self.finalAnimFrame.textChanged.connect(lambda: self.__onParamChanged(2))
        self.windshieldNodeName.textChanged.connect(lambda: self.__onParamChanged(3))
        self.outputPath.textChanged.connect(lambda: self.__onParamChanged(4))

    @Slot()
    def __onParamChanged(self, param):
        self.initFrame = self.initalAnimFrame.text() if param == 0 else self.initFrame
        self.midFrame = self.midlleAnimationFrame.text() if param == 1 else self.midFrame
        self.finalFrame = self.finalAnimFrame.text() if param == 2 else self.finalFrame
        self.windshieldName = self.windshieldNodeName.text() if param == 3 else self.windshieldName
        self.bakePath = self.outputPath.text() if param == 4 else self.bakePath

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
        confItem = self.wiperConfigsMap[ID]
        confItem.hide()
        self.configGroupBoxlayout.removeWidget(confItem)
        del (confItem)
        self.wiperConfigsMap.pop(ID)

    def __browseOutputFile(self, outputPath):
        fileDialog = QFileDialog(self)
        # fileDialog.setAcceptMode(QFileDialog.AcceptOpen)
        bakePath = fileDialog.getSaveFileName(self, "Bake Texture in", outputPath, "Images (*.png)")
        if bakePath:
            self.outputPath.setText(bakePath[0])

    def __bakeTexture(self):
        wipersItems = self.__getWiperPointsList()
        wiperTool = WiperTool_Max(theGlass=self.windshieldName,
                                  startFrame=int(self.initFrame), midFrame=int(self.midFrame),
                                  endFrame=int(self.finalFrame), dummySets=wipersItems,
                                  outputpath=self.bakePath)
        wiperTool.run()

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
        params.update({"initFrame": self.initFrame})
        params.update({"midFrame": self.midFrame})
        params.update({"endFrame": self.finalFrame})
        params.update({"windshieldName": self.windshieldName})
        params.update({"bakePath": self.bakePath})
        params.update({"wiperItems": wiperArrayString})
        sdkprop.setUserPropDict(rt.rootNode, "WipeMaskGenerator", params)

    def __loadParams(self):
        params = sdkprop.getUserPropDict(rt.rootNode, "WipeMaskGenerator")

        if params:
            self.initFrame = params["initFrame"] if params.has_key("initFrame") else 0
            self.midFrame = params["midFrame"] if params.has_key("midFrame") else 0
            self.finalFrame = params["endFrame"] if params.has_key("endFrame") else 0
            self.windshieldName = params["windshieldName"] if params.has_key("windshieldName") else None
            self.bakePath = params["bakePath"] if params.has_key("bakePath") else None
            wipersItems = self.__parseWiperItemsString(params["wiperItems"]) if params.has_key("wiperItems") else None
            if not wipersItems:
                self.__addConfiguration(uuid.uuid4())
            else:
                for wItems in wipersItems:
                    self.__addConfiguration(uuid.uuid4(),wItems)
        else:
            self.__addConfiguration(uuid.uuid4())

    def closeEvent(self, *args, **kwargs):
        self.__saveParams()

if __name__ == '__main__':
    wiperGenerator = WipeMaskGenerator()
    utility.attachToMax(wiperGenerator)
    wiperGenerator.show()