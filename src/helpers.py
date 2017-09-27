# -*- coding: utf-8 -*-
import arrow
from datetime import datetime

class DateHelper(object):
    def today():
        return arrow.now().date()
    
    def make_date(dt_string: str, fmt=None):
        if fmt is None:
            return arrow.get(dt_string).date()
        # witout else will work correctly
        try:
            return datetime.strptime(dt_string, fmt).date()
        except ValueError:
            msg = f"Error parsing date <{dt_string}> with format <{fmt}>"
            raise ValueError(msg)
       
    def as_string(date):   
        try:
           return date.strftime("%Y-%m-%d")
        except AttributeError:
            raise TypeError(f"<{date}> must be datetime.date or similar type")
