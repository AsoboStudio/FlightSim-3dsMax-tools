Assembly = dotNetClass "System.Reflection.Assembly"
Assembly.loadfrom "C:\Program Files\Autodesk\3ds Max 2019\bin\assemblies\Max2Babylon.dll"
maxScriptManager = dotNetObject "Max2Babylon.MaxScriptManager"

maxScriptManager.GetGuid()

if $ != undefined then
(
	for n in (selection as array) do
	(
		guid = maxScriptManager.GetGuid(n.handle)
		print(guid)
	)
)
else
(
	messagebox "Nothing selected"
)