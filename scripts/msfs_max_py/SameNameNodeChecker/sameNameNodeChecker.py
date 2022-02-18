from pymxs import runtime as rt
from maxsdk import node
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

import SameNameNodeChecker.ui.mainwindow_ui as mainWindowUI
import SameNameNodeChecker.view.treeViewNames as treeViewNames
from maxsdk.globals import *
from maxsdk import qtUtils, sceneUtils, userprop, utility
import pymxs
import time
import datetime

class NamewDouble():
    OrigName = None
    DoublesNames = []
    def __init__(self, _origName, _doublesNames):
        self.OrigName = _origName
        self.DoublesNames = _doublesNames

class MainWindow(QWidget, mainWindowUI.Ui_SameNameNodeChecker):
    GLOBAL_IDENTICALS_NAMES = []
    sceneNodes = []

    def __init__(self):
        QWidget.__init__(self)
        self.setupUi(self)
        self.retranslateUi(self)
        #button
        self.pushButton.pressed.connect(lambda: self._runSameNameNodeChecker())
        self.RenameChecked.pressed.connect(lambda: self._RenameTicked())
        self.DeleteChecked.pressed.connect(lambda: self._DeleteTicked())
        self.ApplyModToScene.pressed.connect(lambda: self._ApplymodToScene())
        #Treeview
        self.verticalLayout_2.removeWidget(self.NameCopyTab)
        self.NameCopyTab.setHidden(True)
        self.NameCopyTab = treeViewNames.TreeViewName(self.verticalLayoutWidget)

        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        #sizePolicy.setHeightForWidth(self.NameCopyTab.sizePolicy().hasHeightForWidth())
        self.NameCopyTab.setSizePolicy(sizePolicy)
        self.NameCopyTab.setMinimumHeight(500)
        self.NameCopyTab.setMaximumHeight(500)

        self.NameCopyTab.setAlternatingRowColors(True)
        self.NameCopyTab.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.NameCopyTab.setIndentation(10)
        self.NameCopyTab.setObjectName("NameCopyTab")
        self.NameCopyTab.setColumnWidth(0, 140)
        self.NameCopyTab.setColumnWidth(1, 40)
        self.NameCopyTab.setColumnWidth(2, 40)
        self.NameCopyTab.setSortingEnabled(True)
        self.NameCopyTab.sortItems(0, Qt.SortOrder.AscendingOrder)
        self.NameCopyTab.header().setDefaultSectionSize(50)
        self.NameCopyTab.headerItem().setText(0, QApplication.translate("SameNameNodeChecker", "          BaseName", None, -1))
        self.NameCopyTab.headerItem().setText(1, QApplication.translate("SameNameNodeChecker", "Suffixe to add", None, -1))
        self.NameCopyTab.headerItem().setText(2, QApplication.translate("SameNameNodeChecker", "Final Name", None, -1))
        self.checkBoxNames = qtUtils.createCheckBox(qtWidget=self.NameCopyTab)
        self.NameCopyTab.setGlobalCheckBox(self.checkBoxNames)

        self.verticalLayout_2.insertWidget(4, self.NameCopyTab)



    def isNameInOriginName(self ,_name):
        if self.GLOBAL_IDENTICALS_NAMES != None:
            for i in range(len(self.GLOBAL_IDENTICALS_NAMES)):
                if self.GLOBAL_IDENTICALS_NAMES[i].OrigName == _name:
                    return True, i
        return False, 0

    def isNameInDoubles(self, _name):
        if self.GLOBAL_IDENTICALS_NAMES != None:
            for i in range(len(self.GLOBAL_IDENTICALS_NAMES)):
                for j in range(len(self.GLOBAL_IDENTICALS_NAMES[i].DoublesNames)):
                    if self.GLOBAL_IDENTICALS_NAMES[i].DoublesNames[j] == _name:
                        return True, i, j
        return False, 0, 0
    
    def PropDicInallMapPropDic(self, CurName, SceneNodeNames):
        for ALP in SceneNodeNames:
            if CurName != ALP:
                if CurName.name == ALP.name:
                    b, pos = self.isNameInOriginName(_name= ALP.name)

                    d, pos2, pos3 = self.isNameInDoubles(_name= ALP)
                    e, pos4, pos4 = self.isNameInDoubles(_name= CurName)
                    if b:
                        if e == False:
                            if CurName not in self.GLOBAL_IDENTICALS_NAMES[pos].DoublesNames:
                                self.GLOBAL_IDENTICALS_NAMES[pos].DoublesNames.append(CurName)
                        if d == False:
                            if ALP not in self.GLOBAL_IDENTICALS_NAMES[pos].DoublesNames:
                                self.GLOBAL_IDENTICALS_NAMES[pos].DoublesNames.append(ALP)
                            
                    else:
                        if d == False and e == False:
                            doubleList = []
                            doubleList.append(ALP)
                            self.GLOBAL_IDENTICALS_NAMES.append(NamewDouble(str(CurName.name),doubleList))
    
    def _runSameNameNodeChecker(self):
        self.GLOBAL_IDENTICALS_NAMES = []
        self.sceneNodes = []
        self.sceneNodes = list(node.getAllNodes()) 
        
        for SN in self.sceneNodes:
            self.PropDicInallMapPropDic(CurName = SN, SceneNodeNames = self.sceneNodes)

        self.NameCopyTab.createTree(_nameDic= self.GLOBAL_IDENTICALS_NAMES)
    
    def _RenameTicked(self):
        checkedItems = self.NameCopyTab.getCheckedQTItem()
        for i in range(len(checkedItems)):
            if self.suffIncrComb.currentIndex() == 0:
                checkedItems[i].setText(1,"{0}".format(self.lineEdit.text()))
            if self.suffIncrComb.currentIndex() == 1:
                checkedItems[i].setText(1,"{0}_{1}".format(self.lineEdit.text(),i))
            if self.suffIncrComb.currentIndex() == 2:
                checkedItems[i].setText(1,"{0}_{1}:{2}:{3}".format(self.lineEdit.text(), time.gmtime()[4], time.gmtime()[5], datetime.datetime.now().microsecond))
            
            if self.KeepBaseName.isChecked():
                checkedItems[i].setText(2,"{0}{1}".format(checkedItems[i].text(0),checkedItems[i].text(1)))
            else:
                checkedItems[i].setText(2,"{0}".format(checkedItems[i].text(1)))

    def _DeleteTicked(self):
        checkedItems = self.NameCopyTab.getCheckedQTItem()
        for i in range(len(checkedItems)):
            checkedItems[i].setText(1,"")
            checkedItems[i].setText(2,"")
    
    def _ApplymodToScene(self):
        filledItems = self.NameCopyTab.getFilledQtitems()
        for i in range(len(filledItems)):
            node = self.NameCopyTab.getNodebyQTItem(filledItems[i])
            node.name = filledItems[i].text(2)
        qtUtils.popup("You have succefully renamed {0} nodes !".format(i+1))



            


def run():

    SameNameNodeChecker = MainWindow()
    if MAXVERSION() <= MAX2020:
        import MaxPlus
        MaxPlus.AttachQWidgetToMax(SameNameNodeChecker)
    SameNameNodeChecker.show()