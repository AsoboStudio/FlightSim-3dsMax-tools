"""Module to handle PySide2 QTreeWidget in the 3dsMax context. 
"""
import os

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from MultiExporter.view.treeView import TreeView
from maxsdk import layer, qtUtils, sceneUtils, userprop, utility
from pymxs import runtime as rt

class TreeViewName(TreeView):
    """Class to gather scene node name duplicates, and put them in a QTreeWidget. Widget are connected to Scene Node using the Dictionary _rootDict
    """
    def __init__(self, parent):
        TreeView.__init__(self, parent)
        self._baseNameDict = {}

    def createTree(self, _nameDic):
        self.clearSelection()
        self._rootDict.clear()
        self.clear()

        for nD in _nameDic:
            qTreeParent = QTreeWidgetItem()
            qTreeParent.setText(0, nD.OrigName)
            for doubles in nD.DoublesNames:
                qTreeChild = QTreeWidgetItem()
                qTreeChild.setText(0,doubles.name)
                qTreeChild.setCheckState(0,Qt.CheckState.Unchecked)
                qTreeParent.addChild(qTreeChild)
                self._rootDict[qTreeChild] = doubles
            self.addTopLevelItem(qTreeParent)
        self.expandAll()

    def getNodebyQTItem(self, qtItem):
        for k in self._rootDict.keys():
            if k is qtItem:
                return self._rootDict[k]
        print("No Node from this Qt item")

    def getCheckedNodes(self):
        selected = []
        for k in self._rootDict.keys():
            if k.checkState(0) == Qt.Checked:
                Node = self._rootDict[k]
                selected.append(Node)
        return selected

    def getCheckedQTItem(self):
        selected = []
        for k in self._rootDict.keys():
            if k.checkState(0) == Qt.Checked:
                selected.append(k)
        return selected
    
    def getAllQTItems(self):
        result = []
        for k in self._rootDict.keys():
            result.append(k)
        #print("All Qt Items : {0}".format(result))
        return result

    def getFilledQtitems(self):
        AllLayers = self.getAllQTItems()
        filledLayers = []
        for lay in AllLayers:
            if lay.text(1) != "":
                filledLayers.append(lay)
        return filledLayers


    def refreshTree(self):
        self.createTree()