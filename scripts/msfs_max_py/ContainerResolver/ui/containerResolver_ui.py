# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\KittyHawk1\ASSETS\KittyHawk_Data\Tools\3DSMAX\FlightSimPackage\src\scripts\Utilities\ContainerResolver\resources\containerResolver.ui'
#
# Created: Thu Jul  8 18:14:04 2021
#      by: pyside2-uic  running on PySide2 5.6.0a1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_ContainerResolver(object):
    def setupUi(self, ContainerResolver):
        ContainerResolver.setObjectName("ContainerResolver")
        ContainerResolver.resize(1759, 34)
        self.horizontalLayout = QtWidgets.QHBoxLayout(ContainerResolver)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.name_lbl = QtWidgets.QLabel(ContainerResolver)
        self.name_lbl.setObjectName("name_lbl")
        self.horizontalLayout.addWidget(self.name_lbl)
        self.line_3 = QtWidgets.QFrame(ContainerResolver)
        self.line_3.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.horizontalLayout.addWidget(self.line_3)
        self.status_lbl = QtWidgets.QLabel(ContainerResolver)
        self.status_lbl.setMaximumSize(QtCore.QSize(100, 16777215))
        self.status_lbl.setObjectName("status_lbl")
        self.horizontalLayout.addWidget(self.status_lbl)
        self.line_2 = QtWidgets.QFrame(ContainerResolver)
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.horizontalLayout.addWidget(self.line_2)
        self.path_lbl = QtWidgets.QLabel(ContainerResolver)
        self.path_lbl.setObjectName("path_lbl")
        self.horizontalLayout.addWidget(self.path_lbl)
        self.line = QtWidgets.QFrame(ContainerResolver)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout.addWidget(self.line)
        self.info_lbl = QtWidgets.QLabel(ContainerResolver)
        self.info_lbl.setObjectName("info_lbl")
        self.horizontalLayout.addWidget(self.info_lbl)

        self.retranslateUi(ContainerResolver)
        QtCore.QMetaObject.connectSlotsByName(ContainerResolver)

    def retranslateUi(self, ContainerResolver):
        ContainerResolver.setWindowTitle(QtWidgets.QApplication.translate("ContainerResolver", "ContainerResolver", None, -1))
        self.name_lbl.setText(QtWidgets.QApplication.translate("ContainerResolver", "TextLabel", None, -1))
        self.status_lbl.setText(QtWidgets.QApplication.translate("ContainerResolver", "TextLabel", None, -1))
        self.path_lbl.setText(QtWidgets.QApplication.translate("ContainerResolver", "TextLabel", None, -1))
        self.info_lbl.setText(QtWidgets.QApplication.translate("ContainerResolver", "TextLabel", None, -1))

