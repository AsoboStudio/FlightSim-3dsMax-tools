from pymxs import runtime as rt
from pymxs import attime as at
import os

WIPERMESH_NAME = "WiperMesh"


class WiperTool_Max(object):
    wiperMesh = rt.undefined

    def __init__(self, theGlass, animInStart, animInEnd, animOutStart,animOutEnd, dummySets, outputpath):
        self.theGlass = rt.getnodebyname(theGlass)
        self.theGlass.layer.current = True
        self.animInStartFrame = animInStart
        self.animInEndFrame = animInEnd
        self.animOutStartFrame = animOutStart
        self.animOutEndFrame = animOutEnd
        self.dummySets = dummySets
        if rt.DEBUG_MODE:
            print(self.animInStartFrame)
            print(self.animInEndFrame)
            print(self.animOutStartFrame)
            print(self.animOutEndFrame)
            print(self.dummySets)
        self.outputpath = outputpath
      
    
    def projectVertexColor(self, nodeToBake, nodeToProject, outputPath, padding):
        """
        Project the vertex color of a given node to a given surface and bake the result in the given path 

        Parameters
        ----------
            nodeToBake : INode
                the node used to bake the texture
            nodeToProject : INode
                the node used to project the vertex color
            outputPath : str
                the path of the baked texture
        """
        rt.disableSceneRedraw()
        rt.select(nodeToBake)
        snap = rt.snapshot(nodeToBake, name=nodeToBake.name + "_new")
        snap.material  =  rt.standard(showInViewport=False, name="GlassMat")
        nodeToProject.material = rt.standard(diffuseMap=rt.Vertex_Color(), showInViewport=False, name="WiperMat")
        # --Clear all render elements
        snap.iNodeBakeProperties .removeAllBakeElements()
        # --Preparing the Bake Elements:
        be1 = rt.diffusemap()  # --instance of the bake element class
        be1.outputSzX = be1.outputSzY = 1024  # --set the size of the baked map --specifythe full file path, name and type:
        be1.fileType = outputPath
        be1.fileName = rt.filenameFromPath(be1.fileType)
        be1.filterOn = True  # --enable filtering
        be1.shadowsOn = False  # --disable shadows
        be1.lightingOn = False  # --disable lighting
        be1.enabled = True  # --enable baking
        snap.iNodeBakeProperties.nDilations = padding  # --expand the texturea bit
        snap.iNodeBakeProperties.addBakeElement(be1)  # --add first element
        snap.iNodeBakeProperties.bakeEnabled = True  # --enabling baking
        snap.iNodeBakeProperties.bakeChannel = 2  # --channel to bake   
        snap.INodeBakeProjProperties.bakeEnabled = True  # --enabling baking
        snap.INodeBakeProjProperties.bakeChannel = 2  # --channel to bake       
        snap.INodeBakeProjProperties.subObjBakeChannel =2 
        snap.INodeBakeProjProperties.enabled = True  #enable projection baking

        # add a projection modifier and set it as the projection source
        projection =rt.Projection()
        rt.addModifier(snap, projection)
        projection.addObjectNode(nodeToProject)
        projection.resetCage()        
        snap.INodeBakeProjProperties.projectionMod  = projection
        snap.INodeBakeProjProperties.rayMissColor = rt.Point3(0, 0, 0)
        
        #select the object enter modify mode, offset the cage and bake the texture at the given path

        rt.select(snap)  # --we are baking the selection, so we select the object --Call the rendererto bake both elements:
        rt.execute("max modify mode")
        projection.pushCage(0.1)
        rt.render(rendertype=rt.Name("bakeSelected"), vfb=False, progressBar=True, outputSize=rt.Point2(1024, 1024))
        print("baked image in {0}".format(be1.fileType))
        rt.delete(snap)
        rt.enableSceneRedraw()
        rt.CompleteRedraw()
    
    def saturate(self, x):
        return max(0, min(1, x))

    def remap(self, original_value, original_min, original_max, new_min, new_max):
        return new_min + (new_max - new_min) * self.saturate(float(float(original_value - original_min) / float(original_max - original_min)))
    
    def lerp(self,v0,v1,t): 
        return (1 - t) * v0 + t * v1;

    def setColorByFrame(self, frame, vColor):
        """
        Set the color at the given frame for the given vector

        Parameters
        ----------
            nodeToBake : int
                the frame used to calcualte the color
            nodeToProject : Point3
                the vertex Color value set for the given frame
        """
        if frame <= self.animInEndFrame:         
            colorValue = self.remap(frame, self.animInStartFrame, self.animInEndFrame, 0, 255)
            vColor.x = colorValue
        else:
            colorValue = self.remap(frame, self.animOutStartFrame,self.animOutEndFrame, 0, 255)
            vColor.y = colorValue
        vColor.z = 255



    def buildWiperMesh(self, p1, p2):
        """
        Build the wiper mesh 

        Parameters
        ----------
            p1 : Point3
                the world position of the first dummy placed on the exterior part of the wiper
            p2 : Point3
                the world position of the second dummy placed on the exterior part of the wiper
        """

        
        animationLength = self.animInEndFrame - self.animInStartFrame +1
        projectMeshVertices = []
        projectMeshFaces = []
        
        vColors = [rt.Point3(0,0,0) for i in range(animationLength*2)]
        
        vert_count = 0

        if rt.DEBUG_MODE:
            print("------------------------------------------------------------------")
        
        #fill projectMeshVertices with the exterior points of the wiper for each frame
        f = self.animInStartFrame
        while f <= self.animInEndFrame:
            with at(f):
                projectMeshVertices.append(p1.transform.position)
                projectMeshVertices.append(p2.transform.position)
                f += 1

        # fill the vertexColors array during animation IN
        vIndex = 0
        f = self.animInStartFrame
        while f <= self.animInEndFrame:
            with at(f):
                self.setColorByFrame(f, vColors[vIndex])
                self.setColorByFrame(f, vColors[vIndex + 1])
                f += 1
                vIndex += 2

        # fill the vertexColors array during animation OUT
        vIndex = 0
        f = self.animOutEndFrame
        while f >= self.animOutStartFrame:
            with at(f):
                self.setColorByFrame(f, vColors[vIndex])
                self.setColorByFrame(f, vColors[vIndex + 1])
                f -= 1
                vIndex += 2


        axis = rt.Point3(1,0,0)
        result = rt.dot(p2.transform.position, axis)
        
        
        for i in range(1, len(projectMeshVertices) - 1):
            #build the triangle with the righ orientation
            if i % 2 != 0:
                    projectMeshFaces.append(rt.Point3(vert_count + 3, vert_count + 2, vert_count + 1))
            else:
                projectMeshFaces.append(rt.Point3(vert_count + 2, vert_count + 3, vert_count + 1))
                    
            vert_count += 1        

        #build the mesh with an array of vertex and triangles
        projectionMesh = rt.mesh(vertices=rt.Array(*(projectMeshVertices)), faces=rt.Array(*(projectMeshFaces)))
        rt.defaultVCFaces(projectionMesh)

        #set the vertex color for each vertex
        for i in range(len(projectMeshVertices)):
            rt.setVertColor(projectionMesh, i+1, vColors[i])       

        if result > 0:
            rt.select( projectionMesh)
            rt.execute("max modify mode")            
            normalModifier = rt.NormalModifier()
            rt.addModifier(projectionMesh, rt.NormalModifier())
            normal =rt.Name("Normal")
            projectionMesh.modifiers[normal].flip = True
        
        rt.maxOps.CollapseNode(projectionMesh, False)


        #quadrify
        rt.select( projectionMesh)
        rt.convertToPoly(projectionMesh)
        rt.execute("max modify mode")
        rt.PolyToolsModeling.Quadrify(True, False)
        edge = rt.Name("EDGE")
        edgeNumber = projectionMesh.EditablePoly.getNumEdges()
        edgeList = [1] if result < 0 else [2]    
        edgeSelection = rt.BitArray(*(edgeList))
        rt.subObjectLevel = 2        
        projectionMesh.EditablePoly.SetSelection(edge, edgeSelection)
        projectionMesh.EditablePoly.SelectEdgeRing ()
        projectionMesh.connectEdgeSegments = 3
        rt.execute('macros.run "Ribbon - Modeling" "ConnectEdges"')

        return projectionMesh

    def run(self):
        if not self.outputpath:
            print("Error missing output path")


        # build a mesh based on the trajectory drawed by the wipers
        for dummySet in self.dummySets:
            point1 = rt.getnodebyname(dummySet[0])
            point2 = rt.getnodebyname(dummySet[1])
            if point1 and point2:               
                wMesh = self.buildWiperMesh(point1, point2)
                if self.wiperMesh == rt.undefined:
                    self.wiperMesh = wMesh
                else:
                    rt.polyop.attach(self.wiperMesh, wMesh)
            else:
                print("Error: with wiper points names")

        

        # bake the previously built mesh vertex color data into the secondary uv set of the glass
        if self.wiperMesh:
            rt.convertToMesh(self.theGlass)
            self.wiperMesh.name = WIPERMESH_NAME
            dirName = os.path.dirname(self.outputpath)
            basename = os.path.basename(self.outputpath)
            info = os.path.splitext(basename)
            textureName = info[0]
            noPaddingTexPath = os.path.join(dirName,textureName + "_noPadding_RG" + info[1])
            paddingTextPath = os.path.join(dirName,textureName + "_padding_B" + info[1])
            self.projectVertexColor(self.theGlass, self.wiperMesh, paddingTextPath, 64)
            self.projectVertexColor(self.theGlass, self.wiperMesh, noPaddingTexPath, 0)
            rt.maxOps.CollapseNode(self.wiperMesh, False)
            rt.delete(self.wiperMesh)








# uncomment this to test without ui
# dummySets = [
#     ["A320:Wiper_PointA_r", "A320:Wiper_PointB_r"],
#     ["A320:Wiper_PointA_l", "A320:Wiper_PointB_l"]
#     ]
# rt.DEBUG_MODE=True
# output = r"E:\KH_QA_Release\ASSETS\KittyHawk_Data\Content\fs\SimObjects\Airplanes\Asobo_A320_NEO\Texture\WiperMask.tga"
# tool = WiperTool_Max(theGlass="x0_WINDSHIELD", animInStart=1, animInEnd=10,animOutStart=11, animOutEnd=20,dummySets=dummySets,outputpath=output )
# tool.run()
