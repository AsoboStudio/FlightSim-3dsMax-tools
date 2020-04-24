@echo off
setlocal enabledelayedexpansion

if not defined MSFS_SDK (
    echo MSFS_SDK is NOT defined
	goto ErrorCopyPlug
)

echo Please enter your 3DSMAX version
echo choose 1 for 2016
echo choose 2 for 2017
echo choose 3 for 2018
echo choose 4 for 2019
echo choose 5 for 2020
set /P N= :

:switch-case-maxversion
  goto :switch-case-N-%N% 2>nul || (
    echo Input version not accepted
    pause
    exit
  )
  
  :switch-case-N-1
    set _maxversion=2016
	goto copy-objects
  :switch-case-N-2
    set _maxversion=2017
	goto copy-objects
  :switch-case-N-3
    set _maxversion=2018
	goto copy-objects
  :switch-case-N-4
    set _maxversion=2019
	goto copy-objects
  :switch-case-N-5
	set _maxversion=2020
	goto copy-objects

:copy-objects
	set SourceDir="%~dp0"
	set DestDir="C:\Program Files\Autodesk\3ds Max %_maxversion%"
	echo :: Max version %_maxversion%
	set ScriptDir="%MSFS_SDK%\Tools\3dsMax\FlightSimPackage\scripts"
	
	echo :: Copying plug-in files
	echo :: From: %SourceDir%
	echo :: To: %DestDir%

	robocopy "%~dp0\plugins\glTF-Exporter\3ds Max\Public\%_maxversion%" %DestDir%\bin\assemblies *.* /S /R:0
	if errorlevel 8 goto ErrorCopyPlug

	robocopy "%~dp0\startup" %DestDir%\scripts\Startup FlightSim_SDK_Startup.ms /S
	if errorlevel 8 goto ErrorCopyPlug

	echo :: Copying scripts files
	echo :: From: %SourceDir%
	echo :: To: %ScriptDir%
	
	robocopy "%~dp0\scripts" %ScriptDir% *.* /S /R:0 /mir
	if errorlevel 8 goto ErrorCopyPlug

	

	goto Ok

:ErrorCopyPlug
for /l %%X in (1,1,10) do (
echo "*********************************************************"
echo ">>>>>> ERROR: Plug-in and Scripts couldn't be copied! <<<<<<<"
echo "*********************************************************"
)
pause
exit

:Ok
echo :: Scritps and plug-in copy succeeded!
pause
exit

