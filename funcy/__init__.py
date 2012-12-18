from .calc import *
from .colls import *
from .decorators import *
from .funcolls import *
from .funcs import *
from .seqs import *
from .strings import *
from .flow import ignore, silent, retry, fallback # partially experimental
# from debug import * # fully experimental


def inc(x):
    return x + 1

def dec(x):
    return x - 1

def even(x):
    return x % 2 == 0

def odd(x):
    return x % 2 == 1
