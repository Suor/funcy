from functools import wraps
from contextlib import contextmanager


# @contextmanager
# def retry(tries):
#     for attempt in range(tries):
#         yield

def retry(tries, cont=Exception):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(tries):
                try:
                    return func(*args, **kwargs)
                except cont:
                    # Reraise error on last attempt
                    if attempt + 1 == tries:
                        raise
        return wrapper
    return decorator


def repeat(n):
    def decorator(func):
        @wraps(func)
        def wrapper():
            for _ in range(n):
                func()
        return wrapper
    return decorator


def call(func):
    func()


# @call
# @repeat(3)
# def some_func():
#     print 'hi'


import sys
from dis import dis

@contextmanager
def repeat(tries):
    # f = sys._getframe(1)
    # print sys._getframe(1)
    # yield
    # raise StopIteration
    yield


# with repeat(2):
#     print 'bye'

def repeat(n):
    for i in range(n):
        try:
            yield i
        except ZeroDivisionError:
            print '0div'

for x in repeat(3):
    print 'bye', (10 / (2-x))

