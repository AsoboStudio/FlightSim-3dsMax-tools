from pymxs import runtime as rt
import FlightSimMaterial
import os
import sys

IBLFOLDER = os.path.join(os.path.dirname(FlightSimMaterial.__file__), "IBLmap")


def SetIBLmaps(radianceMap, irradianceMap):
    multimats = filter(lambda m: rt.classOf(m) == rt.MultiMaterial, rt.sceneMaterials)
    flightSimMats = filter(lambda m: rt.ClassOf(m) == rt.FlightSim, rt.sceneMaterials)
    for multi in multimats:
        for m in multi.materialList:
            if rt.ClassOf(m) == rt.FlightSim:
                flightSimMats.append(m)
    for mat in flightSimMats:
        mat.loadShader()
        mat.radianceMap = radianceMap
        mat.irradianceMap = irradianceMap
        # make use switching from legacy to PBR viewport set the right Tech



def UseStudioIBL():
    radianceMap = os.path.join(IBLFOLDER, "Studio_Radiance.dds")
    irradianceMap = os.path.join(IBLFOLDER, "Studio_Irradiance.dds")
    SetIBLmaps(radianceMap, irradianceMap)


def UseExteriorIBL():
    radianceMap = os.path.join(IBLFOLDER, "Exterior_Radiance.dds")
    irradianceMap = os.path.join(IBLFOLDER, "Exterior_Irradiance.dds")
    SetIBLmaps(radianceMap, irradianceMap)


def UseInteriorIBL():
    radianceMap = os.path.join(IBLFOLDER, "Interior_Radiance.dds")
    irradianceMap = os.path.join(IBLFOLDER, "Interior_Irradiance.dds")
    SetIBLmaps(radianceMap, irradianceMap)


def UseLegacyShader():
    multimats = filter(lambda m: rt.classOf(m) == rt.MultiMaterial, rt.sceneMaterials)
    flightSimMats = filter(lambda m: rt.ClassOf(m) == rt.FlightSim, rt.sceneMaterials)
    for multi in multimats:
        for m in multi.materialList:
            if rt.ClassOf(m) == rt.FlightSim:
                flightSimMats.append(m)
    for mat in flightSimMats:
        mat.setShaderTechniqueByName("Tech_Legacy")


# def SetupIBL(iblType):
#     if iblType == 0:
#         UseStudioIBL()
#     elif iblType == 1:
#         UseExteriorIBL()
#     elif iblType == 2:
#         UseInteriorIBL()
#     else:
#         print("Error, no valid IBL selected")
#
# def HelloWorld():
#     print "hello"

