from .compat import PY2


if PY2:
    from .py2 import *  # noqa
    from .py2 import __all__
else:
    from .py3 import *  # noqa
    from .py3 import __all__  # noqa
