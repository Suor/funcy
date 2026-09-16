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

# -- LazyObject becomes the object built by init --
class Client:
    def get(self, key: str) -> int: return 0

@LazyObject
def client() -> Client:
    return Client()
reveal_type(client)  # R: Client
reveal_type(client.get("a"))  # R: int

# -- wrap_prop --
import threading
reveal_type(wrap_prop(threading.Lock()))  # R: (...) -> Any

# -- monkey --
class Target:
    pass

@monkey(Target)
def new_method(self: Target) -> int:
    return 42

# -- Should be errors --
cached_property(42)  # E: not a callable
