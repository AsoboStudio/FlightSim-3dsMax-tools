# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'e:\KittyHawk_Staging_ccreutz\ASSETS\KittyHawk_Data\Tools\3DSMAX\FlightSimPackage\src\scripts\MultiExporter\resources\mainwindow.ui'
#
# Created: Wed Jul  1 15:01:15 2020
#      by: pyside2-uic  running on PySide2 5.6.0a1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_MultiExporter(object):
    def setupUi(self, MultiExporter):
        MultiExporter.setObjectName("MultiExporter")
        MultiExporter.resize(1621, 855)
        MultiExporter.setMinimumSize(QtCore.QSize(679, 450))
        self.horizontalLayout = QtWidgets.QHBoxLayout(MultiExporter)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.scrollArea = QtWidgets.QScrollArea(MultiExporter)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 1601, 835))
        self.scrollAreaWidgetContents.setMinimumSize(QtCore.QSize(300, 400))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox.setMinimumSize(QtCore.QSize(0, 0))
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_5.setContentsMargins(0, -1, 0, -1)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        spacerItem = QtWidgets.QSpacerItem(20, 5, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout_5.addItem(spacerItem)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(5, 0, 5, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.btnAddExport = QtWidgets.QPushButton(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnAddExport.sizePolicy().hasHeightForWidth())
        self.btnAddExport.setSizePolicy(sizePolicy)
        self.btnAddExport.setMinimumSize(QtCore.QSize(150, 30))
        self.btnAddExport.setObjectName("btnAddExport")
        self.horizontalLayout_2.addWidget(self.btnAddExport)
        self.btnRemoveExport = QtWidgets.QPushButton(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnRemoveExport.sizePolicy().hasHeightForWidth())
        self.btnRemoveExport.setSizePolicy(sizePolicy)
        self.btnRemoveExport.setMinimumSize(QtCore.QSize(150, 30))
        self.btnRemoveExport.setObjectName("btnRemoveExport")
        self.horizontalLayout_2.addWidget(self.btnRemoveExport)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.btnRefresh = QtWidgets.QPushButton(self.groupBox)
        self.btnRefresh.setMinimumSize(QtCore.QSize(30, 30))
        self.btnRefresh.setMaximumSize(QtCore.QSize(30, 30))
        font = QtGui.QFont()
        font.setPointSize(32)
        font.setWeight(75)
        font.setUnderline(False)
        font.setBold(True)
        self.btnRefresh.setFont(font)
        self.btnRefresh.setAutoDefault(False)
        self.btnRefresh.setDefault(False)
        self.btnRefresh.setFlat(False)
        self.btnRefresh.setObjectName("btnRefresh")
        self.horizontalLayout_2.addWidget(self.btnRefresh)
        self.btnOpenExportFolder = QtWidgets.QPushButton(self.groupBox)
        self.btnOpenExportFolder.setMinimumSize(QtCore.QSize(150, 30))
        self.btnOpenExportFolder.setObjectName("btnOpenExportFolder")
        self.horizontalLayout_2.addWidget(self.btnOpenExportFolder)
        self.verticalLayout_5.addLayout(self.horizontalLayout_2)
        self.verticalLayout.addWidget(self.groupBox)
        self.tabWidget = QtWidgets.QTabWidget(self.scrollAreaWidgetContents)
        self.tabWidget.setEnabled(True)
        self.tabWidget.setDocumentMode(False)
        self.tabWidget.setTabsClosable(False)
        self.tabWidget.setObjectName("tabWidget")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.tab_3)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setContentsMargins(5, 0, 5, -1)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.cbVisibleOnly = QtWidgets.QCheckBox(self.tab_3)
        self.cbVisibleOnly.setObjectName("cbVisibleOnly")
        self.horizontalLayout_3.addWidget(self.cbVisibleOnly)
        self.cbIncludeLods = QtWidgets.QCheckBox(self.tab_3)
        self.cbIncludeLods.setChecked(False)
        self.cbIncludeLods.setObjectName("cbIncludeLods")
        self.horizontalLayout_3.addWidget(self.cbIncludeLods)
        self.cbExportableOnly = QtWidgets.QCheckBox(self.tab_3)
        self.cbExportableOnly.setObjectName("cbExportableOnly")
        self.horizontalLayout_3.addWidget(self.cbExportableOnly)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.verticalLayout_4.addLayout(self.horizontalLayout_3)
        self.treeLODs = QtWidgets.QTreeWidget(self.tab_3)
        self.treeLODs.setAlternatingRowColors(True)
        self.treeLODs.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.treeLODs.setIndentation(20)
        self.treeLODs.setObjectName("treeLODs")
        item_0 = QtWidgets.QTreeWidgetItem(self.treeLODs)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        self.treeLODs.header().setDefaultSectionSize(80)
        self.verticalLayout_4.addWidget(self.treeLODs)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setContentsMargins(5, 0, 5, -1)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_2 = QtWidgets.QLabel(self.tab_3)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_6.addWidget(self.label_2)
        self.flattenComboBox = QtWidgets.QComboBox(self.tab_3)
        self.flattenComboBox.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.flattenComboBox.setObjectName("flattenComboBox")
        self.flattenComboBox.addItem("")
        self.flattenComboBox.addItem("")
        self.flattenComboBox.addItem("")
        self.horizontalLayout_6.addWidget(self.flattenComboBox)
        self.line = QtWidgets.QFrame(self.tab_3)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout_6.addWidget(self.line)
        self.label_3 = QtWidgets.QLabel(self.tab_3)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_6.addWidget(self.label_3)
        self.lodValue = QtWidgets.QLineEdit(self.tab_3)
        self.lodValue.setMaximumSize(QtCore.QSize(50, 16777215))
        self.lodValue.setObjectName("lodValue")
        self.horizontalLayout_6.addWidget(self.lodValue)
        self.line_6 = QtWidgets.QFrame(self.tab_3)
        self.line_6.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_6.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_6.setObjectName("line_6")
        self.horizontalLayout_6.addWidget(self.line_6)
        self.cbKeepInstances = QtWidgets.QCheckBox(self.tab_3)
        self.cbKeepInstances.setObjectName("cbKeepInstances")
        self.horizontalLayout_6.addWidget(self.cbKeepInstances)
        self.line_2 = QtWidgets.QFrame(self.tab_3)
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.horizontalLayout_6.addWidget(self.line_2)
        self.btnSetLODValues = QtWidgets.QPushButton(self.tab_3)
        self.btnSetLODValues.setObjectName("btnSetLODValues")
        self.horizontalLayout_6.addWidget(self.btnSetLODValues)
        self.line_7 = QtWidgets.QFrame(self.tab_3)
        self.line_7.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_7.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_7.setObjectName("line_7")
        self.horizontalLayout_6.addWidget(self.line_7)
        self.label_6 = QtWidgets.QLabel(self.tab_3)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_6.addWidget(self.label_6)
        self.cbObjectOptionPreset = QtWidgets.QComboBox(self.tab_3)
        self.cbObjectOptionPreset.setObjectName("cbObjectOptionPreset")
        self.cbObjectOptionPreset.addItem("")
        self.horizontalLayout_6.addWidget(self.cbObjectOptionPreset)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem3)
        self.btnConformLayers = QtWidgets.QPushButton(self.tab_3)
        self.btnConformLayers.setObjectName("btnConformLayers")
        self.horizontalLayout_6.addWidget(self.btnConformLayers)
        self.verticalLayout_4.addLayout(self.horizontalLayout_6)
        self.tabWidget.addTab(self.tab_3, "")
        self.tabPreset = QtWidgets.QWidget()
        self.tabPreset.setObjectName("tabPreset")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.tabPreset)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.splitter = QtWidgets.QSplitter(self.tabPreset)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.splitter)
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_3.setContentsMargins(-1, 0, 1, -1)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.treePresets = QtWidgets.QTreeWidget(self.verticalLayoutWidget)
        self.treePresets.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.treePresets.sizePolicy().hasHeightForWidth())
        self.treePresets.setSizePolicy(sizePolicy)
        self.treePresets.setDragEnabled(True)
        self.treePresets.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
        self.treePresets.setDefaultDropAction(QtCore.Qt.MoveAction)
        self.treePresets.setAlternatingRowColors(True)
        self.treePresets.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.treePresets.setObjectName("treePresets")
        item_0 = QtWidgets.QTreeWidgetItem(self.treePresets)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.NoBrush)
        item_0.setBackground(1, brush)
        self.treePresets.header().setDefaultSectionSize(40)
        self.verticalLayout_3.addWidget(self.treePresets)
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setContentsMargins(5, -1, 5, -1)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.btnAddPreset = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.btnAddPreset.setObjectName("btnAddPreset")
        self.horizontalLayout_9.addWidget(self.btnAddPreset)
        self.btnAddGroup = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.btnAddGroup.setObjectName("btnAddGroup")
        self.horizontalLayout_9.addWidget(self.btnAddGroup)
        self.line_3 = QtWidgets.QFrame(self.verticalLayoutWidget)
        self.line_3.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.horizontalLayout_9.addWidget(self.line_3)
        self.btnDuplicatePreset = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.btnDuplicatePreset.setObjectName("btnDuplicatePreset")
        self.horizontalLayout_9.addWidget(self.btnDuplicatePreset)
        self.btnRemovePreset = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.btnRemovePreset.setObjectName("btnRemovePreset")
        self.horizontalLayout_9.addWidget(self.btnRemovePreset)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_9.addItem(spacerItem4)
        self.btnEditPresetPath = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.btnEditPresetPath.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.btnEditPresetPath.setObjectName("btnEditPresetPath")
        self.horizontalLayout_9.addWidget(self.btnEditPresetPath)
        self.verticalLayout_3.addLayout(self.horizontalLayout_9)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setContentsMargins(5, 0, 5, -1)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label.setObjectName("label")
        self.horizontalLayout_8.addWidget(self.label)
        self.presetParamName = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.presetParamName.setMinimumSize(QtCore.QSize(100, 0))
        self.presetParamName.setMaximumSize(QtCore.QSize(130, 16777215))
        self.presetParamName.setObjectName("presetParamName")
        self.horizontalLayout_8.addWidget(self.presetParamName)
        self.line_4 = QtWidgets.QFrame(self.verticalLayoutWidget)
        self.line_4.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.horizontalLayout_8.addWidget(self.line_4)
        self.label_5 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_8.addWidget(self.label_5)
        self.cbOptionPreset = QtWidgets.QComboBox(self.verticalLayoutWidget)
        self.cbOptionPreset.setObjectName("cbOptionPreset")
        self.cbOptionPreset.addItem("")
        self.horizontalLayout_8.addWidget(self.cbOptionPreset)
        self.line_5 = QtWidgets.QFrame(self.verticalLayoutWidget)
        self.line_5.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_5.setObjectName("line_5")
        self.horizontalLayout_8.addWidget(self.line_5)
        self.btnApplyPresetEdit = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.btnApplyPresetEdit.setMaximumSize(QtCore.QSize(40, 16777215))
        self.btnApplyPresetEdit.setObjectName("btnApplyPresetEdit")
        self.horizontalLayout_8.addWidget(self.btnApplyPresetEdit)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem5)
        self.verticalLayout_3.addLayout(self.horizontalLayout_8)
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.splitter)
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.treeLayer = QtWidgets.QTreeWidget(self.verticalLayoutWidget_2)
        self.treeLayer.setAlternatingRowColors(True)
        self.treeLayer.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.treeLayer.setObjectName("treeLayer")
        self.verticalLayout_7.addWidget(self.treeLayer)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setContentsMargins(5, 0, 5, -1)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.btnApplyPresetLayer = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.btnApplyPresetLayer.setObjectName("btnApplyPresetLayer")
        self.horizontalLayout_5.addWidget(self.btnApplyPresetLayer)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem6)
        self.btnLayerExpandAll = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.btnLayerExpandAll.setObjectName("btnLayerExpandAll")
        self.horizontalLayout_5.addWidget(self.btnLayerExpandAll)
        self.btnLayerCollapseAll = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.btnLayerCollapseAll.setObjectName("btnLayerCollapseAll")
        self.horizontalLayout_5.addWidget(self.btnLayerCollapseAll)
        self.verticalLayout_7.addLayout(self.horizontalLayout_5)
        self.verticalLayout_2.addWidget(self.splitter)
        self.tabWidget.addTab(self.tabPreset, "")
        self.verticalLayout.addWidget(self.tabWidget)
        self.groupBox_2 = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_6.setContentsMargins(0, -1, 0, -1)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setContentsMargins(5, 0, 5, -1)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.btnGenerateXML = QtWidgets.QPushButton(self.groupBox_2)
        self.btnGenerateXML.setMinimumSize(QtCore.QSize(120, 30))
        self.btnGenerateXML.setObjectName("btnGenerateXML")
        self.horizontalLayout_4.addWidget(self.btnGenerateXML)
        self.btnOptions = QtWidgets.QPushButton(self.groupBox_2)
        self.btnOptions.setMinimumSize(QtCore.QSize(120, 30))
        self.btnOptions.setObjectName("btnOptions")
        self.horizontalLayout_4.addWidget(self.btnOptions)
        spacerItem7 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem7)
        self.btnExportTicked = QtWidgets.QPushButton(self.groupBox_2)
        self.btnExportTicked.setMinimumSize(QtCore.QSize(120, 30))
        self.btnExportTicked.setObjectName("btnExportTicked")
        self.horizontalLayout_4.addWidget(self.btnExportTicked)
        self.btnExportSelected = QtWidgets.QPushButton(self.groupBox_2)
        self.btnExportSelected.setMinimumSize(QtCore.QSize(120, 30))
        self.btnExportSelected.setObjectName("btnExportSelected")
        self.horizontalLayout_4.addWidget(self.btnExportSelected)
        self.btnExportAll = QtWidgets.QPushButton(self.groupBox_2)
        self.btnExportAll.setMinimumSize(QtCore.QSize(120, 30))
        self.btnExportAll.setObjectName("btnExportAll")
        self.horizontalLayout_4.addWidget(self.btnExportAll)
        self.verticalLayout_6.addLayout(self.horizontalLayout_4)
        spacerItem8 = QtWidgets.QSpacerItem(20, 5, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout_6.addItem(spacerItem8)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setContentsMargins(5, -1, 5, -1)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label_4 = QtWidgets.QLabel(self.groupBox_2)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_7.addWidget(self.label_4)
        self.progressBar = QtWidgets.QProgressBar(self.groupBox_2)
        self.progressBar.setMinimum(0)
        self.progressBar.setMaximum(1)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setTextVisible(True)
        self.progressBar.setTextDirection(QtWidgets.QProgressBar.TopToBottom)
        self.progressBar.setObjectName("progressBar")
        self.horizontalLayout_7.addWidget(self.progressBar)
        self.verticalLayout_6.addLayout(self.horizontalLayout_7)
        self.verticalLayout.addWidget(self.groupBox_2)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.horizontalLayout.addWidget(self.scrollArea)

        self.retranslateUi(MultiExporter)
        self.tabWidget.setCurrentIndex(0)
        self.flattenComboBox.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MultiExporter)

    def retranslateUi(self, MultiExporter):
        MultiExporter.setWindowTitle(QtWidgets.QApplication.translate("MultiExporter", "Multi Exporter", None, -1))
        self.groupBox.setTitle(QtWidgets.QApplication.translate("MultiExporter", "Add/Remove Export Path to Scene Explorer/ Viewport Selection", None, -1))
        self.btnAddExport.setText(QtWidgets.QApplication.translate("MultiExporter", "Add/Edit Export Path", None, -1))
        self.btnRemoveExport.setText(QtWidgets.QApplication.translate("MultiExporter", "Remove Export Path", None, -1))
        self.btnRefresh.setText(QtWidgets.QApplication.translate("MultiExporter", "R", None, -1))
        self.btnRefresh.setShortcut(QtWidgets.QApplication.translate("MultiExporter", "R", None, -1))
        self.btnOpenExportFolder.setText(QtWidgets.QApplication.translate("MultiExporter", "Open Export Folder", None, -1))
        self.cbVisibleOnly.setText(QtWidgets.QApplication.translate("MultiExporter", "Only Visible", None, -1))
        self.cbIncludeLods.setText(QtWidgets.QApplication.translate("MultiExporter", "Only LODs", None, -1))
        self.cbExportableOnly.setText(QtWidgets.QApplication.translate("MultiExporter", "Only Exportable", None, -1))
        self.treeLODs.headerItem().setText(0, QtWidgets.QApplication.translate("MultiExporter", "DONE", None, -1))
        self.treeLODs.headerItem().setText(1, QtWidgets.QApplication.translate("MultiExporter", "IN", None, -1))
        self.treeLODs.headerItem().setText(2, QtWidgets.QApplication.translate("MultiExporter", "CODE", None, -1))
        self.treeLODs.headerItem().setText(3, QtWidgets.QApplication.translate("MultiExporter", "DONE IN CODE DON\'T EDIT.", None, -1))
        __sortingEnabled = self.treeLODs.isSortingEnabled()
        self.treeLODs.setSortingEnabled(False)
        self.treeLODs.topLevelItem(0).setText(0, QtWidgets.QApplication.translate("MultiExporter", "DONE IN CODE DON\'T EDIT.", None, -1))
        self.treeLODs.topLevelItem(0).child(0).setText(0, QtWidgets.QApplication.translate("MultiExporter", "DONE IN CODE DON\'T EDIT.", None, -1))
        self.treeLODs.topLevelItem(0).child(1).setText(0, QtWidgets.QApplication.translate("MultiExporter", "DONE IN CODE DON\'T EDIT.", None, -1))
        self.treeLODs.topLevelItem(0).child(2).setText(0, QtWidgets.QApplication.translate("MultiExporter", "DONE IN CODE DON\'T EDIT.", None, -1))
        self.treeLODs.setSortingEnabled(__sortingEnabled)
        self.label_2.setText(QtWidgets.QApplication.translate("MultiExporter", "Flatten On Export", None, -1))
        self.flattenComboBox.setCurrentText(QtWidgets.QApplication.translate("MultiExporter", "True", None, -1))
        self.flattenComboBox.setItemText(0, QtWidgets.QApplication.translate("MultiExporter", "True", None, -1))
        self.flattenComboBox.setItemText(1, QtWidgets.QApplication.translate("MultiExporter", "False", None, -1))
        self.flattenComboBox.setItemText(2, QtWidgets.QApplication.translate("MultiExporter", "-", None, -1))
        self.label_3.setText(QtWidgets.QApplication.translate("MultiExporter", "LOD Value", None, -1))
        self.lodValue.setPlaceholderText(QtWidgets.QApplication.translate("MultiExporter", "70.0000", None, -1))
        self.cbKeepInstances.setText(QtWidgets.QApplication.translate("MultiExporter", "Keep Instances", None, -1))
        self.btnSetLODValues.setText(QtWidgets.QApplication.translate("MultiExporter", "Set Values", None, -1))
        self.label_6.setText(QtWidgets.QApplication.translate("MultiExporter", "Preset Options :", None, -1))
        self.cbObjectOptionPreset.setItemText(0, QtWidgets.QApplication.translate("MultiExporter", "DONE IN CODE DON\'T EDIT.", None, -1))
        self.btnConformLayers.setText(QtWidgets.QApplication.translate("MultiExporter", "Conform Layers", None, -1))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QtWidgets.QApplication.translate("MultiExporter", "Objects", None, -1))
        self.treePresets.headerItem().setText(0, QtWidgets.QApplication.translate("MultiExporter", "DONE", None, -1))
        self.treePresets.headerItem().setText(1, QtWidgets.QApplication.translate("MultiExporter", "IN CODE DON\'T EDIT", None, -1))
        __sortingEnabled = self.treePresets.isSortingEnabled()
        self.treePresets.setSortingEnabled(False)
        self.treePresets.topLevelItem(0).setText(0, QtWidgets.QApplication.translate("MultiExporter", "DONE IN", None, -1))
        self.treePresets.topLevelItem(0).setText(1, QtWidgets.QApplication.translate("MultiExporter", "DONE IN CODE DON\'T EDIT.DONE IN CODE DON\'T EDIT.DONE IN CODE DON\'T EDIT.DONE IN CODE DON\'T EDIT.DONE IN CODE DON\'T EDIT.DONE IN CODE DON\'T EDIT.DONE IN CODE DON\'T EDIT.DONE IN CODE DON\'T EDIT.DONE IN CODE DON\'T EDIT.DONE IN CODE DON\'T EDIT.DONE IN CODE DON\'T EDIT.", None, -1))
        self.treePresets.setSortingEnabled(__sortingEnabled)
        self.btnAddPreset.setText(QtWidgets.QApplication.translate("MultiExporter", "Add Preset", None, -1))
        self.btnAddGroup.setText(QtWidgets.QApplication.translate("MultiExporter", "Add Group", None, -1))
        self.btnDuplicatePreset.setText(QtWidgets.QApplication.translate("MultiExporter", "Duplicate", None, -1))
        self.btnRemovePreset.setText(QtWidgets.QApplication.translate("MultiExporter", "Remove", None, -1))
        self.btnEditPresetPath.setText(QtWidgets.QApplication.translate("MultiExporter", "Edit Path", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("MultiExporter", "Name :", None, -1))
        self.label_5.setText(QtWidgets.QApplication.translate("MultiExporter", "Option Preset :", None, -1))
        self.cbOptionPreset.setItemText(0, QtWidgets.QApplication.translate("MultiExporter", "DONE IN CODE DON\'T EDIT.", None, -1))
        self.btnApplyPresetEdit.setText(QtWidgets.QApplication.translate("MultiExporter", "OK", None, -1))
        self.treeLayer.headerItem().setText(0, QtWidgets.QApplication.translate("MultiExporter", "         Layers", None, -1))
        self.btnApplyPresetLayer.setText(QtWidgets.QApplication.translate("MultiExporter", "Apply", None, -1))
        self.btnLayerExpandAll.setText(QtWidgets.QApplication.translate("MultiExporter", "Expand All", None, -1))
        self.btnLayerCollapseAll.setText(QtWidgets.QApplication.translate("MultiExporter", "Collapse All", None, -1))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabPreset), QtWidgets.QApplication.translate("MultiExporter", "Presets", None, -1))
        self.groupBox_2.setTitle(QtWidgets.QApplication.translate("MultiExporter", "Export", None, -1))
        self.btnGenerateXML.setText(QtWidgets.QApplication.translate("MultiExporter", "Generate XML", None, -1))
        self.btnOptions.setText(QtWidgets.QApplication.translate("MultiExporter", "Options", None, -1))
        self.btnExportTicked.setText(QtWidgets.QApplication.translate("MultiExporter", "Export Ticked", None, -1))
        self.btnExportSelected.setText(QtWidgets.QApplication.translate("MultiExporter", "Export Selected", None, -1))
        self.btnExportAll.setText(QtWidgets.QApplication.translate("MultiExporter", "Export All", None, -1))
        self.label_4.setText(QtWidgets.QApplication.translate("MultiExporter", "Progress :", None, -1))
        self.progressBar.setFormat(QtWidgets.QApplication.translate("MultiExporter", "%v/%m", None, -1))

