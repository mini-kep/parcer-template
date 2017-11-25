import pytest

from datetime import date
from decimal import Decimal

from parsers.scrapper import Scrapper
from parsers.getter.cbr_fx import (make_url,
                                   transform,
                                   xml_text_to_stream,
                                   USDRUR)


@pytest.fixture
def fake_xml_content(url=None):
    return """<?xml version="1.0" encoding="windows-1251" ?>
              <ValCurs DateRange1="01.01.1992" DateRange2="02.01.2000">
              <Record Date="01.07.1992">
              <Nominal>1</Nominal>
              <Value>125,2600</Value></Record>
              </ValCurs>
              """


class Test_make_url:
    def test_make_url_with_good_args(self):
        url = make_url(date(2017, 12, 5), date(2018, 12, 5))
        assert '05/12/2017&date_req2=05/12/2018' in url

    def test_make_url_with_end_date_less_than_start_date_raises_ValueError_exception(
            self):
        with pytest.raises(ValueError):
            make_url(date(2018, 12, 5), date(2017, 12, 5))

    def test_make_url_with_bad_date_format_raises_TypeError_exception(self):
        with pytest.raises(TypeError):
            make_url('bad_date_format', None)


def test_xml_text_to_stream(fake_xml_content):
    gen = xml_text_to_stream(fake_xml_content)
    d = next(gen)
    assert d['date'] == '1992-07-01'
    assert d['freq'] == 'd'
    assert d["name"] == "USDRUR_CB"
    assert d['value'] == Decimal('125.2600')

# FIXME: method naming


class Test_transform:
    def test_transform_with_year_less_than_1997_devide_and_round_datapoint_value(
            self):
        datapoint = {'date': '1996-12-29', 'value': 11.25987}
        assert transform(datapoint) == {'date': '1996-12-29', 'value': 0.0113}

    def test_transform_with_year_over_than_1997_takes_original_datapoint_value(
            self):
        datapoint = {'date': '2017-09-25', 'value': 11.25987}
        assert transform(datapoint) == datapoint

    def test_transform_with_bad_args_raises_exception(self):
        datapoint = {'date': date(2017, 12, 5), 'value': 11.25987}
        with pytest.raises(TypeError):
            transform(datapoint)


# FIXME: change scrapper

class FakeScrapper(Scrapper):
    def get(self, url):
        return fake_xml_content()


def test_get_cbr_er():
    start = date(1992, 7, 1)
    end = date(2017, 10, 4)
    result = USDRUR(start, end, scrapper_class=FakeScrapper)
    result.extract()
    d = result.items[0]
    assert d['date'] == '1992-07-01'
    assert d['freq'] == 'd'
    assert d["name"] == "USDRUR_CB"
    assert d['value'] == Decimal('0.1253')
