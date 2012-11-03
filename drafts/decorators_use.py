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
def iterate(call):
    for i in range(5): call.func(i)

print iterate.__name__

@iterate
def test(i):
    print 'test', i

test()


@decorator
def retry(call, tries, cont=Exception):
    for attempt in range(tries):
        try:
            return call()
        except cont:
            # Reraise error on last attempt
            if attempt + 1 == tries:
                raise

@decorator
def silent():
    try:
        yield
    except Exception as e:
        return None
