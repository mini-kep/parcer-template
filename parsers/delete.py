import requests
from parsers.config import UPLOAD_URL
                         
def delete(params, token, endpoint=UPLOAD_URL):
    """Delete method."""
    return requests.delete(url=endpoint,
                           params=params,                             
                           headers={'API_TOKEN': token})
                           
                           
if __name__ == "__main__":
    names = ["UST_10YEAR", 
  "UST_1MONTH", 
  "UST_1YEAR", 
  "UST_20YEAR", 
  "UST_2YEAR", 
  "UST_30YEAR", 
  "UST_30YEARDISPLAY", 
  "UST_3MONTH", 
  "UST_3YEAR", 
  "UST_5YEAR", 
  "UST_6MONTH", 
  "UST_7YEAR"
]
    token = None

    for name in names:
        d = dict(freq='d', 
                 name=name, 
                 start_date='2017-04-14', 
                 end_date='2017-04-14')
        assert 200 == delete(d, token).status_code        
        
    params = dict(freq='d', 
                  name='UST_30YEARDISPLAY')
    response = delete(params, token)
    assert 200 == response.status_code
                                   