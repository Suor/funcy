from funcy.strings import *


def test_re_find():
    assert re_find(r'\d+', 'x34y12') == '34'
    assert re_find(r'y(\d+)', 'x34y12') == '12'
    assert re_find(r'([a-z]+)(\d+)', 'x34y12') == ('x', '34')
    assert re_find(r'(?P<l>[a-z]+)(?P<d>\d+)', 'x34y12') == {'l': 'x', 'd': '34'}


def test_re_all():
    assert re_all(r'\d+', 'x34y12') == ['34', '12']
    assert re_all(r'([a-z]+)(\d+)', 'x34y12') == [('x', '34'), ('y', '12')]
    assert re_all(r'(?P<l>[a-z]+)(?P<d>\d+)', 'x34y12') \
                    == [{'l': 'x', 'd': '34'}, {'l': 'y', 'd': '12'}]

def test_str_join():
    assert str_join([1, 2, 3]) == '123'
    assert str_join('_', [1, 2, 3]) == '1_2_3'
    assert isinstance(str_join(u'_', [1, 2, 3]), type(u''))


def test_cut_prefix():
    assert cut_prefix('name:alex', 'name:') == 'alex'
    assert cut_prefix('alex', 'name:') == 'alex'

def test_cut_suffix():
    assert cut_suffix('name.py', '.py') == 'name'
    assert cut_suffix('name', '.py') == 'name'
