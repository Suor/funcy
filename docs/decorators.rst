Decorators
==========

.. decorator:: decorator

    An easy way to create decorators. Here is simple logging decorator::

        @decorator
        def log(call):
            print call.func.__name__, call.args, call.kwargs
            return call()

    ``call`` object also support by name arg introspection and passing additional arguments to decorated function::

        @decorator
        def with_phone(call):
            # call.request gets actual request value upon function call
            phone = Phone.objects.get(number=call.request.GET['phone'])
            # phone arg is added to *args passed to decorated function
            return call(phone)

        @with_phone
        def some_view(request, phone):
            # ... some code using phone
            return # ...

    You can see more examples in :mod:`flow` and :mod:`debug` modules source code.
