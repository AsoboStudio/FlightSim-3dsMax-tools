import os
import sys

dir_path = os.path.dirname(os.path.realpath(__file__))
sdk_path = os.path.join(dir_path, os.pardir)

if dir_path not in sys.path:
    sys.path.append(dir_path)

if sdk_path not in sys.path:
    sys.path.append(sdk_path)


import animation_tool.mainWindow as mainWindow

# when in development mode we should reload all packages
reload(mainWindow)
import animation_tool.macro as macro
reload(macro)

# import maxsdk.debug

if __name__ == "__main__":
    main_view = mainWindow.MainView()
    main_view.show()
