from funcy.objects import *


def test_monkey():
    class A(object):
        def f(self):
            return 7

    @monkey(A)
    def f(self):
        return f.original(self) * 6

    assert A().f() == 42


def test_monkey_property():
    class A(object):
        pass

    @monkey(A)
    @property
    def prop(self):
        return 42

    assert A().prop == 42
