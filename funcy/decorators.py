import sys, inspect
from functools import partial


__all__ = ['decorator']


def decorator(deco):
    # Any arguments after first become decorator arguments
    args = argcounts(deco) != (1, False, False)

    if args:
        # A decorator with arguments is essentialy a decorator fab
        def decorator_fab(*dargs, **dkwargs):
            return make_decorator(deco, dargs, dkwargs)
        return wraps(deco)(decorator_fab)
    else:
        return wraps(deco)(make_decorator(deco))


def make_decorator(deco, dargs=(), dkwargs={}):
    def _decorator(func):
        def wrapper(*args, **kwargs):
            call = Call(func, args, kwargs)
            return deco(call, *dargs, **dkwargs)
        return wraps(func)(wrapper)
    return _decorator


class Call(object):
    """
    A call object to pass as first argument to decorator.
    Call object is just a proxy for decorated function with call arguments saved in its attributes.
    """
    def __init__(self, func, args, kwargs):
        self._func, self._args, self._kwargs = func, args, kwargs
        self._introspected = False

    def __call__(self, *a, **kw):
        if not a and not kw:
            return self._func(*self._args, **self._kwargs)
        else:
            return self._func(*(self._args + a), **dict(self._kwargs, **kw))

    def __getattr__(self, name):
        if not self._introspected:
            # Find real func to call getcallargs() on it
            # We need to do it since our decorators don't preserve signature
            func = unwrap(self._func)
            self.__dict__.update(getcallargs(func, *self._args, **self._kwargs))
            self._introspected = True
        try:
            return self.__dict__[name]
        except KeyError:
            raise AttributeError('Function %s does not have argument %s' \
                                 % (self._func.__name__, name))


def argcounts(func):
    spec = inspect.getargspec(func)
    return (len(spec.args), bool(spec.varargs), bool(spec.keywords))


### Fix functools.wraps to make it safely work with callables without all the attributes

# These are already safe in python 3.2
if sys.version_info >= (3, 2):
    from functools import update_wrapper, wraps
else:
    # These are for python 2, so list of attributes is far shorter.
    # Python 3.2 and ealier will get reduced functionality, but we don't support it :)
    WRAPPER_ASSIGNMENTS = ('__module__', '__name__', '__doc__')
    WRAPPER_UPDATES = ('__dict__',)
    # Copy-pasted these two from python 3.3 functools source code
    def update_wrapper(wrapper,
                       wrapped,
                       assigned = WRAPPER_ASSIGNMENTS,
                       updated = WRAPPER_UPDATES):
        wrapper.__wrapped__ = wrapped
        for attr in assigned:
            try:
                value = getattr(wrapped, attr)
            except AttributeError:
                pass
            else:
                setattr(wrapper, attr, value)
        for attr in updated:
            getattr(wrapper, attr).update(getattr(wrapped, attr, {}))
        # Return the wrapper so this can be used as a decorator via partial()
        return wrapper

    def wraps(wrapped,
              assigned = WRAPPER_ASSIGNMENTS,
              updated = WRAPPER_UPDATES):
        return partial(update_wrapper, wrapped=wrapped,
                       assigned=assigned, updated=updated)


### Backport of python 3.4 inspect.unwrap utility

try:
    from inspect import unwrap
except ImportError:
    # A simplified version, no stop keyword-only argument
    def unwrap(func):
        f = func  # remember the original func for error reporting
        memo = set([id(f)]) # Memoise by id to tolerate non-hashable objects
        while hasattr(func, '__wrapped__'):
            func = func.__wrapped__
            id_func = id(func)
            if id_func in memo:
                raise ValueError('wrapper loop when unwrapping {!r}'.format(f))
            memo.add(id_func)
        return func


### Backport of inspect.getcallargs for python 2.6

try:
    from inspect import getcallargs
except ImportError:
    def getcallargs(func, *positional, **named):
        """Get the mapping of arguments to values.
        A dict is returned, with keys the function argument names (including the
        names of the * and ** arguments, if any), and values the respective bound
        values from 'positional' and 'named'."""
        args, varargs, varkw, defaults = inspect.getargspec(func)
        f_name = func.__name__
        arg2value = {}

        # The following closures are basically because of tuple parameter unpacking.
        assigned_tuple_params = []
        def assign(arg, value):
            if isinstance(arg, str):
                arg2value[arg] = value
            else:
                assigned_tuple_params.append(arg)
                value = iter(value)
                for i, subarg in enumerate(arg):
                    try:
                        subvalue = next(value)
                    except StopIteration:
                        raise ValueError('need more than %d %s to unpack' %
                                         (i, 'values' if i > 1 else 'value'))
                    assign(subarg,subvalue)
                try:
                    next(value)
                except StopIteration:
                    pass
                else:
                    raise ValueError('too many values to unpack')

        def is_assigned(arg):
            if isinstance(arg,str):
                return arg in arg2value
            return arg in assigned_tuple_params

        if inspect.ismethod(func) and func.im_self is not None:
            # implicit 'self' (or 'cls' for classmethods) argument
            positional = (func.im_self,) + positional
        num_pos = len(positional)
        num_total = num_pos + len(named)
        num_args = len(args)
        num_defaults = len(defaults) if defaults else 0
        for arg, value in zip(args, positional):
            assign(arg, value)
        if varargs:
            if num_pos > num_args:
                assign(varargs, positional[-(num_pos-num_args):])
            else:
                assign(varargs, ())
        elif 0 < num_args < num_pos:
            raise TypeError('%s() takes %s %d %s (%d given)' % (
                f_name, 'at most' if defaults else 'exactly', num_args,
                'arguments' if num_args > 1 else 'argument', num_total))
        elif num_args == 0 and num_total:
            raise TypeError('%s() takes no arguments (%d given)' %
                            (f_name, num_total))
        for arg in args:
            if isinstance(arg, str) and arg in named:
                if is_assigned(arg):
                    raise TypeError("%s() got multiple values for keyword "
                                    "argument '%s'" % (f_name, arg))
                else:
                    assign(arg, named.pop(arg))
        if defaults:    # fill in any missing values with the defaults
            for arg, value in zip(args[-num_defaults:], defaults):
                if not is_assigned(arg):
                    assign(arg, value)
        if varkw:
            assign(varkw, named)
        elif named:
            unexpected = next(iter(named))
            if isinstance(unexpected, unicode):
                unexpected = unexpected.encode(sys.getdefaultencoding(), 'replace')
            raise TypeError("%s() got an unexpected keyword argument '%s'" %
                            (f_name, unexpected))
        unassigned = num_args - len([arg for arg in args if is_assigned(arg)])
        if unassigned:
            num_required = num_args - num_defaults
            raise TypeError('%s() takes %s %d %s (%d given)' % (
                f_name, 'at least' if defaults else 'exactly', num_required,
                'arguments' if num_required > 1 else 'argument', num_total))
        return arg2value
