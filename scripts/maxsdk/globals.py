import pymxs

rt = pymxs.runtime

MAX2021 = 23000
MAX2020 = 22000
MAX2019 = 21000

def DEBUG_MODE():
    vGlobal = rt.name("DEBUG_MODE")
    try:
        if rt.globalVars.get(vGlobal):
            return True
        else:
            return False
    except:
        return False

def MAXVERSION():
    return rt.maxversion()[0]
    
def GetMaxMainWindow():
    if MAXVERSION() >= MAX2021:
        import qtmax
        return qtmax.GetQMaxMainWindow()
    else:
        import MaxPlus
        return MaxPlus.GetQMaxMainWindow()