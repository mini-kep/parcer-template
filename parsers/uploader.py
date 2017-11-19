"""Upload data from parsers to database."""
import requests
from time import sleep

from parsers.config import HEROKU_API_KEY as UPLOAD_API_TOKEN
from parsers.serialiser import to_json

UPLOAD_URL = 'https://minikep-db.herokuapp.com/api/datapoints'


def post(data, token=UPLOAD_API_TOKEN, endpoint=UPLOAD_URL):
    """Post *data* as json to API endpoint."""
    json_data = to_json(data)
    return requests.post(url=endpoint,
                         data=json_data,                             
                         headers={'API_TOKEN': token})
                         
def delete(params, token, endpoint=UPLOAD_URL):
    """Delete method."""
    return requests.delete(url=endpoint,
                           params=params,                             
                           headers={'API_TOKEN': token})
                         
def safe_post(data_chunk, upload_func=post, max_attempts=5, delay=10):
    """Repeat attempts for upload_func=post().
    
     Safety enhanced by max_attempts=5. Delay between attempots is 10ms.    
    
    Return:
        True, if success server response is 200.
        False, otherwise.
    """
    num_of_attempts = 0
    while(num_of_attempts < max_attempts):
        response = upload_func(data=data_chunk)
        if response.status_code == 200:
            break
        num_of_attempts += 1
        if num_of_attempts == max_attempts:
            return False
        sleep(delay)
    return True    
 
    
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
  
   
def upload_datapoints(gen, upload_func=safe_post):
    """Save data from *gen* list or iterator to database endpoint 
       via *upload_func* function. 
       
     Args:
         gen - list or generator of datapoints to send         
         max_attempts - how many times should uploaed try to upload (default: 5)
         delay - sleep time between attempts, ms (default: 10 )
     Returns:
         True on success (status code 200 reсieved from server)
         False otherwise
    """    
    for chunk in yield_chunks(gen):        
        if not upload_func(chunk):
            return False
    return True

# TODO: make Sender/Uploader classes
#       - add mock posters
#       - add timer

# code below not used / not imported

class Sender(): #pragma: no cover
    def __init__(self, data_chunk):
        self.gen = list(data_chunk)
        # add timer
        #self.elapsed = 0
        self.attempts = 0 
        self.max_attempts = 3 # times
        self.delay = 5 # seconds 
        self.code_200_received = False              
        
    def post(self):
        for self.attempts in range(1, self.max_attempts+1):
            response = post(data=self.data_chunk)
            if response.status_code == 200:
                self.code_200_received = True
                break
            sleep(self.delay)
        self.code_200_received = False     
    
    @property
    def status(self):
        return dict(datapoints=len(self.gen),
                    uploaded=self.code_200_received,
                    attempts=self.attempts)

    def __repr__(self):
        return f'Sender: {self.status}'
    
class Uploader: #pragma: no cover
    def __init__(self, gen, chunk_size=1000):
        gen = list(gen)
        self.size = len(gen)
        chunks = yield_chunks(gen, chunk_size)
        self.senders = [Sender(chunk) for chunk in chunks]
        
    @property    
    def elapsed(self):
        return sum([sender.elapsed for sender in self.senders])

    def run(self):
        for sender in self.senders:
            sender.post()

    @property
    def status(self):
        return [sender.status for sender in self.senders]
            
    def __repr__(self):        
        return (f'Uploader: {self.size} datapoints'
                 ', '
                f'{len(self.senders)} chunks'
                 '\n'
                f'{self.status}')

        