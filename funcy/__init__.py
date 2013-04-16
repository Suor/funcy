from .calc import *
from .colls import *
from .decorators import *
from .funcolls import *
from .funcs import *
from .seqs import *
from .strings import *
from .flow import *
from .objects import cached_property
from .namespaces import namespace
from .debug import *


def inc(x):
    return x + 1

def dec(x):
    return x - 1

def even(x):
    return x % 2 == 0

def odd(x):
    return x % 2 == 1
