dict_of = lambda o: {k:getattr(o,k) for k in dir(o) if 'globals' not in k and not callable(getattr(o,k))}

from django.db import connections

def fetch(query, params=[], db='default'):
    cursor = connections[db].cursor()
    cursor.execute(query, params)
    return cursor.fetchall()
