# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\KittyHawk1\ASSETS\KittyHawk_Data\Tools\3DSMAX\FlightSimPackage\src\scripts\Utilities\ConvertTextureToPoligonMesh\resources\convertTextureToMesh.ui'
#
# Created: Fri Jul  9 17:35:56 2021
#      by: pyside2-uic  running on PySide2 5.6.0a1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_ConvertTextureToMesh(object):
    def setupUi(self, ConvertTextureToMesh):
        ConvertTextureToMesh.setObjectName("ConvertTextureToMesh")
        ConvertTextureToMesh.resize(585, 114)
        ConvertTextureToMesh.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.verticalLayout = QtWidgets.QVBoxLayout(ConvertTextureToMesh)
        self.verticalLayout.setObjectName("verticalLayout")
        self.info_lbl = QtWidgets.QLabel(ConvertTextureToMesh)
        self.info_lbl.setObjectName("info_lbl")
        self.verticalLayout.addWidget(self.info_lbl)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.path_lbl = QtWidgets.QLabel(ConvertTextureToMesh)
        self.path_lbl.setText("")
        self.path_lbl.setObjectName("path_lbl")
        self.horizontalLayout.addWidget(self.path_lbl)
        self.browse_btn = QtWidgets.QPushButton(ConvertTextureToMesh)
        self.browse_btn.setMaximumSize(QtCore.QSize(100, 16777215))
        self.browse_btn.setObjectName("browse_btn")
        self.horizontalLayout.addWidget(self.browse_btn)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.useAlpha_chb = QtWidgets.QCheckBox(ConvertTextureToMesh)
        self.useAlpha_chb.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.useAlpha_chb.setChecked(True)
        self.useAlpha_chb.setTristate(False)
        self.useAlpha_chb.setObjectName("useAlpha_chb")
        self.verticalLayout.addWidget(self.useAlpha_chb)
        self.convertToMesh_btn = QtWidgets.QPushButton(ConvertTextureToMesh)
        self.convertToMesh_btn.setObjectName("convertToMesh_btn")
        self.verticalLayout.addWidget(self.convertToMesh_btn)

        self.retranslateUi(ConvertTextureToMesh)
        QtCore.QMetaObject.connectSlotsByName(ConvertTextureToMesh)

    def retranslateUi(self, ConvertTextureToMesh):
        ConvertTextureToMesh.setWindowTitle(QtWidgets.QApplication.translate("ConvertTextureToMesh", "Convert Texture To Mesh", None, -1))
        self.info_lbl.setText(QtWidgets.QApplication.translate("ConvertTextureToMesh", "Define a texture with alpha channel and select the objects you want to convert", None, -1))
        self.browse_btn.setText(QtWidgets.QApplication.translate("ConvertTextureToMesh", "Browse Texture", None, -1))
        self.useAlpha_chb.setText(QtWidgets.QApplication.translate("ConvertTextureToMesh", "Use Material Alpha", None, -1))
        self.convertToMesh_btn.setText(QtWidgets.QApplication.translate("ConvertTextureToMesh", "Convert To Mesh", None, -1))

