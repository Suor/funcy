from funcy.strings import *


def test_re_find():
    assert re_find(r'\d+', 'x34y12') == '34'
    assert re_find(r'([a-z]+)(\d+)', 'x34y12') == ('x', '34')
    assert re_find(r'(?P<l>[a-z]+)(?P<d>\d+)', 'x34y12') == {'l': 'x', 'd': '34'}

def test_re_all():
    assert re_all(r'\d+', 'x34y12') == ['34', '12']
    assert re_all(r'([a-z]+)(\d+)', 'x34y12') == [('x', '34'), ('y', '12')]
    assert re_all(r'(?P<l>[a-z]+)(?P<d>\d+)', 'x34y12') \
                    == [{'l': 'x', 'd': '34'}, {'l': 'y', 'd': '12'}]
