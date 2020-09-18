import os
import sys

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

import MultiExporter.constants as const
import MultiExporter.presetUtils as presetUtils
from maxsdk import layer, qtUtils, sceneUtils, userprop, utility
from pymxs import runtime as rt



class TreeView(QTreeWidget):
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
            roots = sceneUtils.filterObjectsWithUserProperty(roots, const.PROP_EXPORT_PATH)  # only object ready for export
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
                if(self._rootDict.has_key(i)):
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

    def createRootWidget(self, obj, offset=1):
        qTreeWidget = QTreeWidgetItem()
        qTreeWidget.setCheckState(0, Qt.CheckState.Unchecked)
        self.updateRootWidget(obj, qTreeWidget, offset)
        return qTreeWidget

    def updateRootWidget(self, obj, widget, offset=1):
        path = rt.getUserProp(obj, const.PROP_EXPORT_PATH)

        widget.setText(offset, obj.name)
        widget.setTextColor(offset, "#FFAAAA" if path == None or path == "" else "#AAFFAA")

        lodValue = rt.getUserProp(obj, const.PROP_LOD_VALUE)
        widget.setText(offset + 1, unicode(lodValue))
        widget.setTextColor(offset + 1, "#FFAAAA" if lodValue == None or lodValue == 0 else "#AAFFAA")

        flattenValue = rt.getUserProp(obj, const.PROP_FLATTEN)
        widget.setText(offset + 2, str(flattenValue))
        widget.setTextColor(offset + 2, "#FFAAAA" if flattenValue == None else "#AAFFAA")
        
        instanceValue = rt.getUserProp(obj, const.PROP_KEEP_INSTANCES)
        widget.setText(offset + 3, str(instanceValue))
        widget.setTextColor(offset + 3, "#FFAAAA" if instanceValue == None else "#AAFFAA")

        widget.setText(offset+4, path)

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


class TreeViewCategory(TreeView):
    def __init__(self, parent):
        TreeView.__init__(self, parent)
        self._baseNameDict = {}

    def createTree(self):
        self.clearSelection()
        self._rootDict.clear()
        self.clear()
        self.createCategoryDictionary()
        for category in self._baseNameDict:  # build the QTree based on this dictionary
            qTreeParent = QTreeWidgetItem()
            qTreeParent.setText(0, category)
            # self._rootDict[qTreeParent] = self._baseNameDict[category] # add list of lods to the parent widget ref in the dictionary
            for obj in self._baseNameDict[category]:
                qTreeChild = QTreeWidgetItem()
                self.updateRootWidget(obj, qTreeChild, 0)
                qTreeChild.setCheckState(0, Qt.CheckState.Unchecked)
                qTreeParent.addChild(qTreeChild)
                # add each object to its corresponding widget in the dict
                self._rootDict[qTreeChild] = obj
            self.addTopLevelItem(qTreeParent)
        self.expandAll()

    def refreshTree(self):
        self.createTree()

    def createCategoryDictionary(self):
        roots = self.gatherSceneObjects()
        self._baseNameDict.clear()
        for r in roots:  # for each base name excluding LODS
            baseName = utility.removeLODSuffix(r.name)
            if(not self._baseNameDict.has_key(baseName)):
                self._baseNameDict[baseName] = list()
        for lo in roots:  # add each LOD to the correct category
            baseName = utility.removeLODSuffix(lo.name)
            if(self._baseNameDict.has_key(baseName)):
                self._baseNameDict[baseName].append(lo)
            else:
                print("{0} doesn't have a LOD0 but still has other LODs. {1} will not show in the list.".format(
                    baseName, lo.name))

    def getSelectedCategory(self):
        selectedCategory = []
        for selectedItem in self.selectedItems():
            baseName = selectedItem.text(0)
            if(selectedItem.parent()):
                baseName = selectedItem.parent().text(0)
            if(baseName not in selectedCategory):
                selectedCategory.append(baseName)
        return selectedCategory

    def getAllRootsList(self):
        allRoots = []
        for v in self._baseNameDict.values():
            for o in v:
                if(o not in allRoots):
                    allRoots.append(o)
        return allRoots
#################
# TreeViewLayer #
#################


class TreeViewLayer(TreeView):
    def __init__(self, parent):
        TreeView.__init__(self, parent)
        self._layerDict = {}
        self.isEdited = False

    def gatherLayers(self):
        return layer.getAllRootLayer()

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
        #        if(v == r.layer):
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
        qTreeChild.setText(0, lay.name)
        # add widget to dictionary with actual layer as value
        self._layerDict[qTreeChild] = lay
        childrenLayers = layer.getChildrenLayer(lay)
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
            s.setCheckState(0, self._qGlobalCheckBox.checkState())
            for h in hier:
                h.setCheckState(0, self._qGlobalCheckBox.checkState())
        self.isEdited = True

    def intializeCheckLayers(self, layerNames):
        topItem = [x for x in self._layerDict.keys() if x.parent() is None]
        childItem = [x for x in self._layerDict.keys() if x.parent() is not None]
        # A change to a parent's checkbox cascades to its children
        # So we first work on the parents and then the children
        for item in topItem + childItem: 
            if item.text(0) in layerNames:
                item.setCheckState(0, Qt.Checked)
            else:
                item.setCheckState(0, Qt.Unchecked)
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

    @Slot()
    def _selectionChanged(self):
        selection = self.getSelectedLayers()
        sceneUtils.selectLayers(selection)

    def _doubleClickedItem(self):
        return None
##################
# TreeViewPreset #
##################


class TreeViewPreset(TreeView):
    hasChanged = Signal()  # custom signal

    def __init__(self, parent, presetStorageId = const.PROP_PRESET_LIST, groupStorageId = const.PROP_PRESET_GROUP_LIST):
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

    @Slot()
    def _changedWidgetItem(self, widget, col):
        for i in range(widget.childCount()):
            child = widget.child(i)
            child.setCheckState(col, widget.checkState(col))
        newName = widget.text(0)
        newName = userprop.cleanupStringForPropListStorage(newName)
        widget.setText(0, newName)
        if self._rootDict.has_key(widget):
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
                g = presetUtils.GroupObject(groupID)
                groups.append(g)
        return groups

    def _gatherSceneObjects(self):
        rootNode = sceneUtils.getSceneRootNode()
        presetList = userprop.getUserPropList(rootNode, self.presetStorageId)
        presets = []
        if presetList is not None:
            for presetID in presetList:
                p = presetUtils.PresetObject(presetID)
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
                    option = presetUtils.OptionPresetObject(g.optionPreset)
                else:
                    option = presetUtils.getDefaultExportPresetOptions()
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
                qTreeWidget = self._createRootWidget(obj=r, offset=0)
                # add widget to dictionary with object as value
                self._rootDict[qTreeWidget] = r
                group = None
                for k in self._groupDict.keys():
                    if k.identifier == r.group:
                        group = k
                        break
                if (group != None):
                    self._groupDict[group].addChild(qTreeWidget)
                else:
                    self.addTopLevelItem(qTreeWidget)
        self.expandAll()

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
                break
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
            option = presetUtils.getDefaultExportPresetOptions()
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
