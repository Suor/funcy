from .funcs import compose, ijuxt
from .colls import some, none, one


__all__ = ['all_fn', 'any_fn', 'none_fn', 'one_fn', 'some_fn']


def all_fn(*fs):
    """Constructs a predicate, which holds when all fs hold."""
    return compose(all, ijuxt(*fs))

def any_fn(*fs):
    """Constructs a predicate, which holds when any fs holds."""
    return compose(any, ijuxt(*fs))

def none_fn(*fs):
    """Constructs a predicate, which holds when none of fs hold."""
    return compose(none, ijuxt(*fs))

def one_fn(*fs):
    """Constructs a predicate, which holds when exactly one of fs holds."""
    return compose(one, ijuxt(*fs))

def some_fn(*fs):
    """Constructs a function, which calls fs one by one
       and returns first truthy result."""
    return compose(some, ijuxt(*fs))
