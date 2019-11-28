import sys
import pytest
from funcy.objects import *
from funcy import suppress


### @cached_property

def test_cached_property():
    calls = [0]

    class A(object):
        @cached_property
        def prop(self):
            calls[0] += 1
            return 7

    a = A()
    assert a.prop == 7
    assert a.prop == 7
    assert calls == [1]

    a.prop = 42
    assert a.prop == 42

    del a.prop
    assert a.prop == 7
    assert calls == [2]

def test_cached_property_doc():
    class A(object):
        @cached_property
        def prop(self):
            "prop doc"
            return 7

    assert A.prop.__doc__ == "prop doc"


def test_cached_readonly():
    class A(object):
        @cached_readonly
        def prop(self):
            return 7

    a = A()
    assert a.prop == 7
    with pytest.raises(AttributeError):
        a.prop = 8


def test_wrap_prop():
    calls = []

    # Not using @contextmanager to not make this a decorator
    class Manager:
        def __init__(self, name):
            self.name = name

        def __enter__(self):
            calls.append(self.name)
            return self

        def __exit__(self, *args):
            pass

    class A(object):
        @wrap_prop(Manager('p'))
        @property
        def prop(self):
            return 1

        @wrap_prop(Manager('cp'))
        @cached_property
        def cached_prop(self):
            return 1

    a = A()
    assert a.prop and calls == ['p']
    assert a.prop and calls == ['p', 'p']
    assert a.cached_prop and calls == ['p', 'p', 'cp']
    assert a.cached_prop and calls == ['p', 'p', 'cp']

    # Wrap __set__ for data props
    a = A()
    calls[:] = []
    with suppress(AttributeError):
        a.prop = 2
    assert calls == ['p']

    # Do not wrap __set__ for non-data props
    a.cached_property = 2
    assert calls == ['p']


### Monkey tests

def test_monkey():
    class A(object):
        def f(self):
            return 7

    @monkey(A)
    def f(self):
        return f.original(self) * 6

    assert A().f() == 42


def test_monkey_with_name():
    class A(object):
        def f(self):
            return 7

    @monkey(A, name='f')
    def g(self):
        return g.original(self) * 6

    assert A().f() == 42


def test_monkey_property():
    class A(object):
        pass

    @monkey(A)
    @property
    def prop(self):
        return 42

    assert A().prop == 42


def f(x):
    return x

def test_monkey_module():
    this_module = sys.modules[__name__]

    @monkey(this_module)
    def f(x):
        return f.original(x) * 2

    assert f(21) == 42


def test_namespace():
    class tests(namespace):
        is_int = lambda x: isinstance(x, int)

    tests.is_int(10)


def test_lazy_object():
    class A(object):
        x = 42
        def __init__(self):
            log.append('init')

    log = []
    a = LazyObject(A)
    assert not log
    assert a.x == 42
