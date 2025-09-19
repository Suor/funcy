from .decorators import unwrap as unwrap
from _typeshed import Incomplete
from typing import NamedTuple

IS_PYPY: Incomplete
ARGS: Incomplete
two_arg_funcs: str
STD_MODULES: Incomplete

class Spec(NamedTuple):
    max_n: Incomplete
    names: Incomplete
    req_n: Incomplete
    req_names: Incomplete
    varkw: Incomplete

def get_spec(func, _cache={}): ...
