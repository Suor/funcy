from typing import cast
from funcy import decorator, wraps
from funcy.typing import DecoReturning

# -- simple decorator preserves function signature --
@decorator
def my_deco(call):
    return call()

@my_deco
def greet(name: str) -> str:
    return f"hello {name}"

reveal_type(greet)  # R: (name: str) -> str

# -- decorator factory preserves function signature --
# Kwonly params: only those factories may also be used bare, without a call
@decorator
def with_tag(call, *, tag="div"):
    return call()

@with_tag(tag="span")
def render(text: str) -> str:
    return text

reveal_type(render)  # R: (text: str) -> str

# -- decorator factory used without args preserves function signature --
@with_tag
def render2(text: str) -> str:
    return text

reveal_type(render2)  # R: (text: str) -> str

# -- decorator factory args are checked --
@decorator
def retry_n(call, n: int):
    return call()

@retry_n(3)
def flaky() -> int:
    return 1

reveal_type(flaky)  # R: () -> int

# -- returning= declares what the decorated function returns --
@decorator(returning=str)
def to_str(call):
    return str(call())

@to_str
def num() -> int:
    return 1

reveal_type(num)  # R: () -> str

# -- returning= on a factory: return type and its own args --
@decorator(returning=str)
def tagged(call, *, tag: str = "div"):
    return f"<{tag}>{call()}</{tag}>"

@tagged(tag="span")
def render3(text: str) -> int:
    return 1

reveal_type(render3)  # R: (text: str) -> str

@tagged
def render4(text: str) -> int:
    return 1

reveal_type(render4)  # R: (text: str) -> str

# -- returning= a generic alias, None or a union --
@decorator(returning=list[int])
def to_list(call):
    return [1]

@to_list
def nums() -> int:
    return 1

reveal_type(nums)  # R: () -> list[int]

@decorator(returning=None)
def to_none(call):
    return None

@to_none
def nothing() -> int:
    return 1

reveal_type(nothing)  # R: () -> None

@decorator(returning=str | None)
def maybe_str(call):
    return None

@maybe_str
def maybe() -> int:
    return 1

reveal_type(maybe)  # R: () -> str | None

# -- DecoReturning: same, for a decorator you can't annotate --
casted = cast(DecoReturning[str | None], my_deco)

@casted
def num2(x: int) -> int:
    return x

reveal_type(num2)  # R: (x: int) -> str | None

# -- a deco filling an arg in: call(conn) appends, the param stays in the signature --
class Conn: pass

with_conn = cast(DecoReturning[int], my_deco)

@with_conn
def query(sql: str, conn: Conn) -> str:
    return sql

reveal_type(query)  # R: (sql: str, conn: Conn) -> int

# -- wraps preserves wrapper type --
def original(x: int, y: str) -> bool: return True
def wrapper(*args: object, **kwargs: object) -> bool:
    return original(*args, **kwargs)  # type: ignore[arg-type]  # ty: ignore[invalid-argument-type]
wrapped = wraps(original)(wrapper)
reveal_type(wrapped)  # R: (x: int, y: str) -> bool

# -- Should be errors --
retry_n("three")  # E: wrong decorator arg type
tagged(taggg="span")  # E: unknown decorator arg
tagged(tag=42)  # E: wrong decorator arg type
query("select 1", "extra")  # E: the decorator fills the second arg in
