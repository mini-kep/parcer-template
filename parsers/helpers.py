# -*- coding: utf-8 -*-
import arrow
from datetime import datetime


def today():
    """Get today date.

    Returns:
        datetime.date
    """
    return arrow.now().date()

def make_date(date_string: str, fmt='%Y-%m-%d'):
    """Create a date from *date_string* using *fmt* date format.
    
    Args:
        *date_string*(str) - text string like '2017-09-01'
        fmt(str) - format string like '%Y-%m-%d'

    Returns:
        datetime.date
    """
    if date_string is None:
        return None
    try:
        return datetime.strptime(date_string, fmt).date()
    except ValueError:
        msg = f"Error parsing date <{date_string}> with format <{fmt}>"
        raise ValueError(msg)

def as_string(date):
    """Convert date to "%Y-%m-%d" format as in '2017-09-25'.

    Args:
        date (datetime.date)

    Returns:
        str, formatted as YYYY-MM-DD
    """
    try:
        return date.strftime("%Y-%m-%d")
    except AttributeError:
        raise TypeError(f"<{date}> must be datetime.date or similar type")

assert make_date(None) is None


def interpret_frequency(freq):
    """Make a text description of frequency based on *freq* string."""
    mapper = dict(a='annual',
                  q='quarterly',
                  m='monthly',
                  w='weekly',
                  d='daily')
    return mapper[freq].capitalize()


class Markdown:
    def add_dividers(row):
        content = " | ".join(row)
        return "| {} |".format(content)

    def table(rows):
        """Translate *rows* to markdown table. Use first row as header.

           Args:
               rows(list) - list of strings, each sting is table column element

           Returns:
               string with markdown table.
        """
        table = list(rows)
        header = table[0]
        horiz = ["-" * len(x) for x in header]
        body = table[1:]

        table = [header, horiz]
        table.extend(body)

        table = [Markdown.add_dividers(row) for row in table]
        return '\n'.join(table)

    # FIXME: there are no test for short_link
    def short_link(url, n=40):
        """Shorten *url* to *n* characters and provide markdown link"""
        if len(url) > n:
            text = url[:n] + '...'
        else:
            text = url
        return f'[{text}]({url})'
