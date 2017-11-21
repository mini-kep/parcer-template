import arrow
from datetime import date, datetime
from decimal import Decimal  
import requests
from urllib.parse import urlparse

from parsers.uploader import upload_datapoints
from parsers.timer import Timer 


def format_date(date_string: str, fmt):
    """Convert *date_string* with format *fmt* to YYYY-MM-DD."""
    return datetime.strptime(date_string, fmt).strftime("%Y-%m-%d")


def format_value(value_string: str, precision=2):
    """Convert float to Decimal."""
    return round(Decimal(value_string), precision)


def fetch(url):
    """Fetch content from *url* from internet."""
    content = requests.get(url).text
    if "Error" in content:
        raise ValueError(f"Cannot read from URL <{url}>")
    if 'Error in parameters' in content:
        raise Exception(f'Error in parameters: {url}')
    return content


def make_date(s):
    """Convert string s to datetime.date under flexible rules.
    Args:
        s - can be ISO date string (ex: '2017-01-01') 
            or int year (ex: 2017). Year always coerced to Jan 1. 
    Returns:        
        datetime.date
    """ 
    if s is None:
        return None
    elif '-' in str(s):
        return arrow.get(s).date() 
    else:
        return date(int(s), 1, 1)


class ParserBase(object):
    """Must customise in child class:
       - observation_start_date 
       - url
       - parse_response        
    """
    
    # must change this to actual parser start date
    observation_start_date = NotImplementedError("Must be a string like '1990-01-15'")
                                                                  
    def __init__(self, start_date=None, end_date=None, silent=True):
        obs = make_date(self.observation_start_date)
        self.start_date = (make_date(start_date) or obs)    
        if end_date is None: 
            self.end_date = date.today()
        else: 
           self.end_date = make_date(end_date)
        self.response = None
        self.parsing_result = []
        self.silent = silent      
        # tell abou class
        self.echo()
        self.echo(self.__class__.__doc__)
        self.echo(f'Date range: {self.start_date} {self.end_date}')

    @property
    def elapsed(self): 
        return self.timer.elapsed

    @property
    def url(self):
        raise NotImplementedError('Must return string with URL')
    
    @property    
    def site(self):
        return urlparse(self.url).netloc
    
    def parse_response(self, x):
        if not isinstance(x, str):
            raise TypeError(x) 
        raise NotImplementedError('Must return list or generator of dictionaries,' 
                                  'each dicttionary has keys: name, date, freq, value')
   
    def extract(self, downloader=fetch):
        # main worker
        with Timer() as t:
            self.response = downloader(self.url)
            self.parsing_result = self.parse_response(self.response) 
        #end    
        self.echo(f'Source: {self.site}')
        self.echo(f'Datapoints read in {t.elapsed:.2f} sec')
        self.echo(f'{len(self.parsing_result):5} datapoints total')
        self.echo(f'{len(self.items):5} in date range')
        return True
    
    def is_in_date_range(self, item):
        dt = make_date(item['date'])        
        return self.start_date <= dt <= self.end_date
        
    @property
    def items(self):
        """Return subset of parsing result bound by start and end date"""
        return [d for d in self.parsing_result if self.is_in_date_range(d)]

    #IDEA: should upload function be injected too, same as in extract()? 

    def upload(self):
        # nothing to uplaod?
        if not self.items:
            self.echo(f'No datapoints to upload in this date range')
            if self.parsing_result:    
                return True    
            else:
                return False
        # main worker
        with Timer() as t:
            result_bool = upload_datapoints(self.items)
        # end
        self.echo(f'{len(self.items):5} datapoints uploaded'
                  f' in {t.elapsed:.2f} sec')
        return result_bool 
    
    def echo(self, msg=''):
        if not self.silent:
            print(msg)
    
    def __repr__(self):
        def isodate(dt):
            return f"'{dt.strftime('%Y-%m-%d')}'"
        start = isodate(self.start_date)
        end = isodate(self.end_date)
        return f'{self.__class__.__name__}({start}, {end})'
