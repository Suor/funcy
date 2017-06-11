import re

from funcy.debug import *
from funcy.flow import silent


def test_tap():
    assert capture(tap, 42) == '42\n'
    assert capture(tap, 42, label='Life and ...') == 'Life and ...: 42\n'


def test_log_calls():
    log = []

    @log_calls(log.append)
    def f(x, y):
        return x + y

    f(1, 2)
    f('a', 'b')
    assert log == [
        "Call f(1, 2)",
        "-> 3 from f(1, 2)",
        "Call f('a', 'b')",
        "-> 'ab' from f('a', 'b')",
    ]

def test_print_calls():
    def f(x, y):
        return x + y

    capture(print_calls(f), 1, 2) == "Call f(1, 2)\n-> 3 from f(1, 2)\n",
    capture(print_calls()(f), 1, 2) == "Call f(1, 2)\n-> 3 from f(1, 2)\n",


def test_log_calls_raise():
    log = []

    @log_calls(log.append, stack=False)
    def f():
        raise Exception('something bad')

    silent(f)()
    assert log == [
        "Call f()",
        "-> Exception: something bad raised in f()",
    ]


def test_log_errors():
    log = []

    @log_errors(log.append)
    def f(x):
        return 1 / x

    silent(f)(1)
    silent(f)(0)
    assert len(log) == 1
    assert log[0].startswith('Traceback')
    assert re.search(r'ZeroDivisionError: .*\n    raised in f\(0\)$', log[0])


def test_log_errors_manager():
    log = []
    try:
        with log_errors(log.append):
            1 / 0
    except ZeroDivisionError:
        pass
    try:
        with log_errors(log.append, 'name check', stack=False):
            hey
    except NameError:
        pass
    assert len(log) == 2
    print(log)
    assert log[0].startswith('Traceback')
    assert re.search(r'ZeroDivisionError: .* zero\s*$', log[0])
    assert not log[1].startswith('Traceback')
    assert re.search(r"NameError: (global )?name 'hey' is not defined raised in name check", log[1])


def test_print_errors():
    def error():
        1 / 0

    f = print_errors(error)
    assert f.__name__ == 'error'
    assert 'ZeroDivisionError' in capture(silent(f))

    g = print_errors(stack=False)(error)
    assert g.__name__ == 'error'
    assert capture(silent(g)).startswith('ZeroDivisionError')


def test_print_errors_manager():
    @silent
    def f():
        with print_errors:
            1 / 0

    assert 'ZeroDivisionError' in capture(f)
    assert capture(f).startswith('Traceback')


def test_print_errors_recursion():
    @silent
    @print_errors(stack=False)
    def f(n):
        if n:
            f(0)
            1 / 0

    assert 'f(1)' in capture(f, 1)


def test_log_durations(monkeypatch):
    timestamps = iter([0, 0.01, 1, 1.01])
    monkeypatch.setattr('time.time', lambda: next(timestamps))
    log = []

    @log_durations(log.append)
    def f():
        pass

    f()
    with log_durations(log.append, 'hello'):
        pass

    for line in log:
        m = re.search(r'^\s*(\d+\.\d+) ms in (f\(\)|hello)$', line)
        assert m
        assert float(m.group(1)) == 10


def test_log_iter_dirations():
    log = []
    for item in log_iter_durations([1, 2], log.append):
        pass
    assert len(log) == 2


### An utility to capture stdout

import sys
try:
    from cStringIO import StringIO
except ImportError:
    from io import StringIO

def capture(command, *args, **kwargs):
    out, sys.stdout = sys.stdout, StringIO()
    try:
        command(*args, **kwargs)
        sys.stdout.seek(0)
        return sys.stdout.read()
    finally:
        sys.stdout = out
