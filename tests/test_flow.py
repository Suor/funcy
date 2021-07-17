from datetime import timedelta
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

    with pytest.raises(Exception, match="text") as e: raiser("text")()
    assert e.type is Exception

    with pytest.raises(MyError):
        raiser(MyError)()
    with pytest.raises(MyError, match="some message"):
        raiser(MyError('some message'))()
    with pytest.raises(MyError, match="some message") as e:
        raiser(MyError, 'some message')()

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


def test_reraise():
    @reraise((TypeError, ValueError), MyError)
    def erry(e):
        raise e

    with pytest.raises(MyError): erry(TypeError)
    with pytest.raises(MyError): erry(ValueError)

    with pytest.raises(MyError):
        with reraise(ValueError, MyError):
            raise ValueError

    with pytest.raises(TypeError):
        with reraise(ValueError, MyError):
            raise TypeError

    with pytest.raises(MyError, match="heyhey"):
        with reraise(ValueError, lambda e: MyError(str(e) * 2)):
            raise ValueError("hey")


def test_retry():
    with pytest.raises(MyError):
        _make_failing()()
    assert retry(2, MyError)(_make_failing())() == 1

    with pytest.raises(MyError):
        retry(2, MyError)(_make_failing(n=2))()


def test_retry_timeout(monkeypatch):
    timeouts = []
    monkeypatch.setattr('time.sleep', timeouts.append)

    def failing():
        raise MyError

    # sleep only between tries, so retry is 11, but sleep summary is ~0.1 sec
    del timeouts[:]
    with pytest.raises(MyError):
        retry(11, MyError, timeout=1)(failing)()
    assert timeouts == [1] * 10

    # exponential timeout
    del timeouts[:]
    with pytest.raises(MyError):
        retry(4, MyError, timeout=lambda a: 2 ** a)(failing)()
    assert timeouts == [1, 2, 4]


def test_retry_many_errors():
    assert retry(2, (MyError, RuntimeError))(_make_failing())() == 1
    assert retry(2, [MyError, RuntimeError])(_make_failing())() == 1


def test_retry_filter():
    error_pred = lambda e: 'x' in str(e)
    retry_deco = retry(2, MyError, filter_errors=error_pred)

    assert retry_deco(_make_failing(e=MyError('x')))() == 1
    with pytest.raises(MyError):
        retry_deco(_make_failing())()


def _make_failing(n=1, e=MyError):
    calls = []

    def failing():
        if len(calls) < n:
            calls.append(1)
            raise e
        return 1

    return failing


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


@pytest.mark.parametrize('typ',
    [pytest.param(int, id='int'), pytest.param(lambda s: timedelta(seconds=s), id='timedelta')])
def test_throttle(monkeypatch, typ):
    timestamps = iter([0, 0.01, 1, 1.000025])
    monkeypatch.setattr('time.time', lambda: next(timestamps))

    calls = []

    @throttle(typ(1))
    def throttled(x):
        calls.append(x)

    throttled(1)
    throttled(2)
    throttled(3)
    throttled(4)
    assert calls == [1, 3]


def test_throttle_class():
    class A:
        def foo(self):
            return 42

    a = A()
    assert throttle(1)(a.foo)() == 42


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
    def call(n, x=None):
        calls.append(n)
        return n

    call(1)
    call(2)
    call(1, 42)
    assert calls == [1, 2]


def test_once_per_args():
    calls = []

    @once_per_args
    def call(n, x=None):
        calls.append(n)
        return n

    call(1)
    call(2)
    call(1, 42)
    assert calls == [1, 2, 1]
    call(1)
    assert calls == [1, 2, 1]


def test_wrap_with():
    calls = []

    # Not using @contextmanager to not make this a decorator
    class Manager:
        def __enter__(self):
            calls.append(1)
            return self

        def __exit__(self, *args):
            pass

    @wrap_with(Manager())
    def calc():
        pass

    calc()
    assert calls == [1]
