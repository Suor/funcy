import sys
import inspect
from functools import partial
from .compat import PY2


__all__ = ['decorator', 'wraps', 'unwrap', 'ContextDecorator', 'contextmanager']


def decorator(deco):
    """
    Transforms a flat wrapper into decorator::

        @decorator
        def func(call, methods, content_type=DEFAULT):  # These are decorator params
            # Access call arg by name
            if call.request.method not in methods:
                # ...
            # Decorated functions and all the arguments are accesible as:
            print(call._func, call_args, call._kwargs)
            # Finally make a call:
            return call()
    """
    if has_single_arg(deco):
        return make_decorator(deco)
    elif has_1pos_and_kwonly(deco):
        # Any arguments after first become decorator arguments
        # And a decorator with arguments is essentially a decorator fab
        def decorator_fab(_func=None, **dkwargs):  # TODO: make _func pos only in Python 3
            if _func is not None:
                return make_decorator(deco, (), dkwargs)(_func)
            return make_decorator(deco, (), dkwargs)
    else:
        def decorator_fab(*dargs, **dkwargs):
            return make_decorator(deco, dargs, dkwargs)

    return wraps(deco)(decorator_fab)


def make_decorator(deco, dargs=(), dkwargs={}):
    @wraps(deco)
    def _decorator(func):
        def wrapper(*args, **kwargs):
            call = Call(func, args, kwargs)
            return deco(call, *dargs, **dkwargs)
        return wraps(func)(wrapper)

    # NOTE: should I update name to show args?
    # Save these for introspection
    _decorator._func, _decorator._args, _decorator._kwargs = deco, dargs, dkwargs
    return _decorator


class Call(object):
    """
    A call object to pass as first argument to decorator.

    Call object is just a proxy for decorated function
    with call arguments saved in its attributes.
    """
    def __init__(self, func, args, kwargs):
        self._func, self._args, self._kwargs = func, args, kwargs

    def __call__(self, *a, **kw):
        if not a and not kw:
            return self._func(*self._args, **self._kwargs)
        else:
            return self._func(*(self._args + a), **dict(self._kwargs, **kw))

    def __getattr__(self, name):
        try:
            res = self.__dict__[name] = arggetter(self._func)(name, self._args, self._kwargs)
            return res
        except TypeError as e:
            raise AttributeError(*e.args)

    def __str__(self):
        func = getattr(self._func, '__qualname__', str(self._func))
        args = ", ".join(list(map(str, self._args)) + ["%s=%s" % t for t in self._kwargs.items()])
        return "%s(%s)" % (func, args)

    def __repr__(self):
        return "<Call %s>" % self


if PY2:
    def has_single_arg(func):
        spec = inspect.getargspec(func)
        return len(spec.args) == 1 and not spec.varargs and not spec.keywords

    def has_1pos_and_kwonly(func):
        spec = inspect.getargspec(func)
        return len(spec.args) == 1 and not spec.varargs
else:
    from collections import Counter
    from inspect import Parameter as P

    def has_single_arg(func):
        sig = inspect.signature(func)
        if len(sig.parameters) != 1:
            return False
        arg = next(iter(sig.parameters.values()))
        return arg.kind not in (arg.VAR_POSITIONAL, arg.VAR_KEYWORD)

    def has_1pos_and_kwonly(func):
        sig = inspect.signature(func)
        kinds = Counter(p.kind for p in sig.parameters.values())
        return kinds[P.POSITIONAL_ONLY] + kinds[P.POSITIONAL_OR_KEYWORD] == 1 \
            and kinds[P.VAR_POSITIONAL] == 0


def get_argnames(func):
    func = getattr(func, '__original__', None) or unwrap(func)
    return func.__code__.co_varnames[:func.__code__.co_argcount]

def arggetter(func, _cache={}):
    if func in _cache:
        return _cache[func]

    original = getattr(func, '__original__', None) or unwrap(func)
    argnames = get_argnames(original)
    indexes = dict((name, i) for i, name in enumerate(argnames))
    defaults_tuple = original.__defaults__
    if defaults_tuple:
        defaults = dict(zip(argnames[-len(defaults_tuple):], defaults_tuple))
    else:
        defaults = {}

    def get_arg(name, args, kwargs):
        if name not in indexes:
            raise TypeError("%s() doesn't have argument named %s" % (func.__name__, name))
        else:
            index = indexes[name]
            if index < len(args):
                return args[index]
            elif name in kwargs:
                return kwargs[name]
            elif name in defaults:
                return defaults[name]
            else:
                raise TypeError("%s() missing required argument: '%s'" % (func.__name__, name))

    _cache[func] = get_arg
    return get_arg


### Backport python 3.4 contextlib utilities
### namely ContextDecorator and contextmanager (also producing decorator)

if sys.version_info >= (3, 4):
    from contextlib import ContextDecorator, contextmanager
else:
    class ContextDecorator(object):
        "A base class or mixin that enables context managers to work as decorators."

        def _recreate_cm(self):
            """Return a recreated instance of self.

            Allows an otherwise one-shot context manager like
            _GeneratorContextManager to support use as
            a decorator via implicit recreation.

            This is a private interface just for _GeneratorContextManager.
            See issue #11647 for details.
            """
            return self

        def __call__(self, func):
            @wraps(func)
            def inner(*args, **kwds):
                with self._recreate_cm():
                    return func(*args, **kwds)
            return inner


    class _GeneratorContextManager(ContextDecorator):
        """Helper for @contextmanager decorator."""

        def __init__(self, func, *args, **kwds):
            self.gen = func(*args, **kwds)
            self.func, self.args, self.kwds = func, args, kwds
            # Issue 19330: ensure context manager instances have good docstrings
            doc = getattr(func, "__doc__", None)
            if doc is None:
                doc = type(self).__doc__
            self.__doc__ = doc
            # Unfortunately, this still doesn't provide good help output when
            # inspecting the created context manager instances, since pydoc
            # currently bypasses the instance docstring and shows the docstring
            # for the class instead.
            # See http://bugs.python.org/issue19404 for more details.

        def _recreate_cm(self):
            # _GCM instances are one-shot context managers, so the
            # CM must be recreated each time a decorated function is
            # called
            return self.__class__(self.func, *self.args, **self.kwds)

        def __enter__(self):
            try:
                return next(self.gen)
            except StopIteration:
                raise RuntimeError("generator didn't yield")

        def __exit__(self, type, value, traceback):
            if type is None:
                try:
                    next(self.gen)
                except StopIteration:
                    return
                else:
                    raise RuntimeError("generator didn't stop")
            else:
                if value is None:
                    # Need to force instantiation so we can reliably
                    # tell if we get the same exception back
                    value = type()
                try:
                    self.gen.throw(type, value, traceback)
                    raise RuntimeError("generator didn't stop after throw()")
                except StopIteration as exc:
                    # Suppress the exception *unless* it's the same exception that
                    # was passed to throw().  This prevents a StopIteration
                    # raised inside the "with" statement from being suppressed
                    return exc is not value
                except:  # noqa
                    # only re-raise if it's *not* the exception that was
                    # passed to throw(), because __exit__() must not raise
                    # an exception unless __exit__() itself failed.  But throw()
                    # has to raise the exception to signal propagation, so this
                    # fixes the impedance mismatch between the throw() protocol
                    # and the __exit__() protocol.
                    #
                    if sys.exc_info()[1] is not value:
                        raise


    def contextmanager(func):
        """
        A decorator helping to create context managers. Resulting functions also
        behave as decorators.

        A simple example::

            @contextmanager
            def tag(name):
                print("<%s>" % name)
                yield
                print("</%s>" % name)

            with tag("h1"):
                print "foo",
            # -> <h1> foo </h1>

        Using as decorator::

            @tag('strong')
            def shout(text):
                print(text.upper())

            shout('hooray')
            # -> <strong> HOORAY </strong>
        """
        @wraps(func)
        def helper(*args, **kwds):
            return _GeneratorContextManager(func, *args, **kwds)
        return helper


### Fix functools.wraps to make it safely work with callables without all the attributes
### We also add __original__ to it

from functools import WRAPPER_ASSIGNMENTS, WRAPPER_UPDATES

def update_wrapper(wrapper,
                   wrapped,
                   assigned = WRAPPER_ASSIGNMENTS,
                   updated = WRAPPER_UPDATES):
    for attr in assigned:
        try:
            value = getattr(wrapped, attr)
        except AttributeError:
            pass
        else:
            setattr(wrapper, attr, value)
    for attr in updated:
        getattr(wrapper, attr).update(getattr(wrapped, attr, {}))

    # Set it after to not gobble it in __dict__ update
    wrapper.__wrapped__ = wrapped

    # Set an original ref for faster and more convenient access
    wrapper.__original__ = getattr(wrapped, '__original__', None) or unwrap(wrapped)

    # Return the wrapper so this can be used as a decorator via partial()
    return wrapper

def wraps(wrapped,
          assigned = WRAPPER_ASSIGNMENTS,
          updated = WRAPPER_UPDATES):
    """
    An utility to pass function metadata from wrapped function to a wrapper.
    Copies all function attributes including ``__name__``, ``__module__`` and
    ``__doc__``.

    In addition adds ``__wrapped__`` attribute referring to the wrapped function
    and ``__original__`` attribute referring to innermost wrapped one.

    Mostly used to create decorators::

        def some_decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                do_something(*args, **kwargs)
                return func(*args, **kwargs)
            return wrapper

    But see also :func:`@decorator<decorator>` for that.
    This is extended version of :func:`functools.wraps`.
    """
    return partial(update_wrapper, wrapped=wrapped,
                   assigned=assigned, updated=updated)


### Backport of python 3.4 inspect.unwrap utility

try:
    from inspect import unwrap
except ImportError:
    # A simplified version, no stop keyword-only argument
    def unwrap(func):
        """
        Get the object wrapped by ``func``.

        Follows the chain of :attr:`__wrapped__` attributes returning the last
        object in the chain.

        This is a backport from python 3.4.
        """
        f = func  # remember the original func for error reporting
        memo = set([id(f)]) # Memoise by id to tolerate non-hashable objects
        while hasattr(func, '__wrapped__'):
            func = func.__wrapped__
            id_func = id(func)
            if id_func in memo:
                raise ValueError('wrapper loop when unwrapping {!r}'.format(f))
            memo.add(id_func)
        return func
