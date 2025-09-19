from typing import assert_type, Callable
from funcy import decorator


@decorator
def inc(call):
    return call() + 1

inc()
inc(1)
inc(1, 2)

reveal_type(inc)
assert_type(inc, Callable)
