from datetime import datetime, timedelta
import time
import threading

from .compat import map, range, raise_from, Hashable
from .decorators import decorator, wraps, get_argnames, arggetter, contextmanager


__all__ = ['raiser', 'ignore', 'silent', 'suppress', 'nullcontext', 'reraise', 'retry', 'fallback',
           'limit_error_rate', 'ErrorRateExceeded', 'throttle',
           'post_processing', 'collecting', 'joining',
           'once', 'once_per', 'once_per_args',
           'wrap_with']


### Error handling utilities

def raiser(exception_or_class=Exception, *args, **kwargs):
    """Constructs function that raises the given exception
       with given arguments on any invocation."""
    if isinstance(exception_or_class, str):
        exception_or_class = Exception(exception_or_class)

    def _raiser(*a, **kw):
        if args or kwargs:
            raise exception_or_class(*args, **kwargs)
        else:
            raise exception_or_class
    return _raiser


# Not using @decorator here for speed,
# since @ignore and @silent should be used for very simple and fast functions
def ignore(errors, default=None):
    """Alters function to ignore given errors, returning default instead."""
    errors = _ensure_exceptable(errors)

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except errors:
                return default
        return wrapper
    return decorator

def silent(func):
    """Alters function to ignore all exceptions."""
    return ignore(Exception)(func)

### Backport of Python 3.4 suppress
try:
    from contextlib import suppress
except ImportError:
    class suppress(object):
        """Context manager to suppress specified exceptions

        After the exception is suppressed, execution proceeds with the next
        statement following the with statement.
        """

        def __init__(self, *exceptions):
            self._exceptions = exceptions

        def __enter__(self):
            pass

        def __exit__(self, exctype, excinst, exctb):
            # Unlike isinstance and issubclass, CPython exception handling
            # currently only looks at the concrete type hierarchy (ignoring
            # the instance and subclass checking hooks). While Guido considers
            # that a bug rather than a feature, it's a fairly hard one to fix
            # due to various internal implementation details. suppress provides
            # the simpler issubclass based semantics, rather than trying to
            # exactly reproduce the limitations of the CPython interpreter.
            #
            # See http://bugs.python.org/issue12029 for more details
            return exctype is not None and issubclass(exctype, self._exceptions)


### Backport of Python 3.7 nullcontext
try:
    from contextlib import nullcontext
except ImportError:
    class nullcontext(object):
        """Context manager that does no additional processing.

        Used as a stand-in for a normal context manager, when a particular
        block of code is only sometimes used with a normal context manager:

        cm = optional_cm if condition else nullcontext()
        with cm:
            # Perform operation, using optional_cm if condition is True
        """

        def __init__(self, enter_result=None):
            self.enter_result = enter_result

        def __enter__(self):
            return self.enter_result

        def __exit__(self, *excinfo):
            pass


@contextmanager
def reraise(errors, into):
    """Reraises errors as other exception."""
    errors = _ensure_exceptable(errors)
    try:
        yield
    except errors as e:
        if callable(into) and not _is_exception(into):
            raise_from(into(e), e)
        else:
            raise_from(into, e)


@decorator
def retry(call, tries, errors=Exception, timeout=0, filter_errors=None):
    """Makes decorated function retry up to tries times.
       Retries only on specified errors.
       Sleeps timeout or timeout(attempt) seconds between tries."""
    errors = _ensure_exceptable(errors)
    for attempt in range(tries):
        try:
            return call()
        except errors as e:
            if not (filter_errors is None or filter_errors(e)):
                raise

            # Reraise error on last attempt
            if attempt + 1 == tries:
                raise
            else:
                timeout_value = timeout(attempt) if callable(timeout) else timeout
                if timeout_value > 0:
                    time.sleep(timeout_value)


def fallback(*approaches):
    """Tries several approaches until one works.
       Each approach has a form of (callable, expected_errors)."""
    for approach in approaches:
        func, catch = (approach, Exception) if callable(approach) else approach
        catch = _ensure_exceptable(catch)
        try:
            return func()
        except catch:
            pass

def _ensure_exceptable(errors):
    """Ensures that errors are passable to except clause.
       I.e. should be BaseException subclass or a tuple."""
    return errors if _is_exception(errors) else tuple(errors)


def _is_exception(value):
    """Is the given value an exception?"""
    return isinstance(value, type) and issubclass(value, BaseException)


class ErrorRateExceeded(Exception):
    pass

def limit_error_rate(fails, timeout, exception=ErrorRateExceeded):
    """If function fails to complete fails times in a row,
       calls to it will be intercepted for timeout with exception raised instead."""
    if isinstance(timeout, int):
        timeout = timedelta(seconds=timeout)

    def decorator(func):
        func.fails = 0
        func.blocked = None

        @wraps(func)
        def wrapper(*args, **kwargs):
            if func.blocked:
                if datetime.now() - func.blocked < timeout:
                    raise exception
                else:
                    func.blocked = None

            try:
                result = func(*args, **kwargs)
            except:  # noqa
                func.fails += 1
                if func.fails >= fails:
                    func.blocked = datetime.now()
                raise
            else:
                func.fails = 0
                return result
        return wrapper
    return decorator


def throttle(period):
    """Allows only one run in a period, the rest is skipped"""
    if isinstance(period, timedelta):
        period = timedelta.total_seconds()

    def decorator(func):
        blocked_until = None

        @wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal blocked_until

            now = time.time()
            if blocked_until and blocked_until > now:
                return
            blocked_until = now + period

            return func(*args, **kwargs)

        return wrapper

    return decorator


### Post processing decorators

@decorator
def post_processing(call, func):
    """Post processes decorated function result with func."""
    return func(call())

collecting = post_processing(list)
collecting.__name__ = 'collecting'
collecting.__doc__ = "Transforms a generator into list returning function."

@decorator
def joining(call, sep):
    """Joins decorated function results with sep."""
    return sep.join(map(sep.__class__, call()))


### Initialization helpers

def once_per(*argnames):
    """Call function only once for every combination of the given arguments."""
    def once(func):
        lock = threading.Lock()
        done_set = set()
        done_list = list()

        get_arg = arggetter(func)

        @wraps(func)
        def wrapper(*args, **kwargs):
            with lock:
                values = tuple(get_arg(name, args, kwargs) for name in argnames)
                if isinstance(values, Hashable):
                    done, add = done_set, done_set.add
                else:
                    done, add = done_list, done_list.append

                if values not in done:
                    add(values)
                    return func(*args, **kwargs)
        return wrapper
    return once

once = once_per()
once.__doc__ = "Let function execute once, noop all subsequent calls."

def once_per_args(func):
    """Call function once for every combination of values of its arguments."""
    return once_per(*get_argnames(func))(func)


@decorator
def wrap_with(call, ctx):
    """Turn context manager into a decorator"""
    with ctx:
        return call()
