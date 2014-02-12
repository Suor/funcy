Objects
=======

.. decorator:: cached_property

    Creates a property caching its result. One can rewrite cached value simply by assigning property. And clear cache by deleting it.

    A great way to lazily attach some data to an object::

        class MyUser(AbstractBaseUser):
            @cached_property
            def public_phones(self):
                return list(self.phones.filter(confirmed=True, public=True))


.. decorator:: @monkey(cls_or_module)
