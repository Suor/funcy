Objects
=======

.. decorator:: cached_property

    Creates a property caching its result. One can rewrite cached value simply by assigning property. And clear cache by deleting it.

    A great way to lazily attach some data to an object::

        class MyUser(AbstractBaseUser):
            @cached_property
            def public_phones(self):
                return list(self.phones.filter(confirmed=True, public=True))

    **CAVEAT:** only one cached value is stored for each property, so if you call ancestors cached property from outside of corresponding child property it will save ancestors value, which will prevent future evaluations from ever calling child function.


.. decorator:: cached_readonly

    Creates a read-only property caching its result. Same as :func:`cached_property` but protected against rewrites.


.. decorator:: monkey(cls_or_module, name=None)

    Monkey-patches class or module by adding decorated function or property to it named ``name`` or the same as decorated function. Saves overwritten method to ``original`` attribute of decorated function for a kind of inheritance::

        # A simple caching of all get requests,
        # even for models for which you can't easily change Manager
        @monkey(QuerySet)
        def get(self, *args, **kwargs):
            if not args and list(kwargs) == ['pk']:
                cache_key = '%s:%d' % (self.model, kwargs['pk'])
                result = cache.get(cache_key)
                if result is None:
                    result = get.original(self, *args, **kwargs)
                    cache.set(cache_key, result)
                return result
            else:
                return get.original(self, *args, **kwargs)


.. class:: namespace

    A base class that prevents its member functions turning into methods::

        class Checks(namespace):
            is_str = isa(str)
            max_len = lambda l: lambda value: len(value) <= l

        field_checks = all_fn(Checks.is_str, Checks.max_len(30))

    This is noop in Python 3 as it doesn't have unbound methods anyway.


.. class:: LazyObject(init)

    Creates a object only really setting itself up on first attribute access. Since attribute access happens immediately before any method call, this permits delaying initialization until first call::

        @LazyObject
        def redis_client():
            if isinstance(settings.REDIS, str):
                return StrictRedis.from_url(settings.REDIS)
            else:
                return StrictRedis(**settings.REDIS)

        # Will be only created on first use
        redis_client.set(...)


.. raw:: html
    :file: descriptions.html
