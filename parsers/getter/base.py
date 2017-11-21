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
        raise ValueError(f"Cannot read from: {url}")
    #if 'Error in parameters' in content:
    #    raise ValueError(f'Error in url parameters: {url}')
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


class Logger(object):
    """Print comments to console."""    
    def __init__(self, silent=True):
        self.silent = silent
    
    def echo(self, msg=''):
        if not self.silent:
            print(msg)            


class Scrapper(object):    
    """Download data from url."""    
    def __init__(self, download_func, silent=True):
        self.download_func = download_func
        self.logger = Logger(silent)
    
    @staticmethod        
    def site(url):
        return urlparse(url).netloc
        
    def get(self, url):  
        with Timer() as t:
            response = self.download_func(url)
        self.logger.echo(f'Read data from: {self.site(url)}')
        self.logger.echo(t)       
        return response

class Uploader(object):
    """Post to database."""  
    def __init__(self, upload_func, silent=True):
        self.upload_func = upload_func
        self.logger = Logger(silent)    
        
    def post(self, data):  
        with Timer() as t:
            result_bool = self.upload_func(data)
        self.logger.echo(f'{len(data)} datapoints uploaded')
        self.logger.echo(t)        
        return result_bool
    
# TODO: move to tests        
s = Scrapper(lambda x: x)
assert '123' == s.get('123')

u = Uploader(lambda x: True)
assert u.post([])
    
DATE_FLOOR = make_date(1864) 

class ParserBase(object):
    """Must customise in child class:
       - observation_start_date 
       - url
       - get_datapoints        
    """
    
    # in child class must change this to actual parser start date - 
    # the earlier date on which the parser can return data
    observation_start_date = NotImplementedError("Must be a string like '1990-01-15'")
     
    def _init_start(self, start_date):
        # HACK: make this class testable 
        try:
            obs = make_date(self.observation_start_date)
        except NotImplementedError:
            obs = DATE_FLOOR  
        return make_date(start_date) or obs        

    def _init_end(self, end_date):
        if end_date:
            return make_date(end_date)
        else:           
            return date.today()
                                                             
    def __init__(self, start_date=None, 
                       end_date=None, 
                       silent=True,
                       download_func = fetch,
                       upload_func = upload_datapoints):
        self.logger = Logger(silent)
        self.scrapper = Scrapper(download_func, silent)
        self.uploader =  Uploader(upload_func, silent)
        self.parsing_result = []
        self.start_date = self._init_start(start_date)
        self.end_date = self._init_end(end_date)
        # tell about class init        
        self.logger.echo(self.__class__.__doc__)
        self.logger.echo(f'Date range: {self.start_date} {self.end_date}')

    @property
    def url(self):
        raise NotImplementedError('Must return string with URL, '
                                  'usually based on start and end date '
                                  'or frequency.')
    
    @staticmethod
    def get_datapoints(response_str):
        raise NotImplementedError('Must return list or generator of dictionaries. ' 
                                  'Each dicttionary has keys: '
                                  'name, date, freq, value')
    
    def parse_response(self, response_str):
        if not isinstance(response_str, str):
            raise TypeError(response_str) 
        return self.get_datapoints(response_str)   
   
    def extract(self):
        response = self.scrapper.get(self.url)
        self.parsing_result = self.parse_response(response) 
        self.log_extract_result()
        return True
    
    def log_extract_result(self):
        n = len(self.parsing_result)
        k = len(self.items)
        self.logger.echo(f'{n} datapoints extracted, {k} in date range')
    
    def is_in_date_range(self, item):
        dt = make_date(item['date'])        
        return self.start_date <= dt <= self.end_date
        
    @property
    def items(self):
        """Return subset of parsing result bound by start and end date"""
        return [d for d in self.parsing_result if self.is_in_date_range(d)]

    def upload(self):
        # nothing to upload?
        if not self.parsing_result:
            self.logger.echo('No datapoints or parser not run.')
            return False
        if not self.items:
            self.logger.echo(f'No datapoints in date range')
            return False        
        return self.uploader.post(self.items)        
    
    def __repr__(self):
        def isodate(dt):
            return f"'{dt.strftime('%Y-%m-%d')}'"
        start = isodate(self.start_date)
        end = isodate(self.end_date)
        return f'{self.__class__.__name__}({start}, {end})'
