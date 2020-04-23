# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\KittyHawk\ASSETS\KittyHawk_Data\Tools\3DSMAX\FlightSimPackage\src\scripts\MultiExporter\resources\mainwindow.ui'
#
# Created: Wed Apr 22 18:03:13 2020
#      by: pyside2-uic  running on PySide2 5.6.0a1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_MultiExporter(object):
    def setupUi(self, MultiExporter):
        MultiExporter.setObjectName("MultiExporter")
        MultiExporter.resize(614, 450)
        MultiExporter.setMinimumSize(QtCore.QSize(614, 450))
        self.horizontalLayout = QtWidgets.QHBoxLayout(MultiExporter)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.scrollArea = QtWidgets.QScrollArea(MultiExporter)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 594, 430))
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
        self.btnOpenExportFolder = QtWidgets.QPushButton(self.groupBox)
        self.btnOpenExportFolder.setMinimumSize(QtCore.QSize(150, 30))
        self.btnOpenExportFolder.setObjectName("btnOpenExportFolder")
        self.horizontalLayout_2.addWidget(self.btnOpenExportFolder)
        self.verticalLayout_5.addLayout(self.horizontalLayout_2)
        self.verticalLayout.addWidget(self.groupBox)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setContentsMargins(5, 0, 5, -1)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.cbVisibleOnly = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.cbVisibleOnly.setObjectName("cbVisibleOnly")
        self.horizontalLayout_3.addWidget(self.cbVisibleOnly)
        self.cbIncludeLods = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.cbIncludeLods.setChecked(False)
        self.cbIncludeLods.setObjectName("cbIncludeLods")
        self.horizontalLayout_3.addWidget(self.cbIncludeLods)
        self.cbExportableOnly = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.cbExportableOnly.setChecked(True)
        self.cbExportableOnly.setObjectName("cbExportableOnly")
        self.horizontalLayout_3.addWidget(self.cbExportableOnly)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.btnRefresh = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.btnRefresh.setMaximumSize(QtCore.QSize(50, 23))
        self.btnRefresh.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.btnRefresh.setAutoDefault(False)
        self.btnRefresh.setDefault(False)
        self.btnRefresh.setFlat(False)
        self.btnRefresh.setObjectName("btnRefresh")
        self.horizontalLayout_3.addWidget(self.btnRefresh)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.tabWidget = QtWidgets.QTabWidget(self.scrollAreaWidgetContents)
        self.tabWidget.setEnabled(True)
        self.tabWidget.setDocumentMode(False)
        self.tabWidget.setTabsClosable(False)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.tab)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.toLayerList = QtWidgets.QTreeWidget(self.tab)
        self.toLayerList.setTabKeyNavigation(False)
        self.toLayerList.setAlternatingRowColors(True)
        self.toLayerList.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.toLayerList.setObjectName("toLayerList")
        self.toLayerList.headerItem().setText(0, "         Layers")
        self.toLayerList.header().setDefaultSectionSize(40)
        self.verticalLayout_2.addWidget(self.toLayerList)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.tab_2)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.toExportList = QtWidgets.QTreeWidget(self.tab_2)
        self.toExportList.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.toExportList.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.toExportList.setAlternatingRowColors(True)
        self.toExportList.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.toExportList.setIndentation(10)
        self.toExportList.setColumnCount(4)
        self.toExportList.setProperty("topLevelItemCount", 0)
        self.toExportList.setObjectName("toExportList")
        self.toExportList.header().setDefaultSectionSize(50)
        self.verticalLayout_3.addWidget(self.toExportList)
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.tab_3)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
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
        self.line_2 = QtWidgets.QFrame(self.tab_3)
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.horizontalLayout_6.addWidget(self.line_2)
        self.btnSetLODValues = QtWidgets.QPushButton(self.tab_3)
        self.btnSetLODValues.setObjectName("btnSetLODValues")
        self.horizontalLayout_6.addWidget(self.btnSetLODValues)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem3)
        self.btnConformLayers = QtWidgets.QPushButton(self.tab_3)
        self.btnConformLayers.setObjectName("btnConformLayers")
        self.horizontalLayout_6.addWidget(self.btnConformLayers)
        self.verticalLayout_4.addLayout(self.horizontalLayout_6)
        self.tabWidget.addTab(self.tab_3, "")
        self.verticalLayout.addWidget(self.tabWidget)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setContentsMargins(5, 0, 5, -1)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.btnGenerateXML = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.btnGenerateXML.setMinimumSize(QtCore.QSize(120, 30))
        self.btnGenerateXML.setObjectName("btnGenerateXML")
        self.horizontalLayout_4.addWidget(self.btnGenerateXML)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem4)
        self.btnExportTicked = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.btnExportTicked.setMinimumSize(QtCore.QSize(120, 30))
        self.btnExportTicked.setObjectName("btnExportTicked")
        self.horizontalLayout_4.addWidget(self.btnExportTicked)
        self.btnExportSelected = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.btnExportSelected.setMinimumSize(QtCore.QSize(120, 30))
        self.btnExportSelected.setObjectName("btnExportSelected")
        self.horizontalLayout_4.addWidget(self.btnExportSelected)
        self.btnExportAll = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.btnExportAll.setMinimumSize(QtCore.QSize(120, 30))
        self.btnExportAll.setObjectName("btnExportAll")
        self.horizontalLayout_4.addWidget(self.btnExportAll)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setContentsMargins(5, -1, 5, -1)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label_4 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_7.addWidget(self.label_4)
        self.progressBar = QtWidgets.QProgressBar(self.scrollAreaWidgetContents)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.horizontalLayout_7.addWidget(self.progressBar)
        self.verticalLayout.addLayout(self.horizontalLayout_7)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.horizontalLayout.addWidget(self.scrollArea)

        self.retranslateUi(MultiExporter)
        self.tabWidget.setCurrentIndex(2)
        self.flattenComboBox.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MultiExporter)

    def retranslateUi(self, MultiExporter):
        MultiExporter.setWindowTitle(QtWidgets.QApplication.translate("MultiExporter", "Multi Exporter", None, -1))
        self.groupBox.setTitle(QtWidgets.QApplication.translate("MultiExporter", "Add/Remove Export Path to Scene Explorer/ Viewport Selection", None, -1))
        self.btnAddExport.setText(QtWidgets.QApplication.translate("MultiExporter", "Add/Edit Export Path", None, -1))
        self.btnRemoveExport.setText(QtWidgets.QApplication.translate("MultiExporter", "Remove Export Path", None, -1))
        self.btnOpenExportFolder.setText(QtWidgets.QApplication.translate("MultiExporter", "Open Export Folder", None, -1))
        self.cbVisibleOnly.setText(QtWidgets.QApplication.translate("MultiExporter", "Only Visible", None, -1))
        self.cbIncludeLods.setText(QtWidgets.QApplication.translate("MultiExporter", "Only LODs", None, -1))
        self.cbExportableOnly.setText(QtWidgets.QApplication.translate("MultiExporter", "Only Exportable", None, -1))
        self.btnRefresh.setText(QtWidgets.QApplication.translate("MultiExporter", "Refresh", None, -1))
        self.btnRefresh.setShortcut(QtWidgets.QApplication.translate("MultiExporter", "R", None, -1))
        self.toLayerList.headerItem().setText(1, QtWidgets.QApplication.translate("MultiExporter", "LOD Value", None, -1))
        self.toLayerList.headerItem().setText(2, QtWidgets.QApplication.translate("MultiExporter", "Flatten", None, -1))
        self.toLayerList.headerItem().setText(3, QtWidgets.QApplication.translate("MultiExporter", "Path", None, -1))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QtWidgets.QApplication.translate("MultiExporter", "Layer View", None, -1))
        self.toExportList.setSortingEnabled(False)
        self.toExportList.headerItem().setText(0, QtWidgets.QApplication.translate("MultiExporter", "         Object", None, -1))
        self.toExportList.headerItem().setText(1, QtWidgets.QApplication.translate("MultiExporter", "LOD value", None, -1))
        self.toExportList.headerItem().setText(2, QtWidgets.QApplication.translate("MultiExporter", "Flatten", None, -1))
        self.toExportList.headerItem().setText(3, QtWidgets.QApplication.translate("MultiExporter", "Path", None, -1))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QtWidgets.QApplication.translate("MultiExporter", "Object View", None, -1))
        self.treeLODs.headerItem().setText(0, QtWidgets.QApplication.translate("MultiExporter", "         Hierarchy", None, -1))
        self.treeLODs.headerItem().setText(1, QtWidgets.QApplication.translate("MultiExporter", "LOD value", None, -1))
        self.treeLODs.headerItem().setText(2, QtWidgets.QApplication.translate("MultiExporter", "Flatten", None, -1))
        self.treeLODs.headerItem().setText(3, QtWidgets.QApplication.translate("MultiExporter", "Path", None, -1))
        __sortingEnabled = self.treeLODs.isSortingEnabled()
        self.treeLODs.setSortingEnabled(False)
        self.treeLODs.topLevelItem(0).setText(0, QtWidgets.QApplication.translate("MultiExporter", "Nouvel élément", None, -1))
        self.treeLODs.topLevelItem(0).child(0).setText(0, QtWidgets.QApplication.translate("MultiExporter", "Nouveau sous-élément", None, -1))
        self.treeLODs.topLevelItem(0).child(1).setText(0, QtWidgets.QApplication.translate("MultiExporter", "Nouvel élément", None, -1))
        self.treeLODs.topLevelItem(0).child(2).setText(0, QtWidgets.QApplication.translate("MultiExporter", "Nouvel élément", None, -1))
        self.treeLODs.setSortingEnabled(__sortingEnabled)
        self.label_2.setText(QtWidgets.QApplication.translate("MultiExporter", "Flatten On Export", None, -1))
        self.flattenComboBox.setCurrentText(QtWidgets.QApplication.translate("MultiExporter", "True", None, -1))
        self.flattenComboBox.setItemText(0, QtWidgets.QApplication.translate("MultiExporter", "True", None, -1))
        self.flattenComboBox.setItemText(1, QtWidgets.QApplication.translate("MultiExporter", "False", None, -1))
        self.flattenComboBox.setItemText(2, QtWidgets.QApplication.translate("MultiExporter", "-", None, -1))
        self.label_3.setText(QtWidgets.QApplication.translate("MultiExporter", "LOD Value", None, -1))
        self.lodValue.setPlaceholderText(QtWidgets.QApplication.translate("MultiExporter", "70.0000", None, -1))
        self.btnSetLODValues.setText(QtWidgets.QApplication.translate("MultiExporter", "Set Values", None, -1))
        self.btnConformLayers.setText(QtWidgets.QApplication.translate("MultiExporter", "Conform Layers", None, -1))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QtWidgets.QApplication.translate("MultiExporter", "LOD View", None, -1))
        self.btnGenerateXML.setText(QtWidgets.QApplication.translate("MultiExporter", "Generate XML", None, -1))
        self.btnExportTicked.setText(QtWidgets.QApplication.translate("MultiExporter", "Export Ticked", None, -1))
        self.btnExportSelected.setText(QtWidgets.QApplication.translate("MultiExporter", "Export Selected", None, -1))
        self.btnExportAll.setText(QtWidgets.QApplication.translate("MultiExporter", "Export All", None, -1))
        self.label_4.setText(QtWidgets.QApplication.translate("MultiExporter", "Export Progress :", None, -1))

