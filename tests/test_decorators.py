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
    def add(call, *, n=1):
        return call() + n

    def ten(a, b):
        return 10

    # Should work with or without parentheses
    assert add(n=2)(ten)(1, 2) == 12
    assert add()(ten)(1, 2) == 11
    assert add(ten)(1, 2) == 11


def test_decorator_access_args():
    @decorator
    def return_x(call):
        return call.x

    # no arg
    with pytest.raises(AttributeError): return_x(lambda y: None)(10)

    # pos arg
    assert return_x(lambda x: None)(10) == 10
    with pytest.raises(AttributeError): return_x(lambda x: None)()
    assert return_x(lambda x=11: None)(10) == 10
    assert return_x(lambda x=11: None)() == 11

    # pos-only
    assert return_x(lambda x, /: None)(10) == 10
    with pytest.raises(AttributeError): return_x(lambda x, /: None)()
    assert return_x(lambda x=11, /: None)(10) == 10
    assert return_x(lambda x=11, /: None)() == 11
    # try to pass by name
    with pytest.raises(AttributeError): return_x(lambda x, /: None)(x=10)
    assert return_x(lambda x=11, /: None)(x=10) == 11

    # kw-only
    assert return_x(lambda _, /, *, x: None)(x=10) == 10
    with pytest.raises(AttributeError): return_x(lambda _, /, *, x: None)()
    assert return_x(lambda _, /, *, x=11: None)(x=10) == 10
    assert return_x(lambda _, /, *, x=11: None)() == 11

    # varargs
    assert return_x(lambda *x: None)(1, 2) == (1, 2)
    assert return_x(lambda _, *x: None)(1, 2) == (2,)

    # varkeywords
    assert return_x(lambda **x: None)(a=1, b=2) == {'a': 1, 'b': 2}
    assert return_x(lambda **x: None)(a=1, x=3) == {'a': 1, 'x': 3}  # Not just 3
    assert return_x(lambda a, **x: None)(a=1, b=2) == {'b': 2}
    assert return_x(lambda a, /, **x: None)(a=1, b=2) == {'a': 1, 'b': 2}


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
