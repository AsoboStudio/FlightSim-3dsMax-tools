import os
import sys
import re

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

import MaxPlus
import MultiExporter.ui.mainwindow_ui as mainWindowUI
import exporter
import qtUtils
from maxsdk import dialog as sdkdialog
from maxsdk import perforce as sdkperforce
from maxsdk import userprop, utility, sceneUtils, layer
from pymxs import runtime as rt
import treeView
reload(userprop)
reload(sceneUtils)
reload(sdkperforce)
reload(sdkdialog)
reload(mainWindowUI)
reload(layer)
reload(qtUtils)
reload(exporter)
reload(treeView)

class MainWindow(QWidget, mainWindowUI.Ui_MultiExporter):
    # Dictionary used to connect QWidget to PYMXS object
    _qLODTree = treeView.TreeViewCategory
    _qRootTree = treeView.TreeView
    _qLayerTree = treeView.TreeViewLayer    

    def __init__(self):
        QWidget.__init__(self)
        self.setupUi(self)
        #buttons
        self.btnAddExport.pressed.connect(lambda: self._clickedAddExport())
        self.btnRemoveExport.pressed.connect(lambda: self._clickedRemoveExport())
        self.btnRefresh.pressed.connect(lambda: self._refreshTool())
        self.tabWidget.currentChanged.connect(lambda : self._changedTab())
        self.btnConformLayers.pressed.connect(lambda: self._clickedConformLayers())
        #export
        self.btnExportSelected.pressed.connect(lambda: self._clickedExportSelected())
        self.btnExportAll.pressed.connect(lambda: self._clickedExportAll())
        self.btnExportTicked.pressed.connect(lambda: self._clickedExportTicked())
        self.btnOpenExportFolder.pressed.connect(lambda: self._clickedOpenExportFolder())
        #lod view
        self.btnSetLODValues.pressed.connect(lambda: self._clickedSetLODValues())
        self.btnGenerateXML.pressed.connect(lambda: self._clickedGenerateXML())
        self.checkBoxLODModifier = qtUtils.createCheckBox(qtWidget=self.tab_3)
        self._qLODTree = treeView.TreeViewCategory(self.treeLODs,self.checkBoxLODModifier)
        self._qLODTree._qTreeView.itemSelectionChanged.connect(lambda: self._selectionChangedLOD())
        #root view
        self.checkBoxModifier = qtUtils.createCheckBox(qtWidget=self.tab_2)
        self._qRootTree = treeView.TreeView(self.toExportList,self.checkBoxModifier)
        #layer view
        self.checkBoxLayerModifier = qtUtils.createCheckBox(qtWidget=self.tab)
        self._qLayerTree = treeView.TreeViewLayer(self.toLayerList, self.checkBoxLayerModifier)
        
        self.cbVisibleOnly.stateChanged.connect(lambda: self._changeCheckboxVisibility())
        self.cbIncludeLods.stateChanged.connect(lambda: self._changeCheckboxLODs())
        self.cbExportableOnly.stateChanged.connect(lambda: self._changeCheckboxExportable())
        self.groupBox.setContextMenuPolicy(Qt.NoContextMenu)
        #self.setContextMenuPolicy(Qt.NoContextMenu)
        self.toExportList.setContextMenuPolicy(Qt.ActionsContextMenu)
        self._qLODTree.createTree()
        self._qRootTree.createTree()
        #self._qLayerTree.createTree()

    def contextMenuEvent(self, event):
        r = self.tabWidget.geometry()
        if(r.contains(event.pos())):          
            menu = QMenu(self)
            exportAction = menu.addAction("Export Selected")
            openFolder = menu.addAction("Open in Explorer")
            action = menu.exec_(self.mapToGlobal(event.pos()))
            if action == exportAction:
                self._clickedExportSelected()
            if action == openFolder:
                self._clickedOpenExportFolder()

    @Slot()
    def _clickedConformLayers(self):
        self.conformSceneLayersToLODView()

    @Slot()
    def _clickedGenerateXML(self):
        categories = self._qLODTree.getSelectedCategory()
        log = ""
        for category in categories:
            objects = self._qLODTree._baseNameDict[category]
            metadataPath = exporter.getMetadataPath(objects[0]) # lookup first LOD of the category and get metadata path
            if(not exporter.createLODMetadata(metadataPath,objects)):
                log += "Couldn't generate {0} metadata xml file.\n".format(category)
        if(log != ""):
            qtUtils.popup(title="XML Generation Error", text=log + "Check the log")

        
    @Slot()
    def _changedTab(self):
        currentTab = self.tabWidget.currentIndex() 
        self.btnGenerateXML.setEnabled(currentTab == 2)
        self._refreshTool()


        
    @Slot()
    def _clickedOpenExportFolder(self):
        selected = self.getCurrentlySelectedRootList()        
        if(len(selected) > 0):
            exportPath = exporter.getAbsoluteExportPath(selected[0])
            if(exportPath): 
                exportPath = os.path.split(exportPath)[0]
                os.startfile(exportPath)

    @Slot()
    def _changeCheckboxExportable(self):
        state = self.cbExportableOnly.checkState() == Qt.Checked
        self._qLODTree._showOnlyExportable = state
        self._qRootTree._showOnlyExportable = state
        self._qLayerTree._showOnlyExportable = state
        self._refreshTool()

    @Slot()
    def _changeCheckboxLODs(self):
        state = self.cbIncludeLods.checkState() == Qt.Checked
        self._qLODTree._showOnlyLODs = state
        self._qRootTree._showOnlyLODs = state
        self._qLayerTree._showOnlyLODs = state
        self._refreshTool()

    @Slot()
    def _changeCheckboxVisibility(self):
        state = self.cbVisibleOnly.checkState() == Qt.Checked
        self._qLODTree._showOnlyVisible = state
        self._qRootTree._showOnlyVisible = state
        self._qLayerTree._showOnlyVisible = state
        self._refreshTool()

    @Slot()
    def _selectionChangedLOD(self):
        selected = self._qLODTree.getSelectedRootList()
        lodValue = None
        flattenValue = None
        if(len(selected) == 1):
            lodValue = rt.getUserProp(selected[0],"flightsim_lod_value")
            if(lodValue is not None):
                self.lodValue.setText(str(lodValue))
            else: 
                self.lodValue.setText("-")
            flattenValue = rt.getUserProp(selected[0],"flightsim_flatten")
            if(flattenValue is not None):
                self.flattenComboBox.setCurrentIndex(0 if flattenValue else 1)
            else:
                self.flattenComboBox.setCurrentIndex(2)
        else:
            self.flattenComboBox.setCurrentIndex(2)
            self.lodValue.setText("-")

    @Slot()
    def _clickedSetLODValues(self):
        lods = self._qLODTree.getSelectedRootList()
        for lod in lods:
            lodValueChoice = self.lodValue.text()
            if(lodValueChoice != "-"):
                validValue = qtUtils.validateLineEdit(lodValueChoice)
                if(validValue):
                    userprop.setUserProp(lod,"flightsim_lod_value", validValue)

            flattenChoice = self.flattenComboBox.currentIndex() 
            if(flattenChoice != 2):
                flatten = True if flattenChoice == 0 else False
                userprop.setUserProp(lod,"flightsim_flatten", flatten )
        self._refreshTool()

    @Slot()
    def _clickedExportTicked(self):
        selected = self.getCurrentlyCheckedRootList()
        self.sendToExporter(selected)

    @Slot()
    def _clickedExportSelected(self):
        selected = self.getCurrentlySelectedRootList()
        self.sendToExporter(selected)

    @Slot()
    def _clickedAddExport(self):
        selected = sceneUtils.getSelectedObjects()
        exporter.addExportPathToObjects(selected)
        self._refreshTool()

    @Slot()
    def _clickedRemoveExport(self):
        selected = sceneUtils.getSelectedObjects()
        exporter.removeExportPathToObjects(selected)
        self._refreshTool()

    @Slot()
    def _clickedExportAll(self):
        fullList = self.getCurrentFullList()
        self.sendToExporter(fullList)

    @Slot()
    def _refreshTool(self):
        self.getCurrentTree().refreshTree()

    def getCurrentTree(self):
        currentTab = self.tabWidget.currentIndex() 
        if(currentTab == 0):
            return self._qLayerTree
        if(currentTab == 1):
            return self._qRootTree
        if(currentTab == 2):
            return self._qLODTree
        return None

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
        if(self.getCurrentTree() != self._qLODTree):
            return
        if(not qtUtils.popup_Yes_No(
            title="Conform",
            text="""Conforming the scene layers to the LOD View will destroy all your layers and create a hierarchy of layers reflecting the LOD View object list. It will put all the other objects in the default layer. This is optional.\n
            Are you really sure you want to do this ?""")):
            return
        layerManager = rt.layerManager
        defaultLayer = layerManager.getLayer(0)
        allObjects = sceneUtils.getAllObjects()
        for x in allObjects:
            defaultLayer.addNode(x)
        for baseName in self._qLODTree._baseNameDict.keys():
            currentCategory = layerManager.getLayerFromName(baseName)
            if(currentCategory is None):
                print "creating new category"
                currentCategory = layerManager.newLayerFromName(baseName)
            for o in self._qLODTree._baseNameDict[baseName]:
                currentLayer = layerManager.getLayerFromName(o.name)
                if(currentLayer is None):
                    print "creating new layer"
                    currentLayer = layerManager.newLayerFromName(o.name)
                hierarchy = sceneUtils.getDescendants(o)
                for oo in hierarchy:
                    currentLayer.addNode(oo)
                currentLayer.setParent(currentCategory)
        layer.deleteAllEmptyLayerHierarchies()

    def sendToExporter(self,objects):
        count = len(objects)
        log = ""
        if(count > 0):
            self.progressBar.setRange(0,count)
            self.progressBar.setValue(0)
            i=0
            for o in objects:
                log += exporter.exportObject(o)
                i+=1
                self.progressBar.setValue(i)
        if(log != ""):
            log += "Check Log"
            qtUtils.popup(title="Export Error",text=log) 

def run():
    multiExporter = MainWindow()
    utility.attachToMax(multiExporter)
    multiExporter.show()