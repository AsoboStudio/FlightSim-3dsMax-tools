import MaxPlus
from PySide2 import QtWidgets
import os
import sys

# to add module from parent folder
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

import maxsdk.node as sdknode
reload(sdknode)

def run():
    warningList = []
    sceneNodes = map(lambda x: x.GetName(), sdknode.getChildren(MaxPlus.Core.GetRootNode()))
    sceneNodes.sort(key= lambda x: x.lower())

    for i in range(len(sceneNodes) -1):
        if sceneNodes[i] == sceneNodes[i+1]:
            warningList.append(sceneNodes[i])

    if len(warningList) > 0:
        mainWindow = QtWidgets.QWidget()
        mainWindow.setContentsMargins(10, 10, 10, 10)
        verticalLayout = QtWidgets.QVBoxLayout()
        titleLabel = QtWidgets.QLabel()
        spacer = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        titleLabel.setText("There are multiple Nodes with following names.\n"
                           "Use unique name to facilitate animator's work,\n"
                           "most of the Animator Tools are based on node name ")
        titleLabel.setStyleSheet('color: red')
        listWidget = QtWidgets.QListWidget()

        for r in warningList:
            item = QtWidgets.QListWidgetItem()
            line = QtWidgets.QLineEdit()
            line.setText(r)
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
        dialog = QtWidgets.QMessageBox(text="Good,no nodes in scene with duplicated name", parent=MaxPlus.GetQMaxMainWindow())
        dialog.show()
