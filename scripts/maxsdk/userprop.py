from pymxs import runtime as rt

def setUserProp(node, keyName, value):
    if isinstance(value, str):
        rt.setUserProp(node, keyName, value)
    if isinstance(value, unicode):
        rt.setUserProp(node, keyName, value)
    if isinstance(value, int):
        rt.setUserProp(node, keyName, str(value))
    if isinstance(value, float):
        rt.setUserProp(node, keyName, str(value))


def getUserProp(node, keyName, defaultValue = None):
    res = rt.getUserProp(node, keyName)
    if res != None:
        return res
    else:
        return defaultValue


def getUserPropDict(node, propName, keyName=None):
    res = getUserProp(node, propName)
    dictRes = dict()
    try:
        keyValue = res.split(";")

        for kv in keyValue:
            k = kv.split("~")[0]
            v = kv.split("~")[1]
            dictRes.update({k: v})
        if not keyName:
            return dictRes
        else:
            return dictRes[keyName]
    except:
        return dictRes



def setUserPropDict(node, propName, dictObj):
    if isinstance(dictObj,dict):
        propertyValue = ""
        for i in range(len(dictObj.items())):
            key = list(dictObj.keys())[i]
            value = list(dictObj.values())[i]
            propertyValue += "{0}~{1}".format(str(key), str(value))
            if i < len(dictObj.items()) -1:
                propertyValue +=";"
        setUserProp(node, propName, propertyValue)

def setUserPropList(node, propName, listObj):
    if isinstance(listObj, list):
        propertyValue = ""
        objCount = len(listObj)
        for i in range(objCount):
            propertyValue += cleanupStringForPropListStorage(listObj[i])
            #if (i < objCount - 1):
            propertyValue += ";"
        rt.setUserProp(node, propName, propertyValue)

def getUserPropList(node, propName):
    res = rt.getUserProp(node, propName)
    if (res is None):
        return None
    listRes = list()    
    values = res.split(";")
    for v in values:
        if (v != None and v != ""):            
            listRes.append(v)
    return listRes

def removeUserProp(node, keyName):
    rt.deleteUserProp(node, keyName)
    
def getUserPropBuffer(node):
    propBuffer = rt.getUserPropBuffer(node)
    return propBuffer

def setUserPropBuffer(node, buffer):
    rt.setUserPropBuffer(node,buffer)

def openUserPropertyWindow():
    if(rt.UserDefinedPlus_isOpen):
        rt.macros.run("ASOBO","UserDefinedPlus") # if open, close it first
    rt.macros.run("ASOBO", "UserDefinedPlus")  # and open/reopen it to focus  

def cleanupStringForPropListStorage(string):
    cleanString = str()
    for c in string:        
        if (ord(c) < 128) and c != ";":
            cleanString += c
    return cleanString

def convertUserPropToObviousType(i):
    if (i == "False" or i == "false" or i == "FALSE"):
        return False
    elif (i == "True" or i == "true" or i == "TRUE"):
        return True
    else:
        try:
            return int(i)
        except:
            try:
                return float(i)
            except:
                try:
                    return str(i)
                except:
                    return unicode(i)
            


