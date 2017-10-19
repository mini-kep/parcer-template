"""Upload data from parsers to database""".

import requests
import json

# EP: note the constants always start of file and capitalised, PEP8
#     <https://www.python.org/dev/peps/pep-0008/#constants>

# Hardcoded params for uploading data to database 
UPLOAD_URL = 'https://minikep-db.herokuapp.com/api/incoming'
UPLOAD_API_TOKEN = '123'


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


def upload_to_database(gen, endpoint=UPLOAD_URL, token=UPLOAD_API_TOKEN)):
    """Save data from generator *gen* to database endpoint.
    
    Returns:
        True on success (status code 200),
        False otherwise     
    """
    _data = to_json(gen)
    response = requests.post(url=endpoint,
                             data=_data,                             
                             headers={'API_TOKEN': token})
    if response.status_code == 200:
        return True
    else:
        return False
