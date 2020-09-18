"""This module handles the option panel of the multi exporter.

It is connected to the BabylonPYMXS and babylon exporter as it is getting default values for the fields from it. It is possible to run this option menu outside the context of the mutli exporter
"""
import os
import sys

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

import uuid
import BabylonPYMXS
import MultiExporter.constants as const
from MultiExporter import exporter, presetUtils,treeView
import MultiExporter.ui.settingsWindow_ui as settingsWindowUI
from maxsdk import perforce as sdkperforce
from maxsdk import qtUtils, sceneUtils, userprop, utility
from pymxs import runtime as rt

APPLY_UPTODATE = "Save"
APPLY_OUTDATED = "Save*"

# Add parameters at the end of the list if needed
# It will break existing asset if you don't


class ComboBoxOptionPreset(QComboBox):
    """
    QComboBox to handle OptionPreset. 

    \nComboBoxOptionPreset will read, create and store the OptionPreset in the root node of the scene.
    \nIf no option preset are already stored in the scene then intanciating a ComboBoxOptionPreset will set it up.
    """    
    onModifiedData = Signal()

    def __init__(self, menu, parent):
        """
        \nin:
        menu=OptionsMenu
        parent=QWidget
        """
        QComboBox.__init__(self, parent)
        self.menu = menu
        self.presetObjectList = []
        self._intializeContent()
        self.currentIndexChanged.connect(lambda i: self._changedIndex(i))
        self.setEditable(True)
        self.liEd = self.lineEdit()
        self.liEd.editingFinished.connect(self._renamedCurrent)
        self.setInsertPolicy(self.NoInsert)
        self.oldIndex = 0

    def _getInfoByIdentifier(self, identifier):
        for i,presetObj in enumerate(self.presetObjectList):
            if presetObj.identifier == identifier:
                return (i,presetObj)
        return None
    def getOptionPresetByIdentifier(self, identifier):
        try:
            return self._getInfoByIdentifier(identifier)[1]
        except TypeError:
            return None

    def getOptionPresetIndexByIdentifier(self, identifier):
        try:
            return self._getInfoByIdentifier(identifier)[0]
        except TypeError:
            return None            

    def focusOutEvent(self, focusEvent):
        if self.menu is not None:
            if self.menu.madeChanges == True:
                self.hidePopup()               
            else:
                focusEvent.accept()
            return
        else:
            QComboBox.focusOutEvent(self,focusEvent)


    def wheelEvent(self, wheelEvent):
        if self.menu is not None:
            if self.menu.madeChanges == True:
                wheelEvent.ignore()
                return                

        QComboBox.wheelEvent(self,wheelEvent)

    def updatePreset(self,index,newDict):
        self.presetObjectList[index].edit(dictionary=newDict)        

    def _intializeContent(self):
        self.clear()
        self.presetObjectList = []
        optionPresetList = userprop.getUserPropList(
            sceneUtils.getSceneRootNode(), const.PROP_OPTIONS_LIST)
        if optionPresetList is None:
            optionPresetList = list()
        if len(optionPresetList) > 0:
            defaultPresetId = optionPresetList[0]
        else:
            defaultPresetId = const.PROP_OPTIONS_ENTRY_PREFIX.format(uuid.uuid4())
        defaultPreset = presetUtils.OptionPresetObject(
            defaultPresetId, listStorage=const.PROP_OPTIONS_LIST)
        defaultPreset.create("default", getCurrentSettingsAsDict())
        self.presetObjectList.append(defaultPreset)           
        for i in range(1,len(optionPresetList)):
            option = optionPresetList[i]
            preset = presetUtils.OptionPresetObject(
                option, const.PROP_OPTIONS_LIST)
            self.presetObjectList.append(preset)            
        for item in self.presetObjectList:
            self.addItem(item.name, item)

    def refresh(self):
        self._intializeContent()

    def addPreset(self, name):
        presetId = const.PROP_OPTIONS_ENTRY_PREFIX.format(uuid.uuid4())
        preset = presetUtils.OptionPresetObject(presetId, listStorage=const.PROP_OPTIONS_LIST)        
        preset.create(name, getCurrentSettingsAsDict())
        self.presetObjectList.append(preset)
        self.addItem(preset.name, preset)
        self.setCurrentIndex(self.count() - 1)
        self.onModifiedData.emit()
    
    def _renamedCurrent(self):
        currentID = self.currentIndex()
        if(currentID != 0):
            newName = userprop.cleanupStringForPropListStorage(self.liEd.text())
            self.setItemText(currentID, newName)
            current = self.itemData(currentID)
            current.edit(name=newName)
            self.onModifiedData.emit()

    def _changedIndex(self, index):
        pass


class OptionsMenu(QWidget, settingsWindowUI.Ui_settingsWindow):
    """
    QWidget to handle Babylon parameters.
    This widget is an option menu window for the multi exporter, though it stands alone and can read and set babylon export settings.
    \nSignal :
    onClosed : emits when the window is closed
    onModifiedData : emits when the settings change or an option preset is created/renamed. 
    """
    onClosed = Signal()
    onModifiedData = Signal()

    def __init__(self):
        QWidget.__init__(self)
        self.setupUi(self)
        self.btnSave.pressed.connect(lambda: self.saveSettings())
        self.btnSave.setText(APPLY_UPTODATE)
        self.btnCancel.pressed.connect(lambda: self.close())
        self.madeChanges = False

        # PRESET BUTTONS
        self.btnAddOptionPreset.clicked.connect(self._clickedAddOptionPreset)

        self.lineTextureQuality.setValidator(QIntValidator())

        #Add parameters at the end of the list if needed
        
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
            self.lineTextureQuality: "babylonjs_txtCompression",
            self.cbWriteTextures: "babylonjs_writetextures",
            self.cbOverwriteTexture: "babylonjs_overwritetextures",
            self.cbMergeAO: "babylonjs_mergeAOwithMR",
            self.cbKeepInstances: "flightsim_keepInstances"
        }
        # in case there is different behaviours to have for a same QWidget put the second case in here and implement it further down :
        self.specialWidgetToProperty = {
            self.comboAnimationExport: "babylonjs_export_animations_type",
        }
        self.initializeWidgets()
        for widget in self.widgetToProperty.keys() + self.specialWidgetToProperty.keys():
            if(isinstance(widget, QCheckBox)):
                signal = widget.stateChanged
            elif (isinstance(widget, QGroupBox)):
                signal = widget.toggled
            elif (isinstance(widget, QComboBox)):
                signal = widget.activated
            elif (isinstance(widget, QLineEdit)):
                signal = widget.textEdited
            signal.connect(lambda: self.changedOption())

        # PRESET COMBO
        presetCombo = ComboBoxOptionPreset(self,self)
        presetCombo.setFixedSize(self.comboOptionPreset.size())
        presetCombo.setEditable(True)
        self.horizontalLayout_8.removeWidget(self.comboOptionPreset)
        self.comboOptionPreset.setHidden(True)
        self.comboOptionPreset = presetCombo
        self.comboOptionPreset.activated.connect(lambda i: self.changedActivePreset(i))
        self.comboOptionPreset.onModifiedData.connect(self.onModifiedData.emit)
        self.horizontalLayout_8.insertWidget(1, self.comboOptionPreset)

    def _clickedAddOptionPreset(self):
        self.comboOptionPreset.addPreset("NewPreset")

    def changedOption(self):
        self.madeChanges = True
        self.btnSave.setText(APPLY_OUTDATED)

    def appliedOption(self):
        self.madeChanges = False
        self.btnSave.setText(APPLY_UPTODATE)

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
        self.onModifiedData.emit()

        self.close()

    def closeEvent(self, event):
        if self.tryClosing():
            self.onClosed.emit()
            event.accept()
        else:
            event.ignore()
            
    def changedActivePreset(self, index):
        preset = self.comboOptionPreset.presetObjectList[index]
        self.initializeWidgets(preset.dictionary)
        self.onModifiedData.emit()


    def initializeWidgets(self, dictObj=None):
        """
        Initialize each widgets in the option menu by doing this:
        - Get corresponding UserProperty of a widget in the self.widgetToProperty dictionary
        - Using this userProperty get the value in the input dictObj.
        - if it isn't in the dictObj look in the root node
        - if it isn't stored in the root then get the default value from BabylonPYMXS
        - if it isn't in BabylonPYMXS default values use the type default (False, 0, 0.0, "")
        - finally set this value in the widget

        \nin:
        dictObj=dict[str] var
        """
        sceneRoot = sceneUtils.getSceneRootNode()
        for widget in self.widgetToProperty.keys():
            prop = self.widgetToProperty[widget]
            state = None
            if dictObj is not None:
                if dictObj.has_key(prop):
                    state = dictObj[prop]                   
            if state is None:
                state = userprop.getUserProp(sceneRoot, prop)
            #INITIALIZE
            if (state == None):
                state = BabylonPYMXS.getPropertyDefaultValue(prop)
            if(isinstance(widget, QCheckBox)):
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
            #INITIALIZE
            if dictObj is not None:
                if dictObj.has_key(prop):
                    state = dictObj[prop]    
            if (state is None):
                state = BabylonPYMXS.getPropertyDefaultValue(prop)
            if isinstance(special, QComboBox):
                if state is None:
                    state = special.itemText(0)
                special.setCurrentText(state)
        self.appliedOption()

    def saveSettings(self):
        sceneRoot = sceneUtils.getSceneRootNode()
        newSettings = dict()
        currentPresetIndex = self.comboOptionPreset.currentIndex()
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
            if currentPresetIndex == 0:
                userprop.setUserProp(sceneRoot, prop, str(state))
            newSettings[prop] = state
        for special in self.specialWidgetToProperty.keys():
            prop = self.specialWidgetToProperty[special]
            if (isinstance(special, QComboBox)):
                state = special.currentText()
            if currentPresetIndex == 0:
                userprop.setUserProp(sceneRoot, prop, state)
            newSettings[prop] = state
            

        self.comboOptionPreset.updatePreset(currentPresetIndex, newSettings)
        self.btnSave.setText(APPLY_UPTODATE)
        self.madeChanges = False
        self.onModifiedData.emit()

def getCurrentSettingsAsDict():
    """
    Returns the current babylon parameters saved in the root node as a dict

    \nout:
    dictionary  key: pymxs user property string 
                value: var
    """
    sceneRoot = sceneUtils.getSceneRootNode()
    newDict = dict()
    for val in BabylonPYMXS.babylonParameters:
        newDict[val] = userprop.getUserProp(sceneRoot, val)
    return newDict

def run():
    optionsMenu = OptionsMenu()
    utility.attachToMax(optionsMenu)
    optionsMenu.show()
    return optionsMenu
