import sys
import os

localappdata_path=os.environ.get('LOCALAPPDATA')
# WARNING!: this path could not corrsipond on your pc
pydev_path = os.path.join(localappdata_path,"JetBrains/Toolbox/apps/PyCharm-P/ch-0/192.6603.34/helpers/pydev")
if not pydev_path in sys.path:
    sys.path.append(pydev_path)
print sys.path
import pydevd_pycharm
pydevd_pycharm.settrace('localhost', port=7720, suspend=False)