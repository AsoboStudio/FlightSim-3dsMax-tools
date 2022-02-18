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

class TreeViewCategory(TreeView):
    """Class to gather scene node, sort them by LOD and put them in a QTreeWidget. Widget are connected to Scene Node using the Dictionary _rootDict
    """
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

    def filterTree(self, filterr = ""):
        if filterr != "":    
            #InitVars
            self.clearSelection()
            self._rootDict.clear()
            self.clear()
            self.createCategoryDictionary()

            for category in self._baseNameDict:  # build the QTree based on this dictionary
                qTreeParent = QTreeWidgetItem()
                qTreeParent.setText(0, category)
                isRelevant = False
                for obj in self._baseNameDict[category]:
                    if filterr in obj.name:
                        qTreeChild = QTreeWidgetItem()
                        self.updateRootWidget(obj, qTreeChild, 0)
                        qTreeChild.setCheckState(0, Qt.CheckState.Unchecked)
                        qTreeParent.addChild(qTreeChild)
                        # add each object to its corresponding widget in the dict
                        self._rootDict[qTreeChild] = obj
                        isRelevant = True
                if isRelevant:
                    self.addTopLevelItem(qTreeParent)

            self.expandAll()
        else:
            self.refreshTree()

    def refreshTree(self):
        self.createTree()

    def createCategoryDictionary(self):
        roots = self.gatherSceneObjects()
        self._baseNameDict.clear()
        for r in roots:  # for each base name excluding LODS
            baseName = utility.removeLODSuffix(r.name)
            if(baseName not in self._baseNameDict):
                self._baseNameDict[baseName] = list()
        for lo in roots:  # add each LOD to the correct category
            baseName = utility.removeLODSuffix(lo.name)
            if(baseName in self._baseNameDict):
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