import pandas as pd
import numpy as np
import io

from parsers.getter.base import ParserBase, format_value


def make_url(freq):
    return ('https://raw.githubusercontent.com/mini-kep/'
            'parser-rosstat-kep/master/data/processed/latest/'
            f'df{freq}.csv')


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


def yield_all_dicts(df, freq):
    d = df.to_dict('index')
    for dt in d.keys():
        for name, value in d[dt].items():
            yield {'date': dt.strftime("%Y-%m-%d"),
                   'freq': freq,
                   'name': name,
                   'value': format_value(value)}


def is_valid(d):
    # no datapoints with year, qtr or month - these are supplementary variables
    # we exclide them here
    negative_conditions = [d['name'] in ['year', 'qtr', 'month']]
    # no NaN values
    negative_conditions.append(np.isnan(float(d['value'])))
    # are any negative conditions met?
    return not any(negative_conditions)


class KEP_Annual(ParserBase):
    """Annual data from KEP publication (Rosstat)"""
    observation_start_date = '1999-01-01'
    freq = 'a'

    @property
    def url(self):
        return make_url(self.freq)

    def parse_response(self, response_text):
        df = read_csv(io.StringIO(response_text))
        gen = filter(is_valid, yield_all_dicts(df, self.freq))
        return list(gen)


class KEP_Qtr(KEP_Annual):
    """Quarterly data from KEP publication (Rosstat)"""
    freq = 'q'


class KEP_Monthly(KEP_Annual):
    """Monthly data from KEP publication (Rosstat)"""
    freq = 'm'


if __name__ == "__main__":  # pragma:  no cover
    u = KEP_Monthly(2016)
    u.extract()
    print(u.items[0])
