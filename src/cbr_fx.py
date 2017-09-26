""" Download USD RUR official exchange rate from Bank of Russia web site."""

from datetime import date
import requests
import xml.etree.ElementTree as ET

from helpers import DateHelper


def as_cbr_date(dt):    
    if isinstance(dt, date):
        return dt.strftime('%d/%m/%Y')
    else:
        raise TypeError(dt)

def make_url(start_str=None, end_str=None):
    fmt = '%d/%m/%Y'
    _start = DateHelper.get_start(start_str, '1992-07-01')
    _end = DateHelper.get_end(end_str)
    start, end = (x.strftime(fmt) for x in [_start, _end])
    return ("http://www.cbr.ru/scripts/XML_dynamic.asp"
            f"?date_req1={start}"
            f"&date_req2={end}&VAL_NM_RQ=R01235")


def to_float(string):
    # starting 02.06.1993 there are values like "2 153,0000"
    s = string.replace(",",".") \
              .replace(chr(160),"")
    try:
        return float(s)
    except ValueError:
        raise ValueError("Error parsing value <{}>".format(string))
            

def transform(datapoint):
     """Divide values before 1997-12-30 by 1000."""
     #FIXME: compare by strings is not good
     if datapoint['date'] <= "1997-12-30":
         datapoint['value'] = round(datapoint['value'] / 1000, 4)
     return datapoint


def xml_text_to_stream(xml_text):        
        root = ET.fromstring(xml_text)
        for child in root:
            date = DateHelper.to_date(child.attrib['Date'], "%d.%m.%Y")
            value = to_float(child[1].text)
            yield {"date": date,
               "freq": "d",
               "name": "USDRUR_CB",
               "value": value}  
            
def get_cbr_er(start_str, end_str):
    url= make_url(start_str, end_str)
    xml_text = requests.get(url).text
    for d in map(transform, xml_text_to_stream(xml_text)):
        yield d
    
            
if __name__ == "__main__":
    gen = get_cbr_er(None, None)    
    a = next(gen)
    assert a == {'date': '1992-07-01', 'freq': 'd', 
                 'name': 'USDRUR_CB', 'value': 0.1253}