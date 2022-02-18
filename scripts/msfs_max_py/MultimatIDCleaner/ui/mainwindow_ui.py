# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\P4v\KittyHawk_WS2\ASSETS\KittyHawk_Data\Tools\3DSMAX\FlightSimPackage\src\scripts\MultimatIDCleaner\resources\mainwindow.ui',
# licensing of 'd:\P4v\KittyHawk_WS2\ASSETS\KittyHawk_Data\Tools\3DSMAX\FlightSimPackage\src\scripts\MultimatIDCleaner\resources\mainwindow.ui' applies.
#
# Created: Wed Mar 31 10:07:35 2021
#      by: pyside2-uic  running on PySide2 5.12.5
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_MultimatCleaner(object):
    def setupUi(self, MultimatCleaner):
        MultimatCleaner.setObjectName("MultimatCleaner")
        MultimatCleaner.resize(394, 208)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MultimatCleaner.sizePolicy().hasHeightForWidth())
        MultimatCleaner.setSizePolicy(sizePolicy)
        MultimatCleaner.setMinimumSize(QtCore.QSize(394, 208))
        MultimatCleaner.setMaximumSize(QtCore.QSize(394, 208))
        MultimatCleaner.setFocusPolicy(QtCore.Qt.StrongFocus)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("C:/Users/tbourille/Downloads/a-asobo-blue.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MultimatCleaner.setWindowIcon(icon)
        self.Title = QtWidgets.QLabel(MultimatCleaner)
        self.Title.setGeometry(QtCore.QRect(0, 10, 391, 41))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Title.sizePolicy().hasHeightForWidth())
        self.Title.setSizePolicy(sizePolicy)
        self.Title.setMinimumSize(QtCore.QSize(391, 41))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.Title.setFont(font)
        self.Title.setAlignment(QtCore.Qt.AlignCenter)
        self.Title.setObjectName("Title")
        self.pushButton = QtWidgets.QPushButton(MultimatCleaner)
        self.pushButton.setGeometry(QtCore.QRect(90, 60, 211, 41))
        self.pushButton.setObjectName("pushButton")
        self.textBrowser = QtWidgets.QTextBrowser(MultimatCleaner)
        self.textBrowser.setGeometry(QtCore.QRect(90, 130, 211, 71))
        self.textBrowser.setObjectName("textBrowser")
        self.label = QtWidgets.QLabel(MultimatCleaner)
        self.label.setGeometry(QtCore.QRect(0, 100, 391, 30))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")

        self.retranslateUi(MultimatCleaner)
        QtCore.QMetaObject.connectSlotsByName(MultimatCleaner)

    def retranslateUi(self, MultimatCleaner):
        MultimatCleaner.setWindowTitle(QtWidgets.QApplication.translate("MultimatCleaner", "MultimatCleaner", None, -1))
        self.Title.setText(QtWidgets.QApplication.translate("MultimatCleaner", "Multimat ID Cleaner", None, -1))
        self.pushButton.setText(QtWidgets.QApplication.translate("MultimatCleaner", "Clean Multimat ID of selected objects", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("MultimatCleaner", "Result:", None, -1))

