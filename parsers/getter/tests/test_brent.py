from parsers.getter import brent
from decimal import Decimal
import mock

from parsers.getter.brent import parse_response, fetch, make_url, format_string
from parsers.getter.tests.fixtures import foo_obj


# muroslav2909: I am not sure that's is a good way create fake method outsidee the test.
# Thats why we use mocker. To patch everything that we want make fake call
def fake_fetch(url=None):
    return """{"series":[{"data":[["20170925",59.42]]}]}"""


def test_yield_brent_dict():
    gen = brent.yield_brent_dicts(download_func=fake_fetch)
    d = next(gen)
    assert d['date'] == '2017-09-25'
    assert d['value'] == Decimal('59.42')


# muroslav2909: I want propose this way
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


# EP: this part I do not understand
def test_fetch(mocker):
    return_value = foo_obj(**{"text": 'some_text'})
    mocker.patch('requests.get', mock.MagicMock(return_value=return_value))
    assert fetch('some_url') == 'some_text'


def test_make_url():
    key = "NOT_EIA_ACCESS_KEY"
    url = make_url(access_key=key)
    assert key in url


def test_format_string_with_good_args():
    assert format_string('20171231') == '2017-12-31'


def test_format_string_with_bad_args():
    try:
        format_string('bad_date_format')
    except ValueError as e:
        assert str(e) == "time data 'bad_date_format' does not match format '%Y%m%d'"


def test_format_string_with_None_args():
    try:
        format_string(None)
    except TypeError as e:
        assert str(e) == "strptime() argument 1 must be str, not None"
