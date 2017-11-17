"""Upload data from parsers to database."""
import requests
import json
import decimal
from time import sleep


UPLOAD_URL = 'https://minikep-db.herokuapp.com/api/datapoints'

# FIXME: unsecure as a constant
UPLOAD_API_TOKEN = '123'

# COMMENTS (NOT TODO):
#    many list() calls

def convert_decimal_to_float(obj):
    """Helper function to serilaise Decimals to float type.
       Used inside to_json(). 
    """
    if isinstance(obj, decimal.Decimal):
        return float(obj)
    raise TypeError


def to_json(gen): 
    """Convert generator *gen* to json string.    
    
    Returns:
        string
    """
    return json.dumps(list(gen), default=convert_decimal_to_float)


def post(data, token=UPLOAD_API_TOKEN, endpoint=UPLOAD_URL):
    """Post *data* as json to API endpoint."""
    json_data = to_json(data)
    return requests.post(url=endpoint,
                         data=json_data,                             
                         headers={'API_TOKEN': token})

# COMMENT: may return server response instead of bool
    
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
  
   
def upload_datapoints(gen, upload_func=safe_post, upload_kwarg={}):
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
        if not upload_func(chunk, upload_kwarg):
            return False
    return True
