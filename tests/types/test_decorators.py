import pytest
from funcy import decorator


@pytest.mark.mypy_testing
def basic():
    @decorator
    def inc(call) -> int:
        return call() + 1

    inc()
    inc(1) # ER: No overload variant .* matches argument type "int"  [call-overload]

    inc_id = inc(lambda x: x)
    reveal_type(inc_id(10))  # R: builtins.int


@pytest.mark.mypy_testing
def preserve_signature():
    @decorator
    def inc(call):
        return call()

    @inc
    def foo(s: str, n: int) -> str:
        return s * n

    def foo_real(s: str, n: int) -> str:
        return s * n

    reveal_type(inc)
    reveal_type(foo)
    foo('a', 3)
    foo(3, 'a')
    foo_real(3, 'a')
    reveal_type(foo('a', 3))  # R: builtins.int
