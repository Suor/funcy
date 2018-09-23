Calculation
===========

.. decorator:: memoize(key_func=None)

    Memoizes decorated function results, trading memory for performance. Can skip memoization
    for failed calculation attempts::

        @memoize                          # Omitting parentheses is ok
        def ip_to_city(ip):
            try:
                return request_city_from_slow_service(ip)
            except NotFound:
                return None               # return None and memoize it
            except Timeout:
                raise memoize.skip(CITY)  # return CITY, but don't memoize it

    Additionally ``@memoize`` exposes its memory for you to manipulate::

        # Prefill memory
        ip_to_city.memory.update({...})

        # Forget everything
        ip_to_city.memory.clear()

    Custom `key_func` could be used to work with unhashable objects, insignificant arguments, etc::

        @memoize(key_func=lambda obj, verbose=None: obj.key)
        def do_things(obj, verbose=False):
            # ...


.. decorator:: make_lookuper

    As :func:`@memoize<memoize>`, but with prefilled memory. Decorated function should return all available arg-value pairs, which should be a dict or a sequence of pairs. Resulting function will raise ``LookupError`` for any argument missing in it::

        @make_lookuper
        def city_location():
            return {row['city']: row['location'] for row in fetch_city_locations()}

    If decorated function has arguments then separate lookuper with its own lookup table is created for each combination of arguments. This can be used to make lookup tables on demand::

        @make_lookuper
        def function_lookup(f):
            return {x: f(x) for x in range(100)}

        fast_sin = function_lookup(math.sin)
        fast_cos = function_lookup(math.cos)

    Or load some resources, memoize them and use as a function::

        @make_lookuper
        def translate(lang):
            return make_list_of_pairs(load_translation_file(lang))

        russian_phrases = lmap(translate('ru'), english_phrases)


.. decorator:: silent_lookuper

    Same as :func:`@make_lookuper<make_lookuper>`, but returns ``None`` on memory miss.


.. decorator:: cache(timeout, key_func=None)

    Caches decorated function results for ``timeout``.
    It can be either number of seconds or :class:`py3:datetime.timedelta`::

        @cache(60 * 60)
        def api_call(query):
            # ...

    Cache can be invalidated before timeout with::

        api_call.invalidate(query)  # Forget cache for query
        api_call.invalidate_all()   # Forget everything

    Custom ``key_func`` could be used same way as in :func:`@memoize<memoize>`::

        # Do not use token in cache key
        @cache(60 * 60, key_func=lambda query, token=None: query)
        def api_call(query, token=None):
            # ...


.. raw:: html
    :file: descriptions.html
