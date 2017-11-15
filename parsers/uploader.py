# FIXME: change endpoint
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


def upload_datapoints(ust_data, upload_func=post):
    """Save data from the ust data list by chunks to database endpoint.
    
       Returns:
          True on success (status code 200),
          False otherwise
    """
    ust_data_chunks = [ust_data[i:i + 1000] for i in range(0, len(ust_data), 1000)]
    for ust in ust_data_chunks:
        json_ust_data = to_json(ust)
        num_of_attempts = 0
        while(num_of_attempts < 5):
            response = upload_func(data=json_ust_data)
            if response.status_code == 200:
                break
            num_of_attempts += 1
            if num_of_attempts == 5:
                return False
            sleep(10)
    return True
