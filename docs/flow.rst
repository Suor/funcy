Flow
====

.. decorator:: silent

    Ignore all real exceptions (descendants of :exc:`~py3:exceptions.Exception`). Handy for cleaning data such as user input::


        brand_id = silent(int)(request.GET['brand_id'])
        ids = keep(silent(int), request.GET.getlist('id'))

    And in data import/transform::

        get_greeting = compose(silent(string.lower), re_finder(r'(\w+)!'))
        map(get_greeting, ['a!', ' B!', 'c.'])
        # -> ['a', 'b', None]

    .. note:: Avoid silencing non-primitive functions, use :func:`@ignore()<ignore>` instead and even then be careful not to swallow exceptions unintentionally.


.. decorator:: ignore(errors, default=None)

    Same as :func:`@silent<silent>`, but able to specify ``errors`` to catch and ``default`` to return in case of error caught. ``errors`` can either be exception class or a tuple of them.


.. function:: suppress(*errors)

    A context manager which suppresses given exceptions under its scope::

        with suppress(HttpError):
            # Assume this request can fail, and we are ok with it
            make_http_request()


.. function:: nullcontext(enter_result=None)

    A noop context manager that returns ``enter_result`` from ``__enter__``::

        ctx = nullcontext()
        if threads:
            ctx = op_thread_lock

        with ctx:
            # ... do stuff


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
            def _initialize_class(self, cls):
                pre_save.connect(self._pre_save, sender=cls)
                # ... set up signals, no dups


.. function:: raiser(exception_or_class=Exception, *args, **kwargs)

    Constructs function that raises given exception with given arguments on any invocation. You may pass a string instead of exception as a shortcut::

        mocker.patch('mod.Class.propname', property(raiser("Shouldn't be called")))

    This will raise an ``Exception`` with a corresponding message.


.. decorator:: reraise(errors, into)

    Intercepts any error of ``errors`` classes and reraises it as ``into`` error. Can be used as decorator or a context manager::

        @reraise(requests.RequestsError, MyAPIError)
        def api_call(...):
            # ...

    ``into`` can also be a callable to transform the error before reraising::

        @reraise(requests.RequestsError, lambda e: MyAPIError(error_desc(e)))
        def api_call(...):
            # ...


.. decorator:: retry(tries, errors=Exception, timeout=0, filter_errors=None)

    Every call of the decorated function is tried up to ``tries`` times. The first attempt counts as a try. Retries occur when any subclass of ``errors`` is raised, where``errors`` is an exception class or a list/tuple of exception classes. There will be a delay in ``timeout`` seconds between tries.

    A common use is to wrap some unreliable action::

        @retry(3, errors=HttpError)
        def download_image(url):
            # ... make http request
            return image

    Errors to retry may addtionally be filtered with ``filter_errors`` when classes are not specific enough::

        @retry(3, errors=HttpError, filter_errors=lambda e: e.status_code >= 500)
        def download_image(url):
            # ...

    You can pass a callable as ``timeout`` to achieve exponential delays or other complex behavior::

        @retry(3, errors=HttpError, timeout=lambda a: 2 ** a)
        def download_image(url):
            # ... make http request
            return image


.. function:: fallback(*approaches)

    Tries several approaches until one works. Each approach is either callable or a tuple ``(callable, errors)``, where errors is an exception class or a tuple of classes, which signal to fall back to next approach. If ``errors`` is not supplied then fall back is done for any :exc:`~py3:exceptions.Exception`::

        fallback(
            (partial(send_mail, ADMIN_EMAIL, message), SMTPException),
            partial(log.error, message),          # Handle any Exception
            (raiser(FeedbackError, "Failed"), ()) # Handle nothing
        )


.. function:: limit_error_rate(fails, timeout, exception=ErrorRateExceeded)

    If function fails to complete ``fails`` times in a row, calls to it will be intercepted for ``timeout`` with ``exception`` raised instead. A clean way to short-circuit function taking too long to fail::

        @limit_error_rate(fails=5, timeout=60,
                          exception=RequestError('Temporary unavailable'))
        def do_request(query):
            # ... make a http request
            return data

    Can be combined with :func:`ignore` to silently stop trying for a while::

        @ignore(ErrorRateExceeded, default={'id': None, 'name': 'Unknown'})
        @limit_error_rate(fails=5, timeout=60)
        def get_user(id):
            # ... make a http request
            return data


.. function:: throttle(period)

    Only runs a decorated function once in a ``period``::

        @throttle(60)
        def process_beat(pk, progress):
            Model.objects.filter(pk=pk).update(beat=timezone.now(), progress=progress)

        # Processing something, update progress info no more often then once a minute
        for i in ...:
            process_beat(pk, i / n)
            # ... do actual processing


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

    Use ``bytes`` separator to get bytes result::

        @joining(b' ')
        def car_desc(self):
            yield self.year_made
            # ...

    See also :func:`str_join`.


.. decorator:: post_processing(func)

    Passes decorated function result through ``func``. This is the generalization of :func:`@collecting<collecting>` and :func:`@joining()<joining>`. Could save you writing a decorator or serve as an extended comprehension:

    ::

        @post_processing(dict)
        def make_cond(request):
            if request.GET['new']:
                yield 'year__gt', 2000
            for key, value in request.GET.items():
                if value == '':
                    continue
                # ...


.. decorator:: wrap_with(ctx)

    Turns a context manager into a decorator::

        @wrap_with(threading.Lock())
        def protected_func(...):
            # ...

.. raw:: html
    :file: descriptions.html
