from .funcs import compose, ijuxt
from .colls import some, none, one


__all__ = ['all_fn', 'any_fn', 'none_fn', 'one_fn', 'some_fn']


def all_fn(*fs):
    return compose(all, ijuxt(*fs))

def any_fn(*fs):
    return compose(any, ijuxt(*fs))

def none_fn(*fs):
    return compose(none, ijuxt(*fs))

def one_fn(*fs):
    return compose(one, ijuxt(*fs))

def some_fn(*fs):
    return compose(some, ijuxt(*fs))
