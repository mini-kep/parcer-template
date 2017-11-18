import arrow
from parsers.uploader import upload_datapoints
import parsers.getter.util as util
from time import time         

def make_date(x):
    if '-' in str(x):
        return arrow.get(x).date() 
    else:
        return date(int(x), 1, 1)

class GetterBase(object):
    """
    Three things must be customised:
        observation_start_date 
        url 
        parse_response        
    """
    
    # must change this to actual parser start date
    observation_start_date = make_date('1990-01-01')
                                                                  
    def __init__(self, start_date, end_date=None):
        self.start_date= make_date(start_date) or self.observation_start_date    
        if end_date is None: 
            self.end_date = date.today()
        else: 
           self.end_date = make_date(end_date)
        self.response = None
        self.elapsed = None
        self.parsing_result = []
   
    @property
    def url(self):
        raise NotImplementedError
    
    def parse_response(self):
        raise NotImplementedError
    
    def _extract(self, downloader=util.fetch):
        self.response = downloader(self.url)
        self.parsing_result = self.parse_response(self.response) 
        return self
    
    def extract(self):
        start_time = time() 
        self._extract()
        self.elapsed = round(time() - start_time, 2)
        print(f'Read data from: {self.url}\nTime elapsed: {self.elapsed} sec.')
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

    def upload(self):
        return upload_datapoints(self.items)
    
    def __repr__(self):
        def isodate(dt):
            return dt.strftime("%Y-%m-%d")
        start = isodate(self.start_date)
        end = isodate(self.end_date)
        return f'{self.__class__.__name__}(\'{start}\', \'{end}\')'