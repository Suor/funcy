import pytest
from funcy.flow import *


def test_silent():
    assert silent(int)(1) == 1
    assert silent(int)('1') == 1
    assert silent(int)('hello') is None

    assert silent(str.upper)('hello') == 'HELLO'


class MyError(Exception):
    pass


def test_ignore():
    assert ignore(Exception)(raiser(Exception))() is None
    assert ignore(Exception)(raiser(MyError))() is None
    assert ignore((TypeError, MyError))(raiser(MyError))() is None

    with pytest.raises(TypeError):
        ignore(MyError)(raiser(TypeError))()

    assert ignore(MyError, default=42)(raiser(MyError))() == 42


def test_raiser():
    with pytest.raises(Exception) as e: raiser()()
    assert e.type is Exception

    with pytest.raises(MyError): raiser(MyError)()
    with pytest.raises(MyError) as e: raiser(MyError, 'some message')()
    assert e.value.args == ('some message',)

    with pytest.raises(MyError): raiser(MyError('some message'))()
    with pytest.raises(MyError): raiser(MyError)('junk', keyword='junk')


def test_suppress():
    with suppress(Exception):
        raise Exception
    with suppress(Exception):
        raise MyError

    with pytest.raises(TypeError):
        with suppress(MyError):
            raise TypeError

    with suppress(TypeError, MyError):
        raise MyError


def test_retry():
    calls = []

    def failing(n=1):
        if len(calls) < n:
            calls.append(1)
            raise MyError
        return 1

    with pytest.raises(MyError): failing()
    calls = []
    assert retry(2, MyError)(failing)() == 1
    calls = []
    with pytest.raises(MyError): retry(2, MyError)(failing)(2)


def test_fallback():
    assert fallback(raiser(), lambda: 1) == 1
    with pytest.raises(Exception): fallback((raiser(), MyError), lambda: 1)
    assert fallback((raiser(MyError), MyError), lambda: 1) == 1


def test_limit_error_rate():
    calls = []

    @limit_error_rate(2, 60, MyError)
    def limited(x):
        calls.append(x)
        raise TypeError

    with pytest.raises(TypeError): limited(1)
    with pytest.raises(TypeError): limited(2)
    with pytest.raises(MyError): limited(3)
    assert calls == [1, 2]


def test_post_processing():
    @post_processing(max)
    def my_max(l):
        return l

    assert my_max([1, 3, 2]) == 3


def test_collecting():
    @collecting
    def doubles(l):
        for i in l:
            yield i * 2

    assert doubles([1, 2]) == [2, 4]


def test_once():
    calls = []

    @once
    def call(n):
        calls.append(n)
        return n

    call(1)
    call(2)
    assert calls == [1]


def test_once_per():
    calls = []

    @once_per('n')
    def call(n):
        calls.append(n)
        return n

    call(1)
    call(2)
    call(1)
    assert calls == [1, 2]

