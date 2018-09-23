Decorators
==========

.. module:: funcy

.. decorator:: decorator

    Transforms a flat wrapper into a decorator with or without arguments.
    ``@decorator`` passes special ``call`` object as a first argument to a wrapper.
    A resulting decorator will preserve function module, name and docstring.
    It also adds ``__wrapped__`` attribute referring to wrapped function
    and ``__original__`` attribute referring to innermost wrapped one.

    Here is a simple logging decorator::

        @decorator
        def log(call):
            print(call._func.__name__, call._args, call._kwargs)
            return call()

    ``call`` object also supports by name arg introspection and passing additional arguments to decorated function::

        @decorator
        def with_phone(call):
            # call.request gets actual request value upon function call
            request = call.request
            # ...
            phone = Phone.objects.get(number=request.GET['phone'])
            # phone arg is added to *args passed to decorated function
            return call(phone)

        @with_phone
        def some_view(request, phone):
            # ... some code using phone
            return # ...

    A better practice would be adding keyword argument not positional. This makes such decorators more composable::

        @decorator
        def with_phone(call):
            # ...
            return call(phone=phone)

        @decorator
        def with_user(call):
            # ...
            return call(user=user)

        @with_phone
        @with_user
        def some_view(request, phone=None, user=None):
            # ...
            return # ...

    If a function wrapped with ``@decorator`` has arguments other than ``call``, then decorator with arguments is created::

        @decorator
        def joining(call, sep):
            return sep.join(call())

    You can see more examples in :mod:`flow` and :mod:`debug` submodules source code.


.. decorator:: contextmanager

    A decorator helping to create context managers. Resulting functions also
    behave as decorators. This is a reexport or backport of :func:`py3:contextlib.contextmanager`.


.. autodecorator:: wraps(wrapped, [assigned], [updated])

.. autofunction:: unwrap

.. autoclass:: ContextDecorator


.. raw:: html
    :file: descriptions.html
