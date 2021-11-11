from __future__ import absolute_import
from inspect import CO_VARARGS, CO_VARKEYWORDS
try:
    from inspect import signature
except ImportError:
    signature = None  #
from collections import namedtuple
import types
import re

from .compat import PY2
from .decorators import unwrap


# This provides sufficient introspection for *curry() functions.
#
# We only really need a number of required positional arguments.
# If arguments can be specified by name (not true for many builtin functions),
# then we need to now their names to ignore anything else passed by name.
#
# Stars mean some positional argument which can't be passed by name.
# Functions not mentioned here get one star "spec".
ARGS = {}


builtins_name = '__builtin__' if PY2 else 'builtins'
ARGS[builtins_name] = {
    'bool': 'x',
    'complex': 'real,imag',
    'enumerate': 'sequence,start' if PY2 else 'iterable,start',
    'file': 'file-**',
    'float': 'x',
    'int': 'x-*',
    'long': 'x-*',
    'open': 'name-**' if PY2 else 'file-**',
    'round': 'number-*',
    'setattr': '***',
    'str': '*-*' if PY2 else 'object-*',
    'unicode': 'string-**',
    '__import__': 'name-****',
    '__buildclass__': '***',
    # Complex functions with different set of arguments
    'iter': '*-*',
    'format': '*-*',
    'type': '*-**',
}
# Add two argument functions
two_arg_funcs = '''cmp coerce delattr divmod filter getattr hasattr isinstance issubclass
                   map pow reduce'''
ARGS[builtins_name].update(dict.fromkeys(two_arg_funcs.split(), '**'))


ARGS['functools'] = {'reduce': '**'}


ARGS['itertools'] = {
    'accumulate': 'iterable-*',
    'combinations': 'iterable,r',
    'combinations_with_replacement': 'iterable,r',
    'compress': 'data,selectors',
    'groupby': 'iterable-*',
    'permutations': 'iterable-*',
    'repeat': 'object-*',
}
two_arg_funcs = 'dropwhile filterfalse ifilter ifilterfalse starmap takewhile'
ARGS['itertools'].update(dict.fromkeys(two_arg_funcs.split(), '**'))


ARGS['operator'] = {
    'delslice': '***',
    'getslice': '***',
    'setitem': '***',
    'setslice': '****',
}
two_arg_funcs = """
    _compare_digest add and_ concat contains countOf delitem div eq floordiv ge getitem
    gt iadd iand iconcat idiv ifloordiv ilshift imatmul imod imul indexOf ior ipow irepeat
    irshift is_ is_not isub itruediv ixor le lshift lt matmul mod mul ne or_ pow repeat rshift
    sequenceIncludes sub truediv xor
"""
ARGS['operator'].update(dict.fromkeys(two_arg_funcs.split(), '**'))
ARGS['operator'].update([
    ('__%s__' % op.strip('_'), args) for op, args in ARGS['operator'].items()])
ARGS['_operator'] = ARGS['operator']


# Fixate this
STD_MODULES = set(ARGS)


# Describe some funcy functions, mostly for r?curry()
ARGS['funcy.seqs'] = {
    'map': 'f*', 'lmap': 'f*', 'xmap': 'f*',
    'mapcat': 'f*', 'lmapcat': 'f*',
}
ARGS['funcy.colls'] = {
    'merge_with': 'f*',
}


type_classes = (type, types.ClassType) if hasattr(types, 'ClassType') else type
Spec = namedtuple("Spec", "max_n names req_n req_names kw")


def get_spec(func, _cache={}):
    func = getattr(func, '__original__', None) or unwrap(func)
    try:
        return _cache[func]
    except (KeyError, TypeError):
        pass

    mod = getattr(func, '__module__', None)
    if mod in STD_MODULES or mod in ARGS and func.__name__ in ARGS[mod]:
        _spec = ARGS[mod].get(func.__name__, '*')
        required, _, optional = _spec.partition('-')
        req_names = re.findall(r'\w+|\*', required)  # a list with dups of *
        max_n = len(req_names) + len(optional)
        req_n = len(req_names)
        spec = Spec(max_n=max_n, names=set(), req_n=req_n, req_names=set(req_names), kw=False)
        _cache[func] = spec
        return spec
    elif isinstance(func, type_classes):
        # Old style classes without base
        if not hasattr(func, '__init__'):
            return Spec(max_n=0, names=set(), req_n=0, req_names=set(), kw=False)
        # __init__ inherited from builtin classes
        objclass = getattr(func.__init__, '__objclass__', None)
        if objclass and objclass is not func:
            return get_spec(objclass)
        # Introspect constructor and remove self
        spec = get_spec(func.__init__)
        self_set = set([func.__init__.__code__.co_varnames[0]])
        return spec._replace(max_n=spec.max_n - 1, names=spec.names - self_set,
                             req_n=spec.req_n - 1, req_names=spec.req_names - self_set)
    else:
        try:
            defaults_n = len(func.__defaults__)
        except (AttributeError, TypeError):
            defaults_n = 0
        try:
            varnames = func.__code__.co_varnames
            n = func.__code__.co_argcount
            names = set(varnames[:n])
            req_n = n - defaults_n
            req_names = set(varnames[:req_n])
            kw = bool(func.__code__.co_flags & CO_VARKEYWORDS)
            # If there are varargs they could be required, but all keywords args can't be
            max_n = req_n + 1 if func.__code__.co_flags & CO_VARARGS else n
            return Spec(max_n=max_n, names=names, req_n=req_n, req_names=req_names, kw=kw)
        except AttributeError:
            # We use signature last to be fully backwards compatible. Also it's slower
            try:
                sig = signature(func)
            except (ValueError, TypeError):
                raise ValueError('Unable to introspect %s() arguments'
                    % (getattr(func, '__qualname__', None) or getattr(func, '__name__', func)))
            else:
                spec = _cache[func] = _sig_to_spec(sig)
                return spec


def _sig_to_spec(sig):
    max_n, names, req_n, req_names, kw = 0, set(), 0, set(), False
    for name, param in sig.parameters.items():
        max_n += 1
        if param.kind == param.VAR_KEYWORD:
            kw = True
        elif param.kind == param.VAR_POSITIONAL:
            req_n += 1
        else:
            names.add(name)
            if param.default is param.empty:
                req_n += 1
                req_names.add(name)
    return Spec(max_n=max_n, names=names, req_n=req_n, req_names=req_names, kw=kw)
