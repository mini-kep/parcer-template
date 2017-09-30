from parsers.getter import brent
from decimal import Decimal
import mock

# I am not sure that's is a good way create fake method outsidee the test.
# Thats why we use mocker. To patch everything that we want make fake call
from parsers.getter.brent import parse_response


def fake_fetch(url=None):
    return """{"series":[{"data":[["20170925",59.42]]}]}"""

def test_yield_brent_dict():
    gen = brent.yield_brent_dicts(download_func=fake_fetch)
    d = next(gen)
    assert d['date'] == '2017-09-25'
    assert d['value'] == Decimal('59.42')

# I want propose this way
def test_yield_brent_dict_2():
    fake_fetch = mock.MagicMock(return_value="""{"series":[{"data":[["20170925",59.42]]}]}""")
    gen = brent.yield_brent_dicts(download_func=fake_fetch)
    d = next(gen)
    fake_fetch.assert_called_once()
    assert d['date'] == '2017-09-25'
    assert d['value'] == Decimal('59.42')

# If we chhose way 1
def test_parse_response_1():
    text = fake_fetch()
    assert parse_response(text) == [['20170925', 59.42]]

# If we chhose way 2
def test_parse_response_2():
    text = """{"series":[{"data":[["20170925",59.42]]}]}"""
    assert parse_response(text) == [['20170925', 59.42]]