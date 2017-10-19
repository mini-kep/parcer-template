import pytest
import requests_mock
from decimal import Decimal
from parsers.getter.util import (fetch,
                                 format_date,
                                 format_value)

# FIXME: this line of code gets repeated 3 times below, do we have a chance to recylce it? a ixture/setup method?
#        url = "http://www.testpage.com"
#        with requests_mock.mock() as mocked_content:

#fixtures
@pytest.fixture(scope='module')
def mocked_content():
    with requests_mock.mock() as mocked_content:
        yield mocked_content

@pytest.fixture
def setup_url():
    url = "http://www.testpage.com"
    yield url


class Test_fetch:

    def test_fetch_good_response(self, mocked_content, setup_url):
        mocked_content.get(setup_url, text="good response from url")
        assert fetch(setup_url) == 'good response from url'

    def test_fetch_with_non_readable_URL_raises_ValueError(self, mocked_content, setup_url):
        with pytest.raises(ValueError):
            mocked_content.get(setup_url, text="Error reponse")
            fetch(setup_url)

    def test_fetch_returns_Error_in_parameters_raises_Exception(self, mocked_content, setup_url):
        with pytest.raises(Exception):
            mocked_content.get(setup_url, text="Error in parameters")
            fetch(setup_url)

class Test_format_date:
    def test_format_date_with_valid_date_string(self):
        assert format_date('2017-01-04T00:00:00', fmt='%Y-%m-%dT%H:%M:%S') == '2017-01-04'
        assert format_date('20170104', fmt="%Y%m%d") == '2017-01-04'

    def test_format_date_with_invalid_date_string_raises_ValueError(self):
        with pytest.raises(ValueError):
            format_date('bad_date_format', fmt='%Y-%m-%dT%H:%M:%S')
        with pytest.raises(ValueError):
            format_date('bad_date_format', fmt="%Y%m%d")

    def test_format_date_with_None_raises_TypeError(self):
        with pytest.raises(TypeError):
            format_date(None, fmt='%Y-%m-%dT%H:%M:%S')
        with pytest.raises(TypeError):
            format_date(None, fmt="%Y%m%d")

class Test_format_value:
    def test_format_value_with_valid_parameters(self):
        assert format_value('2.26') == Decimal('2.26')

    # FIXME:
    # EP: Very sceptical about this - we test for passing a list - but what is the likelihood we encounter a list in code?
    #     This test gives a flase sense we tested for invalid parameter, but such parameter will never be encountered,
    #     so what is the use? this is a bit fantasy case and rather useless test I think.
    #     Much more likely - a value like '1 020' is passed - we have seen it in cbr_fx.py
    #---------------------------------------------------------------------------------------------------------------------
    # JV :  I wanted to test, if program throws exception when some invalid parameter is passed.
    #       so I supposed that such situation can occur, that in source will be wrong value so parsed value
    #       will be also wrong. But aggre with you that '1 020' is more realistic situation which can be encountered
    #---------------------------------------------------------------------------------------------------------------------
    #
    # EP: this is exactly a situaltion for 
    #     <#9 in concentrate around practical risks in program execution, not fantasy situations>
    #     <https://github.com/mini-kep/intro/tree/master/testing_guidelines#checklist>
    #    '12 356' is highly preferred over a list as an input. (list deleted)
    
    
    def test_format_value_with_invalid_parameters(self):
        with pytest.raises(Exception):
            format_value('12 356' )

    def test_format_value_with_None_parameter(self):
        with pytest.raises(TypeError):
            format_value(None)
