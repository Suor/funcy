from .primitives import *
from .calc import *
from .colls import *
from .decorators import *
from .funcolls import *
from .funcs import *
from .seqs import *
from .types import *
from .strings import *
from .flow import *
from .objects import *
from .namespaces import namespace
from .debug import *
from .primitives import *


# Python 2 style zip() for Python 3
import sys

if sys.version_info[0] == 3:
    _zip = zip
    def zip(*seqs):
        return list(_zip(*seqs))

