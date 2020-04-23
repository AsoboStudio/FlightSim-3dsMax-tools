import json
import sys
import os
import MaxPlus

import pymxs

rt = pymxs.runtime

max = MaxPlus.Core.EvalMAXScript

import re

from PySide2 import QtWidgets
from PySide2 import QtCore
from PySide2.QtUiTools import QUiLoader

# to add module from parent folder
parentFolder = os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)

if not parentFolder in sys.path:
    sys.path.append(parentFolder)

from maxsdk import utility

reload(utility)
from maxsdk import layer as sdk_layer

reload(sdk_layer)
from maxsdk import serializable as sdk_serializable

reload(sdk_serializable)
from maxsdk import ui as sdk_ui

reload(sdk_ui)
from maxsdk import node as sdk_node

reload(sdk_node)

# import maxsdk.debug

UI = None
LOD_PREFIX = "x"
LOD_NUMBER = 0
SAVE_PATH = os.path.dirname(os.path.realpath(__file__))
TRIS_COUNT = 0

LOGGER = None


class LodTool(QtWidgets.QDialog):

    def __init__(self, ui_path, parent=MaxPlus.GetQMaxMainWindow()):
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

        self.lod_slider = self.ui.findChildren(QtWidgets.QSlider, 'lodSlider')[0]
        self.lod_slider.valueChanged.connect(self.on_slider_value_changed)

        self.reduce_checker = self.ui.findChildren(QtWidgets.QCheckBox, "reduceCheckBox")[0]
        self.reduce_amount = self.ui.findChildren(QtWidgets.QSpinBox, "reduceAmountSpin")[0]

        self.create_next_lod = self.ui.findChildren(QtWidgets.QPushButton, 'createLodBtn')[0]
        self.create_next_lod.clicked.connect(self.on_next_lod_btn_click)

        self.source_lod = self.ui.findChildren(QtWidgets.QComboBox, "sourceLod")[0]
        self.source_lod_index = self.source_lod.currentIndex()
        self.source_lod.currentIndexChanged.connect(self.on_source_lod_value_changed)

        self.target_lod = self.ui.findChildren(QtWidgets.QComboBox, "targetLod")[0]
        self.target_lod_index = self.target_lod.currentIndex()
        self.target_lod.currentIndexChanged.connect(self.on_target_lod_value_changed)

        self.copy_lod = self.ui.findChildren(QtWidgets.QPushButton, "copyAnimationLod")[0]
        self.copy_lod.clicked.connect(self.on_copy_lod_btn_click)

        self.copy_skin = self.ui.findChildren(QtWidgets.QPushButton, "copySkinLod")[0]
        self.copy_skin.clicked.connect(self.on_copy_skin_lod_btn_click)
        self.copySkinBySelectionRadio = self.ui.findChildren(QtWidgets.QRadioButton, "copySkinBySelection")[0]

        self.copy_hierarchy = self.ui.findChildren(QtWidgets.QPushButton, "copyHierarchyLod")[0]
        self.copy_hierarchy.clicked.connect(self.on_copy_hierarchy_lod_btn_click)
        self.copyHierarchyBySelectionRadio = self.ui.findChildren(QtWidgets.QRadioButton, "copyHierarchyBySelection")[0]

        self.save_lod = self.ui.findChildren(QtWidgets.QPushButton, "saveBtn")[0]
        self.load_lod = self.ui.findChildren(QtWidgets.QPushButton, "loadBtn")[0]
        self.save_lod.clicked.connect(self.on_save_lod_btn_click)
        self.load_lod.clicked.connect(self.on_load_lod_btn_click)

        self.replace_lod = self.ui.findChildren(QtWidgets.QLineEdit, "replaceLineEdit")[0]
        self.with_lod = self.ui.findChildren(QtWidgets.QLineEdit, "withLineEdit")[0]
        self.rename_btn = self.ui.findChildren(QtWidgets.QPushButton, "renameBtn")[0]
        self.rename_selection_lod_based = self.ui.findChildren(QtWidgets.QPushButton, "renameSelectionLodBased")[0]
        self.rename_btn.clicked.connect(self.on_rename_lod_btn_click)
        self.rename_selection_lod_based.clicked.connect(self.on_rename_selection_lod_based_click)

        global LOGGER
        LOGGER = self.ui.findChildren(QtWidgets.QTextBrowser, "logger")[0]

        global LOD_NUMBER
        LOD_NUMBER = self.lod_slider.maximum()

    def on_slider_value_changed(self):
        hide_all_lyr()
        show_lod_lyr(self.lod_slider.value(), False)
        self.tri_count_label.setText(str(TRIS_COUNT))
        MaxPlus.ViewportManager.RedrawViewportsNow(MaxPlus.Animation.GetTime())

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


def show_lod_lyr(lod_value, lod_visibility):
    print lod_value
    print lod_visibility
    lyr_root_name = UI.prefix_line.text() + str(lod_value)
    UI.lod_label.setText("Tool is looking for: " + lyr_root_name)
    lyr = rt.LayerManager.getLayerFromName(lyr_root_name)
    if lyr is None:
        log_verbose("MISSING LAYER: " + lyr_root_name)
        return
    lyr_children = [lyr]
    lyr_children = utility.get_layer_children(lyr, lyr_children)
    for child in lyr_children:
        layer = MaxPlus.LayerManager.GetLayer(child.name)
        layer_nodes = layer.GetNodes()
        for n in layer_nodes:
            n.UnhideObjectAndLayer(lod_visibility)
        layer.Hide(lod_visibility)
    global TRIS_COUNT
    TRIS_COUNT = sdk_node.getTrisCount(sdk_layer.getAllNodeInLayerHierarchy(lyr))
    log_clear()


def hide_all_lyr():
    for i in range(LOD_NUMBER + 1):
        show_lod_lyr(i, True)


def set_new_copy_layer(n, curren_prefix, next_prefix):
    previous_name = n.GetName().replace(next_prefix, curren_prefix)
    previous_node = MaxPlus.INode.GetINodeByName(previous_name)
    l = previous_node.GetLayer()
    new_layer_name = l.GetName().replace(curren_prefix, next_prefix)
    new_layer = MaxPlus.LayerManager.GetLayer(new_layer_name)
    new_layer.AddToLayer(n)


def reduce_polygon_amount(n, poly_reduce, reduce_amount):
    if not poly_reduce or reduce_amount == 0:
        return
    node = rt.getNodeByName(n.GetName())
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
        if not selected_layer.GetName().startswith(LOD_PREFIX):
            log_verbose("Select a valid LOD layer")
            return
        # remove LOD prefix and get the index
        current_lod_index = selected_layer.GetName()[len(LOD_PREFIX):][0]
    except:
        log_verbose("Select a valid root LOD layer")
        return

    rt_lyr = rt.LayerManager.getLayerFromName(selected_layer.GetName())
    next_lod_index = int(current_lod_index) + 1
    current_prefix = LOD_PREFIX + str(current_lod_index)
    next_prefix = LOD_PREFIX + str(next_lod_index)

    nextLayerName = rt_lyr.name.replace(current_prefix, next_prefix)
    ex = rt.LayerManager.getLayerFromName(nextLayerName)

    clone_layer_hierarchy(rt_lyr, None, lambda l: utility.replace_layer_prefix(l, current_prefix, next_prefix))

    # all the nodes in layer hierachy that are child of Max Root node
    source_children = sdk_layer.getAllNodeInLayerHierarchy(rt_lyr)
    lyr_root_children = []
    for s in source_children:
        if s.GetParent() not in source_children:
            lyr_root_children.append(s)

    if len(lyr_root_children) <= 0:
        log_verbose("Root node is not under layer hierarchy")

    replace_node_lamba = lambda n: utility.replace_node_prefix(n, current_prefix, next_prefix)
    set_layer_lambda = lambda n: set_new_copy_layer(n, current_prefix, next_prefix)
    reduce_poly_lmbda = lambda n: reduce_polygon_amount(n, poly_reduce, reduce_amount)

    lambda_list = [set_layer_lambda, reduce_poly_lmbda]
    for obj in lyr_root_children:
        utility.clone_hierarchy(obj, obj.GetParent(), replace_node_lamba, lambda_list)


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
        toskin.Convert(MaxPlus.ClassIds.PolyMeshObject)
        MaxPlus.SelectionManager.SelectNode(toskin)
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

    current_time = MaxPlus.Animation.GetTime()
    MaxPlus.ViewportManager.DisableSceneRedraw()
    # serialzie with custom encoder
    with open(path, 'w') as outfile:
        jsonFile = json.dumps([ob for ob in animated_nodes], outfile, cls=sdk_serializable.INodeEncoder, indent=4)
        outfile.write(jsonFile)

    MaxPlus.ViewportManager.EnableSceneRedraw()
    MaxPlus.Animation.SetTime(current_time, True)


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

    current_time = MaxPlus.Animation.GetTime()
    MaxPlus.ViewportManager.DisableSceneRedraw()

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

    MaxPlus.ViewportManager.EnableSceneRedraw()
    MaxPlus.Animation.SetTime(current_time, True)


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
        selection = MaxPlus.SelectionManager.GetNodes()
        for n in selection:
            if n in src_lod_nodes:
                # find the binomial node and copy
                targetName = n.GetName().replace(src_lod_prefix, target_lod_prefix)
                target = MaxPlus.INode.GetINodeByName(targetName)
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
        selection = MaxPlus.SelectionManager.GetNodes()
        for n in selection:
            if n in src_lod_nodes:
                if (n.GetParent().IsRoot):
                    continue
                # find the binomial node and copy
                targetName = n.GetName().replace(src_lod_prefix, target_lod_prefix)
                target = MaxPlus.INode.GetINodeByName(targetName)
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
            target = MaxPlus.INode.GetINodeByName(targetName)
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
    scene_layers = sdk_layer.getAllLayersMP()
    scene_object = scene_layers + scene_node

    regex = "^(?i)x[0-9]_{0}$".format(old_name)
    log_clear()
    matched = []
    for n in scene_object:
        if re.match(regex, n.GetName()):
            matched.append(n)
    if len(matched) == 0:
        log_verbose("No result found")
    else:
        for n in matched:
            prefix = n.GetName()[:3].lower()
            result = prefix + new_name
            log_append("{0} rename into {1}".format(n.GetName(), result))
            n.SetName(result)


def rename_node_based_on_lod0():
    selected = MaxPlus.SelectionManager.GetNodes()
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
    msg_box = QtWidgets.QMessageBox(MaxPlus.GetQMaxMainWindow())
    msg_box.setText(message)
    msg_box.show()


def display_confirm_message(message):
    msg_box = QtWidgets.QMessageBox(MaxPlus.GetQMaxMainWindow())
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
