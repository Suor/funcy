from funcy import decorator, wraps

# -- simple decorator preserves function signature --
@decorator
def my_deco(call):
    return call()

@my_deco
def greet(name: str) -> str:
    return f"hello {name}"

reveal_type(greet)  # R: (name: str) -> str

# -- decorator factory (multi-arg) preserves function signature --
@decorator
def with_tag(call, tag="div"):
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

# -- wraps preserves wrapper type --
def original(x: int, y: str) -> bool: return True
def wrapper(*args: object, **kwargs: object) -> bool:
    return original(*args, **kwargs)  # type: ignore[arg-type]
wrapped = wraps(original)(wrapper)
reveal_type(wrapped)  # R: (x: int, y: str) -> bool
