dict_of = lambda o: {k:getattr(o,k) for k in dir(o) if 'globals' not in k and not callable(getattr(o,k))}
