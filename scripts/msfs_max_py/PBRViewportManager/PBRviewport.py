from pymxs import runtime as rt
import os
from maxsdk.globals import *

scripts = (os.path.join(os.path.join(os.path.dirname(__file__),os.pardir),os.pardir))
FlightSimMaterial = os.path.abspath(os.path.join(os.path.join(scripts,"msfs_max_mx"),"FlightSimMaterial"))
IBLFOLDER = os.path.join(FlightSimMaterial, "IBLmap")


def SetIBLmaps(radianceMap, irradianceMap):
    multimats = filter(lambda m: rt.classOf(m) == rt.MultiMaterial, rt.sceneMaterials)
    flightSimMats = filter(lambda m: rt.ClassOf(m) == rt.FlightSim, rt.sceneMaterials)
    if(MAXVERSION() >= MAX2021):
        multimats = list(multimats)
        flightSimMats = list(flightSimMats)
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
    multimats = list(filter(lambda m: rt.classOf(m) == rt.MultiMaterial, rt.sceneMaterials))
    flightSimMats = list(filter(lambda m: rt.ClassOf(m) == rt.FlightSim, rt.sceneMaterials))
    for multi in multimats:
        for m in multi.materialList:
            if rt.ClassOf(m) == rt.FlightSim:
                flightSimMats.append(m)
    for mat in flightSimMats:
        mat.setShaderTechniqueByName("Tech_Legacy")


