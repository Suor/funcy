Flow
====

.. decorator:: silent

    Ignore all real exceptions (descendants of :exc:`~py:exceptions.Exception`). Handy for cleaning data such as user input::


        brand_id = silent(int)(request.GET['brand_id'])
        ids = keep(silent(int), request.GET.getlist('id'))

    And in data import/transform::

        get_greeting = compose(silent(string.lower), re_finder(r'(\w+)!'))
        map(get_greeting, ['a!', ' B!', 'c.'])
        # -> ['a', 'b', None]

    .. note:: Avoid silencing non-primitive functions, use :func:`ignore` instead and even then be careful not to swallow exceptions unintentionally.


.. decorator:: ignore(errors, default=None)

    Same as :func:`silent`, but able to specify ``errors`` to catch and ``default`` to return in case of error caught. ``errors`` can either be exception class or tuple of them.


.. function:: suppress(*errors)

    A context manager which suppresses given exceptions under its scope::

        with suppress(HttpError):
            # Assume this request can fail, and we are ok with it
            make_http_request()


.. decorator:: once
               once_per_args
               once_per(*argnames)

    Call function only once, once for every combination of values of its arguments or once for every combination of given arguments. Thread safe. Handy for various initialization purposes::

        # Global initialization
        @once
        def initialize_cache():
            conn = some.Connection(...)
            # ... set up everything

        # Per argument initialization
        @once_per_args
        def initialize_language(lang):
            conf = load_language_conf(lang)
            # ... set up language

        # Setup each class once
        class SomeManager(Manager):
            @once_per('cls')
            def contribute_to_class(self, cls):
                pre_save.connect(self._pre_save, sender=cls)
                # ... set up signals, no dups


.. function:: raiser(exception_or_class=Exception, *args, **kwargs)

    Constructs function that raises given exception with given arguments on any invocation.


.. decorator:: retry(tries, errors=Exception, timeout=0)

    Every call of decorated function retried up to ``tries`` times if any subclass of ``errors`` occurs (could be exception class or a tuple of them). There will be delay in ``timeout`` seconds between tries. You can use callable object which returns value as ``timeout``::

        @retry(3, errors=HttpError)
        def download_image(url):
            # ... make http request
            return image


.. function:: fallback(*approaches)

    Tries several approaches until one works. Each approach is either callable or a tuple ``(callable, errors)``, where errors is an exception class or a tuple of classes, which signal to fall back to next approach. If ``errors`` is not supplied then fall back is done for any :exc:`~py:exceptions.Exception`::

        fallback(
            (partial(send_mail, ADMIN_EMAIL, message), SMTPException),
            partial(log.error, message),
            raiser(FeedbackError, "Unable to notify admin")
        )


.. function:: limit_error_rate(fails, timeout, exception=ErrorRateExceeded)

    If function fails to complete ``fails`` times in a row, calls to it will be intercepted for ``timeout`` with ``exception`` raised instead. A clean way to short-circuit function taking too long to fail::

        @limit_error_rate(fails=5, timeout=60, exception=RequestError('Temporary unavailable'))
        def do_request(query):
            # ... make a http request
            return data

    Can be combined with :func:`ignore` to silently stop trying for a while::

        @ignore(ErrorRateExceeded, default={'id': None, 'name': 'Unknown'})
        @limit_error_rate(fails=5, timeout=60)
        def get_user(id):
            # ... make a http request
            return data


.. decorator:: collecting

    Transforms generator or other iterator returning function into list returning one.

    Handy to prevent quirky iterator-returning properties::

        @property
        @collecting
        def path_up(self):
            node = self
            while node:
                yield node
                node = node.parent

    Also makes list constructing functions beautifully yielding.

    .. Or you could just write::

    ..     @property
    ..     def path_up(self):
    ..         going_up = iterate(attrgetter('parent'), self)
    ..         return list(takewhile(bool, going_up))


.. decorator:: joining(sep)

    Wraps common python idiom "collect then join" into a decorator. Transforms generator or alike into function, returning string of joined results. Automatically converts all elements to separator type for convenience.

    Goes well with generators with some ad-hoc logic within::

        @joining(', ')
        def car_desc(self):
            yield self.year_made
            if self.engine_volume: yield '%s cc' % self.engine_volume
            if self.transmission:  yield self.get_transmission_display()
            if self.gear:          yield self.get_gear_display()
            # ...

    Use ``unicode`` separator to get unicode result::

        @joining(u', ')
        def car_desc(self):
            yield self.year_made
            # ...

    See also :func:`str_join`.


.. .. decorator:: postprocessing(func)
