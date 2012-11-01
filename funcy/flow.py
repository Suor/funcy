from datetime import datetime, timedelta
from functools import wraps


def silent(func):
    @wraps(func)
    def wrappper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return None
    return wrapper


def retry(tries, cont=Exception):
    def decorator(func):
        @wraps(func)
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


def limit_error_rate(fails=None, timeout=None, exception=None):
    if isinstance(timeout, int):
        timeout = timedelta(seconds=timeout)

    def decorator(func):
        func.fails = 0
        func.blocked = None

        @wraps(func)
        def wrapper(*args, **kwargs):
            if func.blocked and datetime.now() - func.blocked < timeout:
                raise exception

            try:
                result = func(*args, **kwargs)
            except:
                func.fails += 1
                if func.fails >= fails:
                    func.blocked = datetime.now()
                raise
            else:
                func.fails = 0
                func.blocked = None
                return result
        return wrapper
    return decorator
