from operator import __add__, __sub__
import sys
import pytest
from whatever import _

from funcy import lmap, merge_with
from funcy.funcs import *
from funcy.seqs import keep


def test_caller():
    assert caller([1, 2])(sum) == 3

def test_constantly():
    assert constantly(42)() == 42
    assert constantly(42)('hi', 'there', volume='shout') == 42

def test_partial():
    assert partial(__add__, 10)(1) == 11
    assert partial(__add__, 'abra')('cadabra') == 'abracadabra'

    merge = lambda a=None, b=None: a + b
    assert partial(merge, a='abra')(b='cadabra') == 'abracadabra'
    assert partial(merge, b='abra')(a='cadabra') == 'cadabraabra'

def test_func_partial():
    class A(object):
        f = func_partial(lambda x, self: x + 1, 10)

    assert A().f() == 11

def test_rpartial():
    assert rpartial(__sub__, 10)(1) == -9
    assert rpartial(pow, 2, 85)(10) == 15

    merge = lambda a, b, c='bra': a + b + c
    assert rpartial(merge, a='abra')(b='cada') == 'abracadabra'
    assert rpartial(merge, 'cada', c='fancy')('abra', c='funcy') == 'abracadafuncy'

def test_curry():
    assert curry(lambda: 42)() == 42
    assert curry(_ * 2)(21) == 42
    assert curry(_ * _)(6)(7) == 42
    assert curry(__add__, 2)(10)(1) == 11
    assert curry(__add__)(10)(1) == 11  # Introspect builtin
    assert curry(lambda x,y,z: x+y+z)('a')('b')('c') == 'abc'

def test_curry_funcy():
    # curry() doesn't handle required star args,
    # but we can code inspection for funcy utils.
    assert curry(lmap)(int)('123') == [1, 2, 3]
    assert curry(merge_with)(sum)({1: 1}) == {1: 1}

def test_rcurry():
    assert rcurry(__sub__, 2)(10)(1) == -9
    assert rcurry(lambda x,y,z: x+y+z)('a')('b')('c') == 'cba'
    assert rcurry(str.endswith, 2)('c')('abc') is True

def test_autocurry():
    at = autocurry(lambda a, b, c: (a, b, c))

    assert at(1)(2)(3) == (1, 2, 3)
    assert at(1, 2)(3) == (1, 2, 3)
    assert at(1)(2, 3) == (1, 2, 3)
    assert at(1, 2, 3) == (1, 2, 3)
    with pytest.raises(TypeError): at(1, 2, 3, 4)
    with pytest.raises(TypeError): at(1, 2)(3, 4)

    assert at(a=1, b=2, c=3) == (1, 2, 3)
    assert at(c=3)(1, 2) == (1, 2, 3)
    assert at(c=4)(c=3)(1, 2) == (1, 2, 3)
    with pytest.raises(TypeError): at(a=1)(1, 2, 3)

def test_autocurry_named():
    at = autocurry(lambda a, b, c=9: (a, b, c))

    assert at(1)(2) == (1, 2, 9)
    assert at(1)(2, 3) == (1, 2, 3)
    assert at(a=1)(b=2) == (1, 2, 9)
    assert at(c=3)(1)(2) == (1, 2, 3)
    assert at(c=3, a=1, b=2) == (1, 2, 3)

    with pytest.raises(TypeError): at(b=2, c=9, d=42)(1)

def test_autocurry_kwargs():
    at = autocurry(lambda a, b, **kw: (a, b, kw))
    assert at(1, 2) == (1, 2, {})
    assert at(1)(c=9)(2) == (1, 2, {'c': 9})
    assert at(c=9, d=5)(e=7)(1, 2) == (1, 2, {'c': 9, 'd': 5, 'e': 7})

    at = autocurry(lambda a, b=2, c=3: (a, b, c))
    assert at(1) == (1, 2, 3)
    assert at(a=1) == (1, 2, 3)
    assert at(c=9)(1) == (1, 2, 9)
    assert at(b=3, c=9)(1) == (1, 3, 9)
    with pytest.raises(TypeError): at(b=2, d=3, e=4)(a=1, c=1)


def test_autocurry_kwonly():
    at = autocurry(lambda a, *, b: (a, b))
    assert at(1, b=2) == (1, 2)
    assert at(1)(b=2) == (1, 2)
    assert at(b=2)(1) == (1, 2)

    at = autocurry(lambda a, *, b=10: (a, b))
    assert at(1) == (1, 10)
    assert at(b=2)(1) == (1, 2)

    at = autocurry(lambda a=1, *, b: (a, b))
    assert at(b=2) == (1, 2)
    assert at(0)(b=2) == (0, 2)

    at = autocurry(lambda *, a=1, b: (a, b))
    assert at(b=2) == (1, 2)
    assert at(a=0)(b=2) == (0, 2)

# TODO: move this here once we drop Python 3.7
if sys.version_info >= (3, 8):
    pytest.register_assert_rewrite("tests.py38_funcs")
    from .py38_funcs import test_autocurry_posonly  # noqa


def test_autocurry_builtin():
    assert autocurry(complex)(imag=1)(0) == 1j
    assert autocurry(lmap)(_ + 1)([1, 2]) == [2, 3]
    assert autocurry(int)(base=12)('100') == 144
    if sys.version_info >= (3, 7):
        assert autocurry(str.split)(sep='_')('a_1') == ['a', '1']

def test_autocurry_hard():
    def required_star(f, *seqs):
        return lmap(f, *seqs)

    assert autocurry(required_star)(__add__)('12', 'ab') == ['1a', '2b']

    _iter = autocurry(iter)
    assert list(_iter([1, 2])) == [1, 2]
    assert list(_iter([0, 1, 2].pop)(0)) == [2, 1]

    _keep = autocurry(keep)
    assert list(_keep('01')) == ['0', '1']
    assert list(_keep(int)('01')) == [1]
    with pytest.raises(TypeError): _keep(1, 2, 3)

def test_autocurry_class():
    class A:
        def __init__(self, x, y=0):
            self.x, self.y = x, y

    assert autocurry(A)(1).__dict__ == {'x': 1, 'y': 0}

    class B: pass
    autocurry(B)()

    class I(int): pass
    assert autocurry(int)(base=12)('100') == 144

def test_autocurry_docstring():
    @autocurry
    def f(a, b):
        'docstring'

    assert f.__doc__ == 'docstring'


def test_compose():
    double = _ * 2
    inc    = _ + 1
    assert compose()(10) == 10
    assert compose(double)(10) == 20
    assert compose(inc, double)(10) == 21
    assert compose(str, inc, double)(10) == '21'
    assert compose(int, r'\d+')('abc1234xy') == 1234

def test_rcompose():
    double = _ * 2
    inc    = _ + 1
    assert rcompose()(10) == 10
    assert rcompose(double)(10) == 20
    assert rcompose(inc, double)(10) == 22
    assert rcompose(double, inc)(10) == 21

def test_complement():
    assert complement(identity)(0) is True
    assert complement(identity)([1, 2]) is False

def test_juxt():
    assert ljuxt(__add__, __sub__)(10, 2) == [12, 8]
    assert lmap(ljuxt(_ + 1, _ - 1), [2, 3]) == [[3, 1], [4, 2]]

def test_iffy():
    assert lmap(iffy(_ % 2, _ * 2, _ / 2), [1,2,3,4]) == [2,1,6,2]
    assert lmap(iffy(_ % 2, _ * 2), [1,2,3,4]) == [2,2,6,4]
    assert lmap(iffy(_ * 2), [21, '', None]) == [42, '', None]
    assert lmap(iffy(_ % 2, _ * 2, None), [1,2,3,4]) == [2, None, 6, None]
    assert lmap(iffy(_ + 1, default=1), [1, None, 2]) == [2, 1, 3]
    assert lmap(iffy(set([1,4,5]), _ * 2), [1, 2, 3, 4]) == [2, 2, 3, 8]
    assert lmap(iffy(r'\d+', str.upper), ['a2', 'c']) == ['A2', 'c']
    assert lmap(iffy(set([1,4,5])), [False, 2, 4]) == [False, False, True]
    assert lmap(iffy(None), [False, 2, 3, 4]) == [False, 2, 3, 4]
