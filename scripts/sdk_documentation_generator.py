import inspect
import os
import types

import maxsdk


def get_module_documentation(module):
    doc = ""
    for name, mem in inspect.getmembers(module):
        functionPage = ""
        if type(mem) == types.FunctionType:
            name = mem.__name__
            description = mem.__doc__
            argList = ""
            allArg = inspect.getargspec(mem)
            chosenArg = []
            if allArg.args is not None:
                chosenArg += allArg.args
            if allArg.keywords is not None:
                chosenArg += allArg.keywords

            for j,args in enumerate(chosenArg):
                if args is not None:                    
                    argList += str(args)
                    if j != len(chosenArg) - 1:
                        argList += " , " 
                            
            functionPage += "{0}( {1} )\n\n".format(name, argList)
            if description is not None:
                functionPage += description + "\n\n"
            functionPage = functionPage.replace("    ", "")
            functionPage = functionPage.replace("\n", "\n    ")
            doc += functionPage
            doc += "\n"
    return doc

def get_all_submodule(module):
    submodules = []
    for name, mem in inspect.getmembers(maxsdk):
        if type(mem) == types.ModuleType:
            submodules.append((name, mem))
            
    print(submodules)
    return submodules

def main(outputPath, module):
    document = ""
    document += "<h1>MAXSDK DOCUMENTATION :</h1>\n"
    desiredPath = os.path.join(outputPath, module.__name__)

    if not os.path.exists(desiredPath):
        os.mkdir(desiredPath)
    sdkModules = get_all_submodule(module)
    for name, mod in sdkModules:
        page = "<h1>{0} DOCUMENTATION :</h1>\n".format(name).upper()
        moduleDoc = mod.__doc__
        if moduleDoc is not None:
            page += moduleDoc + "\n\n"
        currentDoc = get_module_documentation(mod)
        if currentDoc is not None:
            page += currentDoc
    
        with open(os.path.join(desiredPath,"{0}.md".format(name)), "w+") as f:
            f.write(page)
    print("finished")


if __name__ == "__main__":
    main("E:\\", maxsdk)
