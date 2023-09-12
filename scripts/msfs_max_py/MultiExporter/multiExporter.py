"""
Provides a UI to export multiple flight sim object type quickly

run() will create the window and connect it to max. 
"""

import os
import re
import uuid
import sys
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from maxsdk.globals import *
from maxsdk.node import *
from maxsdk.utility import *
from maxsdk.dialog import *
from maxsdk.layer import *
from maxsdk.perforce import *
from maxsdk.qtUtils import *
from maxsdk.sceneUtils import *
import maxsdk.userprop as userprop
from maxsdk.logger import LoggerWidget
from BabylonPYMXS import *
from MultiExporter.view import treeViewLayer
from MultiExporter.view import treeViewPreset
from MultiExporter.view import treeViewCategory
import MultiExporter.optionsMenu as optionsMenu
import MultiExporter.presetUtils as presetUtils
import MultiExporter.constants as constants
import MultiExporter.exporter as exporter
import MultiExporter.ui.mainwindow_ui as mainWindowUI
    
    

from pymxs import runtime as rt


import stat
if MAXVERSION() >= MAX2021:
    from configparser import ConfigParser, RawConfigParser
else:
    from ConfigParser import ConfigParser, RawConfigParser



class MainWindow(QMainWindow, mainWindowUI.Ui_MultiExporter):
    def __init__(self, parent=None):
        
        parent=QWidget.find(rt.windows.getMAXHWND())
        QMainWindow.__init__(self, parent)
        self.setWindowTitle("MultiExporter")
        
        ## MainWidget for the MainWindow
        self.mainWidget = QWidget()
        self.setCentralWidget(self.mainWidget)   
         
        self.setupUi(self.mainWidget)

        initialize()
        self.initUI()
        self.resize(1700, 900) 

    def initUI(self):
        self.optionsMenuWindow = None
        
        # buttons
        self.btnAddExport.pressed.connect(self._clickedAddExport)
        self.btnRemoveExport.pressed.connect(self._clickedRemoveExport)
       
        self.btnRefresh.pressed.connect(self.refreshTool)
        font = QFont()
        font.setPointSize(32)
        font.setWeight(75)
        font.setUnderline(False)
        font.setBold(False)
        self.btnRefresh.setFont(font)
        
        # self.btnRefresh.setText(u"\U0001F5D8")
        self.btnRefresh.setText("Refresh")
        self.btnRefresh.setToolTip("Refresh tool")
        self.tabWidget.currentChanged.connect(self._changedTab)
        self.btnConformLayers.pressed.connect(self._clickedConformLayers)
        self.btnAddPreset.pressed.connect(self._clickedAddPreset)
        self.btnRemovePreset.pressed.connect(self._clickedRemovePreset)
        self.btnDuplicatePreset.pressed.connect(self._clickedDuplicatePreset)
        self.btnApplyPresetLayer.pressed.connect(self._clickedApplyLayerSelection)
        self.btnEditPresetPath.pressed.connect(self._clickedEditPresetPath)
        self.btnAddGroup.pressed.connect(self._clickedAddPresetGroup)
        self.btnApplyPresetEdit.pressed.connect(self._clickedApplyPresetEdit)
        self.btnApplyPresetEdit.setEnabled(False)

        self.btnSavePresetConf.pressed.connect(self._clickedExportChekedPresetConf)
        self.btnImportPresetConf.pressed.connect(self._clickedImportPreset)
        
        self.presetParamName.returnPressed.connect(self._clickedApplyPresetEdit)
        self.config = ConfigParser()
        # export
        self.btnExportSelected.pressed.connect(self._clickedExportSelected)
        self.btnExportAll.pressed.connect(self._clickedExportAll)
        self.btnExportTicked.pressed.connect(self._clickedExportTicked)
        self.btnOpenExportFolder.pressed.connect(self._clickedOpenExportFolder)
        # lod view
        self.btnSetLODValues.pressed.connect(self._clickedSetLODValues)
        self.lodValue.returnPressed.connect(self._clickedSetLODValues)

        self.btnGenerateXML.pressed.connect(self._clickedGenerateXML)
        self.btnOptions.pressed.connect(self._openOptionsMenu)
        

        # LOD VIEW TREE CREATION
        self.verticalLayout_4.removeWidget(self.treeLODs)
        self.treeLODs.setHidden(True)
        self.treeLODs = treeViewCategory.TreeViewCategory(self.tab_3)
        self.treeLODs.setAlternatingRowColors(True)
        self.treeLODs.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.treeLODs.setIndentation(20)
        self.treeLODs.setObjectName("treeLODs")
        self.treeLODs.setColumnWidth(0, 450)
        self.treeLODs.setColumnWidth(1, 40)        
        self.treeLODs.setColumnWidth(2, 40)
        self.treeLODs.setColumnWidth(3, 40)
        self.treeLODs.setSortingEnabled(True)
        self.treeLODs.sortItems(0, Qt.SortOrder.AscendingOrder)
        self.treeLODs.header().setDefaultSectionSize(80)
        self.treeLODs.headerItem().setText(0, QApplication.translate("MultiExporter", "         Hierarchy", None, -1))
        self.treeLODs.headerItem().setText(1, QApplication.translate("MultiExporter", "LOD value", None, -1))
        self.treeLODs.headerItem().setText(2, QApplication.translate("MultiExporter", "Keep Instances", None, -1))
        self.treeLODs.headerItem().setText(3, QApplication.translate("MultiExporter", "Path", None, -1))
        self.verticalLayout_4.insertWidget(1, self.treeLODs)
        self.checkBoxLODModifier = qtUtils.createCheckBox(qtWidget=self.treeLODs)
        self.treeLODs.setGlobalCheckBox(self.checkBoxLODModifier)
        self.treeLODs.itemSelectionChanged.connect(self._selectionChangedLOD)
        self.cbObjectOptionPreset.setHidden(True)
        self.cbObjectOptionPreset = optionsMenu.ComboBoxOptionPreset(None, self.tab_3)
        self.cbObjectOptionPreset.setObjectName("cbObjectOptionPreset")
        self.cbObjectOptionPreset.setEditable(False)
        self.cbObjectOptionPreset.setMaximumWidth(130)
        self.cbObjectOptionPreset.setMinimumWidth(130)
        
        self.horizontalLayout_6.insertWidget(12,self.cbObjectOptionPreset)

        # PRESET VIEW TREE CREATION
        self.verticalLayout_3.removeWidget(self.treePresets)
        self.treePresets.setHidden(True)
        self.treePresets = treeViewPreset.TreeViewPreset(self.verticalLayoutWidget)
        self.treePresets.setEnabled(True)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.treePresets.sizePolicy().hasHeightForWidth())
        self.treePresets.setSizePolicy(sizePolicy)
        self.treePresets.setDragEnabled(True)
        self.treePresets.setDragDropMode(QAbstractItemView.DragDrop)
        self.treePresets.setDefaultDropAction(Qt.MoveAction)
        self.treePresets.setAlternatingRowColors(True)
        self.treePresets.setSortingEnabled(True)
        self.treePresets.sortItems(0, Qt.SortOrder.AscendingOrder)
        self.treePresets.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.treePresets.setObjectName("treePresets")
        self.treePresets.header().setDefaultSectionSize(40)
        self.treePresets.headerItem().setText(0, QApplication.translate("MultiExporter", "         Preset", None, -1))
        self.treePresets.headerItem().setText(1, QApplication.translate("MultiExporter", "Path", None, -1))
        self.verticalLayout_3.insertWidget(0, self.treePresets)
        self.treePresets.itemSelectionChanged.connect(self._selectionChangedPreset)
        self.cbOptionPreset.setHidden(True)
        self.cbOptionPreset = optionsMenu.ComboBoxOptionPreset(None,self.verticalLayoutWidget)
        self.cbOptionPreset.setObjectName("cbOptionPreset")
        self.cbOptionPreset.setEditable(False)
        self.cbOptionPreset.setMaximumWidth(130)
        self.cbOptionPreset.setMinimumWidth(130)
        self.horizontalLayout_8.insertWidget(4,self.cbOptionPreset)
        self.cbOptionPreset.activated.connect(self._clickedApplyPresetEdit)

        # LAYER VIEW TREE CREATION
        self.treeLayer.setHidden(True)
        self.verticalLayout_7.removeWidget(self.treeLayer)
        self.treeLayer = treeViewLayer.TreeViewLayer(self.verticalLayoutWidget_2)
        self.treeLayer.setAlternatingRowColors(True)
        self.treeLayer.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.treeLayer.setSortingEnabled(True)
        self.treeLayer.sortItems(0, Qt.SortOrder.AscendingOrder)
        self.treeLayer.setObjectName("treeLayer")
        self.treeLayer.headerItem().setText(0, QApplication.translate("MultiExporter", "         Layers", None, -1))
        self.verticalLayout_7.insertWidget(0, self.treeLayer)
        self.checkBoxLayerModifier = qtUtils.createCheckBox(qtWidget=self.treeLayer)
        # self.checkBoxLayerModifier.setTristate(True)
        self.treeLayer.setGlobalCheckBox(self.checkBoxLayerModifier)
        self.checkBoxPresetModifier = qtUtils.createCheckBox(qtWidget=self.treePresets)
        self.treePresets.setGlobalCheckBox(self.checkBoxPresetModifier)
        self.treeLayer.itemChanged.connect(self._changedLayerItem)

        self.btnLayerExpandAll.pressed.connect(self.treeLayer.expandAll)
        self.btnLayerCollapseAll.pressed.connect(self.treeLayer.collapseAll)

        self.btnPresetExpandAll.pressed.connect(self.treePresets.expandAll)
        self.btnPresetCollapseAll.pressed.connect(self.treePresets.collapseAll)
        
        self.filterBar.returnPressed.connect(self._clickedFilterItem)
        self.filterButton.pressed.connect(self._clickedFilterItem)


        # FILTER
        self.cbVisibleOnly.stateChanged.connect(self._changeCheckboxVisibility)
        self.cbIncludeLods.stateChanged.connect(self._changeCheckboxLODs)
        self.cbExportableOnly.stateChanged.connect(self._changeCheckboxExportable)

        # CREATE TREES AND INITIALIZE DATA
        self._changeCheckboxExportable()
        self._changeCheckboxLODs()
        self._changeCheckboxVisibility()
        self.lastEditedPreset = None
        self.treePresets.createTree()
        self.treeLODs.createTree()
        self.treeLayer.createTree()
        self._selectionChangedPreset()
        self._changedTab()
        self._refreshOptionPreset()

        #CustomPrivateMembers
        self.cancelEdit = False

        self.setFocus()
        # self.flagsOnTop = Qt.WindowFlags(Qt.WindowStaysOnTopHint)
        # self.flagswindNorm = Qt.WindowFlags(~Qt.WindowStaysOnTopHint)
        # self.setWindowFlags(self.flagsOnTop)
        self.installEventFilter(self)


        loggerWidget = LoggerWidget()
        self.loggerAreaVLayout.addWidget(loggerWidget)

        handler.emitter.logRecord.connect(loggerWidget.appendLogRecord)

    def _clickedFilterItem(self):
        text = self.filterBar.text()
        self.treeLODs.filterTree(filterr = text)

    def contextMenuEvent(self, event):
        r = self.tabWidget.geometry()
        if(r.contains(event.pos())):
            menu = QMenu(self)
            isLodView = self.getCurrentTree() == self.treeLODs
            isPresetView = self.getCurrentTree() == self.treePresets
            exportAction = menu.addAction("Export Selected")
            if(isLodView):
                generateXML = menu.addAction("Generate XML")
            if (isPresetView):
                rename = menu.addAction("Rename")
                addPreset = menu.addAction("Add Preset")
                addGroup = menu.addAction("Add Group")
                remove = menu.addAction("Remove Selected")
                duplicate = menu.addAction("Duplicate Selected")
            openFolder = menu.addAction("Open in Explorer")
            action = menu.exec_(self.mapToGlobal(event.pos()))
            if(isLodView):
                if action == generateXML:
                    self._clickedGenerateXML()
            if (isPresetView):
                if action == rename:
                    self.treePresets.startEditingSelectedItem()
                if action == addPreset:
                    self._clickedAddPreset()
                if action == addGroup:
                    self._clickedAddPresetGroup()
                if action == remove:
                    self._clickedRemovePreset()
                if action == duplicate:
                    self._clickedDuplicatePreset()
            if action == exportAction:
                self._clickedExportSelected()
            if action == openFolder:
                self._clickedOpenExportFolder()

    def _refreshOptionPreset(self):
        self.cbOptionPreset.refresh()
        self.cbObjectOptionPreset.refresh()


    def _openOptionsMenu(self):
        if (self.optionsMenuWindow == None):
            self.optionsMenuWindow = optionsMenu.OptionsMenu()
            self.optionsMenuWindow.show()
            self.optionsMenuWindow.onClosed.connect(lambda: self._closeOptionsMenu())
            self.optionsMenuWindow.onModifiedData.connect(lambda : self._refreshOptionPreset())
        else:
            self.optionsMenuWindow.activateWindow()

    def _closeOptionsMenu(self):
        self.optionsMenuWindow = None
        self.show()


    def _clickedConformLayers(self, prompt=True):
        self.conformSceneLayersToLODView(prompt=prompt)

    def _clickedGenerateXML(self, prompt=True):

        dlg = QMessageBox(self)
        dlg.setWindowTitle("Generate XML")
        dlg.setText("Do you want to generate an xml for a simobject ?")
        dlg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        dlg.setIcon(QMessageBox.Question)
        button = dlg.exec_()

        if button == QMessageBox.Yes:
            categories = self.treeLODs.getSelectedCategory()
            log = ""
            count = len(categories)
            i = 0
            if count > 0:
                self.progressBar.setRange(0, count)
                self.progressBar.setValue(0)
                for category in categories:
                    objects = self.treeLODs._baseNameDict[category]
                    objects = sortObjectsByLODLevels(objects)
                    metadataPath = exporter.getMetadataPath(objects[0])
                    if (metadataPath is None or metadataPath == ".xml"):
                        log += "\nERROR : No path on {0}. Skipping this XML file.".format(
                            objects[0].name)
                    else:
                        log += exporter.createLODMetadataForSimObject(metadataPath, objects)
                    i += 1
                    self.progressBar.setValue(i)
                if (log != ""):
                    print(log)
                    if prompt:
                        qtUtils.popup_scroll(title="XML Generation Ouput", text=log)
                        
        else:
        	categories = self.treeLODs.getSelectedCategory()
        	log = ""
        	count = len(categories)
        	i = 0
        if count > 0:
            self.progressBar.setRange(0, count)
            self.progressBar.setValue(0)
            for category in categories:
                objects = self.treeLODs._baseNameDict[category]
                objects = sortObjectsByLODLevels(objects)
                metadataPath = exporter.getMetadataPath(objects[0])
                if (metadataPath is None or metadataPath == ".xml"):
                    log += "\nERROR : No path on {0}. Skipping this XML file.".format(
                        objects[0].name)
                else:
                    log += exporter.createLODMetadata(metadataPath, objects)
                i += 1
                self.progressBar.setValue(i)
            if (log != ""):
                print(log)
                if prompt:
                    qtUtils.popup_scroll(title="XML Generation Ouput", text=log)

    def _clickedAddPresetGroup(self):
        newGroup = presetUtils.createNewGroup()
        presets = self.treePresets.getSelectedPresets()
        if len(presets) > 0:
            for preset in presets:
                preset.edit(group=newGroup.identifier)
        self.refreshTool()
        self.treePresets.startEditingItemWithGroupID(newGroup.identifier)

    def _clickedAddPreset(self,forcedPath=None):
        groups = self.treePresets.getSelectedGroups()
        groupID = None
        if (len(groups) > 0):
            groupID = groups[0].identifier
        if forcedPath is None:
            filePath = presetUtils.askForNewPath("Create New Preset")
        else:
            filePath = convertAbsolutePathToRelative(forcedPath, rt.pathConfig.getCurrentProjectFolder())
        if(filePath != None):
            presetName = os.path.split(filePath)[1]
            presetName = os.path.splitext(presetName)[0]
            presetUtils.createNewPreset(
                presetName, group=groupID, filePath=filePath)
            self.refreshTool()
    
    def _clickedExportChekedPresetConf(self):
        currentTree = self.getCurrentTree()
        if (currentTree == self.treePresets):
            selected = self.treePresets.getCheckedPresets()
            _filePath = qtUtils.openSaveFileNameDialog(caption="Export preset config location",  _filter= "MEP(*.mep)", _dir="", forcedExtension=".mep")
            if(len(selected) > 0 and _filePath != None):
                for i in range(len(selected)):
                    PrsObjDic = {}
                    for POK in dir(selected[i]):
                        ExculeList = ["_load","_write","create","delete","edit","get"]
                      
                        if MAXVERSION() >= MAX2021:
                            if POK not in ExculeList and "__" not in POK and isinstance(getattr(selected[i],POK), str):
                                PrsObjDic[POK] = getattr(selected[i],POK)
                                #print("{0} = {1}".format(POK,PrsObjDic[POK]))
                        else:
                            if POK not in ExculeList and "__" not in POK and (isinstance(getattr(selected[i],POK), str) or isinstance(getattr(selected[i],POK), unicode)):
                                PrsObjDic[POK] = getattr(selected[i],POK)
                                #print("{0} = {1}".format(POK,PrsObjDic[POK]))
                        
                        if POK not in ExculeList and "__" not in POK and isinstance(getattr(selected[i],POK), list):
                            ListinStr = ""
                            lst = getattr(selected[i],POK)
                            for j in range(len(lst)):
                                if j == 0:
                                    ListinStr = "{0}".format(lst[j])
                                else:
                                    ListinStr = "{0},{1}".format(ListinStr,lst[j])
                            PrsObjDic[POK] = ListinStr

                    
                    #Debug What will be serialized
                    for objs in PrsObjDic:
                        print("{0} = {1}".format(objs,PrsObjDic[objs]))
                    if i == 0:
                        self.writeExportPresetsCFG(presetName = selected[i].identifier, _PrsObjDic = PrsObjDic, filepath = _filePath, needReset= True)
                    else:
                        self.writeExportPresetsCFG(presetName = selected[i].identifier, _PrsObjDic = PrsObjDic, filepath = _filePath, needReset= False)

                        
    def writeExportPresetsCFG(self, presetName ="PresetConfig", _PrsObjDic = None, filepath = os.path.join(rt.pathConfig.getCurrentProjectFolder(),"MultiExporter.mep"), needReset = False):
        if needReset == True:
            for configs in self.config.sections():
                self.config.remove_section(configs)

        if len(_PrsObjDic) > 0:        
            if MAXVERSION() >= MAX2021:
                self.config[presetName] = {}
                PresetConfig = self.config[presetName]
                for Pobjs in _PrsObjDic:
                    PresetConfig[Pobjs] = _PrsObjDic[Pobjs]
            else:
                if self.config.has_section(presetName):
                    self.config.remove_section(presetName)            
                self.config.add_section(presetName)
                for Pobjs in _PrsObjDic:
                    self.config.set(presetName, Pobjs, _PrsObjDic[Pobjs])
                
            #UpdateFile
            if os.path.isfile(filepath):
                os.chmod(filepath, stat.S_IWRITE)
            with open(filepath, 'w') as configFile:
                self.config.write(configFile)

    def getPresetsCFG(self, filepath = os.path.join(rt.pathConfig.getCurrentProjectFolder(),"MultiExporter.mep")): #
        OutPresList = []
        for configs in self.config.sections():
            self.config.remove_section(configs)
        self.config.read(filepath)
        for sec in self.config.sections():
            OutPresetDic = {}
            for (key, val) in self.config.items(sec):
                OutPresetDic[key] = val
            OutPresList.append(OutPresetDic)

        return OutPresList

    def _clickedImportPreset(self):
        _filePath = qtUtils.openSaveFileNameDialog(caption="Import preset configuration",  _filter= "MEP(*.mep)", _dir="", forcedExtension=".mep")
        presetList = self.getPresetsCFG(filepath = _filePath)
        for preset in presetList:
            name = ""
            LayerNames = []
            path = ""
            missingLayers = []
            #Prepare Data For Preset Creation
            for param in preset:
                if param == "name":
                    name = preset[param]
                if param == "layernames":
                    LayerNames = preset[param].split(",")
                if param == "path":
                    path = preset[param]
            
            #CheckforSceneIncompatibility
            for strLay in LayerNames:
                lay = layer.get_layer(strLay)
                if lay == None:
                    missingLayers.append(strLay)
            if len(missingLayers) > 0:
                misLayString = ""
                for i in range(len(missingLayers)):
                    if i == 0:
                        misLayString = missingLayers[i]
                    else:
                        misLayString = "{0}, {1}".format(misLayString, missingLayers[i])
                qtUtils.popup("Your scene configuration does not match with the preset you are trying to import (Layers: {0} are missing)".format(misLayString), title="Preset Import Error")
                return
            #CreatenewPreset
            newPreset = presetUtils.createNewPreset(labelName = name, group=None, filePath=path)
            newPreset.edit(layerNames=LayerNames)
        
        self.refreshTool()
        

    def _clickedRemovePreset(self, prompt=True):
        groups = self.treePresets.getSelectedGroups()
        presets = self.treePresets.getSelectedPresets()
        for group in groups:
            childs = self.treePresets.getPresetsFromGroup(group)
            for child in childs:
                presets.append(child)
        presetUtils.confirmAndRemove(presets=presets, groups=groups, prompt=prompt)
        self.refreshTool()
        
    def _clickedDuplicatePreset(self):
        groups = self.treePresets.getSelectedGroups()
        presets = self.treePresets.getSelectedPresets()
        groupTransfer = dict()
        for group in groups:
            oldId = group.identifier
            newGroup = presetUtils.createNewGroup(groupName=group.name, optionPreset=group.optionPreset)
            newId = newGroup.identifier
            groupTransfer[oldId] = newId
            childs = self.treePresets.getPresetsFromGroup(group)
            for child in childs:
                presets.append(child)
        if presets != None:
            r = qtUtils.popup_Yes_No(text="You have pending preset to duplicate. Give them a common new path ?", title="Same root path ?")
            if r:
                initDir = os.path.split(presetUtils.getAbsoluteExportPath(presets[0]))[0]
                expPathRoot = ""
                while expPathRoot == "":
                    expPathRoot = qtUtils.openSaveFolderPathDialog(_caption="Common Export Path for Duplication ", _dir=initDir)
            for preset in presets:            
                targetGroup = preset.group
                if targetGroup in groupTransfer:
                    targetGroup = groupTransfer[targetGroup]
                filepath = preset.path
                if r:
                    tempStringPathArrey = filepath.split("\\")
                    filename = tempStringPathArrey[len(tempStringPathArrey)-1]
                    filepath = os.path.join(expPathRoot,filename)

                presetUtils.createNewPreset(labelName=preset.name, group=targetGroup, filePath=filepath, layerNames=preset.layerNames)
            
        self.refreshTool()



    def _changedTab(self):
        currentTab = self.tabWidget.currentIndex()
        isLODView = currentTab == 0
        isPresetView = currentTab == 1
        self.btnGenerateXML.setEnabled(isLODView)
        self.btnAddExport.setEnabled(isLODView)
        self.btnRemoveExport.setEnabled(isLODView)

    def _clickedOpenExportFolder(self):
        currentTree = self.getCurrentTree()
        exportPath = None
        if(currentTree == self.treeLODs):
            selected = self.getCurrentlySelectedRootList()
            if(len(selected) > 0):
                exportPath = exporter.getAbsoluteExportPath(selected[0])
        elif (currentTree == self.treePresets):
            selected = self.treePresets.getSelectedPresets()
            if (len(selected) > 0):
                exportPath = presetUtils.getAbsoluteExportPath(selected[0])
        if exportPath is not None:
            try:
                exportPath = os.path.split(exportPath)[0]
                os.startfile(exportPath)
            except WindowsError as err:
                qtUtils.popup(title="WindowsError", text=err.strerror)

    def _changeCheckboxExportable(self):
        state = self.cbExportableOnly.checkState() == Qt.Checked
        self.treeLODs._showOnlyExportable = state
        self.treeLayer._showOnlyExportable = state
        self.refreshTool()

    def _changeCheckboxLODs(self):
        state = self.cbIncludeLods.checkState() == Qt.Checked
        self.treeLODs._showOnlyLODs = state
        self.treeLayer._showOnlyLODs = state
        self.refreshTool()

    def _changeCheckboxVisibility(self):
        state = self.cbVisibleOnly.checkState() == Qt.Checked
        self.treeLODs._showOnlyVisible = state
        self.treeLayer._showOnlyVisible = state
        self.refreshTool()

    def _clickedEditPresetPath(self):
        selected = self.treePresets.getSelectedPresets()
        presetUtils.addExportPathToPresets(selected)
        for i in range(len(selected)):
            iD = selected[i].identifier
            self.treePresets.resfreshQtItemFromID(id = iD, cObj = selected[i])

    def _changedLayerItem(self):
        selected = self.treePresets.getSelectedPresets()
        if (len(selected) == 1 and self.cancelEdit == False):
            self.lastEditedPreset = selected[0]
            self.treeLayer.isEdited = True
            self.btnApplyPresetLayer.setText("Apply*")

    def _selectionChangedPreset(self):
        groups = self.treePresets.getSelectedGroups()
        if (self.treeLayer.isEdited):
            if(self.lastEditedPreset):
                if (qtUtils.popup_Yes_No(
                        title="Apply Unsaved Changes ?",
                        text="You have unsaved changes on a preset, do you want to apply them now ?")
                    ):
                    layerSelection = self.treeLayer.getCheckedLayerNames()
                    self.applyLayerSelectionToPreset(
                        self.lastEditedPreset, layerSelection)
        if (len(groups) == 1):
            self.treeLayer.setEnabled(False)
            self.presetParamName.setText(groups[0].name)
            optionPresetId = self.cbOptionPreset.getOptionPresetIndexByIdentifier(groups[0].optionPreset)
            if optionPresetId is not None:                
                self.cbOptionPreset.setCurrentIndex(optionPresetId)
            else:
                self.cbOptionPreset.setCurrentIndex(0)
            self.treeLayer.uncheckAllLayers()
            return
        presets = self.treePresets.getSelectedPresets()
        if (len(presets) == 1):
            self.treeLayer.setEnabled(True)
            preset = presets[0]
            optionPreset = self.treePresets.joinOptionsToPresets([preset])[0][1] # create 1 length list, pass through function and get first result and first index of the tuple      
            layerNames = preset.layerNames
            self.treeLayer.intializeCheckLayers(layerNames)
            if len(self.treeLayer.getPartCheckedLayerNames()) == 0:
                checkedItem = self.treeLayer.getCheckedLayer()
                self.cancelEdit = True
                for ci in checkedItem:
                    self.treeLayer._changedWidgetItem(widget=ci, col=0)
                self.cancelEdit = False

            self.btnApplyPresetLayer.setText("Apply")
            self.presetParamName.setText(str(preset.name))
            paramDict = optionPreset.get()[1]
            exportedSelectionBehaviour = "babylonjs_mergecontainersandxref" in paramDict.keys() and paramDict["babylonjs_mergecontainersandxref"] == True
            self.treeLayer.setExportedSelectionBehaviour(exportedSelectionBehaviour)
        else:
            self.treeLayer.uncheckAllLayers()
            self.treeLayer.setEnabled(False)
            self.presetParamName.setText("-")

    def _clickedApplyPresetEdit(self):
        groups = self.treePresets.getSelectedGroups()
        txt = self.presetParamName.text()
        optionIndex = self.cbOptionPreset.currentIndex()
        if(len(groups) >= 1):
            self.treeLayer.setEnabled(False)
            optionPreset = self.cbOptionPreset.itemData(optionIndex)
            for group in groups:
                if optionIndex > -1:                        
                    group.edit(optionPreset=optionPreset.identifier)
                if txt != "-":
                    group.edit(name=txt)            
        else:
            ## TODO -- See if this is useless
            selectedPresets = self.treePresets.getSelectedPresets()
            if(len(selectedPresets) > 0):
                rt.messageBox("Option presets are applied to groups, please select a group.")
            for preset in selectedPresets:
                preset.edit(name=txt)
        self.refreshTool()

    def _clickedApplyLayerSelection(self):
        presets = self.treePresets.getSelectedPresets()
        if (len(presets) == 1):
            checkedLayers = self.treeLayer.getCheckedLayerNames()
            self.applyLayerSelectionToPreset(presets[0], checkedLayers)

    def applyLayerSelectionToPreset(self, preset, layerNames):
        r = qtUtils.popup_Yes_No(title="Apply Unsaved Changes ?",text="You need to save the scene to apply")
        baseFile = rt.maxFilePath + rt.maxFileName
        if r:
            preset.edit(layerNames=layerNames)
            self.btnApplyPresetLayer.setText("Apply")
            self.treeLayer.isEdited = False
            if baseFile != None:
                s = rt.saveMaxFile(baseFile)
                if s == False:
                    rt.messageBox("Save failed, choose another path, or checkout your file.")
                    f = rt.getSaveFileName(caption="Save as", filename=baseFile)
                    while f == None:
                        f = rt.getSaveFileName(caption="Save as", filename=baseFile)
                    rt.saveMaxFile(f) if f != None else rt.messageBox("Save failed")                      
                else:
                    print("successfully saved the scene ")
            else:
                while f == None:
                    f = rt.getSaveFileName(caption="Save as", filename=baseFile)
                rt.saveMaxFile(f) if f != None else rt.messageBox("Save failed")

    def _selectionChangedLOD(self):
        selected = self.treeLODs.getSelectedRootList()
        lodValue = None
        if(len(selected) == 1):
            lodValue = rt.getUserProp(selected[0], constants.PROP_LOD_VALUE)
            if(lodValue is not None):
                self.lodValue.setText(str(lodValue))
            else:
                self.lodValue.setText("-")
            keepInstances = rt.getUserProp(selected[0], constants.PROP_KEEP_INSTANCES)
            if (keepInstances is not None):
                self.cbKeepInstances.setCheckState(Qt.Checked if keepInstances else Qt.Unchecked)
            else:
                self.cbKeepInstances.setCheckState(Qt.Unchecked)
        else:
            self.lodValue.setText("-")
            self.cbKeepInstances.setCheckState(Qt.PartiallyChecked)


    def _clickedSetLODValues(self):
        lods = self.treeLODs.getSelectedRootList()
        for lod in lods:
            lodValueChoice = self.lodValue.text()
            if(lodValueChoice != "-"):
                validValue = qtUtils.validateFloatLineEdit(lodValueChoice)
                if(validValue):
                    userprop.setUserProp(
                        lod, constants.PROP_LOD_VALUE, validValue)
                
            keepInstances = self.cbKeepInstances.checkState()
            if (keepInstances != Qt.PartiallyChecked):
                keepInst = True if keepInstances == Qt.Checked else False
                userprop.setUserProp(lod, constants.PROP_KEEP_INSTANCES, keepInst)
                
        self.refreshTool()

    def _clickedExportTicked(self):
        currentTree = self.getCurrentTree()
        if(currentTree == self.treeLODs):
            selected = self.getCurrentlyCheckedRootList()
            self.sendToExporter(selected)
        if (currentTree == self.treePresets):
            selected = self.treePresets.getCheckedPresetsWithOption()
            self.sendPresetsWithOptionsToExporter(selected)

    def _clickedExportSelected(self):
        currentTree = self.getCurrentTree()
        if(currentTree == self.treeLODs):
            selected = self.getCurrentlySelectedRootList()
            self.sendToExporter(selected)
        elif (currentTree == self.treePresets):
            #presets = self.treePresets.getSelectedPresetsAndGroupsContent()
            presetsAndOptions = self.treePresets.getSelectedPresetsAndGroupsContentWithOption()
            self.sendPresetsWithOptionsToExporter(presetsAndOptions)
            #self.sendPresetsToExporter(presets)

    def _clickedAddExport(self, forcedPath = None, prompt=True):
        selected = getSelectedObjects()
        exporter.addExportPathToObjects(selected,forcedPath=forcedPath,prompt=prompt)
        self.refreshTool()

    def _clickedRemoveExport(self, prompt=True):
        selected = getSelectedObjects()
        exporter.removeExportPathToObjects(selected,prompt=prompt)
        self.refreshTool()

    def _clickedExportAll(self,prompt=True):
        currentTree = self.getCurrentTree()
        if(currentTree == self.treeLODs):
            fullList = self.getCurrentFullList()
            self.sendToExporter(fullList, prompt=prompt)
        elif (currentTree == self.treePresets):
            fullList = self.treePresets.getAllPresetsListWithOption()
            self.sendPresetsWithOptionsToExporter(fullList, prompt=prompt)

    def refreshTool(self):
        tree = self.getCurrentTree()
        if(tree == self.treePresets):
            self.treeLayer.refreshTree()
        tree.refreshTree()
        self._refreshOptionPreset()

    def getCurrentTree(self):
        currentTab = self.tabWidget.currentIndex()
        if (currentTab == 0):
            return self.treeLODs
        if (currentTab == 1):
            return self.treePresets
        if (currentTab == 2):
            return self.treeAnimation

    def getCurrentFullList(self):
        fullList = []
        tree = self.getCurrentTree()
        if(tree):
            fullList = tree.getAllRootsList()
        return fullList

    def getCurrentlySelectedRootList(self):
        selected = []
        tree = self.getCurrentTree()
        if(tree):
            selected = tree.getSelectedRootList()
        return selected

    def getCurrentlyCheckedRootList(self):
        selected = []
        tree = self.getCurrentTree()
        if(tree):
            selected = tree.getCheckedRootList()
        return selected

    def conformSceneLayersToLODView(self,prompt=True):
        if(self.getCurrentTree() != self.treeLODs):
            return
        if(prompt==True):
            if(not qtUtils.popup_Yes_No(
                title="Conform",
                text="""Conforming the scene layers to the LOD View will destroy all your layers and create a hierarchy of layers reflecting the LOD View object list. It will put all the other objects in the default layer. This is optional.\n
                Are you really sure you want to do this ?""")):
                return
        conformSceneLayersToTemplate(self.treeLODs._baseNameDict)


    def sendToExporter(self, objects,prompt=True):
        count = len(objects)
        log = ""
        optionPreset = self.cbObjectOptionPreset.itemData(self.cbObjectOptionPreset.currentIndex())
        if(count > 0):
            exporter.exportObjects(objects, optionPreset, prompt=prompt)
            
    def checkoutGLTF(self,gltfPath):
        extensionLessPath = os.path.splitext(gltfPath)[0]
        P4edit(extensionLessPath + ".bin")
        P4edit(extensionLessPath + ".gltf")

    def checkForDuplUniqueIDs(self, _presetsAndOptions):
        for preset, optionPreset in _presetsAndOptions:
            nodesconc = getNodesFromPresetObject(preset)
            isDouble, doubleList = is_double_unique_ID(nodesconc)
            if isDouble:
                finalText = ""
                for i in range(len(doubleList)):
                    nodesList = ""
                    for nd in range(len(doubleList[i].Nodes)):
                        if nd == 0:
                            nodesList = "{0}".format(doubleList[i].Nodes[nd])
                        else:
                            nodesList = "{0}, {1}".format(nodesList,doubleList[i].Nodes[nd] )
                    if i == 0:
                        finalText = "{0} are sharing the same Unique id : {1}".format(nodesList, doubleList[i].UniqueID)
                    else:
                        finalText = "{0} || {1} are sharing the same Unique id : {2}".format(finalText,nodesList, doubleList[i].UniqueID)
                    print("{0} are sharing the same Unique id : {1}".format(nodesList, doubleList[i].UniqueID))
                
                r = qtUtils.popup_Yes_No("{0}. This export might generate RPT errors, continue anyway ?".format(finalText), title="There are errors in your export configuration !")
                return r
                
    def sendPresetsWithOptionsToExporter(self, presetsAndOptions, prompt=True):
        '''
        in : presetsAndOptions = list(tuple(PresetObject,OptionPresetObject))
        '''
        count = len(presetsAndOptions)
        if (count < 0):
            return        
        # if self.checkForDuplUniqueIDs(_presetsAndOptions = presetsAndOptions) == False:
        #     return
        exportParametersWithNoSceneModifications = []
        exportParametersWithSceneModifications = []
        for preset, optionPreset in presetsAndOptions:
            assetFilePath = convertRelativePathToAbsolute(preset.path, rt.pathConfig.getCurrentProjectFolder())
            ##Log
            
            param = BabylonParameters(assetFilePath, "gltf")
            if optionPreset != None:
                param = applyOptionPresetToBabylonParam(optionPreset, param)
                param.exportLayers = preset.layerNames
            else:
                rt.messageBox("There is no option preset applied to this group, please select one.")
                return
            

            try:
                relativeTextureFolder = param.textureFolder[1:] if (param.textureFolder[:1] == "\\") else param.textureFolder
                param.textureFolder = convertRelativePathToAbsolute(relativeTextureFolder, rt.pathConfig.getCurrentProjectFolder())
            except Exception as error:
                print ("Error resolving texturePath")
                print(error)
            if param.usePreExportProcess:
                exportParametersWithSceneModifications.append(param)
            else:
                exportParametersWithNoSceneModifications.append(param)
        
        if len(exportParametersWithSceneModifications) > 0:
            rt.holdMaxFile()
            success = runPreExportProcess()
            if success:
                for exp in exportParametersWithSceneModifications:
                    runBabylonExporter(exp)
                    self.checkoutGLTF(exp.outputPath)
                    ## TODO check if this causes viewport conf
                if not param.applyPreprocessToScene:
                    rt.fetchMaxFile(quiet = True)
            else:
                rt.fetchMaxFile(quiet = True)
            
        
        for exp in exportParametersWithNoSceneModifications:
            runBabylonExporter(exp)
            self.checkoutGLTF(exp.outputPath)

        self.refreshTool()

################################
##### ROOT DEBUG FUNCTION ######
################################




def _printRootNodeProperties():
    rootNode = getSceneRootNode()
    print(userprop.getUserPropBuffer(rootNode))


def _cleanupProp(prop):
    rootNode = getSceneRootNode()
    userprop.removeUserProp(rootNode, prop)

def _cleanupRootNodeProperties():
    rootNode = getSceneRootNode()
    userprop.setUserPropBuffer(rootNode, "")  # CLEANUP ROOT NODE PROPERTIES
    print("Root node user properties wiped")
################################
###### OPENING PROCEDURES ######
################################

def convertBabylonMultiExporterData():
    log = ""
    root = getSceneRootNode()
    print("Converting")
    if userprop.getUserProp(root,"babylonjs_ExportItemListBackup") is None: # Only convert if we didn't before
        exportItemList = userprop.getUserPropList(root, "babylonjs_ExportItemList")
        rawExportItemList = userprop.getUserProp(root, "babylonjs_ExportItemList")
        if exportItemList is not None:
            for exportItem in exportItemList:
                try:
                    itemProp = userprop.getUserProp(root, exportItem)
                    itemProp = str(itemProp).replace(";;", ";-;")
                    item = userprop.parseUserPropAsList(itemProp)
                    if (item is not None):
                        expPath = item[1]
                        serialLayers = item[3]
                        print(serialLayers)
                        layerNames = [x for x in item[3].split("~")]
                        absPath = convertRelativePathToAbsolute(expPath, rt.maxfilepath)
                        relPath = convertAbsolutePathToRelative(absPath, rt.pathConfig.getCurrentProjectFolder())
                        presetName = os.path.splitext(os.path.split(relPath)[1])[0]
                        presetUtils.createNewPreset(presetName, None, relPath, layerNames)
                        log += "{0}\n".format(presetName)
                except Exception as error:
                    log += "Couldn't convert " + exportItem + " of the path because " + error
                    print(error)
            # Uncomment if you want to destroy the original Babylon Preset
            userprop.setUserProp(root, "babylonjs_ExportItemListBackup", rawExportItemList)
            # userprop.removeUserProp(root, "babylonjs_ExportItemList")
    return log


def updateObsoleteExportPath():
    log = ""
    roots = getAllRoots(getAllObjects())
    for r in roots:
        oldPath = userprop.getUserProp(r, constants.PROP_OLD_EXPORT_PATH)
        newPath = userprop.getUserProp(r, constants.PROP_EXPORT_PATH)
        if oldPath is not None and newPath is None:
            newPath = convertRelativePathToAbsolute(
                oldPath, rt.maxFilePath)
            newPath = convertAbsolutePathToRelative(
                newPath, rt.pathConfig.getCurrentProjectFolder())
            userprop.setUserProp(r, constants.PROP_EXPORT_PATH, newPath)
            log += "{0}\n".format(r.name)
    return log


def writeDefaultBabylonParametersInRootNode():
    sceneRoot = getSceneRootNode()
    for prop in propertyToDefault.keys():
        value = userprop.getUserProp(
            sceneRoot, prop, propertyToDefault[prop])
        userprop.setUserProp(sceneRoot, prop, value)


def checkSavedMaxFilePath():  # UNUSED
    sceneRoot = getSceneRootNode()
    if rt.maxFilePath == "" or rt.maxFilePath is None:
        qtUtils.popup(title="Scene File is not saved.",
                      text="You need to save your Max scene to use the exporter.")
        return False
    savedFilePath = userprop.getUserProp(
        sceneRoot, constants.PROP_SAVED_MAXFILE_PATH)
    if (savedFilePath is None):
        userprop.setUserProp(
            sceneRoot, constants.PROP_SAVED_MAXFILE_PATH, rt.maxFilePath)
        return True
    else:
        if (savedFilePath != rt.maxFilePath):
            qtUtils.popup(
                title="Max File path changed",
                text="The scene .max file path changed since last time you used the Multi-Exporter.\n\n"
                "If you changed the path of your Max file please make sure all the export path in the Multi-Exporter are still correct.\n\n"
                "NOTE : This can be caused by having different workspaces working on the same file, "
                "it will not be a problem if the .max file didn't change relative to the project.\n\n"
                "If you didn't change the Max file path please ignore this message."
            )
            userprop.setUserProp(
                sceneRoot, constants.PROP_SAVED_MAXFILE_PATH, rt.maxFilePath)
            return True
        else:
            return True

def checkIfContainerUnloaded():
    cont = get_all_containers()
    for c in cont:
        if c.unloaded == True:
            r = rt.queryBox("You have unloaded containers in your scene, you must load them all to export correctly, load them automaticly ?")
            if r :
                load_all_containers()
            break

def convertOldScene(skip_conversion=False,prompt = False):
    if not skip_conversion:
            log = None
            try:
                log = updateObsoleteExportPath()
            except Exception as error:
                print ("impossible to convert old format")
                print(error)
            if log and log != "" and prompt:
                qtUtils.popup_scroll(
                    title="Updated Export Path",
                    text="Update export path property keyword of following objects : {0}".format(
                        log)
                )
            try:
                log = convertBabylonMultiExporterData()
                if log != "" and prompt:
                    qtUtils.popup_scroll(
                        title="Updated Multi Exporter Presets",
                        text="Converted the babylon export entries to work with the MultiExporter : {0}".format(
                            log)
                    )
            except Exception as error:
                print(error)

def initialize(prompt=True, skip_conversion=False):
        writeDefaultBabylonParametersInRootNode()
        checkIfContainerUnloaded()
        #lpierabella: 
        # I prefer to removed the conversion as it is there since a lot of time and maybe we do not need it anymore
        # It is also impacting loafing time
        # eventually we could move the conversion to a separate tool if required in the future
        # convertOldScene(skip_conversion) 
        initializeBabylonExport()
        
window = None

def show():
    global window
    window = MainWindow()
    window.show()
