import datetime
import mock
import pytest
from decimal import Decimal

from parsers.getter.cbr_fx import make_url, to_float, transform, get_cbr_er, xml_text_to_stream, get_xml
from parsers.getter.tests.fixtures import foo_obj


def test_get_xml_without_exception(mocker):
    return_value = foo_obj(**{"text": 'expected_text'})
    mocker.patch('requests.get', mock.MagicMock(return_value=return_value))
    assert get_xml("some_url") == 'expected_text'


def test_get_xml_with_exception(mocker):
    return_value = foo_obj(**{"text": 'Error in parameters'})
    mocker.patch('requests.get', mock.MagicMock(return_value=return_value))
    with pytest.raises(Exception) as e:
        get_xml("some_url")
        assert str(e.value) == 'Error in parameters: some_url'


def test_make_url_with_good_args():
    assert '05/12/2017&date_req2=05/12/2018' in make_url(
        datetime.date(2017, 12, 5), datetime.date(2018, 12, 5))

# author: muroslav2909
# NOTE: end_date less than start_date. I think should be some validation
# inside method.


def test_make_url_with_end_date_less_than_start_date():
    assert '05/12/2018&date_req2=05/12/2017' in make_url(
        datetime.date(2018, 12, 5), datetime.date(2017, 12, 5))


def test_make_url_with_bad_date_format():
    with pytest.raises(AttributeError) as e:
        make_url('bad_date_format', None)
    assert "object has no attribute 'strftime'" in str(e.value)


def test_to_float_with_good_args():
    assert to_float('2 153,0000') == 2153.0


def test_to_float_with_bad_args():
    string = '2!153/0000'
    with pytest.raises(ValueError) as e:
        to_float(string)
    assert str(e.value) == "Error parsing value <{}>".format(string)


def test_transform_with_year_less_than_1997():
    datapoint = {'date': '1996-12-29', 'value': 11.25987}
    assert transform(datapoint) == {'date': '1996-12-29', 'value': 0.0113}


def test_transform_with_year_over_than_1997():
    datapoint = {'date': '2017-09-25', 'value': 11.25987}
    assert transform(datapoint) == datapoint


def test_transform_with_bad_args():
    datapoint = {'date': datetime.date(2017, 12, 5), 'value': 11.25987}
    with pytest.raises(TypeError) as e:
        transform(datapoint)
    assert str(
        e.value) == "'<=' not supported between instances of 'datetime.date' and 'str'"


def test_get_cbr_er(mocker):
    start_str = '1998-12-05'
    end_str = '1998-12-08'
    mocker.patch('parsers.getter.cbr_fx.make_url', mock.MagicMock(
        return_value='http://www.cbr.ru/scripts/XML_dynamic.asp?date_req1=05/12/1998&date_req2=08/12/1998&VAL_NM_RQ=R01235'))
    result = [{'date': start_str,
               'freq': 'd',
               'name': 'USDRUR_CB',
               'value': Decimal('19.5700')},
              {'date': end_str,
               'freq': 'd',
               'name': 'USDRUR_CB',
               'value': Decimal('20.4000')}]
    assert list(get_cbr_er(start_str, end_str)) == result
