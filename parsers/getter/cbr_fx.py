""" Download USD RUR official exchange rate from Bank of Russia web site."""


from datetime import date
import xml.etree.ElementTree as ET
import parsers.getter.util as util


def make_url(start_date, end_date):
    start, end = (x.strftime('%d/%m/%Y') for x in [start_date, end_date])
    usd_code = 'R01235'
    return ("http://www.cbr.ru/scripts/XML_dynamic.asp"
            f"?date_req1={start}"
            f"&date_req2={end}"
            f"&VAL_NM_RQ={usd_code}")


def xml_text_to_stream(xml_text):
    root = ET.fromstring(xml_text)
    for child in root:
        # starting 02.06.1993 there are values like "2 153,0000"
        date_str = child.attrib['Date']
        date = util.format_date(date_str, fmt="%d.%m.%Y")
        value_str = child[1].text \
            .replace(",", ".") \
            .replace(" ", "") \
            .replace(chr(160), "")  # replace abother space-like chraracter
        value = util.format_value(value_str, precision=4)
        yield {"date": date,
               "freq": "d",
               "name": "USDRUR_CB",
               "value": value}


def transform(datapoint):
    """Divide values before 1997-12-30 by 1000."""
    # FIXME: compare by strings is not so good
    if datapoint['date'] <= "1997-12-30":
        datapoint['value'] = round(datapoint['value'] / 1000, 4)
    return datapoint


def get_cbr_er(start_date, end_date, downloader=util.fetch):
    url = make_url(start_date, end_date)
    xml_text = downloader(url)
    return map(transform, xml_text_to_stream(xml_text))


if __name__ == "__main__":
    s = date(1992, 1, 1)
    e = date(2017, 10, 4)
    gen = get_cbr_er(s, e)
    for i in range(20):
        print(next(gen))
