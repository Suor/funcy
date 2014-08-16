# -*- coding: utf-8 -*-
import gc, time, sys, inspect
from functools import wraps

sys.path.insert(0, '/home/suor/projects/funcy')
from funcy import decorator


@decorator
def empty_funcy(call):
    return call()

def empty_old_school(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

import wrapt

@wrapt.decorator
def empty_wrapt(wrapped, instance, args, kwargs):
    return wrapped(*args, **kwargs)

# getx decorators

@decorator
def getx_funcy(call):
    return call.x

def getx_old_school(func):
    @wraps(func)
    def wrapper(x):
        return x
    return wrapper

@wrapt.decorator
def getx_wrapt(wrapped, instance, args, kwargs):
    if 'x' in kwargs:
        return kwargs[x]
    else:
        return args[0]


def undecorated():
    return sum(range(20))

funcy_decorated = empty_funcy(undecorated)
funcy_decorated.__name__ = 'funcy_decorated'

old_school_decorated = empty_old_school(undecorated)
old_school_decorated.__name__ = 'old_school_decorated'

@empty_wrapt
def wrapt_decorated():
    return sum(range(20))


def undecorated_getx(x):
    return x

funcy_getx = getx_funcy(undecorated_getx)
funcy_getx.__name__ = 'funcy_getx'

old_school_getx = getx_old_school(undecorated_getx)
old_school_getx.__name__ = 'old_school_getx'

@getx_wrapt
def wrapt_getx(x):
    return x


def bench_test(test, *args):
    print 'Benchmarking %s ...' % test.__name__
    real, clock = 0, 0
    n = 1
    while real < 1:
        gc.disable()
        real, clock = bench_once(test, n, *args)
        gc.enable()
        n *= 2

    n /= 2
    # min_time = min(r[0] for r in l)
    # min_clock = min(r[1] for r in l)

    # return total * 2 / n # Or use normalized?
    # return min_clock
    print '%d loops, time %s, clock %s' % (n, format_time(real/n), format_time(clock/n))

def bench_once(test, n, *args):
    start = time.time()
    clock = time.clock()
    for _ in xrange(n):
        test(*args)
    return (time.time() - start, time.clock() - clock)

def format_time(sec):
    return '%07d ns' % (sec * 1e9)

from profilehooks import profile


# def make_decorator(deco, dargs=(), dkwargs={}):
#     def _decorator(func):
#         def wrapper(*args, **kwargs):
#             call = Call(func, args, kwargs)
#             return deco(call, *dargs, **dkwargs)
#         return wraps(func)(wrapper)
#     return _decorator

WRAPPER_TEMPLATE = """
def __wrapper_fab(__deco, __func):
    def __wrapper{spec}:
        __call = lambda: __func{spec}
        __call._func = __func
        __call._args = __func
        __call._kwargs = __func
{assigns}
        return __deco(__call)
    return __wrapper
""".strip()

def compile_template(func):
    try:
        spec = inspect.getargspec(func)
    except TypeError:
        spec = ArgSpec((), 'args', 'kwargs', None)

    # Slicing with [1:-1] to get rid of parentheses
    spec_str = inspect.formatargspec(*spec)

    assigns = '\n'.join("        __call.{0} = {0}".format(arg) for arg in spec.args)
    func_str = WRAPPER_TEMPLATE.format(name=func.__name__, spec=spec_str, assigns=assigns)

    env = {}
    # print func_str
    exec func_str in env
    return env['__wrapper_fab']

def dec2(deco):
    def _decorator(func):
        template = compile_template(func)
        return wraps(func)(template(deco, func))
    return wraps(deco)(_decorator)

@dec2
def empty_dec2(call):
    return call()

dec2_decorated = empty_dec2(undecorated)
dec2_decorated.__name__ = 'dec2_decorated'

@dec2
def getx_dec2(call):
    return call.x

dec2_getx = getx_dec2(undecorated_getx)
dec2_getx.__name__ = 'dec2_getx'

# def undecorated(x, y=100):
#     return x * y

# dec2 = decorator2(undecorated)
# print dec2(42)
# print dec2.__name__
# print inspect.getargspec(dec2)

# print dec2_getx(42)

# bench_test(undecorated)
# bench_test(old_school_decorated)
# bench_test(funcy_decorated)
# bench_test(wrapt_decorated)
# bench_test(dec2_decorated)

# bench_test(undecorated_getx, 42)
# bench_test(old_school_getx, 42)
# bench_test(funcy_getx, 42)
# bench_test(wrapt_getx, 42)
# bench_test(dec2_getx, 42)

bench_test(empty_old_school, undecorated)
bench_test(empty_funcy, undecorated)
bench_test(empty_wrapt, undecorated)
bench_test(empty_dec2, undecorated)
