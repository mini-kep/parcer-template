# FIXME: change endpoint
UPLOAD_URL = 'https://minikep-db.herokuapp.com/api/incoming'

# FIXME: unsecure
UPLOAD_API_TOKEN = '123'

"""Upload data from parsers to database"""
import requests
import json
import decimal


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


def upload_datapoints(gen, upload_func=post):
    """Save data from generator *gen* to database endpoint.
    
       Returns:
          True on success (status code 200),
          False otherwise
    """
    response = upload_func(data=to_json(gen))
    if response.status_code == 200:
        return True
    else:
        return False
