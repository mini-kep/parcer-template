# -*- coding: utf-8 -*-
import datetime
import pytest

from helpers import DateHelper

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


# TODO below: do type type checks 
# TODO below: get_end and get_start need min 2 methods becuase if-then 

class Test_get_end:
    def test_on_none_argument_returns_today(self):
        assert DateHelper.get_end(None) == datetime.date.today()

class Test_get_start:
    def test_on_none_argument_returns_date(self):
        #EP: this is actually unintented use, must change default to string
        #    see actual use of get_start in parsers.py        
        date = datetime.date(2000, 1, 25)
        assert DateHelper.get_start(dt=None, default=date) == date

# note: to_date is likely to be refactored
class Test_to_date:
    def test_on_valid_format_day_month_year(self):
        assert DateHelper.to_date('13-02-1254','%d-%m-%Y') == '1254-02-13'
    def test_on_invalid_format(self):
        with pytest.raises(Exception):
            assert DateHelper.to_date('13-02-1254','%dk%m-%Y') == '1254-02-13'

# After tests: need doctsrings for DateHelper. 
# TODO below: get_end and get_start need min 2 methods becuase if-then 
            
if __name__ == '__main__':
    pytest.main([__file__])
    


