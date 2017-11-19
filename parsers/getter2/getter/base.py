import arrow
from time import time        
from datetime import date, datetime
from decimal import Decimal  


import requests
from parsers.uploader import upload_datapoints


def format_date(date_string: str, fmt):
    """Convert *date_string* to YYYY-MM-DD"""
    return datetime.strptime(date_string, fmt).strftime("%Y-%m-%d")


def format_value(value_string: str, precision=2):
    return round(Decimal(value_string), precision)


def fetch(url):
    """Fetch content from *url* from internet."""
    content = requests.get(url).text
    if "Error" in content:
        raise ValueError(f"Cannot read from URL <{url}>")
    if 'Error in parameters' in content:
        raise Exception(f'Error in parameters: {url}')
    return content


def make_date(x):
    if '-' in str(x):
        return arrow.get(x).date() 
    else:
        return date(int(x), 1, 1)


class Timer:
    def __init__(self):
        self.start()     
        
    def start(self):
        self.start = time()
        self.elapsed = 0

    def stop(self):
        self.elapsed = time() - self.start
        return self

    def __repr__(self):
        #FIXME: add formatting to f-string
        t = round(self.elapsed, 2)
        return f'Time elapsed: {t} sec.'
        

class ParserBase(object):
    """   
    Must customise in child class:
       - observation_start_date 
       - url
       - parse_response        
    """
    
    # must change this to actual parser start date
    observation_start_date = '1990-01-02'
                                                                  
    def __init__(self, start_date=None, end_date=None):
        self.start_date = (make_date(start_date) 
                           or make_date(self.observation_start_date))    
        if end_date is None: 
            self.end_date = date.today()
        else: 
           self.end_date = make_date(end_date)

        self.response = None
        self.timer = Timer()
        self.parsing_result = []
   
    @property
    def url(self):
        raise NotImplementedError
    
    def parse_response(self):
        raise NotImplementedError
    
    @property
    def elapsed(self): 
        return self.timer.elapsed
        
    def _extract(self, downloader=fetch, verbose=False):
        if verbose:            
             print(f'Reading data from: {self.url}')
        self.response = downloader(self.url)
        self.parsing_result = self.parse_response(self.response) 
        return self
    
    def extract(self):
        self.timer.start() 
        self._extract(verbose=True)
        self.timer.stop()
        print(self.timer)
        return self
        
    @property
    def items(self):
        """Parsing result bound by start and end date"""
        result = []
        for item in self.parsing_result:
            dt = make_date(item['date'])        
            if self.start_date <= dt <= self.end_date:
                result.append(item)
        return result        

    def _upload(self):
        return upload_datapoints(self.items)
        
    def upload(self):
        self.timer.start()
        result_bool = self._upload()
        self.timer.stop()
        print(f'Uploaded {len(self.parsing_result)} datapoints')
        print(self.timer)
        return result_bool 
    
    def __repr__(self):
        def isodate(dt):
            return dt.strftime("%Y-%m-%d")
        def par(s):            
            return x.join(["\'"])
        class_name = self.__class__.__name__    
        start = isodate(self.start_date)
        end = isodate(self.end_date)
        return f'{class_name}({start}, {end})'    
