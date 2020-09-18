import sys
import os
import MaxPlus
import pymxs
import re
import itertools
from PySide2 import QtWidgets
from PySide2 import QtGui

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path)
sys.path.append(os.path.join(os.path.dirname(dir_path), os.pardir))

import layer_validation
from maxsdk import utility as sdk_utility
from maxsdk import layer as sdkLayer
import maxsdk.node as sdknode
import node_validation

rt = pymxs.runtime

report = []

def getLodsInScene():
    result = []
    for i in range(10):
        lodLayer = MaxPlus.LayerManager.GetLayer("x" + str(i))
        if lodLayer:
            result.append(lodLayer)
    return result

def stripNameSpace(name):
    return re.sub(r".*?:","",name)

def stripLod(name):
    return re.sub(r"x[0-9]_", "", name)

def getBinomialOfPrevLod(node):
    result = re.search('x([0-9])_', node.GetName())
    lodNumber = int(result.group(1))
    nextLodPart = "x{0}_".format(lodNumber -1)
    next =re.sub("x([0-9])_",nextLodPart,node.GetName())
    nextNode = MaxPlus.INode.GetINodeByName(next)
    if not nextNode or nextNode.GetName() == node.GetName():
        return None
    else:
        return nextNode



def isTreeConsistent(source,next):
    global report
    prev = getBinomialOfPrevLod(next)
    if prev is None or prev.GetName() != source.GetName():
        report.append(next.GetName())
    else:
        src_children = list(sdknode.getChildren(source))
        src_children.sort(key=lambda x: str(x.GetName()).lower())

        target_children = list(sdknode.getChildren(next))
        target_children.sort(key=lambda x: str(x.GetName()).lower())

        for f, b in itertools.izip(src_children, target_children):
            isTreeConsistent(f, b)


def isNextLayerConsistent(sourceLayer, nextLayer):
    global report
    report.append("Report of layer {0} over {1}".format(nextLayer.GetName(),sourceLayer.GetName()))
    rtNextLayer = rt.LayerManager.getLayerFromName(nextLayer.GetName())
    rtSourceLayer = rt.LayerManager.getLayerFromName(sourceLayer.GetName())
    nodesInNextLod = sdkLayer.getAllNodeInLayerHierarchy(rtNextLayer)
    nodesInSourceLod = sdkLayer.getAllNodeInLayerHierarchy(rtSourceLayer)
    sourceNodesRoots = sdknode.getBaseNodes(nodesInSourceLod)
    nextNodesRoots = sdknode.getBaseNodes(nodesInNextLod)
    for n in nextNodesRoots:
        prev = getBinomialOfPrevLod(n)
        if prev is not None and prev in sourceNodesRoots:
            isTreeConsistent(prev,n)
        else:
            report.append(n.GetName())

def checkLODsHierarchy():
    lodsLayers = getLodsInScene()
    if lodsLayers:
        for i in range(len(lodsLayers) - 1):
            sourceLayer = lodsLayers[i]
            targetLayer = lodsLayers[i + 1]
            isNextLayerConsistent(sourceLayer, targetLayer)


def run():
    if not layer_validation.check_layers_names(silent=True):
        dialog = QtWidgets.QMessageBox(text="Layers name not valid", parent=MaxPlus.GetQMaxMainWindow())
        dialog.show()
    else:
        checkLODsHierarchy()
        if len(report) > 2:
            mainWindow = QtWidgets.QWidget()
            mainWindow.setContentsMargins(10, 10, 10, 10)
            verticalLayout = QtWidgets.QVBoxLayout()
            titleLabel = QtWidgets.QLabel()
            spacer = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
            titleLabel.setText(
                "Following nodes are not present in the previous LOD or they have a different position in hierachy")
            titleLabel.setStyleSheet('color: red')
            listWidget = QtWidgets.QListWidget()

            for r in report:
                item = QtWidgets.QListWidgetItem()
                line = QtWidgets.QLineEdit()
                line.setText(r)
                if "Report" in r:
                    line.setStyleSheet('color: yellow')
                line.setReadOnly(True)
                listWidget.addItem(item)
                listWidget.setItemWidget(item, line)

            mainWindow.setLayout(verticalLayout)
            verticalLayout.addWidget(titleLabel)
            verticalLayout.addItem(spacer)
            verticalLayout.addWidget(listWidget)
            MaxPlus.AttachQWidgetToMax(mainWindow)
            mainWindow.show()
        else:
            dialog = QtWidgets.QMessageBox(text="LOD hierarchy validated", parent=MaxPlus.GetQMaxMainWindow())
            dialog.show()

