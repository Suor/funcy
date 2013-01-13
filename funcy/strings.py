import re
from operator import methodcaller
from itertools import imap

from .funcs import identity, iffy


__all__ = ['re_iter', 're_all', 're_find', 're_finder', 're_test', 're_tester']


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
    # TODO: optimize compose() and use:
    # from .funcs import compose
    # return compose(iffy(getter), regex.search)

def re_tester(regex, flags=0):
    return lambda s: bool(re.search(regex, s, flags))

# TODO: re_allfinder? better name?
