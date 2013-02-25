from functools import wraps


def cached_property(func):
    @property
    @wraps(func)
    def wrapper(self):
        attname = '_' + func.__name__
        if not hasattr(self, attname):
            setattr(self, attname, func(self))
        return getattr(self, attname)
    return wrapper
