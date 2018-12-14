import sys
import six

from funcy.objects import *


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


def test_singleton_meta():
    @six.add_metaclass(SingletonMeta)
    class A:
        pass

    @six.add_metaclass(SingletonMeta)
    class B:
        pass

    assert A() is A()
    assert A() == A()
    assert A() is not B()
    assert A() != B()
