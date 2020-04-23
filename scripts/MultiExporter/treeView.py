import os
import sys

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from maxsdk import sceneUtils, utility, userprop, layer

from pymxs import runtime as rt

class TreeView(): 

    def __init__(self,qTreeView,qGlobalCheckBox=None):
        self._qTreeView = qTreeView
        self._showOnlyExportable = True
        self._showOnlyVisible = False
        self._showOnlyLODs = False
        if(qTreeView):
            self._rootDict = {}
            self._qTreeView.setColumnWidth(0,240)
            self._qTreeView.setColumnWidth(1,40)
            self._qTreeView.setColumnWidth(2,40)   
            self._qTreeView.setSortingEnabled(True)
            self._qTreeView.sortItems(0,Qt.SortOrder.AscendingOrder)
            self._qTreeView.itemSelectionChanged.connect(lambda: self._selectionChanged())
            self._qTreeView.itemDoubleClicked.connect(lambda: self._doubleClickedItemLOD())    
        if(qGlobalCheckBox):
            self._qGlobalCheckBox = qGlobalCheckBox
            self._qGlobalCheckBox.setTristate(False)
            self._qGlobalCheckBox.stateChanged.connect(lambda: self._modifyCheckBox())    

    def gatherSceneObjects(self):
        roots = sceneUtils.getAllRoots(sceneUtils.getAllObjects())     
        if(self._showOnlyExportable):   
            roots = sceneUtils.filterObjectsWithUserProperty(roots, "Exp") # only object ready for export
        if(self._showOnlyVisible):
            roots = sceneUtils.filterObjectsVisible(roots)
        if(self._showOnlyLODs):
            roots = sceneUtils.filterLODLevel(roots,"[0-9]+")
        return roots

    def createTree(self):
        self._qTreeView.clearSelection()
        self._rootDict.clear()
        self._qTreeView.clear()
        roots = self.gatherSceneObjects()
        for r in roots:            
            qTreeWidget = self.createRootWidget(obj = r, offset=0)
            self._rootDict[qTreeWidget] = r # add widget to dictionary with object as value
            self._qTreeView.addTopLevelItem(qTreeWidget)
        self._qTreeView.expandAll()

    def refreshTree(self):
        roots = self.gatherSceneObjects()
        for r in roots :
            if( r not in self._rootDict.values()):
                qTreeWidget = self.createRootWidget(r,0)
                self._rootDict[qTreeWidget] = r # add widget to dictionary with object as value
                self._qTreeView.addTopLevelItem(qTreeWidget)

        # search for object in the tool list not in the scene anymore   
        # do the search backward because we remove objects from the list as we go through
        for i in reversed(range(len(self._rootDict.values()))): 
            value = self._rootDict.values()[i]
            key = self._rootDict.keys()[i]
            if( value not in roots ): # if the object in the list not in the scene anymore get rid of it
                self._qTreeView.takeTopLevelItem(self._qTreeView.indexOfTopLevelItem(key))
                self._rootDict.pop(key)
            else: # else update the path and content
                try:
                    self.updateRootWidget(value,key,0)
                except:
                    print "cleaning up old values"
                    self._qTreeView.takeTopLevelItem(self._qTreeView.indexOfTopLevelItem(key))
                    self._rootDict.pop(key)


    def getSelectedRootList(self):
        selectedRoots = []
        for i in self._qTreeView.selectedItems() :
            selectedRoots.append(self._rootDict[i])
        return selectedRoots

    def getAllRootsList(self):
        allRoots = []
        for v in self._rootDict.values():
            if(v not in allRoots):
                allRoots.append(v)
        return allRoots        

    def getSelectedQtItems(self):
        return self._qTreeView.selectedItems()

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
        path = rt.getUserProp(obj, "Exp")
        widget.setText(offset, obj.name)
        widget.setText(offset+1, unicode(rt.getUserProp(obj, "flightsim_lod_value")))
        widget.setText(offset+2,str(rt.getUserProp(obj, "flightsim_flatten")))
        widget.setText(offset+3, path)
        widget.setTextColor(offset, "#FFAAAA" if path == None or path == "" else "#AAFFAA")


    def getCheckedRootList(self):
        checkedRoots = []
        for i in self._rootDict.keys():
            if i.checkState(0) == Qt.Checked:
                checkedRoots.append(self._rootDict[i])
        return checkedRoots

    @Slot()
    def _doubleClickedItemLOD(self):
        selected = self._qTreeView.selectedItems()
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
        selection = self._qTreeView.selectedItems()
        for s in selection :
            if s.childCount() == 0:
                s.setCheckState(0,self._qGlobalCheckBox.checkState())
            else:
                for i in range(s.childCount()):
                    c = s.child(i)
                    c.setCheckState(0,self._qGlobalCheckBox.checkState())

####################
# TreeViewCategory #
####################

class TreeViewCategory(TreeView):  
    def __init__(self,qTreeView,qGlobalCheckBox=None):
        TreeView.__init__(self,qTreeView,qGlobalCheckBox) 
        if(qTreeView):
            self._baseNameDict = {}

    def createTree(self):
        self._qTreeView.clearSelection()
        self._rootDict.clear()
        self._qTreeView.clear()
        self.createCategoryDictionary()
        for category in self._baseNameDict: # build the QTree based on this dictionary 
            qTreeParent = QTreeWidgetItem()
            qTreeParent.setText(0, category)   
            self._rootDict[qTreeParent] = self._baseNameDict[category] # add list of lods to the parent widget ref in the dictionary
            for obj in self._baseNameDict[category]:
                qTreeChild = QTreeWidgetItem()        
                self.updateRootWidget(obj,qTreeChild,0) 
                qTreeChild.setCheckState(0,Qt.CheckState.Unchecked)
                qTreeParent.addChild(qTreeChild) 
                self._rootDict[qTreeChild] = obj # add each object to its corresponding widget in the dict                    
            self._qTreeView.addTopLevelItem(qTreeParent)
        self._qTreeView.expandAll()

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
        for selectedItem in self._qTreeView.selectedItems():
            baseName = selectedItem.text(0)
            if(selectedItem.parent()):
                baseName = selectedItem.parent().text(0)
            if(baseName not in selectedCategory):
                selectedCategory.append(baseName)
        return selectedCategory


    def getSelectedRootList(self):
        selectedRoots = []
        for selectedItem in self._qTreeView.selectedItems() : 
            root = self._rootDict[selectedItem]
            if(len(root) > 0):
                for r in root :
                    if(r not in selectedRoots):
                        selectedRoots.append(r)
            else:
               if(root not in selectedRoots):
                   selectedRoots.append(root)
        return selectedRoots

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

    def __init__(self,qTreeView,qGlobalCheckBox=None):
        TreeView.__init__(self,qTreeView,qGlobalCheckBox) 
        if(qTreeView):
            self._layerDict = {}

    def gatherLayers(self):
        return layer.getAllRootLayer()

    def createTree(self):
        layers = self.gatherLayers()
        self._qTreeView.clear()
        self._rootDict.clear()
        self._layerDict.clear()
        for l in layers:
            qTreeWidget = self.buildQTreeLayer(None,l)
            self._qTreeView.addTopLevelItem(qTreeWidget)
        self._qTreeView.expandAll()
        roots = self.gatherSceneObjects()
        for r in roots:
            for k in self._layerDict.keys():
                v = self._layerDict[k]
                if(v == r.layer):
                    qObjectChild = self.createRootWidget(r,0)
                    k.addChild(qObjectChild)
                    self._rootDict[qObjectChild] = r
                    break

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

    def getSelectedRootList(self):
        selectedRoots = []
        for item in self._qTreeView.selectedItems() :
            items = self.getQtItemsDescendants(item)
            for i in items:
                if(self._rootDict.has_key(i)):
                    obj = self._rootDict[i]
                    if(obj not in selectedRoots):
                        selectedRoots.append(obj)        
        return selectedRoots

    @Slot()
    def _selectionChanged(self):
        selection = self.getSelectedRootList()
        selection = sceneUtils.getDescendantsOfMultiple(selection)
        rt.select(selection)
