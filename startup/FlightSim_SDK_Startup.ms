FlightSimPluginPath = systemTools.getEnvVariable "MSFS_SDK"

if FlightSimPluginPath == undefined then
(
    FlightSimPluginPath = pathConfig.appendPath (symbolicPaths.getPathValue(9)) "FlightSimTools"    
)
else
(
    FlightSimPluginPath = FlightSimPluginPath + "Tools\3dsMax\FlightSimPackage\scripts"
)

if ((getfiles (FlightSimPluginPath+"\\*")).count == 0) then
(
    print("The Microsoft Flight Simulator SDK tools are not properly installed.\nPlease re-run the installer to fix the issue\n")
) 
else
(
    if ((maxversion())[1] >= 20000) then
    (
        try
        (
            global IS_PUBLIC_SDK = true
            python.Init()
            sys = python.Import("sys")
            sys.path.append(FlightSimPluginPath)
            python.Import("msfs_max_py") -- importing the package trigger the installation of menu
        )
        catch
        (
            errorMessage = getCurrentException()
            messageBox ("Error opening msfs_max_py.py:\n" + errorMessage) title:"FlightSim" beep:true
        )
    )
    else
    (
        try
        (
            filein(pathConfig.appendPath FlightSimPluginPath @"msfs_max_ms\FlightSim_EntryPoint.ms")
        )
        catch
        (
            errorMessage = getCurrentException()
            messageBox ("Error opening FlightSim_EntryPoint.ms:\n" + errorMessage) title:"FlightSim" beep:true
        )
    )
)  