import pytest
from decimal import Decimal

from parsers.getter.brent import (make_url,
                                  parse_response,
                                  yield_brent_dicts)

# fixture
@pytest.fixture
def fake_fetch(url=None):
    return """{"series":[{"data":[["20170925",59.42]]}]}"""

  
def test_make_url():
    key = "NO_KEY"
    url = make_url(access_key=key)
    assert key in url
    assert url.startswith("http")


def test_parse_response(fake_fetch):
    assert parse_response(fake_fetch) == [['20170925', 59.42]]


def test_yield_brent_dict():
    gen = yield_brent_dicts(downloader=fake_fetch)
    d = next(gen)
    assert d['date'] == '2017-09-25'
    assert d['value'] == Decimal('59.42')
    assert d['freq'] == 'd'
    assert d['name'] == 'BRENT'

if __name__ == "__main__":
    pytest.main([__file__])
