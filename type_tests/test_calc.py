from funcy import memoize, cache, make_lookuper, silent_lookuper

# -- memoize as decorator (no args) --
@memoize
def fib(n: int) -> int:
    return n if n < 2 else fib(n - 1) + fib(n - 2)
reveal_type(fib)  # R: (n: int) -> int

# -- memoize with key_func --
@memoize(key_func=lambda x: x % 10)
def mod_cache(x: int) -> str:
    return str(x)
reveal_type(mod_cache)  # R: (x: int) -> str

# -- cache --
@cache(60)
def cached_fn(x: int) -> str:
    return str(x)
reveal_type(cached_fn)  # R: (x: int) -> str

# -- make_lookuper --
@make_lookuper
def my_lookup() -> dict[str, int]:
    return {"a": 1, "b": 2}
reveal_type(my_lookup)  # R: (...) -> int

# -- silent_lookuper --
@silent_lookuper
def my_silent() -> dict[str, int]:
    return {"a": 1, "b": 2}
reveal_type(my_silent)  # R: (...) -> int | None
