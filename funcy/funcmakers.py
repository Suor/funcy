from inspect import isbuiltin
from functools import wraps
from operator import itemgetter
from collections import Mapping, Set
from itertools import ifilter, ifilterfalse

from .simple_funcs import identity
from .strings import re_tester, re_finder, _re_type


__all__ = ('make_func', 'make_pred', 'wrap_mapper', 'wrap_selector')


def make_func(f, builtin=False, test=False):
    if callable(f):
        return f
    elif f is None:
        # pass None to builtin as predicate or mapping function for speed
        return None if builtin else \
               bool if test else identity
    elif isinstance(f, (str, unicode, _re_type)):
        return re_tester(f) if test else re_finder(f)
    elif isinstance(f, (int, slice)):
        return itemgetter(f)
    elif isinstance(f, Mapping):
        return f.get
    elif isinstance(f, Set):
        return f.__contains__
    else:
        raise TypeError("Can't make a func from %s" % f.__class__.__name__)

def make_pred(pred, builtin=False):
    return make_func(pred, builtin=builtin, test=True)


def _wrap_higher_order(func, test):
    # NOTE: builtin housekeeping is optimization:
    #       map(None, ...) is much faster than map(identity, ...)
    builtin = isbuiltin(func) or func in {ifilter, ifilterfalse}
    return wraps(func)(lambda f, *seqs: func(make_func(f, builtin=builtin, test=test), *seqs))

def wrap_mapper(func):
    return _wrap_higher_order(func, test=False)

def wrap_selector(func):
    return _wrap_higher_order(func, test=True)
