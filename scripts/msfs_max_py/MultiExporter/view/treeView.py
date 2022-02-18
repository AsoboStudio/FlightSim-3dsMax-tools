"""Module to handle PySide2 QTreeWidget in the 3dsMax context. 
"""
import os
import sys
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from ..constants import *
from ..presetUtils import *    

from maxsdk import layer, qtUtils, sceneUtils, userprop, utility
from pymxs import runtime as rt



class TreeView(QTreeWidget):
    """Parent class, unused.
    """
    def __init__(self, parent):
        QTreeWidget.__init__(self, parent)
        self._showOnlyExportable = True
        self._showOnlyVisible = False
        self._showOnlyLODs = False
        self._rootDict = {}  # holds link between QTreeWidgetItem and 3ds max node
        self.itemSelectionChanged.connect(lambda: self._selectionChanged())
        self.itemDoubleClicked.connect(lambda: self._doubleClickedItem())
        self.itemChanged.connect(lambda x, y: self._changedWidgetItem(x, y))

    def setGlobalCheckBox(self, qGlobalCheckBox):
        self._qGlobalCheckBox = qGlobalCheckBox
        self._qGlobalCheckBox.setTristate(False)
        self._qGlobalCheckBox.stateChanged.connect(lambda: self._modifyCheckBox())

    def gatherSceneObjects(self):
        roots = sceneUtils.getAllRoots(sceneUtils.getAllObjects())
        if(self._showOnlyExportable):
            roots = sceneUtils.filterObjectsWithUserProperty(roots, PROP_EXPORT_PATH)  # only object ready for export
        if(self._showOnlyVisible):
            roots = sceneUtils.filterObjectsVisible(roots)
        if(self._showOnlyLODs):
            roots = sceneUtils.filterLODLevel(roots)
        return roots

    def createTree(self):
        self.clearSelection()
        self._rootDict.clear()
        self.clear()
        roots = self.gatherSceneObjects()
        if (isinstance(roots, list) and roots is not None):
            for r in roots:
                qTreeWidget = self.createRootWidget(obj=r, offset=0)
                # add widget to dictionary with object as value
                self._rootDict[qTreeWidget] = r
                self.addTopLevelItem(qTreeWidget)
        self.expandAll()

    def refreshTree(self):
        roots = self.gatherSceneObjects()
        for r in roots:
            if(r not in self._rootDict.values()):
                qTreeWidget = self.createRootWidget(r, 0)
                # add widget to dictionary with object as value
                self._rootDict[qTreeWidget] = r
                self.addTopLevelItem(qTreeWidget)
        # search for object in the tool list not in the scene anymore
        # do the search backward because we remove objects from the list as we go through
        for i in reversed(range(len(self._rootDict.values()))):
            value = self._rootDict.values()[i]
            key = self._rootDict.keys()[i]
            if(value not in roots):  # if the object in the list not in the scene anymore get rid of it
                self.takeTopLevelItem(self.indexOfTopLevelItem(key))
                self._rootDict.pop(key)
            else:  # else update the path and content
                try:
                    self.updateRootWidget(value, key, 0)
                except:
                    print("cleaning up old values")
                    self.takeTopLevelItem(self.indexOfTopLevelItem(key))
                    self._rootDict.pop(key)

    def getSelectedRootList(self):
        selectedRoots = []
        for item in self.selectedItems():
            items = self.getQtItemsDescendants(item)
            for i in items:
                if( i in self._rootDict):
                    obj = self._rootDict[i]
                    if(obj not in selectedRoots):
                        selectedRoots.append(obj)
        return selectedRoots

    def getAllRootsList(self):
        allRoots = []
        for v in self._rootDict.values():
            if(v not in allRoots):
                allRoots.append(v)
        return allRoots

    def getSelectedQtItems(self):
        return self.selectedItems()

    def getQtItemsDescendants(self, item):
        hierarchy = []
        hierarchy.append(item)
        for i in range(item.childCount()):
            c = item.child(i)
            hierarchy += self.getQtItemsDescendants(c)
        return hierarchy

    def getTopParentQtItem(self, widget):
        widgetParent = widget.parent()
        if widgetParent is None:
            return widget
        else:
            return self.getTopParentQtItem(widgetParent)

    def getParentQtItem(self, widget):
        widgetParent = widget.parent()
        if widgetParent is None:
            return widget
        else:
            return widgetParent

    def createRootWidget(self, obj, offset=1):
        qTreeWidget = QTreeWidgetItem()
        qTreeWidget.setCheckState(0, Qt.CheckState.Unchecked)
        self.updateRootWidget(obj, qTreeWidget, offset)
        return qTreeWidget

    def updateRootWidget(self, obj, widget, offset=1):
        path = rt.getUserProp(obj, PROP_EXPORT_PATH)

        widget.setText(offset, obj.name)
        widget.setTextColor(offset, "#FFAAAA" if path == None or path == "" else "#AAFFAA")

        lodValue = rt.getUserProp(obj, PROP_LOD_VALUE)
        widget.setText(offset + 1, str(lodValue))
        widget.setTextColor(offset + 1, "#FFAAAA" if lodValue == None or lodValue == 0 else "#AAFFAA")
        
        instanceValue = rt.getUserProp(obj, PROP_KEEP_INSTANCES)
        widget.setText(offset + 2, str(instanceValue))
        widget.setTextColor(offset + 2, "#FFAAAA" if instanceValue == None else "#AAFFAA")

        widget.setText(offset+3, path)

    def getCheckedRootList(self):
        checkedRoots = []
        for i in self._rootDict.keys():
            if i.checkState(0) == Qt.Checked:
                checkedRoots.append(self._rootDict[i])
        return checkedRoots

    @Slot()
    def _doubleClickedItem(self):
        selected = self.selectedItems()
        s = selected[len(selected) - 1]
        if(s.childCount() == 0):
            rt.select(self._rootDict[s])
            userprop.openUserPropertyWindow()

    @Slot()
    def _selectionChanged(self):
        selection = self.getSelectedRootList()
        selection = sceneUtils.getDescendantsOfMultiple(selection)
        rt.select(selection)

    @Slot()
    def _modifyCheckBox(self):
        selection = self.selectedItems()
        for s in selection:
            hier = self.getQtItemsDescendants(s)
            for h in hier:
                if h in self._rootDict:
                    h.setCheckState(0, self._qGlobalCheckBox.checkState())

    @Slot()
    def _changedWidgetItem(self, widget, col):
        for i in range(widget.childCount()):
            child = widget.child(i)
            child.setCheckState(col, widget.checkState(col))



