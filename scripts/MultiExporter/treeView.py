import os
import sys

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import presetUtils
import constants as const

from maxsdk import layer, sceneUtils, userprop, utility, qtUtils
from pymxs import runtime as rt

reload(const)
class TreeView(QTreeWidget):
    def __init__(self, parent):
        QTreeWidget.__init__(self,parent)
        self._showOnlyExportable = True
        self._showOnlyVisible = False
        self._showOnlyLODs = False
        self._rootDict = {} # holds link between QTreeWidgetItem and 3ds max node
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
            roots = sceneUtils.filterObjectsWithUserProperty(roots, const.PROP_EXPORT_PATH) # only object ready for export
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
        if (isinstance(roots,list) and roots is not None):
            for r in roots:            
                qTreeWidget = self.createRootWidget(obj = r, offset=0)
                self._rootDict[qTreeWidget] = r # add widget to dictionary with object as value
                self.addTopLevelItem(qTreeWidget)
        self.expandAll()

    def refreshTree(self):
        roots = self.gatherSceneObjects()
        for r in roots :
            if( r not in self._rootDict.values()):
                qTreeWidget = self.createRootWidget(r,0)
                self._rootDict[qTreeWidget] = r # add widget to dictionary with object as value
                self.addTopLevelItem(qTreeWidget)

        # search for object in the tool list not in the scene anymore   
        # do the search backward because we remove objects from the list as we go through
        for i in reversed(range(len(self._rootDict.values()))): 
            value = self._rootDict.values()[i]
            key = self._rootDict.keys()[i]
            if( value not in roots ): # if the object in the list not in the scene anymore get rid of it
                self.takeTopLevelItem(self.indexOfTopLevelItem(key))
                self._rootDict.pop(key)
            else: # else update the path and content
                try:
                    self.updateRootWidget(value,key,0)
                except:
                    print "cleaning up old values"
                    self.takeTopLevelItem(self.indexOfTopLevelItem(key))
                    self._rootDict.pop(key)


    def getSelectedRootList(self):
        selectedRoots = []
        for item in self.selectedItems() :
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

    def getQtItemsDescendants(self,item):    
        hierarchy = []
        hierarchy.append(item)
        for i in range(item.childCount()):
            c = item.child(i)
            hierarchy += self.getQtItemsDescendants(c)
        return hierarchy

    def createRootWidget(self, obj, offset = 1):
        qTreeWidget = QTreeWidgetItem()
        qTreeWidget.setCheckState(0,Qt.CheckState.Unchecked)
        self.updateRootWidget(obj,qTreeWidget,offset)
        return qTreeWidget
    
    def updateRootWidget(self, obj, widget, offset=1):
        path = rt.getUserProp(obj, const.PROP_EXPORT_PATH)
        widget.setText(offset, obj.name)
        widget.setText(offset+1, unicode(rt.getUserProp(obj, const.PROP_LOD_VALUE)))
        widget.setText(offset+2, str(rt.getUserProp(obj, const.PROP_FLATTEN)))
        widget.setText(offset+3, path)
        widget.setTextColor(offset, "#FFAAAA" if path == None or path == "" else "#AAFFAA")


    def getCheckedRootList(self):
        checkedRoots = []
        for i in self._rootDict.keys():
            if i.checkState(0) == Qt.Checked:
                checkedRoots.append(self._rootDict[i])
        return checkedRoots

    @Slot()
    def _doubleClickedItem(self):
        selected = self.selectedItems()
        s = selected[len(selected) -1]
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
        for s in selection :
            hier = self.getQtItemsDescendants(s)
            for h in hier: 
                if h in self._rootDict:
                    h.setCheckState(0,self._qGlobalCheckBox.checkState())
    @Slot()
    def _changedWidgetItem(self, widget, col):
        for i in range(widget.childCount()):
            child = widget.child(i)
            child.setCheckState(col,widget.checkState(col))
            

class TreeViewCategory(TreeView):  
    def __init__(self,parent):
        TreeView.__init__(self,parent) 
        self._baseNameDict = {}

    def createTree(self):
        self.clearSelection()
        self._rootDict.clear()
        self.clear()
        self.createCategoryDictionary()
        for category in self._baseNameDict: # build the QTree based on this dictionary 
            qTreeParent = QTreeWidgetItem()
            qTreeParent.setText(0, category)   
            #self._rootDict[qTreeParent] = self._baseNameDict[category] # add list of lods to the parent widget ref in the dictionary
            for obj in self._baseNameDict[category]:
                qTreeChild = QTreeWidgetItem()        
                self.updateRootWidget(obj,qTreeChild,0) 
                qTreeChild.setCheckState(0,Qt.CheckState.Unchecked)
                qTreeParent.addChild(qTreeChild) 
                self._rootDict[qTreeChild] = obj # add each object to its corresponding widget in the dict                    
            self.addTopLevelItem(qTreeParent)
        self.expandAll()

    def refreshTree(self):
        self.createTree()

    def createCategoryDictionary(self):
        roots = self.gatherSceneObjects()
        self._baseNameDict.clear()
        for r in roots: # for each base name excluding LODS
            baseName = utility.removeLODSuffix(r.name)
            if(not self._baseNameDict.has_key(baseName)):
                self._baseNameDict[baseName] = list()
        for lo in roots: # add each LOD to the correct category
            baseName = utility.removeLODSuffix(lo.name)
            if(self._baseNameDict.has_key(baseName)):
                self._baseNameDict[baseName].append(lo)
            else:
                print("{0} doesn't have a LOD0 but still has other LODs. {1} will not show in the list.".format(baseName,lo.name))

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
                if( o not in allRoots):
                    allRoots.append(o)
        return allRoots
        

#################
# TreeViewLayer #
################# 
class TreeViewLayer(TreeView):

    def __init__(self,parent):
        TreeView.__init__(self,parent) 
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
        #self.expandAll()
        #roots = self.gatherSceneObjects()
        #for r in roots:
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
    def buildQTreeLayer(self,widget,lay):
        qTreeChild = QTreeWidgetItem()
        qTreeChild.setCheckState(0,Qt.CheckState.Unchecked)
        qTreeChild.setText(0,lay.name)
        self._layerDict[qTreeChild] = lay # add widget to dictionary with actual layer as value
        childrenLayers = layer.getChildrenLayer(lay)
        
        for c in childrenLayers:
            self.buildQTreeLayer(qTreeChild,c)

        if widget is not None: # if it's not the initial call
            widget.addChild(qTreeChild) # bind new widget to parent
            return None # and we get out of the function
        else:
            return qTreeChild # only return reference to the widget when in the initial call

    def _modifyCheckBox(self):
        selection = self.selectedItems()
        for s in selection :
            hier = self.getQtItemsDescendants(s)
            s.setCheckState(0,self._qGlobalCheckBox.checkState())
            for h in hier: 
                h.setCheckState(0, self._qGlobalCheckBox.checkState())
        self.isEdited = True
            

    def intializeCheckLayers(self, layerNames):         
        for k in self._layerDict.keys():
            if k.text(0) in layerNames :
                k.setCheckState(0, Qt.CheckState.Checked)
            else:
                k.setCheckState(0, Qt.CheckState.Unchecked)
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
                if ( i not in layers):
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

    hasChanged = Signal() # custom signal
    def __init__(self,parent):
        TreeView.__init__(self, parent)
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
                if (groupID.identifier == target.text(4)): # retreive group id that we stored in the fourth column for convenience
                    found = True
                    for s in selected:
                        s.edit(group=target.text(4))
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
                if (widget.text(4) == self._groupDict[k].text(4)):
                    k.edit(newName)
                    break
        
        if(col != 0):
            self.hasChanged.emit()      

            
    def _gatherGroups(self):
        rootNode = sceneUtils.getSceneRootNode()
        groupList = userprop.getUserPropList(rootNode, const.PROP_PRESET_GROUP_LIST)
        groups = []
        if groupList is not None:
            for groupID in groupList:
                g = presetUtils.GroupObject(groupID)
                groups.append(g)
        return groups


    def _gatherSceneObjects(self):
        rootNode = sceneUtils.getSceneRootNode()
        presetList = userprop.getUserPropList(rootNode, const.PROP_PRESET_LIST)
        presets = []
        if presetList is not None:
            for presetID in presetList:
                p = presetUtils.PresetObject(presetID)
                presets.append(p)
        return presets
        
    def _createRootWidget(self, obj, offset = 1):
        qTreeWidget = QTreeWidgetItem()
        qTreeWidget.setCheckState(0, Qt.CheckState.Unchecked)
        qTreeWidget.setFlags(Qt.ItemIsDropEnabled | Qt.ItemIsEditable | Qt.ItemIsSelectable | Qt.ItemIsDragEnabled | Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
        
        self._updateRootWidget(obj,qTreeWidget,offset)
        return qTreeWidget
    
    def _updateRootWidget(self, obj, widget, offset=1):
        
        widget.setText(offset, str(obj.name))
        path = str(obj.path)
        widget.setText(offset + 1, qtUtils.truncateStringFromLeft(path, 50))
        widget.setToolTip(offset + 1,path)
        
    def _modifyCheckBox(self):
        selection = self.selectedItems()
        for s in selection :
            hier = self.getQtItemsDescendants(s)
            for h in hier: 
                h.setCheckState(0,self._qGlobalCheckBox.checkState())

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
            self.editItem(items[0],0)
      
    def createTree(self):
        self.clearSelection()
        self._rootDict.clear()
        self.clear()
        self._groupDict.clear()

        roots = self._gatherSceneObjects()
        groups = self._gatherGroups()
        if (isinstance(groups, list) and groups is not None):
            for g in groups:
                qTreeWidget = QTreeWidgetItem()
                qTreeWidget.setFlags(Qt.ItemIsDropEnabled | Qt.ItemIsEditable | Qt.ItemIsSelectable | Qt.ItemIsDragEnabled | Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
                qTreeWidget.setCheckState(0, Qt.CheckState.Unchecked)
                qTreeWidget.setText(0, str(g.name))
                qTreeWidget.setText(4, g.identifier)  # store the group id in the fourth column
                self._groupDict[g] = qTreeWidget
                self.addTopLevelItem(qTreeWidget)
        if (isinstance(roots,list) and roots is not None):
            for r in roots:            
                qTreeWidget = self._createRootWidget(obj = r, offset=0)
                self._rootDict[qTreeWidget] = r  # add widget to dictionary with object as value
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
        #newRoots = self._gatherSceneObjects()
        #newGroups = self._gatherGroups()
        #for group in newGroups:
        #    for k in self._groupDict.keys():
        #        if k.identifer == group.identifier:

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
            for k in self._groupDict.keys():
                if (item.text(4) == self._groupDict[k].text(4)):
                    selected.append(k)
                    break
        return selected

    def getCheckedPresets(self):
        selected = []
        for k in self._rootDict.keys():
            if k.checkState(0) == Qt.Checked:
                preset = self._rootDict[k]
                selected.append(preset)
        return selected



