Functions
=========

.. function:: identity(x)
.. function:: constantly(x)
.. function:: caller(*args, **kwargs)
.. function:: partial(func, *args, **kwargs)

    Like :func:`functools.partial` but returns real function.

.. function:: curry(func[, n])
.. function:: compose(*fs)
.. function:: complement(pred)
.. function:: juxt(*fs)
.. function:: ijuxt(*fs)
.. function:: iffy([pred], action, [default=identity])

