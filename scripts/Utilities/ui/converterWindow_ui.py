# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'e:\KittyHawk_Staging_ccreutz\ASSETS\KittyHawk_Data\Tools\3DSMAX\FlightSimPackage\src\scripts\Utilities\resources\converterWindow.ui'
#
# Created: Tue Jul  7 13:44:08 2020
#      by: pyside2-uic  running on PySide2 5.6.0a1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_XMLtoJSON(object):
    def setupUi(self, XMLtoJSON):
        XMLtoJSON.setObjectName("XMLtoJSON")
        XMLtoJSON.setWindowModality(QtCore.Qt.NonModal)
        XMLtoJSON.resize(569, 126)
        self.verticalLayout = QtWidgets.QVBoxLayout(XMLtoJSON)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_2 = QtWidgets.QLabel(XMLtoJSON)
        self.label_2.setScaledContents(False)
        self.label_2.setWordWrap(True)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(XMLtoJSON)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.lineXML = QtWidgets.QLineEdit(XMLtoJSON)
        self.lineXML.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.lineXML.setObjectName("lineXML")
        self.horizontalLayout.addWidget(self.lineXML)
        self.btnBrowseXML = QtWidgets.QToolButton(XMLtoJSON)
        self.btnBrowseXML.setObjectName("btnBrowseXML")
        self.horizontalLayout.addWidget(self.btnBrowseXML)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_3 = QtWidgets.QLabel(XMLtoJSON)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_2.addWidget(self.label_3)
        self.lineJSON = QtWidgets.QLineEdit(XMLtoJSON)
        self.lineJSON.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.lineJSON.setObjectName("lineJSON")
        self.horizontalLayout_2.addWidget(self.lineJSON)
        self.btnBrowseJSON = QtWidgets.QToolButton(XMLtoJSON)
        self.btnBrowseJSON.setObjectName("btnBrowseJSON")
        self.horizontalLayout_2.addWidget(self.btnBrowseJSON)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.btnGenerate = QtWidgets.QPushButton(XMLtoJSON)
        self.btnGenerate.setObjectName("btnGenerate")
        self.horizontalLayout_3.addWidget(self.btnGenerate)
        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.retranslateUi(XMLtoJSON)
        QtCore.QMetaObject.connectSlotsByName(XMLtoJSON)

    def retranslateUi(self, XMLtoJSON):
        XMLtoJSON.setWindowTitle(QtWidgets.QApplication.translate("XMLtoJSON", "XMLtoJSON", None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate("XMLtoJSON", "Generate a JSON file importable in the BabylonAnimationGroup tool from a legacy modeldef.xml", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("XMLtoJSON", "XML Input :", None, -1))
        self.btnBrowseXML.setText(QtWidgets.QApplication.translate("XMLtoJSON", "...", None, -1))
        self.label_3.setText(QtWidgets.QApplication.translate("XMLtoJSON", "Json Output :", None, -1))
        self.btnBrowseJSON.setText(QtWidgets.QApplication.translate("XMLtoJSON", "...", None, -1))
        self.btnGenerate.setText(QtWidgets.QApplication.translate("XMLtoJSON", "Generate JSON", None, -1))

