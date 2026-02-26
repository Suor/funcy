from funcy import cached_property, cached_readonly, wrap_prop, monkey, LazyObject

# -- cached_property --
class MyClass:
    @cached_property
    def value(self) -> int:
        return 42

    @cached_readonly
    def ro_value(self) -> str:
        return "hello"

obj = MyClass()
reveal_type(obj.value)  # R: int
reveal_type(obj.ro_value)  # R: str

# -- LazyObject --
lazy = LazyObject(lambda: [1, 2, 3])
reveal_type(lazy)  # R: LazyObject

# -- wrap_prop --
# FIX: what is this, should use real prop, and it's not Any, prop type is not changed
reveal_type(wrap_prop(None))  # R: (...) -> Any

# -- monkey --
class Target:
    pass

@monkey(Target)
def new_method(self: Target) -> int:
    return 42

# -- Should be errors --
cached_property(42)  # E: not a callable
