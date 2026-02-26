from funcy import (
    identity, constantly, caller,
    rpartial, func_partial,
    curry, rcurry, autocurry,
    iffy, compose, rcompose, complement, juxt, ljuxt,
)

# -- identity preserves type --
x: int = 42
s: str = "hello"
reveal_type(identity(x))  # R: int  # XFAIL[ty]: Literal narrowing
reveal_type(identity(s))  # R: str  # XFAIL[ty]: Literal narrowing

# -- constantly returns a function that always returns x --
f = constantly(x)
reveal_type(f)  # R: (...) -> int  # XFAIL[ty]: Literal narrowing
reveal_type(f("anything"))  # R: int  # XFAIL[ty]: Literal narrowing

# -- caller --
def add_int(a: int, b: int) -> int: return a + b
reveal_type(caller(1, 2)(add_int))  # R: int

# -- rpartial / func_partial preserve return type --
def add(a: int, b: int) -> int: return a + b
reveal_type(rpartial(add, 1))  # R: (...) -> int
reveal_type(func_partial(add, 1))  # R: (...) -> int

# FIX: can do better than Any
# -- curry / rcurry --
reveal_type(curry(add))  # R: (...) -> Any
reveal_type(rcurry(add))  # R: (...) -> Any

# -- autocurry preserves function signature --
reveal_type(autocurry(add))  # R: (a: int, b: int) -> int

# -- iffy --
def int_to_str(x: int) -> str: return str(x)
reveal_type(iffy(bool, int_to_str))  # R: (...) -> Any

# -- compose / rcompose --
reveal_type(compose(int_to_str, abs))  # R: (...) -> Any
reveal_type(rcompose(abs, int_to_str))  # R: (...) -> Any

# -- complement --
reveal_type(complement(bool))  # R: (...) -> bool

# -- juxt / ljuxt --
reveal_type(juxt(int_to_str, abs))  # R: (...) -> Iterator[Any]
reveal_type(ljuxt(int_to_str, abs))  # R: (...) -> list[Any]
