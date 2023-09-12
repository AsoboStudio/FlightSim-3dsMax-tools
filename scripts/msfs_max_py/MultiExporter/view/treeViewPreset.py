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
from maxsdk import layer, qtUtils, sceneUtils, userprop, utility
from pymxs import runtime as rt


class TreeViewPreset(TreeView):
    """Class to gather presets in the root node and put them in a QTreeWidget. Widget are connected to Preset using the Dictionary _rootDict and Group Widget using the _groupDict
    """
    hasChanged = Signal()  # custom signal

    def __init__(self, parent, presetStorageId = PROP_PRESET_LIST, groupStorageId = PROP_PRESET_GROUP_LIST):
        TreeView.__init__(self, parent)
        self.presetStorageId = presetStorageId
        self.groupStorageId = groupStorageId
        self._groupDict = {}
    # upon dropping widget find target and find its group then store selected widgets in said group

    def dropEvent(self, event):
        target = self.itemAt(event.pos())
        found = False
        selected = self.getSelectedPresets()
        if (target):
            parent = target.parent()
            if (parent):
                target = target.parent()
            for groupID in self._groupDict.keys():
                # retreive group id that we stored in the fourth column for convenience
                data = target.data(0, Qt.UserRole)
                if data is not None:
                    if (groupID.identifier == target.data(0,Qt.UserRole).identifier):
                        found = True
                        for s in selected:
                            s.edit(group=target.data(0,Qt.UserRole).identifier)
                        break
        if not found:
            for s in selected:
                s.edit(group="-")
        self.hasChanged.emit()
        self.refreshTree()

    @Slot()
    def _changedWidgetItem(self, widget, col):
        for i in range(widget.childCount()):
            child = widget.child(i)
            child.setCheckState(col, widget.checkState(col))
        newName = widget.text(0)
        newName = userprop.cleanupStringForPropListStorage(newName)
        widget.setText(0, newName)
        if widget in self._rootDict:
            preset = self._rootDict[widget]
            preset.edit(name=newName)
        else:
            for k in self._groupDict.keys():
                if (widget.data(0,Qt.UserRole).identifier == self._groupDict[k].data(0,Qt.UserRole).identifier):
                    print(newName,widget.data(0,Qt.UserRole).identifier)
                    k.edit(name=newName)
                    break
        if(col != 0):
            self.hasChanged.emit()

    def _gatherGroups(self):
        rootNode = sceneUtils.getSceneRootNode()
        groupList = userprop.getUserPropList(
            rootNode, self.groupStorageId)
        groups = []
        if groupList is not None:
            for groupID in groupList:
                g = GroupObject(groupID)
                groups.append(g)
        return groups

    def _gatherSceneObjects(self):
        rootNode = sceneUtils.getSceneRootNode()
        presetList = userprop.getUserPropList(rootNode, self.presetStorageId)
        presets = []
        if presetList is not None:
            for presetID in presetList:
                p = PresetObject(presetID)
                presets.append(p)
        return presets

    def _createRootWidget(self, obj, offset=1):
        qTreeWidget = QTreeWidgetItem()
        qTreeWidget.setCheckState(0, Qt.CheckState.Unchecked)
        qTreeWidget.setFlags(Qt.ItemIsDropEnabled | Qt.ItemIsEditable | Qt.ItemIsSelectable |
                             Qt.ItemIsDragEnabled | Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
        self._updateRootWidget(obj, qTreeWidget, offset)
        return qTreeWidget

    def _updateRootWidget(self, obj, widget, offset=1):
        widget.setText(offset, str(obj.name))
        path = str(obj.path)
        widget.setText(offset + 1, qtUtils.truncateStringFromLeft(path, 50))
        widget.setToolTip(offset + 1, path)

    def _modifyCheckBox(self):
        selection = self.selectedItems()
        for s in selection:
            hier = self.getQtItemsDescendants(s)
            for h in hier:
                h.setCheckState(0, self._qGlobalCheckBox.checkState())

    def _doubleClickedItem(self):
        return None

    def _selectionChanged(self):
        return None

    def startEditingItemWithGroupID(self, groupID):
        for k in self._groupDict.keys():
            if k.identifier == groupID:
                widget = self._groupDict[k]
                self.setCurrentItem(widget)
                self.editItem(widget, 0)
                break

    def startEditingSelectedItem(self):
        items = self.getSelectedQtItems()

        if (len(items) > 0):
            self.editItem(items[0], 0)
            self.hasChanged.emit()

    def createTree(self):
        self.clearSelection()
        self._rootDict.clear()
        self.clear()
        self._groupDict.clear()
        roots = self._gatherSceneObjects()
        groups = self._gatherGroups()
        sceneRoot = sceneUtils.getSceneRootNode()
        if (isinstance(groups, list) and groups is not None):
            for g in groups:
                qTreeWidget = QTreeWidgetItem()
                qTreeWidget.setFlags(Qt.ItemIsDropEnabled | Qt.ItemIsEditable | Qt.ItemIsSelectable |
                                     Qt.ItemIsDragEnabled | Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
                qTreeWidget.setCheckState(0, Qt.CheckState.Unchecked)
                qTreeWidget.setText(0, str(g.name))
                if g.optionPreset is not None:
                    option = OptionPresetObject(g.optionPreset)
                else:
                    option = getDefaultExportPresetOptions()
                optionName = option.name
                qTreeWidget.setText(1, "Export with : '{0}'".format(optionName))
                # store the group id in the fourth column
                qTreeWidget.setData(0,Qt.UserRole,g)
                qTreeWidget.setData(1,Qt.UserRole,option)
                qTreeWidget.setText(4, g.identifier)
                self._groupDict[g] = qTreeWidget
                self.addTopLevelItem(qTreeWidget)
        if (isinstance(roots, list) and roots is not None):
            for r in roots:
                qTreeWidgetPreset = self._createRootWidget(obj=r, offset=0)
                self._rootDict[qTreeWidgetPreset] = r
                group = None
                for k in self._groupDict.keys():
                    if k.identifier == r.group:
                        group = k
                        break
                if (group != None):
                    self._groupDict[group].addChild(qTreeWidgetPreset)
                else:
                    self.addTopLevelItem(qTreeWidgetPreset)

    def getPresetsFromGroup(self,_group):
        presets = []
        for qtroots in self._rootDict.keys():
            if self._rootDict[qtroots].group == _group.identifier:
                presets.append(self._rootDict[qtroots])
        return presets


    def refreshTree(self):
        self.createTree()

    def getAllPresetsList(self):
        allRoots = []
        for v in self._rootDict.values():
            if(v not in allRoots):
                allRoots.append(v)
        return allRoots

    def getSelectedPresets(self):
        selected = []
        qtItems = self.getSelectedQtItems()
        for item in qtItems:
            if(item in self._rootDict):
                prop = self._rootDict[item]
                selected.append(prop)
        return selected

    def getSelectedPresetsAndGroupsContent(self):
        selected = []
        qtItems = self.getSelectedQtItems()
        for item in qtItems:
            hierarchy = self.getQtItemsDescendants(item)
            for obj in hierarchy:
                if(obj in self._rootDict):
                    prop = self._rootDict[obj]
                    if(prop not in selected):
                        selected.append(prop)
        return selected

    def getSelectedGroups(self):
        selected = []
        qtItems = self.getSelectedQtItems()
        for item in qtItems:
            dat = item.data(0, Qt.UserRole)            
            if dat is not None:
                selected.append(dat)
        return selected

    def getCheckedPresets(self):
        selected = []
        for k in self._rootDict.keys():
            if k.checkState(0) == Qt.Checked:
                preset = self._rootDict[k]
                selected.append(preset)
        return selected

    def getQtItemFromIdentifier(self, identifier):
        for k, v in self._rootDict.items():
            if v.identifier == identifier:
                return k
        return None
    
    def getOptionPresetOfQtItem(self, qtItem):
        parent = qtItem.parent()
        option = None
        if parent is not None:
            option = parent.data(1, Qt.UserRole) 
        if option is None:
            option = getDefaultExportPresetOptions()
        return option

    def getOptionPresetFromIdentifier(self, identifier):
        return self.getOptionPresetOfQtItem(self.getQtItemFromIdentifier(identifier))

    def joinOptionsToPresets(self, presets):
        """
        Takes a list of preset as input and returns a list of tuple(preset, option)

        in: list(PresetObject)
        out: list(tuple(PresetObject,OptionPresetObject))
        """
        result = []
        for preset in presets:
            option = self.getOptionPresetFromIdentifier(preset.identifier)
            tup = (preset,option)
            result.append(tup)
        return result    

    def getSelectedPresetsWithOption(self):
        selected = self.getSelectedPresets()
        return self.joinOptionsToPresets(selected)

    def getSelectedPresetsAndGroupsContentWithOption(self):
        selected = self.getSelectedPresetsAndGroupsContent()
        return self.joinOptionsToPresets(selected)

    def getAllPresetsListWithOption(self):
        selected = self.getAllPresetsList()
        return self.joinOptionsToPresets(selected)

    def getCheckedPresetsWithOption(self):
        selected = self.getCheckedPresets()
        return self.joinOptionsToPresets(selected)
        
    def resfreshQtItemFromID(self, id, cObj):
        QTItem = self.getQtItemFromIdentifier(id)
        self._updateRootWidget(obj = cObj, widget = QTItem, offset = 0)