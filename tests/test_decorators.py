import pytest
from funcy.decorators import *


def test_decorator_no_args():
    @decorator
    def inc(call):
        return call() + 1

    @inc
    def ten():
        return 10

    assert ten() == 11


def test_decorator_with_args():
    @decorator
    def add(call, n):
        return call() + n

    @add(2)
    def ten():
        return 10

    assert ten() == 12


def test_decorator_kw_only_args():
    @decorator
    def add(call, **kwargs):  # TODO: use real kw-only args in Python 3
        return call() + kwargs.get("n", 1)

    def ten(a, b):
        return 10

    # Should work with or without parentheses
    assert add(n=2)(ten)(1, 2) == 12
    assert add()(ten)(1, 2) == 11
    assert add(ten)(1, 2) == 11


def test_decorator_access_arg():
    @decorator
    def multiply(call):
        return call() * call.n

    @multiply
    def square(n):
        return n

    assert square(5) == 25


def test_decorator_access_nonexistent_arg():
    @decorator
    def return_x(call):
        return call.x

    @return_x
    def f():
        pass

    with pytest.raises(AttributeError): f()


def test_decorator_required_arg():
    @decorator
    def deco(call):
        call.x

    @deco
    def f(x, y=42):
        pass

    with pytest.raises(AttributeError): f()


def test_double_decorator_defaults():
    @decorator
    def deco(call):
        return call.y

    @decorator
    def noop(call):
        return call()

    @deco
    @noop
    def f(x, y=1):
        pass

    assert f(42) == 1


def test_decorator_defaults():
    @decorator
    def deco(call):
        return call.y, call.z

    @deco
    def f(x, y=1, z=2):
        pass

    assert f(42) == (1, 2)


def test_decorator_with_method():
    @decorator
    def inc(call):
        return call() + 1

    class A(object):
        def ten(self):
            return 10

        @classmethod
        def ten_cls(cls):
            return 10

        @staticmethod
        def ten_static():
            return 10

    assert inc(A().ten)() == 11
    assert inc(A.ten_cls)() == 11
    assert inc(A.ten_static)() == 11


def test_decorator_with_method_descriptor():
    @decorator
    def exclaim(call):
        return call() + '!'

    assert exclaim(str.upper)('hi') == 'HI!'


def test_chain_arg_access():
    @decorator
    def decor(call):
        return call.x + call()

    @decor
    @decor
    def func(x):
        return x

    assert func(2) == 6


def test_meta_attribtes():
    @decorator
    def decor(call):
        return call()

    def func(x):
        "Some doc"
        return x

    decorated = decor(func)
    double_decorated = decor(decorated)

    assert decorated.__name__ == 'func'
    assert decorated.__module__ == __name__
    assert decorated.__doc__ == "Some doc"
    assert decorated.__wrapped__ is func
    assert decorated.__original__ is func

    assert double_decorated.__wrapped__ is decorated
    assert double_decorated.__original__ is func


def test_decorator_introspection():
    @decorator
    def decor(call, x):
        return call()

    assert decor.__name__ == 'decor'

    decor_x = decor(42)
    assert decor_x.__name__ == 'decor'
    assert decor_x._func is decor.__wrapped__
    assert decor_x._args == (42,)
    assert decor_x._kwargs == {}
