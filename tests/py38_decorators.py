import pytest
from funcy.decorators import decorator


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
