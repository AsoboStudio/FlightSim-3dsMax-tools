# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\KittyHawk\ASSETS\KittyHawk_Data\Tools\3DSMAX\FlightSimPackage\src\scripts\WiperTool\resources\wiperConfigItem.ui'
#
# Created: Mon Apr  6 20:01:12 2020
#      by: pyside2-uic  running on PySide2 5.6.0a1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_wiperPointsDefinition(object):
    def setupUi(self, wiperPointsDefinition):
        wiperPointsDefinition.setObjectName("wiperPointsDefinition")
        wiperPointsDefinition.resize(658, 80)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(wiperPointsDefinition.sizePolicy().hasHeightForWidth())
        wiperPointsDefinition.setSizePolicy(sizePolicy)
        wiperPointsDefinition.setMinimumSize(QtCore.QSize(0, 80))
        wiperPointsDefinition.setMaximumSize(QtCore.QSize(658, 80))
        self.horizontalLayout = QtWidgets.QHBoxLayout(wiperPointsDefinition)
        self.horizontalLayout.setContentsMargins(30, 5, 0, 5)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.wiperConfig = QtWidgets.QGroupBox(wiperPointsDefinition)
        self.wiperConfig.setObjectName("wiperConfig")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.wiperConfig)
        self.verticalLayout_2.setSpacing(2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_5 = QtWidgets.QLabel(self.wiperConfig)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_3.addWidget(self.label_5)
        self.wiperPointA = QtWidgets.QLineEdit(self.wiperConfig)
        self.wiperPointA.setObjectName("wiperPointA")
        self.horizontalLayout_3.addWidget(self.wiperPointA)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_6 = QtWidgets.QLabel(self.wiperConfig)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_4.addWidget(self.label_6)
        self.wiperPointB = QtWidgets.QLineEdit(self.wiperConfig)
        self.wiperPointB.setObjectName("wiperPointB")
        self.horizontalLayout_4.addWidget(self.wiperPointB)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.horizontalLayout.addWidget(self.wiperConfig)
        self.addConfig = QtWidgets.QPushButton(wiperPointsDefinition)
        self.addConfig.setMinimumSize(QtCore.QSize(30, 30))
        self.addConfig.setMaximumSize(QtCore.QSize(30, 30))
        self.addConfig.setObjectName("addConfig")
        self.horizontalLayout.addWidget(self.addConfig)
        self.removeConfig = QtWidgets.QPushButton(wiperPointsDefinition)
        self.removeConfig.setMinimumSize(QtCore.QSize(30, 30))
        self.removeConfig.setMaximumSize(QtCore.QSize(30, 30))
        self.removeConfig.setObjectName("removeConfig")
        self.horizontalLayout.addWidget(self.removeConfig)

        self.retranslateUi(wiperPointsDefinition)
        QtCore.QMetaObject.connectSlotsByName(wiperPointsDefinition)

    def retranslateUi(self, wiperPointsDefinition):
        wiperPointsDefinition.setWindowTitle(QtWidgets.QApplication.translate("wiperPointsDefinition", "wiper Points Definition", None, -1))
        self.wiperConfig.setTitle(QtWidgets.QApplication.translate("wiperPointsDefinition", "WiperItem", None, -1))
        self.label_5.setText(QtWidgets.QApplication.translate("wiperPointsDefinition", "WiperPointA", None, -1))
        self.label_6.setText(QtWidgets.QApplication.translate("wiperPointsDefinition", "WiperPointB", None, -1))
        self.addConfig.setText(QtWidgets.QApplication.translate("wiperPointsDefinition", "+", None, -1))
        self.removeConfig.setText(QtWidgets.QApplication.translate("wiperPointsDefinition", "-", None, -1))

