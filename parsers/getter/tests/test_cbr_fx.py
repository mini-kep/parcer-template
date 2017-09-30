import datetime
import mock
from parsers.getter import cbr_fx
from parsers.getter.cbr_fx import make_url
from parsers.getter.tests.fixtures import foo_obj

def test_get_xml_without_exception(mocker):
    return_value = foo_obj(**{"text": 'expected_text'})
    mocker.patch('requests.get', mock.MagicMock(return_value=return_value))
    assert cbr_fx.get_xml("some_url") == 'expected_text'

def test_get_xml_with_exception(mocker):
    return_value = foo_obj(**{"text": 'Error in parameters'})
    mocker.patch('requests.get', mock.MagicMock(return_value=return_value))
    try:
        cbr_fx.get_xml("some_url")
    except Exception as e:
        assert str(e) == 'Error in parameters: some_url'

def test_make_url_with_good_date():
    assert '05/12/2017&date_req2=05/12/2018' in make_url(datetime.date(2017, 12, 5), datetime.date(2018, 12, 5))

# author: muroslav2909
# NOTE: end_date less than start_date. I think should be some validation inside method.
def test_make_url_with_end_date_less_than_start_date():
    assert '05/12/2018&date_req2=05/12/2017' in make_url(datetime.date(2018, 12, 5), datetime.date(2017, 12, 5))

def test_make_url_with_bad_date_format():
    try:
        make_url('bad_date_format', None)
    except AttributeError as e:
        assert "object has no attribute 'strftime'" in str(e)