from datetime import datetime, timedelta
from functools import wraps

from .decorators import decorator


@decorator
def ignore(call, errors):
    try:
        return call()
    except errors:
        return None

silent = ignore(Exception) # Ignore all real exceptions

@decorator
def retry(call, tries, errors=Exception):
    for attempt in range(tries):
        try:
            return call()
        except errors:
            # Reraise error on last attempt
            if attempt + 1 == tries:
                raise


class ErrorRateExceeded(Exception):
    pass

def limit_error_rate(fails, timeout, exception=ErrorRateExceeded):
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
