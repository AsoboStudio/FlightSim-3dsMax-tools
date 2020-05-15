import os
import sys

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

import BabylonPYMXS
import exporter
import MaxPlus
import MultiExporter.ui.settingsWindow_ui as settingsWindowUI
import treeView
import constants as const
import presetUtils

from maxsdk import perforce as sdkperforce
from maxsdk import qtUtils, sceneUtils, userprop, utility
from pymxs import runtime as rt

reload(userprop)
reload(sceneUtils)
reload(sdkperforce)
reload(settingsWindowUI)
reload(qtUtils)
reload(exporter)
reload(treeView)
reload(const)
reload(presetUtils)
reload(BabylonPYMXS)

APPLY_UPTODATE = "Save"
APPLY_OUTDATED = "Save*"

class OptionsMenu(QWidget, settingsWindowUI.Ui_settingsWindow):
    onClosed = Signal()
    def __init__(self):
        QWidget.__init__(self)
        self.setupUi(self)
        self.btnSave.pressed.connect(lambda: self.saveSettings())
        self.btnSave.setText(APPLY_UPTODATE)
        self.btnCancel.pressed.connect(lambda: self.close())
        self.madeChanges = False
        self.widgetToProperty = {
            self.cbAutosave: "babylonjs_autosave",
            self.cbExportHidden: "babylonjs_exporthidden",
            self.cbRemoveLODPrefix: "flightsim_removelodprefix",          
            self.cbRemoveNamespace: "flightsim_removenamespaces",          
            self.cbFlattenHierarchies: "babylonjs_flattenScene",          
            self.cbExportMaterial: "babylonjs_export_materials",          
            self.comboNormalMap: "flightsim_tangent_space_convention",          
            self.cbDontOptimizeAnim: "babylonjs_donotoptimizeanimations",          
            self.cbExportNonAnimated: "babylonjs_animgroupexportnonanimated",          
            self.gbUsePreExport: "babylonjs_preproces",          
            self.cbMergeContainers: "babylonjs_mergecontainersandxref",          
            self.cbApplyPreprocessToScene: "babylonjs_applyPreprocess",          
            self.comboBakeAnimationOptions: "babylonjs_bakeAnimationsType",          
            self.cbAsoboAnimationRetargeting: "babylonjs_asb_animation_retargeting",
            self.lineTextureQuality:"babylonjs_txtCompression",          
            self.cbWriteTextures:"babylonjs_writetextures",          
            self.cbOverwriteTexture:"babylonjs_overwritetextures",          
            self.cbMergeAO: "babylonjs_mergeAOwithMR"           
        }
        # in case there is different behaviours to have for a same QWidget put the second case in here :
        self.specialWidgetToProperty = {
            self.comboAnimationExport: "babylonjs_export_animations_type",          
        }
            
        self.initializeWidgets()

        for widget in self.widgetToProperty.keys() + self.specialWidgetToProperty.keys():
            if(isinstance(widget,QCheckBox)):
                signal = widget.stateChanged
            elif (isinstance(widget, QGroupBox)):
                signal = widget.toggled
            elif (isinstance(widget, QComboBox)):
                signal = widget.activated
            elif (isinstance(widget, QLineEdit)):
                signal = widget.textEdited
            signal.connect(lambda: self.changedOption())   

    def changedOption(self):
        self.madeChanges = True
        self.btnSave.setText(APPLY_OUTDATED)

    def tryClosing(self):
        if(self.madeChanges):
            popup = qtUtils.popup_Yes_No(
                title="Are you sure ?",
                text="You have unapplied changes, do you really want to exit without saving them ?"
            )
            return popup
        else:
            return True

    def saveAndQuit(self):
        self.saveSettings()
        self.close()

    def closeEvent(self, event):
        if self.tryClosing():
            self.onClosed.emit()
            event.accept()
        else:
            event.ignore()

    def initializeWidgets(self):
        sceneRoot = sceneUtils.getSceneRootNode()
        for widget in self.widgetToProperty.keys():
            prop = self.widgetToProperty[widget]
            state = userprop.getUserProp(sceneRoot, prop)
            if (state == None):
                state = BabylonPYMXS.getPropertyDefaultValue(prop)
            if(isinstance(widget,QCheckBox)):
                widget.setCheckState(Qt.Checked if state else Qt.Unchecked)
            elif (isinstance(widget, QGroupBox)):
                if (state is None):
                    state = False
                widget.setChecked(state)
            elif (isinstance(widget, QComboBox)):
                if state is None:
                    state = 0
                widget.setCurrentIndex(state)
            elif (isinstance(widget, QLineEdit)):
                widget.setText(str(state))
        
        for special in self.specialWidgetToProperty.keys():
            prop = self.specialWidgetToProperty[special]
            state = userprop.getUserProp(sceneRoot, prop)
            if (state == None):
                state = BabylonPYMXS.getPropertyDefaultValue(prop)
            if isinstance(special, QComboBox):
                if state is None:
                    state = special.itemText(0)
                special.setCurrentText(state)

    def saveSettings(self):
        sceneRoot = sceneUtils.getSceneRootNode()
        for widget in self.widgetToProperty.keys():
            prop = self.widgetToProperty[widget]
            if (isinstance(widget, QCheckBox)):
                state = True if widget.checkState() == Qt.Checked else False
            elif (isinstance(widget, QGroupBox)):
                state = widget.isChecked()
            elif (isinstance(widget, QComboBox)):
                state = widget.currentIndex()
            elif (isinstance(widget, QLineEdit)):
                state = widget.text()
            userprop.setUserProp(sceneRoot,prop, str(state))
        for special in self.specialWidgetToProperty.keys():
            prop = self.specialWidgetToProperty[special]
            if (isinstance(special, QComboBox)):
                state = special.currentText()
            userprop.setUserProp(sceneRoot, prop, state)
        self.btnSave.setText(APPLY_UPTODATE)
        self.madeChanges = False

def run():
    optionsMenu = OptionsMenu()
    utility.attachToMax(optionsMenu)
    optionsMenu.show()
    return optionsMenu
