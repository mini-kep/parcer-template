# -*- coding: utf-8 -*-
import datetime
import pytest

from helpers import DateHelper

class Test_today:
    def test_today(self):
        assert DateHelper.today() == datetime.date.today()

class Test_make_date:
    def test_make_date_on_valid_input(self):
        date = DateHelper.make_date('2007-01-25')
        assert date.day == 25
        assert date.month == 1
        assert date.year == 2007

    def test_make_date_on_valid_input_in_slashed_format(self):
        date = DateHelper.make_date('2007/01/25')
        assert date.day == 25
        assert date.month == 1
        assert date.year == 2007

    def test_make_date_on_valid_input_none(self):
        assert DateHelper.make_date(None) == datetime.date.today()

    def test_make_date_on_invalid_input_out_of_range(self):
        with pytest.raises(ValueError):
            DateHelper.make_date('2007-25-01')

    def test_make_date_on_invalid_input_empty_str_raises_exception(self):
        with pytest.raises(Exception):
            DateHelper.make_date('')

    def test_make_date_on_no_argument_empty_raises_type_error(self):
        with pytest.raises(TypeError):
            DateHelper.make_date()