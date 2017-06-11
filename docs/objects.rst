Objects
=======

.. decorator:: cached_property

    Creates a property caching its result. One can rewrite cached value simply by assigning property. And clear cache by deleting it.

    A great way to lazily attach some data to an object::

        class MyUser(AbstractBaseUser):
            @cached_property
            def public_phones(self):
                return list(self.phones.filter(confirmed=True, public=True))


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
            is_str = lambda value: isinstance(value, str)
            max_len = lambda l: lambda value: len(value) <= l

        field_checks = all_fn(Checks.is_str, Checks.max_len(30))

