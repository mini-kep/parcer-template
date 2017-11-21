"""
Delete datapoints based on parameters.

WARNING: use with caution!

"""
import sys
from pathlib import Path

class PathContext():
    def __init__(self):
        self.path = str(Path(__file__).parent)

    def __enter__(self):
        sys.path.insert(0, self.path)

    def __exit__(self, exc_type, exc_value, traceback):
        sys.path.remove(self.path)

with PathContext():
    from parsers.uploader import delete

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
    #response = delete(d, token)
    
    
params = dict(freq='d', 
              name='UST_30YEARDISPLAY')
response = delete(params, token)
    