""" Download USD RUR official exchange rate from Bank of Russia web site."""

from datetime import date
import requests
import xml.etree.ElementTree as ET
from decimal import Decimal

from helpers import DateHelper

# R01235 is USD code


def make_url(start_date, end_date):
    start, end = (x.strftime('%d/%m/%Y') for x in [start_date, end_date])
    return ("http://www.cbr.ru/scripts/XML_dynamic.asp"
            f"?date_req1={start}"
            f"&date_req2={end}"
            "&VAL_NM_RQ=R01235")


def to_float(string):
    # starting 02.06.1993 there are values like "2 153,0000"
    s = string.replace(",", ".") \
              .replace(chr(160), "")
    try:
        return float(s)
    except ValueError:
        raise ValueError("Error parsing value <{}>".format(string))


def transform(datapoint):
    """Divide values before 1997-12-30 by 1000."""
    # FIXME: compare by strings is not so good
    if datapoint['date'] <= "1997-12-30":
        datapoint['value'] = round(datapoint['value'] / 1000, 4)
    return datapoint


def xml_text_to_stream(xml_text):
    root = ET.fromstring(xml_text)
    for child in root:
        date = DateHelper.make_date(child.attrib['Date'], fmt="%d.%m.%Y")
        value = round(Decimal(to_float(child[1].text)),4)
        yield {"date": DateHelper.as_string(date),
               "freq": "d",
               "name": "USDRUR_CB",
               "value": value}


def get_xml(url):
    xml_text = requests.get(url).text
    if 'Error in parameters' in xml_text:
        raise Exception(f'Error in parameters: {url}')
    else:
        return xml_text


def get_cbr_er(start_str, end_str):
    url = make_url(start_str, end_str)
    xml_text = get_xml(url)
    return map(transform, xml_text_to_stream(xml_text))


if __name__ == "__main__":
    s = date(1991, 7, 1)
    e = date(2017, 9, 26)
    # gen = get_cbr_er(s, e)
    # a = next(gen)
    # assert a == {'date': '1992-07-01', 'freq': 'd',
    #             'name': 'USDRUR_CB', 'value': 0.1253}
