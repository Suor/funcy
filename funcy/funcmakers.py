from inspect import getargspec, formatargspec, ArgSpec
from functools import wraps
from operator import itemgetter
from collections import Mapping, Set

from .cross import imap, ifilter, ifilterfalse, basestring, PY2
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
    elif isinstance(f, (basestring, _re_type)):
        return re_tester(f) if test else re_finder(f)
    elif isinstance(f, (int, slice)):
        return itemgetter(f)
    elif isinstance(f, Mapping):
        return f.__getitem__
    elif isinstance(f, Set):
        return f.__contains__
    else:
        raise TypeError("Can't make a func from %s" % f.__class__.__name__)

def make_pred(pred, builtin=False):
    return make_func(pred, builtin=builtin, test=True)


def _wrap_higher_order(func, test):
    # NOTE: builtin housekeeping:
    #       map(None, ...) is much faster than map(identity, ...),
    #       also map(None, ...) works as zip() for multiple seqs
    builtin = PY2 and func in set([map, filter, imap, ifilter, ifilterfalse])

    # We are going to construct function using eval to preserve signature.
    # So we need to inspect it first.
    try:
        spec = getargspec(func)
    except TypeError:
        spec = ArgSpec(('f',), 'seqs', None, None)
    # HACK: due to bug in python 3.4 - http://bugs.python.org/issue22203
    if not spec.args:
        spec = ArgSpec(('f',), 'seqs', None, None)

    # Slicing with [1:-1] to get rid of parentheses
    spec_str = formatargspec(*spec)[1:-1]
    rest = ArgSpec(spec.args[1:], *spec[1:])
    rest_str = formatargspec(*rest)[1:-1]

    # We use nested lambda to make func and make_func locals which are faster
    func_str = "lambda __func, __make_func: " \
               "lambda {spec}: __func(__make_func({f}, {builtin}, {test}), {rest})" \
               .format(spec=spec_str, f=spec.args[0], rest=rest_str,
                       builtin=builtin, test=test)

    wrapper = eval(func_str, {}, {})(func, make_func)
    return wraps(func)(wrapper)

def wrap_mapper(func):
    return _wrap_higher_order(func, test=False)

def wrap_selector(func):
    return _wrap_higher_order(func, test=True)
