import requests
from urllib.parse import urlparse

from parsers.helpers import Timer, Logger


def fetch(url):
    """Fetch content from *url* from internet."""
    content = requests.get(url).text
    if "Error" in content:
        raise ValueError(f"Cannot read from: {url}")
    return content

    
class Scrapper(object):    
    """Download data from url."""    
    def __init__(self, download_func=fetch, silent=True):
        self.download_func = download_func
        self.logger = Logger(silent)
    
    @staticmethod        
    def site(url):
        return urlparse(url).netloc
        
    def get(self, url):  
        with Timer() as t:
            response = self.download_func(url)
        self.logger.echo(f'Read data from <{self.site(url)}>', t)
        return response
