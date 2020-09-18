"""
Provides a UI to export multiple flight sim object type quickly

run() will create the window and connect it to max. 
"""

import os
import re
import sys
import uuid

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from maxsdk.globals import *
import BabylonPYMXS

from MultiExporter import optionsMenu, presetUtils,treeView,constants,exporter
import MultiExporter.ui.mainwindow_ui as mainWindowUI

from maxsdk import dialog as sdkdialog
from maxsdk import layer
from maxsdk import perforce as sdkperforce
from maxsdk import qtUtils, sceneUtils, userprop, utility
from pymxs import runtime as rt


class MainWindow(QWidget, mainWindowUI.Ui_MultiExporter):
    def __init__(self):
        QWidget.__init__(self)
        self.setupUi(self)
        self.optionsMenuWindow = None
        # buttons
        self.btnAddExport.pressed.connect(lambda: self._clickedAddExport())
        self.btnRemoveExport.pressed.connect(
            lambda: self._clickedRemoveExport())
        self.btnRefresh.pressed.connect(lambda: self.refreshTool())
        font = QFont()
        font.setPointSize(32)
        font.setWeight(75)
        font.setUnderline(False)
        font.setBold(False)
        self.btnRefresh.setFont(font)
        self.btnRefresh.setText(u"\U0001F5D8")
        self.tabWidget.currentChanged.connect(lambda: self._changedTab())
        self.btnConformLayers.pressed.connect(
            lambda: self._clickedConformLayers())
        self.btnAddPreset.pressed.connect(lambda: self._clickedAddPreset())
        self.btnRemovePreset.pressed.connect(lambda: self._clickedRemovePreset())
        self.btnDuplicatePreset.pressed.connect(self._clickedDuplicatePreset)
        self.btnApplyPresetLayer.pressed.connect(lambda: self._clickedApplyLayerSelection())
        self.btnEditPresetPath.pressed.connect(lambda: self._clickedEditPresetPath())
        self.btnAddGroup.pressed.connect(lambda: self._clickedAddPresetGroup())
        self.btnApplyPresetEdit.pressed.connect(lambda: self._clickedApplyPresetEdit())
        
        self.presetParamName.returnPressed.connect(lambda: self._clickedApplyPresetEdit())
        # export
        self.btnExportSelected.pressed.connect(
            lambda: self._clickedExportSelected())
        self.btnExportAll.pressed.connect(lambda: self._clickedExportAll())
        self.btnExportTicked.pressed.connect(
            lambda: self._clickedExportTicked())
        self.btnOpenExportFolder.pressed.connect(
            lambda: self._clickedOpenExportFolder())
        # lod view
        self.btnSetLODValues.pressed.connect(
            lambda: self._clickedSetLODValues())
        self.btnGenerateXML.pressed.connect(lambda: self._clickedGenerateXML())
        self.btnOptions.pressed.connect(lambda: self._openOptionsMenu())
        

        # LOD VIEW TREE CREATION
        self.verticalLayout_4.removeWidget(self.treeLODs)
        self.treeLODs.setHidden(True)
        self.treeLODs = treeView.TreeViewCategory(self.tab_3)
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
        self.treeLODs.headerItem().setText(2, QApplication.translate("MultiExporter", "Flatten", None, -1))
        self.treeLODs.headerItem().setText(3, QApplication.translate("MultiExporter", "Keep Instances", None, -1))
        self.treeLODs.headerItem().setText(4, QApplication.translate("MultiExporter", "Path", None, -1))
        self.verticalLayout_4.insertWidget(1, self.treeLODs)
        self.checkBoxLODModifier = qtUtils.createCheckBox(qtWidget=self.treeLODs)
        self.treeLODs.setGlobalCheckBox(self.checkBoxLODModifier)
        self.treeLODs.itemSelectionChanged.connect(lambda: self._selectionChangedLOD())
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
        self.treePresets = treeView.TreeViewPreset(self.verticalLayoutWidget)
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
        self.treePresets.itemSelectionChanged.connect(lambda: self._selectionChangedPreset())
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
        self.treeLayer = treeView.TreeViewLayer(self.verticalLayoutWidget_2)
        self.treeLayer.setAlternatingRowColors(True)
        self.treeLayer.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.treeLayer.setSortingEnabled(True)
        self.treeLayer.sortItems(0, Qt.SortOrder.AscendingOrder)
        self.treeLayer.setObjectName("treeLayer")
        self.treeLayer.headerItem().setText(0, QApplication.translate("MultiExporter", "         Layers", None, -1))
        self.verticalLayout_7.insertWidget(0, self.treeLayer)
        self.checkBoxLayerModifier = qtUtils.createCheckBox(qtWidget=self.treeLayer)
        self.treeLayer.setGlobalCheckBox(self.checkBoxLayerModifier)
        self.checkBoxPresetModifier = qtUtils.createCheckBox(qtWidget=self.treePresets)
        self.treePresets.setGlobalCheckBox(self.checkBoxPresetModifier)
        self.treeLayer.itemChanged.connect(lambda: self._changedLayerItem())
        self.treePresets.hasChanged.connect(lambda: self._droppedPresetWidget())

        self.btnLayerExpandAll.pressed.connect(self.treeLayer.expandAll)
        self.btnLayerCollapseAll.pressed.connect(self.treeLayer.collapseAll)
        
        # FILTER
        self.cbVisibleOnly.stateChanged.connect(lambda: self._changeCheckboxVisibility())
        self.cbIncludeLods.stateChanged.connect(lambda: self._changeCheckboxLODs())
        self.cbExportableOnly.stateChanged.connect(lambda: self._changeCheckboxExportable())

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
            if action == exportAction:
                self._clickedExportSelected()
            if action == openFolder:
                self._clickedOpenExportFolder()

    def _refreshOptionPreset(self):
        self.cbOptionPreset.refresh()
        self.cbObjectOptionPreset.refresh()


    def _openOptionsMenu(self):
        if (self.optionsMenuWindow == None):
            self.optionsMenuWindow = optionsMenu.run()
            self.optionsMenuWindow.onClosed.connect(
                lambda: self._closeOptionsMenu())
            self.optionsMenuWindow.onModifiedData.connect(lambda : self._refreshOptionPreset())
        else:
            self.optionsMenuWindow.activateWindow()

    def _closeOptionsMenu(self):
        self.optionsMenuWindow = None

    @Slot()
    def _droppedPresetWidget(self):
        self.refreshTool()

    def _clickedConformLayers(self):
        self.conformSceneLayersToLODView()

    def _clickedGenerateXML(self):
        categories = self.treeLODs.getSelectedCategory()
        log = ""
        count = len(categories)
        i = 0
        if count > 0:
            self.progressBar.setRange(0, count)
            self.progressBar.setValue(0)
            for category in categories:
                objects = self.treeLODs._baseNameDict[category]
                objects = sceneUtils.sortObjectsByLODLevels(objects)
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
                qtUtils.popup_scroll(title="XML Generation Ouput", text=log)

    def _clickedAddPresetGroup(self):
        newGroup = presetUtils.createNewGroup()
        presets = self.treePresets.getSelectedPresets()
        if len(presets) > 0:
            for preset in presets:
                preset.edit(group=newGroup.identifier)
        self.refreshTool()
        self.treePresets.startEditingItemWithGroupID(newGroup.identifier)

    def _clickedAddPreset(self):
        groups = self.treePresets.getSelectedGroups()
        groupID = None
        if (len(groups) > 0):
            groupID = groups[0].identifier
        filePath = presetUtils.askForNewPath("Create New Preset")
        if(filePath != None):
            presetName = os.path.split(filePath)[1]
            presetName = os.path.splitext(presetName)[0]
            presetUtils.createNewPreset(
                presetName, group=groupID, filePath=filePath)
            self.refreshTool()

    def _clickedRemovePreset(self):
        groups = self.treePresets.getSelectedGroups()
        presets = self.treePresets.getSelectedPresets()
        presetUtils.confirmAndRemove(presets=presets, groups=groups)
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
        for preset in presets:            
            targetGroup = preset.group
            if groupTransfer.has_key(targetGroup):
                targetGroup = groupTransfer[targetGroup] 
            presetUtils.createNewPreset(labelName=preset.name, group=targetGroup, filePath=preset.path, layerNames=preset.layerNames)
            
        self.refreshTool()



    def _changedTab(self):
        currentTab = self.tabWidget.currentIndex()
        isLODView = currentTab == 0
        isPresetView = currentTab == 1
        self.btnGenerateXML.setEnabled(isLODView)
        self.btnAddExport.setEnabled(isLODView)
        self.btnRemoveExport.setEnabled(isLODView)
        self.refreshTool()

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
        self.refreshTool()

    def _changedLayerItem(self):
        selected = self.treePresets.getSelectedPresets()
        if (len(selected) == 1):
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
            layerNames = preset.layerNames
            self.treeLayer.intializeCheckLayers(layerNames)
            self.btnApplyPresetLayer.setText("Apply")
            self.presetParamName.setText(unicode(preset.name))
        else:
            self.treeLayer.uncheckAllLayers()
            self.treeLayer.setEnabled(False)
            self.presetParamName.setText("-")

    def _clickedApplyPresetEdit(self):
        groups = self.treePresets.getSelectedGroups()
        txt = self.presetParamName.text()
        optionIndex = self.cbOptionPreset.currentIndex()
        if(len(groups) == 1):
            self.treeLayer.setEnabled(False)
            optionPreset = self.cbOptionPreset.itemData(optionIndex)
            groups[0].edit(name=txt,optionPreset=optionPreset.identifier)            
        else:
            selectedPresets = self.treePresets.getSelectedPresets()
            for preset in selectedPresets:
                preset.edit(name=txt)
        self.refreshTool()

    def _clickedApplyLayerSelection(self):
        presets = self.treePresets.getSelectedPresets()
        if (len(presets) == 1):
            checkedLayers = self.treeLayer.getCheckedLayerNames()
            self.applyLayerSelectionToPreset(presets[0], checkedLayers)

    def applyLayerSelectionToPreset(self, preset, layerNames):
        preset.edit(layerNames=layerNames)
        self.btnApplyPresetLayer.setText("Apply")
        self.treeLayer.isEdited = False

    def _selectionChangedLOD(self):
        selected = self.treeLODs.getSelectedRootList()
        lodValue = None
        flattenValue = None
        if(len(selected) == 1):
            lodValue = rt.getUserProp(selected[0], constants.PROP_LOD_VALUE)
            if(lodValue is not None):
                self.lodValue.setText(str(lodValue))
            else:
                self.lodValue.setText("-")
            flattenValue = rt.getUserProp(selected[0], constants.PROP_FLATTEN)
            if(flattenValue is not None):
                self.flattenComboBox.setCurrentIndex(0 if flattenValue else 1)
            else:
                self.flattenComboBox.setCurrentIndex(2)
            keepInstances = rt.getUserProp(selected[0], constants.PROP_KEEP_INSTANCES)
            if (keepInstances is not None):
                self.cbKeepInstances.setCheckState(Qt.Checked if keepInstances else Qt.Unchecked)
            else:
                self.cbKeepInstances.setCheckState(Qt.Unchecked)
        else:
            self.flattenComboBox.setCurrentIndex(2)
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
            flattenChoice = self.flattenComboBox.currentIndex()
            if(flattenChoice != 2):
                flatten = True if flattenChoice == 0 else False
                userprop.setUserProp(lod, constants.PROP_FLATTEN, flatten)
                
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

    def _clickedAddExport(self):
        selected = sceneUtils.getSelectedObjects()
        exporter.addExportPathToObjects(selected)
        self.refreshTool()

    def _clickedRemoveExport(self):
        selected = sceneUtils.getSelectedObjects()
        exporter.removeExportPathToObjects(selected)
        self.refreshTool()

    def _clickedExportAll(self):
        currentTree = self.getCurrentTree()
        if(currentTree == self.treeLODs):
            fullList = self.getCurrentFullList()
            self.sendToExporter(fullList)
        elif (currentTree == self.treePresets):
            fullList = self.treePresets.getAllPresetsListWithOption()
            self.sendPresetsWithOptionsToExporter(fullList)

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

    def conformSceneLayersToLODView(self):
        if(self.getCurrentTree() != self.treeLODs):
            return
        if(not qtUtils.popup_Yes_No(
            title="Conform",
            text="""Conforming the scene layers to the LOD View will destroy all your layers and create a hierarchy of layers reflecting the LOD View object list. It will put all the other objects in the default layer. This is optional.\n
            Are you really sure you want to do this ?""")):
            return
        sceneUtils.conformSceneLayersToTemplate(self.treeLODs._baseNameDict)


    def sendToExporter(self, objects):
        count = len(objects)
        log = ""
        optionPreset = self.cbObjectOptionPreset.itemData(self.cbObjectOptionPreset.currentIndex())
        if(count > 0):
            exporter.exportObjects(objects, optionPreset)

    def sendPresetsWithOptionsToExporter(self, presetsAndOptions):
        '''
        in : presetsAndOptions = list(tuple(PresetObject,OptionPresetObject))
        '''
        count = len(presetsAndOptions)
        if(count > 0):
            exporter.exportPresetsAndOptions(presetsAndOptions)

################################
##### ROOT DEBUG FUNCTION ######
################################


def _printRootNodeProperties():
    rootNode = sceneUtils.getSceneRootNode()
    print(userprop.getUserPropBuffer(rootNode))


def _cleanupProp(prop):
    rootNode = sceneUtils.getSceneRootNode()
    userprop.removeUserProp(rootNode, prop)


def _cleanupRootNodeProperties():
    rootNode = sceneUtils.getSceneRootNode()
    userprop.setUserPropBuffer(rootNode, "")  # CLEANUP ROOT NODE PROPERTIES
    print("Root node user properties wiped")
################################
###### OPENING PROCEDURES ######
################################


def updateObsoleteExportPath():
    log = ""
    roots = sceneUtils.getAllRoots(sceneUtils.getAllObjects())
    for r in roots:
        oldPath = userprop.getUserProp(r, constants.PROP_OLD_EXPORT_PATH)
        newPath = userprop.getUserProp(r, constants.PROP_EXPORT_PATH)
        if oldPath is not None and newPath is None:
            newPath = utility.convertRelativePathToAbsolute(
                oldPath, rt.maxFilePath)
            newPath = utility.convertAbsolutePathToRelative(
                newPath, rt.pathConfig.getCurrentProjectFolder())
            userprop.setUserProp(r, constants.PROP_EXPORT_PATH, newPath)
            log += "{0}\n".format(r.name)
    return log


def writeDefaultBabylonParametersInRootNode():
    sceneRoot = sceneUtils.getSceneRootNode()
    for prop in BabylonPYMXS.propertyToDefault.keys():
        value = userprop.getUserProp(
            sceneRoot, prop, BabylonPYMXS.propertyToDefault[prop])
        userprop.setUserProp(sceneRoot, prop, value)


def checkSavedMaxFilePath():  # UNUSED
    sceneRoot = sceneUtils.getSceneRootNode()
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

multiExporter = None
def run():
    global multiExporter
    # Some babylon export parameters are needed
    writeDefaultBabylonParametersInRootNode()
    log = updateObsoleteExportPath()
    if log != "":
        qtUtils.popup_scroll(
            title="Updated Export Path",
            text="Update export path property keyword of following objects : {0}".format(
                log)
        )

    BabylonPYMXS.initializeBabylonExport()
    multiExporter = MainWindow()
    multiExporter.show()


# _cleanupProp("fs_export_preset_a8e403c3-aac2-4bc9-b99b-8faac5cd90b5")
# _cleanupProp("fs_export_preset_32756c41-2f78-4a7c-ae6e-4326f8e75045")
# _cleanupProp("flightsim_export_preset")
# _cleanupProp("flightsim_export_preset_group")
#_cleanupRootNodeProperties()
_printRootNodeProperties()