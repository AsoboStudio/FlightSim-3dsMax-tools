# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\lpierabella\Documents\3dsMax\scripts\KittyHawk\FlightSimPackage\src\scripts\AnimationExporter\resources\mainwindow.ui'
#
# Created: Fri Feb 28 18:22:06 2020
#      by: pyside2-uic  running on PySide2 5.6.0a1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(820, 153)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.verticalLayout = QtWidgets.QVBoxLayout(MainWindow)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.exportTypeLbl = QtWidgets.QLabel(MainWindow)
        self.exportTypeLbl.setMaximumSize(QtCore.QSize(100, 16777215))
        self.exportTypeLbl.setObjectName("exportTypeLbl")
        self.horizontalLayout_2.addWidget(self.exportTypeLbl)
        self.exportTypeCmb = QtWidgets.QComboBox(MainWindow)
        self.exportTypeCmb.setObjectName("exportTypeCmb")
        self.exportTypeCmb.addItem("")
        self.exportTypeCmb.addItem("")
        self.exportTypeCmb.addItem("")
        self.horizontalLayout_2.addWidget(self.exportTypeCmb)
        self.bakeAnimChk = QtWidgets.QCheckBox(MainWindow)
        self.bakeAnimChk.setMaximumSize(QtCore.QSize(150, 16777215))
        self.bakeAnimChk.setObjectName("bakeAnimChk")
        self.horizontalLayout_2.addWidget(self.bakeAnimChk)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label = QtWidgets.QLabel(MainWindow)
        self.label.setMinimumSize(QtCore.QSize(100, 0))
        self.label.setMaximumSize(QtCore.QSize(100, 16777215))
        self.label.setObjectName("label")
        self.horizontalLayout_4.addWidget(self.label)
        self.exportFolderCmb = QtWidgets.QComboBox(MainWindow)
        self.exportFolderCmb.setObjectName("exportFolderCmb")
        self.horizontalLayout_4.addWidget(self.exportFolderCmb)
        self.browseExportBtn = QtWidgets.QPushButton(MainWindow)
        self.browseExportBtn.setMaximumSize(QtCore.QSize(50, 16777215))
        self.browseExportBtn.setObjectName("browseExportBtn")
        self.horizontalLayout_4.addWidget(self.browseExportBtn)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.exportBtn = QtWidgets.QPushButton(MainWindow)
        self.exportBtn.setMinimumSize(QtCore.QSize(100, 40))
        self.exportBtn.setObjectName("exportBtn")
        self.horizontalLayout_3.addWidget(self.exportBtn)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.logger = QtWidgets.QLabel(MainWindow)
        self.logger.setText("")
        self.logger.setObjectName("logger")
        self.verticalLayout.addWidget(self.logger)
        spacerItem1 = QtWidgets.QSpacerItem(20, 46, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "FlightSim Batch Exporter", None, -1))
        self.exportTypeLbl.setText(QtWidgets.QApplication.translate("MainWindow", "Export type", None, -1))
        self.exportTypeCmb.setItemText(0, QtWidgets.QApplication.translate("MainWindow", "Animation", None, -1))
        self.exportTypeCmb.setItemText(1, QtWidgets.QApplication.translate("MainWindow", "Model", None, -1))
        self.exportTypeCmb.setItemText(2, QtWidgets.QApplication.translate("MainWindow", "All", None, -1))
        self.bakeAnimChk.setText(QtWidgets.QApplication.translate("MainWindow", "Bake Animations", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("MainWindow", "Export Path", None, -1))
        self.browseExportBtn.setText(QtWidgets.QApplication.translate("MainWindow", "Browse", None, -1))
        self.exportBtn.setText(QtWidgets.QApplication.translate("MainWindow", "Export", None, -1))

