import sys
import pytest
from funcy.decorators import *
from funcy.decorators import arggetter


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


# TODO: replace this with a full version once we drop Python 3.7
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

    # varargs
    assert return_x(lambda *x: None)(1, 2) == (1, 2)
    assert return_x(lambda _, *x: None)(1, 2) == (2,)

    # varkeywords
    assert return_x(lambda **x: None)(a=1, b=2) == {'a': 1, 'b': 2}
    assert return_x(lambda **x: None)(a=1, x=3) == {'a': 1, 'x': 3}  # Not just 3
    assert return_x(lambda a, **x: None)(a=1, b=2) == {'b': 2}


if sys.version_info >= (3, 8):
    pytest.register_assert_rewrite("tests.py38_decorators")
    from .py38_decorators import test_decorator_access_args  # noqa


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


@pytest.mark.parametrize('method_name', ['method', 'class_method'])
@pytest.mark.parametrize('wrapped', [False, True])
def test_decorator_access_bound_method_args(method_name, wrapped):
    @decorator
    def capture(call):
        return call.x, call.y, call.args, call.kwargs

    @decorator
    def passthrough(call):
        return call()

    wrap = passthrough if wrapped else lambda f: f

    class A(object):
        @wrap
        def method(self, x, y=2, *args, **kwargs):
            pass

        @classmethod
        @wrap
        def class_method(cls, x, y=2, *args, **kwargs):
            pass

    wrapped = capture(getattr(A(), method_name))
    assert wrapped(1) == (1, 2, (), {})
    assert wrapped(1, 3, 4, z=5) == (1, 3, (4,), {'z': 5})
    assert wrapped(x=6, y=7) == (6, 7, (), {})


def test_arggetter_bound_method_positional_only():
    # Defining this through exec retains compatibility with Python 3.4-3.7.
    if sys.version_info < (3, 8):
        pytest.skip('positional-only parameters require Python 3.8+')
    namespace = {}
    exec('class A:\n    def method(self, x, /, y=2): pass', namespace)
    method = namespace['A']().method
    get_arg = arggetter(method)
    assert get_arg('x', (1,), {}) == 1
    assert get_arg('y', (1,), {}) == 2
    assert get_arg('y', (1,), {'y': 3}) == 3
    with pytest.raises(TypeError, match='missing required argument'):
        get_arg('x', (), {'x': 1})
