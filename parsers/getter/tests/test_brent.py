import pytest
from decimal import Decimal
import requests_mock
from parsers.config import EIA_ACCESS_KEY

# EP (delete): note cleaner imports, had duplicates
from parsers.getter.brent import (format_string,
                                  format_value,
                                  make_url,
                                  fetch, # not tested
                                  parse_response,
                                  yield_brent_dicts)

# fixture

def fake_fetch(url=None):
    return """{"series":[{"data":[["20170925",59.42]]}]}"""


# EP (delete): note tests are in same order as they appear in brent.py, it easier reading


# NOTE (EP): earlier we had a parametrisation, close to this:
# <https://github.com/requests/requests/blob/master/tests/test_requests.py#L511-L522>
# I asked to write longname methods to descibe the tests
# current rule is to keep parametrisation for running on different sets for data,
# ususally this is one paramater.

class Test_format_string:
    # EP: quick naming is ok, but better use 'something on something does something'
    def test_format_string_on_valid_arg_returns_string(self):
        assert format_string('20171231') == '2017-12-31'

    def test_format_string_on_bad_arg_raises_ValueError(self):
        with pytest.raises(ValueError):
            format_string('bad_date_format')
        # EP (delete): we are not testing for error message content, it is hard to mainitain
        #assert "bad_date_format' does not match format '%Y%m%d'" in str(value_error.value)

    def test_format_string_on_None_raises_TypeError(self):
        with pytest.raises(TypeError):
            format_string(None)

def test_format_value():
    return format_value('59.42') == Decimal('59.42')

# parsing flow

def test_make_url():
    key = "NO_KEY"
    url = make_url(access_key=key)
    assert key in url
    assert url.startswith("http")


def test_parse_response():
    text = fake_fetch()
    assert parse_response(text) == [['20170925', 59.42]]


def test_yield_brent_dict():
    gen = yield_brent_dicts(downloader=fake_fetch)
    d = next(gen)
    assert d['date'] == '2017-09-25'
    assert d['value'] == Decimal('59.42')
    assert d['freq'] == 'd'
    assert d['name'] == 'BRENT'


def test_fetch(access_key=EIA_ACCESS_KEY):
    url = "http://api.eia.gov/series/?api_key="+access_key+"&series_id=PET.RBRTE.D"
    with requests_mock.mock() as m:
        m.get(url, text='fake response from url')
        assert fetch(url) == 'fake response from url'

# TODO: must test this with <from mock import patch> + decorator

#from mock import patch
#
#class MockingTestTestCase(unittest.TestCase):
#
#@patch('app.mocking.get_user_name')
#def test_mock_stubs(self, test_patch):
#test_patch.return_value = 'Mocked This Silly'
#ret = test_method()
#self.assertEqual(ret, 'Mocked This Silly')


if __name__ == "__main__":
    pytest.main([__file__])
