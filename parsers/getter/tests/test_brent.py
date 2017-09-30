import pytest

# TODO (MS): import testers first, then modules under testing 
from parsers.getter import brent
from decimal import Decimal
import mock
from parsers.getter.brent import parse_response, fetch, make_url, format_string


#EP: must keep order of fucntons same as in brent.py 

def test_make_url():
    key = "NOT_EIA_ACCESS_KEY"
    url = make_url(access_key=key)
    assert key in url

# FIXME: this less readable than asserts. each test has to have a long name. no parametrization here.
# FIXME: must convert to three tests with longer, descriptive names, 
#        def test_something_on_something_return/behaves/raises_somehting() 

@pytest.mark.parametrize('date_string, expected', [
    ('20171231', '2017-12-31'),
    ('bad_date_format', "time data 'bad_date_format' does not match format '%Y%m%d'"),
    (None, "strptime() argument 1 must be str, not None"),
])
def test_format_string(date_string, expected):
    try:
        result = format_string(date_string)
        assert result == expected
    except Exception as e:
        assert Exception == ValueError or TypeError
        assert str(e) == expected

# TODO: use initials for comments
# MS: I am not sure that's is a good way create fake method outsidee the test.
# Thats why we use mocker. To patch everything that we want make fake call
def fake_fetch(url=None):
    return """{"series":[{"data":[["20170925",59.42]]}]}"""

def test_yield_brent_dict():
    gen = brent.yield_brent_dicts(download_func=fake_fetch)
    d = next(gen)
    assert d['date'] == '2017-09-25'
    assert d['value'] == Decimal('59.42')

# MS: I want propose this way
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
# TODO: 
from parsers.getter.tests.fixtures import foo_obj
def test_fetch(mocker):
    kwargs = {"text": 'some_text'}
    mocker.patch('requests.get', mock.MagicMock(return_value=foo_obj(**kwargs)))
    assert fetch('some_url') == 'some_text'
