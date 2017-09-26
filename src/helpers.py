# -*- coding: utf-8 -*-
import arrow
from datetime import datetime

class DateHelper(object):
    def today():
        return arrow.now().date()
    
    def make_date(dt, default=None):
        return arrow.get(dt).date() 
        
    def get_start(dt, default: str):
        if dt is None:
            return DateHelper.make_date(default)
        else:
            return DateHelper.make_date(dt)

    def get_end(dt):
        if dt is None:
            return DateHelper.today()
        else:
            return DateHelper.make_date(dt)
        
    def to_date(date_string, fmt):
        try:
            return datetime.strptime(date_string, fmt).strftime("%Y-%m-%d")
        except ValueError:
            raise ValueError(f"Error parsing date <{date_string}>")
            