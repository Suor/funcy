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

        russian_phrases = map(translate('ru'), english_phrases)


.. decorator:: silent_lookuper

    Same as :func:`@make_lookuper<make_lookuper>`, but returns ``None`` on memory miss.


.. decorator:: cache(timeout, key_func=None)

    Same as :func:`@memoize<memoize>`, but doesn't use cached results older than ``timeout``. It can be either number of seconds or :class:`py:datetime.timedelta`. Also, doesn't support skipping.
