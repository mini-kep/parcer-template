import pytest
from getter import brent
from decimal import Decimal

def fake_fetch(url):
    return """{"series":[{"data":[["20170925",59.42]]}]}"""

def test_yield_brent_dict():
    gen = getter.brent.yield_brent_dicts(download_func=fake_fetch)
    d = next(gen)
    assert d['date'] == '2017-09-25'
    assert d['value'] == Decimal('59.42')
