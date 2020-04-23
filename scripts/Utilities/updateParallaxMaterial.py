from pymxs import runtime as rt
import os
import logging
import sys
from maxsdk import perforce as sdkperforce

def updateParallax():
    multimats = filter(lambda m: rt.classOf(m) == rt.MultiMaterial, rt.sceneMaterials)
    flightSimMats = filter(lambda m: rt.ClassOf(m) == rt.FlightSim, rt.sceneMaterials)
    for multi in multimats:
        for m in multi.materialList:
            if rt.ClassOf(m) == rt.FlightSim:
                flightSimMats.append(m)
    for mat in flightSimMats:
        if mat.materialTYpe == 8:
            heightmapPath = mat.HeightmapTex
            if heightmapPath:
                mat.corridor = True
                mat.HeightmapTex = ""
                print "{0} has been update".format(mat.name)


maxFile = {r"d:\KittyHawk\ASSETS\KittyHawk_Data\ART\fs\object\Global\Asobo_Buildings\Airports\Specific\Adolfo_Suarez\Adolfo_Suarez_Airport.max",
r"d:\KittyHawk\ASSETS\KittyHawk_Data\ART\fs\object\Global\Asobo_Buildings\Airports\Specific\Billy_Bishop\billy_bishop.max",
r"d:\KittyHawk\ASSETS\KittyHawk_Data\ART\fs\object\Global\Asobo_Buildings\Airports\Specific\Blaise_Diagne\Blaise_Diagne.max",
r"d:\KittyHawk\ASSETS\KittyHawk_Data\ART\fs\object\Global\Asobo_Buildings\Airports\Specific\Cairo\Cairo_airport.max",
r"d:\KittyHawk\ASSETS\KittyHawk_Data\ART\fs\object\Global\Asobo_Buildings\Airports\Specific\Chicago_OHare\Chicago_Ohare_Hangars.max",
r"d:\KittyHawk\ASSETS\KittyHawk_Data\ART\fs\object\Global\Asobo_Buildings\Airports\Specific\Chicago_OHare\ChicagoOHare_Airport_Good_Positionning.max",
r"d:\KittyHawk\ASSETS\KittyHawk_Data\ART\fs\object\Global\Asobo_Buildings\Airports\Specific\Denver\Denver_Airport.max",
r"d:\KittyHawk\ASSETS\KittyHawk_Data\ART\fs\object\Global\Asobo_Buildings\Airports\Specific\Frankfurt\Frankfurt_Blockout.max",
r"d:\KittyHawk\ASSETS\KittyHawk_Data\ART\fs\object\Global\Asobo_Buildings\Airports\Specific\Gibraltar\Gibraltar_Good_Positionning.max",
r"d:\KittyHawk\ASSETS\KittyHawk_Data\ART\fs\object\Global\Asobo_Buildings\Airports\Specific\Heathrow\Heathrow_airport.max",
r"d:\KittyHawk\ASSETS\KittyHawk_Data\ART\fs\object\Global\Asobo_Buildings\Airports\Specific\Innsbruck\Innsbrudck_Buildings.max",
r"d:\KittyHawk\ASSETS\KittyHawk_Data\ART\fs\object\Global\Asobo_Buildings\Airports\Specific\Madere\Tarmac_Madere.max",
r"d:\KittyHawk\ASSETS\KittyHawk_Data\ART\fs\object\Global\Asobo_Buildings\Airports\Specific\Paris_Charles_De_Gaulle\Paris_Charles_De_Gaulle.max",
r"d:\KittyHawk\ASSETS\KittyHawk_Data\ART\fs\object\Global\Asobo_Buildings\Airports\Specific\Paro\Paro_Good_Positionning.max",
r"d:\KittyHawk\ASSETS\KittyHawk_Data\ART\fs\object\Global\Asobo_Buildings\Airports\Specific\Queenstown\Queenstown_Builidng.max",
r"d:\KittyHawk\ASSETS\KittyHawk_Data\ART\fs\object\Global\Asobo_Buildings\Airports\Specific\Saba\Saba_airport.max",
r"d:\KittyHawk\ASSETS\KittyHawk_Data\ART\fs\object\Global\Asobo_Buildings\Airports\Specific\San_Francisco\SanFrancisco_Airport.max",
r"d:\KittyHawk\ASSETS\KittyHawk_Data\ART\fs\object\Global\Asobo_Buildings\Airports\Specific\San_Francisco\SanFrancisco_Hangars.max",
r"d:\KittyHawk\ASSETS\KittyHawk_Data\ART\fs\object\Global\Asobo_Buildings\Airports\Specific\Seattle_Tacoma\Seattle_Approaching_Light_Bridge.max",
r"d:\KittyHawk\ASSETS\KittyHawk_Data\ART\fs\object\Global\Asobo_Buildings\Airports\Specific\Seattle_Tacoma\Seattle_Good_Positionning.max",
r"d:\KittyHawk\ASSETS\KittyHawk_Data\ART\fs\object\Global\Asobo_Buildings\Airports\Specific\Seattle_Tacoma\Seattle_Hangars.max",
r"d:\KittyHawk\ASSETS\KittyHawk_Data\ART\fs\object\Global\Asobo_Buildings\Airports\Specific\Sedona\Sedona.max",
r"d:\KittyHawk\ASSETS\KittyHawk_Data\ART\fs\object\Global\Asobo_Buildings\Airports\Specific\Sydney\Sydney_airport.max",
r"d:\KittyHawk\ASSETS\KittyHawk_Data\ART\fs\object\Global\Asobo_Buildings\Airports\Specific\Sydney\Sydney_airport_Terminal02.max",
r"d:\KittyHawk\ASSETS\KittyHawk_Data\ART\fs\object\Global\Asobo_Buildings\Airports\Specific\Sydney\Sydney_Buildings.max",
r"d:\KittyHawk\ASSETS\KittyHawk_Data\ART\fs\object\Global\Asobo_Buildings\Airports\Specific\Toncontin\toncontin_airport.max"}

maxFile = {r"d:\KittyHawk\ASSETS\KittyHawk_Data\ART\fs\object\Global\Asobo_Buildings\Specific\Frankfurt\Frankfurt_Blockout.max"}

for file in maxFile:
    # loaded = rt.loadMaxFile(file, quiet=True)
    # sdkperforce.P4edit(file)
    updateParallax()
    # rt.saveMaxFile(file)
