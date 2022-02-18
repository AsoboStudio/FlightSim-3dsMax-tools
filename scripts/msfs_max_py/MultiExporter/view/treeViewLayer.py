"""Module to handle PySide2 QTreeWidget in the 3dsMax context. 
"""
import os
import sys
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from ..constants import *
from ..presetUtils import *
from MultiExporter.view.treeView import TreeView

from maxsdk import layer as sdklayer
from maxsdk import qtUtils as sdkqtUtils
from maxsdk import sceneUtils as sdksceneUtils
from maxsdk import utility as sdkutility

from pymxs import runtime as rt

class TreeViewLayer(TreeView):
    """Class to gather scene layers and represent them as a hierarchy in a QTreeView. _layerDict connects the QtItems with their corresponding sdklayer
    """
    def __init__(self, parent):
        TreeView.__init__(self, parent)
        self._layerDict = {}
        self.isEdited = False
        self.exportByHierarchy = False
        self.repercuteCheck = True

    def gatherLayers(self):
        return sdklayer.getAllRootLayer()

    def createTree(self):
        layers = self.gatherLayers()
        self.clear()
        self._rootDict.clear()
        self._layerDict.clear()
        for l in layers:
            qTreeWidget = self.buildQTreeLayer(None, l)
            self.addTopLevelItem(qTreeWidget)
        self.expandAll()
        
        # self.expandAll()
        #roots = self.gatherSceneObjects()
        # for r in roots:
        #    for k in self._layerDict.keys():
        #        v = self._layerDict[k]
        #        if(v == r.sdklayer):
        #            qObjectChild = self.createRootWidget(r,0)
        #            k.addChild(qObjectChild)
        #            self._rootDict[qObjectChild] = r
        #            break

    def refreshTree(self):
        self.createTree()
    # recursive function to build hierarchy of layers

    def buildQTreeLayer(self, widget, lay):
        qTreeChild = QTreeWidgetItem()
        qTreeChild.setCheckState(0, Qt.CheckState.Unchecked)

        # if widget is not None: # don't affect root obj
        #     qTreeChild.setTextColor(0,"#FFAAAA" if self.exportByHierarchy else "#AAFFAA")
        # else:
        #     qTreeChild.setTextColor(0,"#AAFFAA" if self.exportByHierarchy else "#AAFFAA")

        qTreeChild.setText(0, lay.name)
        # add widget to dictionary with actual sdklayer as value
        self._layerDict[qTreeChild] = lay
        childrenLayers = sdklayer.getChildrenLayer(lay)
        for c in childrenLayers:
            self.buildQTreeLayer(qTreeChild, c)
        if widget is not None:  # if it's not the initial call
            widget.addChild(qTreeChild)  # bind new widget to parent
            return None  # and we get out of the function
        else:
            return qTreeChild  # only return reference to the widget when in the initial call

    def _modifyCheckBox(self):
        selection = self.selectedItems()
        for s in selection:
            hier = self.getQtItemsDescendants(s)
            parents = self.getTopParentQtItem(s)
            s.setCheckState(0, self._qGlobalCheckBox.checkState())
            for h in hier:
                h.setCheckState(0, self._qGlobalCheckBox.checkState())
            # for p in parents:
            #     p.setCheckState(0, self._qGlobalCheckBox.checkState())
        self.isEdited = True

    def intializeCheckLayers(self, layerNames):
        topItem = [x for x in self._layerDict.keys() if x.parent() is None]
        childItem = [x for x in self._layerDict.keys() if x.parent() is not None]
        # A change to a parent's checkbox cascades to its children
        # So we first work on the parents and then the children
        self.repercuteCheck = False

        for item in topItem + childItem: 
            if item.text(0) in layerNames:
                item.setCheckState(0, Qt.Checked)
            else:
                item.setCheckState(0, Qt.Unchecked)

        self.repercuteCheck = True
        
        self.isEdited = False

    def uncheckAllLayers(self):
        for k in self._layerDict.keys():
            k.setCheckState(0, Qt.CheckState.Unchecked)
        self.isEdited = False

    def getCheckedLayerNames(self):
        layerNames = []
        for item in self._layerDict.keys():
            if item.checkState(0) == Qt.CheckState.Checked:
                layerNames.append(item.text(0))
        return layerNames
    
    def getCheckedLayer(self):
        layer = []
        for item in self._layerDict.keys():
            if item.checkState(0) == Qt.CheckState.Checked:
                layer.append(item)
        return layer
    
    def getPartCheckedLayerNames(self):
        layerNames = []
        for item in self._layerDict.keys():
            if item.checkState(0) == Qt.CheckState.PartiallyChecked:
                layerNames.append(item.text(0))
        return layerNames   

    def getSelectedLayers(self):
        layers = []
        selection = self.getSelectedQtItems()
        for s in selection:
            items = self.getQtItemsDescendants(s)
            for item in items:
                i = self._layerDict[item]
                if (i not in layers):
                    layers.append(i)
        return layers

    def setExportedSelectionBehaviour(self, state):
        if self.exportByHierarchy != state:
            self.exportByHierarchy = state


    @Slot()
    def _changedWidgetItem(self, widget, col):
        if (self.repercuteCheck == False):
            return # Don't do anything when not repercuting 

        state = widget.checkState(col)

        for i in range(widget.childCount()):
            child = widget.child(i)
            child.setCheckState(col, state)
        self.repercuteCheck = False
        if widget.parent() is not None:
            par = widget.parent()
            self._updateParentCheckbox(parent = par, checkBoxColumn = col)
        self.repercuteCheck = True

    def _updateParentCheckbox(self, parent, checkBoxColumn):
        col = checkBoxColumn
        if (parent.childCount() != 0):
            isallUnchecked = True
            isallChecked = True      
            for i in range(parent.childCount()):
                if parent.child(i).checkState(0) == Qt.CheckState.Unchecked or parent.child(i).checkState(0) == Qt.CheckState.PartiallyChecked:
                    isallChecked = False
                if parent.child(i).checkState(0) == Qt.CheckState.Checked or parent.child(i).checkState(0) == Qt.CheckState.PartiallyChecked:
                    isallUnchecked = False
                if isallChecked == False and isallUnchecked == False:
                    break                
            if isallChecked:
                parent.setCheckState(col, Qt.CheckState.Checked)
            if isallUnchecked:
                parent.setCheckState(col, Qt.CheckState.Unchecked)
            if isallChecked == False and isallUnchecked == False:
                parent.setCheckState(col, Qt.CheckState.PartiallyChecked)
        else:
            parent.setCheckState(col, state)
        if parent.parent() is not None:
            newParent = parent.parent()
            self._updateParentCheckbox(newParent, col)


    @Slot()
    def _selectionChanged(self):
        selection = self.getSelectedLayers()
        sdksceneUtils.selectLayers(selection)

    def _doubleClickedItem(self):
        return None