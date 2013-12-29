import inspect
from functools import wraps


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
            call = make_call(func, args, kwargs)
            return deco(call, *dargs, **dkwargs)
        return wraps(func)(wrapper)
    return _decorator


def make_call(func, args, kwargs):
    """
    Constructs a call object to pass as first argument to decorator.
    Call object is just a proxy for decorated function with call arguments saved in its attributes.
    """
    # NOTE: we use class enclosed this way instead of creating normal object with attributes
    #       cause it's much faster
    class Call(object):
        def __call__(self, *a, **kw):
            return func(*(args + a), **dict(kwargs, **kw))

        _args = args
        _kwargs = kwargs
        _func = func

        def __getattr__(self, name):
            if not inspect.isfunction(func):
                raise TypeError("Can't introspect argument %s for non-function" % name)
            if not self.__dict__:
                self.__dict__ = getcallargs(func, *args, **kwargs)
            try:
                return self.__dict__[name]
            except KeyError:
                raise AttributeError("Function %s does not have argument %s" \
                                     % (func.__name__, name))

    return Call()


def argcounts(func):
    spec = inspect.getargspec(func)
    return (len(spec.args), bool(spec.varargs), bool(spec.keywords))


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
