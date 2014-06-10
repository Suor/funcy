import sys

if sys.version_info[0] == 2:
    from .py2 import *
    from .py2 import __all__
else:
    from .py3 import *
    from .py3 import __all__
