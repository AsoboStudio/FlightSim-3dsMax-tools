from pymxs import runtime as rt
import os

def run():
    rt.execute('Assembly = dotNetClass "System.Reflection.Assembly"')
    dllPath = os.path.join(rt.symbolicPaths.getPathValue(1),"bin\\assemblies\\Max2Babylon.dll")
    rt.execute('Assembly.loadfrom "{0}"'.format(dllPath))
    rt.execute('maxScriptManager = dotNetObject "Max2Babylon.MaxScriptManager"')
    rt.maxScriptManager.AutoAssignLodInAnimationGroup()