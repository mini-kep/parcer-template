UPLOAD_URL = 'https://minikep-db.herokuapp.com/api/datapoints'

# FIXME: unsecure
UPLOAD_API_TOKEN = '123'

"""Upload data from parsers to database"""
import requests
import json
import decimal
from time import sleep


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


def post(data, endpoint=UPLOAD_URL, token=UPLOAD_API_TOKEN):
    """Post *data* json to API endpoint."""
    return requests.post(url=endpoint,
                         data=data,                             
                         headers={'API_TOKEN': token})


def upload_datapoints(gen, upload_func=post, chunk_size=1000, max_attempts=5, delay=10):
    """Save data from *gen* list or interator by chunks to database endpoint.
    
     Args:
         chunk_size - number of datapoints to send at one time
         max_attempts - how many times should uploaed try to upload
         delay - sleep time between attempts, ms
     Returns:
         True on success (status code 200 revieved from server),
         False otherwise
    """
    data_chunks = [gen[i:i + chunk_size] for i in range(0, len(gen), chunk_size)]
    for block in data_chunks:
        json_block = to_json(block)
        num_of_attempts = 0
        while(num_of_attempts < max_attempts):
            response = upload_func(data=json_block)
            if response.status_code == 200:
                break
            num_of_attempts += 1
            if num_of_attempts == max_attempts:
                return False
            sleep(delay)
    return True
