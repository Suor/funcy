from funcy import memoize, cache, make_lookuper, silent_lookuper

# -- memoize as decorator (no args) --
@memoize
def fib(n: int) -> int:
    return n if n < 2 else fib(n - 1) + fib(n - 2)
reveal_type(fib(10))  # R: int
# memoize exposes invalidate / invalidate_all / memory
fib.invalidate(1)
fib.invalidate_all()
reveal_type(fib.memory)  # R: dict[Any, Any]

# -- memoize with key_func --
@memoize(key_func=lambda x: x % 10)
def mod_cache(x: int) -> str:
    return str(x)
reveal_type(mod_cache(1))  # R: str

# -- memoize on a method binds self --
class Repo:
    @memoize
    def get(self, key: int) -> str:
        return str(key)
reveal_type(Repo().get(1))  # R: str  # XFAIL[pyrefly]: can't match self-typed __get__ overload

# -- cache --
@cache(60)
def cached_fn(x: int) -> str:
    return str(x)
reveal_type(cached_fn(1))  # R: str
cached_fn.invalidate(1)

# -- make_lookuper --
@make_lookuper
def my_lookup() -> dict[str, int]:
    return {"a": 1, "b": 2}
reveal_type(my_lookup)  # R: (str) -> int

# make_lookuper with args builds a lookuper per args
@make_lookuper
def by_lang(lang: str) -> dict[int, str]:
    return {1: "one"}
reveal_type(by_lang("en")(1))  # R: str

# -- silent_lookuper --
@silent_lookuper
def my_silent() -> dict[str, int]:
    return {"a": 1, "b": 2}
reveal_type(my_silent)  # R: (str) -> int | None

# -- Should be errors --
fib("x")  # E: wrong arg type
fib.invalidate("x")  # E: invalidate takes the same args
my_lookup(1)  # E: wrong key type
