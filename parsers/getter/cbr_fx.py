""" Download USD RUR official exchange rate from Bank of Russia web site."""


from parsers.getter.base import ParserBase, format_date, format_value
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
    # FIXME: compare by strings is not good
    if datapoint['date'] <= "1997-12-30":
        datapoint['value'] = round(datapoint['value'] / 1000, 4)
    return datapoint


class USDRUR(ParserBase):
    """Official USD/RUR exchange rate (Bank of Russia)"""
    observation_start_date = '1992-07-01'
    freq = 'd'

    @property
    def url(self):
        return make_url(self.start_date, self.end_date)

    @staticmethod
    def get_datapoints(response):
        gen = map(transform, xml_text_to_stream(response))
        return list(gen)


if __name__ == "__main__":  # pragma: no cover
    dt = '1992-07-01'
    u = USDRUR(dt, dt)
    u.extract()
    assert float(u.items[0]['value']) == 0.1253
    print(u.items[0])
