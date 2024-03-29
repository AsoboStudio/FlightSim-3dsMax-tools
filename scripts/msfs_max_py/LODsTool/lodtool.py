import json
import os
import re
import pymxs
from maxsdk.globals import *


from PySide2 import QtWidgets
from PySide2.QtUiTools import QUiLoader

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

if MAXVERSION() < MAX2017:
    import MaxPlus
    from maxsdk import serializable as sdk_serializable
    max = MaxPlus.Core.EvalMAXScript
else:
    max = pymxs.runtime.execute

qtMainwindows = GetMaxMainWindow()

rt = pymxs.runtime


from maxsdk import utility

from maxsdk import layer as sdk_layer
from maxsdk import node as sdk_node
from maxsdk import animation as sdk_anim
from maxsdk import sceneUtils, userprop

from MultiExporter import presetUtils,constants  # force to start from the package added in sys.path

# import maxsdk.debug

UI = None
LOD_PREFIX = "x"
LOD_NUMBER = 0
SAVE_PATH = os.path.dirname(os.path.realpath(__file__))
TRIS_COUNT = 0

LOGGER = None


class LodTool(QtWidgets.QDialog):

    def __init__(self, ui_path, parent=qtMainwindows):
        
        super(LodTool, self).__init__(parent)
        loader = QUiLoader()
        self.setMinimumWidth(500)
        self.ui = loader.load(ui_path)
        mainLayout = QtWidgets.QVBoxLayout()
        self.setLayout(mainLayout)
        mainLayout.addWidget(self.ui)
        self.prefix_line = self.ui.findChildren(QtWidgets.QLineEdit, 'prefixLine')[0]
        self.prefix_line.setText(LOD_PREFIX)
        self.lod_label = self.ui.findChildren(QtWidgets.QLabel, 'lodLabel')[0]
        self.tri_count_label = self.ui.findChildren(QtWidgets.QLabel, 'trisCountLabel')[0]

        self._groupDict = {}
        self._rootDict = {}
        self.lod_slider = self.ui.findChildren(QtWidgets.QSlider, 'lodSlider')[0]
        self.lod_slider.valueChanged.connect(self.on_slider_value_changed)

        self.reduce_checker = self.ui.findChildren(QtWidgets.QCheckBox, "reduceCheckBox")[0]
        self.reduce_amount = self.ui.findChildren(QtWidgets.QSpinBox, "reduceAmountSpin")[0]

        self.create_next_lod = self.ui.findChildren(QtWidgets.QPushButton, 'createLodBtn')[0]
        self.create_next_lod.clicked.connect(self.on_next_lod_btn_click)

        self.source_subtitle = self.ui.findChildren(QtWidgets.QLabel, 'label_3')[0]
        self.animation_label = self.ui.findChildren(QtWidgets.QLabel, 'label_4')[0]
        self.target_subtitle = self.ui.findChildren(QtWidgets.QLabel, 'label_5')[0]

        #------------------------------
        self.source_lod = self.ui.findChildren(QtWidgets.QComboBox, "sourceLod")[0]
        self.source_lod_index = self.source_lod.currentIndex()

        self.target_lod = self.ui.findChildren(QtWidgets.QComboBox, "targetLod")[0]
        self.target_lod_index = self.target_lod.currentIndex()

        self.copy_lod = self.ui.findChildren(QtWidgets.QPushButton, "copyAnimationLod")[0]

        self.copy_skin = self.ui.findChildren(QtWidgets.QPushButton, "copySkinLod")[0]
        self.copySkinBySelectionRadio = self.ui.findChildren(QtWidgets.QRadioButton, "copySkinBySelection")[0]

        self.copy_hierarchy = self.ui.findChildren(QtWidgets.QPushButton, "copyHierarchyLod")[0]
        self.copyHierarchyBySelectionRadio = self.ui.findChildren(QtWidgets.QRadioButton, "copyHierarchyBySelection")[0]

        self.save_lod = self.ui.findChildren(QtWidgets.QPushButton, "saveBtn")[0]
        self.load_lod = self.ui.findChildren(QtWidgets.QPushButton, "loadBtn")[0]
        self.replace_lod = self.ui.findChildren(QtWidgets.QLineEdit, "replaceLineEdit")[0]
        self.with_lod = self.ui.findChildren(QtWidgets.QLineEdit, "withLineEdit")[0]
        self.rename_btn = self.ui.findChildren(QtWidgets.QPushButton, "renameBtn")[0]
        self.rename_selection_lod_based = self.ui.findChildren(QtWidgets.QPushButton, "renameSelectionLodBased")[0]
        self.rename_btn.clicked.connect(self.on_rename_lod_btn_click)

        self.btn_ExpandAll = self.ui.findChildren(QtWidgets.QPushButton, 'ExpandAll')[0]
        self.btn_CollapseAll = self.ui.findChildren(QtWidgets.QPushButton, 'CollapseAll')[0]


        self.chkDetailView = self.ui.findChildren(QtWidgets.QCheckBox, 'chkDetailView')[0]
        self.chkDetailView.stateChanged.connect(self._chkDetailViewChanged)

        self.PrsToShowList = self.ui.findChildren(QtWidgets.QTreeWidget, 'PrsToShowList')[0]
        self.PrsToShowList.setAlternatingRowColors(True)
        self.PrsToShowList.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.PrsToShowList.setIndentation(10)
        self.PrsToShowList.setSortingEnabled(True)
        self.PrsToShowList.sortItems(0, Qt.SortOrder.AscendingOrder)
        self.PrsToShowList.header().setDefaultSectionSize(50)
        self.PrsToShowList.itemChanged.connect(self._modifyCheckBox)
        if self.chkDetailView.isChecked():
            self.PrsToShowList.setEnabled(True)
            self.createPresetTree(_LOD = self.lod_slider.value())
        else:
            self.PrsToShowList.setEnabled(False)

        self.btn_ExpandAll.clicked.connect(self.PrsToShowList.expandAll)
        self.btn_CollapseAll.clicked.connect(self.PrsToShowList.collapseAll)

        if MAXVERSION() < MAX2021:
            self.source_lod.currentIndexChanged.connect(self.on_source_lod_value_changed)
            self.target_lod.currentIndexChanged.connect(self.on_target_lod_value_changed)
            self.copy_lod.clicked.connect(self.on_copy_lod_btn_click)
            self.copy_skin.clicked.connect(self.on_copy_skin_lod_btn_click)
            self.copy_hierarchy.clicked.connect(self.on_copy_hierarchy_lod_btn_click)
            self.save_lod.clicked.connect(self.on_save_lod_btn_click)
            self.load_lod.clicked.connect(self.on_load_lod_btn_click)
            self.rename_selection_lod_based.clicked.connect(self.on_rename_selection_lod_based_click)
        else:
            self.source_lod.setVisible(False)
            self.target_lod.setVisible(False)
            self.copy_lod.setVisible(False)
            self.copy_skin.setVisible(False)
            self.copySkinBySelectionRadio.setVisible(False)
            self.copy_hierarchy.setVisible(False)
            self.copyHierarchyBySelectionRadio.setVisible(False)
            self.save_lod.setVisible(False)
            self.load_lod.setVisible(False)
            self.rename_selection_lod_based.setVisible(False)
            self.source_subtitle.setVisible(False)
            self.animation_label.setVisible(False)
            self.target_subtitle.setVisible(False)


        global LOGGER
        LOGGER = self.ui.findChildren(QtWidgets.QTextBrowser, "logger")[0]

        global LOD_NUMBER
        LOD_NUMBER = self.lod_slider.maximum()

    def _gatherScenePresets(self):
        
        rootNode = sceneUtils.getSceneRootNode()
        presetList = userprop.getUserPropList(rootNode, constants.PROP_PRESET_LIST)
        presets = []
        if presetList is not None:
            for presetID in presetList:
                p = presetUtils.PresetObject(presetID)
                presets.append(p)
        return presets

    def _gatherGroups(self):
        rootNode = sceneUtils.getSceneRootNode()
        groupList = userprop.getUserPropList(rootNode, constants.PROP_PRESET_GROUP_LIST)
        groups = []
        if groupList is not None:
            for groupID in groupList:
                g = presetUtils.GroupObject(groupID)
                groups.append(g)
        return groups

    def createPresetTree(self, _LOD):
        self.PrsToShowList.clearSelection()
        self.PrsToShowList.clear()
        self._groupDict.clear()
        self._rootDict.clear()
        PresetsList = self._gatherScenePresets()
        groups = self._gatherGroups()
        if (isinstance(groups, list) and groups is not None):
            for g in groups:
                qTreeWidget = QTreeWidgetItem()
                qTreeWidget.setFlags(Qt.ItemIsDropEnabled | Qt.ItemIsEditable | Qt.ItemIsSelectable |
                                     Qt.ItemIsDragEnabled | Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
                qTreeWidget.setCheckState(0, Qt.CheckState.Unchecked)
                qTreeWidget.setText(0, str(g.name))
                self._groupDict[g] = qTreeWidget
                self.PrsToShowList.addTopLevelItem(qTreeWidget)
        if (isinstance(PresetsList, list) and PresetsList is not None):
            for r in PresetsList:
                if "LOD0{0}".format(str(_LOD)) in r.name:
                    qTreeWidgetPreset = QTreeWidgetItem()
                    qTreeWidgetPreset.setText(0, r.name) #Preset name
                    qTreeWidgetPreset.setCheckState(0,Qt.CheckState.Unchecked)
                    self._rootDict[qTreeWidgetPreset] = r
                    group = None
                    for k in self._groupDict.keys():
                        if k.identifier == r.group:
                            group = k
                            break
                    if (group != None):
                        self._groupDict[group].addChild(qTreeWidgetPreset)
                    else:
                        self.addTopLevelItem(qTreeWidgetPreset)
        self.PrsToShowList.expandAll()

    def getQTChildrens(self, item):
        hierarchy = []
        hierarchy.append(item)
        for i in range(item.childCount()):
            c = item.child(i)
            hierarchy += self.getQTChildrens(c)
        return hierarchy        

    def _modifyCheckBox(self, _lastQtItem):
        selection = self.PrsToShowList.selectedItems()
        childs = self.getQTChildrens(_lastQtItem)
        if childs != None:
            for ch in childs:
                ch.setCheckState(0, _lastQtItem.checkState(0))
        if len(selection) > 1:
            self.PrsToShowList.itemChanged.disconnect(self._modifyCheckBox)
            for qti in selection:
                qti.setCheckState(0, _lastQtItem.checkState(0))
            self.PrsToShowList.itemChanged.connect(self._modifyCheckBox)
        self._showCheckedLayers()

    def _showCheckedLayers(self):
        sdk_layer.disableAll()
        showLOD(self.lod_slider.value())
        layersToShow = []
        for qtPres in self._rootDict:
            if qtPres.checkState(0) == Qt.Checked:
                for LayName in self._rootDict[qtPres].layerNames:
                    lay = sdk_layer.get_layer(LayName)
                    if lay != None:
                        layersToShow.append(lay)
        sdk_layer.enableThese(layersToShow)
                        
    def _chkDetailViewChanged(self):
        if self.chkDetailView.isChecked():
            self.PrsToShowList.setEnabled(True)
            self.createPresetTree(_LOD = self.lod_slider.value())
        else:
            self.PrsToShowList.setEnabled(False)

    def on_slider_value_changed(self):
        rt.disableSceneRedraw()
        hideAllLODs()
        showLOD(self.lod_slider.value())
        self.tri_count_label.setText(str(TRIS_COUNT))
        rt.enableSceneRedraw()
        if self.chkDetailView.isChecked():
            self.createPresetTree(_LOD = self.lod_slider.value())


    def on_source_lod_value_changed(self):
        self.source_lod_index = self.source_lod.currentIndex()

    def on_target_lod_value_changed(self):
        self.target_lod_index = self.target_lod.currentIndex()

    def on_copy_skin_lod_btn_click(self):
        copy_lod_skin(self.source_lod_index, self.target_lod_index, self.copySkinBySelectionRadio.isChecked())

    def on_copy_hierarchy_lod_btn_click(self):
        copy_lod_hierarchy(self.source_lod_index, self.target_lod_index, self.copyHierarchyBySelectionRadio.isChecked())

    def on_copy_lod_btn_click(self):
        copy_lod_animations(self.source_lod_index, self.target_lod_index)

    def on_save_lod_btn_click(self):
        options = QtWidgets.QFileDialog.Options()
        fileName, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save Animation info", "",
                                                            "JSON Files (*.json)", options=options)
        if not fileName:
            return
        save_lod_animations(self.source_lod_index, fileName)

    def on_load_lod_btn_click(self):
        options = QtWidgets.QFileDialog.Options()
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Load Animation info", "",
                                                            "JSON Files (*.json)", options=options)
        if not fileName:
            return
        load_lod_animations(self.target_lod_index, fileName)

    def on_next_lod_btn_click(self):
        poly_reduce = self.reduce_checker.isChecked()
        reduce_amount = self.reduce_amount.value()
        create_next_lod(poly_reduce, reduce_amount)

    def on_rename_lod_btn_click(self):
        old_name = self.replace_lod.text()
        new_name = self.with_lod.text()
        rename_lod(old_name, new_name)

    def on_rename_selection_lod_based_click(self):
        rename_node_based_on_lod0()


def setLodVisibility(lod_value, lod_visibility):
    lyrPrefix = UI.prefix_line.text() + str(lod_value)
    lyr = rt.LayerManager.getLayerFromName(lyrPrefix)
    if lyr:
        lyr.on = lod_visibility
        if lod_visibility:
            descendents = sdk_layer.getLayerDescendants([lyr])
            for descendentLayer in descendents:
                descendentLayer.on = lod_visibility
                nodesInLayer = sdk_layer.getNodesInLayer(descendentLayer)
                for n in nodesInLayer:
                    rt.unhide(n)
                global TRIS_COUNT
                TRIS_COUNT = sdk_node.getTrisCount(sdk_layer.getAllNodeInLayerTree(lyr))
                log_clear()

def showLOD(LODValue):
    setLodVisibility(LODValue, True)
    lyrPrefix = UI.prefix_line.text() + str(LODValue)
    UI.lod_label.setText("Tool is looking for: " + lyrPrefix)
    lyr = rt.LayerManager.getLayerFromName(lyrPrefix)
    if not lyr:
        log_verbose("MISSING LAYER: " + lyrPrefix)


def hideAllLODs():
    for i in range(LOD_NUMBER + 1):
        setLodVisibility(i, False)


def set_new_copy_layer(n, curren_prefix, next_prefix):
    previous_name = n.name.replace(next_prefix, curren_prefix)
    previous_node = sdk_node.get_node_by_name(previous_name) #MaxPlus.INode.GetINodeByName(previous_name)
    l = previous_node.layer
    new_layer_name = l.name.replace(curren_prefix, next_prefix)
    new_layer = sdk_layer.get_layer(new_layer_name) #MaxPlus.LayerManager.GetLayer(new_layer_name)
    new_layer.addnode(n)


def reduce_polygon_amount(n, poly_reduce, reduce_amount):
    if not poly_reduce or reduce_amount == 0:
        return
    node = rt.getNodeByName(n.name)
    mod = rt.ProOptimizer()
    mod.VertexPercent = reduce_amount
    mod.KeepUV = True
    mod.LockUV = True
    mod.LockMat = True
    mod.OptimizationMode = 1
    mod.ToleranceUV = 0.1
    mod.KeepVC = True
    mod.MergePoints = True
    mod.MergePointsThreshold = 0.01
    rt.addModifier(node, mod)
    rt.CompleteRedraw()
    p = node.modifiers[0]
    p.Calculate = True


def clone_layer_hierarchy(root, parent, func):
    new_lyr = rt.LayerManager.newLayer()
    new_lyr.setName(root.name + "_temp")
    func(new_lyr) #rename layer
    if parent is not None:
        new_lyr.setParent(parent)

    num_children = root.getNumChildren()
    for i in range(1, num_children + 1):
        child = root.getChild(i)
        clone_layer_hierarchy(child, new_lyr, func)


def create_next_lod(poly_reduce, reduce_amount):
    selected_layer = sdk_layer.getSelectedLayer()
    try:
        if selected_layer is None:
            log_verbose("Select a LOD layer")
            return
        if not selected_layer.name.startswith(LOD_PREFIX):
            log_verbose("Select a valid LOD layer")
            return
        # remove LOD prefix and get the index
        current_lod_index = selected_layer.name[len(LOD_PREFIX):][0]
    except Exception as error:
        log_verbose("Select a valid root LOD layer >>{0}".format(error))
        return

    rt_lyr = rt.LayerManager.getLayerFromName(selected_layer.name)
    next_lod_index = int(current_lod_index) + 1
    current_prefix = LOD_PREFIX + str(current_lod_index)
    next_prefix = LOD_PREFIX + str(next_lod_index)

    nextLayerName = rt_lyr.name.replace(current_prefix, next_prefix)
    ex = rt.LayerManager.getLayerFromName(nextLayerName)

    clone_layer_hierarchy(rt_lyr, None, lambda l: utility.replace_layer_prefix(l, current_prefix, next_prefix))

    # all the nodes in layer hierachy that are child of Max Root node
    source_children = sdk_layer.getAllNodeInLayerTree(rt_lyr)
    lyr_root_children = []
    for s in source_children:
        if s.parent not in source_children:
            lyr_root_children.append(s)

    if len(lyr_root_children) <= 0:
        log_verbose("Root node is not under layer hierarchy")

    replace_node_lamba = lambda n: utility.replace_node_prefix(n, current_prefix, next_prefix)
    set_layer_lambda = lambda n: set_new_copy_layer(n, current_prefix, next_prefix)
    reduce_poly_lmbda = lambda n: reduce_polygon_amount(n, poly_reduce, reduce_amount)

    lambda_list = [set_layer_lambda, reduce_poly_lmbda]
    for obj in lyr_root_children:
        utility.clone_hierarchy(obj, obj.parent, replace_node_lamba, lambda_list)


def copy_anim(source, target):
    if target is None:
        return
    # print "copy {0} in {1}".format(source.GetName(), target.GetName())
    source_transform_control = utility.GetTransformControl(source)

    pos_controller = source_transform_control.GetPositionController()
    rot_controller = source_transform_control.GetRotationController()
    scale_controller = source_transform_control.GetScaleController()

    # todo: make some check (pivot are the same)?
    utility.copy_transform_from_controller(pos_controller, source.GetName(), target.GetName())
    utility.copy_transform_from_controller(rot_controller, source.GetName(), target.GetName())
    utility.copy_transform_from_controller(scale_controller, source.GetName(), target.GetName())


def copy_skin(skinned, toskin):
    if list(skinned.Modifiers) is None:
        return
    hasSkin = False
    for m in skinned.Modifiers:
        mod_name = str(m)
        if mod_name == "Animatable(Skin)":
            hasSkin = True
    if hasSkin:
        if MAXVERSION() < MAX2017:
            toskin.Convert(MaxPlus.ClassIds.PolyMeshObject)
            MaxPlus.SelectionManager.SelectNode(toskin)
        else:
            rt.convertToPoly(toskin)
            rt.select(toskin)

        max("max modify mode")
        sdk_node.removeAllModifiers(toskin)
        log_append("TRYING copying skin from {0} to {1}".format(skinned.GetName(), toskin.GetName()))
        max("addMesh = #(${0});addModifier ${1}(Skin_Wrap());${1}.modifiers[#Skin_Wrap].meshList = addMesh;".format(
            skinned.GetName(), toskin.GetName()))
        max("$.modifiers[#Skin_Wrap].ConvertToSkin on")
        max("deleteModifier $ 2")
        log_append("SUCCESS")


def save_lod_animations(source_lod_index, path):
    src_lod_prefix = UI.prefix_line.text() + str(source_lod_index)
    lod_source_root = rt.LayerManager.getLayerFromName(src_lod_prefix)
    if lod_source_root is None:
        log_verbose("MISSING LOD LAYER: " + src_lod_prefix)
        return
    src_lod_nodes = sdk_layer.getAllNodeInLayerHierarchy(lod_source_root)
    animated_nodes = []

    # filters nmode
    for n in src_lod_nodes:
        if (n.IsAnimated()):
            animated_nodes.append(n)

    current_time = sdk_anim.get_animTime()

    MaxPlus.ViewportManager.DisableSceneRedraw() if MAXVERSION() < MAX2017 else rt.disableSceneRedraw()      
    # serialzie with custom encoder
    with open(path, 'w') as outfile:
        jsonFile = json.dumps([ob for ob in animated_nodes], outfile, cls=sdk_serializable.INodeEncoder, indent=4)
        outfile.write(jsonFile)

    if MAXVERSION() < MAX2017:
        MaxPlus.ViewportManager.EnableSceneRedraw()
        MaxPlus.Animation.SetTime(current_time, True)
    else:
        rt.enableSceneRedraw()
        rt.sliderTime = current_time



def load_lod_animations(target_lod_index, fileName):
    with open(fileName) as json_file:
        data = json.load(json_file)
        for p in data:
            sdk_serializable.INodeEncoder.decodeNode(p)


def copy_lod_animations(source_lod_index, target_lod_index):
    if source_lod_index == target_lod_index:
        log_verbose("You can't copy,source and target are the same")
        return
    src_lod_prefix = UI.prefix_line.text() + str(source_lod_index)
    lod_source_root = rt.LayerManager.getLayerFromName(src_lod_prefix)
    if lod_source_root is None:
        log_verbose("MISSING LOD LAYER: " + src_lod_prefix)
        return

    src_lod_nodes = utility.get_unparent_nodes_in_layer_hierarchy(lod_source_root)

    target_lod_prefix = UI.prefix_line.text() + str(target_lod_index)
    target_root_lod = rt.LayerManager.getLayerFromName(target_lod_prefix)
    if target_root_lod is None:
        log_verbose("MISSING LOD LAYER: " + target_lod_prefix)
        return
    target_lod_nodes = sdk_layer.getAllNodeInLayerHierarchy(target_root_lod)

    for t in target_lod_nodes:
        # remove all animations in target
        utility.remove_transform_keys(t)

    current_time = sdk_anim.get_animTime()

    if MAXVERSION() < MAX2017:
        MaxPlus.ViewportManager.DisableSceneRedraw()
    else:
        rt.disableSceneRedraw()

    for s in src_lod_nodes:
        children_list = [s]
        children_list += list(utility.GetChildren(s))
        for c in children_list:
            # find the binomial node and copy
            s_name = c.GetName().replace(src_lod_prefix, "")
            t = c.GetName().replace(src_lod_prefix, target_lod_prefix)
            target = utility.GetObjectByName(t)
            t_name = t.replace(target_lod_prefix, "")
            if s_name == t_name and target is not None:
                copy_anim(c, target)
                utility.remove_unused_key(c, target)

    if MAXVERSION() < MAX2017:
        MaxPlus.ViewportManager.EnableSceneRedraw()
        MaxPlus.Animation.SetTime(current_time, True)
    else:
        rt.enableSceneRedraw()
        rt.sliderTime = current_time



def copy_lod_skin(source_lod_index, target_lod_index, selectionBased=False):
    if source_lod_index == target_lod_index:
        log_verbose("You can't copy,source and target are the same")
        return

    src_lod_prefix = UI.prefix_line.text() + str(source_lod_index)
    target_lod_prefix = UI.prefix_line.text() + str(target_lod_index)

    lod_source_root = rt.LayerManager.getLayerFromName(src_lod_prefix)
    if lod_source_root is None:
        log_verbose("MISSING LOD LAYER: " + src_lod_prefix)
        return

    src_lod_nodes = sdk_layer.getAllNodeInLayerHierarchy(lod_source_root)

    if selectionBased:
        selection = sdk_node.get_selected_nodes()
        for n in selection:
            if n in src_lod_nodes:
                # find the binomial node and copy
                targetName = n.GetName().replace(src_lod_prefix, target_lod_prefix)
                target = sdk_node.get_node_by_name(targetName)
                if target:
                    target_no_lod = target.GetName().replace(target_lod_prefix, "")
                    source_nod_lod = n.GetName().replace(src_lod_prefix, "")
                    if target_no_lod == source_nod_lod:
                        copy_skin(n, target)
                else:
                    log_append(
                        "{0} not copied, cant found a binomial node {1} on next LOD".format(n.GetName(), targetName))
            else:
                log_verbose("the selected node {0} is not part of the source LOD".format(n.GetName()))
    else:

        target_root_lod = rt.LayerManager.getLayerFromName(target_lod_prefix)
        if target_root_lod is None:
            log_verbose("MISSING LOD LAYER: " + target_lod_prefix)
            return
        target_lod_nodes = sdk_layer.getAllNodeInLayerHierarchy(target_root_lod)

        log_clear()
        for t in target_lod_nodes:
            # find the binomial node and copy
            t_name = t.GetName().replace(target_lod_prefix, "")
            skinned_name = t.GetName().replace(target_lod_prefix, src_lod_prefix)
            skinned = utility.GetObjectByName(skinned_name)
            if skinned is None:
                continue
            else:
                s_name = skinned.GetName().replace(src_lod_prefix, "")
                if s_name == t_name:
                    copy_skin(skinned, t)


def copy_lod_hierarchy(source_lod_index, target_lod_index, selectionBased=False):
    if source_lod_index == target_lod_index:
        log_verbose("You can't copy,source and target are the same")
        return

    src_lod_prefix = UI.prefix_line.text() + str(source_lod_index)
    target_lod_prefix = UI.prefix_line.text() + str(target_lod_index)

    lod_source_root = rt.LayerManager.getLayerFromName(src_lod_prefix)
    if lod_source_root is None:
        log_verbose("MISSING LOD LAYER: " + src_lod_prefix)
        return

    src_lod_nodes = sdk_layer.getAllNodeInLayerHierarchy(lod_source_root)

    if selectionBased:
        selection = sdk_node.get_selected_nodes()
        for n in selection:
            if n in src_lod_nodes:
                if (n.GetParent().IsRoot):
                    continue
                # find the binomial node and copy
                targetName = n.GetName().replace(src_lod_prefix, target_lod_prefix)
                target = sdk_node.get_node_by_name(targetName) #MaxPlus.INode.GetINodeByName(targetName)
                if target:
                    target.SetParent(n.GetParent())
                    log_append("OK: {0} new parent is {1}".format(targetName, n.GetParent().GetName()))
                else:
                    log_append("WARNING: {0} skipped, cant found {1} on next LOD".format(n.GetName(), targetName))
            else:
                log_verbose("WARNING: {0} is not part of the source LOD".format(n.GetName()))
    else:

        for n in src_lod_nodes:
            if (n.GetParent().IsRoot):
                continue
            # find the binomial node and copy
            targetName = n.GetName().replace(src_lod_prefix, target_lod_prefix)
            target = sdk_node.get_node_by_name(targetName)
            if target:
                target.SetParent(n.GetParent())
                log_append("OK: {0} new parent is {1}".format(targetName, n.GetParent().GetName()))
            else:
                log_append("WARNING: {0} skipped, cant found {1} on next LOD".format(n.GetName(), targetName))


def rename_lod(old_name, new_name):
    if not new_name:
        log_verbose("New name for {0} is not defined".format(old_name))
        return
    scene_node = list(utility.getAllNodes())
    scene_layers = sdk_layer.getAllLayers()
    scene_object = scene_layers + scene_node

    regex = "^(?i)x[0-9]_{0}$".format(old_name)
    log_clear()
    matched = []
    for n in scene_object:
        if re.match(regex, n.name):
            matched.append(n)
    if len(matched) == 0:
        log_verbose("No result found")
    else:
        for n in matched:
            prefix = n.name[:3].lower()
            result = prefix + new_name
            log_append("{0} rename into {1}".format(n.name, result))
            n.setName(result)


def rename_node_based_on_lod0():
    selected = sdk_node.get_selected_nodes() #MaxPlus.SelectionManager.GetNodes()
    if not selected:
        return
    message = "Do you really want to rename following nodes:\n"
    for node in selected:
        message = message + node.GetName() + "\n"

    if (display_confirm_message(message)):
        orderedInLodLayer = []
        nodeNameWithoutLOD = None
        for node in selected:
            layerName = node.GetLayer().GetName()
            regex = "^x[0-9]"
            if re.match(regex, layerName):
                if node.GetName()[1] == "0":
                    nodeNameWithoutLOD = node.GetName()[3:]
                orderedInLodLayer.append(node)
            else:
                log_verbose(node.GetName() + " is not under a lod layer")
        for node in orderedInLodLayer:
            layerName = node.GetLayer().GetName()
            lodValue = layerName[1]
            node.SetName("x{0}_{1}".format(lodValue, nodeNameWithoutLOD))


def log_append(value):
    text = LOGGER.toPlainText()
    LOGGER.setText(text + value + "\n")


def log_verbose(value):
    LOGGER.setText(value)


def log_clear():
    LOGGER.setText("")


def display_message(message):
    msg_box = QtWidgets.QMessageBox(qtMainwindows)
    msg_box.setText(message)
    msg_box.show()


def display_confirm_message(message):
    msg_box = QtWidgets.QMessageBox(qtMainwindows)
    msg_box.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.Cancel)
    msg_box.setDefaultButton(QtWidgets.QMessageBox.Yes)
    msg_box.setText(message)
    ret = msg_box.exec_()
    if ret == QtWidgets.QMessageBox.Yes:
        return True
    else:
        return False


def run():
    ui_path = os.path.join(os.path.dirname(__file__), "lod_tool.ui")
    global UI
    UI = LodTool(ui_path)
    UI.show()

