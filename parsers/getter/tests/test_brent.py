import pytest
from decimal import Decimal

# EP (delete): note cleaner imports, had duplicates
from parsers.getter.brent import (make_url,
                                  parse_response,
                                  yield_brent_dicts)

# fixture
@pytest.fixture
def fake_fetch(url=None):
    return """{"series":[{"data":[["20170925",59.42]]}]}"""


# EP (delete): note tests are in same order as they appear in brent.py, it
# easier reading


# NOTE (EP): earlier we had a parametrisation, close to this:
# <https://github.com/requests/requests/blob/master/tests/test_requests.py#L511-L522>
# I asked to write longname methods to descibe the tests
# current rule is to keep parametrisation for running on different sets for data,
# ususally this is one paramater.


def test_make_url():
    key = "NO_KEY"
    url = make_url(access_key=key)
    assert key in url
    assert url.startswith("http")


def test_parse_response(fake_fetch):
    #text = fake_fetch()
    assert parse_response(fake_fetch) == [['20170925', 59.42]]


def test_yield_brent_dict():
    gen = yield_brent_dicts(downloader=fake_fetch)
    d = next(gen)
    assert d['date'] == '2017-09-25'
    assert d['value'] == Decimal('59.42')
    assert d['freq'] == 'd'
    assert d['name'] == 'BRENT'


# TODO: must test this with <from mock import patch> + decorator

#from mock import patch
#
# class MockingTestTestCase(unittest.TestCase):
#
#@patch('app.mocking.get_user_name')
# def test_mock_stubs(self, test_patch):
#test_patch.return_value = 'Mocked This Silly'
#ret = test_method()
#self.assertEqual(ret, 'Mocked This Silly')


if __name__ == "__main__":
    pytest.main([__file__])
