from funcy.types import *


def test_iterable():
    assert iterable([])
    assert iterable({})
    assert iterable('abc')
    assert iterable(iter([]))
    assert iterable(x for x in range(10))
    assert iterable(range(10))

    assert not iterable(1)


def test_is_iter():
    assert is_iter(iter([]))
    assert is_iter(x for x in range(10))

    assert not is_iter([])
    assert not is_iter(range(10))
