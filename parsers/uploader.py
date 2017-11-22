"""Upload data from parsers to database."""
import requests
from time import sleep

from parsers.config import HEROKU_API_KEY as UPLOAD_API_TOKEN, UPLOAD_URL
from parsers.serialiser import to_json
from parsers.helpers import Logger, Timer


def post(data, token=UPLOAD_API_TOKEN, endpoint=UPLOAD_URL):
    """
    Post *data* as json to API endpoint.
    Returns: status_code
    """
    json_data = to_json(data)
    return requests.post(url=endpoint,
                         data=json_data,                             
                         headers={'API_TOKEN': token}).status_code
                         
def delete(params, token, endpoint=UPLOAD_URL):
    """Delete method."""
    return requests.delete(url=endpoint,
                           params=params,                             
                           headers={'API_TOKEN': token})
 
    
def yield_chunks(gen, chunk_size=1000):
    """Split generator or list into smaller parts.
    
    Args:
        gen - list or generator of datapoints to send 
        chunk_size - number of datapoints to send at one time
    Yields:    
        list of size *chunk_size* or smaller
    """
    gen = list(gen)
    for i in range(0, len(gen), chunk_size):        
        yield gen[i:i + chunk_size]    
  
class Poster():
    """Post to database:
     - attempts to post to db and delay between attempts (safe post mechanism)
     - collects response status 
     - holds number of attempts     
    """
    max_attempts = 3  # times
    delay = 5  # seconds
    
    def __init__(self, data_chunk, post_func=post, silent=True):
        self.gen = list(data_chunk)
        self.post_func = post_func
        self.attempts = 0
        self.status_code = None

    def post(self):
        """Posts chunk of data to database using self.post()."""
        for self.attempts in range(1, self.max_attempts + 1):
            self.status_code = self.post_func(data=self.gen)
            if self.status_code == 200:
                break
            sleep(self.delay)
            
    @property            
    def is_success(self):
        return self.status_code == 200
        
    @property
    def status_message(self):
        n = len(self.gen)
        if self.is_success:
            return f'Uploaded {n} datapoints in {self.attempts} attempt(s)'
        else:
            return f'Failed to upload {n} datapoints in {self.attempts} attempt(s)'

    def __repr__(self):
        return f'Poster: {self.attempts} attempts, status code {self.status_code}'


class Uploader(object):
    """Post data to database.
    
    Handles:
    - separate incoming data to chunks
    - make a queue of Sender instances, one per chunk
    - invoke Senders' .post() methods
    - provide logging to console
    - provide collection of posting results (number of attempts of each sender)
    """
    def __init__(self, poster_class=Poster, silent=False):
        self.logger = Logger(silent)   
        self.poster_class = poster_class
        self.posters = []
        self.logger = Logger(silent)
        
    def make_queue(self, data):
        return [self.poster_class(data_chunk) for data_chunk in yield_chunks(data)]
        
    def post(self, data):        
        with Timer() as t:
            self.posters = self.make_queue(data) 
            for poster in self.posters:
                poster.post()    
                self.logger.echo(poster.status_message)                         
        self.logger.echo('Finished upload', t)
        return self.is_success
    
    @property
    def is_success(self):
        return all([p.is_success for p in self.posters])
 

if __name__ == "__main__":
    data = [
  {
    "date": "1999-12-31", 
    "freq": "a", 
    "name": "GDP_yoy", 
    "value": 106.4
  }, 
  {
    "date": "2000-12-31", 
    "freq": "a", 
    "name": "GDP_yoy", 
    "value": 110.0
  }]
    
    p = Poster(data)
    p.post()
    assert p.status_code == 200
    
    u = Uploader()
    u.post(data)
    for sender in u.posters:
        assert sender.status_code == 200
