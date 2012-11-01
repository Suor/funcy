from functools import wraps

from funcy.decorators import decorator, call_decorator


@call_decorator
def silent(call):
    try:
        return call()
    except Exception as e:
        return None


def retry(tries, cont=Exception):
    def decorator(func):
        @wraps
        def wrapper(*args, **kwargs):
            for attempt in range(tries):
                try:
                    return func(*args, **kwargs)
                except cont:
                    # Reraise error on last attempt
                    if attempt + 1 == tries:
                        raise
        return wrapper
    return decorator


def retry(tries, cont=Exception):
    @decorator
    def wrapper(func, *args, **kwargs):
        for attempt in range(tries):
            try:
                return func(*args, **kwargs)
            except cont:
                # Reraise error on last attempt
                if attempt + 1 == tries:
                    raise
    return wrapper


@call_decorator(tries=None, cont=Exception)
def retry(call):
    for attempt in range(tries):
        try:
            return call()
        except cont:
            # Reraise error on last attempt
            if attempt + 1 == tries:
                raise

@call_decorator
def retry(call, tries, cont=Exception):
    for attempt in range(tries):
        try:
            return call()
        except cont:
            # Reraise error on last attempt
            if attempt + 1 == tries:
                raise


# introspect "call" parameter to make call_decorator
# introspect __call__ ?

@decorator
def retry(tries, cont=Exception):
    for attempt in range(tries):
        try:
            return __call__()
        except cont:
            # Reraise error on last attempt
            if attempt + 1 == tries:
                raise

# ===>

def retry(tries, cont=Exception):
    def decorator(__func__):
        @wraps(__func__)
        def wrapper(*args, **kwargs):
            __call__ = lambda: __func__(*args, **kwargs)
            def essense(tries, cont=Exception):
                for attempt in range(tries):
                    try:
                        return __call__()
                    except cont:
                        # Reraise error on last attempt
                        if attempt + 1 == tries:
                            raise
            return essense(tries, cont)
        return wrapper
    return decorator
