import sys

if sys.version_info[0] == 2:
    from .py2 import *
else:
    from .py3 import *
