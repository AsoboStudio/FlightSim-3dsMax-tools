from pymxs import runtime as rt
import os

from PySide2.QtWidgets import *
from PySide2.QtCore import *
from maxsdk import userprop
import BabylonPYMXS

reload(userprop)
from maxsdk import node as sdknode
from maxsdk import perforce as sdkperforce


def flattenMesh(rootNode):
    hierarchy = list(sdknode.getChildren(rootNode))
    hierarchy.append(rootNode)
    objsToFlatten = rt.Array()
    toKeep = rt.Array()
    for node in hierarchy:
        cls = rt.classOf(node)
        if cls == rt.Editable_Poly or cls == rt.Editable_Mesh or cls == rt.PolyMeshObject:
            rt.append(objsToFlatten, node)
        else:
            rt.append(toKeep, node)

    flattened = rt.createMesh(objsToFlatten, name=rootNode.name, transform=rootNode.transform)
    for node in toKeep:
        snapNode = rt.snapshot(node)
        snapNode.parent = flattened
        sdknode.name = node.name

    flattened.name = rootNode.name
    return flattened


class QExportProgress(QDialog):
    def __init__(self, steps, parent=None):
        super(QExportProgress, self).__init__(parent, Qt.Window)
        self.steps = steps
        self.setWindowTitle("Export Progress")
        self.progressInfo = QLabel()
        self.progressbar = QProgressBar()
        layout0 = QVBoxLayout()
        self.progressbar.setGeometry(200, 80, 250, 20)
        layout0.addWidget(self.progressbar)
        layout0.addWidget(self.progressInfo)
        self.setLayout(layout0)

    def increaseProgress(self):
        stepValue = 100 / self.steps
        currentValue = self.progressbar.value()
        if currentValue == -1:
            currentValue = 0
        self.progressbar.setValue(currentValue + stepValue)
        if currentValue >= 101:
            self.close()

    def setExportInfo(self, info):
        returnLine = "\n\n"
        currentText = self.progressInfo.text()
        self.progressInfo.setText(currentText + info + returnLine)


def getGizmoChild(root):
    gizmo = rt.Array()
    for o in root.children:
        cClass = str(rt.classOf(o))
        if cClass == "BoxGizmo" or cClass == "SphereGizmo" or cClass == "CylGizmo" or cClass == "LodSphere" or cClass == "FadesSphere" or cClass == "SphereFade" or cClass == "CylinderCollider" or cClass == "SphereCollider" or cClass == "BoxCollider":
            rt.append(gizmo, o)
    return gizmo


def executeMAxScriptDependencies():
    flattenFile = os.path.join(os.path.dirname(__file__), "flatten.ms")
    flattenFunction = open(flattenFile, "r").read()
    rt.execute(flattenFunction)

def convertToBoxCollider(gizmo):
    newGizmo = rt.AsoboBoxGizmo()
    newGizmo.parent = gizmo.parent
    newGizmo.transform = gizmo.transform
    newGizmo.boxGizmo.width = gizmo.width
    newGizmo.boxGizmo.height = gizmo.height
    newGizmo.boxGizmo.length = gizmo.length
    newGizmo.name = gizmo.name
    gizmo.layer.addnode(newGizmo)
    rt.delete(gizmo)
    print newGizmo.boxGizmo.height
    if newGizmo.boxGizmo.height <= 0:
        newGizmo.boxgizmo.height *= -1
        newGizmo.boxgizmo.width *= -1
        newGizmo.boxgizmo.length *= -1
        rt.toolMode.coordsys(rt.Name("local"))
        rt.rotate(newGizmo, (rt.EulerAngles(180, 0, 0)))


def convertToSphereCollider(gizmo):
    newGizmo = rt.AsoboSphereGizmo()
    newGizmo.parent = gizmo.parent
    newGizmo.transform = gizmo.transform
    newGizmo.sphereGizmo.radius = gizmo.radius
    newGizmo.name = gizmo.name
    gizmo.layer.addnode(newGizmo)
    rt.delete(gizmo)
    if newGizmo.sphereGizmo.radius <= 0:
        newGizmo.sphereGizmo.radius *= -1


def convertToCylinderCollider(gizmo):
    newGizmo = rt.AsoboCylinderGizmo()
    newGizmo.parent = gizmo.parent
    newGizmo.transform = gizmo.transform
    newGizmo.cylGizmo.radius = gizmo.radius
    newGizmo.cylGizmo.height = gizmo.height
    newGizmo.name = gizmo.name
    gizmo.layer.addnode(newGizmo)
    rt.delete(gizmo)
    if newGizmo.cylGizmo.height <= 0:
        newGizmo.cylGizmo.height *= -1
        newGizmo.cylGizmo.radius *= -1
        rt.toolMode.coordsys(rt.Name("local"))
        rt.rotate(newGizmo, (rt.EulerAngles(180, 0, 0)))



def ExportEnvAsset(exportPath, maxNode, exportProgress, flatten=True):

    rt.clearSelection()
    toExport = rt.snapshot(maxNode)
    gizmos = getGizmoChild(toExport)
    for g in gizmos:
        if str(rt.classOf(g)) == "AsoboBoxGizmo":
            convertToBoxCollider(g)
        elif str(rt.classOf(g)) == "AsoboCylinderGizmo":
            convertToCylinderCollider(g)
        elif str(rt.classOf(g)) == "AsoboSphereGizmo":
            convertToSphereCollider(g)

    if maxNode.children and flatten:
        toExport = flattenMesh(maxNode)

    rt.select(toExport)
    toExport.transform = rt.matrix3(1)
    for o in toExport.children:
        rt.selectMore(o)
    assetFilePath = os.path.join(exportPath, maxNode.name)
    param = BabylonPYMXS.BabylonParameters(assetFilePath, "gltf")
    param.exportOnlySelected = True
    param.exportMaterials = True
    BabylonPYMXS.runBabylonExporter(param)
    sdkperforce.P4edit(assetFilePath + ".bin")
    sdkperforce.P4edit(assetFilePath + ".gltf")

    if maxNode.children:
        hierarchy = list(sdknode.getChildren(toExport))
        hierarchy.append(toExport)
        for h in hierarchy:
            rt.delete(h)

    exportProgress.increaseProgress()
    exportProgress.setExportInfo("exported {0}    in    {1}".format(maxNode.name, assetFilePath))

# Execute a maxscript dependency to run createMesh() in flattenMesh()
executeMAxScriptDependencies()