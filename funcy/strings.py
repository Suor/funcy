import re
from operator import methodcaller

from .cross import imap
from .primitives import EMPTY
from .simple_funcs import identity, iffy


__all__ = ['re_iter', 're_all', 're_find', 're_finder', 're_test', 're_tester',
           'str_join',
           'cut_prefix', 'cut_suffix']


def _make_getter(regex):
    if regex.groups == 0:
        return methodcaller('group')
    elif regex.groups == 1 and regex.groupindex == {}:
        return methodcaller('group', 1)
    elif regex.groupindex == {}:
        return methodcaller('groups')
    elif regex.groups == len(regex.groupindex):
        return methodcaller('groupdict')
    else:
        return identity

_re_type = type(re.compile(r''))

def _prepare(regex, flags):
    if not isinstance(regex, _re_type):
        regex = re.compile(regex, flags)
    return regex, _make_getter(regex)


def re_iter(regex, s, flags=0):
    regex, getter = _prepare(regex, flags)
    return imap(getter, regex.finditer(s))

def re_all(regex, s, flags=0):
    return list(re_iter(regex, s, flags))

def re_find(regex, s, flags=0):
    return re_finder(regex, flags)(s)

def re_test(regex, s, flags=0):
    return re_tester(regex, flags)(s)


def re_finder(regex, flags=0):
    regex, getter = _prepare(regex, flags)
    return lambda s: iffy(getter)(regex.search(s))

def re_tester(regex, flags=0):
    if not isinstance(regex, _re_type):
        regex = re.compile(regex, flags)
    return lambda s: bool(regex.search(s))


def str_join(sep, seq=EMPTY):
    if seq is EMPTY:
        return str_join('', sep)
    else:
        return sep.join(imap(sep.__class__, seq))

def cut_prefix(s, prefix):
    return s[len(prefix):] if s.startswith(prefix) else s

def cut_suffix(s, suffix):
    return s[:-len(suffix)] if s.endswith(suffix) else s
