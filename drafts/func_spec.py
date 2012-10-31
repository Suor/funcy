def check_spec(types, args):
    if len(args) != len(types):
        raise TypeError('%s() takes exactly %d arguments (%d given)'
                            % (func.__name__, len(types), len(args)))
    for a, t in zip(args, types):
        if not isinstance(a, t):
            argtypes = ', '.join(type(a).__name__ for a in args)
            raise TypeError('Unsupported argument types for %s(): (%s)'
                                % (func.__name__, argtypes))
