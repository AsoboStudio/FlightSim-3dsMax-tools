FlightSimPluginPath = getFilenamePath (getThisScriptFilename())
filein (pathConfig.appendPath FlightSimPluginPath @"FlightSimMaterial\FlightSimMaterial.ms")
filein (pathConfig.appendPath FlightSimPluginPath @"FlightSim_Menu.ms")
filein (pathConfig.appendPath FlightSimPluginPath @"FlightSim_ProjectedDecal.ms")
filein (pathConfig.appendPath FlightSimPluginPath @"FlightSim_SphereCollider.ms")
filein (pathConfig.appendPath FlightSimPluginPath @"FlightSim_BoxCollider.ms")
filein (pathConfig.appendPath FlightSimPluginPath @"FlightSim_SphereFade.ms")
filein (pathConfig.appendPath FlightSimPluginPath @"FlightSim_CylinderCollider.ms")
filein (pathConfig.appendPath FlightSimPluginPath @"FlightSim_MacroLightOmni.ms")
filein (pathConfig.appendPath FlightSimPluginPath @"FlightSim_MacroLightSpot.ms")
filein (pathConfig.appendPath FlightSimPluginPath @"FlightSim_Light.ms")

print "EntryPoint"