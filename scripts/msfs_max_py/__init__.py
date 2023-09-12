from pymxs import runtime as rt
import os
import sys
import importlib
sys.path.append(os.path.dirname(__file__))
from maxsdk.globals import *


# start installing FlightSim material and legacy maxscript script
c = os.path.dirname(__file__)
cmd = 'filein @"{0}\\..\\msfs_max_ms\\FlightSim_EntryPoint.ms"'.format(c)
rt.execute(cmd)

IS_PUBLIC_SDK = rt.globalVars.get("IS_PUBLIC_SDK")

if not IS_PUBLIC_SDK:
    if MAXVERSION() >= MAX2021:
        from configparser import ConfigParser
        configur = ConfigParser()
        configur.read(os.path.join(c,'internal_tools.ini'))
        internal_modules = [] 
        for k in configur["INTERNAL"]:
            internal_modules.append(configur["INTERNAL"].get(k).replace('"',''))
    else:
        from ConfigParser import RawConfigParser
        configur = RawConfigParser()
        configur.read(os.path.join(c,'internal_tools.ini'))
        internal_modules = [] 
        for (a,b) in configur.items("INTERNAL"):
            internal_modules.append((a,b)[1].replace('"',''))

  
    
    
if isMAX2019V3_SUP():
    import MultiExporter
    import ModeldefConverter
    import PBRViewportManager
    
    if MAXVERSION() < MAX2023 and not IS_PUBLIC_SDK:
        for module in internal_modules:
            importlib.import_module(module)

print("FlightSim python package installed") 

