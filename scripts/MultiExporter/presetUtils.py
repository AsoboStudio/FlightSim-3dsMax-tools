"""
This module contains classes and function to handle preset in the multi exporter.

The presets are stored in the root node of the max scene.
"""

import os
import sys
import uuid
import MultiExporter.constants as const
from maxsdk import qtUtils, sceneUtils, userprop, utility
from pymxs import runtime as rt

class SerializableObject():
    """Stores a string "name" in the root node
    """
    def __init__(self, identifier, listStorage = None):
        self.identifier = identifier
        self.defaultName = "New"
        self.listStorage = "defaultSerializableObjectPool" if listStorage is None else listStorage # const.PROP_PRESET_GROUP_LIST
        self.name = None
        self._load()

    def get(self):
        self._load()
        return self.name

    def __hash__(self):
        return self.identifier.__hash__()  # hash(self.identifier)

    def __eq__(self, a):
        if isinstance(a, unicode) or isinstance(a, str):
            return self.identifier == a
        if(isinstance(a, PresetObject)):
            return self.identifier == a.identifier
        return False

    def edit(self, name):
        self._load()
        self.name = self.name if name is None else name
        self._write()

    def create(self, name):
        self.name = name
        self._write()

    def delete(self):
        self._load()
        sceneRoot = sceneUtils.getSceneRootNode()
        propList = userprop.getUserPropList(sceneRoot, self.listStorage)
        if self.identifier in propList:
            propList.remove(self.identifier)
            userprop.removeUserProp(sceneRoot, self.identifier)
        userprop.setUserPropList(sceneRoot, self.listStorage, propList)

    def _load(self):
        sceneRoot = sceneUtils.getSceneRootNode()
        propList = userprop.getUserPropList(sceneRoot, self.listStorage)
        if propList is not None:
            if self.identifier in propList:
                preset = userprop.getUserProp(sceneRoot, self.identifier)
                self.name = preset

    def _write(self):
        sceneRoot = sceneUtils.getSceneRootNode()
        propList = userprop.getUserPropList(sceneRoot, self.listStorage)
        if (propList is None):
            presetList = list()
        else:
            presetList = propList
        if self.name is None:
            newPreset = self.defaultName
        else:
            newPreset = self.name
        if self.identifier not in presetList:
            presetList.append(self.identifier)
        userprop.setUserProp(sceneRoot, self.identifier, newPreset)
        userprop.setUserPropList(sceneRoot, self.listStorage, presetList)


class OptionPresetObject(SerializableObject):
    """Stores a name and a dictionary in the root node
    """
    def __init__(self, identifier, listStorage=const.PROP_OPTIONS_LIST):
        SerializableObject.__init__(self, identifier, listStorage)
        self.listStorage = listStorage
        self.defaultName = "New Option Preset"
        self.name = None
        self.dictionary = None
        self._load()

    def get(self):
        self._load()
        return (self.name, self.dictionary)
        
    def edit(self, name=None, dictionary=None):
        self._load()
        self.name = self.name if name is None else name
        self.dictionary = self.dictionary if dictionary is None else dictionary
        self._write()

    def create(self, name, dictionary={}):
        self.name = name
        self.dictionary = dictionary
        self._write()

    def _load(self):
        sceneRoot = sceneUtils.getSceneRootNode()
        propList = userprop.getUserPropList(sceneRoot, self.listStorage)
        if propList is not None:
            if self.identifier in propList:
                groupTuple = userprop.getUserPropHeadedDict(
                    sceneRoot, self.identifier)
                if(isinstance(groupTuple, tuple)):
                    self.name = groupTuple[0]
                    self.dictionary = groupTuple[1]

    def _write(self):
        sceneRoot = sceneUtils.getSceneRootNode()
        propList = userprop.getUserPropList(sceneRoot, self.listStorage)
        if (propList is None):
            presetList = list()
        else:
            presetList = propList

        if self.name is None:
            self.name = self.defaultName
        newGroup = (self.name, self.dictionary)
        if self.identifier not in presetList:
            presetList.append(self.identifier)
        userprop.setUserPropHeadedDict(sceneRoot, self.identifier, newGroup)
        userprop.setUserPropList(sceneRoot, self.listStorage, presetList)

class GroupObject(SerializableObject):
    """Stores a name and an identifier in the root node
    """
    def __init__(self, identifier, listStorage = const.PROP_PRESET_GROUP_LIST):
        SerializableObject.__init__(self, identifier, listStorage)
        self.listStorage = listStorage
        self.defaultName = "New Group"
        self.optionPreset = None
        self._load()

    def get(self):
        self._load()
        return (self.name, self.optionPreset)

    def edit(self, name=None, optionPreset=None):
        self._load()
        self.name = self.name if name is None else name
        self.optionPreset = self.optionPreset if optionPreset is None else optionPreset
        self._write()

    def create(self, name, optionPreset=None):
        self.name = name
        self.optionPreset = optionPreset
        self._write()

    def delete(self):
        self._load()
        sceneRoot = sceneUtils.getSceneRootNode()
        propList = userprop.getUserPropList(sceneRoot, self.listStorage)
        if self.identifier in propList:
            propList.remove(self.identifier)
            userprop.removeUserProp(sceneRoot, self.identifier)
        userprop.setUserPropList(sceneRoot, self.listStorage, propList)

    def _load(self):
        sceneRoot = sceneUtils.getSceneRootNode()
        propList = userprop.getUserPropList(sceneRoot, self.listStorage)
        if propList is not None:
            if self.identifier in propList:
                preset = userprop.getUserPropList(sceneRoot, self.identifier)
                self.name = preset[0]
                
                self.optionPreset = None if len(preset) < 2 else preset[1]

    def _write(self):
        sceneRoot = sceneUtils.getSceneRootNode()
        propList = userprop.getUserPropList(sceneRoot, self.listStorage)
        if (propList is None):
            presetList = list()
        else:
            presetList = propList
        newPreset = []
        if self.name is None:
            newPreset.append(self.defaultName)
        else:
            newPreset.append(self.name)

        newPreset.append(self.optionPreset)
        
        if self.identifier not in presetList:
            presetList.append(self.identifier)
        userprop.setUserPropList(sceneRoot, self.identifier, newPreset)
        userprop.setUserPropList(sceneRoot, self.listStorage, presetList)


class PresetObject(SerializableObject):
    """Stores a name, a group identifier, a path and a list of layer names in the root node
    """
    def __init__(self, identifier, listStorage = const.PROP_PRESET_LIST):
        self.identifier = identifier
        self.listStorage = listStorage
        self.defaultName = "New Preset"
        self.name = None
        self.group = None
        self.path = None
        self.layerNames = None
        self._load()
    
    def get(self):
        self._load()
        return (self.name,self.group,self.path,self.layerNames)

    def edit(self, name=None, group=None, path=None, layerNames=None):
        self._load()
        self.name = self.name if name is None else name
        self.group = self.group if group is None else group
        self.path = self.path if path is None else path
        self.layerNames = self.layerNames if layerNames is None else layerNames
        self._write()

    def create(self, name, group, path, layerNames=[]):
        self.name = name
        self.group = group
        self.path = path
        self.layerNames = layerNames
        self._write()

    def _load(self):
        sceneRoot = sceneUtils.getSceneRootNode()
        propList = userprop.getUserPropList(sceneRoot, self.listStorage)
        if propList is not None:
            if self.identifier in propList:
                preset = userprop.getUserPropList(sceneRoot, self.identifier)
                self.name = preset[const.PROP_PRESET_PARAM_NAME_ID]
                self.group = preset[const.PROP_PRESET_PARAM_GROUP_ID]
                self.path = preset[const.PROP_PRESET_PARAM_PATH_ID]
                self.layerNames = preset[const.PROP_PRESET_PARAM_OFFSET: len(
                    preset)]

    def _write(self):
        sceneRoot = sceneUtils.getSceneRootNode()
        propList = userprop.getUserPropList(sceneRoot, self.listStorage)
        if (propList is None):
            presetList = list()
        else:
            presetList = propList
        newPreset = []
        newPreset.insert(const.PROP_PRESET_PARAM_NAME_ID, str(
            self.defaultName) if self.name is None else str(self.name))
        newPreset.insert(const.PROP_PRESET_PARAM_GROUP_ID,
                         "-" if self.group is None else self.group)
        newPreset.insert(const.PROP_PRESET_PARAM_PATH_ID,
                         ".\\" if self.path is None else self.path)
        for layer in self.layerNames:
            newPreset.append(layer)
        if self.identifier not in presetList:
            presetList.append(self.identifier)
        userprop.setUserPropList(sceneRoot, self.identifier, newPreset)
        userprop.setUserPropList(sceneRoot, self.listStorage, presetList)


def getDefaultExportPresetOptions():
    sceneRoot = sceneUtils.getSceneRootNode()
    optionPresetList = userprop.getUserPropList(sceneRoot, const.PROP_OPTIONS_LIST)
    option = OptionPresetObject(optionPresetList[0])
    return option

# PRESET AND PRESET GROUP UTILITY
def createNewPreset(labelName=None, group=None, filePath=None, layerNames=None):
    """
    Creates a new preset, writes it to the root node and return a reference to the PresetObject Wrapper

    \nin:
    labelName=str
    group=str : GroupObject.identifier
    filePath=str
    layerNames=list(str)

    \nout:
    PresetObject
    """
    presetID = uuid.uuid4()      
    presetName = const.PROP_PRESET_ENTRY_PREFIX.format(presetID)
    storage = const.PROP_PRESET_LIST
    preset = PresetObject(presetName,storage)
    preset.create(name=labelName,group=group, path=filePath, layerNames=[] if layerNames is None else layerNames)
    return preset


def createNewGroup(groupName=None,optionPreset=None):
    """
    Creates a new preset group, writes it to the root node and return a reference to the GroupObject Wrapper

    \nin:
    groupName=str
    optionPreset=str : OptionPresetObject.identifier

    \nout:
    GroupObject
    """
    groupHash = uuid.uuid4()
    groupID = const.PROP_PRESET_GROUP_ENTRY_PREFIX.format(groupHash)
    storage = const.PROP_PRESET_GROUP_LIST      
    group = GroupObject(groupID, storage)
    group.create(name=groupName,optionPreset=optionPreset)
    return group


def confirmAndRemove(groups=[], presets=[], refreshFunc=None):
    """Opens a dialog to confirm the user wants to delete passed groups and presets.
    """
    passAll = False
    rejectAll = False
    for preset in presets:
        if(passAll == False):
            popup = qtUtils.popup_Yes_YesToAll_No_NoToAll(
                title="Delete Preset ?", text="Are you sure you want to delete the preset {0}".format(preset.name))
            if popup == 0:
                rejectAll = True
                break
            if popup == 2:
                passAll = True
            if popup < 2:
                continue
        preset.delete()
        if refreshFunc is not None:
            refreshFunc()
    for group in groups:
        if rejectAll == True:
            break
        if(passAll == False):
            popup = qtUtils.popup_Yes_YesToAll_No_NoToAll(
                title="Delete Group ?", text="Are you sure you want to delete the group {0}".format(group.name))
            if(popup == 0):
                break
            if(popup == 2):
                passAll = True
            if (popup < 2):
                continue
        group.delete()
        if refreshFunc is not None:
            refreshFunc()


def removePreset(preset):
    preset.delete()


def removeGroup(group):
    group.delete()


def getExportPath(presetID):
    rootNode = sceneUtils.getSceneRootNode()
    presetParam = userprop.getUserPropList(rootNode, presetID)
    return presetParam[const.PROP_PRESET_PARAM_PATH_ID]


def getAbsoluteExportPath(presetID):
    expPath = presetID.path
    return utility.convertRelativePathToAbsolute(expPath, rt.pathConfig.getCurrentProjectFolder())


def addExportPathToPresets(presets):
    for preset in presets:
        initDir = os.path.split(getAbsoluteExportPath(preset))[0]
        expPath = askForNewPath(
            "Export Path for {}".format(preset.name), initDir=initDir)
        if(expPath != None):
            preset.edit(path=expPath)


def askForNewPath(title="", initDir=""):
    """Opens a dialog to get a new path from the user
    """
    expPath = qtUtils.openSaveFileNameDialog(
        caption=title,  _filter="GLTF(*.gltf)", _dir=initDir)
    if expPath != None:
        expPath = utility.convertAbsolutePathToRelative(
            expPath, rt.pathConfig.getCurrentProjectFolder())
    return expPath
