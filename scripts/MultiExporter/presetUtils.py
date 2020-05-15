import sys
import os
import uuid

import constants as const
from maxsdk import userprop, sceneUtils, qtUtils, utility
from pymxs import runtime as rt

reload(const)
reload(userprop)
reload(sceneUtils)
reload(qtUtils)

class SerializableObject():
    def __init__(self, identifier):
        self.identifier = identifier
        self.defaultName = "New Serializable Object"
        self.listStorage = "defaultSerializableObjectPool" #const.PROP_PRESET_GROUP_LIST
        self.name = None
        self._load()

    def __hash__(self):
        return self.identifier.__hash__()#hash(self.identifier)

    def __eq__(self, a):
        if isinstance(a,unicode) or isinstance(a,str):
            return self.identifier == a
        if(isinstance(a,PresetObject)):
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
        userprop.setUserPropList(sceneRoot, self.listStorage,presetList)

class GroupObject(SerializableObject):
    def __init__(self, identifier):
        SerializableObject.__init__(self, identifier)
        self.listStorage = const.PROP_PRESET_GROUP_LIST
        self.defaultName = "New Group"
        self._load()


class PresetObject(SerializableObject):
    def __init__(self, identifier):
        self.identifier = identifier
        self.listStorage = const.PROP_PRESET_LIST
        self.defaultName = "New Preset"
        self.name = None
        self.group = None
        self.path = None
        self.layerNames = None
        self._load()

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
                self.layerNames = preset[const.PROP_PRESET_PARAM_OFFSET : len(preset)]

    def _write(self):
        sceneRoot = sceneUtils.getSceneRootNode()
        propList = userprop.getUserPropList(sceneRoot, self.listStorage)
        if (propList is None):
            presetList = list()
        else:
            presetList = propList
        newPreset = []
        newPreset.insert(const.PROP_PRESET_PARAM_NAME_ID, str(self.defaultName) if self.name is None else str(self.name))
        newPreset.insert(const.PROP_PRESET_PARAM_GROUP_ID, "-" if self.group is None else self.group)
        newPreset.insert(const.PROP_PRESET_PARAM_PATH_ID, ".\\" if self.path is None else self.path)

        for layer in self.layerNames:
            newPreset.append(layer)
        if self.identifier not in presetList:
            presetList.append(self.identifier)

        userprop.setUserPropList(sceneRoot, self.identifier, newPreset)
        userprop.setUserPropList(sceneRoot, self.listStorage,presetList)

# PRESET AND PRESET GROUP UTILITY

def createNewPreset(labelName=None, group=None, filePath=None):
    presetID = uuid.uuid4()
    presetName = const.PROP_PRESET_ENTRY_PREFIX.format(presetID)
    preset = PresetObject(presetName)
    preset.create(labelName, group, filePath)
    return preset

def createNewGroup(groupName=None):
    groupHash = uuid.uuid4()
    groupID = const.PROP_PRESET_GROUP_ENTRY_PREFIX.format(groupHash)
    group = GroupObject(groupID)
    group.create(groupName)
    return group

def confirmAndRemove(groups=[], presets=[], refreshFunc=None):    
    passAll = False
    rejectAll = False
    for preset in presets:
        if(passAll == False):
            popup = qtUtils.popup_Yes_YesToAll_No_NoToAll(title="Delete Preset ?", text="Are you sure you want to delete the preset {0}".format(preset.name))
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
            popup = qtUtils.popup_Yes_YesToAll_No_NoToAll(title="Delete Group ?", text="Are you sure you want to delete the group {0}".format(group.name))
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
        expPath = askForNewPath("Export Path for {}".format(preset.name),initDir=initDir)
        if(expPath != None):                  
            preset.edit(path=expPath)

def askForNewPath(title = "", initDir =""):
    expPath = qtUtils.openSaveFileNameDialog(caption=title,  _filter ="GLTF(*.gltf)", _dir=initDir)
    if expPath != None:
        expPath = utility.convertAbsolutePathToRelative(expPath, rt.pathConfig.getCurrentProjectFolder())
    return expPath


