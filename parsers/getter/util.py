from datetime import datetime
from decimal import Decimal
import requests


def fetch(url):
    """Fetch content from *url* from internet."""
    content = requests.get(url).text
    if "Error" in content:
        raise ValueError(f"Cannot read from URL <{url}>")
    if 'Error in parameters' in content:
        raise Exception(f'Error in parameters: {url}')
    return content


def format_date(date_string: str, fmt):
    return datetime.strptime(date_string, fmt).strftime("%Y-%m-%d")


def format_value(value_string: str, precision=2):
    return round(Decimal(value_string), precision)
