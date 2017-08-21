from collections import defaultdict
from .cross import PY2


# This provides sufficient introspection for *curry() functions.
#
# We only really need a number of required positional arguments.
# If arguments can be specified by name (not true for many builtin functions),
# then we need to now their names to ignore anything else passed by name.
#
# Stars mean some positional argument which can't be passed by name.
# Functions not mentioned here get one star "spec".
REQUIRED_ARGS = {}


# These complex functions not really handled for now:
#     format, iter, type
builtins_name = '__builtin__' if PY2 else 'builtins'
REQUIRED_ARGS[builtins_name] = {
    'bool': 'x',
    'complex': ('real', 'imag'),
    'enumerate': ('sequence' if PY2 else 'iterable', 'start'),
    'file': ('file',),
    'float': 'x',
    'int': 'x',
    'long': 'x',
    'open': ('name' if PY2 else 'file',),
    'round': ('number',),
    'setattr': '***',
    'str': ('*' if PY2 else 'object',),
    'unicode': ('string',),
    '__import__': ('name',),
    '__buildclass__': '***',
}
# Add two argument functions
two_arg_funcs = '''cmp coerce delattr divmod filter getattr hasattr isinstance issubclass
                   map pow reduce'''
REQUIRED_ARGS[builtins_name].update(dict.fromkeys(two_arg_funcs.split(), '**'))


REQUIRED_ARGS['functools'] = {'reduce': '**'}


REQUIRED_ARGS['itertools'] = {
    'accumulate': ('iterable',),
    'combinations': ('iterable', 'r'),
    'combinations_with_replacement': ('iterable', 'r'),
    'compress': ('data', 'selectors'),
    'groupby': ('iterable',),
    'permutations': ('iterable',),
    'repeat': ('object',),
}
two_arg_funcs = 'dropwhile filterfalse ifilter ifilterfalse starmap takewhile'
REQUIRED_ARGS['itertools'].update(dict.fromkeys(two_arg_funcs.split(), '**'))


REQUIRED_ARGS['operator'] = {
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
REQUIRED_ARGS['operator'].update(dict.fromkeys(two_arg_funcs.split(), '**'))
REQUIRED_ARGS['operator'].update([
    ('__%s__' % op.strip('_'), args) for op, args in REQUIRED_ARGS['operator'].items()])
REQUIRED_ARGS['_operator'] = REQUIRED_ARGS['operator']


from .decorators import unwrap


def get_required_args(func):
    func = getattr(func, '__original__', None) or unwrap(func)
    print(func.__call__)
    try:
        defaults_len = len(func.__defaults__)
    except (AttributeError, TypeError):
        defaults_len = 0
    try:
        names = func.__code__.co_varnames
        count = func.__code__.co_argcount - defaults_len
        return names[:count] if names else '*' * count
    except AttributeError:
        if func.__module__ in REQUIRED_ARGS:
            return REQUIRED_ARGS[func.__module__].get(func.__name__, '*')
        else:
            raise ValueError('Unable to introspect function required arguments')

