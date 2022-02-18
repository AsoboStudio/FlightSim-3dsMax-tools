import os
import unittest
from maxsdk import sceneUtils, userprop, perforce
from pymxs import runtime as rt
from MultiExporter import multiExporter, constants, exporter, optionsMenu

from datetime import datetime

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

class A_ExporterTest(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        rt.resetMaxFile(rt.Name("noprompt"))
        self.rootA = rt.Box()        
        self.boxA = rt.Box()
        self.boxA.parent = self.rootA
        self.gizmoA = rt.AsoboBoxGizmo()
        self.gizmoA.parent = self.rootA

        self.rootB = rt.Box()        
        self.boxb = rt.Box()
        self.boxb.parent = self.rootB
        self.gizmoB = rt.AsoboBoxGizmo()
        self.gizmoB.parent = self.rootB

        self.rootLOD0 = rt.Box()
        self.rootLOD0.name = "test_LOD0"
        self.rootLOD1 = rt.Box()
        self.rootLOD1.name = "test_LOD1"
        self.rootLOD2 = rt.Box()
        self.rootLOD2.name = "test_LOD2"
        self.rootLOD3 = rt.Box()
        self.rootLOD3.name = "test_LOD3"

        self.exportPath = os.path.join(rt.pathConfig.getCurrentProjectFolder(),"Tools\\3DSMAX\\FlightSimPackage\\src\\samples\\Export\\")
        multiExporter.run(prompt=False, skip_conversion=True)
    
    def test_a_add_export(self):
        allRoots = sceneUtils.getAllRoots(sceneUtils.getAllObjects())
        exporter.addExportPathToObjects(allRoots, forcedPath=self.exportPath, prompt=False)

    def test_b_remove_export(self):
        allRoots = sceneUtils.getAllRoots(sceneUtils.getAllObjects())
        exporter.removeExportPathToObjects(allRoots,prompt=False)

    def test_c_add_export_from_ui(self):
        multiExporter.multiExporter.treeLODs.selectAll()        
        self.assertEqual(len(multiExporter.multiExporter.treeLODs.getSelectedRootList()), 6)
        multiExporter.multiExporter._clickedAddExport(forcedPath=self.exportPath, prompt=False)

    def test_d_change_values(self):
        multiExporter.multiExporter.treeLODs.selectAll()
        multiExporter.multiExporter.lodValue.setText("60")
        multiExporter.multiExporter.flattenComboBox.setCurrentIndex(1)
        multiExporter.multiExporter.cbKeepInstances.setChecked(True)
        multiExporter.multiExporter._clickedSetLODValues()

    def test_e_generate_xml(self):
        multiExporter.multiExporter.tabWidget.setCurrentIndex(0)
        multiExporter.multiExporter.treeLODs.selectAll()        
        multiExporter.multiExporter._clickedGenerateXML(prompt=False)
        
    def test_f_export_objects(self):
        multiExporter.multiExporter.tabWidget.setCurrentIndex(0)
        multiExporter.multiExporter.treeLODs.selectAll()
        multiExporter.multiExporter._clickedExportAll(prompt=False)

    def test_h_remove_export_from_ui(self):
        multiExporter.multiExporter.refreshTool()
        multiExporter.multiExporter.treeLODs.selectAll()
        multiExporter.multiExporter._clickedRemoveExport(prompt=False)

    def test_i_conform_layers(self):
        multiExporter.multiExporter._clickedConformLayers(prompt=False)

    def test_j_create_presets(self):
        multiExporter.multiExporter.tabWidget.setCurrentIndex(1)
        multiExporter.multiExporter._clickedAddPreset(forcedPath= os.path.join(self.exportPath,"presetTest.gltf"))
        multiExporter.multiExporter.treePresets.selectAll()
        for i in range(multiExporter.multiExporter.treeLayer.topLevelItemCount()):
            item = multiExporter.multiExporter.treeLayer.topLevelItem(i)
            item.setCheckState(0, Qt.Checked)
        multiExporter.multiExporter._clickedApplyLayerSelection()
        multiExporter.multiExporter._clickedDuplicatePreset()
        multiExporter.multiExporter._clickedExportAll()

    def test_k_option_menu(self):
        multiExporter.multiExporter._openOptionsMenu()
        multiExporter.multiExporter.optionsMenuWindow._clickedAddOptionPreset()
        multiExporter.multiExporter.optionsMenuWindow.cbExportMaterial.setChecked(False)
        multiExporter.multiExporter.optionsMenuWindow.saveSettings()
        multiExporter.multiExporter.optionsMenuWindow.close()
        multiExporter.multiExporter._closeOptionsMenu()
    
    def test_l_group_and_option_presets(self):
        multiExporter.multiExporter.tabWidget.setCurrentIndex(1)
        multiExporter.multiExporter.treePresets.selectAll()
        multiExporter.multiExporter._clickedAddPresetGroup()
        multiExporter.multiExporter.treePresets.selectAll()
        multiExporter.multiExporter.cbOptionPreset.setCurrentIndex(1)
        multiExporter.multiExporter.btnApplyPresetEdit.pressed.emit()
        multiExporter.multiExporter._clickedExportAll()

    def test_m_delete_presets(self):
        multiExporter.multiExporter.treePresets.selectAll()
        multiExporter.multiExporter._clickedRemovePreset(prompt=False)    


    @classmethod
    def tearDownClass(self):
        print("finished")
        multiExporter.multiExporter.close()

class B_PlaneExportTest(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        rt.resetMaxFile(rt.Name("noprompt"))
        projectPath = rt.pathConfig.getCurrentProjectFolder()
        self.path = os.path.join(projectPath, "Tools\\3DSMAX\\FlightSimPackage\\src\\samples\\CESSNA_152_FOR_TESTING.max")
        perforce.P4edit(self.path)
        rt.loadMaxFile(self.path, quiet=True)
        multiExporter.run(prompt=False, skip_conversion=True)
        
    def test_a_export_all(self):
        multiExporter.multiExporter.tabWidget.setCurrentIndex(1)
        multiExporter.multiExporter._clickedExportAll(prompt=False)

    @classmethod
    def tearDownClass(self):
        perforce.P4revert(self.path)
        multiExporter.multiExporter.close()

        
class C_EnvironmentExportTest(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        rt.resetMaxFile(rt.Name("noprompt"))
        projectPath = rt.pathConfig.getCurrentProjectFolder()
        self.path = os.path.join(projectPath, "Tools\\3DSMAX\\FlightSimPackage\\src\\samples\\Paris_Charles_De_Gaulle_FOR_TESTING.max")
        perforce.P4edit(self.path)
        rt.loadMaxFile(self.path, quiet=True)
        multiExporter.run(prompt=False, skip_conversion=True)

    def test_a_generate_xml(self):
        multiExporter.multiExporter._clickedGenerateXML(prompt=False)
        
    def test_b_export_all(self):
        multiExporter.multiExporter._clickedExportAll(prompt=False)
        
    @classmethod
    def tearDownClass(self):
        perforce.P4revert(self.path)
        multiExporter.multiExporter.close()

        
class D_CharacterExportTest(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        rt.resetMaxFile(rt.Name("noprompt"))
        projectPath = rt.pathConfig.getCurrentProjectFolder()
        self.path = os.path.join(projectPath, "Tools\\3DSMAX\\FlightSimPackage\\src\\samples\\Master_Bear_Adult_FOR_TESTING.max")
        perforce.P4edit(self.path)
        rt.loadMaxFile(self.path, quiet=True)
        multiExporter.run(prompt=False, skip_conversion=True)
      
    def test_a_export_all(self):
        multiExporter.multiExporter.tabWidget.setCurrentIndex(1)
        multiExporter.multiExporter._clickedExportAll(prompt=False)

    @classmethod
    def tearDownClass(self):
        perforce.P4revert(self.path)
        multiExporter.multiExporter.close()

def cleanup_temp_export_folder():
    dirPath = os.path.join(rt.pathConfig.getCurrentProjectFolder(),"Tools\\3DSMAX\\FlightSimPackage\\src\\samples\\Export\\")
    for fileName in os.listdir(dirPath):
        perforce.P4revert(os.path.join(dirPath,fileName))

if __name__ == "__main__":
    utest = unittest.main(exit=False)
    rt.setListenerSel([0,-1])
    text = rt.getListenerSelText()
    direct = os.path.dirname(__file__)
    direct = os.path.join(direct, "..\\..\\log\\")
    date=str(datetime.utcnow()).split(".")[0].replace(":","-").replace(" ","_").replace(".","-")
    filePath = os.path.join(direct,"PackageTestingProcedure_{0}.txt".format(date))
    with open(filePath, "w+") as output:
        output.flush()
        output.write(text)
        os.startfile(filePath)

    fails = utest.result.failures
    errors = utest.result.errors

    exitCode = 0  

    if (len(fails) > 0 or len(errors) > 0):
        exitCode = 1

    cleanup_temp_export_folder()

    rt.quitMax()