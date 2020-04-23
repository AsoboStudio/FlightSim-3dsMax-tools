
FlightSimPluginPath =  (pathConfig.appendPath (pathConfig.getCurrentProjectFolder()) @"Tools\3DSMAX\FlightSimPackage\src\scripts")

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
