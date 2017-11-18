""" Download USD RUR official exchange rate from Bank of Russia web site."""


from parsers.ust.base import ParserBase, format_date, format_value, fetch
import xml.etree.ElementTree as ET


def make_url(start_date, end_date):
    if start_date <= end_date:
        start, end = (x.strftime('%d/%m/%Y') for x in [start_date, end_date])
        usd_code = 'R01235'
        return ("http://www.cbr.ru/scripts/XML_dynamic.asp"
                f"?date_req1={start}"
                f"&date_req2={end}"
                f"&VAL_NM_RQ={usd_code}")
    else:
        raise ValueError(f"<{end_date}> is less then {start_date}.")


def xml_text_to_stream(xml_text):
    root = ET.fromstring(xml_text)
    for child in root:
        # starting 02.06.1993 there are values like "2 153,0000"
        date_str = child.attrib['Date']
        date = format_date(date_str, fmt="%d.%m.%Y")
        value_str = child[1].text \
            .replace(",", ".") \
            .replace(" ", "") \
            .replace(chr(160), "")  # replace another space-like chraracter
        value = format_value(value_str, precision=4)
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


def get_cbr_er(start_date, end_date, downloader=fetch):
    url = make_url(start_date, end_date)
    xml_text = downloader(url)
    return map(transform, xml_text_to_stream(xml_text))


class USDRUR_CB(ParserBase):
    """EIA Brent oil price."""

    observation_start_date = '1992-07-01'
                                                                  
    @property
    def url(self):
        return make_url(self.start_date, self.end_date)
    
    def parse_response(self, response_text):
        gen = map(transform, xml_text_to_stream(response_text))
        return list(gen)


if __name__ == "__main__":
    dt = '1992-07-01'
    u = USDRUR_CB(dt, dt)
    u.extract()
    assert float(u.items[0]['value']) == 0.1253
    print(u.items[0])
