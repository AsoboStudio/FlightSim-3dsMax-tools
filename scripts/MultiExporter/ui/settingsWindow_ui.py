# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\KittyHawk\ASSETS\KittyHawk_Data\Tools\3DSMAX\FlightSimPackage\src\scripts\MultiExporter\resources\settingsWindow.ui'
#
# Created: Tue May 12 19:26:06 2020
#      by: pyside2-uic  running on PySide2 5.6.0a1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_settingsWindow(object):
    def setupUi(self, settingsWindow):
        settingsWindow.setObjectName("settingsWindow")
        settingsWindow.resize(569, 250)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(settingsWindow.sizePolicy().hasHeightForWidth())
        settingsWindow.setSizePolicy(sizePolicy)
        settingsWindow.setMinimumSize(QtCore.QSize(569, 250))
        settingsWindow.setMaximumSize(QtCore.QSize(639, 335))
        settingsWindow.setBaseSize(QtCore.QSize(569, 250))
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(settingsWindow)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.tabWidget = QtWidgets.QTabWidget(settingsWindow)
        self.tabWidget.setObjectName("tabWidget")
        self.tabSettings = QtWidgets.QWidget()
        self.tabSettings.setObjectName("tabSettings")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.tabSettings)
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.groupBox_5 = QtWidgets.QGroupBox(self.tabSettings)
        self.groupBox_5.setTitle("")
        self.groupBox_5.setObjectName("groupBox_5")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.groupBox_5)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.cbAutosave = QtWidgets.QCheckBox(self.groupBox_5)
        self.cbAutosave.setObjectName("cbAutosave")
        self.horizontalLayout.addWidget(self.cbAutosave)
        self.cbExportHidden = QtWidgets.QCheckBox(self.groupBox_5)
        self.cbExportHidden.setObjectName("cbExportHidden")
        self.horizontalLayout.addWidget(self.cbExportHidden)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout_7.addLayout(self.horizontalLayout)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.groupBox_2 = QtWidgets.QGroupBox(self.groupBox_5)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.cbRemoveLODPrefix = QtWidgets.QCheckBox(self.groupBox_2)
        self.cbRemoveLODPrefix.setObjectName("cbRemoveLODPrefix")
        self.verticalLayout_3.addWidget(self.cbRemoveLODPrefix)
        self.cbRemoveNamespace = QtWidgets.QCheckBox(self.groupBox_2)
        self.cbRemoveNamespace.setObjectName("cbRemoveNamespace")
        self.verticalLayout_3.addWidget(self.cbRemoveNamespace)
        self.cbFlattenHierarchies = QtWidgets.QCheckBox(self.groupBox_2)
        self.cbFlattenHierarchies.setObjectName("cbFlattenHierarchies")
        self.verticalLayout_3.addWidget(self.cbFlattenHierarchies)
        self.gridLayout.addWidget(self.groupBox_2, 0, 0, 1, 1)
        self.gbUsePreExport = QtWidgets.QGroupBox(self.groupBox_5)
        self.gbUsePreExport.setCheckable(True)
        self.gbUsePreExport.setChecked(False)
        self.gbUsePreExport.setObjectName("gbUsePreExport")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.gbUsePreExport)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.cbMergeContainers = QtWidgets.QCheckBox(self.gbUsePreExport)
        self.cbMergeContainers.setObjectName("cbMergeContainers")
        self.verticalLayout_4.addWidget(self.cbMergeContainers)
        self.cbApplyPreprocessToScene = QtWidgets.QCheckBox(self.gbUsePreExport)
        self.cbApplyPreprocessToScene.setObjectName("cbApplyPreprocessToScene")
        self.verticalLayout_4.addWidget(self.cbApplyPreprocessToScene)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label = QtWidgets.QLabel(self.gbUsePreExport)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName("label")
        self.horizontalLayout_3.addWidget(self.label)
        self.comboBakeAnimationOptions = QtWidgets.QComboBox(self.gbUsePreExport)
        self.comboBakeAnimationOptions.setMinimumSize(QtCore.QSize(140, 0))
        self.comboBakeAnimationOptions.setObjectName("comboBakeAnimationOptions")
        self.comboBakeAnimationOptions.addItem("")
        self.comboBakeAnimationOptions.addItem("")
        self.comboBakeAnimationOptions.addItem("")
        self.horizontalLayout_3.addWidget(self.comboBakeAnimationOptions)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.verticalLayout_4.addLayout(self.horizontalLayout_3)
        self.gridLayout.addWidget(self.gbUsePreExport, 1, 1, 1, 1)
        self.groupBox_4 = QtWidgets.QGroupBox(self.groupBox_5)
        self.groupBox_4.setObjectName("groupBox_4")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.groupBox_4)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.cbExportMaterial = QtWidgets.QCheckBox(self.groupBox_4)
        self.cbExportMaterial.setMinimumSize(QtCore.QSize(0, 20))
        self.cbExportMaterial.setObjectName("cbExportMaterial")
        self.verticalLayout_5.addWidget(self.cbExportMaterial)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_2 = QtWidgets.QLabel(self.groupBox_4)
        self.label_2.setMinimumSize(QtCore.QSize(0, 20))
        self.label_2.setMaximumSize(QtCore.QSize(16777215, 30))
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_4.addWidget(self.label_2)
        self.comboNormalMap = QtWidgets.QComboBox(self.groupBox_4)
        self.comboNormalMap.setObjectName("comboNormalMap")
        self.comboNormalMap.addItem("")
        self.comboNormalMap.addItem("")
        self.horizontalLayout_4.addWidget(self.comboNormalMap)
        spacerItem2 = QtWidgets.QSpacerItem(40, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem2)
        self.verticalLayout_5.addLayout(self.horizontalLayout_4)
        spacerItem3 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        self.verticalLayout_5.addItem(spacerItem3)
        self.gridLayout.addWidget(self.groupBox_4, 0, 1, 1, 1)
        self.groupBox = QtWidgets.QGroupBox(self.groupBox_5)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.comboAnimationExport = QtWidgets.QComboBox(self.groupBox)
        self.comboAnimationExport.setMaximumSize(QtCore.QSize(80, 16777215))
        self.comboAnimationExport.setObjectName("comboAnimationExport")
        self.comboAnimationExport.addItem("")
        self.comboAnimationExport.addItem("")
        self.comboAnimationExport.addItem("")
        self.verticalLayout.addWidget(self.comboAnimationExport)
        self.cbDontOptimizeAnim = QtWidgets.QCheckBox(self.groupBox)
        self.cbDontOptimizeAnim.setObjectName("cbDontOptimizeAnim")
        self.verticalLayout.addWidget(self.cbDontOptimizeAnim)
        self.cbExportNonAnimated = QtWidgets.QCheckBox(self.groupBox)
        self.cbExportNonAnimated.setAutoExclusive(False)
        self.cbExportNonAnimated.setObjectName("cbExportNonAnimated")
        self.verticalLayout.addWidget(self.cbExportNonAnimated)
        self.gridLayout.addWidget(self.groupBox, 1, 0, 1, 1)
        self.verticalLayout_7.addLayout(self.gridLayout)
        self.horizontalLayout_6.addWidget(self.groupBox_5)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem4)
        self.tabWidget.addTab(self.tabSettings, "")
        self.tabAdvanced = QtWidgets.QWidget()
        self.tabAdvanced.setObjectName("tabAdvanced")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.tabAdvanced)
        self.verticalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.groupBox_6 = QtWidgets.QGroupBox(self.tabAdvanced)
        self.groupBox_6.setTitle("")
        self.groupBox_6.setObjectName("groupBox_6")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.groupBox_6)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.groupBox_8 = QtWidgets.QGroupBox(self.groupBox_6)
        self.groupBox_8.setObjectName("groupBox_8")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout(self.groupBox_8)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.cbAsoboAnimationRetargeting = QtWidgets.QCheckBox(self.groupBox_8)
        self.cbAsoboAnimationRetargeting.setObjectName("cbAsoboAnimationRetargeting")
        self.verticalLayout_10.addWidget(self.cbAsoboAnimationRetargeting)
        self.verticalLayout_6.addWidget(self.groupBox_8)
        self.groupBox_7 = QtWidgets.QGroupBox(self.groupBox_6)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_7.sizePolicy().hasHeightForWidth())
        self.groupBox_7.setSizePolicy(sizePolicy)
        self.groupBox_7.setObjectName("groupBox_7")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.groupBox_7)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_5 = QtWidgets.QLabel(self.groupBox_7)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_2.addWidget(self.label_5)
        self.lineTextureQuality = QtWidgets.QLineEdit(self.groupBox_7)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineTextureQuality.sizePolicy().hasHeightForWidth())
        self.lineTextureQuality.setSizePolicy(sizePolicy)
        self.lineTextureQuality.setMaximumSize(QtCore.QSize(50, 50))
        self.lineTextureQuality.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lineTextureQuality.setObjectName("lineTextureQuality")
        self.horizontalLayout_2.addWidget(self.lineTextureQuality)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem5)
        self.verticalLayout_8.addLayout(self.horizontalLayout_2)
        self.cbWriteTextures = QtWidgets.QCheckBox(self.groupBox_7)
        self.cbWriteTextures.setObjectName("cbWriteTextures")
        self.verticalLayout_8.addWidget(self.cbWriteTextures)
        self.cbOverwriteTexture = QtWidgets.QCheckBox(self.groupBox_7)
        self.cbOverwriteTexture.setObjectName("cbOverwriteTexture")
        self.verticalLayout_8.addWidget(self.cbOverwriteTexture)
        self.cbMergeAO = QtWidgets.QCheckBox(self.groupBox_7)
        self.cbMergeAO.setObjectName("cbMergeAO")
        self.verticalLayout_8.addWidget(self.cbMergeAO)
        self.verticalLayout_6.addWidget(self.groupBox_7)
        self.verticalLayout_9.addWidget(self.groupBox_6)
        spacerItem6 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_9.addItem(spacerItem6)
        self.tabWidget.addTab(self.tabAdvanced, "")
        self.verticalLayout_2.addWidget(self.tabWidget)
        spacerItem7 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem7)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        spacerItem8 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem8)
        self.btnSave = QtWidgets.QPushButton(settingsWindow)
        self.btnSave.setObjectName("btnSave")
        self.horizontalLayout_7.addWidget(self.btnSave)
        self.btnCancel = QtWidgets.QPushButton(settingsWindow)
        self.btnCancel.setObjectName("btnCancel")
        self.horizontalLayout_7.addWidget(self.btnCancel)
        self.verticalLayout_2.addLayout(self.horizontalLayout_7)

        self.retranslateUi(settingsWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(settingsWindow)

    def retranslateUi(self, settingsWindow):
        settingsWindow.setWindowTitle(QtWidgets.QApplication.translate("settingsWindow", "Export Options", None, -1))
        self.cbAutosave.setText(QtWidgets.QApplication.translate("settingsWindow", "Autosave 3ds Max File", None, -1))
        self.cbExportHidden.setText(QtWidgets.QApplication.translate("settingsWindow", "Export Hidden Objects", None, -1))
        self.groupBox_2.setTitle(QtWidgets.QApplication.translate("settingsWindow", "Objects", None, -1))
        self.cbRemoveLODPrefix.setText(QtWidgets.QApplication.translate("settingsWindow", "Remove LOD Prefix", None, -1))
        self.cbRemoveNamespace.setText(QtWidgets.QApplication.translate("settingsWindow", "Remove Namespace", None, -1))
        self.cbFlattenHierarchies.setText(QtWidgets.QApplication.translate("settingsWindow", "Flatten Hierarchies", None, -1))
        self.gbUsePreExport.setTitle(QtWidgets.QApplication.translate("settingsWindow", "Use Pre-export Process", None, -1))
        self.cbMergeContainers.setText(QtWidgets.QApplication.translate("settingsWindow", "Merge Containers and XRef", None, -1))
        self.cbApplyPreprocessToScene.setText(QtWidgets.QApplication.translate("settingsWindow", "Apply Preprocess To Scene", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("settingsWindow", "Bake Animation Options", None, -1))
        self.comboBakeAnimationOptions.setItemText(0, QtWidgets.QApplication.translate("settingsWindow", "Do Not Bake Animations", None, -1))
        self.comboBakeAnimationOptions.setItemText(1, QtWidgets.QApplication.translate("settingsWindow", "Bake All Animations", None, -1))
        self.comboBakeAnimationOptions.setItemText(2, QtWidgets.QApplication.translate("settingsWindow", "Selective Bake", None, -1))
        self.groupBox_4.setTitle(QtWidgets.QApplication.translate("settingsWindow", "Material", None, -1))
        self.cbExportMaterial.setText(QtWidgets.QApplication.translate("settingsWindow", "Export Material", None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate("settingsWindow", "Normal Map Convention", None, -1))
        self.comboNormalMap.setItemText(0, QtWidgets.QApplication.translate("settingsWindow", "DirectX", None, -1))
        self.comboNormalMap.setItemText(1, QtWidgets.QApplication.translate("settingsWindow", "OpenGL", None, -1))
        self.groupBox.setTitle(QtWidgets.QApplication.translate("settingsWindow", "Animation", None, -1))
        self.comboAnimationExport.setItemText(0, QtWidgets.QApplication.translate("settingsWindow", "Export", None, -1))
        self.comboAnimationExport.setItemText(1, QtWidgets.QApplication.translate("settingsWindow", "Not Export", None, -1))
        self.comboAnimationExport.setItemText(2, QtWidgets.QApplication.translate("settingsWindow", "Export ONLY", None, -1))
        self.cbDontOptimizeAnim.setText(QtWidgets.QApplication.translate("settingsWindow", "Do not optimize animations", None, -1))
        self.cbExportNonAnimated.setText(QtWidgets.QApplication.translate("settingsWindow", "(Animation Group) Export Non-Animated Objects", None, -1))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabSettings), QtWidgets.QApplication.translate("settingsWindow", "Settings", None, -1))
        self.groupBox_8.setTitle(QtWidgets.QApplication.translate("settingsWindow", "GLTF", None, -1))
        self.cbAsoboAnimationRetargeting.setText(QtWidgets.QApplication.translate("settingsWindow", "ASOBO_animation_retargeting", None, -1))
        self.groupBox_7.setTitle(QtWidgets.QApplication.translate("settingsWindow", "Textures", None, -1))
        self.label_5.setText(QtWidgets.QApplication.translate("settingsWindow", "Texture Quality", None, -1))
        self.lineTextureQuality.setText(QtWidgets.QApplication.translate("settingsWindow", "100", None, -1))
        self.lineTextureQuality.setPlaceholderText(QtWidgets.QApplication.translate("settingsWindow", "100", None, -1))
        self.cbWriteTextures.setText(QtWidgets.QApplication.translate("settingsWindow", "Write Textures", None, -1))
        self.cbOverwriteTexture.setText(QtWidgets.QApplication.translate("settingsWindow", "Overwrite Texture", None, -1))
        self.cbMergeAO.setText(QtWidgets.QApplication.translate("settingsWindow", "Merge AO Map", None, -1))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabAdvanced), QtWidgets.QApplication.translate("settingsWindow", "Advanced", None, -1))
        self.btnSave.setText(QtWidgets.QApplication.translate("settingsWindow", "Save", None, -1))
        self.btnCancel.setText(QtWidgets.QApplication.translate("settingsWindow", "Exit", None, -1))

