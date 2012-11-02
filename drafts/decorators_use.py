from functools import wraps

from funcy.decorators import decorator, call_decorator

@decorator
def repeat(n):
    print "> Start %d iterations" % n
    for i in range(n):
        yield
    print '> Done'

@repeat(2)
def test():
    print 'test'

test()


@decorator
def iterate(func):
    for i in range(5): func(i)

print iterate.__name__

@iterate()
def test(i):
    print 'test', i

test()
