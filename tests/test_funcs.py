from operator import __add__, __sub__
import pytest
from whatever import _

from funcy.cross import map
from funcy.funcs import *


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

def test_curry():
    assert curry(lambda: 42)() == 42
    assert curry(_ * 2)(21) == 42
    assert curry(_ * _)(6)(7) == 42
    assert curry(__add__, 2)(10)(1) == 11
    assert curry(lambda x,y,z: x+y+z)('a')('b')('c') == 'abc'

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


def test_compose():
    double = _ * 2
    inc    = _ + 1
    assert compose()(10) == 10
    assert compose(double)(10) == 20
    assert compose(inc, double)(10) == 21
    assert compose(str, inc, double)(10) == '21'
    assert compose(int, r'\d+')('abc1234xy') == 1234

def test_complement():
    assert complement(identity)(0) is True
    assert complement(identity)([1, 2]) is False

def test_juxt():
    assert juxt(__add__, __sub__)(10, 2) == [12, 8]
    assert map(juxt(_ + 1, _ - 1), [2, 3]) == [[3, 1], [4, 2]]

def test_iffy():
    assert map(iffy(_ % 2, _ * 2, _ / 2), [1,2,3,4]) == [2,1,6,2]
    assert map(iffy(_ % 2, _ * 2), [1,2,3,4]) == [2,2,6,4]
    assert map(iffy(_ * 2), [21, '', None]) == [42, '', None]
    assert map(iffy(_ % 2, _ * 2, None), [1,2,3,4]) == [2, None, 6, None]
