FlightSimPluginPath = systemTools.getEnvVariable "MSFS_SDK"

if FlightSimPluginPath == undefined then
(
    FlightSimPluginPath = pathConfig.appendPath (symbolicPaths.getPathValue(9)) "FlightSimTools"    
)
else
(
    FlightSimPluginPath = pathConfig.appendPath(FlightSimPluginPath  "Tools\3dsMax\FlightSimPackage\scripts")
)

EntryPoint = pathConfig.appendPath FlightSimPluginPath @"FlightSim_EntryPoint.ms"

if ((getfiles EntryPoint).count == 0) then
(
    print("The Microsoft Flight Simulator SDK tools are not properly installed.\nPlease re-run the installer to fix the issue\n")
) 
else
(
    try
    (
        filein(pathConfig.appendPath FlightSimPluginPath @"FlightSim_EntryPoint.ms")
    )
    catch
    (
        errorMessage = getCurrentException()
        messageBox ("Error opening FlightSim_EntryPoint.ms:\n" + errorMessage) title:"FlightSim" beep:true
    )
    
    if ((maxversion())[1] > 20000) then
    (
        try
        (
            python.ExecuteFile (pathConfig.appendPath FlightSimPluginPath @"main.py")
        )
        catch
        (
            errorMessage = getCurrentException()
            messageBox ("Error opening main.py:\n" + errorMessage) title:"FlightSim" beep:true
        )
    )
)  



