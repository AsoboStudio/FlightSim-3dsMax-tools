from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import *
import MaxPlus
import qtdriver
import maxsdk.skin as sdkskin

reload(sdkskin)
import maxsdk.node as sdknode

reload(sdknode)
import maxsdk.utility as sdkutility

reload(sdkutility)
import re
import macro

max = MaxPlus.Core.EvalMAXScript
import pymxs
import itertools

rt = pymxs.runtime


class CopyDirection(object):
    LEFT_TO_RIGHT = 0
    RIGHT_TO_LEFT = 1


LOGGER = None


class MainView(QMainWindow):

    def __init__(self):
        super(MainView, self).__init__()
        MaxPlus.AttachQWidgetToMax(self)
        loader = QUiLoader()
        root_ui = loader.load(qtdriver.get_view_path("main_view"))
        root_ui.setContentsMargins(10, 10, 10, 10)
        self.setCentralWidget(root_ui)
        self.setWindowTitle("Animation Tools")

        self.copy_direction = CopyDirection.LEFT_TO_RIGHT

        toggleDirectionBtn = root_ui.findChildren(QPushButton, "toggleMirrorDirection")[0]
        self.toggleLbl = root_ui.findChildren(QLabel, "toggleLabel")[0]
        resetScaleBtn = root_ui.findChildren(QPushButton, "resetScaleBtn")[0]
        mirrorObjectBtn = root_ui.findChildren(QPushButton, "mirrorObjectBtn")[0]
        mirrorSkinBtn = root_ui.findChildren(QPushButton, "mirrorSkinBtn")[0]
        right_suffix_lbl = root_ui.findChildren(QLineEdit, "rightSuffixLbl")[0]
        left_suffix_lbl = root_ui.findChildren(QLineEdit, "leftSuffixLbl")[0]
        self.mirrorAxis = root_ui.findChildren(QComboBox, "mirrorAxis")[0]
        mirrorAnimationBtn = root_ui.findChildren(QPushButton, "mirrorAnimationBtn")[0]
        bakeAnimationBtn = root_ui.findChildren(QPushButton, "bakeAnimationBtn")[0]
        self.chk_includeChildren = root_ui.findChildren(QCheckBox, "chk_includeChildren")[0]
        self.chk_keepExistent = root_ui.findChildren(QCheckBox, "chk_keepExistent")[0]
        self.chk_deleteKeysOnSource = root_ui.findChildren(QCheckBox, "chk_deleteKeysOnSource")[0]
        self.logger_area = root_ui.findChildren(QTextBrowser, "logger")[0]
        self.right_suffix = right_suffix_lbl.text()
        self.left_suffix = left_suffix_lbl.text()

        global LOGGER
        LOGGER = root_ui.findChildren(QTextBrowser, "logger")[0]

        bakeAnimationBtn.clicked.connect(self.on_bake_animation_clicked)
        mirrorSkinBtn.clicked.connect(self.on_mirror_skin_clicked)
        toggleDirectionBtn.clicked.connect(self.on_toogledir_clicked)
        mirrorObjectBtn.clicked.connect(self.on_mirror_hierarchy_without_skin_clicked)
        resetScaleBtn.clicked.connect(self.on_reset_scale_clicked)
        mirrorAnimationBtn.clicked.connect(self.on_mirror_animation_btn_click)
        left_suffix_lbl.textChanged.connect(self.on_left_text_changed)
        right_suffix_lbl.textChanged.connect(self.on_right_text_changed)

    def log_append(self,value):
        text = LOGGER.toPlainText()
        LOGGER.setText(text + value + "\n")

    def log_verbose(self, value):
        LOGGER.setText(value)

    def log_clear(self):
        LOGGER.setText("")

    def on_mirror_animation_btn_click(self):
        self.log_clear()
        try:
            MaxPlus.ViewportManager.DisableSceneRedraw()
            copyDirection = CopyDirection.LEFT_TO_RIGHT if self.copy_direction == CopyDirection.LEFT_TO_RIGHT else CopyDirection.RIGHT_TO_LEFT
            macro.mirrorUnskinned(self.left_suffix, self.right_suffix, copyDirection)
        finally:
            MaxPlus.ViewportManager.EnableSceneRedraw()
            MaxPlus.ViewportManager.ForceCompleteRedraw()

    def on_left_text_changed(self, text):
        self.left_suffix = text

    def on_right_text_changed(self, text):
        self.right_suffix = text

    def on_toogledir_clicked(self):
        if self.copy_direction == CopyDirection.LEFT_TO_RIGHT:
            self.copy_direction = CopyDirection.RIGHT_TO_LEFT
            self.toggleLbl.setText("Right To Left")
            return
        if self.copy_direction == CopyDirection.RIGHT_TO_LEFT:
            self.copy_direction = CopyDirection.LEFT_TO_RIGHT
            self.toggleLbl.setText("Left To Right")
            return

    def on_mirror_skin_clicked(self):
        self.log_clear()
        try:
            MaxPlus.ViewportManager.DisableSceneRedraw()
            selection = MaxPlus.SelectionManager.GetNodes()
            if len(selection) > 0:
                for src in selection:
                    target = self.find_binomial(src)
                    if target:
                        if list(src.Modifiers) is None:
                            return
                        self.log_append("copying {0} to {1}".format(src.GetName(), target.GetName()))
                        if self.copy_direction == CopyDirection.LEFT_TO_RIGHT:
                            macro.mirror_skin(src, target, self.left_suffix, self.right_suffix,
                                              self.mirrorAxis.currentText())
                        if self.copy_direction == CopyDirection.RIGHT_TO_LEFT:
                            macro.mirror_skin(src, target, self.right_suffix, self.left_suffix,
                                              self.mirrorAxis.currentText())

        finally:
            MaxPlus.ViewportManager.EnableSceneRedraw()
            MaxPlus.ViewportManager.ForceCompleteRedraw()

    def find_binomial(self, node):
        if self.copy_direction == CopyDirection.LEFT_TO_RIGHT:
            return macro.find_binomial(node, self.left_suffix, self.right_suffix)
        if self.copy_direction == CopyDirection.RIGHT_TO_LEFT:
            return macro.find_binomial(node, self.right_suffix, self.left_suffix)

    def mirrorNode(self, node, mirrorAxis):
        original_parent = node.GetParent()
        temp_mesh = MaxPlus.Factory.CreateGeomObject(MaxPlus.ClassIds.Sphere)
        temp_parent = MaxPlus.Factory.CreateNode(temp_mesh)
        node.SetParent(temp_parent)

        rtNode = rt.getNodeByName(temp_parent.GetName())
        p = rt.Point3(1, 1, 1)
        if mirrorAxis == "X":
            p = rt.Point3(-1, 1, 1)
        elif mirrorAxis == "Y":
            p = rt.Point3(1, -1, 1)
        elif mirrorAxis == "Z":
            p = rt.Point3(1, 1, -1)
        else:
            print "Error axis do not match"
        rt.scale(rtNode, p)

        node.SetParent(original_parent)
        MaxPlus.INode.Delete(temp_parent)

    def on_mirror_hierarchy_without_skin_clicked(self):
        MaxPlus.Animation.SetTime(0, False)
        self.log_clear()
        MaxPlus.ViewportManager.DisableSceneRedraw()
        try:
            selection = MaxPlus.SelectionManager.GetNodes()
            if len(selection) <= 0:
                self.display_message("Select at least one node")
                return
            root_node_list = self.getRootNodesFromList(selection)
            for root_node in root_node_list:
                target_root = MaxPlus.INode.CreateTreeCopy(root_node)
                sdkutility.ResetXForm(target_root, True, True)
                mirror_axis = self.mirrorAxis.currentText()
                children = list(sdknode.getChildren(target_root))
                self.rename_delete_modifiers(target_root)
                for node in children:
                    self.rename_delete_modifiers(node)

                self.mirrorNode(target_root, mirror_axis)
                sdkutility.ResetXForm(target_root, True, True)
        finally:
            MaxPlus.ViewportManager.EnableSceneRedraw()
            MaxPlus.ViewportManager.ForceCompleteRedraw()

    def ResetScale(self,node, includeChild, scaleOnly):
        if (includeChild == False):
            node.ResetTransform(MaxPlus.Core.GetCurrentTime(),scaleOnly)
        else:
            node.ResetTransform(MaxPlus.Core.GetCurrentTime(),scaleOnly)
            numChildren = node.GetNumChildren()
            nodes = []
            for i in range(0, numChildren):
                nodes.append(node.GetChild(i))
            for n in nodes:
                self.ResetScale(n, includeChild, scaleOnly)

    def on_reset_scale_clicked(self):
        self.log_clear()
        selection = MaxPlus.SelectionManager.GetNodes()
        roots = filter(lambda x : x.GetParent() not in selection, selection)
        for src in roots:
            self.ResetScale(src, True, True)

    def display_message(self, message):
        msg = QMessageBox(MaxPlus.GetQMaxMainWindow())
        msg.setText(message)
        msg.show()

    def rename_delete_modifiers(self, node):
        sdknode.collapseAllModifiers(node)
        if self.copy_direction == CopyDirection.LEFT_TO_RIGHT:
            self.rename_node(node, self.left_suffix, self.right_suffix)
        if self.copy_direction == CopyDirection.RIGHT_TO_LEFT:
            self.rename_node(node, self.right_suffix, self.left_suffix)
        sdkutility.ResetXForm(node, True, True)

    def getRootNodesFromList(self, node_list):
        root_node_list = list()
        for node in node_list:
            if node.GetParent() not in node_list or node.GetParent().GetIsRoot():
                root_node_list.append(node)
        return root_node_list

    def rename_node(self, node, src_suffix, target_suffix):
        regex = r'{0}[a-zA-Z0-9]*'.format(src_suffix)
        target_name = re.sub(regex, target_suffix, node.GetName())
        if target_name != node.GetName():
            self.log_append("{0} renamed to {1}".format(node.GetName(), target_name))
        else:
            self.log_append("cannot rename node: {0}".format(node.GetName()))
        node.SetName(target_name)

    def check_default_condition(self, src_root):
        self.log_clear()
        self.log_append("Mirror src+ " + src_root.GetName())
        target_root = macro.find_binomial(src_root, self.left_suffix, self.right_suffix)
        if not target_root:
            self.log_append("target node on mirrored side not found or does not respect naming convention")
            return False
        if not self.correct_hierachy(src_root, target_root):
            self.log_append("target hierarchy is different from original one")
            return False
        return True

    def correct_hierachy(self, src_root, target_root):
        src_children = map(lambda x: x.GetName(), sdknode.getChildren(src_root))
        src_children.sort()
        target_children = map(lambda x: x.GetName(), sdknode.getChildren(target_root))
        target_children.sort()
        for f, b in itertools.izip(src_children, target_children):
            regex = r'{0}[a-zA-Z0-9]*'.format(self.left_suffix)
            target_name = re.sub(regex, self.right_suffix, f)
            if b != target_name:
                self.log_append("error in : " + b)
                return False
        return True

    def on_bake_animation_clicked(self):
        self.log_clear()
        try:
            MaxPlus.ViewportManager.DisableSceneRedraw()
            selection = MaxPlus.SelectionManager.GetNodes()
            if len(selection) > 0:
                selectionRoots = []
                for node in selection:
                    if (macro.is_top_node(node, selection)):
                        selectionRoots.append(node)
                for node in selectionRoots:
                    includeChildren = self.chk_includeChildren.isChecked()
                    keepExistent = self.chk_keepExistent.isChecked()
                    deleteKeysOnSource = self.chk_deleteKeysOnSource.isChecked()
                    macro.convertToAnimationHelper(node, MaxPlus.Core.GetRootNode(), includeChildren, keepExistent, deleteKeysOnSource)
            else:
                self.log_verbose("Select at least one node")
        finally:
            MaxPlus.ViewportManager.EnableSceneRedraw()
            MaxPlus.ViewportManager.ForceCompleteRedraw()
