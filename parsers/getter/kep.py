from decimal import Decimal
import pandas as pd
import numpy as np


def make_url(freq):
    return ('https://raw.githubusercontent.com/mini-kep/'
            'parser-rosstat-kep/master/data/processed/latest/'
            f'df{freq}.csv')


assert make_url('a') == ('https://raw.githubusercontent.com/mini-kep/'
                         'parser-rosstat-kep/master/data/processed/latest/'
                         'dfa.csv')


def read_csv(source):
    """Wrapper for pd.read_csv(). Treats first column at time index.
       Returns:
           pd.DataFrame()
    """
    converter_arg = dict(converters={0: pd.to_datetime}, index_col=0)
    return pd.read_csv(source, **converter_arg)


def get_dataframe_from_repo(freq):
    """Code to read pandas dataframes from stable URL."""
    url = make_url(freq)
    return read_csv(url)


def yield_all_dicts(freq):
    df = get_dataframe_from_repo(freq)
    d = df.to_dict('index')
    for dt in d.keys():
        for name, value in d[dt].items():
            yield {'date': dt.strftime("%Y-%m-%d"),
                   'freq': 'd',
                   'name': name,
                   'value': round(Decimal(value),4)}


def is_valid(d):
    negative_conditions = []
    negative_conditions.append(d['name'] in ['year', 'qtr', 'month'])
    negative_conditions.append(np.isnan(float(d['value'])))
    return not any(negative_conditions)


def yield_dicts(freq):
    return filter(is_valid, yield_all_dicts(freq))


if "__main__" == __name__:
    a = next(yield_dicts('a'))
