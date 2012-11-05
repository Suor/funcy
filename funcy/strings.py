import re
from operator import methodcaller
from itertools import imap

from .funcs import identity


def _make_getter(regex):
    if regex.groups == 0:
        return methodcaller('group')
    elif regex.groupindex == {}:
        return methodcaller('groups')
    elif regex.groups == len(regex.groupindex):
        return methodcaller('groupdict')
    else:
        return identity

_re_type = type(re.compile(r''))

def _prepare(regex):
    if not isinstance(regex, _re_type):
        regex = re.compile(regex)
    return regex, _make_getter(regex)


def re_iter(regex, s, flags=0):
    regex, getter = _prepare(regex)
    return imap(getter, re.finditer(regex, s, flags))

def re_all(regex, s, flags=0):
    return list(re_iter(regex, s, flags))

def re_find(regex, s, flags=0):
    regex, getter = _prepare(regex)
    result = re.search(regex, s, flags)
    return getter(result) if result else None
