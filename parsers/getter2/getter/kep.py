import pandas as pd
import numpy as np

from parsers.getter2.base import ParserBase, format_value
import io

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
    negative_conditions = []
    # no datapoints with year, qtr or month - these are supplementary variables
    # we exclide them here
    negative_conditions.append(d['name'] in ['year', 'qtr', 'month'])
    # no NaN values
    negative_conditions.append(np.isnan(float(d['value'])))
    # are any negative conditions met?
    return not any(negative_conditions)


def yield_kep_dicts(freq):
    return filter(is_valid, yield_all_dicts(freq))


class KEP(ParserBase):
    """KEP dataset."""

    observation_start_date = '1999-01-01'
    freq = 'a'      
                                        
    @property
    def url(self):
        return make_url(self.freq)
    
    def parse_response(self, response_text):
        self.df = read_csv(io.StringIO(response_text))
        self.gen = list(yield_all_dicts(self.df, self.freq))
        gen = filter(is_valid, self.gen)
        return list(gen)

class KEP_Annual(KEP):
    freq = 'a'
    
class KEP_Monthly(KEP):
    freq = 'm'

class KEP_Qtr(KEP):
    freq = 'q'

if __name__ == "__main__":
    u = KEP_Monthly(2016)
    u.extract()
    print(u.items[0])

