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

    Generally a decorator with arguments is required to be called with ``()`` when applied to function. However, if you use only keyword only parameters aside from ``call`` then you can omit them::

        @decorator
        def rate_limit(call, *, extra_labels=None):
            # ...

        @rate_limit  # no extra labels, parentheses are optional
        def func(request, ...):
            # ...

        @rate_limit(extra_labels=lambda r: [f"user:{r.user.pk}"])
        def func(request, ...):
            # ...

    You can see more examples in :mod:`flow` and :mod:`debug` submodules source code.

    Type checkers see the decorated function keeping its own signature. Pass ``returning=``
    when the decorator returns something else::

        @decorator(returning=HttpResponse)
        def render_to(call, template):
            return render(call.request, template, call())

        @decorator(returning=str)
        def as_json(call):
            return json.dumps(call())

    For a decorator you can't annotate, cast it to the same protocol::

        from funcy.typing import DecoReturning

        retrying = cast(DecoReturning[Response | None], third_party_retry)

    A decorator may also alter the arguments: ``call(conn)`` appends one, so callers of
    the decorated function pass one less. ``DecoReturning`` fits here too — the extra
    argument stays in the signature and passing it won't be caught, everything else is.

    To spell such a call out, cast the decorated function, not the decorator, which is
    used on many functions and has no single signature. The cast needs a name of its
    own, since the name a ``def`` binds already has a type::

        @with_conn
        def _query(sql: str, *, limit: int = 10, conn: Conn) -> list[Row]:
            ...

        query = cast(_Query, _query)  # a Callable will do when names don't matter


.. decorator:: contextmanager

    A decorator helping to create context managers. Resulting functions also
    behave as decorators. This is a reexport or backport of :func:`py3:contextlib.contextmanager`.


.. autodecorator:: wraps(wrapped, [assigned], [updated])

.. autofunction:: unwrap

.. autoclass:: ContextDecorator


.. raw:: html
    :file: descriptions.html
