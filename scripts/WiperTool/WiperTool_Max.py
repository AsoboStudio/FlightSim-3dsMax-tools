from pymxs import runtime as rt
from pymxs import attime as at
import os

UNITSCALER = 10
WIPERMESH_NAME = "WiperMesh"


class WiperTool_Max(object):
    wiperMesh = rt.undefined

    def __init__(self, theGlass, startFrame, midFrame, endFrame, dummySets, outputpath):
        self.theGlass = rt.getnodebyname(theGlass)
        self.startFrame = startFrame
        self.midFrame = midFrame
        self.endFrame = endFrame
        self.dummySets = dummySets
        self.outputpath = outputpath

    def getUVpos(self, obj, mapChannel, theVertex):
        vertexFaces = rt.polyOp.getFacesUsingVert(obj, rt.Array(*(theVertex)))
        mapVertsArray, mapVertsPosArray = rt.Array()
        for currentFace in vertexFaces:
            print "-----vertexface " + str(currentFace)
            polyFace = rt.polyOp.getFaceVerts(obj, currentFace)
            print "polyFace {0}".format(polyFace)
            mapFace = rt.polyOp.getMapFace(obj, mapChannel, currentFace)
            print "mapFace {0}".format(mapFace)
            mapVertex = mapFace[rt.findItem(polyFace, theVertex)]
            print "mapVertex {0}".format(mapVertex)
            rt.appendIfUnique(mapVertsArray, mapVertex)
            mapVertexPos = rt.polyOp.getMapVert(obj, mapChannel, mapVertex)
            rt.appendIfUnique(mapVertsPosArray, mapVertexPos)
            print "mapVertsArray= {0} ".format(mapVertsArray)
            print "mapVertsPosArray= {0}".format(mapVertsPosArray)

    def getUVPosOfProjectionPoint(self, obj, thePoint):
        theFacesArray = rt.Array()  # --init. an array to collect face selection
        rm = rt.RayMeshGridIntersect()  # --create an instance of the Reference Target
        rm.Initialize(10)  # --init. the voxel grid size to 10x10x10
        rm.addNode(obj)  # --add the sphere to the grid
        rm.buildGrid()  # --build the grid data (collecting faces into the grid voxels)
        uvPoint = rt.undefined

        thePos = thePoint.pos
        dir = rt.point3(0, 0, 1)  # --get the normal of the vertex, reverse direction
        theHitsCount = rm.intersectRay(thePos, -dir, False)  # --intersect the ray with the sphere
        if theHitsCount > 0:  # if have hit anything...
            theIndex = rm.getClosestHit()  # --get the index of the closest hit by the ray
            theFace = rm.getHitFace(theIndex)  # --get the face index corresponding to that indexed hit
            # format "trimesh face index % \n" theFace
            baricCoord = rm.getHitBary(theIndex)
            # format "baricCoord % \n" baricCoord

            triFace = rt.getFace(self.theGlass, theFace)
            p1 = rt.getVert(obj, triFace[0])
            p2 = rt.getVert(obj, triFace[1])
            p3 = rt.getVert(obj, triFace[2])

            f = (baricCoord.x * p1) + (baricCoord.y * p2) + (baricCoord.z * p3)
            # format "f point is  % \n" f
            rt.append(theFacesArray, theFace)  # --add to the face array to select the face...
            # --calculate vectors from point f to vertices p1, p2 and p3:
            f1 = p1 - f
            f2 = p2 - f
            f3 = p3 - f
            # --calculate the areas and factors (order of parameters doesn't matter):
            a = rt.length(rt.cross((p1 - p2), (p1 - p3)))  # -- main triangle area a
            a1 = rt.length(rt.cross(f2, f3)) / a  # -- p1's triangle area / a
            a2 = rt.length(rt.cross(f3, f1)) / a  # -- p2's triangle area / a
            a3 = rt.length(rt.cross(f1, f2)) / a  # -- p3's triangle area / a

            MappingFace = rt.meshop.getMapFace(self.theGlass, 1, theFace)
            uv1 = rt.meshop.getMapVert(obj, 1, MappingFace.x)  # --Returns the coordinates of the specified map vertex as a <point3> .
            # format " x: % y:% \n" uv1.x uv1.y
            uv2 = rt.meshop.getMapVert(obj, 1, MappingFace.y)
            # format " x: % y: % \n" uv2.x uv2.y
            uv3 = rt.meshop.getMapVert(obj, 1, MappingFace.z)
            # format " x: % y: % \n" uv3.x uv3.y
            # --find the uv corresponding to point f (uv1/uv2/uv3 are associated to p1/p2/p3):
            fUV = uv1 * a1 + uv2 * a2 + uv3 * a3
            uvPoint = rt.point2(fUV.x, fUV.y)
        # format "projectedUV point x: % y: % \n" uvPoint.x uvPoint.y

        rm.free()
        return uvPoint

    def convertUVToTexSpace(self, thePoint, texWidth, texHeight):  # = --thePoint:point2 texWidht:int texHeight:int

        tX = thePoint.x * texWidth
        tY = texHeight - (thePoint.y * texHeight)
        texturePoint = rt.point2(tX, tY)
        return texturePoint

    def bakeDiffuse(self, obj, size):
        # --Clear all render elements
        obj.iNodeBakeProperties.removeAllBakeElements()
        # --Preparing the Bake Elements:
        be1 = rt.diffusemap()  # --instance of the bake element class
        be1.outputSzX = be1.outputSzY = size  # --set the size of the baked map --specifythe full file path, name and type:
        be1.fileType = self.outputpath
        be1.fileName = rt.filenameFromPath(be1.fileType)
        be1.filterOn = True  # --enable filtering
        be1.shadowsOn = False  # --disable shadows
        be1.lightingOn = False  # --disable lighting
        be1.enabled = True  # --enable baking
        obj.INodeBakeProperties.addBakeElement(be1)  # --add first element
        obj.INodeBakeProperties.bakeEnabled = True  # --enabling baking
        obj.INodeBakeProperties.bakeChannel = 1  # --channel to bake
        obj.INodeBakeProperties.nDilations = 1  # --expand the texturea bit
        rt.select(obj)  # --we are baking the selection, so we select the object --Call the rendererto bake both elements:
        rt.render(rendertype=rt.Name("bakeSelected"), vfb=False, progressBar=True, outputSize=rt.Point2(size, size))
        print("baked image in {0}".format(be1.fileType))

    def bakeVertexColor(self, theMesh):
        rt.execute("max modify mode")
        rt.select(theMesh)
        rt.addModifier(theMesh, rt.Uvwmap())
        theMesh.modifiers[rt.Name("UVW_Map")].length = UNITSCALER
        theMesh.modifiers[rt.Name("UVW_Map")].width = UNITSCALER
        theMesh.modifiers[rt.Name("UVW_Map")].mapChannel = 1
        theMesh.modifiers[rt.Name("UVW_Map")].axis = 2
        uvwgizmo = theMesh.modifiers[rt.Name("UVW_Map")].gizmo
        uvwgizmo.position = rt.point3((UNITSCALER / 2), (UNITSCALER / 2), 0)
        theMesh.material = rt.standard(diffuseMap=rt.Vertex_Color(), showInViewport=False, name="WiperMat")
        self.bakeDiffuse(theMesh, 512)

    def buildWiperMesh(self, theGlass, theDummy1, theDummy2):
        rt.convertToMesh(theGlass)

        projectMeshVertices = rt.Array()
        projectMeshFaces = rt.Array()
        projectMeshVColors = rt.Array()
        vert_count = 0
        # print "------------------------------------------------------------------"
        animLenght = self.midFrame - self.startFrame
        for i in range(self.startFrame, self.midFrame):
            with at(i):
                uvPoint1 = self.getUVPosOfProjectionPoint(theGlass, theDummy1)
                uvPoint2 = self.getUVPosOfProjectionPoint(theGlass, theDummy2)
                if uvPoint1 == rt.undefined or uvPoint2 == rt.undefined:
                    continue
                rt.append(projectMeshVertices, rt.point3(uvPoint1.x, uvPoint1.y, 0) * UNITSCALER)
                rt.append(projectMeshVertices, rt.point3(uvPoint2.x, uvPoint2.y, 0) * UNITSCALER)

        vColors = rt.Array()
        for i in range(self.startFrame, self.endFrame):
            with at(i):
                if i > self.midFrame:
                    vValue = (1 - (float(rt.currentTime - animLenght) / animLenght)) * 255
                    index = i - animLenght
                    vColors[index] = rt.point3(vColors[index].x, vValue, 0)
                else:
                    vValue = (float(rt.currentTime) / animLenght) * 255
                    vColor = rt.point3(vValue, 0, 0)
                    rt.append(vColors, vColor)

        for i in range(self.startFrame, self.midFrame):
            rt.append(projectMeshVColors, vColors[i])
            rt.append(projectMeshVColors, vColors[i])

        for j in range(1, (projectMeshVertices.count - 2)):
            rt.append(projectMeshFaces, rt.Point3(vert_count + 1, vert_count + 3, vert_count + 2))
            vert_count += 1

        projectionMesh = rt.mesh(vertices=projectMeshVertices, faces=projectMeshFaces)

        rt.defaultVCFaces(projectionMesh)

        for i in range(1, projectMeshVertices.count):
            rt.setVertColor(projectionMesh, i, projectMeshVColors[i])
        return projectionMesh

    def run(self):
        if not self.outputpath:
            print "Error missing output path"

        for dummySet in self.dummySets:
            theDummy1 = rt.getnodebyname(dummySet[0])
            theDummy2 = rt.getnodebyname(dummySet[1])
            if theDummy1 and theDummy2:
                wMesh = self.buildWiperMesh(self.theGlass, theDummy1, theDummy2)
                if self.wiperMesh == rt.undefined:
                    self.wiperMesh = wMesh
                else:
                    rt.attach(self.wiperMesh, wMesh)
            else:
                print "Error: with wiper points names"

        if self.wiperMesh:
            self.wiperMesh.name = WIPERMESH_NAME
            self.bakeVertexColor(self.wiperMesh)
            rt.maxOps.CollapseNode(self.wiperMesh, False)
            rt.delete(self.wiperMesh)

##uncomment this t test without ui
# dummySets = [["Point001","Point002"]]
# output = "C:\Users\lpierabella\Desktop\SANDBOX\wiperfx.png"
# tool = WiperTool_Max(theGlass="FUSELAGE_COCKPITWINDOW", startFrame=0, midFrame=100,endFrame=200,dummySets=dummySets,outputpath=output )
# tool.run()