from operator import __add__, __sub__
from whatever import _

from funcy.funcs import *


def test_caller():
    assert caller([1, 2])(sum) == 3

def test_partial():
    assert partial(__add__, 10)(1) == 11
    assert partial(__add__, 'abra')('cadabra') == 'abracadabra'

    merge = lambda a=None, b=None: a + b
    assert partial(merge, a='abra')(b='cadabra') == 'abracadabra'
    assert partial(merge, b='abra')(a='cadabra') == 'cadabraabra'

def test_compose():
    double = _ * 2
    inc    = _ + 1
    assert compose(inc, double)(10) == 21
    assert compose(str, inc, double)(10) == '21'

def test_complement():
    assert complement(identity)(0) == True
    assert complement(identity)([1, 2]) == False

def test_juxt():
    assert juxt(__add__, __sub__)(10, 2) == [12, 8]
