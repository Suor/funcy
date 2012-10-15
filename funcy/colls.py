from __builtin__ import all as _all, any as _any
from itertools import ifilter, imap

from .funcs import complement


def is_distinct(coll):
    raise NotImplementedError


def all(pred, coll=None):
    if coll is None:
        return _all(pred)
    return _all(imap(pred, coll))

def any(pred, coll=None):
    if coll is None:
        return _any(pred)
    return _any(imap(pred, coll))

none = complement(any)

# NOTE: name it some() ?
def first(pred, coll=None):
    if coll is None:
        return first(None, pred)
    return next(ifilter(pred, coll), None)


# TODO: capabilities + type tests




from whatever import _

def test_all():
    assert all([1,2,3])
    assert not all([1,2,''])
    assert all(callable, [abs, open, int])
    assert not all(_ < 3, [1,2,5])

def test_any():
    assert any([0, False, 3, ''])
    assert any([0, False, '']) == False
    assert any(_ > 0, [1,2,0])
    assert any(_ < 0, [1,2,0]) == False

def test_none():
    assert none([0, False])
    assert none(_ < 0, [0, -1]) == False

def test_first():
    assert first([0, '', 2, 3]) == 2
    assert first(_ > 3, range(10)) == 4
