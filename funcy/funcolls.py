from .funcs import compose, ijuxt
from .colls import some, none


__all__ = ['all_fn', 'any_fn', 'none_fn', 'some_fn']


def all_fn(*fs):
    return compose(all, ijuxt(*fs))

def any_fn(*fs):
    return compose(any, ijuxt(*fs))

def none_fn(*fs):
    return compose(none, ijuxt(*fs))

def some_fn(*fs):
    return compose(some, ijuxt(*fs))


from whatever import _


def test_all_fn():
    assert filter(all_fn(_ > 3, _ % 2), range(10)) == [5, 7, 9]

def test_some_fn():
    assert some_fn(_-1, _*0, _+1, _*2)(1) == 2
