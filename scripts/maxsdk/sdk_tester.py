import unittest
import sceneUtils 
import userprop
from pymxs import runtime as rt
from ..MultiExporter import multiExporter, constants

class HierarchyTest(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        rt.resetMaxFile(rt.Name("noprompt"))
        tp = rt.Box()
        tp.name = "topParent"
        fc = rt.Box()
        fc.name = "firstChild"
        fc.parent = tp
        for i in range(10):
            fsc = rt.Box()
            fsc.name = "childNum{0}".format(i)
            fsc.parent = fc
        print("setup Hierarchy")

    def test_gathering_function(self):
        print("testing stuff")
        allRoots = sceneUtils.getAllObjects()
        allScene = sceneUtils.getDescendantsOfMultiple(allRoots)
        roots = sceneUtils.getAllRoots(allScene)
        self.assertEqual(roots[0].name, "topParent", "not equal")
        reGetAll = sceneUtils.getDescendantsOfMultiple(roots)
        self.assertEqual(allScene, reGetAll, "not equal")
        print(type(allRoots[0]))

    def test_delete_function(self):
        print("deleting stuff")
        self.assertEqual(1, 1, "is equal")
        
    @classmethod
    def tearDownClass(self):
        print("finished lol")

class LODTest(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        rt.resetMaxFile(rt.Name("noprompt"))
        self.A = rt.Box()
        self.A.name = "x0_levelofdetailzero"

        self.B = rt.Box()
        self.B.name = "x12_testingSoul"

        self.C = rt.Box()
        self.C.name = "testingSoul_LOD1"

        self.D = rt.Box()
        self.D.name = "testing_LOD23_Soul_LOD234"

        self.GA = rt.BoxGizmo()
        self.GA.name = "Collider_A"
        self.GA.parent = self.D

        self.GB = rt.BoxGizmo()
        self.GB.name = "Collider_B"
        self.GB.parent = self.D

        self.GC = rt.BoxGizmo()
        self.GC.name = "Collider_C"
        self.GC.parent = self.GB
        
        self.E = rt.Box()
        self.E.parent = self.GC

        self.F = rt.Box()
        self.F.parent = self.GB

        self.G = rt.Box()
        self.G.parent = self.GC

        self.H = rt.Box()
        self.H.parent = self.GA


        print("setup LOD")

    def test_gathering_function(self):
        self.assertEqual(sceneUtils.getLODLevel(self.A),0, "lol")
        self.assertEqual(sceneUtils.getLODLevel(self.B),12, "lol")
        self.assertEqual(sceneUtils.getLODLevel(self.C),1, "lol")
        self.assertEqual(sceneUtils.getLODLevel(self.D),234, "lol")

        gizmos = sceneUtils.getGizmosInDescendants(self.D)
        self.assertEqual(len(gizmos), 3)

    def test_lod_value_set_function(self):
        userprop.setUserProp(self.A, constants.PROP_LOD_VALUE, 100)
        lodValue1 = sceneUtils.getLODValue(self.A)
        lodValue2 =  userprop.getUserProp(self.A, constants.PROP_LOD_VALUE)
        self.assertEqual(lodValue1,lodValue2)
        self.assertEqual(lodValue1, 100.0)
        self.assertEqual(lodValue2, 100.0)

    def test_delete_function(self):
        pass
        
    @classmethod
    def tearDownClass(self):
        print("finished lol")

if __name__ == "__main__":
    unittest.main(exit=False)