import pytest
from funcy.flow import *


def test_silent():
    assert silent(int)(1) == 1
    assert silent(int)('1') == 1
    assert silent(int)('hello') is None


def test_raiser():
    class MyError(Exception):
        pass

    with pytest.raises(MyError): raiser(MyError)()
    with pytest.raises(MyError) as e: raiser(MyError, 'some message')()
    assert e.value.args == ('some message',)

    with pytest.raises(MyError): raiser(MyError('some message'))()
    with pytest.raises(MyError): raiser(MyError)('junk', keyword='junk')


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
