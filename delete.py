"""
Delete datapoints based on parameters.

WARNING: use with caution!

"""

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

for name in names:
    d = dict(freq='d', 
             name=name, 
             start_date='2017-04-14', 
             end_date='2017-04-14')
    print(d)
    token = None
    response = delete(d, token)
    print(response)