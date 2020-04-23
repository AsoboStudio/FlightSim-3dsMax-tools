FlightSimPluginPath = systemTools.getEnvVariable "MSFS_SDK" + "Tools\3dsMax\FlightSimPackage\scripts"
if FlightSimPluginPath == undefined then
(
messageBox ("The Microsoft Flight Simulator SDK is not properly installed.\nPlease re-run the installer to fix the issue.")
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
