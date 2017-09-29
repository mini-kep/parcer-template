# -*- coding: utf-8 -*-
import datetime
import pytest

from parsers.helpers import DateHelper
from parsers.helpers import Markdown


class Test_today:
    def test_today(self):
        assert DateHelper.today() == datetime.date.today()


class Test_make_date:

    def test_returns_datetime_date_type(self):
        date = DateHelper.make_date('2007-01-25')
        assert isinstance(date, datetime.date)

    def test_accepts_YYYY_MM_DD(self):
        date = DateHelper.make_date('2007-01-25')
        assert date.day == 25
        assert date.month == 1
        assert date.year == 2007

    def test_accepts_slashed_format(self):
        date = DateHelper.make_date('2007/01/25')
        assert date.day == 25
        assert date.month == 1
        assert date.year == 2007

    def test_on_none_returns_today(self):
        assert DateHelper.make_date(None) == datetime.date.today()

    def test_make_date_on_empty_str_raises_Exception(self):
        with pytest.raises(Exception):
            DateHelper.make_date('')

    def test_make_date_on_no_argument_raises_TypeError(self):
        with pytest.raises(TypeError):
            DateHelper.make_date()

    def test_on_invalid_month_raises_ValueError(self):
        with pytest.raises(ValueError):
            DateHelper.make_date('2007-25-25')

    def test_with_fmt_on_valid_format_day_month_year(self):
        date = DateHelper.make_date('25-03-2000', fmt='%d-%m-%Y')
        assert date == datetime.date(2000, 3, 25)

    def test_on_invalid_format(self):
        with pytest.raises(Exception):
            assert DateHelper.make_date('25-03-2000', '%dk%m-%Y')


class Test_as_string():

    def test_on_expected_arg_type(self):
        date = datetime.date(2000, 1, 15)
        assert DateHelper.as_string(date) == '2000-01-15'

    def test_on_unexpected_arg_type(self):
        with pytest.raises(TypeError):
            assert DateHelper.as_string('2000-01-15')


class Test_Markdown:

    def test_add_dividers(self):
        assert Markdown.add_dividers(
            ['Branch', 'Commit']) == '| Branch | Commit |'
        # WONTFIX:
        # assert add_dividers([1, 2]) == ?
        # assert add_dividers([None]) == ?
        # assert add_dividers(['Branch', None]) == ?
        # also it can be parametrized with this different data

    def test_table(self):
        table1 = [
            ['Branch', 'Commit'],
            ['master', '0123456789abcdef'],
            ['staging', 'fedcba9876543210']
        ]
        md = Markdown.table(table1)
        assert md.startswith("|")
        assert 'Branch' in md
        assert 'fedcba9876543210' in md
        assert md == '| Branch | Commit |\n| ------ | ------ |\n| master | 0123456789abcdef |\n| staging | fedcba9876543210 |'

        # WONTFIX:
        # also what will happen if table1 will have not expected data. ex:
        # to_markdown(None)

    def test_shorten_link(self):
        url = ("http://www.gks.ru/wps/wcm/connect/"
               "rosstat_main/rosstat/ru/statistics/"
               "publications/catalog/"
               "doc_1140080765391")
        assert Markdown.short_link(
            url) == '[http://www.gks.ru/wps/wcm/connect/rossta...](http://www.gks.ru/wps/wcm/connect/rosstat_main/rosstat/ru/statistics/publications/catalog/doc_1140080765391)'


if __name__ == '__main__':
    pytest.main([__file__])
