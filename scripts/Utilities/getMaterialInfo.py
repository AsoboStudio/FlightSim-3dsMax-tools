from pymxs import runtime as rt
import os
import logging
import sys


def initLogger():
    logFilePath = "d:\KittyHawk\ASSETS\KittyHawk_Data\parallaxLogger.log"
    if os.path.exists(logFilePath):
        os.remove(logFilePath)

    logging.basicConfig(level=logging.DEBUG, filename=logFilePath, filemode="a+",
                        format="%(asctime)-15s %(levelname)-8s %(message)s")
    # to debug in max listener
    logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))


def logParallaxInfo():
    multimats = filter(lambda m: rt.classOf(m) == rt.MultiMaterial, rt.sceneMaterials)
    flightSimMats = filter(lambda m: rt.ClassOf(m) == rt.FlightSim, rt.sceneMaterials)
    for multi in multimats:
        for m in multi.materialList:
            if rt.ClassOf(m) == rt.FlightSim:
                flightSimMats.append(m)
    for mat in flightSimMats:
        if mat.materialTYpe == 8:
            heightmapPath = mat.HeightmapTex
            if not heightmapPath:
                logging.info("'{0}' is ParallaxWindow with no heightmap".format(mat.name))
            else:
                logging.info("'{0}' is ParallaxWindow with heightmap path '{1}'".format(mat.name, heightmapPath))


maxFile = list()
initLogger()
for root, dirs, files in os.walk("D:\KittyHawk\ASSETS\KittyHawk_Data", topdown=False):
    for name in files:
        filePath = os.path.join(root, name)
        filename, file_extension = os.path.splitext(filePath)
        if file_extension == ".max" or file_extension == ".MAX":
            maxFile.append(filePath)

for file in maxFile:
    loaded = rt.loadMaxFile(file, True)
    logParallaxInfo()
