import pytest
from funcy.funcs import autocurry


def test_autocurry_posonly():
    at = autocurry(lambda a, /, b: (a, b))
    assert at(1)(b=2) == (1, 2)
    assert at(b=2)(1) == (1, 2)
    with pytest.raises(TypeError): at(a=1)(b=2)

    at = autocurry(lambda a, /, **kw: (a, kw))
    assert at(a=2)(1) == (1, {'a': 2})

    at = autocurry(lambda a=1, /, *, b: (a, b))
    assert at(b=2) == (1, 2)
    assert at(0)(b=3) == (0, 3)
