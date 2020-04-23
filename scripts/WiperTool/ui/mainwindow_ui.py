# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\KittyHawk\ASSETS\KittyHawk_Data\Tools\3DSMAX\FlightSimPackage\src\scripts\WiperTool\resources\mainwindow.ui'
#
# Created: Mon Apr  6 20:01:12 2020
#      by: pyside2-uic  running on PySide2 5.6.0a1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_WiperMaskGenerator(object):
    def setupUi(self, WiperMaskGenerator):
        WiperMaskGenerator.setObjectName("WiperMaskGenerator")
        WiperMaskGenerator.resize(622, 764)
        self.horizontalLayout = QtWidgets.QHBoxLayout(WiperMaskGenerator)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.scrollArea = QtWidgets.QScrollArea(WiperMaskGenerator)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy)
        self.scrollArea.setMinimumSize(QtCore.QSize(0, 0))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, -68, 583, 378))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollAreaWidgetContents_2.sizePolicy().hasHeightForWidth())
        self.scrollAreaWidgetContents_2.setSizePolicy(sizePolicy)
        self.scrollAreaWidgetContents_2.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.formLayout_3 = QtWidgets.QFormLayout(self.scrollAreaWidgetContents_2)
        self.formLayout_3.setObjectName("formLayout_3")
        self.groupBox = QtWidgets.QGroupBox(self.scrollAreaWidgetContents_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setMinimumSize(QtCore.QSize(0, 360))
        self.groupBox.setMaximumSize(QtCore.QSize(16777215, 360))
        self.groupBox.setBaseSize(QtCore.QSize(0, 500))
        self.groupBox.setObjectName("groupBox")
        self.formLayout_2 = QtWidgets.QFormLayout(self.groupBox)
        self.formLayout_2.setVerticalSpacing(0)
        self.formLayout_2.setObjectName("formLayout_2")
        self.label_6 = QtWidgets.QLabel(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)
        self.label_6.setMinimumSize(QtCore.QSize(0, 40))
        self.label_6.setMaximumSize(QtCore.QSize(1999, 37))
        self.label_6.setTextFormat(QtCore.Qt.AutoText)
        self.label_6.setScaledContents(False)
        self.label_6.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_6.setWordWrap(True)
        self.label_6.setObjectName("label_6")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.SpanningRole, self.label_6)
        self.sampleImage = QtWidgets.QLabel(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sampleImage.sizePolicy().hasHeightForWidth())
        self.sampleImage.setSizePolicy(sizePolicy)
        self.sampleImage.setMinimumSize(QtCore.QSize(384, 293))
        self.sampleImage.setMaximumSize(QtCore.QSize(384, 293))
        self.sampleImage.setBaseSize(QtCore.QSize(1, 1))
        self.sampleImage.setFrameShape(QtWidgets.QFrame.Box)
        self.sampleImage.setText("")
        self.sampleImage.setPixmap(QtGui.QPixmap("../ui/PlacementInfo.jpg"))
        self.sampleImage.setScaledContents(True)
        self.sampleImage.setAlignment(QtCore.Qt.AlignCenter)
        self.sampleImage.setWordWrap(False)
        self.sampleImage.setObjectName("sampleImage")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.sampleImage)
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.SpanningRole, self.groupBox)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents_2)
        self.verticalLayout.addWidget(self.scrollArea)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setContentsMargins(10, -1, 10, -1)
        self.gridLayout.setObjectName("gridLayout")
        self.initalAnimFrame = QtWidgets.QLineEdit(WiperMaskGenerator)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.initalAnimFrame.sizePolicy().hasHeightForWidth())
        self.initalAnimFrame.setSizePolicy(sizePolicy)
        self.initalAnimFrame.setMaximumSize(QtCore.QSize(64, 16777215))
        self.initalAnimFrame.setObjectName("initalAnimFrame")
        self.gridLayout.addWidget(self.initalAnimFrame, 0, 1, 1, 1)
        self.finalAnimFrame = QtWidgets.QLineEdit(WiperMaskGenerator)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.finalAnimFrame.sizePolicy().hasHeightForWidth())
        self.finalAnimFrame.setSizePolicy(sizePolicy)
        self.finalAnimFrame.setMaximumSize(QtCore.QSize(64, 16777215))
        self.finalAnimFrame.setObjectName("finalAnimFrame")
        self.gridLayout.addWidget(self.finalAnimFrame, 2, 1, 1, 1)
        self.midlleAnimationFrame = QtWidgets.QLineEdit(WiperMaskGenerator)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.midlleAnimationFrame.sizePolicy().hasHeightForWidth())
        self.midlleAnimationFrame.setSizePolicy(sizePolicy)
        self.midlleAnimationFrame.setMaximumSize(QtCore.QSize(64, 16777215))
        self.midlleAnimationFrame.setObjectName("midlleAnimationFrame")
        self.gridLayout.addWidget(self.midlleAnimationFrame, 1, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 2, 2, 1, 1)
        self.label_10 = QtWidgets.QLabel(WiperMaskGenerator)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_10.sizePolicy().hasHeightForWidth())
        self.label_10.setSizePolicy(sizePolicy)
        self.label_10.setMinimumSize(QtCore.QSize(80, 0))
        self.label_10.setMaximumSize(QtCore.QSize(16777215, 80))
        self.label_10.setObjectName("label_10")
        self.gridLayout.addWidget(self.label_10, 4, 0, 1, 1)
        self.filePathButton = QtWidgets.QPushButton(WiperMaskGenerator)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.filePathButton.sizePolicy().hasHeightForWidth())
        self.filePathButton.setSizePolicy(sizePolicy)
        self.filePathButton.setMaximumSize(QtCore.QSize(16777215, 80))
        self.filePathButton.setObjectName("filePathButton")
        self.gridLayout.addWidget(self.filePathButton, 4, 2, 1, 1)
        self.windshieldNodeName = QtWidgets.QLineEdit(WiperMaskGenerator)
        self.windshieldNodeName.setObjectName("windshieldNodeName")
        self.gridLayout.addWidget(self.windshieldNodeName, 3, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(WiperMaskGenerator)
        self.label_2.setMaximumSize(QtCore.QSize(16777215, 20))
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.label_9 = QtWidgets.QLabel(WiperMaskGenerator)
        self.label_9.setMaximumSize(QtCore.QSize(16777215, 20))
        self.label_9.setObjectName("label_9")
        self.gridLayout.addWidget(self.label_9, 1, 0, 1, 1)
        self.label_11 = QtWidgets.QLabel(WiperMaskGenerator)
        self.label_11.setMinimumSize(QtCore.QSize(80, 0))
        self.label_11.setObjectName("label_11")
        self.gridLayout.addWidget(self.label_11, 3, 0, 1, 1)
        self.label_8 = QtWidgets.QLabel(WiperMaskGenerator)
        self.label_8.setMaximumSize(QtCore.QSize(16777215, 20))
        self.label_8.setObjectName("label_8")
        self.gridLayout.addWidget(self.label_8, 0, 0, 1, 1)
        self.outputPath = QtWidgets.QLineEdit(WiperMaskGenerator)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.outputPath.sizePolicy().hasHeightForWidth())
        self.outputPath.setSizePolicy(sizePolicy)
        self.outputPath.setObjectName("outputPath")
        self.gridLayout.addWidget(self.outputPath, 4, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.line_3 = QtWidgets.QFrame(WiperMaskGenerator)
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.verticalLayout.addWidget(self.line_3)
        self.wiperConfigurationGroupBox_02 = QtWidgets.QScrollArea(WiperMaskGenerator)
        self.wiperConfigurationGroupBox_02.setMinimumSize(QtCore.QSize(0, 150))
        self.wiperConfigurationGroupBox_02.setMaximumSize(QtCore.QSize(16777215, 270))
        self.wiperConfigurationGroupBox_02.setWidgetResizable(True)
        self.wiperConfigurationGroupBox_02.setObjectName("wiperConfigurationGroupBox_02")
        self.widgetScroll = QtWidgets.QWidget()
        self.widgetScroll.setGeometry(QtCore.QRect(0, 0, 600, 234))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widgetScroll.sizePolicy().hasHeightForWidth())
        self.widgetScroll.setSizePolicy(sizePolicy)
        self.widgetScroll.setMinimumSize(QtCore.QSize(0, 0))
        self.widgetScroll.setObjectName("widgetScroll")
        self.formLayout = QtWidgets.QFormLayout(self.widgetScroll)
        self.formLayout.setObjectName("formLayout")
        self.wiperConfigurationGroupBox = QtWidgets.QGroupBox(self.widgetScroll)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.wiperConfigurationGroupBox.sizePolicy().hasHeightForWidth())
        self.wiperConfigurationGroupBox.setSizePolicy(sizePolicy)
        self.wiperConfigurationGroupBox.setMinimumSize(QtCore.QSize(0, 100))
        self.wiperConfigurationGroupBox.setObjectName("wiperConfigurationGroupBox")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.SpanningRole, self.wiperConfigurationGroupBox)
        self.wiperConfigurationGroupBox_02.setWidget(self.widgetScroll)
        self.verticalLayout.addWidget(self.wiperConfigurationGroupBox_02)
        self.bakeTexture = QtWidgets.QPushButton(WiperMaskGenerator)
        self.bakeTexture.setMinimumSize(QtCore.QSize(0, 40))
        self.bakeTexture.setObjectName("bakeTexture")
        self.verticalLayout.addWidget(self.bakeTexture)
        self.horizontalLayout.addLayout(self.verticalLayout)

        self.retranslateUi(WiperMaskGenerator)
        QtCore.QMetaObject.connectSlotsByName(WiperMaskGenerator)

    def retranslateUi(self, WiperMaskGenerator):
        WiperMaskGenerator.setWindowTitle(QtWidgets.QApplication.translate("WiperMaskGenerator", "Wiper Mask Generator", None, -1))
        self.groupBox.setTitle(QtWidgets.QApplication.translate("WiperMaskGenerator", "MANDATORY", None, -1))
        self.label_6.setText(QtWidgets.QApplication.translate("WiperMaskGenerator", "Create 2 point helper, parent them to the WiperMesh and position them on the exterior point of the wipe mesh\n"
"It is up to you to define the area impacted by the cleaner part of the wiper \n"
"", None, -1))
        self.label_10.setText(QtWidgets.QApplication.translate("WiperMaskGenerator", "Ouput Path", None, -1))
        self.filePathButton.setText(QtWidgets.QApplication.translate("WiperMaskGenerator", "File", None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate("WiperMaskGenerator", "Final Animation Frame", None, -1))
        self.label_9.setText(QtWidgets.QApplication.translate("WiperMaskGenerator", "Middle Animation Frame", None, -1))
        self.label_11.setText(QtWidgets.QApplication.translate("WiperMaskGenerator", "Windshield Node", None, -1))
        self.label_8.setText(QtWidgets.QApplication.translate("WiperMaskGenerator", "Initial Animation Frame", None, -1))
        self.wiperConfigurationGroupBox.setTitle(QtWidgets.QApplication.translate("WiperMaskGenerator", "Wipers Configuration", None, -1))
        self.bakeTexture.setText(QtWidgets.QApplication.translate("WiperMaskGenerator", "BakeTexture", None, -1))

