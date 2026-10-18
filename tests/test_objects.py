import sys
import pytest
from funcy.objects import *
from funcy import suppress


### @cached_property

def test_cached_property():
    calls = [0]

    class A(object):
        @cached_property
        def prop(self):
            calls[0] += 1
            return 7

    a = A()
    assert a.prop == 7
    assert a.prop == 7
    assert calls == [1]

    a.prop = 42
    assert a.prop == 42

    del a.prop
    assert a.prop == 7
    assert calls == [2]

def test_cached_property_doc():
    class A(object):
        @cached_property
        def prop(self):
            "prop doc"
            return 7

    assert A.prop.__doc__ == "prop doc"


@pytest.mark.parametrize('value', [7, None, False, 0, []])
def test_cached_readonly(value):
    calls = []

    class A(object):
        @cached_readonly
        def prop(self):
            calls.append(self)
            return value

    a = A()
    assert isinstance(A.prop, cached_readonly)
    assert a.prop is value
    assert a.prop is value
    assert calls == [a]
    with pytest.raises(AttributeError):
        a.prop = 8
    assert a.prop is value
    assert calls == [a]

    b = A()
    assert b.prop is value
    assert calls == [a, b]


def test_wrap_prop():
    calls = []

    # Not using @contextmanager to not make this a decorator
    class Manager:
        def __init__(self, name):
            self.name = name

        def __enter__(self):
            calls.append(self.name)
            return self

        def __exit__(self, *args):
            pass

    class A(object):
        @wrap_prop(Manager('p'))
        @property
        def prop(self):
            return 1

        @wrap_prop(Manager('cp'))
        @cached_property
        def cached_prop(self):
            return 1

    a = A()
    assert a.prop and calls == ['p']
    assert a.prop and calls == ['p', 'p']
    assert a.cached_prop and calls == ['p', 'p', 'cp']
    assert a.cached_prop and calls == ['p', 'p', 'cp']

    # Wrap __set__ for data props
    a = A()
    calls[:] = []
    with suppress(AttributeError):
        a.prop = 2
    assert calls == ['p']

    # Do not wrap __set__ for non-data props
    a.cached_property = 2
    assert calls == ['p']


@pytest.mark.parametrize('raises', [False, True])
def test_wrap_prop_delete(raises):
    calls = []

    class Manager:
        def __enter__(self):
            calls.append('enter')

        def __exit__(self, exc_type, exc_value, traceback):
            calls.append(('exit', exc_type))

    class A:
        def __init__(self):
            self.value = 1

        @property
        def prop(self):
            return self.value

        @prop.deleter
        def prop(self):
            calls.append('delete')
            if raises:
                raise ValueError('cannot delete')
            del self.value

        prop = wrap_prop(Manager())(prop)

    a = A()
    if raises:
        with pytest.raises(ValueError, match='cannot delete'):
            del a.prop
        assert a.value == 1
        assert calls == ['enter', 'delete', ('exit', ValueError)]
    else:
        del a.prop
        assert not hasattr(a, 'value')
        assert calls == ['enter', 'delete', ('exit', None)]


def test_wrap_prop_delete_cached_property():
    calls = []

    class A:
        @wrap_prop(suppress())
        @cached_property
        def prop(self):
            calls.append('get')
            return len(calls)

    a = A()
    assert a.prop == 1
    del a.prop
    assert a.prop == 2
    assert calls == ['get', 'get']


### Monkey tests

def test_monkey():
    class A(object):
        def f(self):
            return 7

    @monkey(A)
    def f(self):
        return f.original(self) * 6

    assert A().f() == 42


def test_monkey_with_name():
    class A(object):
        def f(self):
            return 7

    @monkey(A, name='f')
    def g(self):
        return g.original(self) * 6

    assert A().f() == 42


def test_monkey_property():
    class A(object):
        pass

    @monkey(A)
    @property
    def prop(self):
        return 42

    assert A().prop == 42


def f(x):
    return x

def test_monkey_module():
    this_module = sys.modules[__name__]

    @monkey(this_module)
    def f(x):
        return f.original(x) * 2

    assert f(21) == 42


def test_lazy_object():
    class A(object):
        x = 42
        def __init__(self):
            log.append('init')

    log = []
    a = LazyObject(A)
    assert not log
    assert a.x == 42


@pytest.mark.parametrize('fail_first', [False, True])
def test_wrap_prop_recreates_generator_contexts(fail_first):
    from contextlib import contextmanager

    events = []

    @contextmanager
    def transaction():
        events.append('enter')
        try:
            yield
        finally:
            events.append('exit')

    class Record:
        value = 1

        @property
        def field(self):
            if self.value is None:
                raise ValueError('missing value')
            return self.value

        @field.setter
        def field(self, value):
            self.value = value

        @field.deleter
        def field(self):
            self.value = None

        field = wrap_prop(transaction())(field)

    record = Record()
    if fail_first:
        record.value = None
        with pytest.raises(ValueError, match='missing value'):
            _ = record.field
        record.value = 1

    assert record.field == 1
    assert record.field == 1
    record.field = 2
    assert record.field == 2
    del record.field
    record.field = 3
    assert record.field == 3
    assert events == ['enter', 'exit'] * (8 if fail_first else 7)
