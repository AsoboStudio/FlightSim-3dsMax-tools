# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\lpierabella\Documents\3dsMax\scripts\KittyHawk\FlightSimPackage\src\scripts\EnvironmentLODsExporter\resources\mainwindow.ui'
#
# Created: Mon Jan 27 18:08:29 2020
#      by: pyside2-uic  running on PySide2 5.6.0a1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_folderSelectorWidget(object):
    def setupUi(self, folderSelectorWidget):
        folderSelectorWidget.setObjectName("folderSelectorWidget")
        folderSelectorWidget.resize(820, 43)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(folderSelectorWidget.sizePolicy().hasHeightForWidth())
        folderSelectorWidget.setSizePolicy(sizePolicy)
        self.verticalLayout = QtWidgets.QVBoxLayout(folderSelectorWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label = QtWidgets.QLabel(folderSelectorWidget)
        self.label.setMinimumSize(QtCore.QSize(100, 0))
        self.label.setMaximumSize(QtCore.QSize(100, 16777215))
        self.label.setObjectName("label")
        self.horizontalLayout_4.addWidget(self.label)
        self.exportPath = QtWidgets.QLineEdit(folderSelectorWidget)
        self.exportPath.setObjectName("exportPath")
        self.horizontalLayout_4.addWidget(self.exportPath)
        self.browseExportBtn = QtWidgets.QPushButton(folderSelectorWidget)
        self.browseExportBtn.setMaximumSize(QtCore.QSize(50, 16777215))
        self.browseExportBtn.setObjectName("browseExportBtn")
        self.horizontalLayout_4.addWidget(self.browseExportBtn)
        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.retranslateUi(folderSelectorWidget)
        QtCore.QMetaObject.connectSlotsByName(folderSelectorWidget)

    def retranslateUi(self, folderSelectorWidget):
        folderSelectorWidget.setWindowTitle(QtWidgets.QApplication.translate("folderSelectorWidget", "Environments LODs", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("folderSelectorWidget", "Export Path", None, -1))
        self.browseExportBtn.setText(QtWidgets.QApplication.translate("folderSelectorWidget", "Browse", None, -1))

